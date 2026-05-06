"""Recipe runtime dispatcher.

Three execution.types map to three dispatch functions:

    prompt    → dispatch_prompt    (Phase E1 — wired, OpenAI-compatible HTTP)
    workflow  → dispatch_workflow  (Phase E2 / Phase H; n8n)
    agent     → dispatch_agent     (Phase E3)

dispatch_prompt is provider-agnostic at the wire level: it speaks the OpenAI
chat-completions REST shape, which llama-swap, llama.cpp, Ollama, vLLM,
LM Studio, and many cloud gateways all expose. Anthropic / Gemini get added
later as alternative HTTP transports.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error


DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_API_KEY = "local-no-auth"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.2


def dispatch_prompt(
    envelope: dict,
    *,
    skill_bodies: list[str] | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
    default_model: str | None = None,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    stream: bool = True,
    out=None,
    http_post=None,
) -> str:
    """Send the assembled envelope to an OpenAI-compatible /chat/completions endpoint.

    Resolution precedence:
      model    : envelope["model"]  > default_model  > $RECIPE_DEFAULT_MODEL
      base_url : arg                > $OPENAI_API_BASE > DEFAULT_BASE_URL
      api_key  : arg                > $OPENAI_API_KEY  > DEFAULT_API_KEY

    Returns the assistant's full text response. Streams to `out` (default
    sys.stdout) when `stream=True`.

    `http_post` is an injection seam for tests: a callable
    (base_url, api_key, payload, *, out, stream) -> str.
    """
    base_url = (base_url or os.environ.get("OPENAI_API_BASE") or DEFAULT_BASE_URL).rstrip("/")
    api_key = api_key or os.environ.get("OPENAI_API_KEY") or DEFAULT_API_KEY
    model = (
        envelope.get("model")
        or default_model
        or os.environ.get("RECIPE_DEFAULT_MODEL")
    )
    if not model:
        raise ValueError(
            "no model resolvable: set execution.model in the recipe, "
            "pass default_model, or set RECIPE_DEFAULT_MODEL in the environment"
        )

    out = sys.stdout if out is None else out

    system_parts: list[str] = []
    for sb in skill_bodies or []:
        sb = (sb or "").strip()
        if sb:
            system_parts.append(sb)
    prelude = (envelope.get("recipe_prelude") or "").strip()
    if prelude:
        system_parts.append(prelude)
    system_message = "\n\n".join(system_parts)

    messages: list[dict] = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": envelope.get("user_message", "") or ""})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": bool(stream),
    }

    poster = http_post if http_post is not None else _http_post
    return poster(base_url, api_key, payload, out=out, stream=stream)


def _http_post(base_url: str, api_key: str, payload: dict, *, out, stream: bool) -> str:
    """Default HTTP transport. Stdlib only; SSE-streams when stream=True."""
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


def dispatch_workflow(fm: dict, inputs: dict) -> str:
    """POST to the n8n webhook at execution.entrypoint. Phase E2 / Phase H."""
    raise NotImplementedError("dispatch_workflow not yet wired (Phase E2/H — pending n8n)")


def dispatch_agent(fm: dict, agent_body: str, inputs: dict) -> str:
    """Agent loop with skills + MCP tools. Phase E3."""
    raise NotImplementedError("dispatch_agent not yet wired (Phase E3)")
