"""Unit tests for the Context Bridge MCP server tool.

Targets `_search_context_impl` directly with injected fake embedder and
fake VectorStore — no MCP transport, no llama-swap, no Postgres.
"""
from __future__ import annotations

import unittest

from services.context_bridge.store import Document
from services.context_bridge_mcp.server import _search_context_impl, app, search_context


class _FakeEmbedder:
    def __init__(self, vec=None):
        self.vec = vec if vec is not None else [0.1] * 384
        self.calls: list[list[str]] = []

    def embed(self, texts):
        self.calls.append(list(texts))
        return [self.vec for _ in texts]


class _FakeVectorStore:
    def __init__(self, results):
        self.results = results
        self.calls: list[dict] = []

    def search(self, vec, k=5, *, source=None):
        self.calls.append({"vec": vec, "k": k, "source": source})
        return self.results


def _doc(source="jira", source_id="X-1", *, content="c", metadata=None):
    return Document(
        source=source,
        source_id=source_id,
        chunk_idx=0,
        content=content,
        embedding=[],
        metadata={"summary": "S"} if metadata is None else metadata,
    )


class SearchContextImplTest(unittest.TestCase):
    def test_empty_query_short_circuits(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([])
        self.assertEqual(_search_context_impl("", embedder=emb, vector_store=store), [])
        self.assertEqual(_search_context_impl("   ", embedder=emb, vector_store=store), [])
        self.assertEqual(emb.calls, [])
        self.assertEqual(store.calls, [])

    def test_zero_or_negative_k_short_circuits(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([])
        self.assertEqual(
            _search_context_impl("q", k=0, embedder=emb, vector_store=store),
            [],
        )
        self.assertEqual(
            _search_context_impl("q", k=-3, embedder=emb, vector_store=store),
            [],
        )
        self.assertEqual(emb.calls, [])

    def test_calls_embedder_and_store_with_query(self):
        emb = _FakeEmbedder(vec=[0.5] * 384)
        store = _FakeVectorStore([(_doc(), 0.12)])
        _search_context_impl("rate limiting", k=3, embedder=emb, vector_store=store)
        self.assertEqual(emb.calls, [["rate limiting"]])
        self.assertEqual(store.calls[0]["k"], 3)
        self.assertEqual(store.calls[0]["vec"], [0.5] * 384)
        self.assertIsNone(store.calls[0]["source"])

    def test_source_filter_passes_through(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([])
        _search_context_impl("q", source="jira", embedder=emb, vector_store=store)
        self.assertEqual(store.calls[0]["source"], "jira")

    def test_default_k_is_5(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([])
        _search_context_impl("q", embedder=emb, vector_store=store)
        self.assertEqual(store.calls[0]["k"], 5)

    def test_result_shape_includes_required_keys(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([
            (_doc(source_id="PROJ-1", content="hello", metadata={"summary": "S"}), 0.1),
        ])
        out = _search_context_impl("q", embedder=emb, vector_store=store)
        self.assertEqual(len(out), 1)
        r = out[0]
        for key in ("source", "source_id", "chunk_idx", "content", "summary", "distance", "metadata"):
            self.assertIn(key, r)
        self.assertEqual(r["source"], "jira")
        self.assertEqual(r["source_id"], "PROJ-1")
        self.assertEqual(r["content"], "hello")
        self.assertEqual(r["summary"], "S")
        self.assertAlmostEqual(r["distance"], 0.1)

    def test_summary_falls_back_to_title_for_bitbucket(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([
            (_doc(source="bitbucket", source_id="287",
                  metadata={"title": "Auth migration", "state": "OPEN"}), 0.2),
        ])
        [r] = _search_context_impl("q", embedder=emb, vector_store=store)
        self.assertEqual(r["summary"], "Auth migration")

    def test_summary_is_none_when_neither_summary_nor_title_present(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([(_doc(metadata={}), 0.1)])
        [r] = _search_context_impl("q", embedder=emb, vector_store=store)
        self.assertIsNone(r["summary"])

    def test_results_preserve_store_ordering(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([
            (_doc(source_id="A"), 0.1),
            (_doc(source_id="B"), 0.4),
            (_doc(source_id="C"), 0.7),
        ])
        out = _search_context_impl("q", embedder=emb, vector_store=store)
        self.assertEqual([r["source_id"] for r in out], ["A", "B", "C"])

    def test_distance_is_float_not_decimal(self):
        emb = _FakeEmbedder()
        store = _FakeVectorStore([(_doc(), 0.5)])
        [r] = _search_context_impl("q", embedder=emb, vector_store=store)
        self.assertIsInstance(r["distance"], float)


class ToolRegistrationTest(unittest.TestCase):
    """Smoke: the FastMCP app actually has the tool registered."""

    def test_search_context_is_registered(self):
        # FastMCP keeps tools accessible via list_tools() async, but the
        # decorator also wraps the callable so we can call it directly.
        self.assertTrue(callable(search_context))
        self.assertEqual(search_context.__name__, "search_context")

    def test_app_named_context_bridge(self):
        self.assertEqual(app.name, "context-bridge")


if __name__ == "__main__":
    unittest.main()
