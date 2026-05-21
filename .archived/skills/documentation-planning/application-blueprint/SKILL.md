---
name: application-blueprint
description: "Turn a raw application idea into a complete design dossier — vision, architecture, core domain, tech stack, infrastructure, security, feature roadmap, test strategy, and ADRs — ready to hand off to a per-feature pipeline."
risk: low
source: internal
date_added: "2026-05-21"
---

# Application Blueprint

Turn a raw application idea into a complete, reviewable design dossier. You
design; you do not build — no code, no scaffold, no directory tree, no
config files. The only files you write are the dossier documents described
below. The dossier is a *proposal for human review*, never an authority.

## The five-phase generation protocol

Work the phases in order. Each phase's output is the input context for the
next, so a settled architecture precedes everything that depends on it.

1. **Foundation.** From the `brief` (and any `constraints`), write
   `vision.md`: the problem, target users, goals, explicit non-goals,
   success metrics.
2. **Architecture.** Write `architecture.md` (system style, major
   components, data flow, cross-cutting patterns) and `core-domain.md`
   (entities, relationships, ubiquitous language, core business rules).
3. **Dependent design.** Write `tech-stack.md`, `infrastructure.md`, and
   `security.md` — each consistent with the Phase-2 architecture.
4. **Delivery.** Write `feature-roadmap.md` (prioritized, sized MVP feature
   list) and `test-strategy.md`.
5. **Synthesis.** Write one `adr/NNNN-<slug>.md` per significant decision
   surfaced in Phases 2–4, then write `overview.md` **last** — the thin
   index depends on every other doc being finished.

## The ten-artifact dossier

Write under the output directory (default `docs/app-design/`):

1. **`vision.md`** — problem · target users · goals · non-goals · success
   metrics.
2. **`architecture.md`** — system style (monolith / modular-monolith /
   services) · major components · data flow · cross-cutting patterns.
3. **`core-domain.md`** — entities · relationships · ubiquitous language ·
   core business rules.
4. **`tech-stack.md`** — language · framework · datastore · hosting; each
   choice with rationale and the alternatives rejected.
5. **`infrastructure.md`** — runtime · environments · containers/IaC plan ·
   CI/CD plan · external services.
6. **`security.md`** — auth model · secret handling · threat surface ·
   compliance needs.
7. **`feature-roadmap.md`** — the prioritized, sized MVP feature list; ends
   with the handoff block (below).
8. **`test-strategy.md`** — test pyramid · coverage targets · fixture and
   environment approach.
9. **`adr/NNNN-<slug>.md`** — one Architecture Decision Record per
   significant decision. Append-only (see ADR contract).
10. **`overview.md`** — thin synthesis: one paragraph on what the app is,
    the three load-bearing decisions, an index table linking the rest.
    Written last; hard cap ≤ ~40 lines / ~300 words — link, do not restate.

## `mode` input — checkpointed vs one-shot

- `mode` is `one-shot` only when it equals the literal string `"one-shot"`;
  any other value (including unset) is `checkpointed`.
- **checkpointed (default).** After Phase 2, Phase 3, and Phase 4, present
  the phase's artifacts and pause: wait for the user to type `Approve` (or
  give feedback to revise) before continuing. These are checkpoints A, B,
  and C. This mode is for an interactive harness.
- **one-shot.** Run all five phases straight through with no pauses.
- **Non-interactive fallback.** If `mode` is `checkpointed` but no
  interactive user is present (batch dispatch, scheduled run), treat an
  unanswered checkpoint as implicit approval and continue — never hang. The
  run still produces the full dossier.

## Doc ownership contract — the safety guarantee

Every dossier document carries the identical wrapper:

```
<!-- plan-application:owned:start -->
…regenerated each run…
<!-- plan-application:owned:end -->

## Revision log
- YYYY-MM-DD: first draft

## Notes
<!-- human-owned: the recipe never edits below this line -->
```

Rules — non-negotiable:

- Rewrite **only** the content between `owned:start` / `owned:end`.
- **Append** to "Revision log"; never rewrite a prior entry.
- Never read-modify-write anything at or below the `## Notes` header.
- **Missing markers** (a doc hand-created before this convention): do
  **not** clobber. Move the existing body under a
  `## Pre-existing (unmanaged)` heading and add a fresh managed block above
  it. Preserve-and-annotate, never overwrite.

## ADR contract

ADRs are **immutable once written**. A run may *add* `adr/NNNN-<slug>.md`
files using the next sequential number, but never edits an existing ADR's
body. A decision later reversed gets a **new** ADR that supersedes the old;
the only edit ever permitted to an existing ADR is flipping its status line
to `Status: Superseded by NNNN`. The decision history must stay honest.

Each ADR uses: `# NNNN. <title>` · `Status:` (Accepted | Superseded by …) ·
`## Context` · `## Decision` · `## Consequences`.

## Per-artifact owned-section templates

The wrapper is identical for all docs; the **inner shape** is fixed per
doc (a fixed shape keeps re-run diffs meaningful). Fill these in:

- **vision.md** — `### Problem` · `### Target users` · `### Goals` ·
  `### Non-goals` · `### Success metrics`.
- **architecture.md** — `### System style` (+ why) · `### Components`
  (table: component · responsibility · depends on) · `### Data flow` ·
  `### Cross-cutting patterns`.
- **core-domain.md** — `### Entities` (table: entity · key attributes ·
  relationships) · `### Ubiquitous language` (term · meaning) ·
  `### Core rules`.
- **tech-stack.md** — `### Language` · `### Framework` · `### Datastore` ·
  `### Hosting` — each as `choice — rationale — alternatives rejected`.
- **infrastructure.md** — `### Runtime` · `### Environments` ·
  `### Containers / IaC` · `### CI/CD` · `### External services`.
- **security.md** — `### Auth model` · `### Secret handling` ·
  `### Threat surface` · `### Compliance`.
- **feature-roadmap.md** — a table `| Feature | Priority | Size | Depends on |`
  ordered by priority, then the handoff block.
- **test-strategy.md** — `### Test pyramid` · `### Coverage targets` ·
  `### Fixtures & environments`.
- **overview.md** — `**What this is:**` one paragraph · `**Three decisions
  that matter:**` 3 bullets · an index table (`| Doc | Covers |`).

An absent doc is created from its template; an existing one has only its
owned block rewritten.

## Handoff rule

`feature-roadmap.md` must end with an explicit handoff block: state that
each MVP feature is to be run through `feature-kickoff` (or the project's
equivalent feature pipeline) to produce its spec / DB schema / API contract
/ sequence diagram. This recipe stops at the application tier — the
per-feature design work is the feature pipeline's job, not yours.

## Boundaries

- **Design only.** No code, no scaffold, no directory tree, no config
  files, no git operations. The only writes are the dossier under the
  output directory.
- **Empty / missing `brief`**: stop with a clear error — the brief is the
  sole design input; there is nothing to generate without it.
- **Greenfield.** There is no codebase to inspect; every artifact is
  generated from `brief` + `constraints`. The dossier is only as good as
  those inputs — frame every document as a reviewable proposal, and call
  out assumptions explicitly rather than presenting them as settled fact.
- **Re-run**: the ownership + ADR contracts govern — managed blocks
  rewritten, revision logs and prior ADRs and Notes preserved.

## Used by recipes
- `plan-application`
