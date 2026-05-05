# Connector Spec v0.1

A **Connector** declares an external data source (Jira, Bitbucket, GitHub, Confluence, …) that recipes can pull from. It is a *declaration*, not an executable: the actual data movement lives in n8n workflows and a Python embedding service. The connector file exists so recipes can reference data sources by stable IDs and so users have a single place to read setup instructions.

This document is the source of truth for the connector file format and how recipes resolve their `requires_connectors` field.

---

## File format

One Markdown file per connector at `connectors/<id>.md`. The ID is kebab-case and equals the filename stem.

YAML frontmatter + Markdown body, same shape as recipes:
- The frontmatter is the machine-readable declaration.
- The body is what `docs/connectors/<id>.md` publishes — what a user reads to wire credentials.

---

## Frontmatter reference

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique slug, kebab-case. Equals filename stem. |
| `name` | string | yes | Human-readable display name. |
| `description` | string | yes | One-line, plain-English. |
| `status` | enum | yes | `experimental` \| `stable` \| `deprecated`. |
| `provides` | string[] | yes | Names of data shapes this connector exposes (e.g., `issues`, `pull_requests`). |
| `auth_type` | enum | yes | `api_token` \| `oauth2` \| `basic` \| `bearer` \| `none`. |
| `requires_env` | string[] | yes | Env var names needed at runtime (validated when n8n workflow runs, not at lint time). |
| `n8n_workflow` | string | no | Path to the n8n workflow that performs ingest. May be unset for `experimental` connectors. |
| `embed_collection` | string | no | Name of the pgvector collection where normalized data lands. |
| `tags` | string[] | no | Free-form tags for discovery. |

---

## Markdown body

Below the frontmatter, prose with these fixed sections:

```
## What this is
## Setup
## Data shapes
## Used by recipes
```

---

## Registry

`connectors/registry.json` is the index that `recipe lint` resolves `requires_connectors` against. Format:

```json
{
  "version": "1.0.0",
  "type": "connector_registry",
  "connectors": [
    { "id": "jira", "name": "Jira", "description": "...", "status": "experimental", "provides": ["issues"], "tags": [], "path": "connectors/jira.md" }
  ]
}
```

Until a `connector_manager.py sync` exists, the registry is hand-maintained.

---

## How recipes resolve connectors

`recipe lint` checks every `requires_connectors` ID against `connectors/registry.json`:

- ID present in the registry → resolves cleanly.
- ID missing from registry → **warning** if the recipe is `experimental`, **error** otherwise.

A future check (not yet implemented): a `stable` recipe that requires an `experimental` connector should produce a warning.

---

## Reserved paths

- `connectors/<id>.md` — connector declarations
- `connectors/registry.json` — connector index
- `n8n-workflows/connectors/<id>.n8n` — recommended location for ingest workflows
- `services/context_bridge/` — Python embedding service (Phase F.0 scaffold landed; F.1+ wires Postgres + pgvector)

---

## What a connector is *not*

- Not an executable. The connector file does not run code.
- Not a credential store. Credentials live in `.env` and are referenced by `requires_env`.
- Not a data shape definition. The `provides` list is a label, not a schema. Schema enforcement, when added, will live alongside the embedding service.
