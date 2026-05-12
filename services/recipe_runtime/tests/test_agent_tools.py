"""Unit tests for the MCP-aware ToolRuntime.

We never spawn a real MCP server here — those would require subprocess +
network setup. Instead we inject a fake `mcp_spawner` that returns a stub
session honoring the same `list_tools()` / `call_tool(name, args)` async
interface, and verify:
  - built-ins are always exposed
  - MCP tools are namespaced and added to definitions
  - invoke() routes to the right session and stringifies results
  - errors propagate as `error: ...` strings without breaking the loop
  - cleanup runs (spawner __aexit__ is reached)
"""
from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import AsyncExitStack
from pathlib import Path
from types import SimpleNamespace

from services.recipe_runtime.agent_tools import (
    BUILT_IN_TOOLS,
    _format_mcp_result,
    _load_mcp_configs,
    build_tool_runtime,
)


class _FakeSession:
    """Stand-in for mcp.ClientSession. Records call_tool invocations."""

    def __init__(self, server_id: str, tools: list[dict], call_response=None):
        self.server_id = server_id
        self._tool_descriptors = tools
        self.call_response = call_response
        self.calls: list[tuple[str, dict]] = []

    async def list_tools(self):
        tools = [
            SimpleNamespace(
                name=t["name"],
                description=t.get("description", ""),
                inputSchema=t.get(
                    "inputSchema",
                    {"type": "object", "properties": {}, "required": []},
                ),
            )
            for t in self._tool_descriptors
        ]
        return SimpleNamespace(tools=tools)

    async def call_tool(self, name: str, args: dict):
        self.calls.append((name, dict(args)))
        if callable(self.call_response):
            return self.call_response(name, args)
        if self.call_response is not None:
            return self.call_response
        return SimpleNamespace(
            content=[SimpleNamespace(text=f"{self.server_id}:{name}:ok")],
            isError=False,
        )


def _make_spawner(sessions_by_id: dict[str, _FakeSession], track: dict | None = None):
    """Spawner that registers the fake session into the AsyncExitStack."""

    async def _spawner(stack: AsyncExitStack, server_id: str, config: dict):
        del config  # fake spawner doesn't need it; real one passes it to StdioServerParameters
        if track is not None:
            track.setdefault("spawned", []).append(server_id)

        class _Ctx:
            async def __aenter__(self_inner):
                return sessions_by_id[server_id]

            async def __aexit__(self_inner, *_exc):
                if track is not None:
                    track.setdefault("cleaned", []).append(server_id)
                return False

        return await stack.enter_async_context(_Ctx())

    return _spawner


class ToolRuntimeBuiltinTest(unittest.TestCase):
    def test_builtins_always_present_when_no_requires_mcp(self):
        with build_tool_runtime({}, workspace_root=None) as runtime:
            names = {d["name"] for d in runtime.definitions}
        self.assertEqual(names, set(BUILT_IN_TOOLS.keys()))

    def test_builtin_invoke_returns_string(self):
        with build_tool_runtime({}, workspace_root=None) as runtime:
            out = runtime.invoke("get_current_time", {})
        self.assertIn("T", out)  # ISO 8601 separator

    def test_unknown_tool_returns_error_string(self):
        with build_tool_runtime({}, workspace_root=None) as runtime:
            self.assertEqual(runtime.invoke("does_not_exist", {}), "error: unknown tool 'does_not_exist'")


class ToolRuntimeMCPTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "ctx": {"command": "/bin/true", "args": []},
                        "notes": {"command": "/bin/true", "args": []},
                    }
                }
            )
        )

    def test_mcp_tools_appear_namespaced(self):
        sessions = {
            "ctx": _FakeSession(
                "ctx",
                [{"name": "search", "description": "ctx search"}],
            ),
        }
        fm = {"requires_mcp": ["ctx"]}
        with build_tool_runtime(
            fm,
            workspace_root=str(self.root),
            mcp_spawner=_make_spawner(sessions),
        ) as runtime:
            names = {d["name"] for d in runtime.definitions}
        # Built-ins + namespaced MCP tool
        self.assertIn("get_current_time", names)
        self.assertIn("ctx__search", names)

    def test_invoke_routes_to_correct_session(self):
        sessions = {
            "ctx": _FakeSession("ctx", [{"name": "search"}]),
            "notes": _FakeSession("notes", [{"name": "create"}]),
        }
        fm = {"requires_mcp": ["ctx", "notes"]}
        with build_tool_runtime(
            fm,
            workspace_root=str(self.root),
            mcp_spawner=_make_spawner(sessions),
        ) as runtime:
            out_ctx = runtime.invoke("ctx__search", {"q": "hello"})
            out_notes = runtime.invoke("notes__create", {"title": "x"})

        self.assertEqual(out_ctx, "ctx:search:ok")
        self.assertEqual(out_notes, "notes:create:ok")
        self.assertEqual(sessions["ctx"].calls, [("search", {"q": "hello"})])
        self.assertEqual(sessions["notes"].calls, [("create", {"title": "x"})])

    def test_call_tool_iserror_prefixed(self):
        err_result = SimpleNamespace(
            content=[SimpleNamespace(text="rate limited")],
            isError=True,
        )
        sessions = {
            "ctx": _FakeSession("ctx", [{"name": "search"}], call_response=err_result),
        }
        with build_tool_runtime(
            {"requires_mcp": ["ctx"]},
            workspace_root=str(self.root),
            mcp_spawner=_make_spawner(sessions),
        ) as runtime:
            out = runtime.invoke("ctx__search", {})
        self.assertEqual(out, "error: rate limited")

    def test_call_tool_exception_becomes_error_string(self):
        def _raise(_n, _a):
            raise RuntimeError("kaboom")

        sessions = {
            "ctx": _FakeSession("ctx", [{"name": "search"}], call_response=_raise),
        }
        with build_tool_runtime(
            {"requires_mcp": ["ctx"]},
            workspace_root=str(self.root),
            mcp_spawner=_make_spawner(sessions),
        ) as runtime:
            out = runtime.invoke("ctx__search", {})
        self.assertTrue(out.startswith("error: RuntimeError: kaboom"), out)

    def test_cleanup_runs_for_each_server(self):
        sessions = {
            "ctx": _FakeSession("ctx", [{"name": "search"}]),
            "notes": _FakeSession("notes", [{"name": "create"}]),
        }
        track: dict = {}
        with build_tool_runtime(
            {"requires_mcp": ["ctx", "notes"]},
            workspace_root=str(self.root),
            mcp_spawner=_make_spawner(sessions, track=track),
        ) as runtime:
            self.assertEqual(track.get("spawned"), ["ctx", "notes"])
        self.assertEqual(sorted(track.get("cleaned") or []), ["ctx", "notes"])

    def test_init_failure_surfaces_and_cleans_up(self):
        async def _bad_spawner(_stack, _sid, _cfg):
            raise ValueError("could not start server")

        with self.assertRaisesRegex(ValueError, "could not start server"):
            with build_tool_runtime(
                {"requires_mcp": ["ctx"]},
                workspace_root=str(self.root),
                mcp_spawner=_bad_spawner,
            ):
                self.fail("should not enter body on init failure")

    def test_missing_mcp_config_raises_keyerror(self):
        with self.assertRaises(KeyError):
            with build_tool_runtime(
                {"requires_mcp": ["does-not-exist"]},
                workspace_root=str(self.root),
                mcp_spawner=_make_spawner({}),
            ):
                pass

    def test_missing_mcp_json_raises_filenotfound(self):
        empty_root = Path(self.tmp.name) / "empty"
        empty_root.mkdir()
        with self.assertRaises(FileNotFoundError):
            with build_tool_runtime(
                {"requires_mcp": ["ctx"]},
                workspace_root=str(empty_root),
                mcp_spawner=_make_spawner({}),
            ):
                pass


class LoadMCPConfigsTest(unittest.TestCase):
    def test_returns_only_requested_servers(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / ".mcp.json").write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "a": {"command": "x"},
                            "b": {"command": "y"},
                            "c": {"command": "z"},
                        }
                    }
                )
            )
            got = _load_mcp_configs(d, ["a", "c"])
        self.assertEqual(set(got.keys()), {"a", "c"})


class FormatMCPResultTest(unittest.TestCase):
    def test_concatenates_text_blocks(self):
        result = SimpleNamespace(
            content=[
                SimpleNamespace(text="hello "),
                SimpleNamespace(text="world"),
            ],
            isError=False,
        )
        self.assertEqual(_format_mcp_result(result), "hello world")

    def test_error_prefix(self):
        result = SimpleNamespace(
            content=[SimpleNamespace(text="bad input")], isError=True
        )
        self.assertEqual(_format_mcp_result(result), "error: bad input")

    def test_empty_content_with_error(self):
        result = SimpleNamespace(content=[], isError=True)
        self.assertEqual(_format_mcp_result(result), "error: tool reported error")


if __name__ == "__main__":
    unittest.main()
