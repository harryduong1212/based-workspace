"""Context Bridge CLI — Phase F scaffold.

Subcommands:
    init-schema    Create the documents table and pgvector extension.
    ingest         Ingest a fixture or live connector source.
    search         Semantic search over ingested content.

Status: SCAFFOLD. Subcommand bodies are not yet wired to real Postgres or
the embedder. They print intended action and exit with code 2 (NotImplementedError-equivalent)
so callers see a clear "not yet implemented" signal rather than silent success.
"""
import argparse
import sys


def cmd_init_schema(args):
    print("[F.0 SCAFFOLD] init-schema would:")
    print("  1. Connect to Postgres via env (POSTGRES_USER/PASSWORD/DB/PORT)")
    print("  2. CREATE EXTENSION IF NOT EXISTS vector")
    print(f"  3. Apply schema from services/context_bridge/sql/0001_documents.sql")
    print("Run F.1 to wire this up.")
    sys.exit(2)


def cmd_ingest(args):
    print(f"[F.0 SCAFFOLD] ingest would:")
    print(f"  source:  {args.connector}")
    print(f"  fixture: {args.fixture}")
    print(f"  1. Load fixture JSON")
    print(f"  2. Pass each record through the connector adapter")
    print(f"  3. Chunk content (sentence-aware default)")
    print(f"  4. Embed via sentence-transformers (bge-small-en-v1.5)")
    print(f"  5. Upsert into documents on (source, source_id, chunk_idx)")
    print("Run F.2 to wire this up.")
    sys.exit(2)


def cmd_search(args):
    print(f"[F.0 SCAFFOLD] search would:")
    print(f"  query: {args.query!r}")
    print(f"  k:     {args.k}")
    print(f"  1. Embed the query")
    print(f"  2. SELECT ... ORDER BY embedding <-> $1 LIMIT $k")
    print(f"  3. Print ranked results")
    print("Run F.3 to wire this up.")
    sys.exit(2)


def main():
    p = argparse.ArgumentParser(prog="context-bridge", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init-schema", help="Create documents table and pgvector extension")
    p_init.set_defaults(func=cmd_init_schema)

    p_ing = sub.add_parser("ingest", help="Ingest a connector source")
    p_ing.add_argument("--connector", required=True, choices=["jira", "bitbucket"])
    p_ing.add_argument("--fixture", help="Path to a JSON fixture (development mode)")
    p_ing.set_defaults(func=cmd_ingest)

    p_sea = sub.add_parser("search", help="Semantic search over ingested content")
    p_sea.add_argument("query")
    p_sea.add_argument("-k", type=int, default=5)
    p_sea.set_defaults(func=cmd_search)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
