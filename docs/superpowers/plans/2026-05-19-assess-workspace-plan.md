# Implementation Plan: `assess-workspace` recipe + `workspace-state-assessment` skill

- **Date:** 2026-05-19
- **Spec:** `docs/superpowers/specs/2026-05-19-assess-workspace-design.md` (Approved)
- **Status:** Ready to execute

## Nature of this work

No new code module. The deliverables are two prose artifacts (one skill,
one recipe) plus registry/generated-doc bookkeeping. "Tests" are the
existing `validate.py` sync/lint gates plus hand-reviewed live runs.
Therefore the plan is sequenced by *artifact*, not by code layers, and
each step ends at a `validate.py`-checkable state.

## Registration mechanics (verified against the repo)

- `recipes/registry.json` is **generated** — `python scripts/recipe_manager.py sync`
  regenerates it from recipe frontmatter. Never hand-edit it.
- Skill **category** registries (`.archived/skills/<category>/registry.json`,
  `skills[]` array) are **hand-maintained** — `archive_manager.py` only
  prunes/vaults, it has no "add". The new skill needs a manual entry.
- The top-level `.archived/skills/registry.json` lists *categories only*;
  `documentation-planning` already exists → no change there.
- `sync_claude_code.py`, `sync_antigravity.py`, `docs_generator.py`,
  `cross_link.py` generate downstream artifacts from recipes; their
  `--check` variants in `validate.py` fail unless regenerated. Each must be
  run (non-`--check`) after the recipe lands.

## Step 1 — Author the skill

**File:** `.archived/skills/documentation-planning/workspace-state-assessment/SKILL.md`

Frontmatter (match sibling skills' shape — `name`, `description`, `risk`,
`source`, `date_added`; `risk: low`, `source: internal`).

Body must encode, in provider-neutral second-person/imperative prose, no
first person, within the body-size norm of other skills:

1. The **four-phase protocol** (Inventory → Classify → Reconcile/drift →
   Synthesize), including the large-repo "summarize, don't dump" rule and
   why `overview.md` is written last.
2. The **detection heuristic catalog** (manifests, lockfiles, CI configs,
   container/IaC, env files, test dirs, README, license, `git log --stat`).
3. The **doc ownership contract** verbatim: the `owned:start/end` +
   `Drift since last run` + `Notes` skeleton, the append-only drift rule,
   the never-touch-Notes rule, and the **missing-marker
   preserve-and-annotate** safety rule.
4. The **six per-doc owned-section templates** as canonical fill-in
   examples (the inner shapes enumerated in the spec's "Per-doc
   owned-section templates").
5. The **gap taxonomy + severity rubric** (critical/high/medium/low
   triggers; `[severity] title — evidence — action` render; ordering).
6. The **depth gate**: `codebase-cleanup-deps-audit` + `security-audit` are
   invoked **only** when `depth == "deep"`; in `lean` their presence in
   context must be ignored; `security.md`/`next-steps.md` echo a `mode:`
   line; the drift section must treat a mode change as a mode transition,
   not content drift.
7. The **substantive-vs-rewording** instruction for drift (only log
   meaning changes, not paraphrase).

**Exit check:** body adheres to the prompt-ready convention used by
neighboring skills (skim two siblings for length/voice calibration).

## Step 2 — Register the skill

Add an entry to `.archived/skills/documentation-planning/registry.json`
`skills[]` (shape per existing `github-issue-creator` entry: `id`,
`description`, `path`, `tags`, `trigger_conditions`, `anti_triggers`,
`dependencies`, `mcp_tools`). `dependencies: []`, `mcp_tools: []`.

## Step 3 — Author the recipe

**File:** `recipes/assess-workspace.md`

Frontmatter exactly as the spec's "Recipe frontmatter" block, including:
`requires_skills: [workspace-state-assessment, env-config,
codebase-cleanup-deps-audit, security-audit]`, the four inputs (`scope`,
`goal`, `out_dir`, `depth`), the `docs` output, `execution.type: agent`
with **no `model:`** (portability), `requires_human_review: false`.

Body: a `## Agent` section that is a thin orchestration brief —
restating inputs, pointing at the skill-owned protocol, and the
read-only/no-mutation boundary. No methodology duplicated from the skill
(the skill owns judgement; the recipe owns task framing — per the
`skill-recipe-vocab-convention` memory).

## Step 4 — Regenerate downstream artifacts

In order:

1. `python scripts/recipe_manager.py sync` — regenerate `recipes/registry.json`.
2. `python scripts/docs_generator.py` — regenerate generated docs.
3. `python scripts/sync_antigravity.py` — regenerate workflows.
4. `python scripts/sync_claude_code.py` — regenerate `.claude/commands/`.
5. `python scripts/cross_link.py` — refresh backrefs.

## Step 5 — Lint + validate

1. `python scripts/recipe_manager.py lint` (expect clean — the four
   `requires_skills` must all resolve; this is the first place a typo'd
   skill id or unregistered skill surfaces).
2. `python scripts/recipe_manager.py run assess-workspace --dry-run` —
   confirms the envelope assembles and **all four** skill bodies load.
3. `python scripts/validate.py` — full suite. Expectation: **16/16, check
   count unchanged** (no new code-test row; spec is explicit about this).
   Any FAIL here is a sync step missed in Step 4 or a lint issue in Step 5.1.

## Step 6 — Commit

One commit: skill + skill-registry entry + recipe + all regenerated
artifacts together (they are one logical unit; splitting would leave
`validate.py` red between commits). Conventional Commits:
`feat(recipe): assess-workspace + workspace-state-assessment skill`.
Push.

## Step 7 — Live verification (infra-gated — deferred to a stack-up session)

Per the spec's honest-testing scope, functional confidence needs hand
review, which requires the local LLM stack:

1. `lean` run against this repo → review the six docs in `out_dir`.
2. `lean` run against one unrelated small repo → confirm portability (no
   based-workspace assumptions leaked).
3. `deep` run against this repo → confirm the gated `codebase-cleanup-deps-audit`
   + `security-audit` path fires and `security.md`/`next-steps.md` show
   `mode: deep`.
4. Re-run `lean` on this repo unchanged → confirm the "Drift since last
   run" entry reports *no substantive change* (rewording must not register
   as drift) — this is the core verifiable property of the whole design.

Steps 1–6 are pure-code/prose and can be done now. Step 7 is gated on the
LLM stack being up and is the only part that proves behavior rather than
wiring.

## Risk-to-step traceability

| Spec open risk | Caught/contained at |
|---|---|
| Heuristic mislabels exotic stacks | Step 7.2 (unrelated repo review) |
| Agent non-determinism / rewording-as-drift | Step 7.4 (unchanged re-run) |
| Deep-skill context cost on lean runs | Step 5.2 (dry-run shows total system bytes) |
| Prose-only deep-mode gate | Step 7.1 vs 7.3 (`mode:` echo differs) |
| Skill category placement | Step 5.1 (lint resolves the path) |
