# Recipe Runtime

Python package that owns the `execution.type` dispatch for recipes. Replaces the `[STUB]` branches in `scripts/recipe_manager.py:_execute_recipe`.

## Status

**Phase E1/E2 — wired.** `dispatch_prompt` and `dispatch_workflow` are real. `dispatch_agent` is the remaining stub.

- **E1** — `dispatch_prompt` routes via the provider registry in `providers/`. Multi-provider: `local` (llama-swap / OpenAI-compatible), `anthropic`, `gemini`. Cache strategy with two breakpoints is designed but not yet provider-implemented.
- **E2/H** — `dispatch_workflow` POSTs to n8n webhooks via `urllib`. Supports sync and async (callback) modes. The callback receiver lives in `services/control_panel/api.py` at `POST /api/v1/n8n/callback/{run_id}`.
- **E3** — `dispatch_agent` — **not yet wired**. Will implement the agent loop with skill loading and MCP tool exposure.

## Layout

    services/recipe_runtime/
        dispatcher.py          # dispatch_{prompt,workflow,agent}
        prompt_assembler.py    # substitute_inputs + assemble — real, provider-agnostic
        providers/             # provider registry + per-provider modules
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
