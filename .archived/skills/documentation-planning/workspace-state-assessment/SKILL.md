---
name: workspace-state-assessment
description: "Heuristically assess any repository — features, tech stack, infrastructure, security — into a maintained six-doc set plus a prioritized next-steps list, with drift surfaced on re-run."
risk: low
source: internal
date_added: "2026-05-19"
---

# Workspace State Assessment

Turn any repository into a trustworthy, re-runnable picture of its current
state and what to do next. You inspect; you never mutate the codebase. The
only files you write are the six docs described below.

## The four-phase protocol

Work the phases in order. Phasing exists so you stay coherent and do not
exhaust your iteration budget on a large, unfamiliar repo.

1. **Inventory (read-only).** Walk the assessment scope. Collect raw
   signals only — do not judge yet:
   dependency manifests + lockfiles; CI/CD configs; container/IaC files;
   `.env*` and `.env.example`; test directories; `README`; `LICENSE`; and a
   `git log --stat` summary. On a large repo, **summarize** (file counts,
   top-level layout, manifest contents) — never dump file bodies. Hold the
   fact list in your working context; it is not a persisted artifact.
2. **Classify.** Map the inventory into the four content domains and draft
   the owned-section content for `features.md`, `tech-stack.md`,
   `infrastructure.md`, and `security.md` (security via the inlined rubric
   below).
3. **Reconcile / drift.** For each content doc that already exists, read
   its current owned section, diff it against your Phase-2 draft, and write
   one dated entry under "Drift since last run" describing what changed *in
   reality*. Only log substantive change — a reworded sentence that means
   the same thing is **not** drift and must not be logged.
4. **Synthesize.** Write `next-steps.md` from Phases 1–3 (gap-driven,
   severity-ranked, every item carrying its evidence); add a "Toward your
   goal" section only if a goal was supplied. **Then** write `overview.md`
   last — the thin synthesis depends on the finished content docs and the
   top next-steps items.

## The six-doc set

Write under the output directory (default `docs/workspace-state/`):

1. **`overview.md`** — thin synthesis: one paragraph on what the project
   is; a maturity read; a "top 3 that matter" list; an index table linking
   the other five docs. Hard cap ≤ ~40 lines / ~300 words — link, do not
   restate. Regenerated every run.
2. **`features.md`** — capability table grouped by area. Columns:
   capability · kind (user-facing / internal) · evidence
   (entrypoint / route / command / module).
3. **`tech-stack.md`** — fixed subsections: Languages · Frameworks &
   libraries · Build & tooling · Structure note (top-level layout). No
   architecture subsection — that axis is too low-signal for a heuristic
   scan.
4. **`infrastructure.md`** — fixed subsections: Runtime · Containers/IaC ·
   CI/CD · Services & data stores · Deployment surface.
5. **`security.md`** — the inlined security rubric headings, a `mode:`
   line, and (deep mode only) a "Vulnerability & supply-chain" block.
6. **`next-steps.md`** — a `mode:` line; the severity-ordered gap list; an
   optional "Toward your goal" section.

## Doc ownership contract — the safety guarantee

Every doc has the identical wrapper:

```
<!-- assess-workspace:owned:start -->
…regenerated every run…
<!-- assess-workspace:owned:end -->

## Drift since last run
- YYYY-MM-DD: first assessment

## Notes
<!-- human-owned: the recipe never edits below this line -->
```

Rules — non-negotiable:

- Rewrite **only** the content between `owned:start` / `owned:end`.
- **Append** to "Drift since last run"; never rewrite a prior entry.
- Never read-modify-write anything at or below the `## Notes` header.
- **Missing markers** (a doc hand-created before this convention): do
  **not** clobber. Move the existing body under a
  `## Pre-existing (unmanaged)` heading and add a fresh managed block
  above it. Preserve-and-annotate, never overwrite. This is the core
  "nothing is off" guarantee.

## Per-doc owned-section templates

The wrapper is identical for all six; the **inner shape** differs and is
fixed per doc (a fixed shape is what makes drift detection isolate
substantive change instead of rewording noise). Fill these in:

