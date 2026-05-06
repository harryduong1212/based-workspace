"""VectorStore — Postgres + pgvector backend for the Context Bridge.

Phase F.1 wires `init_schema`. F.2 wires `upsert`, F.3 wires `search`.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import psycopg


SCHEMA_FILE = Path(__file__).parent / "sql" / "0001_documents.sql"


@dataclass
class Document:
    source: str
    source_id: str
    chunk_idx: int
    content: str
    embedding: list[float]
    metadata: dict


def _build_dsn_from_env() -> str:
    """Construct a libpq URI from POSTGRES_* env vars (matching .env)."""
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "")
    db = os.environ.get("POSTGRES_DB", "postgres")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


class VectorStore:
    """Postgres + pgvector backend.

    Lazy connection: opens on first use, kept until close(). Use as a
    context manager when you want guaranteed cleanup.
    """

    def __init__(self, dsn: str | None = None):
        self._dsn = dsn
        self._conn: psycopg.Connection | None = None

    @property
    def dsn(self) -> str:
        return self._dsn or _build_dsn_from_env()

    def connect(self) -> psycopg.Connection:
        if self._conn is None or self._conn.closed:
            self._conn = psycopg.connect(self.dsn)
        return self._conn

    def close(self) -> None:
        if self._conn is not None and not self._conn.closed:
            self._conn.close()
        self._conn = None

    def __enter__(self) -> "VectorStore":
        self.connect()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def init_schema(self) -> None:
        """Apply sql/0001_documents.sql. Idempotent (uses IF NOT EXISTS)."""
        sql = SCHEMA_FILE.read_text(encoding="utf-8")
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    def upsert(self, docs: list[Document]) -> int:
        raise NotImplementedError("VectorStore.upsert not yet wired (Phase F.2)")

    def search(self, query_embedding: list[float], k: int = 5) -> list[tuple[Document, float]]:
        raise NotImplementedError("VectorStore.search not yet wired (Phase F.3)")
