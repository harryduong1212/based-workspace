# Design: `create-app` recipe family — `/plan-app` + `/scaffold-app` + `/seed-feature`

- **Date:** 2026-05-21
- **Status:** Approved — ready for implementation planning
- **Author:** brainstormed with the workspace owner
- **Companions:** symmetric with the read-only `/assess-workspace` recipe
  (`2026-05-19-assess-workspace-design.md`); both share the doc
  ownership / drift contract, the `mode: lean|deep` echo, and the deep-
  mode pair (`codebase-cleanup-deps-audit` + `security-audit`).

## Problem

There is no repeatable way to take a *raw application idea* and turn it
into a trustworthy planning + scaffold + first-feature bundle for a new
codebase. The vaulted `.archived/_vault/workflows/custom-workflows/`
sequence (feature-kickoff → SRS → DB → API → sequence → tests) handles
the *per-feature* layer for an app that already exists; nothing currently
handles the *app-init* layer above it. Doing this by hand is inconsistent
and inevitably skips the parts that turn out to matter (ADRs, threat
model baseline, MVP scoping, project-scaffold hygiene).

The output must also be re-runnable: a second pass surfaces what changed
in reality rather than silently overwriting curated content (same
ownership contract as `assess-workspace`).

## Scope

**Three composable, one-shot recipes**, not one mega-recipe:

```
NEW APP:    /plan-app  →  /scaffold-app  →  /seed-feature  (×N)
EXISTING:                                    /seed-feature  (any time)
EXISTING:   /assess-workspace                                (the inverse audit)
```

Each recipe is `execution.type: agent`, one-shot, independently
re-runnable. The "checkpoint" between phases is the user's deliberate
decision to invoke the next recipe — the runtime has no native
pause/resume primitive and adding one is out of scope (deferred per the
risk register).

**Write-heavy by design** — produces real files. Strict blast-radius
controls (below) are load-bearing.

Out of scope: writing application source code beyond a minimal skeleton
(filling functionality belongs to feature implementation, not scaffolding);
mutating an existing codebase via `/plan-app` or `/scaffold-app` (those
require a fresh empty `target_dir`); calling external APIs other than the
chosen LLM provider.

## Components & boundaries

| Unit | Purpose | Notes |
|---|---|---|
| `agent_tools.write_workspace_file` (new built-in tool) | The shared write primitive. Refuses path escape, refuses overwrite without explicit `force=true`, returns clear errors. | Tested via `test_agent_tools` (currently not in `validate.py` — that gap closes as part of this work). |
| `ToolRuntime.write_root` (new param) on `agent_tools.build_tool_runtime` | Separate write scope from `workspace_root`. The new recipes set `write_root = target_dir`; reads stay scoped to `workspace_root` so skill bodies and reference files remain accessible. Defaults to `workspace_root` for read-only recipes (unchanged behavior for `assess-workspace`). | `dispatch_agent` gains a `write_root` kwarg; `runs.start_run` resolves it from the recipe's `target_dir` input. |
| `recipes/plan-app.md` | Greenfield planning. Produces 9 planning artifacts under `target_dir/docs/` (incl. ADRs). | requires_skills: `app-planning` (+ deep pair in deep mode). |
| `recipes/scaffold-app.md` | Reads the planning artifacts; writes project skeleton (configs, source dir, CI, Dockerfile, README, etc.). Refuses if planning artifacts missing. | requires_skills: `app-scaffolding`. |
| `recipes/seed-feature.md` | Read a project (planning + scaffold *or* any existing project); produce SRS + DB schema + API spec + sequence diagram + test plan for **one** named feature. | requires_skills: `feature-seeding`. Standalone-usable on any project. |
| `app-planning` skill (new) | Planning methodology: mandatory stack-choice ADR first, planned-files manifest before write, soft default stack list, ownership/drift contract reuse, the 9 doc templates, depth-gate prose. | category `documentation-planning`. |
| `app-scaffolding` skill (new) | Scaffolding methodology: refuses without planning artifacts, idempotency rules (re-run updates owned sections only), what counts as "skeleton" per stack archetype. | category `documentation-planning`. |
| `feature-seeding` skill (new) | The vaulted feature-pipeline (SRS / DB / API / sequence / tests) inlined as canonical templates; one feature per invocation. | category `documentation-planning`. |
| `codebase-cleanup-deps-audit` + `security-audit` (reused, deep only) | As in `assess-workspace`: deep mode enriches the security artifact. | requires_skills lists them; skill prose hard-gates use on `depth == "deep"`. |

