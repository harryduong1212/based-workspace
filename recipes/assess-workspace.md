---
id: assess-workspace
name: Assess Workspace State
description: >-
  Heuristically assess any repository — features, tech stack, infrastructure,
  security — into a maintained six-doc set plus a prioritized next-steps
  list, with drift surfaced on re-run.
audience: tech
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [assessment, documentation, planning, security]

about: >-
  Produces a trustworthy, re-runnable picture of any repo's current state:
  what it does, what it's built with, how it runs, where it's exposed —
  plus a severity-ranked list of what to do next. Read-only; the only
  output is the six-doc set. A second run surfaces what drifted instead of
  silently overwriting curated content. Portable — no assumptions about
  this workspace's layout. Set `depth=deep` to add a real
  vulnerability / supply-chain / tech-debt pass.
highlights:
  - Six maintained docs — overview, features, tech-stack, infrastructure, security, next-steps
  - Owned-section contract — re-runs surface drift, never clobber human notes
  - Portable — heuristic detection, works on any repository
  - Optional deep mode — dependency CVEs + broader security audit
examples:
  - label: Lean assessment of the current repo
    code: "claude /assess-workspace"
  - label: Deep assessment with a goal lens
    code: "python scripts/recipe_manager.py run assess-workspace --input depth=deep --input goal='ship a public beta'"

requires_skills:
  - workspace-state-assessment
  - codebase-cleanup-deps-audit
  - security-audit
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env: []

triggers:
  cli: assess-workspace
  chat:
    - "assess this workspace"
    - "what's the state of this project"

inputs:
  - name: scope
    type: string
    required: false
    description: Path subset to assess. Defaults to the repository root.
  - name: goal
    type: string
    required: false
    description: >-
      Free-text project intent. When present, next-steps.md adds a
      "Toward your goal" section on top of the objective gap list.
  - name: out_dir
    type: string
    required: false
    description: Output directory for the doc set. Defaults to docs/workspace-state/.
  - name: depth
    type: string
    required: false
    description: >-
      "lean" (default) or "deep". deep additionally runs
      codebase-cleanup-deps-audit + security-audit against security.md and
      next-steps.md. Any value other than "deep" is treated as "lean".

outputs:
  - name: docs
    type: markdown
    description: The six-file doc set under out_dir (overview, features, tech-stack, infrastructure, security, next-steps).

execution:
  type: agent
---

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
