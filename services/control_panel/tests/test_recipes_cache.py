"""Tests for the stat-signature cache in recipes_index.

Covers the cache primitives (_dir_signature / _cached / clear_cache) in
isolation, then the real load_recipes wiring (cache hit returns the same
list object; clear_cache forces a re-parse).
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from services.control_panel import recipes_index as ri
from services.control_panel.config import Config


class DirSignatureTest(unittest.TestCase):
    def test_missing_dir_is_empty(self):
        with TemporaryDirectory() as tmp:
            self.assertEqual(ri._dir_signature(Path(tmp) / "nope"), ())

    def test_stable_when_unchanged(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            self.assertEqual(ri._dir_signature(d), ri._dir_signature(d))

    def test_changes_when_file_added(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            before = ri._dir_signature(d)
            (d / "b.md").write_text("y")
            self.assertNotEqual(before, ri._dir_signature(d))

    def test_changes_when_content_changes(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            f = d / "a.md"
            f.write_text("short")
            before = ri._dir_signature(d)
            f.write_text("a much longer body than before")
            self.assertNotEqual(before, ri._dir_signature(d))

    def test_ignores_non_md(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            sig1 = ri._dir_signature(d)
            (d / "registry.json").write_text("{}")
            self.assertEqual(sig1, ri._dir_signature(d))


class CachedTest(unittest.TestCase):
    def setUp(self):
        ri.clear_cache()
        self.addCleanup(ri.clear_cache)

    def test_builder_runs_once_then_cached(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            calls = []

            def build():
                calls.append(1)
                return ["built"]

            r1 = ri._cached("k", d, build)
            r2 = ri._cached("k", d, build)
            self.assertEqual(calls, [1])
            self.assertIs(r1, r2)

    def test_rebuilds_after_change(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            calls = []

            def build():
                calls.append(1)
                return list(calls)

            ri._cached("k", d, build)
            (d / "b.md").write_text("y")
            ri._cached("k", d, build)
            self.assertEqual(len(calls), 2)

    def test_clear_cache_forces_rebuild(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            calls = []
            ri._cached("k", d, lambda: calls.append(1) or calls)
            ri.clear_cache()
            ri._cached("k", d, lambda: calls.append(1) or calls)
            self.assertEqual(len(calls), 2)

    def test_distinct_keys_are_independent(self):
        with TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "a.md").write_text("x")
            a = ri._cached("recipes", d, lambda: ["R"])
            b = ri._cached("connectors", d, lambda: ["C"])
            self.assertEqual((a, b), (["R"], ["C"]))


class LoadRecipesWiringTest(unittest.TestCase):
    def setUp(self):
        ri.clear_cache()
        self.addCleanup(ri.clear_cache)

    def test_second_call_is_cache_hit(self):
        cfg = Config.from_env()
        first = ri.load_recipes(cfg)
        second = ri.load_recipes(cfg)
        self.assertIs(first, second)
        self.assertTrue(first, "expected at least one recipe in the repo")

    def test_clear_cache_reparses(self):
        cfg = Config.from_env()
        first = ri.load_recipes(cfg)
        ri.clear_cache()
        second = ri.load_recipes(cfg)
        self.assertIsNot(first, second)
        self.assertEqual([r.id for r in first], [r.id for r in second])

    def test_connectors_cache_hit(self):
        cfg = Config.from_env()
        self.assertIs(ri.load_connectors(cfg), ri.load_connectors(cfg))


if __name__ == "__main__":
    unittest.main()
