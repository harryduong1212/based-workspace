---
id: bitbucket
name: Bitbucket
description: Atlassian Bitbucket source code, pull requests, and reviews.
status: experimental
provides:
  - pull_requests
  - repositories
  - commits
auth_type: api_token
requires_env:
  - BITBUCKET_WORKSPACE
  - BITBUCKET_USERNAME
  - BITBUCKET_APP_PASSWORD
n8n_workflow: n8n-workflows/connectors/bitbucket.n8n
embed_collection: bitbucket
tags: [atlassian, scm, code-review]
docs: https://developer.atlassian.com/cloud/bitbucket/rest/intro/
about: >-
  Bitbucket Cloud connector — reads pull requests, repositories, and commits
  via Atlassian's REST API. Used by pr-review-prep to pull the PR body, diff,
  and inline comments. Install writes BITBUCKET_WORKSPACE, BITBUCKET_USERNAME,
  and BITBUCKET_APP_PASSWORD to `.env` via env_writer (values write-only,
  never echoed back). Advanced: the "app password" is Bitbucket's PAT-equivalent
  — scope it to read-only repository + PR access. Uninstall clears the env
  vars but only those NOT shared with another installed connector.
highlights:
  - Provides pull_requests, repositories, and commits to recipes
  - Powers pr-review-prep — without this connector that recipe is unavailable
  - Auth via Bitbucket "app password" (PAT-equivalent) — read-only is enough
  - Live-check probe exercises the API with your real creds
examples:
  - label: Smoke-test (uses the env you just wrote)
    code: "curl -s -u $BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD https://api.bitbucket.org/2.0/repositories/$BITBUCKET_WORKSPACE | jq '.values[].name'"
  - label: List your open PRs
    code: "curl -s -u $BITBUCKET_USERNAME:$BITBUCKET_APP_PASSWORD 'https://api.bitbucket.org/2.0/pullrequests/'$BITBUCKET_USERNAME | jq '.values[] | {title, link: .links.html.href}'"
---

## What this is
Connects to Atlassian Bitbucket to pull pull requests, repository metadata, and commits into the workspace's context store. Used by recipes that summarize review queues, prepare PR review context for AI tools (e.g., CodeRabbit), or correlate code changes with tickets.

## Setup
*(Partial — Context Bridge scaffold is in place, ingestion pending Phase F.2.)*

1. Create a Bitbucket app password at <https://bitbucket.org/account/settings/app-passwords/> with `repository:read` and `pullrequest:read` scopes.
2. Add the following to your `.env` file (template lives in `.env.example`):
   ```
   BITBUCKET_WORKSPACE=your-workspace
   BITBUCKET_USERNAME=your-username
   BITBUCKET_APP_PASSWORD=<paste app password>
   ```
3. Install the `memory` MCP feature from the Control Panel Features page (or
   manually: `pip install -r services/memory_mcp/requirements.txt` and bring up
   the Qdrant container — `podman compose --profile qdrant up -d`). Ingest of
   Bitbucket pull requests happens through the `memory` MCP's `add_memory` tool.
4. *(optional)* Import the n8n workflow at `n8n-workflows/connectors/bitbucket.n8n`
   for scheduled bulk ingestion via n8n.
5. Verify: `python scripts/recipe_manager.py run daily-briefing --dry-run`.

## Data shapes
- **pull_requests** — `{ id, title, state, author, source_branch, dest_branch, created, updated, description, repo }`
- **repositories** — `{ slug, name, description, default_branch, language, updated }`
- **commits** — `{ hash, author, message, date, repo }`

## Used by recipes
- `daily-briefing`
- `pr-review-prep`
- `ticket-to-feature`
