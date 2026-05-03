# Product Plan — based-workspace user-facing layer

> Status as of 2026-05-02 (post Phase-1 vault). This document captures the design, what's been built, and what's left.

## Overview

based-workspace is a powerful but expert-only environment — originally 339 skills (now 159 active + 180 vaulted), 16 workflows, profile-based symlink inheritance, MCP wiring, n8n + pgvector infrastructure. The mental model is too much for non-technical users.

This plan turns it into a **product layer on top of the engine**. The engine stays underneath; users see only one concept: **Recipes**.

Three goals drive the layer:
1. Non-technical and technical users invoke AI agents (Antigravity, Claude) without knowing what skills, profiles, or MCP servers are.
2. Daily routines are automated via n8n.
3. Context from Jira, Bitbucket, etc. is pulled into AI tooling (CodeRabbit, Claude) for code review and feature work.

The layer **wraps**, never refactors, the engine. All existing skill/profile/MCP machinery still works; the new layer is additive.

---

## Architecture

### The three user-facing concepts

| User-facing | Hidden underneath |
|---|---|
| **Recipe** — "what I want to do" | profile + workflow(s) + MCP + connectors + prompt |
| **Connector** — "where my data lives" (Jira, Bitbucket, ...) | n8n workflow + auth + pgvector collection |
| **Routine** — "do this on a schedule" | Recipe wrapped in an n8n cron trigger |

Users never see `SKILL.md`, registries, or MCP configuration. They run:
- *"morning briefing"* in chat
- `python scripts/recipe_manager.py run daily-briefing` in the terminal
- A Routine fires on its cron

### Engine vs. product layer

```
.archived/skills/          ← Library (159 active skills, recipe-eligible)
.archived/_vault/skills/   ← Vault (180 skills, out-of-registry, kept for reference)
.archived/workflows/       ← Workflow library
.agents/skills/            ← Active set (symlinks; what AI sees)
.agents/workflows/         ← Active workflows
recipes/           ← Recipes (NEW — first-class user concept)
connectors/        ← Connectors (NEW — data source declarations)
n8n-workflows/             ← n8n workflow files (existing + reserved paths)
services/context_bridge/   ← Reserved for future Python embed/pgvector service
```

### Two-door documentation

- `docs/recipes/` and `docs/connectors/` — auto-generated, zero jargon, what non-technical users browse.
- `docs/RECIPE_SPEC.md`, `docs/CONNECTOR_SPEC.md`, `docs/RULES.md`, `docs/SKILLS.md`, `docs/WORKFLOWS.md` — power-user references.

The generated `docs/recipes/<id>.md` is rendered verbatim from the recipe file's body. Single source of truth; no duplication.

### Context Bridge architecture

Decision: **n8n owns ingest; Python owns embedding.**

- **n8n**: connectors, scheduling, retries, credentials. Built-in Jira/Bitbucket/GitHub nodes do the boring REST work.
- **Python service** (reserved at `services/context_bridge/`): chunking, embedding, pgvector writes.
- **MCP `postgres-memory`**: exposes retrieval to Claude/Antigravity.

Recipes consume the bridge; they don't reimplement it.

---

## Specifications

- **[RECIPE_SPEC.md](RECIPE_SPEC.md)** — recipe file format, runner behavior, lint rules
- **[CONNECTOR_SPEC.md](CONNECTOR_SPEC.md)** — connector file format, registry shape, lint resolution

### Locked design decisions

These were debated and chosen; they're not up for re-debate without new information.

- Recipes are **flat files** (`recipes/<id>.md`), not folders.
- Execution is a **discriminated type**: `prompt | workflow | agent`. Three is enough.
- **No `extends` / inheritance** for recipes. Flat for readability.
- `recipe run` is **transient** (snapshot/restore `.agents/`); `recipe activate` is persistent.
- **Connectors are first-class** in frontmatter, even before connectors exist as code.
- `audience` is `non-tech | tech | both`. No `power-user` middle ground.
- `experimental` recipes get **lint leniency**: missing connectors and missing entrypoints are warnings, not errors. `stable` recipes must resolve everything.

