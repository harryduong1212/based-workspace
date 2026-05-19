"""FastMCP wrapper — the `skill-discovery` MCP server.

One tool:
  - find_skills(query, k=5) — semantic search over indexed SKILL.md files

The Qdrant connection and Embedder are lazy-initialised on first call so
`import` and `--help` stay cheap even when llama-swap / Qdrant aren't
running yet. Tests substitute fakes via the module-level
`set_test_doubles()` helper.
"""
from __future__ import annotations

import json
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from .embedder import Embedder, EmbedderError
from .store import SkillStore

app = FastMCP("skill-discovery")


# Lazy singletons — swapped out in tests via `set_test_doubles`.
_embedder: Embedder | None = None
_store: SkillStore | None = None


def _get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder


def _get_store() -> SkillStore:
    global _store
    if _store is None:
        _store = SkillStore()
    return _store


def set_test_doubles(*, embedder: Embedder | None = None, store: SkillStore | None = None) -> None:
    """Test-only seam. Replaces the lazy singletons before any tool runs.
    Production code never calls this — the server boots clean."""
    global _embedder, _store
    if embedder is not None:
        _embedder = embedder
    if store is not None:
        _store = store


def reset_test_doubles() -> None:
    """Pair with set_test_doubles — restores the lazy-init path."""
    global _embedder, _store
    _embedder = None
    _store = None


@app.tool()
def find_skills(query: str, k: int = 5) -> str:
    """Find the top-k SKILL.md docs most relevant to `query`.

    Returns a JSON-encoded list of `{name, description, category, path, risk,
    source, score}` objects ordered by similarity (best first). `score` is
    cosine similarity in [-1, 1]; higher is better. The caller is expected
    to read the actual SKILL.md from `path` if it wants the full body.

    Returns an empty JSON array `[]` if the collection is empty (no reindex
    has run yet) or if the query has zero matches. Raises on transport
    failure to the embedder or vector store — agents should treat that as
    "skill discovery unavailable, fall back to manual selection."

    Args:
        query: Natural-language description of what the agent is trying to
            do, e.g. "how do I write a FastAPI endpoint with auth".
        k: How many neighbors to return (1–25). Defaults to 5.
    """
    query_clean = (query or "").strip()
    if not query_clean:
        return json.dumps([])
    k_clean = max(1, min(25, int(k)))

    try:
        query_vec = _get_embedder().embed_one(query_clean)
    except EmbedderError as e:
        # Surface to the agent rather than crashing the tool call — the
        # MCP protocol expects a string back, and an empty-results JSON
        # is misleading. Stringified error is the clearest signal.
        raise RuntimeError(f"skill-discovery embedder unavailable: {e}") from e

    hits = _get_store().search(query_vec, k=k_clean)
    return json.dumps(hits, ensure_ascii=False)


@app.tool()
def skill_index_stats() -> str:
    """Diagnostic — returns `{collection, points}` so the caller can verify
    the index has been populated. Useful when an agent gets zero hits and
    can't tell if it's a query problem or a not-yet-indexed problem."""
    store = _get_store()
    payload: dict[str, Any] = {"collection": store.collection}
    try:
        payload["points"] = store.count()
    except Exception as e:  # noqa: BLE001 — diagnostic, swallow into payload
        payload["error"] = f"{type(e).__name__}: {e}"
        payload["points"] = None
    return json.dumps(payload, ensure_ascii=False)


__all__ = ["app", "find_skills", "skill_index_stats", "set_test_doubles", "reset_test_doubles"]
