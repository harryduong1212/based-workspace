"""Tests for scripts.recipe_replay.

Covers the pure layer (metrics, jaccard, compare), suite YAML round-trip,
and orchestration (replay_against_reference / run_suite) with injected fake
dispatch + judge fns so nothing touches the DB or the network.
"""

import tempfile
import unittest
from pathlib import Path

from scripts.recipe_replay import (
    ReplayCase,
    compare,
    jaccard_similarity,
    load_suite,
    replay_against_reference,
    run_suite,
    save_suite,
    structural_metrics,
    _parse_judge_reply,
)


class StructuralMetricsTest(unittest.TestCase):
    def test_counts_and_headings(self):
        text = "# Title\nsome words here\n## Sub\n```\ncode\n```\nmore\n"
        m = structural_metrics(text)
        self.assertEqual(m["headings"], ["sub", "title"])
        self.assertEqual(m["code_blocks"], 1)
        self.assertFalse(m["errored"])
        self.assertEqual(m["line_count"], 7)
        self.assertGreater(m["word_count"], 0)

    def test_empty_text(self):
        m = structural_metrics("")
        self.assertEqual(m["char_len"], 0)
        self.assertEqual(m["headings"], [])
        self.assertEqual(m["code_blocks"], 0)

    def test_error_marker_detected(self):
        self.assertTrue(structural_metrics("oops\nERROR: boom")["errored"])
        self.assertTrue(structural_metrics("[STUB] not wired")["errored"])

    def test_dangling_fence_rounds_up(self):
        self.assertEqual(structural_metrics("```\ncode never closed")["code_blocks"], 1)


