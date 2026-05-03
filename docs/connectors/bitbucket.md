# Bitbucket

> Atlassian Bitbucket source code, pull requests, and reviews.
>
> **Status:** experimental · **Auth:** api_token

| | |
|---|---|
| **Provides** | pull_requests, repositories, commits |
| **Required env vars** | `BITBUCKET_WORKSPACE`, `BITBUCKET_USERNAME`, `BITBUCKET_APP_PASSWORD` |
| **n8n workflow** | `n8n-workflows/connectors/bitbucket.n8n` |
| **Tags** | atlassian, scm, code-review |

---

## What this is
Connects to Atlassian Bitbucket to pull pull requests, repository metadata, and commits into the workspace's context store. Used by recipes that summarize review queues, prepare PR review context for AI tools (e.g., CodeRabbit), or correlate code changes with tickets.

## Setup
*(Not yet implemented — placeholder for when the Bitbucket connector is wired up.)*

1. Create a Bitbucket app password at <https://bitbucket.org/account/settings/app-passwords/> with `repository:read` and `pullrequest:read` scopes.
2. Add the following to your `.env` file (or run `python scripts/setup_env.py`):
   ```
   BITBUCKET_WORKSPACE=your-workspace
   BITBUCKET_USERNAME=your-username
   BITBUCKET_APP_PASSWORD=<paste app password>
   ```
3. Import the n8n workflow at `n8n-workflows/connectors/bitbucket.n8n` into your local n8n instance.
4. Verify: `python scripts/recipe_manager.py run daily-briefing --dry-run`.

## Data shapes
- **pull_requests** — `{ id, title, state, author, source_branch, dest_branch, created, updated, description, repo }`
- **repositories** — `{ slug, name, description, default_branch, language, updated }`
- **commits** — `{ hash, author, message, date, repo }`

## Used by recipes
- `daily-briefing`
- `pr-review-prep` (planned)