**`env-config` is NOT reused** — same finding as `assess-workspace`:
it's a recipe, not a loadable skill. The lean security-baseline rubric
is inlined into `app-planning`.

## Recipe frontmatter shapes (load-bearing, not full wording)

```yaml
# recipes/plan-app.md
id: plan-app
execution: { type: agent }   # no `model:` — portable
requires_skills: [app-planning, codebase-cleanup-deps-audit, security-audit]
inputs:
  - { name: target_dir, required: true,  description: "Must not exist or must be empty. Created if missing. write_root for the agent." }
  - { name: app_name,   required: true,  description: "kebab-case slug used in paths / package names." }
  - { name: intent,     required: true,  description: "Free-text description of what the app does and for whom." }
  - { name: depth,      required: false, description: "lean (default) | deep (adds CVE + security-audit pass)." }
outputs:
  - { name: planning_artifacts, type: markdown }
```

```yaml
# recipes/scaffold-app.md
id: scaffold-app
execution: { type: agent }
requires_skills: [app-scaffolding]
inputs:
  - { name: target_dir, required: true,  description: "Existing dir produced by plan-app. Must contain the planning artifacts." }
outputs:
  - { name: project_skeleton, type: text }
```

```yaml
# recipes/seed-feature.md
id: seed-feature
execution: { type: agent }
requires_skills: [feature-seeding]
inputs:
  - { name: target_dir,  required: true,  description: "Existing project root (does not require plan-app artifacts; reads what's there)." }
  - { name: feature,     required: true,  description: "Feature name from mvp-features.md or free-text." }
  - { name: feature_intent, required: false, description: "Override / clarification of intent for this feature." }
outputs:
  - { name: feature_artifacts, type: markdown }
```

## Output artifacts

### `/plan-app` — 9 planning docs (under `target_dir/docs/`)

`overview.md` · `architecture.md` (Mermaid system diagram) ·
`tech-stack.md` (chosen stack + rationale) · `core-domain.md` (entities,
ubiquitous language) · `mvp-features.md` (priority table — feeds
`/seed-feature`) · `infrastructure.md` · `security-baseline.md` (inlined
rubric + deep-mode block when `depth=deep`) · `test-strategy.md` ·
`adr/0001-stack-choice.md` (**mandatory first artifact**; alternatives
considered + rationale; written *before* any other doc, so a wrong stack
pick is visible before commitment compounds; subsequent ADRs 0002+ for
each major decision).

### `/scaffold-app` — project skeleton (under `target_dir/`)

Stack-appropriate set drawn from: `README.md` · `LICENSE` · `.gitignore`
· language manifest (`package.json` / `pyproject.toml` / `Cargo.toml`
/ `go.mod` / …) · `Dockerfile` + `.dockerignore` · CI workflow
(`.github/workflows/ci.yml` or platform-appropriate) · linter / formatter
configs · test-runner config · pre-commit hooks config · source-dir
skeleton (e.g. `src/<app_name>/__init__.py`, `index.ts`, `main.go`) ·
`docs/CONTRIBUTING.md`. Final action: `git init` if `target_dir/.git`
absent.

### `/seed-feature` — per-feature artifact set (under `target_dir/docs/`)

For each invocation of feature `F`:
`specs/<F>_srs.md` · `db/<F>_schema.md` (Mermaid ERD) ·
`api/<F>_api_spec.md` · `sequence-diagrams/<F>_sequence.md` (Mermaid) ·
`tests/<F>_tests.md`. Mirrors the vault feature-pipeline structure but
written by one recipe instead of a checkpoint chain.

## Per-doc owned-section templates

Reuse the assess-workspace contract verbatim: identical
`owned:start` / `owned:end` + `Drift since last run` + `Notes` wrapper
for **every** doc this family writes. Inner shapes are fixed per doc
type (the skill prose carries the templates — same rationale as
assess-workspace: a fixed inner shape is what makes drift detection
isolate substantive change instead of rewording noise).

Per-doc inner shapes (authored in the skill, summarized here):

