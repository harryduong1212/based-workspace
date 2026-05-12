"""Unit tests for the memory MCP server.

A `_FakeMemory` substitutes for the real mem0 `Memory` so tests don't
need Qdrant + llama-swap running. The factory hook in `server.py`
isolates lazy init for this purpose.
"""
from __future__ import annotations

import importlib.util
import json
import unittest

_HAS_MCP = importlib.util.find_spec("mcp") is not None


class _FakeMemory:
    def __init__(self):
        self.added: list[tuple[str, str]] = []  # (content, user_id)
        self.search_response: list[dict] | None = None

    def add(self, content: str, user_id: str):
        self.added.append((content, user_id))
        return {"id": "mem_1", "memory": content, "event": "ADD", "user_id": user_id}

    def search(self, query: str, user_id: str, limit: int):
        if self.search_response is not None:
            return self.search_response
        return [{"id": "mem_1", "memory": f"matches: {query}", "score": 0.42}]


@unittest.skipUnless(_HAS_MCP, "mcp not installed; skipping memory_mcp tests")
class MemoryMCPServerTest(unittest.TestCase):
    def setUp(self):
        from services.memory_mcp import server

        self.fake = _FakeMemory()
        server.set_memory_factory(lambda: self.fake)
        # Force a re-init in case prior tests instantiated it.
        server._memory = None

    def tearDown(self):
        from services.memory_mcp import server

        server.set_memory_factory(None)
        server._memory = None

    def test_search_memory_returns_json_list_from_mem0(self):
        from services.memory_mcp.server import search_memory

        # The tool may be wrapped by FastMCP; unwrap to call directly.
        fn = getattr(search_memory, "fn", search_memory)
        out = fn(query="hello", k=3)
        parsed = json.loads(out)
        self.assertEqual(parsed, [{"id": "mem_1", "memory": "matches: hello", "score": 0.42}])

    def test_search_passes_query_and_limit_through(self):
        from services.memory_mcp import server
        from services.memory_mcp.server import search_memory

        recorded = {}

        class _Tracker(_FakeMemory):
            def search(self, query, user_id, limit):
                recorded["query"] = query
                recorded["user_id"] = user_id
                recorded["limit"] = limit
                return []

        server.set_memory_factory(_Tracker)
        server._memory = None

        fn = getattr(search_memory, "fn", search_memory)
        fn(query="anything", k=7)
        self.assertEqual(recorded["query"], "anything")
        self.assertEqual(recorded["limit"], 7)
        self.assertEqual(recorded["user_id"], "default")

    def test_add_memory_calls_mem0_add(self):
        from services.memory_mcp.server import add_memory

        fn = getattr(add_memory, "fn", add_memory)
        out = fn(content="user prefers verbose logs", user_id=None)
        parsed = json.loads(out)
        self.assertEqual(parsed["event"], "ADD")
        self.assertEqual(parsed["memory"], "user prefers verbose logs")
        self.assertEqual(self.fake.added, [("user prefers verbose logs", "default")])

    def test_add_memory_honors_explicit_user_id(self):
        from services.memory_mcp.server import add_memory

        fn = getattr(add_memory, "fn", add_memory)
        fn(content="x", user_id="alice")
        self.assertEqual(self.fake.added[-1][1], "alice")

    def test_memory_factory_isolates_real_init(self):
        """If no factory is set, _get_memory should attempt the real import;
        our fixture replaces the factory so this never hits production paths."""
        from services.memory_mcp import server

        # With our factory set in setUp, _get_memory must return the fake.
        m = server._get_memory()
        self.assertIs(m, self.fake)


if __name__ == "__main__":
    unittest.main()
