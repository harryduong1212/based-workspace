---
id: test-prompt
name: E1 dispatcher smoke test
description: Minimal prompt recipe used by validate.py to confirm dispatch_prompt is wired (no [STUB]) and to sanity-check the local LLM endpoint.
audience: tech
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [test, infra]

requires_skills: []
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env: []

triggers:
  cli: test-prompt

inputs:
  - name: phrase
    type: string
    required: false
    description: Phrase the model echoes back. Defaults to "ping" when omitted.

outputs:
  - name: reply
    type: markdown
    description: The model's response.

execution:
  type: prompt
  model: gemma-3-4b
---

## What this does
Round-trips a tiny prompt through the recipe runtime so we can verify, without any real workload, that:

1. Frontmatter parses, `execution.type=prompt` validates.
2. The assembler substitutes `{input.phrase}` correctly.
3. The dispatcher reaches the OpenAI-compatible endpoint configured in `.env`.
4. The selected `execution.model` is honored.

## How to run
- Dry run (no LLM call, just shows the assembled envelope):

  `python scripts/recipe_manager.py run test-prompt --dry-run`

- Live (hits the local llama-swap endpoint):

  `python scripts/recipe_manager.py run test-prompt --input phrase=hello`

## Prompt
Reply with exactly the phrase between angle brackets, with no extra text or punctuation.

<{input.phrase}>