- **plan-app artifacts:** each gets a stack-archetype-aware structured
  shape (e.g. `tech-stack.md` → Languages · Frameworks · Datastore ·
  Build · Deploy · Rationale subsections; `core-domain.md` → Entities
  table · Aggregates · Ubiquitous language glossary).
- **scaffold-app**: writes files whose *content* is structured by the
  file's purpose (configs are configs, not owned-section-wrapped). The
  owned-section contract applies only to the *docs* (`README.md` and
  `docs/CONTRIBUTING.md` get the wrapper); config files do not.
- **seed-feature**: each artifact wraps its body in the owned-section
  contract so re-running for the same feature surfaces drift (e.g. the
  API spec changing) rather than overwriting.

## Mandatory first-artifact: stack-choice ADR (`/plan-app` only)

The single load-bearing mitigation for the free-form stack risk. Skill
prose enforces:

1. **Before** writing any other artifact, the agent writes
   `adr/0001-stack-choice.md` containing: the picked stack (language,
   framework, datastore, frontend if any, deploy target), 2–3 alternatives
   considered, the rationale for the pick mapped against `intent`, and
   the soft-default list it deviated from (if any).
2. **Then** the agent writes the planned-files manifest as
   `_plan-app_manifest.md` (the next file to write) — a list of every
   remaining file it intends to write with a one-line purpose.
3. **Then** it writes the remaining 8 planning artifacts in order.

This means a re-run of `/plan-app` that catches a wrong stack choice
costs the user one ADR review, not a tree of compounding wrong artifacts.

## Soft default stack list

When `intent` doesn't strongly suggest otherwise, the skill prose lists:
`python-fastapi-postgres` · `node-nextjs-postgres` · `go-gin-postgres` ·
`rust-axum-postgres`. Gravity, not a constraint — the agent can deviate
and document the choice in the ADR.

## Inlined lean security-baseline rubric

Same as `assess-workspace`'s inlined rubric (since `env-config` is a
recipe not a skill): `.env` hygiene · Documentation · Validation · CI/CD.
Encoded once in `app-planning`'s prose; consulted when writing
`security-baseline.md`.

## Depth gate

`depth: lean | deep` on `/plan-app` only (scaffold and seed don't need
it). Same gating mechanism as `assess-workspace`: `requires_skills`
loads all skill bodies always; the gate is prose-level in `app-planning`;
artifacts echo a `mode:` line. Deep mode enriches `security-baseline.md`
and adds evidence-backed items to a `next-steps.md` companion artifact
(deep-only — not produced in lean mode).

## Blast-radius controls

Non-negotiable, enforced by the new tool + by skill prose:

1. **`write_workspace_file` tool:** all writes routed through it; it
   refuses any path that resolves outside `write_root`; refuses
   overwrite unless `force=true` (the recipes never pass `force=true` —
   re-runs use the owned-section read-modify-write loop, which is
   structurally different from overwriting).
2. **`/plan-app` `target_dir` guard:** must not exist OR must be empty.
   First action is to create the directory and `git init` it. Any other
   state is a hard error.
3. **`/scaffold-app` precondition:** `target_dir/docs/adr/0001-stack-choice.md`
   must exist. No planning artifacts → hard error (preserves the
   "plan → review → scaffold" gate without runtime checkpointing).
4. **`/seed-feature` precondition:** `target_dir` must look like a git
   repo (contains `.git/`). Otherwise hard error.
5. **No deletes ever.** The tool refuses delete operations; the agent
   has no mechanism to remove files.

## Considered and rejected alternatives

