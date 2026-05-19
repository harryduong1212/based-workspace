"""Qdrant collection wrapper for the `based_skills` collection.

The `qdrant-client` library is imported lazily so the package can be imported
(and unit-tested with a fake client) without Qdrant being reachable. Tests
inject `client_factory` to substitute a fake.
"""
from __future__ import annotations

import os
from typing import Any, Callable, Iterable

from .indexer import SkillDoc, stable_point_id


# (host, port) → qdrant_client.QdrantClient-shaped object
ClientFactory = Callable[[str, int], Any]


def _default_client_factory(host: str, port: int) -> Any:
    from qdrant_client import QdrantClient  # local import — optional dep

    return QdrantClient(host=host, port=port)


# bge-small-en-v1.5 is 384-dim. Hard-code: the Embedder owns the model
# choice, but the collection has to be created with the *correct* dim before
# any upsert, and bge-small is the locked default per roadmap D2.
DEFAULT_DIM = 384
DEFAULT_COLLECTION = "based_skills"


class SkillStore:
    """Thin wrapper. Three operations: ensure the collection exists, upsert
    a batch of (id, vector, payload) triples, and query."""

    def __init__(
        self,
        *,
        host: str | None = None,
        port: int | None = None,
        collection: str | None = None,
        dim: int = DEFAULT_DIM,
        client_factory: ClientFactory | None = None,
    ):
        self._host = host or os.environ.get("QDRANT_HOST", "localhost")
        self._port = port if port is not None else int(os.environ.get("QDRANT_PORT", "6333"))
        self._collection = collection or os.environ.get("SKILLS_COLLECTION", DEFAULT_COLLECTION)
        self._dim = dim
        self._factory = client_factory or _default_client_factory
        self._client: Any | None = None  # lazy

    @property
    def collection(self) -> str:
        return self._collection

    def _get_client(self) -> Any:
        if self._client is None:
            self._client = self._factory(self._host, self._port)
        return self._client

    def ensure_collection(self) -> bool:
        """Create the collection with the right vector config if it doesn't
        exist yet. Returns True if we created it, False if it already existed.
        Idempotent — safe to call before every reindex."""
        from qdrant_client.http import models as qmodels  # local import

        client = self._get_client()
        existing = {c.name for c in client.get_collections().collections}
        if self._collection in existing:
            return False
        client.create_collection(
            collection_name=self._collection,
            vectors_config=qmodels.VectorParams(
                size=self._dim, distance=qmodels.Distance.COSINE
            ),
        )
        return True

    def upsert_batch(self, docs: Iterable[SkillDoc], vectors: list[list[float]]) -> int:
        """Replace points for `docs` in-place. Caller passes vectors in the
        same order as docs (the embedder respects insertion order, so this is
        cheap to keep aligned). Returns the number of points written."""
        from qdrant_client.http import models as qmodels  # local import

        doc_list = list(docs)
        if len(doc_list) != len(vectors):
            raise ValueError(
                f"upsert_batch: len(docs)={len(doc_list)} != len(vectors)={len(vectors)}"
            )
        if not doc_list:
            return 0

        client = self._get_client()
        points = [
            qmodels.PointStruct(
                id=stable_point_id(doc),
                vector=vec,
                payload=doc.payload(),
            )
            for doc, vec in zip(doc_list, vectors)
        ]
        client.upsert(collection_name=self._collection, points=points, wait=True)
        return len(points)

    def search(self, query_vector: list[float], k: int = 5) -> list[dict[str, Any]]:
        """Top-k semantic neighbors. Returns a list of `{score, ...payload}`
        dicts ordered by similarity (best first). Empty if the collection is
        empty or the query is too far from everything indexed."""
        client = self._get_client()
        # qdrant-client 1.10+ uses `query_points` (returns `.points`); older
        # versions exposed `.search` (returned hits directly). Support both
        # so the fake test client (which exposes `search`) keeps working.
        if hasattr(client, "query_points"):
            results = client.query_points(
                collection_name=self._collection,
                query=query_vector,
                limit=max(1, k),
            )
            hits = list(getattr(results, "points", None) or [])
        else:
            hits = client.search(
                collection_name=self._collection,
                query_vector=query_vector,
                limit=max(1, k),
            )
        out: list[dict[str, Any]] = []
        for hit in hits:
            payload = dict(getattr(hit, "payload", None) or {})
            payload["score"] = float(getattr(hit, "score", 0.0))
            out.append(payload)
        return out

    def count(self) -> int:
        """Diagnostic: how many points live in the collection right now."""
        client = self._get_client()
        result = client.count(collection_name=self._collection, exact=True)
        return int(getattr(result, "count", 0))
