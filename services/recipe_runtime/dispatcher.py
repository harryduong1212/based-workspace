"""Recipe runtime dispatcher.

Three execution.types map to three dispatch functions:

    prompt    → dispatch_prompt    (Phase E1 — wired, multi-provider)
    workflow  → dispatch_workflow  (Phase E2 / Phase H; n8n)
    agent     → dispatch_agent     (Phase E3)

dispatch_prompt routes via the provider registry in `providers/`. Recipes
declare a model as either a bare id (`gemma-3-4b` → defaults to the local
provider) or a `provider/model_id` ref (`anthropic/claude-opus-4-7`,
`gemini/gemini-2.0-flash`). Adding a new provider = one module in
`providers/` plus a registry entry.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from .providers import get_provider, parse_model_ref
from .providers.local import _post_openai_chat


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
    """Send the assembled envelope to the resolved provider.

    Resolution precedence:
      model    : envelope["model"]  > default_model  > $RECIPE_DEFAULT_MODEL
      provider : everything before the first '/' in the resolved model id;
                 bare ids default to the `local` provider.

    `base_url` and `api_key` only apply to the `local` provider (and to the
    `http_post` injection seam used in tests). Other providers read their
    own credentials from the environment (`GEMINI_API_KEY`, `ANTHROPIC_API_KEY`).

    `http_post` is preserved for unit tests and bypasses the provider
    registry — when supplied, the call goes straight through with the
    OpenAI-shape payload.
    """
    out = sys.stdout if out is None else out

    raw_model = (
        envelope.get("model")
        or default_model
        or os.environ.get("RECIPE_DEFAULT_MODEL")
    )
    if not raw_model:
        raise ValueError(
            "no model resolvable: set execution.model in the recipe, "
            "pass default_model, or set RECIPE_DEFAULT_MODEL in the environment"
        )

    provider_name, model_id = parse_model_ref(raw_model)
    messages = _build_messages(envelope, skill_bodies)

    # Test injection seam: bypass provider registry, send OpenAI-shape payload
    # to the supplied transport. Used by services.recipe_runtime.tests.
    if http_post is not None:
        resolved_base = (base_url or os.environ.get("OPENAI_API_BASE") or "http://localhost:11434/v1").rstrip("/")
        resolved_key = api_key or os.environ.get("OPENAI_API_KEY") or "local-no-auth"
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": bool(stream),
        }
        return http_post(resolved_base, resolved_key, payload, out=out, stream=stream)

    # Local provider honors explicit base_url/api_key overrides for parity
    # with the pre-refactor signature; other providers ignore them.
    if provider_name == "local" and (base_url or api_key):
        return _post_openai_chat(
            base_url=(base_url or os.environ.get("LLAMA_SWAP_URL") or os.environ.get("OPENAI_API_BASE") or "http://localhost:11434/v1").rstrip("/"),
            api_key=api_key or os.environ.get("OPENAI_API_KEY") or "local-no-auth",
            messages=messages,
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
            out=out,
        )

    provider = get_provider(provider_name)
    return provider.dispatch_chat(
        messages,
        model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=stream,
        out=out,
    )


def _build_messages(envelope: dict, skill_bodies: list[str] | None) -> list[dict]:
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
    return messages


def dispatch_workflow(fm: dict, inputs: dict, workspace_root: str | None = None) -> str:
    """POST to the n8n webhook at execution.entrypoint. Phase E2 / Phase H.

    URL resolution:
      - If we can read the .n8n file (workspace_root provided) AND N8N_API_KEY is set,
        we look the workflow up in n8n by name and build the atom8n-fork URL:
        `{base}/webhook/{workflow_id}/{node_name_lowercased_double_encoded}/{path}`.
      - Otherwise we fall back to upstream n8n's convention `{base}/webhook/{path}`.
    """
    base_url = os.environ.get("N8N_WEBHOOK_BASE", "http://localhost:5678").rstrip("/")
    api_key = os.environ.get("N8N_API_KEY")
    entrypoint = fm.get("execution", {}).get("entrypoint", "")

    url = None
    if workspace_root and api_key and entrypoint.endswith(".n8n"):
        try:
            url = _resolve_atom8n_webhook_url(workspace_root, entrypoint, base_url, api_key)
        except Exception:
            url = None  # fall through to upstream convention

    if url is None:
        path_seg = (
            os.path.basename(entrypoint)[:-4]
            if entrypoint.endswith(".n8n")
            else entrypoint.lstrip("/")
        )
        url = f"{base_url}/webhook/{path_seg}"

    payload = json.dumps({"inputs": inputs, "recipe": fm}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")

    is_async = fm.get("execution", {}).get("async", False)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
            if is_async:
                try:
                    data = json.loads(body)
                    return data.get("executionId", "pending")
                except json.JSONDecodeError:
                    return "pending"
            return body
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"n8n workflow failed ({e.code}): {error_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"n8n connection failed: {e.reason}") from e


def _resolve_atom8n_webhook_url(
    workspace_root: str, entrypoint: str, base_url: str, api_key: str
) -> str | None:
    """Read the local .n8n file + ask n8n's public API for the workflow id, then
    build the atom8n fork's webhook URL. The node-name segment is double-encoded
    so n8n's HTTP layer decodes once to match the value stored in webhook_entity
    (e.g., `webhook%20trigger`). Returns None if anything can't be resolved."""
    from pathlib import Path
    from urllib.parse import quote as urlquote

    wf_path = Path(workspace_root) / entrypoint
    if not wf_path.is_file():
        return None
    wf_def = json.loads(wf_path.read_text(encoding="utf-8"))
    wf_name = wf_def.get("name")
    nodes = wf_def.get("nodes") or []
    webhook_node = next(
        (n for n in nodes if (n.get("type") or "").endswith("webhook")), None
    )
    if not (wf_name and webhook_node):
        return None
    node_name = webhook_node.get("name") or ""
    node_path = (webhook_node.get("parameters") or {}).get("path") or ""

    req = urllib.request.Request(f"{base_url}/api/v1/workflows")
    req.add_header("X-N8N-API-KEY", api_key)
    with urllib.request.urlopen(req, timeout=10) as resp:
        wfs = json.loads(resp.read().decode("utf-8")).get("data", [])
    match = next((w for w in wfs if w.get("name") == wf_name), None)
    if not match:
        return None
    workflow_id = match.get("id")

    encoded_node = urlquote(node_name.lower(), safe="").replace("%", "%25")
    return f"{base_url}/webhook/{workflow_id}/{encoded_node}/{node_path}"


ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"
MAX_AGENT_ITERATIONS = 10


