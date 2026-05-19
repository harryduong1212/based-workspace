"""Embedder — POSTs to llama-swap's OpenAI-compatible `/embeddings` endpoint.

Kept deliberately dependency-free (stdlib `urllib`) so the package imports
cleanly when the optional `openai` library isn't installed. The wire shape
matches OpenAI exactly: `{"model": ..., "input": <str | list[str]>}` →
`{"data": [{"embedding": [...float], "index": int}, ...]}`.

Tests inject an `http_post` callable to avoid any real network IO.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Callable, Iterable


# (url, body_bytes, headers, timeout_s) → response_bytes
HttpPost = Callable[[str, bytes, dict[str, str], float], bytes]


def _default_http_post(url: str, body: bytes, headers: dict[str, str], timeout_s: float) -> bytes:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310 — internal
        return resp.read()


class EmbedderError(RuntimeError):
    """Wraps any failure to fetch embeddings — keeps the CLI/MCP layer from
    needing to know about urllib/HTTPError specifics."""


class Embedder:
    """One Embedder = one (base_url, model) target. Reused across many calls;
    no internal state beyond config. 384-dim for bge-small-en-v1.5."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout_s: float = 30.0,
        http_post: HttpPost | None = None,
    ):
        self._base_url = (
            base_url or os.environ.get("SKILLS_LLM_BASE", "http://localhost:11434/v1")
        ).rstrip("/")
        self._model = model or os.environ.get("SKILLS_EMBED_MODEL", "bge-small-en-v1.5")
        self._api_key = api_key or os.environ.get("SKILLS_LLM_KEY", "local-no-auth")
        self._timeout_s = timeout_s
        self._http_post = http_post or _default_http_post

    @property
    def model(self) -> str:
        return self._model

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        """Embed a batch of strings → list of vectors (same order as input).
        Raises `EmbedderError` on any non-2xx, malformed response, or transport
        failure. Empty input returns an empty list without making a request."""
        items = list(texts)
        if not items:
            return []
        url = f"{self._base_url}/embeddings"
        payload = json.dumps({"model": self._model, "input": items}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        try:
            raw = self._http_post(url, payload, headers, self._timeout_s)
        except urllib.error.HTTPError as e:
            raise EmbedderError(f"embeddings HTTP {e.code} from {url}: {e.read()[:300]!r}") from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise EmbedderError(f"embeddings transport error to {url}: {e}") from e
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError as e:
            raise EmbedderError(f"embeddings response was not JSON: {raw[:300]!r}") from e
        data = doc.get("data") if isinstance(doc, dict) else None
        if not isinstance(data, list) or len(data) != len(items):
            raise EmbedderError(
                f"embeddings response missing/short `data`: got {len(data) if isinstance(data, list) else 'n/a'}, "
                f"expected {len(items)}"
            )
        out: list[list[float]] = []
        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                raise EmbedderError(f"embeddings data[{i}] not an object: {entry!r}")
            vec = entry.get("embedding")
            if not isinstance(vec, list) or not all(isinstance(x, (int, float)) for x in vec):
                raise EmbedderError(f"embeddings data[{i}].embedding not a list[float]")
            out.append([float(x) for x in vec])
        return out

    def embed_one(self, text: str) -> list[float]:
        """Convenience: embed a single string. Equivalent to `embed([text])[0]`
        but raises a clearer error if the response shape was wrong."""
        result = self.embed([text])
        if not result:
            raise EmbedderError("embed_one: empty result for non-empty input")
        return result[0]
