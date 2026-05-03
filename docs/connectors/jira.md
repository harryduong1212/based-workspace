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
*(Not yet implemented — placeholder for when the Jira connector is wired up.)*

1. Create a Jira API token at <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Add the following to your `.env` file (or run `python scripts/setup_env.py`):
   ```
   JIRA_BASE_URL=https://your-org.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_API_TOKEN=<paste token>
   ```
3. Import the n8n workflow at `n8n-workflows/connectors/jira.n8n` into your local n8n instance.
4. Verify: `python scripts/recipe_manager.py run daily-briefing --dry-run`.

## Data shapes
- **issues** — `{ id, key, summary, status, assignee, priority, labels, created, updated, description, project_key }`
- **projects** — `{ id, key, name, lead }`
- **comments** — `{ id, issue_key, author, body, created }`

## Used by recipes
- `daily-briefing`
- `ticket-to-feature` (planned)
- `pr-review-prep` (planned)
