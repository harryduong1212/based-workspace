"""Embedder — Phase F scaffold.

The default model is `bge-small-en-v1.5` via sentence-transformers (local, free).
F.2 will implement embed(); for now this module documents the intended interface.
"""
from __future__ import annotations


class Embedder:
    """Wraps a sentence-transformers model. Single-instance, lazy-loaded."""

    DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
    DIMENSION = 384  # bge-small-en-v1.5 output size

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self._model = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding per input text. Implemented in F.2."""
        raise NotImplementedError("Embedder.embed not yet wired (Phase F.0 scaffold)")