| Alternative | Why not |
|---|---|
| Single `/create-app` recipe with disk checkpoint state machine | More skill complexity; seed-feature methodology trapped inside it rather than reusable. Three small recipes win on composability + standalone reusability of seed-feature. |
| Adding a real runtime checkpoint primitive (pause/resume agent runs from UI) | Multi-week (touches dispatch_agent + runs.py + SSE + UI). Speculative — built for one use case. Deferred until a second use case demands it. |
| Curated stack catalog (only N pre-templated stacks) | User explicitly chose free-form. Catalog deferred as a potential future hardening pass (skill could later add a `stack:` input that, if set, locks the choice and uses a templated scaffold). |
| Reusing the vault `feature-kickoff` workflow | It's vaulted, not invokable from the live runtime. Pattern preserved by inlining the SRS / DB / API / sequence / tests templates into `feature-seeding` (same approach as the `env-config`-rubric inlining for `assess-workspace`). |
| Reusing `wiki-architect` / `c4-*` for architecture doc | Same as assess-workspace's finding: they impose own doc shapes, fight the owned-section/drift contract. |
| Adding `workspace-state-assessment` to `requires_skills` | **No.** assess-workspace is the *inverse* operation (audit existing state vs. create state from intent). Pulling its 174-line skill into context would inject a directly contradictory framing (`"you inspect; you never mutate"` — opposite of plan-app's job) and would confuse which protocol the agent should follow. The genuinely shared bits (owned-section wrapper, `mode:` echo, deep-mode skill pair, lean security rubric prose) are copied verbatim into the new skills — same approach as inlining the `env-config` rubric. Premature DRY via skill extraction was considered and rejected: ~30 lines of stable shared prose is not worth a third skill's overhead. |
| Wrapping `/plan-app` inside `/assess-workspace`'s flow | These compose *sequentially*, not nested: `plan-app → scaffold-app → seed-feature×N` builds the project; then `/assess-workspace` audits it ("did reality match the plan?"). Zero code coupling needed; pure usage pattern. |

## Error handling & boundaries

- Read-only on the based-workspace itself (where the skills live). The
  only writes happen inside `write_root` (= `target_dir`).
- `/plan-app` on a non-empty `target_dir` → hard error before any LLM call.
- `/scaffold-app` without planning artifacts → hard error.
- `/seed-feature` on a non-git directory → hard error.
- `write_workspace_file` returns a structured error string the agent can
  read and adapt to; it never raises an exception into the agent loop.
- Free-form stack: the stack-choice ADR makes a wrong pick visible
  before compounding; a `/plan-app` re-run with overridden ADR rewrites
  only the owned sections (drift surfaces in "Drift since last run").

## Testing — honest scope

- **Unit tests (code):**
  - `write_workspace_file`: path escape refused, overwrite refused
    without force, write_root enforcement, structured error returns.
  - `ToolRuntime.write_root`: defaults to `workspace_root`, can be set
    separately, propagates to tool invocations.
  - `dispatch_agent`: `write_root` kwarg threaded through to runtime;
    existing tests untouched (default behavior unchanged).
- **Lint / sync (gates):**
  - `recipe_manager.py lint` resolves all three new recipes' skills.
  - `recipe_manager.py sync` regenerates the recipe registry.
  - `validate.py` 16/16 → 16/16 (test_agent_tools row added simultaneously
    — currently not run by validate; closes that gap while we're in there).
- **No deterministic agent-behavior tests** for the three recipes
  themselves — same honesty as assess-workspace's spec. Functional
  confidence comes from one hand-reviewed live run of each recipe.
- **Dry-run smoke:** `recipe_manager.py run <id> --dry-run` confirms
  envelope assembly and skill load for each recipe.

## Open risks (acknowledged, accepted)

- **Free-form stack quality is bound to model knowledge.** Realistic on
  Claude Sonnet/Gemini Pro; weak on local gemma even with the
  `tool_code` shim. Mitigation: mandatory stack-choice ADR first +
  planned-files manifest before remaining writes.
- **No runtime checkpoint primitive.** Composable-recipes design
  sidesteps it; if we later regret this, the runtime addition is the
  documented path forward (architectural-roadmap).
- **Three slash commands the user must chain.** Mitigation: each
  recipe's frontmatter `examples` shows the next step in the chain
  ("after this, run `/scaffold-app --input target_dir=…`").
- **`write_workspace_file` is a new attack surface** — an agent that
  goes off-rails could write to anywhere inside `write_root`. The
  blast-radius controls (no escape, no delete, no overwrite without
  force) bound it; combined with `target_dir` being a fresh empty
  external dir on `/plan-app`, the practical worst case is "wasted disk
  in the new project dir."
- **Three new skills bloat agent context** when all three are loaded
  for the chained workflow. Each is one recipe though, so any given
  invocation loads only its own skill (plus the deep pair if `depth=deep`).
- **`adr/` directory convention** is a new artifact path that
  `assess-workspace` doesn't currently know about. A future
  `assess-workspace` revision could learn to read ADRs as evidence
  for `tech-stack.md`; tracked as a low-priority follow-up.
