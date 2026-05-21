# Implementation Plan: `create-app` recipe family

- **Date:** 2026-05-21
- **Spec:** `docs/superpowers/specs/2026-05-21-create-app-family-design.md` (Approved)
- **Status:** Ready to execute

## Nature of this work

Mix: one real code prerequisite (the write tool + `write_root` plumbing,
the only deterministic-testable part), then three prose artifact pairs
(recipe + skill, one per phase) + bookkeeping. The plan is sequenced
**code-prerequisite first**, then artifact authoring, then validate +
commit. Live verification is the only behavior proof and is
infra/cost-gated (agent-quality work — really wants Claude Sonnet or
Gemini Pro to be honest).

## Phase 1 — Code prerequisite: write tool + `write_root` plumbing

This is the only part with deterministic unit tests, and the rest of the
plan can't proceed without it.

### Step 1.1 — Add `write_workspace_file` built-in tool

**File:** `services/recipe_runtime/agent_tools.py`

- Add to `BUILT_IN_TOOLS` dict alongside `get_current_time` and
  `read_workspace_file`.
- Signature (Anthropic tool shape):
  - `name: "write_workspace_file"`
  - `description: "Write a UTF-8 text file under the write root. Refuses path escape; refuses overwrite unless force=true. Returns a one-line status string."`
  - `input_schema: { path: string (required, relative to write_root), content: string (required), force: bool (optional, default false) }`
- Implementation function `_write_workspace_file(args, *, write_root)`:
  - Resolve `path` relative to `write_root` using `Path.resolve()` and
    verify the resolved path is inside `write_root` (the same containment
    check `read_workspace_file` uses).
  - If the target file exists and `force` is not true → return
    `"error: file already exists at <rel>; pass force=true to overwrite"`.
  - Otherwise create parent dirs (`parents=True, exist_ok=True`) and write
    UTF-8 content. Return `"wrote <rel> (<N> bytes)"`.
  - All errors are *returned strings* — never raise into the agent loop
    (mirrors the `read_workspace_file` pattern).

### Step 1.2 — Thread `write_root` through `ToolRuntime`

**File:** `services/recipe_runtime/agent_tools.py`

- Add `write_root: Path | None` param to `build_tool_runtime(fm,
  workspace_root=..., write_root=None)`. If `None`, default to
  `workspace_root` (preserves existing read-only recipes' behavior
  including `assess-workspace`).
- Store on the `ToolRuntime` instance as `self._write_root`.
- `ToolRuntime.invoke(name, args)` passes `write_root=self._write_root`
  to the built-in dispatch when the tool is `write_workspace_file`.

### Step 1.3 — Thread `write_root` through `dispatch_agent`

**File:** `services/recipe_runtime/dispatcher.py`

- Add `write_root: str | None = None` to `dispatch_agent`'s kwargs.
- Pass it into `build_tool_runtime(fm, workspace_root=..., write_root=...)`.
- No other behavior change. Existing tests pass `write_root` implicitly
  as `None` (default = `workspace_root`) so they remain unchanged.

### Step 1.4 — Thread `write_root` through the Control Panel worker

**File:** `services/control_panel/runs.py`

- In the agent branch of `_worker`, if the recipe's `inputs` contain
  `target_dir`, pass it as `write_root=inputs["target_dir"]` to
  `dispatch_agent`. Otherwise omit (defaults to `workspace_root`).
- This is the integration point between the recipe's `target_dir` input
  and the runtime's write scope.

### Step 1.5 — Tests for the write primitive

**File:** `services/recipe_runtime/tests/test_agent_tools.py` (existing)

Add a `WriteWorkspaceFileTest` class:

- `test_writes_under_write_root` — happy path, file appears at
  `write_root/path` with the right content.
- `test_creates_parent_dirs` — `path="a/b/c/x.txt"` creates `a/b/c/`.
- `test_refuses_overwrite_without_force` — second call with same path,
  no `force=true` → returns error string starting with `"error: file
  already exists"`.
- `test_force_true_overwrites` — second call with `force=true` succeeds
  and updates content.
