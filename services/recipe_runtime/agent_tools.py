"""Tool registry for dispatch_agent.

Two layers:
1. Built-in tools — zero-dependency, safe to expose unconditionally. Used to
   smoke-test the tool-use loop and to give recipe authors a baseline kit.
2. MCP-spawned tools — declared by the recipe via `requires_mcp` and started
   on demand. Deferred to a follow-up commit (Phase E3.5).

The Anthropic Messages API tool format is `{name, description, input_schema}`
where input_schema is JSON Schema. We mirror that shape in `definition` so
the dispatcher can pass it through untouched.
"""
from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Callable


def _tool_get_current_time(_args: dict, **_kwargs: Any) -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _tool_read_workspace_file(args: dict, *, workspace_root: str | None, **_kwargs: Any) -> str:
    if not workspace_root:
        return "error: workspace_root not configured for this dispatch"
    rel = args.get("path") or ""
    if not rel:
        return "error: missing required argument 'path'"
    root = Path(workspace_root).resolve()
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return "error: path escapes workspace root"
    if not target.is_file():
        return f"error: not a file: {rel}"
    text = target.read_text(encoding="utf-8", errors="replace")
    if len(text) > 10_000:
        return text[:10_000] + "\n... [truncated]"
    return text


BUILT_IN_TOOLS: dict[str, dict[str, Any]] = {
    "get_current_time": {
        "definition": {
            "name": "get_current_time",
            "description": "Return the current time in ISO 8601 UTC format.",
            "input_schema": {"type": "object", "properties": {}, "required": []},
        },
        "fn": _tool_get_current_time,
    },
    "read_workspace_file": {
        "definition": {
            "name": "read_workspace_file",
            "description": (
                "Read a UTF-8 text file from the workspace. Returns the first ~10 kB."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path relative to workspace root.",
                    },
                },
                "required": ["path"],
            },
        },
        "fn": _tool_read_workspace_file,
    },
}


def get_tool_catalog(fm: dict, *, workspace_root: str | None) -> list[dict]:
    """Return the Anthropic-format tool definitions exposed to this agent run.

    For now this is the static built-in set. Once MCP wiring lands, we'll
    spawn MCP servers declared in `fm["requires_mcp"]` and merge their
    `list_tools()` output here.
    """
    del fm, workspace_root  # reserved for MCP integration
    return [t["definition"] for t in BUILT_IN_TOOLS.values()]


def invoke_tool(name: str, args: dict, *, workspace_root: str | None = None) -> str:
    """Run a tool and return its output as a string (safe for tool_result)."""
    spec = BUILT_IN_TOOLS.get(name)
    if spec is None:
        return f"error: unknown tool {name!r}"
    fn: Callable[..., str] = spec["fn"]
    return fn(args or {}, workspace_root=workspace_root)
