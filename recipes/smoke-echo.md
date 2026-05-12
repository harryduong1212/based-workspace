---
id: smoke-echo
name: Smoke Echo
description: End-to-end smoke test for the workflow-dispatch path. Webhook → callback round-trip with no external creds.
status: experimental
version: 1
audience: tech
cost: low
tags: [smoke, dispatcher]
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
