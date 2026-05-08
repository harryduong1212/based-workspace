"""Local OpenAI-compatible provider (llama-swap, Ollama, vLLM, LM Studio, ...).

Wire-shape: POST /v1/chat/completions, SSE streaming on `stream=True`. This is
the same code path the runtime used before the multi-provider refactor; it
remains the always-on default for `model: bare-name` recipes.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import TextIO

from .base import Provider


DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_API_KEY = "local-no-auth"


def _resolve_base_url() -> str:
    return (
        os.environ.get("LLAMA_SWAP_URL")
        or os.environ.get("OPENAI_API_BASE")
        or DEFAULT_BASE_URL
    ).rstrip("/")


def _resolve_api_key() -> str:
    return os.environ.get("OPENAI_API_KEY") or DEFAULT_API_KEY


class LocalProvider(Provider):
    name = "local"

    def available(self) -> bool:
        # Local is always "available" — even if the daemon is down, we want the
        # UI to surface it as the default and let dispatch fail with a clear
        # error rather than silently hiding the option.
        return True

    def list_models(self) -> list[str]:
        try:
            req = urllib.request.Request(
                _resolve_base_url() + "/models",
                headers={"Authorization": f"Bearer {_resolve_api_key()}"},
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return sorted(m["id"] for m in data.get("data", []) if "id" in m)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError, KeyError):
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
        return _post_openai_chat(
            base_url=_resolve_base_url(),
            api_key=_resolve_api_key(),
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
            out=out,
        )


def _post_openai_chat(
    *,
    base_url: str,
    api_key: str,
    messages: list[dict],
    model: str,
    max_tokens: int,
    temperature: float,
    stream: bool,
    out: TextIO,
) -> str:
    """Shared OpenAI-compatible chat-completions POST. Used by local + gemini."""
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": bool(stream),
    }
    url = base_url + "/chat/completions"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Accept": "text/event-stream" if stream else "application/json",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=600)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"LLM endpoint returned {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"LLM endpoint unreachable at {url}: {e.reason}") from e

    if not stream:
        data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        out.write(text)
        if not text.endswith("\n"):
            out.write("\n")
        out.flush()
        return text

    chunks: list[str] = []
    with resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").rstrip("\n").rstrip("\r")
            if not line.startswith("data:"):
                continue
            data_str = line[len("data:"):].strip()
            if not data_str or data_str == "[DONE]":
                continue
            try:
                event = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            for choice in event.get("choices", []):
                piece = (choice.get("delta") or {}).get("content")
                if piece:
                    chunks.append(piece)
                    out.write(piece)
                    out.flush()
    out.write("\n")
    out.flush()
    return "".join(chunks)