class JaccardTest(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(jaccard_similarity("a b c", "c b a"), 1.0)

    def test_disjoint(self):
        self.assertEqual(jaccard_similarity("a b", "c d"), 0.0)

    def test_both_empty_is_one(self):
        self.assertEqual(jaccard_similarity("", ""), 1.0)

    def test_partial(self):
        # {a,b,c} vs {b,c,d} -> 2/4
        self.assertEqual(jaccard_similarity("a b c", "b c d"), 0.5)


class CompareTest(unittest.TestCase):
    def test_detects_new_error_and_heading_drift(self):
        ref = "# Report\nall good here\n"
        cand = "# Summary\nERROR: failed\n"
        diff = compare(ref, cand)
        self.assertTrue(diff["new_error"])
        self.assertIn("report", diff["headings_removed"])
        self.assertIn("summary", diff["headings_added"])
        self.assertLess(diff["jaccard"], 1.0)

    def test_no_error_when_baseline_also_errored(self):
        diff = compare("ERROR: a", "ERROR: b")
        self.assertFalse(diff["new_error"])


class SuiteRoundTripTest(unittest.TestCase):
    def test_save_then_load(self):
        case = ReplayCase(
            name="c1",
            recipe_id="code-review",
            inputs={"target": "src/x.py"},
            model="local/gemma-3-4b",
            reference_output="# Review\nlooks fine\n",
            min_jaccard=0.6,
            min_judge_score=70,
            source_run_id="abc123",
        )
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "suite.yaml"
            save_suite(p, [case])
            loaded = load_suite(p)
        self.assertEqual(len(loaded), 1)
        got = loaded[0]
        self.assertEqual(got.name, "c1")
        self.assertEqual(got.recipe_id, "code-review")
        self.assertEqual(got.inputs, {"target": "src/x.py"})
        self.assertEqual(got.min_jaccard, 0.6)
        self.assertEqual(got.min_judge_score, 70)
        self.assertEqual(got.reference_output, "# Review\nlooks fine\n")

    def test_missing_file_is_empty_suite(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_suite(Path(tmp) / "nope.yaml"), [])

    def test_judge_omitted_when_threshold_unset(self):
        case = ReplayCase("c", "r", {}, None, "out", 0.5, None, None)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "s.yaml"
            save_suite(p, [case])
            self.assertNotIn("min_judge_score", p.read_text())
            self.assertIsNone(load_suite(p)[0].min_judge_score)


class JudgeReplyParseTest(unittest.TestCase):
    def test_clean_json(self):
        self.assertEqual(_parse_judge_reply('{"score": 88, "reason": "ok"}'), (88, "ok"))

    def test_chatty_wrapper(self):
        s, r = _parse_judge_reply('Sure!\n{"score": 42, "reason": "drifted"} done')
        self.assertEqual((s, r), (42, "drifted"))

    def test_clamped(self):
        self.assertEqual(_parse_judge_reply('{"score": 999, "reason": "x"}')[0], 100)

    def test_unparseable_is_zero(self):
        self.assertEqual(_parse_judge_reply("no json at all")[0], 0)


class ReplayAgainstReferenceTest(unittest.TestCase):
    def test_pass_when_similar(self):
        ref = "the quick brown fox jumps over the lazy dog"
        res = replay_against_reference(
            "r", {}, None, ref,
            dispatch_fn=lambda *_: ref,
            min_jaccard=0.5,
        )
        self.assertEqual(res["status"], "pass")
        self.assertEqual(res["reasons"], [])

    def test_regress_on_low_jaccard(self):
        res = replay_against_reference(
            "r", {}, None, "alpha beta gamma delta",
            dispatch_fn=lambda *_: "totally different words entirely",
            min_jaccard=0.5,
        )
        self.assertEqual(res["status"], "regress")
        self.assertTrue(any("jaccard" in x for x in res["reasons"]))

    def test_regress_on_new_error(self):
        res = replay_against_reference(
            "r", {}, None, "all fine",
            dispatch_fn=lambda *_: "all fine ERROR: boom",
            min_jaccard=0.0,
        )
        self.assertEqual(res["status"], "regress")
        self.assertTrue(any("error" in x for x in res["reasons"]))

    def test_workflow_recipe_skips(self):
        def boom(*_):
            raise NotImplementedError("workflow cannot replay offline")
        res = replay_against_reference("r", {}, None, "x", dispatch_fn=boom)
        self.assertEqual(res["status"], "skip")

    def test_dispatch_crash_is_error_status(self):
        def boom(*_):
            raise RuntimeError("model unreachable")
        res = replay_against_reference("r", {}, None, "x", dispatch_fn=boom)
        self.assertEqual(res["status"], "error")
        self.assertIn("RuntimeError", res["reasons"][0])

    def test_judge_gate(self):
        ref = "same words same words"
        res = replay_against_reference(
            "r", {}, None, ref,
            dispatch_fn=lambda *_: ref,
            judge_fn=lambda a, b: (10, "not equivalent"),
            min_jaccard=0.0,
            min_judge_score=70,
        )
        self.assertEqual(res["status"], "regress")
        self.assertEqual(res["judge"]["score"], 10)

    def test_judge_skipped_when_threshold_none(self):
        called = []
        replay_against_reference(
            "r", {}, None, "x y z",
            dispatch_fn=lambda *_: "x y z",
            judge_fn=lambda a, b: called.append(1) or (0, ""),
            min_jaccard=0.0,
            min_judge_score=None,
        )
        self.assertEqual(called, [])


class RunSuiteTest(unittest.TestCase):
    def _cases(self):
        return [
            ReplayCase("good", "r1", {}, None, "alpha beta gamma", 0.5, None, None),
            ReplayCase("bad", "r2", {}, None, "alpha beta gamma", 0.9, None, None),
        ]

    def test_tally_and_regressions(self):
        def disp(rid, _inp, _m):
            return "alpha beta gamma" if rid == "r1" else "wholly unrelated text"
        report = run_suite(self._cases(), dispatch_fn=disp)
        self.assertEqual(report["tally"]["pass"], 1)
        self.assertEqual(report["tally"]["regress"], 1)
        self.assertEqual(report["regressions"], 1)

    def test_judge_flag_gates_cost(self):
        seen = []
        cases = [ReplayCase("c", "r", {}, None, "a b c", 0.0, 70, None)]
        run_suite(
            cases,
            judge=False,
            dispatch_fn=lambda *_: "a b c",
            judge_fn=lambda a, b: seen.append(1) or (0, ""),
        )
        self.assertEqual(seen, [])  # judge=False suppresses the call

    def test_error_counts_as_regression(self):
        def disp(*_):
            raise RuntimeError("down")
        cases = [ReplayCase("c", "r", {}, None, "x", 0.5, None, None)]
        report = run_suite(cases, dispatch_fn=disp)
        self.assertEqual(report["regressions"], 1)
        self.assertEqual(report["tally"]["error"], 1)


if __name__ == "__main__":
    unittest.main()
