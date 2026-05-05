"""Recipe runtime dispatcher — Phase E0 scaffold.

Three execution.types map to three dispatch functions. All raise
NotImplementedError until the corresponding phase wires the provider:

    prompt    → dispatch_prompt    (Phase E1; LLM provider decision pending)
    workflow  → dispatch_workflow  (Phase E2 / Phase H; n8n)
    agent     → dispatch_agent     (Phase E3; once Recipes #2/#3 actually need it)
"""
from __future__ import annotations


def dispatch_prompt(fm: dict, prompt_body: str, inputs: dict) -> str:
    """Single AI call with skills loaded into context. Phase E1."""
    raise NotImplementedError("dispatch_prompt not yet wired (Phase E1 — pending LLM provider)")


def dispatch_workflow(fm: dict, inputs: dict) -> str:
    """POST to the n8n webhook at execution.entrypoint. Phase E2 / Phase H."""
    raise NotImplementedError("dispatch_workflow not yet wired (Phase E2/H — pending n8n)")


def dispatch_agent(fm: dict, agent_body: str, inputs: dict) -> str:
    """Agent loop with skills + MCP tools. Phase E3."""
    raise NotImplementedError("dispatch_agent not yet wired (Phase E3)")
