"""Embedder — thin HTTP client to an OpenAI-compatible /v1/embeddings endpoint.

Backed by llama.cpp/llama-swap (containerized), serving the
`bge-small-en-v1.5` GGUF in --embeddings mode. Single-instance, stateless,
no local model weights — same transport contract as the chat dispatcher.
"""
from __future__ import annotations

import json
import os
import urllib.request
import urllib.error


DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_API_KEY = "local-no-auth"


class Embedder:
    DEFAULT_MODEL = "bge-small-en-v1.5"
    DIMENSION = 384

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        http_post=None,
    ):
        self.model_name = model_name
        self._base_url = base_url
        self._api_key = api_key
        self._http_post = http_post

    @property
    def base_url(self) -> str:
        return (self._base_url or os.environ.get("OPENAI_API_BASE") or DEFAULT_BASE_URL).rstrip("/")

    @property
    def api_key(self) -> str:
        return self._api_key or os.environ.get("OPENAI_API_KEY") or DEFAULT_API_KEY

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding per input text. Empty input → empty output."""
        if not texts:
            return []
        if self._http_post is not None:
            return self._http_post(self.base_url, self.api_key, self.model_name, texts)
        return _http_post_default(self.base_url, self.api_key, self.model_name, texts)


def _http_post_default(base_url: str, api_key: str, model: str, texts: list[str]) -> list[list[float]]:
    url = base_url + "/embeddings"
    payload = json.dumps({"model": model, "input": texts}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=300)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Embedder endpoint returned {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Embedder endpoint unreachable at {url}: {e.reason}") from e
    data = json.loads(resp.read().decode("utf-8"))
    return [item["embedding"] for item in data["data"]]
