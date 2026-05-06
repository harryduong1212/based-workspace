---
description: Minimal prompt recipe used by validate.py to confirm dispatch_prompt is wired (no [STUB]) and to sanity-check the local LLM endpoint.
argument-hint: [--input phrase=<value>]
---

<!-- Generated from recipes/test-prompt.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_claude_code.py`. -->

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
