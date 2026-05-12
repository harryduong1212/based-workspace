"""Tool registry for dispatch_agent.

Two layers:
1. Built-in tools — zero-dependency, safe to expose unconditionally.
2. MCP-spawned tools — declared by the recipe via `requires_mcp` and started
   per-dispatch from `<workspace_root>/.mcp.json`. Each server's tools are
   namespaced as `<server_id>__<tool_name>` so collisions with built-ins and
   across servers are impossible.

Usage:
    with build_tool_runtime(fm, workspace_root=...) as runtime:
        tools = runtime.definitions          # Anthropic-format list[dict]
        out = runtime.invoke(name, args)     # routes to built-in or MCP

The MCP lifecycle is delicate: anyio task scopes used by `stdio_client` and
`ClientSession` require that __aenter__ and __aexit__ run in the same task.
We solve this with a long-running runner coroutine that owns the
`AsyncExitStack` for the whole dispatch — init runs to completion, then the
runner parks on `cleanup_event` until `__exit__` signals it.
"""
from __future__ import annotations

import asyncio
import datetime
import json
import threading
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Awaitable, Callable


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


# A spawner returns a session-like object with `list_tools()` and
# `call_tool(name, args)` async methods. The default uses the real MCP SDK;
# tests inject a fake.
MCPSpawner = Callable[[AsyncExitStack, str, dict], Awaitable[Any]]


async def _default_mcp_spawner(stack: AsyncExitStack, server_id: str, config: dict):
    # Lazy import so recipes without requires_mcp never pay the import cost.
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    del server_id  # accepted for protocol parity / debugging; not needed by stdio_client
    params = StdioServerParameters(
        command=config["command"],
        args=list(config.get("args") or []),
        env=config.get("env"),
        cwd=config.get("cwd"),
    )
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()
    return session


def _load_mcp_configs(workspace_root: str | None, server_ids: list[str]) -> dict[str, dict]:
    if not workspace_root:
        raise RuntimeError("workspace_root is required to resolve requires_mcp")
    path = Path(workspace_root) / ".mcp.json"
    if not path.exists():
        raise FileNotFoundError(
            f"requires_mcp declared but {path} not found — copy .mcp.json.example to .mcp.json"
        )
    doc = json.loads(path.read_text(encoding="utf-8"))
    all_servers = doc.get("mcpServers") or {}
    resolved: dict[str, dict] = {}
    missing: list[str] = []
    for sid in server_ids:
        cfg = all_servers.get(sid)
        if cfg is None:
            missing.append(sid)
        else:
            resolved[sid] = cfg
    if missing:
        raise KeyError(
            f"requires_mcp servers not present in .mcp.json: {missing}"
        )
    return resolved


def _format_mcp_result(result: Any) -> str:
    """Flatten a CallToolResult's content blocks into a single string."""
    parts: list[str] = []
    for block in (getattr(result, "content", None) or []):
        text = getattr(block, "text", None)
        if isinstance(text, str):
            parts.append(text)
        else:
            parts.append(repr(block))
    body = "".join(parts)
    if getattr(result, "isError", False):
        return f"error: {body}" if body else "error: tool reported error"
    return body


