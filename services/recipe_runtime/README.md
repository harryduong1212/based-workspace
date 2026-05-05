# Recipe Runtime

Python package that owns the `execution.type` dispatch for recipes. Replaces the `[STUB]` branches in `scripts/recipe_manager.py:_execute_recipe`.

## Status

**Phase E0 — scaffold.** Dispatcher functions raise `NotImplementedError`. The provider-agnostic prompt assembler is real (substitution + envelope structure).

Next phases:
- **E1** — wire `dispatch_prompt` against the chosen LLM provider with the two-cache-breakpoint design below.
- **E2** — wire `dispatch_workflow` to POST n8n webhooks (overlaps with Phase H).
- **E3** — wire `dispatch_agent` with skill loading and MCP tool exposure.

## Layout

    services/recipe_runtime/
        dispatcher.py          # dispatch_{prompt,workflow,agent} — currently stubs
        prompt_assembler.py    # substitute_inputs + assemble — real, provider-agnostic
        README.md              # this file

## Cache strategy (Phase E1)

Two breakpoints, mapped onto Anthropic `cache_control` (or the equivalent for whichever provider lands):

1. **Skill bundle** — concatenated bodies of every `requires_skills` entry, in registry order. Longest-stable: identical across every run of any recipe that loads the same skill set.
2. **Skill bundle + recipe prelude** — adds the recipe's own system-level instructions. Medium-stable: changes only when the recipe is edited.

The `## Prompt` body (after `{input.X}` substitution) is the user message and is **not** cacheable — substitutions vary per run.

## Why a separate service?

The dispatcher is the only piece that ever touches an LLM SDK. Keeping it isolated means:

- Provider swap (Anthropic ↔ Gemini ↔ Ollama) touches one package.
- `prompt_assembler` stays unit-testable without any provider auth.
- The CLI (`scripts/recipe_manager.py`) stays thin — it parses, validates, and delegates.
