"""Context Bridge CLI.

Subcommands:
    init-schema    Create the documents table and pgvector extension.
    ingest         Ingest a fixture or live connector source.
    search         Semantic search over ingested content.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from services.context_bridge.chunkers.sentence import chunk
from services.context_bridge.connectors import bitbucket, jira
from services.context_bridge.embedder import Embedder
from services.context_bridge.store import Document, VectorStore


_ADAPTERS = {
    "jira": jira.adapt,
    "bitbucket": bitbucket.adapt,
}


def cmd_init_schema(args):
    try:
        with VectorStore() as vs:
            vs.init_schema()
    except Exception as e:
        print(f"init-schema FAILED: {e}")
        sys.exit(1)
    print("init-schema OK — pgvector extension + documents table + indexes ready.")


def _build_docs(
    payload: dict,
    connector: str,
    *,
    target_tokens: int,
    embedder: Embedder,
    adapter=None,
) -> list[Document]:
    """Pure pipeline: payload → list[Document]. No IO, no DB.

    Calls the embedder once per source_id with all chunks for that record,
    so each issue/PR is one round-trip rather than one round-trip per chunk.
    """
    adapt_fn = adapter if adapter is not None else _ADAPTERS[connector]
    docs: list[Document] = []
    for source_id, content, metadata in adapt_fn(payload):
        chunks = chunk(content, target_tokens=target_tokens)
        if not chunks:
            continue
        embeddings = embedder.embed(chunks)
        for idx, (text, vec) in enumerate(zip(chunks, embeddings)):
            docs.append(
                Document(
                    source=connector,
                    source_id=source_id,
                    chunk_idx=idx,
                    content=text,
                    embedding=vec,
                    metadata=metadata,
                )
            )
    return docs


def cmd_ingest(args):
    if not args.fixture:
        print("ingest currently requires --fixture (live connector mode is not yet wired).")
        sys.exit(2)
    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"ingest FAILED: fixture not found: {fixture_path}")
        sys.exit(1)

    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    embedder = Embedder()
    try:
        docs = _build_docs(
            payload,
            args.connector,
            target_tokens=args.target_tokens,
            embedder=embedder,
        )
    except NotImplementedError as e:
        print(f"ingest FAILED: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"ingest FAILED: {e}")
        sys.exit(1)

    if not docs:
        print("ingest OK — 0 chunks (no content in payload).")
        return

    distinct_ids = len({(d.source, d.source_id) for d in docs})
    try:
        with VectorStore() as vs:
            n = vs.upsert(docs)
    except Exception as e:
        print(f"ingest FAILED at upsert: {e}")
        sys.exit(1)
    print(f"ingest OK — {n} chunks across {distinct_ids} source_ids written.")


def cmd_search(args):
    embedder = Embedder()
    try:
        [query_embedding] = embedder.embed([args.query])
    except Exception as e:
        print(f"search FAILED at embedder: {e}")
        sys.exit(1)

    try:
        with VectorStore() as vs:
            results = vs.search(query_embedding, k=args.k, source=args.source)
    except Exception as e:
        print(f"search FAILED at store: {e}")
        sys.exit(1)

    if not results:
        print(f"search: no matches for {args.query!r}.")
        return

    print(f"search: {args.query!r} (k={args.k}{', source=' + args.source if args.source else ''})\n")
    for i, (doc, distance) in enumerate(results, start=1):
        meta = doc.metadata or {}
        summary = meta.get("summary") or meta.get("title") or ""
        preview = doc.content.replace("\n", " ").strip()
        if len(preview) > 140:
            preview = preview[:140] + "..."
        head = f"  {i}. [{doc.source}/{doc.source_id} #{doc.chunk_idx}]  ({distance:.4f})"
        if summary:
            head += f"  {summary}"
        print(head)
        if preview:
            print(f"       {preview}")


def main():
    p = argparse.ArgumentParser(prog="context-bridge", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init-schema", help="Create documents table and pgvector extension")
    p_init.set_defaults(func=cmd_init_schema)

    p_ing = sub.add_parser("ingest", help="Ingest a connector source")
    p_ing.add_argument("--connector", required=True, choices=["jira", "bitbucket"])
    p_ing.add_argument("--fixture", help="Path to a JSON fixture (development mode)")
    p_ing.add_argument(
        "--target-tokens",
        type=int,
        default=512,
        help="Target chunk size in tokens (default 512).",
    )
    p_ing.set_defaults(func=cmd_ingest)

    p_sea = sub.add_parser("search", help="Semantic search over ingested content")
    p_sea.add_argument("query")
    p_sea.add_argument("-k", type=int, default=5)
    p_sea.add_argument(
        "--source",
        choices=["jira", "bitbucket"],
        default=None,
        help="Restrict results to one connector (default: all).",
    )
    p_sea.set_defaults(func=cmd_search)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
