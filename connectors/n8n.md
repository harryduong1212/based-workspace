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
docs: https://docs.n8n.io/api/
about: >-
  Bridge to the local n8n workflow engine. Every recipe declared as
  `execution.type: workflow` reaches n8n through this connector — the dispatcher
  POSTs to a webhook URL, n8n runs the flow, then calls back to the Control
  Panel with the result. Install writes N8N_WEBHOOK_BASE + N8N_API_KEY to
  `.env`. N8N_WEBHOOK_BASE points at the editor (e.g. http://localhost:5678).
  Advanced: this connector is only useful once the **n8n** container is also
  installed and running — the n8n container provides the engine; this
  connector provides the workflow-trigger contract.
highlights:
  - Triggers n8n workflows via webhook URLs; webhook callbacks return results
  - Required by every `execution.type: workflow` recipe (e.g. daily-briefing)
  - Pairs with the n8n container — install both to use workflow-type recipes
  - Live-check probe hits n8n's `/healthz` endpoint
examples:
  - label: Health check
    code: "curl -s $N8N_WEBHOOK_BASE/healthz"
  - label: Trigger a workflow by webhook (replace UUID)
    code: "curl -X POST -H \"X-N8N-API-KEY: $N8N_API_KEY\" $N8N_WEBHOOK_BASE/webhook/<uuid> -d '{}'"
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
