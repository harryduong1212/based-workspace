"""Abstract provider interface.

Each subclass wraps one model API. Concrete implementations are stdlib-only
where possible (urllib for HTTP) so the runtime stays import-light; SDK-only
providers (Anthropic) raise ProviderUnavailable when the SDK isn't installed,
and `available()` returns False so the UI can hide them.
"""
from __future__ import annotations

from typing import Iterable, TextIO


class ProviderUnavailable(RuntimeError):
    """Raised when a provider can't be used (missing key, missing SDK, etc.)."""


class Provider:
    """One model-API backend.

    Subclasses must implement:
      - name: short id used in `provider/model` refs (e.g. "local", "gemini")
      - dispatch_chat: send messages, return the assistant's full text
      - available: True iff the provider can be invoked right now (env vars
        present, SDK importable, etc.)

    Optional:
      - list_models: best-effort enumeration of model ids the UI can offer.
        Return [] if unknown — the UI falls back to a free-text field.
    """

    name: str = ""

    def available(self) -> bool:
        raise NotImplementedError

    def list_models(self) -> list[str]:
        return []

    def dispatch_chat(
        self,
        messages: list[dict],
        model: str,
        *,
        max_tokens: int,
        temperature: float,
        stream: bool,
        out: TextIO,
    ) -> str:
        raise NotImplementedError


def stream_chunks_to_out(chunks: Iterable[str], out: TextIO) -> str:
    """Helper used by streaming providers: write each chunk and accumulate."""
    pieces: list[str] = []
    for piece in chunks:
        if not piece:
            continue
        pieces.append(piece)
        out.write(piece)
        out.flush()
    out.write("\n")
    out.flush()
    return "".join(pieces)