- **overview.md** — `**What this is:**` one paragraph · `**Maturity:**`
  one line · `**Top 3 that matter:**` 3 bullets · an index table
  (`| Doc | Covers |`) linking the other five.
- **features.md** — `### <Area>` headings, each with a table
  `| Capability | Kind | Evidence |`.
- **tech-stack.md** — `### Languages` · `### Frameworks & libraries` ·
  `### Build & tooling` · `### Structure note` (top-level dirs/modules).
- **infrastructure.md** — `### Runtime` · `### Containers / IaC` ·
  `### CI/CD` · `### Services & data stores` · `### Deployment surface`.
  Write "none detected" rather than omitting a subsection.
- **security.md** — `mode: lean|deep` · `### .env hygiene` ·
  `### Documentation` · `### Validation` · `### CI/CD` · (deep only)
  `### Vulnerability & supply-chain`.
- **next-steps.md** — `mode: lean|deep` · the severity-ordered list ·
  optional `## Toward your goal`.

An absent doc is created from its template; an existing one has only its
owned block rewritten to match the template.

## Inlined lean-mode security rubric

`security.md` in lean mode is produced from this rubric (it is inlined
here because `env-config` is a recipe, not a loadable skill):

| Area | Check |
|---|---|
| **.env hygiene** | `.env*` is gitignored; no real secrets in `.env.example`; no `.env` in git history (`git log -- .env`). |
| **Documentation** | Every code-referenced env var appears in `.env.example`; every `.env.example` var is still referenced (else dead). |
| **Validation** | Required vars validated fail-fast at startup, not a deep runtime `KeyError`. |
| **CI/CD** | Secrets come from the CI secret store, not committed files; no `echo $SECRET` / unmasked log patterns. |

Never print secret *values* — reference variable names only. If an area
does not apply (e.g. no CI yet), say so and skip it cleanly; do not
fabricate findings.

## next-steps.md gap taxonomy

Severity words match the `comprehensive-review` vocabulary deliberately,
for cross-artifact consistency.

| Severity | Triggers |
|---|---|
| **critical** | Secrets/credentials committed or in git history; `.env` not gitignored. |
| **high** | No CI; no tests / no test directory; unpinned deps with no lockfile; no license on a public repo. |
| **medium** | Stale/abandoned dependencies; containerized but no Dockerfile/healthcheck; no `.env.example`; thin/missing README. |
| **low** | No CONTRIBUTING; doc staleness; missing status badges. |

Render each item as
`[severity] title — evidence: <fact or file> — suggested action`,
ordered by severity descending, then by domain. Every item must carry
concrete evidence — a file, a command output, a manifest fact.

## Depth gate (`depth` input)

- `depth` is `deep` only when it equals the literal string `"deep"`; any
  other value (including unset) is `lean`.
- **lean**: the four phases exactly as above; `security.md` uses only the
  inlined rubric; you must **ignore** the presence of the
  `codebase-cleanup-deps-audit` and `security-audit` skills in context.
- **deep**: additionally apply `codebase-cleanup-deps-audit` (dependency
  CVEs, license / supply-chain) and `security-audit` (broader exposure)
  after Phase 2, feeding Phase 4. Enrich `security.md` with the
  "Vulnerability & supply-chain" block and add their evidence-backed
  findings to `next-steps.md`.
- Always write the actual `mode:` into `security.md` and `next-steps.md`.
  A lean→deep or deep→lean change is a **mode transition**, recorded as
  such in "Drift since last run" — never misreported as content drift.

## Boundaries

- Read-only on the codebase. The only writes are the six docs under the
  output directory. No commits, no issues, no dependency changes.
- Empty / uninitialized repo: still produce all six docs with
  "insufficient signal" owned sections; `next-steps.md` becomes
  "establish baseline" (git init, README, license, CI, tests…).
- Missing scope path: stop with a clear error — never a silent empty run.
- Heuristics on exotic stacks may mislabel; the evidence-per-item rule
  keeps every claim auditable rather than asserted.

## Used by recipes
- `assess-workspace`
