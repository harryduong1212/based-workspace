---
id: smoke-agent
name: Smoke Agent
description: End-to-end smoke test for dispatch_agent — invokes one built-in tool, returns a one-liner.
status: experimental
version: 1
audience: tech
cost: low
tags: [smoke, dispatcher, agent]

about: >-
  Smoke test for the `dispatch_agent` path: spins up an agent, invokes one
  built-in tool (current_time), and returns a one-liner. Used by validate.py
  to confirm the agent runtime + tool wiring is alive — if this fails, no
  agent-type recipe will work. Cheapest end-to-end check in the codebase.
  Costs one Anthropic API call.
highlights:
  - One built-in tool call, one short response — minimum-viable agent path
  - Run by validate.py — if green here, every agent-type recipe can boot
  - Used as the canary when bumping model versions or SDK
examples:
  - label: Run directly
    code: "claude /smoke-agent"
  - label: From validate.py
    code: "python3 scripts/validate.py 2>&1 | grep smoke"

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
