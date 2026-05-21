# Design: `plan-application` recipe + `application-blueprint` skill

- **Date:** 2026-05-21
- **Status:** Approved design — pending implementation plan
- **Author:** brainstormed with the workspace owner

## Problem

Starting a new application from a raw idea is the point of highest leverage
and highest risk: the architecture, domain model, and tech-stack calls made
in the first hour constrain everything after. There is no repeatable way to
turn "I want to build X" into a complete, reviewable set of planning
artifacts. The vaulted `feature-kickoff` pipeline
(`.archived/_vault/workflows/custom-workflows/`) handles a *feature inside
an existing app* — spec → DB → API → sequence — but nothing covers the
*application* tier above it: vision, architecture, core domain, the MVP
feature list those per-feature pipelines then consume.

## Scope

**Planning artifacts only.** The recipe produces app-level design documents
and nothing else — no code, no project scaffold, no directory tree, no
config files. It ends by handing off: each MVP feature in the roadmap is to
be run through `feature-kickoff` (or the project's feature pipeline).

Out of scope: scaffolding, dependency installation, writing application or
test code, creating git repos. The recipe designs; the human (and the
feature pipeline) builds.

**Greenfield.** Unlike `assess-workspace`, there is no existing codebase to
inspect — every artifact is generated from the user's `brief` plus stated
`constraints`. Detection heuristics do not apply here.

## Relationship to `assess-workspace`

The two recipes are mirror images and deliberately rhyme:

| | `plan-application` | `assess-workspace` |
|---|---|---|
| Direction | write-once *creation* for a new app | read-only *audit* of an existing repo |
| Input | a raw idea (`brief`) | an existing repository |
| Doc contract | identical owned-section / drift / Notes wrapper | identical |

Because the doc wrapper is shared, an app planned by `plan-application`
can later be re-assessed by `assess-workspace` against the *same doc
shapes* once it has real code — the planning dossier and the live
assessment speak one vocabulary.

## Components & boundaries

| Unit | Purpose | Depends on |
|---|---|---|
| `recipes/plan-application.md` | Executable orchestration shell — declares inputs/outputs, pulls in the skill, frames the task. No methodology of its own. | the skill below |
| `application-blueprint` skill (new) | The methodology: the five-phase generation protocol, the ten artifact templates, the `mode` (checkpointed/one-shot) semantics, the doc-ownership + ADR contracts, the feature-roadmap handoff rule. | nothing (self-contained prose) |

The skill lives at
`.archived/skills/documentation-planning/application-blueprint/SKILL.md`
(category `documentation-planning` — it produces planning artifacts,
same category as `workspace-state-assessment`).

**Recipe frontmatter (shape, not final wording):**

```yaml
id: plan-application
name: Plan a New Application
description: >-
  Turn a raw application idea into a complete, reviewable design dossier —
  vision, architecture, core domain, tech stack, infrastructure, security,
  feature roadmap, test strategy, and ADRs — ready to hand off to the
  per-feature pipeline.
audience: tech
status: experimental
cost: low
requires_human_review: false
tags: [planning, architecture, design, application]
requires_skills: [application-blueprint]
requires_workflows: []
requires_connectors: []
requires_mcp: []
inputs:
  - name: brief
    type: string
    required: true
    description: The raw application idea / problem statement to design from.
  - name: constraints
    type: string
    required: false
    description: Tech preferences, team size, timeline, scale, compliance —
      anything that should bound the design.
  - name: mode
    type: string
    required: false
    description: '"checkpointed" (default) or "one-shot". checkpointed pauses
      for approval between phases; one-shot generates all artifacts in a
      single pass. Any value other than "one-shot" is treated as checkpointed.'
  - name: out_dir
    type: string
    required: false
    description: Output directory for the dossier. Defaults to docs/app-design/.
outputs:
  - name: dossier
    type: markdown
    description: The ~10-artifact design dossier under out_dir.
execution:
  type: agent
  # No `model:` — a portable recipe must not pin a local-only model id.
```

## Output: the design dossier

Written under `out_dir` (default `docs/app-design/`):

1. **`vision.md`** — problem, target users, goals, explicit non-goals,
   success metrics.
2. **`architecture.md`** — system style (monolith / modular-monolith /
   services), major components, data flow, key cross-cutting patterns.
3. **`core-domain.md`** — the domain model: entities, relationships,
   ubiquitous language, core business rules.
4. **`tech-stack.md`** — language / framework / datastore / hosting choices,
   each with rationale and the alternatives rejected.
5. **`infrastructure.md`** — runtime, environments, containers/IaC plan,
   CI/CD plan, external services.
6. **`security.md`** — auth model, secret handling, threat surface,
   compliance needs.
7. **`feature-roadmap.md`** — the MVP feature list, prioritized and sized;
   **the handoff list** — each feature is a `feature-kickoff` candidate.
8. **`test-strategy.md`** — test pyramid, coverage targets, fixture and
   environment approach.
9. **`adr/NNNN-<slug>.md`** — one Architecture Decision Record per
   significant decision surfaced in phases 2–4. Append-only.
10. **`overview.md`** — thin synthesis: one paragraph on what the app is,
    the three load-bearing decisions, an index table linking the rest.
    Written last; hard length cap (≤ ~40 lines / ~300 words).

## Five-phase generation protocol (prescribed by the skill)

Phasing exists so the architecture is settled before everything that
depends on it is written, and so checkpointed mode has natural pause
points.

| Phase | Produces | Checkpoint (checkpointed mode only) |
|---|---|---|
| 1 — Foundation | `vision.md` | — |
| 2 — Architecture | `architecture.md`, `core-domain.md` | **A** — approve before dependents |
| 3 — Dependent design | `tech-stack.md`, `infrastructure.md`, `security.md` | **B** |
| 4 — Delivery | `feature-roadmap.md`, `test-strategy.md` | **C** |
| 5 — Synthesis | `adr/NNNN-*.md`, then `overview.md` last | — |

Phase 3 artifacts depend on Phase 2's architecture; `overview.md` depends
on every other doc, so it is always written last.

## `mode` semantics

- **`checkpointed` (default).** At checkpoints A/B/C the agent presents the
  phase's artifacts and waits for the user to type `Approve` (or feedback)
  before continuing. Designed for an interactive harness — the Claude Code
  / Antigravity slash command.
- **`one-shot`.** No pauses; all five phases run straight through. Fully
  dispatchable via the recipe runtime and as a scheduled routine.
- **Non-interactive fallback.** When `mode` is `checkpointed` but the
  recipe is dispatched with no interactive user (recipe runtime, routine),
  an unanswered checkpoint is treated as **implicit approve** — the run
  degrades to one-shot behavior rather than hanging. The skill prose states
  this explicitly.
- `mode` is `one-shot` only when it equals the literal string `"one-shot"`;
  any other value (including unset) is `checkpointed`.

## Doc ownership contract

Every artifact carries the same wrapper as `assess-workspace`, so re-runs
update cleanly and the dossier is later re-assessable:

```
<!-- plan-application:owned:start -->
…regenerated each run…
<!-- plan-application:owned:end -->

## Revision log
- YYYY-MM-DD: first draft

## Notes
<!-- human-owned: the recipe never edits below this line -->
```

Rules (identical in spirit to `assess-workspace`):

- Rewrite **only** content between `owned:start` / `owned:end`.
- **Append** to "Revision log"; never rewrite a prior entry.
- Never touch anything at or below `## Notes`.
- **Missing markers**: preserve-and-annotate — move the existing body under
  `## Pre-existing (unmanaged)` and add a fresh managed block above it.
  Never clobber.

## ADR contract

ADRs are **immutable once written**. Each new run may *add* `adr/NNNN-*.md`
files (next sequential number) but never edits an existing ADR. A decision
that is later reversed gets a new ADR that supersedes the old one and marks
the old one `Status: Superseded by NNNN` — the only edit ever permitted to
an existing ADR is that one status line. This mirrors the append-only drift
log: the decision history must stay honest.

## Handoff

`feature-roadmap.md` ends with an explicit handoff block: each MVP feature
is to be run through `feature-kickoff` (or the project's equivalent feature
pipeline). `plan-application` deliberately stops at the application tier;
the per-feature spec/DB/API/sequence work is the feature pipeline's job.

## Error handling & boundaries

- **No codebase mutation.** The only writes are the dossier under `out_dir`.
  No scaffold, no code, no git operations.
- **Empty / missing `brief`**: hard error with a clear message — the brief
  is the sole design input; there is nothing to generate without it.
- **Re-run on an existing dossier**: the ownership contract governs —
  managed blocks are rewritten, the revision log appended, Notes and prior
  ADRs preserved.
- **Agent write-tool caveat** (carried forward from `assess-workspace`,
  not re-litigated): the recipe-runtime agent built-ins are read-only, so
  file-writing relies on the executing harness's Write tool. `plan-application`
  is therefore primarily a slash command; pure recipe-runtime dispatch is
  best-effort.

## Testing — honest scope

This is a methodology skill plus a thin agent recipe; there is no
deterministic agent behavior to unit-test.

- The recipe must pass `recipe_manager.py lint` and the registry /
  generated-docs / Claude-Code / Antigravity / cross-link sync checks
  `validate.py` enforces.
- The new skill body must be prompt-ready per convention: self-contained,
  provider-neutral, second-person / imperative, no first person, within the
  body-size norm of neighboring skills.
- `recipe_manager.py run plan-application --dry-run` confirms the envelope
  assembles and the skill loads.
- `validate.py` stays at its current check count — **no new code-test row**;
  there is no new code module.
- Functional confidence comes from one live `one-shot` run and one live
  `checkpointed` run, both hand-reviewed.

## Open risks (acknowledged, accepted)

- **Compounding wrong assumptions.** A wrong Phase-2 architecture call
  propagates into every dependent doc. `checkpointed` mode (the default)
  exists precisely to catch this at checkpoint A; `one-shot` trades that
  safety for batch-dispatchability.
- **Greenfield hallucination.** With no codebase to ground it, the design
  is only as good as the `brief` + `constraints`. The dossier is a
  *proposal* for human review, never an authority — the skill prose must
  frame it that way.
- **Checkpointed mode in a non-interactive context** degrades to one-shot
  silently. Accepted: the alternative (hanging) is worse, and the run still
  produces the full dossier.
- `documentation-planning` is the chosen skill category; relocation to
  another category is a cheap move, not a design change.
