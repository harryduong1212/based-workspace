"""Anthropic (Claude) provider via the Messages API.

Anthropic does not publish an OpenAI-compatible endpoint, so this provider
talks the native Messages API directly. We use stdlib HTTP rather than the
official SDK to keep the runtime import-light — the SDK adds 30+ transitive
dependencies for what amounts to one POST + SSE parser.

Translation from OpenAI-shape messages:
  - The OpenAI `system` role becomes the top-level `system` field.
  - All other messages go into `messages` with role + content unchanged.
  - Streaming uses Anthropic's `content_block_delta` SSE events.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import TextIO

from .base import Provider


ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"

DEFAULT_MODELS = [
    "claude-opus-4-7",
    "claude-sonnet-4-6",
    "claude-haiku-4-5-20251001",
]


class AnthropicProvider(Provider):
    name = "anthropic"

    def available(self) -> bool:
        return bool(os.environ.get("ANTHROPIC_API_KEY"))

    def list_models(self) -> list[str]:
        return list(DEFAULT_MODELS)

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
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set in environment")

        system_parts: list[str] = []
        chat_messages: list[dict] = []
        for m in messages:
            if m.get("role") == "system":
                content = (m.get("content") or "").strip()
                if content:
                    system_parts.append(content)
            else:
                chat_messages.append({"role": m["role"], "content": m["content"]})

        payload: dict = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": chat_messages,
            "stream": bool(stream),
        }
        if system_parts:
            payload["system"] = "\n\n".join(system_parts)

        url = ANTHROPIC_BASE_URL + "/messages"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": ANTHROPIC_VERSION,
                "Accept": "text/event-stream" if stream else "application/json",
            },
        )

        try:
            resp = urllib.request.urlopen(req, timeout=600)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(f"Anthropic API returned {e.code}: {detail}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"Anthropic API unreachable at {url}: {e.reason}") from e

        if not stream:
            data = json.loads(resp.read().decode("utf-8"))
            text = "".join(
                block.get("text", "")
                for block in data.get("content", [])
                if block.get("type") == "text"
            )
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
                if not data_str:
                    continue
                try:
                    event = json.loads(data_str)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "content_block_delta":
                    delta = event.get("delta") or {}
                    if delta.get("type") == "text_delta":
                        piece = delta.get("text", "")
                        if piece:
                            chunks.append(piece)
                            out.write(piece)
                            out.flush()
        out.write("\n")
        out.flush()
        return "".join(chunks)
