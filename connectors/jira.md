---
id: jira
name: Jira
description: Atlassian Jira issue tracking and project management.
status: experimental
provides:
  - issues
  - projects
  - comments
auth_type: api_token
requires_env:
  - JIRA_BASE_URL
  - JIRA_EMAIL
  - JIRA_API_TOKEN
n8n_workflow: n8n-workflows/connectors/jira.n8n
embed_collection: jira
tags: [atlassian, ticketing, issue-tracking]
---

## What this is
Connects to Atlassian Jira (Cloud or Server) to pull issues, projects, and comments into the workspace's context store. Used by recipes that summarize work-in-progress, generate feature specs from tickets, or enrich PR reviews with ticket context.

## Setup
*(Partial — Context Bridge scaffold is in place, ingestion pending Phase F.2.)*

1. Create a Jira API token at <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Add the following to your `.env` file (template lives in `.env.example`):
   ```
   JIRA_BASE_URL=https://your-org.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_API_TOKEN=<paste token>
   ```
3. Install the `memory` MCP feature from the Control Panel Features page (or
   manually: `pip install -r services/memory_mcp/requirements.txt` and bring up
   the Qdrant container — `podman compose --profile qdrant up -d`). Ingest of
   Jira issues happens through the `memory` MCP's `add_memory` tool.
4. *(optional)* Import the n8n workflow at `n8n-workflows/connectors/jira.n8n`
   for scheduled bulk ingestion via n8n.
5. Verify: `python scripts/recipe_manager.py run daily-briefing --dry-run`.

## Data shapes
- **issues** — `{ id, key, summary, status, assignee, priority, labels, created, updated, description, project_key }`
- **projects** — `{ id, key, name, lead }`
- **comments** — `{ id, issue_key, author, body, created }`

## Used by recipes
- `daily-briefing`
- `pr-review-prep`
- `ticket-to-feature`
