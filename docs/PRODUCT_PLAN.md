# Product Plan — based-workspace user-facing layer

The engine — skills, MCP servers, n8n — is powerful but expert-only. This plan layers a **product surface** on top so users see only one concept: **Recipes**.

The layer wraps the engine; it doesn't refactor it. All existing skill/MCP machinery still works underneath.

> Live status — counts, phase progress, what's next — lives in [`memory/master-plan-phases.md`](../). This doc captures design intent, not state.

---

## The three user-facing concepts

| User-facing | Hidden underneath |
|---|---|
| **Recipe** — "what I want to do" | skills + MCP + connectors + prompt or agent body |
| **Connector** — "where my data lives" (Jira, Bitbucket, ...) | n8n workflow + auth + pgvector collection |
| **Routine** — "do this on a schedule" | Recipe wrapped in an n8n cron trigger |

Users never edit `SKILL.md` files, registries, or MCP configuration. They run:

- *"morning briefing"* in chat
- `python scripts/recipe_manager.py run daily-briefing` in the terminal
- A Routine fires on its cron

## Layout

```
recipes/                          ← Recipes (first-class user concept)
connectors/                       ← Connectors (data-source declarations)
.archived/skills/                 ← Skill library (recipe-eligible)
.archived/_vault/skills/          ← Skill vault (kept for reference)
.archived/_vault/workflows/       ← Vaulted legacy workflows
services/recipe_runtime/          ← Dispatcher for execution.type (Phase E0)
services/context_bridge/          ← Embedding + pgvector retrieval (Phase F.0)
n8n-workflows/                    ← n8n workflow files (some reserved)
.agents/workflows/                ← Antigravity slash commands (auto-generated from recipes)
.claude/commands/                 ← Claude Code slash commands (auto-generated from recipes)
```

## Two-door documentation

| Audience | Path |
|---|---|
| Browsers (non-technical) | [`docs/recipes/`](recipes/), [`docs/connectors/`](connectors/) — auto-generated, zero jargon |
| Power users | [`RECIPE_SPEC.md`](RECIPE_SPEC.md), [`CONNECTOR_SPEC.md`](CONNECTOR_SPEC.md), [`SKILLS.md`](SKILLS.md), [`SKILL_ATTRITION.md`](SKILL_ATTRITION.md), [`RULES.md`](RULES.md) |

The generated `docs/recipes/<id>.md` is rendered verbatim from the recipe file's body — single source of truth.

## Context Bridge architecture

Decision: **n8n owns ingest; Python owns embedding.**

- **n8n**: connectors, scheduling, retries, credentials. Built-in Jira/Bitbucket/GitHub nodes do the boring REST work.
- **`services/context_bridge/`**: chunking, embedding, pgvector writes. Stack locked: Postgres 16+ / pgvector / `BAAI/bge-small-en-v1.5` (384-dim, sentence-transformers).
- **MCP `postgres-memory`**: exposes retrieval to Claude / Antigravity.

Recipes consume the bridge; they don't reimplement it.

## Recipe runtime architecture

`scripts/recipe_manager.py` parses, validates, and delegates to `services/recipe_runtime/`:

- **`dispatcher.py`** — three functions, one per `execution.type`: `dispatch_prompt` (Phase E1), `dispatch_workflow` (Phase E2/H), `dispatch_agent` (Phase E3).
- **`prompt_assembler.py`** — provider-agnostic `{input.X}` substitution and message envelope. Real and unit-tested.

Cache strategy (Phase E1): two breakpoints — skill bundle (longest-stable), skill bundle + recipe prelude (medium-stable). The substituted user message is not cacheable.

## Locked design decisions

These were debated and chosen. Not up for re-debate without new information.

- Recipes are **flat files** (`recipes/<id>.md`), not folders.
- Execution is a **discriminated type**: `prompt | workflow | agent`. Three is enough.
- **No `extends` / inheritance** for recipes. Flat for readability.
- Every `recipe run` is **independent** — no symlink mutation, no snapshot, no persistent activation. (Earlier transient/`recipe activate` design dropped in spec v0.2.)
- **Connectors are first-class** in frontmatter, even before they're wired.
- `audience` is `non-tech | tech | both`. No `power-user` middle ground.
- `experimental` recipes get **lint leniency**: missing connectors and missing entrypoints are warnings, not errors. `stable` recipes must resolve everything.
- Skill library is **two-layer**: Library (`.archived/skills/`, recipe-eligible) and Vault (`.archived/_vault/skills/`, kept for reference). Recipes drive selection — only declared `requires_skills` matter.

## Tooling

| Command | Purpose |
|---|---|
| `recipe_manager.py list [--audience X] [--tag X]` | Recipe catalog |
| `recipe_manager.py show <id>` | Print a recipe file |
| `recipe_manager.py lint [<id>]` | Resolve every reference; CI-friendly exit code |
| `recipe_manager.py sync [--check]` | Regenerate `recipes/registry.json` |
| `recipe_manager.py run <id> [--input k=v]... [--dry-run]` | Run a recipe (executes per `execution.type`) |
| `docs_generator.py [--check]` | Auto-generate `docs/recipes/` + `docs/connectors/` |
| `sync_antigravity.py [--check]` | Render `.agents/workflows/<id>.md` from recipes |
| `sync_claude_code.py [--check]` | Render `.claude/commands/<id>.md` from recipes |
| `skill_attrition_audit.py [--summary] [--json]` | Skills not referenced by any recipe |
| `validate.py` | Umbrella — runs every integrity check; non-zero exit gates CI |

## Verification

```
python3 scripts/validate.py
```

Runs every check: recipe lint, registry sync, generated-doc sync, Antigravity + Claude Code command sync, connectors integrity, service-package imports, and the `prompt_assembler` unit tests.
