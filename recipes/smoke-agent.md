---
id: smoke-agent
name: Smoke Agent
description: End-to-end smoke test for dispatch_agent — invokes one built-in tool, returns a one-liner.
status: experimental
version: 1
audience: tech
cost: low
tags: [smoke, dispatcher, agent]
requires_skills: []
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env:
  - ANTHROPIC_API_KEY

triggers:
  cli: smoke-agent
  chat:
    - smoke agent
    - test agent dispatch

inputs: []

outputs:
  - name: confirmation
    type: markdown
    description: One-line confirmation that the tool call worked.

execution:
  type: agent
  model: anthropic/claude-haiku-4-5-20251001
---

## Agent
Use the `get_current_time` tool exactly once, then reply with a single short sentence in the form:

> The current UTC time is `<ISO timestamp returned by the tool>`.

No other commentary, no markdown formatting, no apologies.

## Why it exists
A failure here means dispatch_agent (tool-use loop, message round-tripping, tool invocation) is broken before any real agent recipe can run. Costs ~$0.001 per execution (Haiku, ~200 tokens round-trip).
