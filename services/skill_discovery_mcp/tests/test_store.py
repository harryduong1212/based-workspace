"""Tests for SkillStore — uses a fake qdrant client injected via
`client_factory`. No real Qdrant required; the qdrant-client lib still has
to be importable (it owns the PointStruct/VectorParams shapes)."""
from __future__ import annotations

import unittest

try:
    import qdrant_client  # noqa: F401 — import probe; tests below skip if absent
    _HAS_QDRANT = True
except ImportError:
    _HAS_QDRANT = False

from services.skill_discovery_mcp.indexer import SkillDoc, stable_point_id


def _doc(name: str = "x", category: str = "c") -> SkillDoc:
    return SkillDoc(
        name=name, description="d", category=category, path="p",
        risk="r", source="s", body_excerpt="b",
    )


class _FakeCollections:
    def __init__(self, names: list[str]) -> None:
        self.collections = [type("C", (), {"name": n})() for n in names]


class _FakeQdrant:
    """Minimal stand-in for qdrant_client.QdrantClient. Records every call
    so tests can assert on it."""

    def __init__(self, *, existing: list[str] | None = None) -> None:
        self._existing = list(existing or [])
        self.created: list[tuple[str, int]] = []
        self.upserts: list[dict[str, object]] = []
        self.last_search: dict[str, object] | None = None
        self._search_results: list[object] = []
        self._count = 0

    # qdrant_client API surface we touch
    def get_collections(self) -> _FakeCollections:
        return _FakeCollections(self._existing)

    def create_collection(self, *, collection_name: str, vectors_config) -> None:  # type: ignore[no-untyped-def]
        self._existing.append(collection_name)
        self.created.append((collection_name, int(vectors_config.size)))

    def upsert(self, *, collection_name: str, points, wait: bool = True) -> None:  # type: ignore[no-untyped-def]
        self.upserts.append({"collection": collection_name, "n": len(points), "wait": wait})

    def search(self, *, collection_name: str, query_vector, limit: int):  # type: ignore[no-untyped-def]
        self.last_search = {
            "collection": collection_name,
            "query_vector": list(query_vector),
            "limit": int(limit),
        }
        return list(self._search_results)

    def count(self, *, collection_name: str, exact: bool = True):  # type: ignore[no-untyped-def]
        return type("R", (), {"count": self._count})()

    # test helpers
    def set_search_results(self, hits: list[object]) -> None:
        self._search_results = hits

    def set_count(self, n: int) -> None:
        self._count = n


@unittest.skipUnless(_HAS_QDRANT, "qdrant-client not installed")
class EnsureCollectionTests(unittest.TestCase):
    def test_creates_when_missing(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore  # local — needs qdrant import to succeed

        fake = _FakeQdrant(existing=[])
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        created = store.ensure_collection()
        self.assertTrue(created)
        self.assertEqual(fake.created, [("based_skills", 384)])

    def test_idempotent_when_present(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        fake = _FakeQdrant(existing=["based_skills"])
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        created = store.ensure_collection()
        self.assertFalse(created)
        self.assertEqual(fake.created, [])  # no second create


@unittest.skipUnless(_HAS_QDRANT, "qdrant-client not installed")
class UpsertBatchTests(unittest.TestCase):
    def test_aligns_docs_and_vectors(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        fake = _FakeQdrant(existing=["based_skills"])
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        docs = [_doc("a"), _doc("b")]
        n = store.upsert_batch(docs, [[0.1, 0.2], [0.3, 0.4]])
        self.assertEqual(n, 2)
        self.assertEqual(fake.upserts[-1]["n"], 2)

    def test_empty_input_is_zero_no_call(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        fake = _FakeQdrant(existing=["based_skills"])
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        self.assertEqual(store.upsert_batch([], []), 0)
        self.assertEqual(fake.upserts, [])

    def test_length_mismatch_raises(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        store = SkillStore(client_factory=lambda h, p: _FakeQdrant(existing=["based_skills"]))
        with self.assertRaises(ValueError):
            store.upsert_batch([_doc("a")], [[0.1], [0.2]])


@unittest.skipUnless(_HAS_QDRANT, "qdrant-client not installed")
class SearchTests(unittest.TestCase):
    def test_returns_payload_with_score(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        fake = _FakeQdrant(existing=["based_skills"])
        fake.set_search_results([
            type("H", (), {"payload": {"name": "x", "description": "d"}, "score": 0.92})(),
            type("H", (), {"payload": {"name": "y", "description": "d2"}, "score": 0.51})(),
        ])
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        hits = store.search([0.0] * 384, k=2)
        self.assertEqual(hits[0]["name"], "x")
        self.assertAlmostEqual(hits[0]["score"], 0.92)
        self.assertEqual(fake.last_search["limit"], 2)  # type: ignore[index]

    def test_k_floor_one(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        fake = _FakeQdrant(existing=["based_skills"])
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        store.search([0.0], k=0)
        self.assertEqual(fake.last_search["limit"], 1)  # type: ignore[index]


@unittest.skipUnless(_HAS_QDRANT, "qdrant-client not installed")
class CountTests(unittest.TestCase):
    def test_returns_int(self) -> None:
        from services.skill_discovery_mcp.store import SkillStore

        fake = _FakeQdrant(existing=["based_skills"])
        fake.set_count(42)
        store = SkillStore(collection="based_skills", client_factory=lambda h, p: fake)
        self.assertEqual(store.count(), 42)


class StablePointIdSurfaceTest(unittest.TestCase):
    """Sanity — confirms the indexer-side helper is reachable from store
    callers' import path (catches an accidental reorganization)."""

    def test_imports_from_indexer(self) -> None:
        from services.skill_discovery_mcp.indexer import stable_point_id as fn

        self.assertIs(fn, stable_point_id)


if __name__ == "__main__":
    unittest.main()
