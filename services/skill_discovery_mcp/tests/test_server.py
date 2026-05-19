"""Tests for the FastMCP tool surface — exercises `find_skills` via the
module-level `set_test_doubles` seam with fake Embedder + fake SkillStore.
No live Qdrant / llama-swap needed."""
from __future__ import annotations

import json
import unittest
from typing import Any

try:
    import mcp  # noqa: F401 — import probe
    _HAS_MCP = True
except ImportError:
    _HAS_MCP = False


class _FakeEmbedder:
    def __init__(self, vector: list[float] | None = None, raises: Exception | None = None) -> None:
        self._vector = vector or [0.1, 0.2, 0.3]
        self._raises = raises
        self.calls: list[str] = []

    def embed_one(self, text: str) -> list[float]:
        self.calls.append(text)
        if self._raises is not None:
            raise self._raises
        return list(self._vector)


class _FakeStore:
    def __init__(self, hits: list[dict[str, Any]] | None = None, count: int = 0) -> None:
        self._hits = hits or []
        self._count = count
        self.searches: list[tuple[list[float], int]] = []

    @property
    def collection(self) -> str:
        return "based_skills"

    def search(self, query_vector: list[float], k: int = 5) -> list[dict[str, Any]]:
        self.searches.append((list(query_vector), k))
        return list(self._hits)

    def count(self) -> int:
        return self._count


@unittest.skipUnless(_HAS_MCP, "mcp package not installed")
class FindSkillsTests(unittest.TestCase):
    def setUp(self) -> None:
        from services.skill_discovery_mcp import server

        self._server = server
        server.reset_test_doubles()

    def tearDown(self) -> None:
        self._server.reset_test_doubles()

    def test_returns_json_list_of_hits(self) -> None:
        emb = _FakeEmbedder(vector=[0.5] * 384)
        store = _FakeStore(hits=[
            {"name": "react-best-practices", "description": "...", "score": 0.91, "category": "frontend-core"},
            {"name": "vector-database-engineer", "description": "...", "score": 0.62, "category": "data-vector"},
        ])
        self._server.set_test_doubles(embedder=emb, store=store)  # type: ignore[arg-type]

        out = getattr(self._server.find_skills, "fn", self._server.find_skills)("how do I memoize a React render?", k=2)  # type: ignore[attr-defined]
        decoded = json.loads(out)
        self.assertEqual(len(decoded), 2)
        self.assertEqual(decoded[0]["name"], "react-best-practices")
        self.assertEqual(emb.calls, ["how do I memoize a React render?"])
        self.assertEqual(store.searches[-1][1], 2)

    def test_empty_query_returns_empty_array_no_embed(self) -> None:
        emb = _FakeEmbedder()
        store = _FakeStore()
        self._server.set_test_doubles(embedder=emb, store=store)  # type: ignore[arg-type]

        self.assertEqual(json.loads(getattr(self._server.find_skills, "fn", self._server.find_skills)("   ", k=5)), [])  # type: ignore[attr-defined]
        self.assertEqual(emb.calls, [])  # never embedded

    def test_k_is_clamped_to_25(self) -> None:
        emb = _FakeEmbedder()
        store = _FakeStore()
        self._server.set_test_doubles(embedder=emb, store=store)  # type: ignore[arg-type]

        getattr(self._server.find_skills, "fn", self._server.find_skills)("query", k=99999)  # type: ignore[attr-defined]
        self.assertEqual(store.searches[-1][1], 25)

    def test_k_floor_is_one(self) -> None:
        emb = _FakeEmbedder()
        store = _FakeStore()
        self._server.set_test_doubles(embedder=emb, store=store)  # type: ignore[arg-type]

        getattr(self._server.find_skills, "fn", self._server.find_skills)("query", k=0)  # type: ignore[attr-defined]
        self.assertEqual(store.searches[-1][1], 1)

    def test_embedder_error_propagates_as_runtime_error(self) -> None:
        from services.skill_discovery_mcp.embedder import EmbedderError

        emb = _FakeEmbedder(raises=EmbedderError("backend unreachable"))
        store = _FakeStore()
        self._server.set_test_doubles(embedder=emb, store=store)  # type: ignore[arg-type]

        with self.assertRaises(RuntimeError) as ctx:
            getattr(self._server.find_skills, "fn", self._server.find_skills)("query")  # type: ignore[attr-defined]
        self.assertIn("backend unreachable", str(ctx.exception))


@unittest.skipUnless(_HAS_MCP, "mcp package not installed")
class SkillIndexStatsTests(unittest.TestCase):
    def setUp(self) -> None:
        from services.skill_discovery_mcp import server

        self._server = server
        server.reset_test_doubles()

    def tearDown(self) -> None:
        self._server.reset_test_doubles()

    def test_reports_collection_and_count(self) -> None:
        store = _FakeStore(count=130)
        self._server.set_test_doubles(store=store)  # type: ignore[arg-type]
        payload = json.loads(getattr(self._server.skill_index_stats, "fn", self._server.skill_index_stats)())  # type: ignore[attr-defined]
        self.assertEqual(payload["collection"], "based_skills")
        self.assertEqual(payload["points"], 130)

    def test_swallows_store_errors_into_payload(self) -> None:
        class _Boom:
            collection = "based_skills"

            def count(self) -> int:
                raise RuntimeError("qdrant down")

        self._server.set_test_doubles(store=_Boom())  # type: ignore[arg-type]
        payload = json.loads(getattr(self._server.skill_index_stats, "fn", self._server.skill_index_stats)())  # type: ignore[attr-defined]
        self.assertIsNone(payload["points"])
        self.assertIn("qdrant down", payload["error"])


if __name__ == "__main__":
    unittest.main()