def dispatch_agent(
    fm: dict,
    agent_body: str,
    inputs: dict,
    *,
    workspace_root: str | None = None,
    skill_bodies: list[str] | None = None,
    max_tokens: int = 4096,
    out=None,
    http_post=None,
) -> str:
    """Multi-turn agent loop against Anthropic's Messages API.

    Loop: send (system + history + tool catalog) → if response carries
    tool_use blocks, invoke each, append tool_results to history, continue.
    Stops on `stop_reason == "end_turn"`, no tool_use blocks, or
    MAX_AGENT_ITERATIONS — whichever comes first.

    Anthropic-only for now. Provider abstraction will come when a second
    tool-use-capable provider matters (Gemini tool_calls have different
    semantics; not worth the layer until needed).

    `http_post` is an injection seam for tests: when supplied it replaces
    the urllib call and receives `(url, headers, payload) -> response_dict`.
    """
    import sys as _sys
    out = _sys.stdout if out is None else out

    raw_model = (fm.get("execution") or {}).get("model") or os.environ.get(
        "RECIPE_DEFAULT_MODEL"
    )
    if not raw_model:
        raise ValueError("no model resolvable for agent dispatch")
    provider_name, model_id = parse_model_ref(raw_model)
    if provider_name != "anthropic":
        raise NotImplementedError(
            f"dispatch_agent currently supports anthropic only; got provider {provider_name!r}"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and http_post is None:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment")

    from .prompt_assembler import substitute_inputs
    from .agent_tools import get_tool_catalog, invoke_tool

    system_parts = [sb.strip() for sb in (skill_bodies or []) if sb and sb.strip()]
    user_message, _applied = substitute_inputs(agent_body or "", inputs)
    tools = get_tool_catalog(fm, workspace_root=workspace_root)

    messages: list[dict] = [{"role": "user", "content": user_message}]
    accumulated: list[str] = []

    for _ in range(MAX_AGENT_ITERATIONS):
        payload = {
            "model": model_id,
            "max_tokens": max_tokens,
            # Snapshot the history so the captured payload doesn't reflect
            # later mutations from the same iteration (matters for testing
            # and for any http_post that retains the request).
            "messages": list(messages),
        }
        if system_parts:
            payload["system"] = "\n\n".join(system_parts)
        if tools:
            payload["tools"] = tools

        response = _anthropic_messages(
            api_key=api_key,
            payload=payload,
            http_post=http_post,
        )

        # Mirror the full assistant message back into history (tool_use blocks
        # included) — Anthropic requires this for tool_result correlation.
        messages.append({"role": "assistant", "content": response.get("content") or []})

        tool_uses: list[dict] = []
        for block in response.get("content") or []:
            btype = block.get("type")
            if btype == "text":
                text = block.get("text") or ""
                if text:
                    accumulated.append(text)
                    try:
                        out.write(text)
                        out.flush()
                    except Exception:
                        pass
            elif btype == "tool_use":
                tool_uses.append(block)

        if response.get("stop_reason") == "end_turn" or not tool_uses:
            break

        tool_results = []
        for tu in tool_uses:
            try:
                result = invoke_tool(
                    tu.get("name") or "",
                    tu.get("input") or {},
                    workspace_root=workspace_root,
                )
            except Exception as e:  # noqa: BLE001 — surface error to the agent
                result = f"error: {type(e).__name__}: {e}"
            tool_results.append(
                {"type": "tool_result", "tool_use_id": tu.get("id"), "content": result}
            )
        messages.append({"role": "user", "content": tool_results})

    return "".join(accumulated)


def _anthropic_messages(*, api_key: str | None, payload: dict, http_post=None) -> dict:
    """POST to Anthropic Messages API. Returns the parsed JSON response.

    If `http_post` is supplied (tests), we delegate. Otherwise this uses
    stdlib HTTP to keep the runtime SDK-free (same pattern as the existing
    Anthropic provider for prompt dispatch).
    """
    if http_post is not None:
        return http_post(payload)

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{ANTHROPIC_BASE_URL}/messages",
        data=body,
        method="POST",
    )
    req.add_header("x-api-key", api_key or "")
    req.add_header("anthropic-version", ANTHROPIC_VERSION)
    req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"anthropic messages failed ({e.code}): {error_body}") from e
