"""Jira connector adapter — Phase F scaffold.

Reads a Jira issue payload (from the live API or a JSON fixture) and yields
(source_id, content, metadata) tuples ready for chunking + embedding.
F.2 wires this up.
"""
from __future__ import annotations
from typing import Iterator


def adapt(payload: dict) -> Iterator[tuple[str, str, dict]]:
    """Yield (source_id, content, metadata) per issue. Implemented in F.2."""
    raise NotImplementedError("connectors.jira.adapt not yet wired (Phase F.2)")
