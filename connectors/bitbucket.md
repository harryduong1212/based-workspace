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
---

## What this is
Connects to Atlassian Bitbucket to pull pull requests, repository metadata, and commits into the workspace's context store. Used by recipes that summarize review queues, prepare PR review context for AI tools (e.g., CodeRabbit), or correlate code changes with tickets.

## Setup
*(Partial — Context Bridge scaffold is in place, ingestion pending Phase F.2.)*

1. Create a Bitbucket app password at <https://bitbucket.org/account/settings/app-passwords/> with `repository:read` and `pullrequest:read` scopes.
2. Add the following to your `.env` file (or run `python scripts/setup_env.py`):
   ```
   BITBUCKET_WORKSPACE=your-workspace
   BITBUCKET_USERNAME=your-username
   BITBUCKET_APP_PASSWORD=<paste app password>
   ```
3. *(Phase F.1+)* Initialize the Context Bridge schema (shared with the Jira connector):
   ```
   pip install -r services/context_bridge/requirements.txt
   python -m services.context_bridge.cli init-schema
   ```
4. *(Phase F.2+)* Ingest a Bitbucket fixture (development mode):
   ```
   python -m services.context_bridge.cli ingest --connector bitbucket \
     --fixture services/context_bridge/tests/fixtures/bitbucket_sample.json
   ```
5. *(Phase H)* Import the n8n workflow at `n8n-workflows/connectors/bitbucket.n8n` for live ingestion.
6. Verify: `python scripts/recipe_manager.py run daily-briefing --dry-run`.

## Data shapes
- **pull_requests** — `{ id, title, state, author, source_branch, dest_branch, created, updated, description, repo }`
- **repositories** — `{ slug, name, description, default_branch, language, updated }`
- **commits** — `{ hash, author, message, date, repo }`

## Used by recipes
- `daily-briefing`
- `pr-review-prep`
- `ticket-to-feature`
