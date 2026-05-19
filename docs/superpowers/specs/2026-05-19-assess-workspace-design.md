# Design: `assess-workspace` recipe + `workspace-state-assessment` skill

- **Date:** 2026-05-19
- **Status:** Approved (2026-05-19, incl. per-doc templates + hybrid deep
  mode; `env-config` corrected skill→recipe, its rubric inlined) —
  implementation plan at
  `docs/superpowers/plans/2026-05-19-assess-workspace-plan.md`
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

Units, each with one clear purpose (the last is conditionally active):

| Unit | Purpose | Depends on |
|---|---|---|
| `recipes/assess-workspace.md` | Executable orchestration shell. Dispatches the agent, declares inputs/outputs, pulls in the skills. No judgement logic of its own. | the skills below |
| `workspace-state-assessment` skill (new) | The methodology: the four-phase protocol, the detection heuristic catalog, the doc/ownership/drift contract, the gap taxonomy + severity rubric, **the lean-mode security/env-hygiene rubric** (inlined — `env-config` is a *recipe*, not a loadable skill), the optional goal-lens. | nothing (self-contained prose) |
| `codebase-cleanup-deps-audit` + `security-audit` skills (existing, reused; **deep mode only**) | Supply the real vulnerability / supply-chain / tech-debt pass that `security.md` + `next-steps.md` perform when `depth: deep`. Inert in `lean` mode (loaded into context but the new skill's prose forbids invoking their methodology). | nothing |

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
requires_skills: [workspace-state-assessment,
  codebase-cleanup-deps-audit, security-audit]
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
  - name: depth
    type: string
    required: false
    description: >-
      "lean" (default) or "deep". lean = single-pass heuristic assessment.
      deep = additionally run codebase-cleanup-deps-audit + security-audit
      against security.md and next-steps.md for a real vulnerability /
      supply-chain / tech-debt pass. Any value other than "deep" is treated
      as "lean".
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
5. **`security.md`** — produced via the skill's inlined security rubric: secret/env
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
   `infrastructure.md`, `security.md` (security via the skill's inlined rubric).
3. **Reconcile / drift.** For each content doc that already exists, read its
   current owned section, diff against the Phase-2 draft, and produce a
   dated "Drift since last run" entry describing what changed in reality.
   The human "Notes" zone is read but never modified.
4. **Synthesize.** Write `next-steps.md` from Phases 1–3 (gap-driven,
   severity-ranked, each item carrying its evidence); if `goal` is set, add
   a "Toward your goal" delta section. **Then** generate `overview.md` last,
   because the thin synthesis depends on the finished content docs and the
   top next-steps items.

## Depth modes (`depth` input)

One recipe, two cost tiers — chosen over two near-duplicate recipes.

- **`lean` (default).** The four-phase protocol exactly as above. Pure
  heuristic inspection. `security.md` uses only the skill's inlined rubric.
  `next-steps.md` is gap-driven from the taxonomy. Fast; safe to schedule
  as a recurring Routine.
- **`deep`.** Adds a vulnerability/supply-chain/tech-debt pass *after*
  Phase 2 and feeding Phase 4: the agent applies `codebase-cleanup-deps-audit`
  (dependency CVEs, license/supply-chain risk) and `security-audit` (broader
  exposure) to enrich `security.md` and to add evidence-backed items to
  `next-steps.md`. Slower and more token-intensive; run on demand.

**Gating mechanism.** `requires_skills` loads all three skill bodies into
the agent context on *every* run — the runtime has no conditional
skill-loading. So the gate is **prose-level, in the new skill**: the
`workspace-state-assessment` skill states that `codebase-cleanup-deps-audit`
and `security-audit` are to be invoked *only* when `depth == "deep"`, and in
`lean` mode their presence in context must be ignored. Determinism of the
gate therefore rests on prompt adherence, not on the runtime — called out
again under Open risks.

**Mode echo.** Both `security.md` and `next-steps.md` record which mode
produced them (e.g. a `mode: deep` line inside the owned section) so a
reader can never mistake a lean pass for a deep one, and so the drift
section can flag a lean→deep or deep→lean transition rather than
misreporting it as content drift.

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

### Per-doc owned-section templates

The owned/drift/notes wrapper above is identical for all six docs. What
differs is the **inner shape of the owned section**, which is *prescribed
per doc by the new skill's prose* — not shipped as template files (a
portable recipe must not litter skeleton files into arbitrary target
repos; embedding the templates in the skill also versions them with the
methodology that reads them back for drift).

A fixed inner shape per doc is not cosmetic — it is what makes Phase-3
drift detection reliable: diffing two runs of a known table/section
structure isolates *substantive* change, whereas diffing free prose
mostly surfaces rewording noise.

Prescribed inner shapes (authored in the skill, summarized here):

- **`overview.md`** — one-paragraph "what this is" · maturity read ·
  "top 3 that matter" list · index table linking the other five docs.
  Hard length cap restated (≤ ~40 lines / ~300 words).
- **`features.md`** — capability table grouped by area; columns:
  capability · kind (user-facing/internal) · evidence (entrypoint/route/
  command/module).
- **`tech-stack.md`** — fixed subsections: Languages · Frameworks &
  libraries · Build & tooling · Structure note (top-level layout). No
  architecture subsection (axis deliberately cut).
- **`infrastructure.md`** — fixed subsections: Runtime · Containers/IaC ·
  CI/CD · Services & data stores · Deployment surface.
- **`security.md`** — the skill's inlined security-rubric headings
  (secret/env hygiene · `.env.example` completeness · secret-handling ·
  CI secret exposure), plus a `mode:` line and (in deep mode) a
  "Vulnerability & supply-chain" block.
- **`next-steps.md`** — `mode:` line · severity-ordered list rendered per
  the taxonomy below · optional "Toward your goal" section.

The skill states these as canonical examples the agent fills in; an
absent doc is created from its template, an existing one has only its
owned block rewritten to match.

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

## Considered and rejected reuse

The catalog was surveyed for skills covering the same axes. Recorded here
so this is not re-litigated:

| Skill(s) | Why not reused |
|---|---|
| `wiki-architect`, `wiki-onboarding`, `c4-architecture` / `c4-context` / `c4-code` | Each imposes its **own** output structure (wiki catalogue, C4 diagram set). That fights the fixed per-doc owned-section shape the drift contract depends on. `c4-*` would also reintroduce the standalone architecture artifact deliberately cut as low-signal for a portable heuristic scan. |
| `plan-writing` | Produces a dependency-ordered task plan; `next-steps.md` is a flat severity-ranked gap list. Wrong shape; would distort the artifact. |
| `comprehensive-review-full-review` | Severity **vocabulary** is matched intentionally for cross-artifact consistency, but the skill itself is not imported — pulling it in would drag a full code-review methodology into a state-assessment task. |
| `production-code-audit`, `codebase-audit-pre-push`, `codebase-cleanup-tech-debt` | Overlap the `deep` pass but are heavier/slower than needed; `codebase-cleanup-deps-audit` + `security-audit` were chosen as the leanest pair that still yields evidence-backed vulnerability/tech-debt findings. The others remain a future "deeper tier" option, not now (YAGNI). |

Reused: `codebase-cleanup-deps-audit` + `security-audit` (`deep` only).
**Not reused — `env-config`:** it is a *recipe*, not a loadable skill, so
it cannot appear in `requires_skills`; its lean security/env-hygiene
rubric is inlined into the new skill instead (the standalone `env-config`
recipe remains for users wanting a dedicated env audit). Net new: the
`workspace-state-assessment` skill + the `assess-workspace` recipe.

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
  smoke confirms the envelope assembles and **all three** skills load
  (`workspace-state-assessment`, `codebase-cleanup-deps-audit`,
  `security-audit`).
- Functional confidence additionally requires one live `depth: deep` run
  reviewed by hand — `lean` correctness does not exercise the gated path.
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
- **Deep-skill context cost on lean runs.** `requires_skills` is static, so
  `codebase-cleanup-deps-audit` + `security-audit` bodies occupy context on
  every `lean` run even though unused. Accepted: the UX of one recipe with a
  `depth` switch beats two near-duplicate recipes, and the bodies are
  bounded by the existing skill body-size norm.
- **Prose-only deep-mode gate.** The `lean`/`deep` boundary is enforced by
  skill prompt instructions, not the runtime. A model could in principle
  invoke the deep skills on a `lean` run. Mitigation: the new skill states
  the gate as a hard precondition and `security.md`/`next-steps.md` echo the
  `mode:` they ran under, so a mis-gated run is at least visible in the
  artifact rather than silent.