---

## Tooling — every new CLI command

| Command | Purpose |
|---|---|
| `recipe_manager.py list [--audience X] [--tag X]` | Recipe catalog |
| `recipe_manager.py show <id>` | Print a recipe file |
| `recipe_manager.py lint [<id>]` | Resolve every reference; CI-friendly exit code |
| `recipe_manager.py sync [--check]` | Regenerate `recipes/registry.json` |
| `recipe_manager.py run <id> [--input k=v]... [--dry-run]` | Run a recipe (executes per `execution.type`; currently stubbed) |
| `archive_manager.py prune-report [--limit N]` | Score every skill in `.archived/skills/` by recipe usage; surface vault candidates |
| `archive_manager.py vault <id>` | Move a single skill out of the active library to `.archived/_vault/skills/` |
| `archive_manager.py unvault <id>` | Restore a vaulted skill |
| `archive_manager.py vault-orphans [--dry-run] [--limit N]` | Bulk-vault unreferenced skills from latest prune-report |
| `docs_generator.py [--check] [--recipes-only] [--connectors-only]` | Auto-generate `docs/recipes/` and `docs/connectors/` |
| `sync_antigravity.py [--check]` | Render `.agents/workflows/<id>.md` from `recipes/` |
| `sync_claude_code.py [--check]` | Render `.claude/commands/<id>.md` from `recipes/` |
| `validate.py` | Umbrella — runs all 6 integrity checks; non-zero exit gates CI |

Preserved utilities:
- `setup_env.py`, `build_n8n_atom.py` — environment + container build

---

## Skill library strategy

**Recipes drive skill selection.** A recipe declares `requires_skills`; the active set is the union of skills required by enabled recipes. Inventory size stops mattering — only the working set does.

### Three-layer model

| Layer | Path | Role |
|---|---|---|
| Active | `.agents/skills/` | What AI sees right now |
| Library | `.archived/skills/` | Curated, recipe-eligible, in registry |
| Vault | `.archived/_vault/skills/` | Kept for reference, NOT in registry, NOT recipe-eligible |

**Vault, don't delete.** Reversible via `unvault <id>`.

### Current state (2026-05-02, post Phase-1 vault)

- **159 active skills** across 37 categories (was 339 across 53).
- **180 skills vaulted** to `.archived/_vault/skills/` — recoverable via `unvault <id>`.
- **0 orphans** — every active skill is referenced by at least one profile or recipe.
- Profile audit is clean (no broken references).

Phase-1 took the workspace from 339 → 159 with zero behavior change (orphans by definition were unreferenced).

**Target after Phase-2/3 pruning:** ~50–80 high-potential skills.

### Pruning phases