class ToolRuntime:
    """Context-managed catalog + invoker for one dispatch_agent run.

    Built-ins are always available. MCP servers declared in
    `fm["requires_mcp"]` are spawned on __enter__ and torn down on __exit__.
    """

    def __init__(
        self,
        fm: dict,
        workspace_root: str | None,
        mcp_spawner: MCPSpawner | None = None,
    ):
        self._fm = fm or {}
        self._workspace_root = workspace_root
        self._mcp_spawner: MCPSpawner = mcp_spawner or _default_mcp_spawner
        self.definitions: list[dict] = []
        self._sessions: dict[str, Any] = {}
        self._route: dict[str, tuple[str, str]] = {}
        self._loop: asyncio.AbstractEventLoop | None = None
        self._loop_thread: threading.Thread | None = None
        self._loop_ready = threading.Event()
        self._runner_future = None
        self._cleanup_event: asyncio.Event | None = None
        self._init_done = threading.Event()
        self._init_error: BaseException | None = None

    # ---- context manager ----

    def __enter__(self) -> "ToolRuntime":
        for spec in BUILT_IN_TOOLS.values():
            self.definitions.append(spec["definition"])

        mcp_ids = [s for s in (self._fm.get("requires_mcp") or []) if s]
        if not mcp_ids:
            return self

        configs = _load_mcp_configs(self._workspace_root, mcp_ids)
        self._start_loop()
        self._runner_future = asyncio.run_coroutine_threadsafe(
            self._runner(configs), self._loop
        )
        if not self._init_done.wait(timeout=30):
            self._teardown()
            raise TimeoutError("MCP runtime init exceeded 30s")
        if self._init_error is not None:
            err = self._init_error
            self._teardown()
            raise err
        return self

    def __exit__(self, *_exc) -> None:
        self._teardown()

    # ---- public API ----

    def invoke(self, name: str, args: dict | None) -> str:
        spec = BUILT_IN_TOOLS.get(name)
        if spec is not None:
            return spec["fn"](args or {}, workspace_root=self._workspace_root)

        route = self._route.get(name)
        if route is None:
            return f"error: unknown tool {name!r}"
        if self._loop is None or self._loop.is_closed():
            return "error: MCP runtime is not active"

        server_id, real_name = route
        session = self._sessions.get(server_id)
        if session is None:
            return f"error: MCP session {server_id!r} not initialized"
        try:
            fut = asyncio.run_coroutine_threadsafe(
                session.call_tool(real_name, args or {}), self._loop
            )
            result = fut.result(timeout=60)
        except Exception as e:  # noqa: BLE001 — surface to the agent
            return f"error: {type(e).__name__}: {e}"
        return _format_mcp_result(result)

    # ---- loop plumbing ----

    def _start_loop(self) -> None:
        loop = asyncio.new_event_loop()

        def _run():
            asyncio.set_event_loop(loop)
            self._loop = loop
            self._loop_ready.set()
            try:
                loop.run_forever()
            finally:
                try:
                    loop.close()
                except Exception:
                    pass

        t = threading.Thread(target=_run, name="mcp-runtime-loop", daemon=True)
        t.start()
        self._loop_thread = t
        if not self._loop_ready.wait(timeout=5):
            raise TimeoutError("MCP runtime loop did not start")

    def _stop_loop(self) -> None:
        if self._loop is None:
            return
        try:
            self._loop.call_soon_threadsafe(self._loop.stop)
        except RuntimeError:
            pass
        if self._loop_thread is not None:
            self._loop_thread.join(timeout=5)
        self._loop = None
        self._loop_thread = None

    def _teardown(self) -> None:
        # Signal the runner to exit; that unwinds the AsyncExitStack inside
        # its own task (anyio cancel-scope correctness).
        if self._cleanup_event is not None and self._loop is not None:
            try:
                self._loop.call_soon_threadsafe(self._cleanup_event.set)
            except RuntimeError:
                pass
        if self._runner_future is not None:
            try:
                self._runner_future.result(timeout=10)
            except Exception:
                pass
            self._runner_future = None
        self._stop_loop()

    async def _runner(self, configs: dict[str, dict]) -> None:
        """Long-lived coroutine: own the stack, init sessions, park, then unwind."""
        cleanup_event = asyncio.Event()
        self._cleanup_event = cleanup_event
        try:
            async with AsyncExitStack() as stack:
                for server_id, cfg in configs.items():
                    session = await self._mcp_spawner(stack, server_id, cfg)
                    self._sessions[server_id] = session
                    tools_result = await session.list_tools()
                    for tool in tools_result.tools:
                        ns = f"{server_id}__{tool.name}"
                        self._route[ns] = (server_id, tool.name)
                        self.definitions.append(
                            {
                                "name": ns,
                                "description": (
                                    tool.description or f"MCP tool from {server_id}"
                                ),
                                "input_schema": tool.inputSchema
                                or {"type": "object", "properties": {}, "required": []},
                            }
                        )
                self._init_done.set()
                await cleanup_event.wait()
        except BaseException as e:  # noqa: BLE001 — propagate init failures
            if not self._init_done.is_set():
                self._init_error = e
                self._init_done.set()
            else:
                # Failure happened post-init (e.g., during cleanup) — swallow.
                pass


def build_tool_runtime(
    fm: dict,
    *,
    workspace_root: str | None,
    mcp_spawner: MCPSpawner | None = None,
) -> ToolRuntime:
    return ToolRuntime(fm, workspace_root, mcp_spawner)
