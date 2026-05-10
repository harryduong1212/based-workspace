# Context Bridge

Python service that owns chunking, embedding, and pgvector retrieval. Exposes its corpus to AI tools (Antigravity, Claude Code) via the `context-bridge` MCP server.

## Status

**Phase F — wired.** All phases are implemented:

- **F.1** — `VectorStore.init_schema()` applies `sql/0001_documents.sql` (idempotent).
- **F.2** — `Embedder.embed()` hits an OpenAI-compatible `/v1/embeddings` endpoint (llama-swap / bge-small-en-v1.5). `VectorStore.upsert()` does delete-then-insert per `(source, source_id)` group. Sentence chunker and Jira/Bitbucket connector adapters are real.
- **F.3** — `VectorStore.search()` uses pgvector cosine distance (`<=>`), optional source filter, top-k.
- **F.4** — `test_round_trip.py` ingests the Jira fixture with the real embedder, queries, and asserts semantic ranking. Skips gracefully when infra is down.
- **F.5** — `services/context_bridge_mcp/server.py` exposes a `search_context` tool via FastMCP (stdio transport).

Remaining work:
- **Gmail connector adapter** — only Jira and Bitbucket adapters exist.
- **Live validation** — integration tests skip when containers are stopped. Confirm end-to-end once infra is up.

## Stack (locked)

- Postgres 16+ with `pgvector` extension
- Embeddings: `BAAI/bge-small-en-v1.5` via `sentence-transformers` (local, free, 384-dim)
- Chunking: sentence-aware default
- Schema: single `documents` table; `source` column distinguishes connector origin; upsert on `(source, source_id, chunk_idx)`

## Layout

    services/context_bridge/
        cli.py                    # `python -m services.context_bridge.cli ...`
        embedder.py               # `Embedder` (HTTP client to /v1/embeddings)
        store.py                  # `VectorStore` (psycopg + pgvector)
        chunkers/sentence.py      # sentence-aware chunker
        connectors/jira.py        # Jira payload → (source_id, content, metadata)
        connectors/bitbucket.py   # Bitbucket payload → same
        sql/0001_documents.sql    # schema migration
        tests/fixtures/*.json     # development-mode input
        tests/test_smoke.py       # package import + fixture parse
        tests/test_cli.py         # _build_docs pipeline (mock embedder)
        tests/test_store.py       # VectorStore unit tests (mock psycopg)
        tests/test_store_integration.py  # live Postgres tests (auto-skip)
        tests/test_round_trip.py  # full ingest→search ranking (auto-skip)

    services/context_bridge_mcp/
        server.py                 # MCP server (search_context tool)

## Setup

    # Postgres reachable via env vars (already in .env): POSTGRES_USER / PASSWORD / DB / PORT
    pip install -r services/context_bridge/requirements.txt
    python -m services.context_bridge.cli init-schema

## Usage

    # Ingest from a fixture (development mode)
    python -m services.context_bridge.cli ingest --connector jira --fixture services/context_bridge/tests/fixtures/jira_sample.json

    # Semantic search
    python -m services.context_bridge.cli search "rate limiting" -k 5

## Why a separate service?

n8n owns ingest scheduling, retries, and credentials (Jira/Bitbucket nodes). Embedding and pgvector belong in Python — n8n is awkward for vector math. The split: **n8n triggers, Python embeds, MCP retrieves.**
