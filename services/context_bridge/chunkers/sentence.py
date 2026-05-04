"""Sentence-aware chunker — Phase F scaffold.

Splits text into ~target-token chunks at sentence boundaries. F.2 wires the real
implementation (likely using nltk or a regex-based sentence splitter).
"""
from __future__ import annotations


def chunk(text: str, target_tokens: int = 512) -> list[str]:
    """Split text into chunks of ~target_tokens. Implemented in F.2."""
    raise NotImplementedError("chunkers.sentence.chunk not yet wired (Phase F.2)")
