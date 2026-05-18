---
id: smoke-echo
name: Smoke Echo
description: End-to-end smoke test for the workflow-dispatch path. Webhook → callback round-trip with no external creds.
status: experimental
version: 1
audience: tech
cost: low
tags: [smoke, dispatcher]

about: >-
  Smoke test for `dispatch_workflow`: dispatcher POSTs to an n8n webhook,
  n8n calls back to the Control Panel with the result, the recipe returns
  the echoed payload. No external API creds needed (the n8n flow is purely
  local). Used by validate.py + as the canary when touching the
  workflow-dispatch contract.
highlights:
  - Workflow round-trip with zero external creds — purely local
  - The canary for any n8n container / webhook contract change
  - Run by validate.py — if green here, all workflow-type recipes can boot
examples:
  - label: Run directly
    code: "claude /smoke-echo"

requires_skills: []
requires_workflows: []
requires_connectors:
  - n8n
requires_mcp: []
requires_env:
  - N8N_WEBHOOK_BASE

triggers:
  cli: smoke-echo
  chat:
    - smoke echo
    - test workflow dispatch

inputs:
  - name: message
    description: Anything — gets echoed back via the callback.

outputs:
  - name: echo
    type: markdown
    description: "echo: <message>"

execution:
  type: workflow
  entrypoint: n8n-workflows/connectors/smoke-echo.n8n
  async: true
---

## What this does
Validates the dispatcher → n8n webhook → callback path end-to-end. No external service required.

## Why it exists
A failure here means the workflow execution model itself is broken before any real recipe (daily-briefing, etc.) can run. Use this any time the n8n integration changes (image upgrade, encryption key rotation, host port shift) to verify the loop still works.
