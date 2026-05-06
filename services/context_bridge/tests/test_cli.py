"""Unit tests for context_bridge.cli — focused on the pure pipeline.

`_build_docs` is the testable seam: payload + adapter → list[Document]
with no IO and no DB. The embedder is replaced with a fake that returns
deterministic vectors and records the texts it was asked to embed.
"""
from __future__ import annotations

import unittest

from services.context_bridge.cli import _build_docs


class _FakeEmbedder:
    """Returns a vector with all dims = chunk_idx-of-call, dimension = `dim`."""

    def __init__(self, dim: int = 384):
        self.dim = dim
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(list(texts))
        return [[float(i)] * self.dim for i, _ in enumerate(texts)]


def _adapter_yielding(*records):
    """Build an adapter that yields the given (source_id, content, metadata) records."""
    def adapt(payload):
        for r in records:
            yield r
    return adapt


class BuildDocsPipelineTest(unittest.TestCase):
    def test_empty_adapter_yields_no_docs(self):
        emb = _FakeEmbedder()
        docs = _build_docs({}, "jira", target_tokens=512, embedder=emb, adapter=_adapter_yielding())
        self.assertEqual(docs, [])
        self.assertEqual(emb.calls, [])

    def test_single_record_single_chunk(self):
        emb = _FakeEmbedder()
        adapt = _adapter_yielding(("PROJ-1", "Short content.", {"summary": "x"}))
        docs = _build_docs({}, "jira", target_tokens=512, embedder=emb, adapter=adapt)
        self.assertEqual(len(docs), 1)
        d = docs[0]
        self.assertEqual(d.source, "jira")
        self.assertEqual(d.source_id, "PROJ-1")
        self.assertEqual(d.chunk_idx, 0)
        self.assertEqual(d.content, "Short content.")
        self.assertEqual(len(d.embedding), 384)
        self.assertEqual(d.metadata, {"summary": "x"})

    def test_record_split_into_multiple_chunks(self):
        """Tiny target_tokens forces multi-chunk splitting; chunk_idx enumerates correctly."""
        emb = _FakeEmbedder()
        long_text = "First sentence here. Second sentence here. Third sentence here."
        adapt = _adapter_yielding(("PROJ-1", long_text, {}))
        # target_tokens=5 → 20 chars/chunk, so each sentence becomes its own chunk.
        docs = _build_docs({}, "jira", target_tokens=5, embedder=emb, adapter=adapt)
        self.assertEqual(len(docs), 3)
        self.assertEqual([d.chunk_idx for d in docs], [0, 1, 2])
        self.assertTrue(all(d.source_id == "PROJ-1" for d in docs))

    def test_record_with_no_chunks_is_skipped(self):
        """Empty content from the adapter must not produce a Document."""
        emb = _FakeEmbedder()
        adapt = _adapter_yielding(
            ("PROJ-1", "", {}),
            ("PROJ-2", "Has content.", {}),
        )
        docs = _build_docs({}, "jira", target_tokens=512, embedder=emb, adapter=adapt)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].source_id, "PROJ-2")

    def test_embedder_called_once_per_source_id(self):
        """Batched embedding: one HTTP round-trip per record, not per chunk."""
        emb = _FakeEmbedder()
        adapt = _adapter_yielding(
            ("PROJ-1", "Sentence one. Sentence two.", {}),
            ("PROJ-2", "Other content.", {}),
        )
        _build_docs({}, "jira", target_tokens=5, embedder=emb, adapter=adapt)
        self.assertEqual(len(emb.calls), 2)

    def test_embeddings_aligned_with_chunks(self):
        emb = _FakeEmbedder()
        adapt = _adapter_yielding(("PROJ-1", "S1. S2. S3.", {}))
        docs = _build_docs({}, "jira", target_tokens=1, embedder=emb, adapter=adapt)
        # FakeEmbedder returns [i]*dim for the i-th text in a single embed() call.
        for i, d in enumerate(docs):
            self.assertEqual(d.embedding[0], float(i))

    def test_connector_name_used_as_source(self):
        emb = _FakeEmbedder()
        adapt = _adapter_yielding(("PR-9", "x", {}))
        docs = _build_docs({}, "bitbucket", target_tokens=512, embedder=emb, adapter=adapt)
        self.assertEqual(docs[0].source, "bitbucket")

    def test_metadata_passes_through_unchanged(self):
        emb = _FakeEmbedder()
        meta = {"status": "Open", "assignee": "Alice", "summary": "X"}
        adapt = _adapter_yielding(("PROJ-1", "x", meta))
        docs = _build_docs({}, "jira", target_tokens=512, embedder=emb, adapter=adapt)
        self.assertIs(docs[0].metadata, meta)


class BuildDocsWithRealAdapterTest(unittest.TestCase):
    """Smoke: pipeline composes with the real jira.adapt over the fixture."""

    def test_fixture_round_trip_through_real_adapter(self):
        import json
        from pathlib import Path
        from services.context_bridge.connectors import jira

        fixture = Path(__file__).parent / "fixtures" / "jira_sample.json"
        payload = json.loads(fixture.read_text())
        emb = _FakeEmbedder()
        docs = _build_docs(payload, "jira", target_tokens=512, embedder=emb, adapter=jira.adapt)
        # 3 issues in the fixture, each short enough for one chunk.
        source_ids = {d.source_id for d in docs}
        self.assertEqual(source_ids, {"PROJ-412", "PROJ-381", "PROJ-419"})
        self.assertTrue(all(d.source == "jira" for d in docs))
        self.assertTrue(all(d.chunk_idx == 0 for d in docs))


if __name__ == "__main__":
    unittest.main()
