"""Google Gemini provider via the OpenAI-compatible shim.

Gemini exposes an OpenAI-compatible chat-completions endpoint at
`https://generativelanguage.googleapis.com/v1beta/openai/`, so we route through
the same POST helper the local provider uses. Auth is `GEMINI_API_KEY` carried
as a Bearer token.
"""
from __future__ import annotations

import os
from typing import TextIO

from .base import Provider
from .local import _post_openai_chat


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"

# Curated default list. The free-text model field in the UI lets the user pick
# anything else Google publishes — this is just the dropdown's seed.
DEFAULT_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]


class GeminiProvider(Provider):
    name = "gemini"

    def available(self) -> bool:
        return bool(os.environ.get("GEMINI_API_KEY"))

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
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment")
        return _post_openai_chat(
            base_url=GEMINI_BASE_URL,
            api_key=api_key,
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
            out=out,
        )
