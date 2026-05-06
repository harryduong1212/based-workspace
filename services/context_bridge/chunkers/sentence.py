"""Sentence-aware chunker — packs sentences greedily up to ~target_tokens.

Token counting uses a 4-chars-per-token heuristic (English-biased but cheap;
no tokenizer dependency). Empty / whitespace-only input yields []. Single
short input yields one chunk. Sentence boundaries: period / question mark /
exclamation point followed by whitespace.
"""
from __future__ import annotations

import re

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def chunk(text: str, target_tokens: int = 512) -> list[str]:
    """Split text into chunks of ~target_tokens, breaking on sentence boundaries."""
    if not text or not text.strip():
        return []
    target_chars = max(target_tokens, 1) * 4
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text.strip()) if s.strip()]
    if not sentences:
        return []

    chunks: list[str] = []
    cur = ""
    for s in sentences:
        if not cur:
            cur = s
        elif len(cur) + 1 + len(s) <= target_chars:
            cur = cur + " " + s
        else:
            chunks.append(cur)
            cur = s
    if cur:
        chunks.append(cur)
    return chunks