- `test_path_escape_refused` — `path="../../escape.txt"` → returns
  error string mentioning path escape.
- `test_write_root_separate_from_workspace_root` — build a runtime with
  `workspace_root=A, write_root=B`; writes go to `B`, reads scoped to
  `A`.

Add a `BuildToolRuntimeTest` test:
- `test_default_write_root_is_workspace_root` — when `write_root=None`,
  writes land in `workspace_root` (so default behavior of read-only
  recipes is unchanged if they ever call the tool).

### Step 1.6 — Wire `test_agent_tools` into `validate.py`

**File:** `scripts/validate.py`

- Add `"services.recipe_runtime.tests.test_agent_tools"` to the
  "Recipe runtime tests" row. This row currently runs
  `test_assembler`, `test_dispatcher`, `test_providers`, `test_agent`
  but not `test_agent_tools` — closes a pre-existing gap simultaneously.

### Step 1.7 — `validate.py` 16/16 (check count unchanged)

Phase 1 produces no new validate row; the new tests fold into the
existing "Recipe runtime tests" row.

## Phase 2 — Author the three skills

Each authored as one prose file with frontmatter `risk: low, source:
internal`. Voice: second-person/imperative, provider-neutral. Calibrate
length against `workspace-state-assessment` (~170 lines after lint
reflow) — these skills carry more (recipe-specific protocol + per-doc
templates + soft defaults + depth gate) and will be slightly longer.

### Step 2.1 — `app-planning` skill

**File:** `.archived/skills/documentation-planning/app-planning/SKILL.md`

Sections (all prescribed by the spec):
1. The two-phase protocol (Phase A: stack-choice ADR + planned-files
   manifest; Phase B: write remaining 8 artifacts in order).
2. The 9 planning artifacts + per-doc inner-shape templates.
3. The owned/drift/notes wrapper (verbatim from `assess-workspace`).
4. Soft default stack list (python-fastapi-postgres /
   node-nextjs-postgres / go-gin-postgres / rust-axum-postgres) — as
   gravity, not constraint.
5. Inlined lean security-baseline rubric (`.env` hygiene / Documentation
   / Validation / CI/CD).
6. Depth gate (`depth = lean | deep` — only literal `"deep"` activates
   deep mode; deep adds the `next-steps.md` companion + the
   "Vulnerability & supply-chain" block to `security-baseline.md`).
7. Hard rules: blast radius (no writes outside `write_root`, no
   deletes), the mandatory-first-artifact rule for the ADR, the
   planned-files manifest requirement.

### Step 2.2 — `app-scaffolding` skill

**File:** `.archived/skills/documentation-planning/app-scaffolding/SKILL.md`

Sections:
1. Preconditions (planning artifacts present — abort if not; reads
   `tech-stack.md` for the picked stack).
2. Stack-archetype-aware file list: language manifest / Dockerfile / CI
   workflow / linter / formatter / test runner / pre-commit hooks /
   source-dir skeleton / README / CONTRIBUTING / `.gitignore` /
   `LICENSE`. For each, the soft-default content patterns per
   archetype.
3. Owned-section contract for `README.md` and `docs/CONTRIBUTING.md`
   (config files are NOT wrapped — they are configs).
4. Final action: `git init` if `.git/` absent.
5. Hard rules: no overwrite without force (skill never passes
   `force=true`); re-run uses owned-section read-modify-write loop.

### Step 2.3 — `feature-seeding` skill

**File:** `.archived/skills/documentation-planning/feature-seeding/SKILL.md`

Sections:
1. Preconditions (`target_dir/.git` exists).
2. The 5 per-feature artifacts (SRS / DB schema / API spec / sequence
   diagram / tests) with the canonical inner-shape templates lifted
   from the vault workflows (`generate-feature-spec.md` →
   `<F>_srs.md`, etc.).
3. Mermaid syntax requirements for ERD + sequence diagram (the vault
   workflows are specific about this).
4. Owned-section contract on every produced artifact (re-run for the
   same feature surfaces drift).
5. Single-feature-per-invocation rule (user re-invokes for the next
   feature; matches the composable design).

