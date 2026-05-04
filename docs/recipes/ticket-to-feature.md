# Ticket to Feature

> Turn a Jira ticket into a feature spec, API sketch, and open-questions list using related context from past tickets and PRs.
>
> **Audience:** tech · **Status:** experimental · **Cost:** medium

| | |
|---|---|
| **Tags** | jira, bitbucket, feature-kickoff, planning |
| **Requires data from** | jira, bitbucket |
| **Skills loaded** | `backend-architect`, `plan-writing`, `software-architecture` |
| **Triggers** | CLI: `ticket-to-feature` · Chat: "spec out PROJ-XXX", "feature kickoff for PROJ-XXX", "turn this ticket into a feature" |

---

## What this does
Pulls the Jira ticket plus its comments, linked PRs, and similar past tickets, then runs an architecture-aware agent that produces a feature specification, an API sketch, and a list of open questions to resolve before implementation starts.

## Who it's for
Engineers, tech leads, and product folks who want a fast first pass at scoping a ticket without manually piecing together context from Jira, Bitbucket, and prior work.

## What you need
- A Jira account and API token (one-time setup: `python scripts/setup_env.py`).
- A Bitbucket account if the ticket has linked PRs.
- The Context Bridge running locally (Phase F) — without it, the agent works only from the ticket itself, not historical context.

## How to run
- **In Antigravity or Claude:** say *"spec out PROJ-412"* or *"feature kickoff for PROJ-412"*.
- **CLI:** `python scripts/recipe_manager.py run ticket-to-feature --input ticket_key=PROJ-412`
- **Human review:** runner pauses before launching the agent; review the assembled context, then approve.

## Example output

> **Feature Spec — PROJ-412: API rate limiting**
>
> **Goal.** Add per-tenant rate limiting to the public API to prevent noisy-neighbor incidents like the one in PROJ-381.
>
> **Scope.** In: per-tenant token bucket on the gateway. Out: per-endpoint quotas (deferred).
>
> **API sketch.**
> - `GET /v1/limits/{tenant}` → 200 `{remaining, reset_at}` | 404
> - Headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset` on every response
> - 429 with `Retry-After` when exhausted
>
> **Open questions.**
> - Storage backend: Redis (matches PR #287) or in-process LRU with epoch sharing?
> - Default budget per tier — does product own this or eng?
> - How does this interact with the auth-middleware rewrite (PROJ-419)?

## Agent

You are the Chief Orchestrator for a feature-kickoff pipeline. Your input is a Jira ticket key. Your output is three artifacts: a feature spec, an API sketch, and an open-questions list.

### Phase 1 — Context assembly
1. Fetch the Jira ticket via the `jira` connector: title, description, status, comments, linked issues.
2. For each linked Bitbucket PR, fetch via the `bitbucket` connector: title, description, diff summary, review comments.
3. Query the `postgres-memory` MCP for similar past tickets (semantic search on title + description). Surface the top 5.

### Phase 2 — Synthesis
Apply the loaded skills (`backend-architect`, `software-architecture`, `plan-writing`):

- **Feature spec** — SRS-style: goal, scope (in/out), constraints, success criteria. Write at `.docs/specs/{ticket_key}_srs.md`.
- **API sketch** — endpoints, request/response shapes, status codes, headers. Write at `.docs/api/{ticket_key}_api.md`.
- **Open questions** — unresolved decisions blocking implementation, each tagged with the stakeholder who should resolve it. Write at `.docs/specs/{ticket_key}_questions.md`.

### Phase 3 — Review checkpoint
Pause and display all three artifacts. Wait for the user to type `Approve`, `Edit`, or `Reject` before continuing.

### Constraints
- Do **not** invent ticket history; if the Context Bridge returns nothing, say so.
- Cite the source for every claim ("per PROJ-381 retro", "per PR #287 review thread").
- Cap each artifact at one screen; details belong in linked sub-docs.
