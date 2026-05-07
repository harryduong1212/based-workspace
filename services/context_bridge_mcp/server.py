"""MCP server exposing the Context Bridge as a `search_context` tool.

Wraps `services.context_bridge.store.VectorStore.search` and the embedder
behind a single MCP tool. The tool is small on purpose — it returns
ranked chunks with their metadata; agents decide what to do with them.

Run as `python -m services.context_bridge_mcp` (stdio transport, the
MCP default). Register from a client by adding to `.mcp.json`:

    {
      "mcpServers": {
        "context-bridge": {
          "command": "python3",
          "args": ["-m", "services.context_bridge_mcp"],
          "cwd": "/abs/path/to/based-workspace"
        }
      }
    }

The server reads Postgres creds from `POSTGRES_*` env vars (same as
the CLI) and the embedder endpoint from `OPENAI_API_BASE` /
`OPENAI_API_KEY`.
"""
from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from services.context_bridge.embedder import Embedder
from services.context_bridge.store import VectorStore


app = FastMCP("context-bridge")


def _search_context_impl(
    query: str,
    k: int = 5,
    source: str | None = None,
    *,
    embedder: Embedder | None = None,
    vector_store: VectorStore | None = None,
) -> list[dict[str, Any]]:
    """Embed the query and return top-k ranked chunks.

    Pure function (modulo IO): the `embedder` and `vector_store` are
    injectable so tests don't need llama-swap or Postgres.
    """
    query = (query or "").strip()
    if not query:
        return []
    if k <= 0:
        return []

    emb = embedder if embedder is not None else Embedder()
    [vec] = emb.embed([query])

    if vector_store is not None:
        results = vector_store.search(vec, k=k, source=source)
    else:
        with VectorStore() as vs:
            results = vs.search(vec, k=k, source=source)

    return [_format_result(doc, distance) for doc, distance in results]


def _format_result(doc, distance: float) -> dict[str, Any]:
    meta = doc.metadata or {}
    return {
        "source": doc.source,
        "source_id": doc.source_id,
        "chunk_idx": doc.chunk_idx,
        "content": doc.content,
        "summary": meta.get("summary") or meta.get("title"),
        "distance": float(distance),
        "metadata": meta,
    }


@app.tool()
def search_context(
    query: str,
    k: int = 5,
    source: str | None = None,
) -> list[dict[str, Any]]:
    """Semantic search over ingested Jira issues and Bitbucket PRs.

    Use this when the user's question would benefit from prior ticket or
    PR context that they've already documented — e.g. "What did we
    decide about X?", "Was there a postmortem for Y?", "Find PRs that
    touched the auth layer." Returns ranked chunks ordered by ascending
    cosine distance (smaller = more similar; range 0–2).

    Args:
        query: Natural-language question or keyword phrase.
        k: Number of results to return (default 5).
        source: Restrict to one connector. Either "jira", "bitbucket",
            or omit for all sources.

    Returns:
        List of result dicts with keys: source, source_id, chunk_idx,
        content, summary, distance, metadata.
    """
    return _search_context_impl(query, k=k, source=source)


def run() -> None:
    """Entry point — runs the MCP server over stdio (the MCP default)."""
    app.run()


if __name__ == "__main__":
    run()
