#!/usr/bin/env python3
"""Live smoke test for the Context Bridge MCP server.

Spawns `python -m services.context_bridge_mcp` as a stdio subprocess,
runs the MCP handshake (initialize → tools/list → tools/call), and
asserts `search_context` is registered and returns a well-formed
result against ingested test data. Skips with exit code 0 if Postgres
or llama-swap is unreachable so this can sit in validate.py without
blocking dev iteration when infra is down.

Used by validate.py.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from services.context_bridge.cli import _build_docs
from services.context_bridge.connectors import jira
from services.context_bridge.embedder import Embedder
from services.context_bridge.store import VectorStore, _build_dsn_from_env

FIXTURE = ROOT / "services" / "context_bridge" / "tests" / "fixtures" / "jira_sample.json"
SOURCE_IDS = ("PROJ-412", "PROJ-381", "PROJ-419")


def _postgres_reachable() -> bool:
    try:
        with psycopg.connect(_build_dsn_from_env(), connect_timeout=2) as c:
            with c.cursor() as cur:
                cur.execute("SELECT 1")
        return True
    except Exception:
        return False


def _llama_swap_reachable() -> bool:
    try:
        with urllib.request.urlopen(Embedder().base_url + "/models", timeout=2):
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return False


def _seed():
    vs = VectorStore()
    vs.init_schema()
    with vs.connect().cursor() as cur:
        cur.execute(
            "DELETE FROM documents WHERE source = 'jira' AND source_id = ANY(%s)",
            (list(SOURCE_IDS),),
        )
    vs.connect().commit()
    payload = json.loads(FIXTURE.read_text())
    docs = _build_docs(payload, "jira", target_tokens=512, embedder=Embedder(), adapter=jira.adapt)
    vs.upsert(docs)
    vs.close()


def _wipe():
    vs = VectorStore()
    with vs.connect().cursor() as cur:
        cur.execute(
            "DELETE FROM documents WHERE source = 'jira' AND source_id = ANY(%s)",
            (list(SOURCE_IDS),),
        )
    vs.connect().commit()
    vs.close()


async def _run_mcp_smoke() -> list[str]:
    """Drive the MCP server via the stdio client and return failure messages."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    failures: list[str] = []
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "services.context_bridge_mcp"],
        cwd=str(ROOT),
        env=os.environ.copy(),
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            if "search_context" not in tool_names:
                failures.append(f"search_context not registered (got {tool_names})")
                return failures

            result = await session.call_tool(
                "search_context",
                {"query": "audit log compliance session tokens", "k": 3, "source": "jira"},
            )
            if result.isError:
                failures.append(f"tool call returned isError: {result.content}")
                return failures

            # FastMCP populates structuredContent with the typed return value
            # under the "result" key. Each item is also serialized as its own
            # TextContent block in result.content for clients that don't read
            # structured content.
            structured = getattr(result, "structuredContent", None) or {}
            payload = structured.get("result")
            if not isinstance(payload, list) or not payload:
                failures.append(f"expected non-empty list in structuredContent['result'], got {payload!r}")
                return failures
            top = payload[0]
            for key in ("source", "source_id", "chunk_idx", "content", "summary", "distance"):
                if key not in top:
                    failures.append(f"top result missing key {key!r}: {top}")
            if top.get("source_id") != "PROJ-419":
                failures.append(
                    f"expected PROJ-419 to rank first for audit-log query, got {top.get('source_id')}"
                )

    return failures


def main():
    if not (_postgres_reachable() and _llama_swap_reachable()):
        print("SKIP — Postgres or llama-swap unreachable; MCP smoke not exercised.")
        return

    _seed()
    try:
        failures = asyncio.run(_run_mcp_smoke())
    finally:
        _wipe()

    if failures:
        print("FAIL — Context Bridge MCP smoke")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("OK — Context Bridge MCP server registers search_context and returns ranked results.")


if __name__ == "__main__":
    main()
