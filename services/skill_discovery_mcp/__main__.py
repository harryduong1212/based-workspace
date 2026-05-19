"""Entry point — two modes.

  python -m services.skill_discovery_mcp           # stdio MCP server (for .mcp.json)
  python -m services.skill_discovery_mcp reindex   # rebuild the Qdrant collection
                                                   # from .archived/skills/

The reindex subcommand is deliberately separate from the server (rather than
an MCP tool) because (a) it's a one-shot operation a human runs, (b) it
takes a few seconds and would block an agent if exposed as a tool, and (c)
the CLI surface lets the user run it without launching an MCP client.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .embedder import Embedder
from .indexer import index_skills
from .store import SkillStore

# `server` imports mcp (FastMCP) — keep it out of the module-level import so
# `reindex` works without the mcp lib installed.


def _default_skills_dir() -> Path:
    """Repo-relative default: <repo_root>/.archived/skills/. Repo root is
    derived from this module's location (services/skill_discovery_mcp/) so
    the CLI works regardless of cwd."""
    here = Path(__file__).resolve()
    repo_root = here.parent.parent.parent  # services/skill_discovery_mcp/ → repo root
    env = os.environ.get("SKILLS_DIR")
    return Path(env) if env else repo_root / ".archived" / "skills"


def cmd_reindex(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m services.skill_discovery_mcp reindex",
        description="Walk SKILLS_DIR, embed each SKILL.md, upsert into Qdrant.",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=_default_skills_dir(),
        help="Root directory containing <category>/<skill>/SKILL.md (default: <repo>/.archived/skills/)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="How many skills to embed per HTTP call (default: 32).",
    )
    args = parser.parse_args(argv)

    skills_dir = args.skills_dir.resolve()
    print(f"[reindex] walking {skills_dir}", file=sys.stderr)
    docs = index_skills(skills_dir)
    print(f"[reindex] parsed {len(docs)} SKILL.md files", file=sys.stderr)
    if not docs:
        print("[reindex] nothing to index — exiting", file=sys.stderr)
        return 0

    embedder = Embedder()
    store = SkillStore()

    created = store.ensure_collection()
    print(
        f"[reindex] collection '{store.collection}' {'created' if created else 'exists'}",
        file=sys.stderr,
    )

    total_written = 0
    for i in range(0, len(docs), args.batch_size):
        batch = docs[i : i + args.batch_size]
        vectors = embedder.embed([d.text_for_embedding for d in batch])
        written = store.upsert_batch(batch, vectors)
        total_written += written
        print(
            f"[reindex] batch {i // args.batch_size + 1}: wrote {written} (total {total_written}/{len(docs)})",
            file=sys.stderr,
        )

    print(f"[reindex] done — {total_written} points in '{store.collection}'", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "reindex":
        return cmd_reindex(argv[1:])
    if argv and argv[0] in {"-h", "--help"}:
        print(__doc__.strip(), file=sys.stderr)
        return 0
    # No subcommand → run as MCP stdio server. Import lazily so the
    # `reindex` path doesn't need `mcp` installed.
    from .server import app

    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
