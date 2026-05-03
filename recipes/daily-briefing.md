---
id: daily-briefing
name: Daily Briefing
description: Morning summary of your Jira tickets and Bitbucket PRs.
audience: both
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [briefing, jira, bitbucket, daily]

requires_skills:
  - debrief-teacher
requires_workflows: []
requires_connectors:
  - jira
  - bitbucket
requires_mcp:
  - postgres-memory
requires_env:
  - JIRA_BASE_URL

triggers:
  cli: daily-briefing
  chat:
    - "morning briefing"
    - "daily summary"
  webhook: /recipes/daily-briefing
  schedule: "0 8 * * *"

inputs:
  - name: focus_project
    type: string
    required: false
    description: Jira project key to scope to.

outputs:
  - name: summary
    type: markdown
    description: Rendered briefing.

execution:
  type: workflow
  entrypoint: n8n-workflows/daily-briefing.n8n
---

## What this does
Pulls your open Jira tickets and pending Bitbucket pull requests, summarizes what's blocking and what's next, and delivers the result to your inbox or chat. Runs every morning at 8am, or on demand.

## Who it's for
Anyone who starts the day reconciling tickets and reviews across multiple tools. No technical setup beyond connecting your Jira and Bitbucket accounts once.

## What you need
- A Jira account (cloud or server)
- A Bitbucket account
- One-time setup: `python scripts/setup_env.py` to store credentials

## How to run
- **In Antigravity or Claude:** say *"morning briefing"* or *"daily summary"*.
- **CLI:** `python scripts/recipe_manager.py run daily-briefing`
- **Scheduled:** runs automatically at 8am once the routine is enabled.
- **Scope to one project:** `... run daily-briefing --input focus_project=PROJ`

## Example output

> **Daily Briefing — 2026-05-01**
>
> **In progress (3)**
> - PROJ-412 — API rate limiting — blocked on review
> - PROJ-419 — Audit log retention — design phase
> - PROJ-421 — Webhook retries — implementation
>
> **Awaiting your review (2)**
> - PR #287 — Migrate auth middleware (3 days old)
> - PR #291 — Add structured logging
>
> **Suggested focus:** unblock PROJ-412 by reviewing PR #287.
