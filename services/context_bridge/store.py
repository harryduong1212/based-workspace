"""VectorStore — Phase F scaffold.

Wraps a psycopg connection and exposes upsert + search. F.1 wires Postgres;
F.3 wires search.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Document:
    source: str          # e.g. "jira", "bitbucket"
    source_id: str       # ticket key, PR id
    chunk_idx: int
    content: str
    embedding: list[float]
    metadata: dict


class VectorStore:
    """Postgres + pgvector backend."""

    def __init__(self, dsn: str | None = None):
        self.dsn = dsn
        self._conn = None

    def init_schema(self) -> None:
        raise NotImplementedError("VectorStore.init_schema not yet wired (Phase F.1)")

    def upsert(self, docs: list[Document]) -> int:
        raise NotImplementedError("VectorStore.upsert not yet wired (Phase F.2)")

    def search(self, query_embedding: list[float], k: int = 5) -> list[tuple[Document, float]]:
        raise NotImplementedError("VectorStore.search not yet wired (Phase F.3)")
