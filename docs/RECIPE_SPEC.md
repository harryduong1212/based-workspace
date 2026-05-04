# Recipe Spec v0.2

A **Recipe** is the user-facing unit of work in based-workspace. It packages a profile of skills, optional n8n workflows, MCP servers, and external data connectors behind a plain-English description so non-technical and technical users can run it the same way.

This document is the source of truth for the recipe file format, runner behavior, and lint rules. It is the interface every recipe author and every tool that consumes recipes must agree on.

---

## File format

One Markdown file per recipe at `recipes/<id>.md`. The ID is kebab-case and equals the filename stem.

Each file has:
- **YAML frontmatter** — structured metadata (covered below)
- **Markdown body** — user-facing documentation; this is what `docs/recipes/<id>.md` publishes

---

## Frontmatter reference

### Identity

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique slug, kebab-case. Must equal filename stem. |
| `name` | string | yes | Human-readable display name. |
| `description` | string | yes | One-line, plain-English. Shown in `recipe list`. |
| `audience` | enum | yes | `non-tech` \| `tech` \| `both`. |
| `version` | semver | yes | Recipe version, independent of the workspace. |
| `status` | enum | yes | `experimental` \| `stable` \| `deprecated`. Affects lint strictness (see below). |
| `cost` | enum | no | `low` \| `medium` \| `high`. Coarse hint for paid API usage. |
| `requires_human_review` | bool | no | If true, runner prompts before executing. Default `false`. |
| `tags` | string[] | no | Free-form tags for `recipe list --tag <x>`. |

### Dependencies

Every reference is resolvable; lint walks each one.

| Field | Type | Resolves against |
|---|---|---|
| `requires_skills` | string[] | `.archived/skills/registry.json` |
| `requires_workflows` | string[] | `.archived/workflows/registry.json` |
| `requires_connectors` | string[] | (future) `connectors/registry.json` |
| `requires_mcp` | string[] | server names in `.vscode/mcp.json` |
| `requires_env` | string[] | env var names; values checked at runtime, not lint-time |

### Invocation

```yaml
triggers:
  cli: daily-briefing            # slug used after `recipe run`
  chat: ["morning briefing"]      # phrases the AI matches in chat
  webhook: /recipes/daily-briefing
  schedule: "0 8 * * *"           # cron; absent = manual only
```

All `triggers.*` fields are optional, but at least one must be present.

### Inputs and outputs

```yaml
inputs:
  - name: focus_project
    type: string
    required: false
    description: Optional Jira project key to scope to.

outputs:
  - name: summary
    type: markdown
    description: Rendered briefing.
```

Supported `type` values: `string`, `number`, `bool`, `markdown`, `json`.

### Execution

```yaml
execution:
  type: prompt | workflow | agent
  entrypoint: <type-specific>
  model: <provider/model id>     # optional; default resolved by the runner
```

| Type | Entrypoint | What runs |
|---|---|---|
| `prompt` | none — `## Prompt` section in body is the entrypoint | One AI call with `requires_skills` loaded into context. |
| `workflow` | path to `.n8n` file | n8n executes the workflow via webhook; runner returns the result. |
| `agent` | none — `## Agent` section in body is the entrypoint | AI agent with `requires_skills` loaded and `requires_mcp` available as tools. |

`model` is provider-agnostic. The runner picks a default when omitted; recipes that need a specific capability (long context, tool use, cheap drafting) can pin one. Examples: `claude-opus-4-7`, `claude-sonnet-4-6`, `gemini-2.5-pro`, `ollama/llama3.1:70b`. Ignored when `execution.type` is `workflow`.

---

## Markdown body

Below the frontmatter, prose with these fixed sections:

```
## What this does
## Who it's for
## What you need
## How to run
## Example output
```

`prompt` and `agent` execution types add one of:

```
## Prompt
## Agent
```

This body is the catalog page. The published doc at `docs/recipes/<id>.md` is generated verbatim; there is no separate documentation file.

---

## Runner behavior

`recipe run <id>`:

1. Load and validate the recipe (same checks as `recipe lint`).
2. Resolve `requires_skills` against the skill registry; their bodies are loaded into the AI call's context for `prompt` and `agent` execution types.
3. Substitute `{input.X}` placeholders in the `## Prompt` or `## Agent` body from `--input k=v` pairs.
4. Dispatch per `execution.type`:
   - `prompt` — one AI call, model from `execution.model` or runner default.
   - `workflow` — POST to the n8n workflow at `execution.entrypoint`; return the response.
   - `agent` — AI agent loop with `requires_skills` in context and `requires_mcp` exposed as tools.
5. Stream output to stdout; honor `--dry-run` by printing the assembled prompt without calling the model.

There is no symlink mutation, no snapshot, no persistent activation — every run is independent. Provider-specific bindings (Antigravity workflows at `.agents/workflows/`, Claude Code slash commands at `.claude/commands/`) are auto-generated from each recipe by `scripts/sync_antigravity.py` and `scripts/sync_claude_code.py`. Edit the recipe at `recipes/<id>.md` and re-run the sync — never edit the generated artifacts directly.

---

## Tooling

The CLI is `python scripts/recipe_manager.py`:

| Command | Effect |
|---|---|
| `recipe list [--audience X] [--tag X]` | Catalog. |
| `recipe show <id>` | Print the user-facing block. |
| `recipe run <id> [--input k=v]... [--dry-run]` | Execute one run per `execution.type`. |
| `recipe lint [<id>]` | Resolve every reference. |
| `recipe sync [--check]` | Regenerate `recipes/registry.json`. |

---

## Lint rules

For `status: stable` recipes, all of the following must hold:

- Every `requires_skills` ID resolves in the skill registry.
- Every `requires_workflows` ID resolves in the workflow registry.
- Every `requires_connectors` ID resolves in the connector registry.
- Every `requires_mcp` name appears in `.vscode/mcp.json`.
- `execution.entrypoint` (when applicable) points at an existing file.
- `id` is unique across all recipes.
- `id` equals the filename stem.
- At least one `triggers.*` field is set.

For `status: experimental` recipes, missing connectors and a missing `execution.entrypoint` file are **warnings**, not errors. This lets a recipe be committed before the machinery it depends on exists.

For `status: deprecated` recipes, lint passes but `recipe run` prints a deprecation notice.

---

## Versioning

The recipe's `version` field tracks changes to that recipe (its frontmatter, prompt content, declared dependencies). The spec version (this document) is separate.

Breaking changes to a recipe — renaming inputs, changing output shape, swapping `execution.type` — should bump the major version.

---

## Registry

`recipes/registry.json` is auto-generated by `recipe sync` and committed. Format mirrors the existing skill and workflow registries: a flat list of `{ id, name, description, audience, status, tags, path }` entries.

`recipe lint` runs `recipe sync --check` to verify the registry matches the contents of `recipes/`.
