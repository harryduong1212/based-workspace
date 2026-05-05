"""Prompt assembler — provider-agnostic message envelope.

Takes a recipe's parsed frontmatter, the body section (extracted via
recipe_manager._extract_section), and the input pairs, and returns a
structured envelope the dispatcher maps onto the chosen provider's
message format.

This module is REAL: substitution + structure are provider-agnostic.
What it does NOT do:
    - Load skill bodies (dispatcher decides loading order for caching)
    - Make LLM calls (that's the dispatcher)
    - Map to Anthropic / Gemini / Ollama specifics (dispatcher again)
"""
from __future__ import annotations
import re

_PLACEHOLDER_RE = re.compile(r"\{input\.(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\}")


def substitute_inputs(text: str, inputs: dict) -> tuple[str, dict]:
    """Replace `{input.X}` placeholders. Returns (substituted, applied_map).

    Missing inputs become empty strings, mirroring how `--input k=v` works
    when an optional input is omitted. Applied map records what was
    substituted (for logging / debugging).
    """
    applied: dict[str, str] = {}

    def _repl(m: re.Match) -> str:
        name = m.group("name")
        value = str(inputs.get(name, ""))
        applied[name] = value
        return value

    return _PLACEHOLDER_RE.sub(_repl, text), applied


def assemble(fm: dict, body_section: str, inputs: dict) -> dict:
    """Build the message envelope for a prompt or agent recipe.

    Args:
        fm: parsed recipe frontmatter
        body_section: the `## Prompt` or `## Agent` section text
            (use recipe_manager._extract_section to get this)
        inputs: substitution dict

    Returns:
        {
          "model": str | None,           # from execution.model; runner picks default if None
          "skill_ids": list[str],        # to be loaded by the dispatcher (cache-stable bundle)
          "recipe_prelude": "",          # reserved for recipe-level system instructions
          "user_message": str,           # substituted body section
          "substitutions": dict,         # what got applied, for debugging
        }
    """
    execu = fm.get("execution") or {}
    user_message, applied = substitute_inputs(body_section or "", inputs)
    return {
        "model": execu.get("model"),
        "skill_ids": list(fm.get("requires_skills") or []),
        "recipe_prelude": "",
        "user_message": user_message,
        "substitutions": applied,
    }
