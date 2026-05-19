# Design: `assess-workspace` recipe + `workspace-state-assessment` skill

- **Date:** 2026-05-19
- **Status:** Approved design — ready for implementation planning
- **Author:** brainstormed with the workspace owner

## Problem

There is no repeatable way to take a workspace (any repository, not just
this one) and produce a comprehensive, trustworthy picture of its current
state — what it does, what it is built with, how it runs, where it is
exposed — together with a prioritized list of what to do next. Doing this
by hand is inconsistent and goes stale. The output also needs to be
*verifiable on re-run*: a second pass must surface what drifted rather than
silently overwriting curated content.

## Scope

**Portable / generic.** The recipe and skill must work against any
repository with no assumptions about this workspace's structure. All
detection is heuristic (dependency manifests, lockfiles, CI configs,
container/IaC files, env files, test directories, README, license, git
history). It does not rely on `validate.py`, the recipe registry, or any
based-workspace-specific layout.

Out of scope: upgrading dependencies, opening issues, committing, or any
mutation of the codebase. The recipe surfaces; the human acts.

## Components & boundaries

Three units, each with one clear purpose:

| Unit | Purpose | Depends on |
|---|---|---|
| `recipes/assess-workspace.md` | Executable orchestration shell. Dispatches the agent, declares inputs/outputs, pulls in the skills. No judgement logic of its own. | the two skills below |
| `workspace-state-assessment` skill (new) | The methodology: the four-phase protocol, the detection heuristic catalog, the doc/ownership/drift contract, the gap taxonomy + severity rubric, the optional goal-lens. | nothing (self-contained prose) |
| `env-config` skill (existing, reused) | Supplies the security-axis rubric (.env hygiene, `.env.example` completeness, secret-handling, CI secret exposure) so the security doc does not restate it. | nothing |

**Recipe frontmatter (shape, not final wording):**

```yaml
id: assess-workspace
name: Assess Workspace State
description: >-
  Heuristically assess any repository — features, tech stack, infrastructure,
  security — and produce a maintained doc set plus a prioritized next-steps
  list, with drift surfaced on re-run.
audience: tech
status: experimental
cost: low
requires_human_review: false
tags: [assessment, documentation, planning, security]
requires_skills: [workspace-state-assessment, env-config]
requires_workflows: []
requires_connectors: []
requires_mcp: []
inputs:
  - name: scope
    type: string
    required: false
    description: Path subset to assess. Defaults to the repository root.
  - name: goal
    type: string
    required: false
    description: Free-text project intent. When present, next-steps.md adds a
      "Toward your goal" delta section on top of the objective gap list.
  - name: out_dir
    type: string
    required: false
    description: Output directory for the doc set. Defaults to docs/workspace-state/.
outputs:
  - name: docs
    type: markdown
    description: The six-file doc set under out_dir.
execution:
  type: agent
  # No `model:` — a portable recipe must not pin a local-only model id.
  # Omitting it makes the dispatcher resolve via $RECIPE_DEFAULT_MODEL
  # (envelope model > default_model > $RECIPE_DEFAULT_MODEL).
```

The skill lives at
`.archived/skills/documentation-planning/workspace-state-assessment/SKILL.md`
(category `documentation-planning` — it produces planning/state artifacts).

## Output: the six-doc set

Written under `out_dir` (default `docs/workspace-state/`):

1. **`overview.md`** — deliberately *thin* synthesis: one paragraph on what
   the project is, a maturity read, the top 3 things that matter most, and
   an index linking the other five docs. Regenerated every run. The skill
   prose enforces leanness explicitly: the `overview.md` owned section is
   capped (target ≤ ~40 lines / ~300 words) and must link rather than
   restate, so it cannot rot into a dumping ground.
2. **`features.md`** — first-class capability inventory: what the project
   actually does (user-facing and internal), grouped, each with the evidence
   that established it (entrypoint, route, command, module).
3. **`tech-stack.md`** — languages, frameworks, key dependencies, build
   tooling, plus a brief "structure" note (top-level module/dir layout). No
   separate architecture doc — that axis is too low-signal for a portable
   heuristic scan.
4. **`infrastructure.md`** — runtime, containers, IaC, CI/CD, services, data
   stores, deployment surface.
5. **`security.md`** — produced via the `env-config` rubric: secret/env
   hygiene, `.env.example` completeness, dependency risk, exposure.
6. **`next-steps.md`** — gap-driven, severity-ranked action list (taxonomy
   below), plus an optional "Toward your goal" section when `goal` is given.

## Four-phase agent protocol (prescribed by the new skill)

Phasing exists specifically so a portable agent does not lose coherence or
exhaust its iteration budget on a large, unfamiliar repo.

