---
id: daily-briefing
name: Daily Briefing
description: Morning summary of your Jira tickets, Bitbucket PRs, and Gmail inbox.
audience: both
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [briefing, jira, bitbucket, gmail, daily]

about: >-
  Workflow-type recipe that fans out to Jira (your tickets), Bitbucket (your
  open PRs + review requests), and Gmail (recent unread). Each connector
  contributes a section; the recipe condenses the lot into a one-page brief
  for your morning. Runs through n8n (so requires the n8n container) and uses
  the memory MCP to track yesterday's brief for delta-aware framing.
  Advanced: schedule it as a routine to land in your inbox at 7am.
highlights:
  - Three connectors, one consolidated morning brief
  - Workflow-type — n8n fans out the per-connector pulls in parallel
  - Memory-aware — flags "still open from yesterday" items
  - Schedulable as a routine via the Control Panel
examples:
  - label: Run it now
    code: "claude /daily-briefing"
  - label: Schedule as a 7am routine
    code: "claude /schedule '0 7 * * *' /daily-briefing"

requires_skills:
  - debrief-teacher
requires_workflows: []
requires_connectors:
  - jira
  - bitbucket
  - gmail
requires_mcp:
  - memory
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
  entrypoint: n8n-workflows/connectors/daily-briefing.n8n
  async: true
---

## What this does
Pulls your open Jira tickets, pending Bitbucket pull requests, and unread/important Gmail threads, then summarizes what's blocking and what's next. Runs every morning at 8am, or on demand.

## Who it's for
Anyone who starts the day reconciling tickets, reviews, and email across multiple tools. No technical setup beyond connecting your Jira, Bitbucket, and Gmail accounts once.

## What you need
- A Jira account (cloud or server)
- A Bitbucket account
- A Gmail account with 2FA + an app password
- One-time setup: copy `.env.example` → `.env` and fill in `JIRA_*`, `BITBUCKET_*`, `GMAIL_*` (use `./scripts/gen_secrets.sh` for randomizable values), or use the Control Panel's per-connector env editor

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