| Phase | Action | Estimate | Status |
|---|---|---|---|
| 1 | Vault all 180 orphans (`vault-orphans`) | -180 | **Done — 339 → 159** |
| 2 | Dedupe within remaining (FastAPI×4, database×4, `*-pro` languages) | -40 to -60 | Pending |
| 3 | Quality filter — "would a fresh LLM call do this better?" | -20 to -40 | Pending |
| 4 | Lock the Core Set (~50 skills you'd be sad to lose) | — | Pending |

---

## Master plan — status

| # | Step | Status |
|---|---|---|
| 1 | Recipe spec | Done — [RECIPE_SPEC.md](RECIPE_SPEC.md) |
| 2 | `prune-report` | Done |
| 3 | Phase-1 vault tooling | Done and **executed** — 339 → 159 skills, 180 vaulted |
| 4 | Phase-2 dedupe | Pending — needs human judgement |
| 5 | Phase-3 + Core Set lock | Pending — needs human judgement |
| 6 | Recipe `run` / `activate` runtime | Done — execution dispatchers stubbed |
| 7 | Context Bridge — connector scaffold | Done — [CONNECTOR_SPEC.md](CONNECTOR_SPEC.md), Jira + Bitbucket scaffolds |
| 8 | Recipes #2 & #3 (Ticket-to-Feature, PR Review Prep) | Pending — needs Jira/Bitbucket auth |
| 9 | Auto-generated `docs/recipes/` and `docs/connectors/` | Done |
| 10 | CI lint glue (`validate.py`) | Done |

Steps 1–3, 6, 7, 9, 10 are complete. **Every step of the master plan that doesn't require external systems is done.**

---

## Files added or modified during the build

### New source files

- `docs/RECIPE_SPEC.md` — recipe format spec
- `docs/CONNECTOR_SPEC.md` — connector format spec
- `recipes/daily-briefing.md` — first recipe (worked example)
- `recipes/registry.json` — auto-generated recipe index
- `connectors/jira.md` — Jira connector scaffold
- `connectors/bitbucket.md` — Bitbucket connector scaffold
- `connectors/registry.json` — connector index (hand-maintained)
- `scripts/recipe_manager.py` — recipe CLI (`list`/`show`/`lint`/`sync`/`activate`/`run`)
- `scripts/docs_generator.py` — `docs/recipes/` + `docs/connectors/` generator
- `scripts/validate.py` — umbrella integrity check
- `scripts/lib/skills_vault.py` — vault/unvault helpers

### Modified

- `scripts/archive_manager.py` — extracted from former `profile_manager.py`; provides `prune-report`, `vault`, `unvault`, `vault-orphans`

### Auto-generated (regenerable from sources)

- `docs/recipes/INDEX.md`
- `docs/recipes/daily-briefing.md`
- `docs/connectors/INDEX.md`
- `docs/connectors/jira.md`
- `docs/connectors/bitbucket.md`

### Reserved paths (declared, not yet implemented)

- `n8n-workflows/connectors/jira.n8n`
- `n8n-workflows/connectors/bitbucket.n8n`
- `n8n-workflows/daily-briefing.n8n`
- `services/context_bridge/`

---

## What's pending

### Blocked on external systems

- Real n8n workflow files for Daily Briefing and the connectors. Needs a running n8n instance.
- Jira / Bitbucket OAuth or API token flow. Needs accounts + tokens.
- Python embedding service (`services/context_bridge/`). Needs decisions on framework (FastAPI? CLI?), embedding model (local or API), and pgvector schema.
- Recipe execution dispatchers — currently stubbed. Need real model dispatch (`prompt`, `agent`) and n8n webhook firing (`workflow`).

### Blocked on human judgement

- Phase-2 dedupe. Which of FastAPI×4, database×4, `*-pro` languages to keep is a taste call. Best done by reviewing `tmp/prune_report.csv` directly.
- Phase-3 quality filter. Per-skill "is this still valuable?" decisions.
- Locking the Core Set (~50 skills).

### Already executed

- **Phase-1 vault** — 180 orphans moved to `.archived/_vault/skills/` on 2026-05-02 via `vault-orphans`. Reversible per-skill with `unvault <id>`.

---

## Where to pick up next session

Pick the option that fits your time and energy:

- **Phase-2 dedupe** — review the 159 active skills for overlap clusters (FastAPI×4, database×4, `*-pro` languages). Vault duplicates with `vault <id>`. Best done by reading [tmp/prune_report.csv](../tmp/prune_report.csv) directly.
- **Continue the build, no auth needed** — write a `connector_manager.py` mirroring `recipe_manager.py` (`list`/`show`/`lint`/`sync`). Useful when there are 3+ connectors.
- **Get a real recipe end-to-end** — wire your Jira account, build the n8n workflow file for `daily-briefing.n8n`, and run `recipe run daily-briefing` for real (not `--dry-run`).
- **Onboard a tester** — point a non-technical friend at `docs/recipes/INDEX.md` and ask whether they understand what's offered. Their confusion is the next product backlog.

To verify everything still works on a fresh checkout:
```
python3 scripts/validate.py
```
Should print 4 PASS markers and exit 0.
