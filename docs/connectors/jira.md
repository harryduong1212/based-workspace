# Jira

> Atlassian Jira issue tracking and project management.
>
> **Status:** experimental · **Auth:** api_token

| | |
|---|---|
| **Provides** | issues, projects, comments |
| **Required env vars** | `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` |
| **n8n workflow** | `n8n-workflows/connectors/jira.n8n` |
| **Tags** | atlassian, ticketing, issue-tracking |

---

## What this is
Connects to Atlassian Jira (Cloud or Server) to pull issues, projects, and comments into the workspace's context store. Used by recipes that summarize work-in-progress, generate feature specs from tickets, or enrich PR reviews with ticket context.

## Setup
*(Partial — Context Bridge scaffold is in place, ingestion pending Phase F.2.)*

1. Create a Jira API token at <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Add the following to your `.env` file (or run `python scripts/setup_env.py`):
   ```
   JIRA_BASE_URL=https://your-org.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_API_TOKEN=<paste token>
   ```
3. *(Phase F.1+)* Initialize the Context Bridge schema:
   ```
   pip install -r services/context_bridge/requirements.txt
   python -m services.context_bridge.cli init-schema
   ```
4. *(Phase F.2+)* Ingest a Jira fixture (development mode):
   ```
   python -m services.context_bridge.cli ingest --connector jira \
     --fixture services/context_bridge/tests/fixtures/jira_sample.json
   ```
5. *(Phase H)* Import the n8n workflow at `n8n-workflows/connectors/jira.n8n` for live ingestion.
6. Verify: `python scripts/recipe_manager.py run daily-briefing --dry-run`.

## Data shapes
- **issues** — `{ id, key, summary, status, assignee, priority, labels, created, updated, description, project_key }`
- **projects** — `{ id, key, name, lead }`
- **comments** — `{ id, issue_key, author, body, created }`

## Used by recipes
- `daily-briefing`
- `pr-review-prep`
- `ticket-to-feature`
