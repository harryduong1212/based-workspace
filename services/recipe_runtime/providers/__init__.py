"""Provider registry for the recipe runtime dispatcher.

A provider speaks one model API (OpenAI-compatible, Anthropic Messages, Gemini
native, etc.) and exposes a uniform `dispatch_chat` to the dispatcher. Adding a
new provider = one new module in this package + one line in `_REGISTRY`.

Resolution from a recipe is `provider/model_id` (e.g. `local/gemma-3-4b`,
`anthropic/claude-opus-4-7`, `gemini/gemini-2.0-flash-exp`). A bare model id
with no slash defaults to `local/`.
"""
from __future__ import annotations

from .base import Provider, ProviderUnavailable

from . import anthropic as _anthropic
from . import gemini as _gemini
from . import local as _local


_REGISTRY: dict[str, Provider] = {
    "local": _local.LocalProvider(),
    "gemini": _gemini.GeminiProvider(),
    "anthropic": _anthropic.AnthropicProvider(),
}


def get_provider(name: str) -> Provider:
    try:
        return _REGISTRY[name]
    except KeyError as e:
        known = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise ValueError(f"unknown provider {name!r}; known: {known}") from e


def list_providers() -> list[str]:
    return sorted(_REGISTRY)


def available_providers() -> list[str]:
    return sorted(name for name, p in _REGISTRY.items() if p.available())


def parse_model_ref(ref: str) -> tuple[str, str]:
    """Split `provider/model_id`. Bare model id falls back to provider=local."""
    ref = (ref or "").strip()
    if not ref:
        raise ValueError("empty model reference")
    if "/" in ref:
        provider, _, model = ref.partition("/")
        provider = provider.strip()
        model = model.strip()
        if not provider or not model:
            raise ValueError(f"malformed model reference {ref!r}; expected 'provider/model'")
        return provider, model
    return "local", ref


__all__ = [
    "Provider",
    "ProviderUnavailable",
    "get_provider",
    "list_providers",
    "available_providers",
    "parse_model_ref",
]
