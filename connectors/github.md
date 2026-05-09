---
id: github
name: GitHub
description: GitHub.com source code, pull requests, issues, and review queue.
status: experimental
provides:
  - pull_requests
  - issues
  - repositories
  - review_requests
auth_type: api_token
requires_env:
  - GITHUB_TOKEN
n8n_workflow: n8n-workflows/connectors/github.n8n
embed_collection: github
tags: [github, scm, code-review]
---

## What this is
Connects to GitHub.com via a Personal Access Token (PAT) for pull requests, issues, repository metadata, and the review queue. Used by recipes that summarize "what's open / what's awaiting my review" or correlate code changes with tickets. GitHub Enterprise Server is not supported by this connector — the API host is hardcoded to `api.github.com`.

## Setup
1. Create a token at <https://github.com/settings/tokens>:
   - **Classic PAT** — scopes `repo`, `read:user`, `read:org` (most flexible). Or
   - **Fine-grained PAT** — *Repository access* on the repos you care about, plus *Repository permissions → Pull requests: Read*, *Contents: Read*, *Metadata: Read*; under *Account permissions* → *Email addresses: Read* + *Profile: Read*.
2. Add to your `.env` (or use the Control Panel's *Set env* button):
   ```
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. Verify via the Control Panel: open `/connectors/github` and click **Test**. The probe issues `GET https://api.github.com/user` with `Authorization: Bearer <token>` and reports the resolved login on success. A 401 response surfaces GitHub's `message` field verbatim (e.g. `Bad credentials` for an invalid/expired token).

## Data shapes
- **pull_requests** — `{ id, number, title, state, draft, author, head, base, created, updated, repo, requested_reviewers }`
- **issues** — `{ id, number, title, state, labels, assignee, author, created, updated, repo }`
- **repositories** — `{ owner, name, default_branch, language, visibility, updated }`
- **review_requests** — `{ pr_number, repo, requested_at, requester }`

## Used by recipes
_(none — not referenced by any recipe.)_
## Notes
- Classic PATs are scoped to all repos the token owner can see. Prefer fine-grained PATs in production-ish setups.
- Tokens expire if you set an expiration. The probe will surface `Bad credentials` once expired — rotate via the same settings page.
- *(Phase H)* Live ingestion via the n8n workflow at `n8n-workflows/connectors/github.n8n` (not yet authored).
