# Context Bridge

Python service that owns chunking, embedding, and pgvector retrieval. Exposes its corpus to AI tools (Antigravity, Claude Code) via the `postgres-memory` MCP server.

## Status

**Phase F.0 — scaffold only.** Module structure, schema SQL, fixture data, and the CLI surface are committed. Embedding, ingestion, and search are stubbed (raise `NotImplementedError`).

Next phases:
- **F.1** — wire `VectorStore.init_schema()` against local Postgres + pgvector.
- **F.2** — wire `Embedder.embed()`, the chunker, the connector adapters, and `VectorStore.upsert()`.
- **F.3** — wire `VectorStore.search()` and the `cli search` command.
- **F.4** — round-trip smoke test (replace placeholder in `tests/test_smoke.py`).
- **F.5** — expose via `postgres-memory` MCP for AI tool retrieval.

## Stack (locked)

- Postgres 16+ with `pgvector` extension
- Embeddings: `BAAI/bge-small-en-v1.5` via `sentence-transformers` (local, free, 384-dim)
- Chunking: sentence-aware default
- Schema: single `documents` table; `source` column distinguishes connector origin; upsert on `(source, source_id, chunk_idx)`

## Layout

    services/context_bridge/
        cli.py                    # `python -m services.context_bridge.cli ...`
        embedder.py               # `Embedder` (sentence-transformers wrapper)
        store.py                  # `VectorStore` (psycopg + pgvector)
        chunkers/sentence.py      # sentence-aware chunker
        connectors/jira.py        # Jira payload → (source_id, content, metadata)
        connectors/bitbucket.py   # Bitbucket payload → same
        sql/0001_documents.sql    # schema migration
        tests/fixtures/*.json     # development-mode input
        tests/test_smoke.py       # round-trip happy path (Phase F.4)

## Setup (Phase F.1+)

    # Postgres reachable via env vars (already in .env): POSTGRES_USER / PASSWORD / DB / PORT
    pip install -r services/context_bridge/requirements.txt
    python -m services.context_bridge.cli init-schema

## Usage (Phase F.2+)

    # Ingest from a fixture (development mode)
    python -m services.context_bridge.cli ingest --connector jira --fixture services/context_bridge/tests/fixtures/jira_sample.json

    # Semantic search
    python -m services.context_bridge.cli search "rate limiting" -k 5

## Why a separate service?

n8n owns ingest scheduling, retries, and credentials (Jira/Bitbucket nodes). Embedding and pgvector belong in Python — n8n is awkward for vector math. The split: **n8n triggers, Python embeds, MCP retrieves.**
