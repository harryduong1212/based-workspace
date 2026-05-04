# PR Review Prep

> Generate a structured review brief for a Bitbucket pull request, with the linked ticket context and past reviewer feedback already pulled in.
>
> **Audience:** tech · **Status:** experimental · **Cost:** low

| | |
|---|---|
| **Tags** | bitbucket, jira, code-review, pr |
| **Requires data from** | bitbucket, jira |
| **Skills loaded** | `comprehensive-review-full-review` |
| **Triggers** | CLI: `pr-review-prep` · Chat: "prep review for PR-NNN", "review brief for PR NNN" |

---

## What this does
Pulls the PR diff, its linked Jira ticket, and similar past PRs, then produces a structured review brief flagging the riskiest changes, the questions already asked in review, and what to spend the most time on.

## Who it's for
Reviewers who want to walk into a PR with the context loaded — what the ticket asked for, what concerns reviewers raised on similar past changes — instead of reading three tabs in parallel.

## What you need
- A Bitbucket account and API token (one-time setup: `python scripts/setup_env.py`).
- A Jira account if the PR is linked to a ticket.
- The Context Bridge running (Phase F) for the "similar past PRs" lookup; without it, the brief works from the PR diff and ticket only.

## How to run
- **In Antigravity or Claude:** say *"prep review for PR 287"*.
- **CLI:** `python scripts/recipe_manager.py run pr-review-prep --input pr_id=287`

## Example output

> **Review brief — PR #287: Migrate auth middleware**
>
> **Linked ticket.** PROJ-419 — Audit log retention. The PR scope matches the ticket's "remove session-token storage" requirement.
>
> **Where to focus.**
> 1. `auth/middleware.py:142-180` — new token-validation path; check that the Redis lookup is wrapped in a timeout (PR #251 broke this same way).
> 2. Migration `0042_drop_session_tokens.sql` — irreversible. Verify the rollback plan in PROJ-419's comments.
> 3. Tests under `tests/auth/` — coverage looks thin for the failure paths.
>
> **Already raised in review.**
> - Reviewer A asked about backwards compatibility with the mobile app — author's reply pending.
> - CI failed once on `test_token_revocation`; passed on retry — flaky or genuine?
>
> **Skip.** Cosmetic test refactors in `tests/auth/test_helpers.py` — out of PR scope per PROJ-419.

## Prompt

You are a senior code reviewer preparing a colleague to do a focused review of a Bitbucket pull request. Produce a structured brief.

### Inputs you have
- The PR's title, description, file diffs, and existing review comments (via the `bitbucket` connector).
- The linked Jira ticket — its description, acceptance criteria, comments — if one exists (via the `jira` connector).
- Similar past PRs and the review concerns raised on them (via the `postgres-memory` MCP semantic search).

### What to produce
A single Markdown document with these sections, in order:

1. **Linked ticket.** Name the ticket, summarize what it asked for in one sentence, and state whether the PR's scope matches.
2. **Where to focus.** Three to five bullets. Each names a file:line range or a migration/config change, says what could go wrong, and cites a past incident or PR where similar code broke (when one exists).
3. **Already raised in review.** Open threads in the PR comments — questions awaiting author reply, concerns not yet resolved.
4. **Skip.** Things in the diff that are out of scope, cosmetic, or covered by other PRs — so the reviewer doesn't waste time.

### Constraints
- Do **not** approve, request changes, or score the PR — that's the human reviewer's job. Stay descriptive.
- Cite sources for every claim ("PR #251 broke this", "per PROJ-419 acceptance criteria").
- If a section has nothing to say, write "(none)" — don't pad.
- Stay under one screen of output.
