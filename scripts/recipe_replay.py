#!/usr/bin/env python3
"""Run-Replay regression harness — re-dispatch stored runs and diff drift.

A "run" is one historical `dispatch_prompt`/`dispatch_agent` execution that
the Control Panel persisted to `.cache/control_panel.db`. This tool re-runs
the same recipe + inputs (optionally against a different model) and reports
how much the output drifted, on three axes:

  1. **Structural metrics** — char/line/word counts, top-level heading set,
     fenced-code-block count, error state. Cheap, deterministic.
  2. **Lexical similarity** — Jaccard over the lowercased word set. A single
     0..1 number that survives reordering but punishes wholesale rewrites.
  3. **Semantic equivalence (optional `--judge`)** — a local LLM scores
     0..100 whether the replay still does the job the baseline did. Off by
     default (costs a model call); injectable for tests.

Four subcommands:

  replay <run_id> [--model M]                 ad-hoc: one DB run, print diff
  replay-recent <recipe_id> --limit N [...]   ad-hoc: N recent DB runs
  baseline add <run_id> --suite P [...]       snapshot a DB run into a
                                              committed, self-contained suite
  replay-suite [--suite P] [--judge]          re-dispatch every suite case,
                                              compare vs the captured
                                              reference, exit 1 on regression

Why the suite captures the reference *inline*: `.cache/` is gitignored, so a
suite that merely referenced run-ids would be unreproducible on a fresh
checkout / in CI. `baseline add` therefore copies the historical output text
+ its metrics into the YAML, and `replay-suite` never touches the DB.

The core functions are import-clean (no `sys.exit`, transports injectable);
the CLI layer owns argument parsing, stdout, and exit codes.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils  # noqa: E402

ROOT_DIR = Path(utils.BASE_DIR)

# A "DispatchFn" re-runs a recipe and returns its full output text. Injected
# by tests so nothing hits the network; the default builds the real envelope
# and calls services.recipe_runtime.dispatcher.
DispatchFn = Callable[[str, dict, "str | None"], str]

# A "JudgeFn" scores semantic equivalence: (reference, candidate) -> (0..100,
# one-line reason). Injected by tests; the default asks a local LLM.
JudgeFn = Callable[[str, str], "tuple[int, str]"]


# --------------------------------------------------------------------------
# 1. Structural metrics + lexical similarity (pure, no I/O)
# --------------------------------------------------------------------------

_WORD_RE = re.compile(r"[a-z0-9]+")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
_FENCE_RE = re.compile(r"^\s*```")
_ERROR_MARKERS = ("[STUB]", "ERROR:", "Traceback (most recent call last)")


def structural_metrics(text: str) -> dict[str, Any]:
    """Cheap, deterministic shape of an output. `headings` is a sorted list
    (not a set) so it round-trips through JSON/YAML unchanged."""
    text = text or ""
    lines = text.splitlines()
    headings: list[str] = []
    fences = 0
    for line in lines:
        if _FENCE_RE.match(line):
            fences += 1
        m = _HEADING_RE.match(line.strip())
        if m:
            headings.append(m.group(2).strip().lower())
    return {
        "char_len": len(text),
        "line_count": len(lines),
        "word_count": len(_WORD_RE.findall(text.lower())),
        "headings": sorted(set(headings)),
        # Fences come in pairs; report whole blocks, rounding a dangling
        # open fence up so a truncated code block still registers.
        "code_blocks": (fences + 1) // 2,
        "errored": any(mark in text for mark in _ERROR_MARKERS),
    }


def jaccard_similarity(a: str, b: str) -> float:
    """|A∩B| / |A∪B| over lowercased word sets. 1.0 == identical vocabulary,
    0.0 == disjoint. Two empty strings count as identical (1.0)."""
    sa = set(_WORD_RE.findall((a or "").lower()))
    sb = set(_WORD_RE.findall((b or "").lower()))
    if not sa and not sb:
        return 1.0
    union = sa | sb
    if not union:
        return 1.0
    return len(sa & sb) / len(union)


def compare(reference: str, candidate: str) -> dict[str, Any]:
    """Full structural + lexical diff between a reference output and a
    candidate replay. Pure — no thresholds applied here; callers decide
    pass/fail from `jaccard` + the metric deltas."""
    ref_m = structural_metrics(reference)
    cand_m = structural_metrics(candidate)
    deltas = {
        "char_len": cand_m["char_len"] - ref_m["char_len"],
        "line_count": cand_m["line_count"] - ref_m["line_count"],
        "word_count": cand_m["word_count"] - ref_m["word_count"],
        "code_blocks": cand_m["code_blocks"] - ref_m["code_blocks"],
    }
    ref_h, cand_h = set(ref_m["headings"]), set(cand_m["headings"])
    return {
        "jaccard": round(jaccard_similarity(reference, candidate), 4),
        "reference_metrics": ref_m,
        "candidate_metrics": cand_m,
        "deltas": deltas,
        "headings_removed": sorted(ref_h - cand_h),
        "headings_added": sorted(cand_h - ref_h),
        # A replay that errors when the baseline didn't is the loudest signal
        # of regression — surfaced as its own flag, not buried in deltas.
        "new_error": cand_m["errored"] and not ref_m["errored"],
    }


# --------------------------------------------------------------------------
# 2. Re-dispatch (the real DispatchFn; injectable for tests)
# --------------------------------------------------------------------------


def _default_dispatch(recipe_id: str, inputs: dict, model: str | None) -> str:
    """Rebuild the recipe's envelope from disk and re-run it, capturing the
    full output as a string. Mirrors services.control_panel.runs._worker but
    synchronous and side-effect-free (no DB write, no streaming).

    Workflow recipes are intentionally unsupported — replaying them needs a
    live n8n and would mutate external state; we raise so the caller marks
    the case skipped rather than silently passing."""
    sys.path.insert(0, str(ROOT_DIR))
    from scripts import recipe_manager as rm
    from services.recipe_runtime import dispatcher
    from services.recipe_runtime.prompt_assembler import assemble

    target = rm.RECIPES_DIR / f"{recipe_id}.md"
    if not target.exists():
        raise FileNotFoundError(f"recipe not found: {recipe_id}")
    fm, body = rm.parse_recipe(target)
    etype = (fm.get("execution") or {}).get("type", "prompt")

    sink = io.StringIO()
    if etype == "workflow":
        raise NotImplementedError(
            f"workflow recipe {recipe_id!r} cannot be replayed offline"
        )
    if etype == "agent":
        agent_body = (
            rm._extract_section(body, "Agent")
            or rm._extract_section(body, "Prompt")
            or body
        )
        skill_bodies = rm._load_skill_bodies(list(fm.get("requires_skills") or []))
        if model:
            fm = {**fm, "execution": {**(fm.get("execution") or {}), "model": model}}
        dispatcher.dispatch_agent(
            fm, agent_body, inputs,
            workspace_root=str(ROOT_DIR),
            skill_bodies=skill_bodies,
            out=sink,
        )
        return sink.getvalue()

    prompt = (
        rm._extract_section(body, "Prompt")
        or rm._extract_section(body, "Agent")
        or body
    )
    envelope = assemble(fm, prompt, inputs)
    if model:
        envelope["model"] = model
    skill_bodies = rm._load_skill_bodies(envelope.get("skill_ids") or [])
    dispatcher.dispatch_prompt(
        envelope, skill_bodies=skill_bodies, out=sink, stream=True
    )
    return sink.getvalue()


# --------------------------------------------------------------------------
# 3. LLM judge (the real JudgeFn; injectable for tests)
# --------------------------------------------------------------------------

_JUDGE_SYSTEM = (
    "You are a regression judge. Given a BASELINE output and a CANDIDATE "
    "output produced by re-running the same task, decide whether the "
    "CANDIDATE still accomplishes what the BASELINE did. Ignore wording, "
    "ordering, and length differences; judge substance only. Reply with one "
    'line of strict JSON: {"score": <0-100 int>, "reason": "<short>"} where '
    "100 means semantically equivalent and 0 means it fails the task."
)

_JSON_OBJ_RE = re.compile(r"\{.*\}", re.DOTALL)


def _parse_judge_reply(raw: str) -> tuple[int, str]:
    """Extract {score, reason} from a possibly-chatty LLM reply. Falls back
    to score 0 with the raw text as the reason if nothing parses — an
    unparseable judge is treated as a regression, not a pass."""
    m = _JSON_OBJ_RE.search(raw or "")
    if not m:
        return 0, f"unparseable judge reply: {(raw or '')[:160]!r}"
    try:
        obj = json.loads(m.group(0))
        score = int(obj.get("score", 0))
        reason = str(obj.get("reason", "")).strip() or "(no reason given)"
        return max(0, min(100, score)), reason
    except (ValueError, TypeError):
        return 0, f"unparseable judge reply: {(raw or '')[:160]!r}"


def _default_judge(reference: str, candidate: str) -> tuple[int, str]:
    """Ask a local LLM whether `candidate` is still equivalent to
    `reference`. Model from $REPLAY_JUDGE_MODEL, else $RECIPE_DEFAULT_MODEL."""
    sys.path.insert(0, str(ROOT_DIR))
    from services.recipe_runtime import dispatcher

    model = os.environ.get("REPLAY_JUDGE_MODEL") or os.environ.get(
        "RECIPE_DEFAULT_MODEL"
    )
    if not model:
        raise RuntimeError(
            "no judge model: set REPLAY_JUDGE_MODEL or RECIPE_DEFAULT_MODEL"
        )
    user = (
        f"BASELINE:\n{reference}\n\n---\n\nCANDIDATE:\n{candidate}\n\n"
        "Respond with the JSON line only."
    )
    envelope = {
        "model": model,
        "skill_ids": [],
        "recipe_prelude": _JUDGE_SYSTEM,
        "user_message": user,
        "substitutions": {},
    }
    sink = io.StringIO()
    dispatcher.dispatch_prompt(envelope, out=sink, stream=False, temperature=0.0)
    return _parse_judge_reply(sink.getvalue())


# --------------------------------------------------------------------------
# 4. Suite model + I/O
# --------------------------------------------------------------------------

DEFAULT_SUITE = ROOT_DIR / "recipes" / "replay-suite.yaml"


@dataclass(frozen=True)
class ReplayCase:
    name: str
    recipe_id: str
    inputs: dict[str, str]
    model: str | None
    reference_output: str
    min_jaccard: float
    min_judge_score: int | None  # None => judge skipped for this case
    source_run_id: str | None


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml

    if not path.exists():
        return {"version": 1, "cases": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return data


def load_suite(path: Path) -> list[ReplayCase]:
    data = _load_yaml(path)
    cases: list[ReplayCase] = []
    for raw in data.get("cases") or []:
        thr = raw.get("thresholds") or {}
        ref = raw.get("reference") or {}
        cases.append(
            ReplayCase(
                name=str(raw["name"]),
                recipe_id=str(raw["recipe_id"]),
                inputs=dict(raw.get("inputs") or {}),
                model=raw.get("model"),
                reference_output=str(ref.get("output", "")),
                min_jaccard=float(thr.get("min_jaccard", 0.5)),
                min_judge_score=(
                    int(thr["min_judge_score"])
                    if thr.get("min_judge_score") is not None
                    else None
                ),
                source_run_id=raw.get("source_run_id"),
            )
        )
    return cases


def _case_to_dict(c: ReplayCase) -> dict[str, Any]:
    thresholds: dict[str, Any] = {"min_jaccard": c.min_jaccard}
    if c.min_judge_score is not None:
        thresholds["min_judge_score"] = c.min_judge_score
    return {
        "name": c.name,
        "recipe_id": c.recipe_id,
        "model": c.model,
        "source_run_id": c.source_run_id,
        "inputs": dict(c.inputs),
        "thresholds": thresholds,
        "reference": {
            "output": c.reference_output,
            "metrics": structural_metrics(c.reference_output),
        },
    }


def save_suite(path: Path, cases: list[ReplayCase]) -> None:
    import yaml

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = {"version": 1, "cases": [_case_to_dict(c) for c in cases]}
    path.write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


# --------------------------------------------------------------------------
# 5. DB access (read-only; only `baseline add` and ad-hoc replay touch it)
# --------------------------------------------------------------------------


def _load_run_row(run_id: str) -> Any:
    sys.path.insert(0, str(ROOT_DIR))
    from services.control_panel import db

    db.init(ROOT_DIR)
    row = db.get_run_row(run_id)
    if row is None:
        raise KeyError(f"run not found: {run_id}")
    return row


def _recent_run_rows(recipe_id: str, limit: int) -> list[Any]:
    sys.path.insert(0, str(ROOT_DIR))
    from services.control_panel import db

    db.init(ROOT_DIR)
    return db.recent_runs(limit=limit, recipe_id=recipe_id)


# --------------------------------------------------------------------------
# 6. Orchestration (pure-ish: takes injected fns, returns dicts)
# --------------------------------------------------------------------------


def replay_against_reference(
    recipe_id: str,
    inputs: dict,
    model: str | None,
    reference_output: str,
    *,
    dispatch_fn: DispatchFn | None = None,
    judge_fn: JudgeFn | None = None,
    min_jaccard: float = 0.5,
    min_judge_score: int | None = None,
) -> dict[str, Any]:
    """Re-dispatch one recipe and grade it against a known-good reference.

    Returns a result dict with `status` in {pass, regress, skip, error} and
    a `reasons` list explaining any non-pass. Never raises for an expected
    failure (workflow recipe, dispatch error) — those become skip/error
    statuses so a batch run keeps going."""
    dispatch = dispatch_fn or _default_dispatch
    try:
        candidate = dispatch(recipe_id, inputs, model)
    except NotImplementedError as e:
        return {"status": "skip", "reasons": [str(e)], "recipe_id": recipe_id}
    except Exception as e:  # noqa: BLE001 — a crashed dispatch is a result
        return {
            "status": "error",
            "reasons": [f"{type(e).__name__}: {e}"],
            "recipe_id": recipe_id,
        }

    diff = compare(reference_output, candidate)
    reasons: list[str] = []
    if diff["new_error"]:
        reasons.append("candidate emitted an error/stub marker; baseline did not")
    if diff["jaccard"] < min_jaccard:
        reasons.append(
            f"jaccard {diff['jaccard']:.3f} < min {min_jaccard:.3f}"
        )

    judge: dict[str, Any] | None = None
    if min_judge_score is not None:
        jf = judge_fn or _default_judge
        score, reason = jf(reference_output, candidate)
        judge = {"score": score, "reason": reason, "min": min_judge_score}
        if score < min_judge_score:
            reasons.append(
                f"judge {score} < min {min_judge_score} ({reason})"
            )

    return {
        "status": "regress" if reasons else "pass",
        "recipe_id": recipe_id,
        "reasons": reasons,
        "diff": diff,
        "judge": judge,
        "candidate_output": candidate,
    }


def run_suite(
    cases: list[ReplayCase],
    *,
    judge: bool = False,
    dispatch_fn: DispatchFn | None = None,
    judge_fn: JudgeFn | None = None,
) -> dict[str, Any]:
    """Grade every case. `judge=False` forces all judge thresholds off for
    this run (the per-case threshold still defines the *intent*; the CLI
    flag gates the cost). Returns an aggregate report; the caller maps
    `regressions > 0` to a non-zero exit."""
    results = []
    for c in cases:
        res = replay_against_reference(
            c.recipe_id,
            c.inputs,
            c.model,
            c.reference_output,
            dispatch_fn=dispatch_fn,
            judge_fn=judge_fn,
            min_jaccard=c.min_jaccard,
            min_judge_score=c.min_judge_score if judge else None,
        )
        res["name"] = c.name
        results.append(res)
    tally = {"pass": 0, "regress": 0, "skip": 0, "error": 0}
    for r in results:
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    return {
        "results": results,
        "tally": tally,
        # error counts as failure too — a recipe that no longer dispatches
        # is a regression by any useful definition.
        "regressions": tally["regress"] + tally["error"],
    }


# --------------------------------------------------------------------------
# 7. CLI
# --------------------------------------------------------------------------


def _print_diff(diff: dict[str, Any]) -> None:
    d = diff["deltas"]
    print(f"  jaccard      : {diff['jaccard']:.4f}")
    print(
        f"  Δ chars/lines/words : {d['char_len']:+d} / "
        f"{d['line_count']:+d} / {d['word_count']:+d}"
    )
    print(f"  Δ code blocks: {d['code_blocks']:+d}")
    if diff["headings_removed"]:
        print(f"  headings gone: {', '.join(diff['headings_removed'])}")
    if diff["headings_added"]:
        print(f"  headings new : {', '.join(diff['headings_added'])}")
    if diff["new_error"]:
        print("  !! candidate emitted an error/stub marker")


def cmd_replay(args: argparse.Namespace) -> int:
    try:
        row = _load_run_row(args.run_id)
    except KeyError as e:
        print(str(e))
        return 1
    print(f"replaying run {args.run_id}  recipe={row.recipe_id}  "
          f"model={args.model or row.model_ref}")
    res = replay_against_reference(
        row.recipe_id,
        dict(row.inputs),
        args.model or None,
        row.output,
        min_jaccard=args.min_jaccard,
    )
    print(f"  status       : {res['status'].upper()}")
    if res.get("diff"):
        _print_diff(res["diff"])
    for r in res["reasons"]:
        print(f"  - {r}")
    return 0 if res["status"] in ("pass", "skip") else 1


def cmd_replay_recent(args: argparse.Namespace) -> int:
    rows = _recent_run_rows(args.recipe_id, args.limit)
    if not rows:
        print(f"no stored runs for recipe {args.recipe_id!r}")
        return 1
    worst = 0
    for row in rows:
        res = replay_against_reference(
            row.recipe_id,
            dict(row.inputs),
            args.model or None,
            row.output,
            min_jaccard=args.min_jaccard,
        )
        jac = res.get("diff", {}).get("jaccard")
        jtxt = f"{jac:.3f}" if jac is not None else "  -  "
        print(f"  {row.id}  {res['status']:<7}  jaccard={jtxt}  "
              f"{'; '.join(res['reasons'])}")
        if res["status"] not in ("pass", "skip"):
            worst = 1
    return worst


def cmd_baseline_add(args: argparse.Namespace) -> int:
    try:
        row = _load_run_row(args.run_id)
    except KeyError as e:
        print(str(e))
        return 1
    if row.status != "done" or not row.output.strip():
        print(f"refusing to baseline run {args.run_id}: status={row.status!r}, "
              f"{len(row.output)} output chars — only completed runs with "
              "output make a useful reference.")
        return 1
    suite_path = Path(args.suite)
    cases = load_suite(suite_path)
    name = args.name or f"{row.recipe_id}-{row.id}"
    if any(c.name == name for c in cases):
        print(f"case {name!r} already in {suite_path} — pick --name or remove it")
        return 1
    cases.append(
        ReplayCase(
            name=name,
            recipe_id=row.recipe_id,
            inputs=dict(row.inputs),
            model=args.model or None,
            reference_output=row.output,
            min_jaccard=args.min_jaccard,
            min_judge_score=args.min_judge_score,
            source_run_id=row.id,
        )
    )
    save_suite(suite_path, cases)
    print(f"added case {name!r} ({row.recipe_id}, {len(row.output)} ref chars) "
          f"-> {suite_path}")
    return 0


def cmd_replay_suite(args: argparse.Namespace) -> int:
    suite_path = Path(args.suite)
    cases = load_suite(suite_path)
    if not cases:
        print(f"no cases in {suite_path} — add one with `baseline add`")
        return 1
    print(f"replay-suite: {len(cases)} case(s) from {suite_path}"
          f"{'  [judge on]' if args.judge else ''}")
    report = run_suite(cases, judge=args.judge)
    for r in report["results"]:
        jac = r.get("diff", {}).get("jaccard")
        jtxt = f"jaccard={jac:.3f}" if jac is not None else ""
        print(f"  [{r['status'].upper():^7}] {r['name']:<28} {jtxt}")
        for reason in r["reasons"]:
            print(f"            - {reason}")
    t = report["tally"]
    print(f"\n  pass={t['pass']} regress={t['regress']} "
          f"skip={t['skip']} error={t['error']}")
    if args.report:
        Path(args.report).write_text(
            json.dumps(report, indent=2, default=str), encoding="utf-8"
        )
        print(f"  report -> {args.report}")
    if report["regressions"]:
        print(f"\nFAIL — {report['regressions']} regression(s).")
        return 1
    print("\nOK — no regressions.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Run-Replay regression harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("replay", help="replay one stored run, print diff")
    pr.add_argument("run_id")
    pr.add_argument("--model", help="override model ref")
    pr.add_argument("--min-jaccard", type=float, default=0.5)
    pr.set_defaults(fn=cmd_replay)

    rr = sub.add_parser("replay-recent", help="replay N recent runs of a recipe")
    rr.add_argument("recipe_id")
    rr.add_argument("--limit", type=int, default=5)
    rr.add_argument("--model", help="override model ref")
    rr.add_argument("--min-jaccard", type=float, default=0.5)
    rr.set_defaults(fn=cmd_replay_recent)

    ba = sub.add_parser("baseline", help="manage the committed replay suite")
    ba_sub = ba.add_subparsers(dest="baseline_cmd", required=True)
    bad = ba_sub.add_parser("add", help="snapshot a stored run into the suite")
    bad.add_argument("run_id")
    bad.add_argument("--suite", default=str(DEFAULT_SUITE))
    bad.add_argument("--name", help="case name (default <recipe>-<run_id>)")
    bad.add_argument("--model", help="pin a model override for replays")
    bad.add_argument("--min-jaccard", type=float, default=0.5)
    bad.add_argument("--min-judge-score", type=int, default=None,
                     help="enable the LLM judge for this case at this floor")
    bad.set_defaults(fn=cmd_baseline_add)

    rs = sub.add_parser("replay-suite", help="run the suite, exit 1 on regress")
    rs.add_argument("--suite", default=str(DEFAULT_SUITE))
    rs.add_argument("--judge", action="store_true",
                    help="enable per-case LLM judge (costs a model call each)")
    rs.add_argument("--report", help="write the full JSON report to this path")
    rs.set_defaults(fn=cmd_replay_suite)

    args = p.parse_args(argv)
    return int(args.fn(args))


if __name__ == "__main__":
    sys.exit(main())