### Step 2.4 — Register all three skills

**File:** `.archived/skills/documentation-planning/registry.json`

Append three `skills[]` entries matching the existing schema
(`workspace-state-assessment` is the reference example). Each has
distinct `trigger_conditions`/`anti_triggers`.

## Phase 3 — Author the three recipes

### Step 3.1 — `recipes/plan-app.md`

Frontmatter per the spec's "Recipe frontmatter shapes". Body sections:
`What this does` / `Who it's for` / `What you need` / `How to run`
(includes the next-step `/scaffold-app` example) / `Example output`
(stub) / `Agent` (thin orchestration brief pointing at the skill;
inputs bound; hard boundary statement).

### Step 3.2 — `recipes/scaffold-app.md`

Frontmatter per spec. Body same shape; `How to run` shows the prior
`/plan-app` step and the next `/seed-feature` step.

### Step 3.3 — `recipes/seed-feature.md`

Frontmatter per spec. Body same shape; `Who it's for` calls out the
standalone use case (any existing project, not just plan-app outputs).

## Phase 4 — Regenerate downstream artifacts

In order:
1. `python scripts/recipe_manager.py sync` — regenerates
   `recipes/registry.json` (15 → 18 recipes).
2. `python scripts/docs_generator.py`.
3. `python scripts/sync_antigravity.py`.
4. `python scripts/sync_claude_code.py`.
5. `python scripts/cross_link.py` — refreshes backrefs (the deep-mode
   skills now have a second recipe-backref).

## Phase 5 — Lint + validate

1. `python scripts/recipe_manager.py lint` — all three new recipes
   resolve their skills (catches typos / unregistered skills).
2. `python scripts/recipe_manager.py run <id> --dry-run` for each of
   the three recipes — confirms envelope assembly and skill load.
3. `python scripts/validate.py` — 16/16. Two simultaneous gains: the
   write-tool tests fold into "Recipe runtime tests" (count unchanged),
   and `test_agent_tools` is now run by validate (gap closed).

## Phase 6 — Commit

Single commit for the whole family (skill + recipe authoring + the
write-tool prerequisite is one logical unit; splitting would leave
validate red between commits). Conventional Commits:
`feat(recipe): create-app family — /plan-app + /scaffold-app + /seed-feature`.

## Phase 7 — Live verification (infra + cost gated; deferred to a real session)

The free-form-stack quality risk means hand review on a strong model is
the only honest behavior verification. Order:

1. `/plan-app` against a fresh empty `target_dir` (a real new project
   idea) → review the 9 artifacts. Particularly: does the stack-choice
   ADR get written FIRST, does the picked stack make sense, are the
   planned-files manifest entries reasonable.
2. `/scaffold-app` on the same `target_dir` → review the project
   skeleton lands cleanly; the precondition check fails fast when the
   planning artifacts are absent.
3. `/seed-feature` for the top MVP feature → review the SRS / DB / API
   / sequence / tests artifacts.
4. Re-run `/plan-app` on the same `target_dir` with the same intent →
   confirm "Drift since last run" reports no substantive change
   (rewording must not register as drift) — the core verifiable
   property of the doc-ownership contract.
5. Re-run `/plan-app` on the same `target_dir` with a *different*
   intent → confirm the drift section captures the substantive change
   without clobbering human `Notes`.

Phases 1–6 are pure-code/prose and can be done now. Phase 7 needs a
strong model (Claude Sonnet / Gemini Pro) — defer to a session with
the appropriate key.

## Risk-to-step traceability

| Spec open risk | Caught/contained at |
|---|---|
| Free-form stack quality | Phase 7.1 (stack-choice ADR review) |
| No checkpoint primitive (must remember chain) | Phase 3 (frontmatter `examples` shows next step in each recipe) |
| Composable family bloats context | N/A — each invocation loads its own skill only |
| `write_workspace_file` blast radius | Phase 1.5 (path escape + overwrite refusal tests) |
| `target_dir` non-empty | Phase 7.1 (precondition error before any LLM call) |
| ADR convention not known to assess-workspace | Out of scope; tracked in spec as a future follow-up |
