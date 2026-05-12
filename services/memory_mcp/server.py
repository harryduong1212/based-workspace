"""FastMCP wrapper around mem0 — the `memory` MCP server.

Two tools:
  - search_memory(query, k=5)   — semantic search over stored facts
  - add_memory(content, user_id) — store a new fact/observation

mem0 itself handles chunking, embedding, vector store I/O, and fact
extraction via an LLM. The wrapper just translates between MCP's
function-call shape and mem0's Python API, and isolates lazy init so
import succeeds even when the backend stack (Qdrant + llama-swap) isn't
running yet — useful for `validate.py` and tests.

Environment knobs (all optional; sensible local defaults):
  QDRANT_HOST      default localhost
  QDRANT_PORT      default 6333
  MEMORY_LLM_BASE  default http://localhost:8083/v1  (llama-swap)
  MEMORY_LLM_MODEL default gemma-3-4b
  MEMORY_EMBED_MODEL default bge-small-en-v1.5
  MEMORY_USER_ID   default "default"  — single-user; ignored if caller supplies
"""
from __future__ import annotations

import json
import os
from typing import Any

from mcp.server.fastmcp import FastMCP

app = FastMCP("memory")

# Lazy-init guards: mem0 + qdrant connection happens on first tool call, not
# at import time. Keeps `python -m services.memory_mcp --help`-style probes
# cheap, and lets tests substitute a fake.
_memory: Any = None
_memory_factory: Any = None


def _default_config() -> dict[str, Any]:
    return {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "host": os.environ.get("QDRANT_HOST", "localhost"),
                "port": int(os.environ.get("QDRANT_PORT", "6333")),
                "collection_name": os.environ.get("MEMORY_COLLECTION", "based_memory"),
            },
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": os.environ.get("MEMORY_LLM_MODEL", "gemma-3-4b"),
                "openai_base_url": os.environ.get(
                    "MEMORY_LLM_BASE", "http://localhost:8083/v1"
                ),
                "api_key": os.environ.get("MEMORY_LLM_KEY", "local-no-auth"),
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": os.environ.get("MEMORY_EMBED_MODEL", "bge-small-en-v1.5"),
                "openai_base_url": os.environ.get(
                    "MEMORY_EMBED_BASE", "http://localhost:8083/v1"
                ),
                "api_key": os.environ.get("MEMORY_EMBED_KEY", "local-no-auth"),
            },
        },
    }


def _get_memory() -> Any:
    """Return the singleton Memory instance, initialising lazily."""
    global _memory
    if _memory is not None:
        return _memory
    if _memory_factory is not None:
        _memory = _memory_factory()
        return _memory
    # Real init — only reachable when the backing services are reachable.
    from mem0 import Memory

    _memory = Memory.from_config(_default_config())
    return _memory


def set_memory_factory(factory: Any) -> None:
    """Test seam — substitute a fake Memory factory before any tool runs."""
    global _memory, _memory_factory
    _memory = None
    _memory_factory = factory


def _user() -> str:
    return os.environ.get("MEMORY_USER_ID", "default")


@app.tool()
def search_memory(query: str, k: int = 5) -> str:
    """Search stored memories by semantic similarity. Returns top k results
    as a JSON list of `{id, memory, score}` (mem0 shape varies by version;
    we serialise whatever mem0 returns).
    """
    results = _get_memory().search(query, user_id=_user(), limit=int(k))
    return json.dumps(results, default=str)


@app.tool()
def add_memory(content: str, user_id: str | None = None) -> str:
    """Add a memory. Returns mem0's response (typically `{id, memory, event}`)
    as JSON. `user_id` defaults to MEMORY_USER_ID env or "default".
    """
    uid = user_id or _user()
    result = _get_memory().add(content, user_id=uid)
    return json.dumps(result, default=str)
