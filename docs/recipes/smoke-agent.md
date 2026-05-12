# Smoke Agent

> End-to-end smoke test for dispatch_agent — invokes one built-in tool, returns a one-liner.
>
> **Audience:** tech · **Status:** experimental · **Cost:** low

| | |
|---|---|
| **Tags** | smoke, dispatcher, agent |
| **Triggers** | CLI: `smoke-agent` · Chat: "smoke agent", "test agent dispatch" |

---

## Agent
Use the `get_current_time` tool exactly once, then reply with a single short sentence in the form:

> The current UTC time is `<ISO timestamp returned by the tool>`.

No other commentary, no markdown formatting, no apologies.

## Why it exists
A failure here means dispatch_agent (tool-use loop, message round-tripping, tool invocation) is broken before any real agent recipe can run. Costs ~$0.001 per execution (Haiku, ~200 tokens round-trip).
