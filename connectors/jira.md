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
docs: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
about: >-
  Jira Cloud connector — reads issues, projects, and comments via Atlassian's
  REST API v3. Powers ticket-to-feature (turns a Jira ticket into a feature
  spec) and daily-briefing's "your tickets today" section. Install writes
  JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN to `.env` via env_writer.
  Advanced: JIRA_BASE_URL is your site root (e.g. `https://acme.atlassian.net`).
  Create the API token at id.atlassian.com — read-only is enough for every
  recipe that uses this.
highlights:
  - Provides issues, projects, and comments via Jira's REST v3 API
  - Powers ticket-to-feature and daily-briefing's ticket summary
  - Read-only token is sufficient — write access not needed
  - Live-check probe hits /rest/api/3/myself with your creds
examples:
  - label: Generate the API token
    code: "xdg-open https://id.atlassian.com/manage-profile/security/api-tokens"
  - label: Smoke-test against your site
    code: "curl -s -u $JIRA_EMAIL:$JIRA_API_TOKEN $JIRA_BASE_URL/rest/api/3/myself | jq '.displayName'"
  - label: List issues assigned to you
    code: "curl -s -u $JIRA_EMAIL:$JIRA_API_TOKEN \"$JIRA_BASE_URL/rest/api/3/search?jql=assignee=currentUser()&fields=summary,status\" | jq '.issues[] | {key, summary: .fields.summary}'"
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
