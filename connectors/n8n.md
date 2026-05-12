---
id: n8n
name: n8n Workflow Engine
description: Integration with the n8n automation engine for executing workflow-based recipes.
status: experimental
provides:
  - workflows
auth_type: api_token
requires_env:
  - N8N_WEBHOOK_BASE
  - N8N_API_KEY
tags: [workflow, automation, n8n]
---

## What this is
Connects to an n8n instance to execute workflow-based recipes (e.g. `daily-briefing.md`).

## Setup

1. Add the following to your `.env` file (or use the Control Panel's connector environment editor):
   ```
   N8N_WEBHOOK_BASE=http://localhost:5678
   N8N_API_KEY=<your n8n api key>
   ```

## Used by recipes
- `smoke-echo`
