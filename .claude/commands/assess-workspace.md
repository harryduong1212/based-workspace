---
description: Heuristically assess any repository — features, tech stack, infrastructure, security — into a maintained six-doc set plus a prioritized next-steps list, with drift surfaced on re-run.
argument-hint: [--input scope=<value>] [--input goal=<value>] [--input out_dir=<value>] [--input depth=<value>]
---

<!-- Generated from recipes/assess-workspace.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_claude_code.py`. -->

## What this does
Inspects a repository heuristically and produces a maintained six-doc set
(overview, features, tech-stack, infrastructure, security, next-steps) plus
a severity-ranked action list. Read-only — the only writes are the docs.
Re-runs surface what drifted rather than overwriting curated content.

## Who it's for
Anyone inheriting, auditing, or steering a codebase who needs an honest
current-state picture and a prioritized punch-list — and wants that picture
to stay trustworthy across re-runs.

## What you need
- A working checkout. Detection is heuristic (manifests, lockfiles, CI
  configs, container/IaC, `.env*`, test dirs, README, license, git log).
- For `depth=deep`: nothing extra — the deep skills load automatically.

## How to run
- **In Antigravity or Claude Code:** say *"assess this workspace"* or run
  `/assess-workspace`.
- **CLI (lean):** `python scripts/recipe_manager.py run assess-workspace`
- **CLI (deep, scoped, goal):**
  `python scripts/recipe_manager.py run assess-workspace --input depth=deep --input scope=services/ --input goal="ship a public beta"`

## Example output

> **docs/workspace-state/overview.md**
>
> <!-- assess-workspace:owned:start -->
> **What this is:** A FastAPI control panel + recipe runtime for an
> AI-workflow workspace.
> **Maturity:** Active, pre-1.0; CI green, partial test coverage.
> **Top 3 that matter:** (1) no license on a public repo (high);
> (2) `.env` once committed in history (critical); (3) thin README.
>
> | Doc | Covers |
> |---|---|
> | features.md | What it does, with evidence |
> | next-steps.md | 7 ranked actions |
> <!-- assess-workspace:owned:end -->
>
> ## Drift since last run
> - 2026-05-19: first assessment

## Agent

You are running the `assess-workspace` recipe. The
`workspace-state-assessment` skill owns the full methodology — the
four-phase protocol, the six-doc set, the owned-section / drift contract,
the per-doc templates, the gap taxonomy, the inlined security rubric, and
the depth gate. Follow it exactly. Do not restate it here.

Inputs bound for this run:

- `scope` = `{input.scope}` — assess this path subset; default is the
  repository root. If a non-empty scope path does not exist, stop with a
  clear error.
- `goal` = `{input.goal}` — if non-empty, add the "Toward your goal"
  section to `next-steps.md`.
- `out_dir` = `{input.out_dir}` — write the six docs here; default
  `docs/workspace-state/`.
- `depth` = `{input.depth}` — apply the skill's depth gate. Treat any
  value other than the literal `deep` as `lean`.

Hard boundary: this recipe is **read-only on the codebase**. The only
files you may write are the six docs under `out_dir`. No commits, no
issues, no dependency or source changes. Honor the missing-marker
preserve-and-annotate rule — never clobber a pre-existing doc.