1. **Inventory (read-only).** Walk `scope`; collect raw signals: dependency
   manifests + lockfiles, CI/CD configs, container/IaC files, env files +
   `.env.example`, test directories, README, license, and a
   `git log --stat` summary. On large repos, *summarize* (counts, top-level
   structure, manifest contents) instead of dumping file bodies. The fact
   list is held in agent context; it is not a persisted artifact (no JSON
   manifest — the doc set is the only output).
2. **Classify.** Map the inventory into the four content domains and draft
   the owned-section content for `features.md`, `tech-stack.md`,
   `infrastructure.md`, `security.md` (security via the `env-config` rubric).
3. **Reconcile / drift.** For each content doc that already exists, read its
   current owned section, diff against the Phase-2 draft, and produce a
   dated "Drift since last run" entry describing what changed in reality.
   The human "Notes" zone is read but never modified.
4. **Synthesize.** Write `next-steps.md` from Phases 1–3 (gap-driven,
   severity-ranked, each item carrying its evidence); if `goal` is set, add
   a "Toward your goal" delta section. **Then** generate `overview.md` last,
   because the thin synthesis depends on the finished content docs and the
   top next-steps items.

## Doc ownership contract (the "nothing is off" mechanism)

Every doc has the same skeleton:

```
<!-- assess-workspace:owned:start -->
…regenerated every run…
<!-- assess-workspace:owned:end -->

## Drift since last run
- 2026-05-19: first assessment

## Notes
<!-- human-owned: the recipe never edits below this line -->
```

Agent contract, enforced by the skill prose:

- Rewrite **only** the content between `owned:start` / `owned:end`.
- **Append** to "Drift since last run"; never rewrite prior drift entries.
- Never read-modify-write anything at or below the `## Notes` header.
- **Missing markers** (doc hand-created before adopting this convention):
  do **not** clobber. Move the existing body under a
  `## Pre-existing (unmanaged)` heading and add a fresh managed block above
  it. This non-destructive rule is the core safety guarantee.

## next-steps.md gap taxonomy

Severity words intentionally match the `comprehensive-review` vocabulary for
cross-artifact consistency, **without** importing that skill.

| Severity | Triggers |
|---|---|
| **critical** | Secrets/credentials committed or in git history; env files not gitignored. |
| **high** | No CI; no test directory / zero tests; unpinned deps with no lockfile; no license when the repo is public. |
| **medium** | Stale or abandoned dependencies; containerized but no Dockerfile/healthcheck; no `.env.example`; thin or missing README. |
| **low** | No CONTRIBUTING; documentation staleness; missing status badges. |

Each item renders as:
`[severity] title — evidence: <fact or file> — suggested action`,
ordered by severity descending, then by domain.

## Error handling & boundaries

- **Read-only on the codebase.** The only writes are the six docs under
  `out_dir`. No commits, no issue creation, no dependency changes.
- **Empty / uninitialized repo:** still produce the doc set with
  "insufficient signal" owned sections; `next-steps.md` becomes "establish
  baseline" (git init, README, license, CI, tests…).
- **Missing `scope` path:** hard error with a clear message — never a
  silent empty run.
- **Large repo:** Phase 1 summarizes rather than dumping; this is the
  rationale for the phased protocol over a single pass.
- **Non-destructive guarantee:** absent ownership markers ⇒
  preserve-and-annotate, never overwrite.

## Testing — honest scope

This is primarily a methodology skill plus a thin agent recipe; there is no
deterministic agent behavior to unit-test, and the spec will not pretend
otherwise.

- The recipe must pass `scripts/recipe_manager.py lint` and the registry /
  generated-docs / Claude-Code / Antigravity sync checks that `validate.py`
  already enforces (recipe added to `recipes/registry.json`, regenerated
  docs in sync).
- The new skill body must be prompt-ready per existing convention:
  self-contained, provider-neutral, second-person/imperative, no first
  person, within the body-size norms other skills follow.
- A `python scripts/recipe_manager.py run assess-workspace --dry-run`
  smoke confirms the envelope assembles and both skills load.
- `validate.py` stays at its current check count — **no new code-test row**
  is added, because there is no new code module to test.
- Functional confidence comes from one live agent run against this
  repository plus at least one unrelated small repo, reviewed by hand.

## Open risks (acknowledged, accepted)

- Heuristic detection on exotic stacks will miss or mislabel things; the
  evidence-per-item rule keeps output auditable rather than authoritative.
- Agent non-determinism means two runs on an unchanged repo may word the
  owned sections differently; the drift section should distinguish
  *substantive* change from rewording (skill prose must call this out).
- `documentation-planning` is the chosen skill category; if a reviewer
  prefers `quality-documentation`, that is a cheap relocation, not a design
  change.
