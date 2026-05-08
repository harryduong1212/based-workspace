"""Unit tests for the provider registry and individual providers.

Network is stubbed via urllib.request.urlopen monkeypatching — no sockets open.
"""
from __future__ import annotations

import io
import json
import os
import unittest
import urllib.request
from contextlib import contextmanager

from services.recipe_runtime import providers as registry
from services.recipe_runtime.providers.anthropic import AnthropicProvider
from services.recipe_runtime.providers.gemini import GeminiProvider
from services.recipe_runtime.providers.local import LocalProvider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@contextmanager
def env(**kwargs):
    """Temporarily set/clear env vars; restore on exit."""
    keys = list(kwargs)
    saved = {k: os.environ.get(k) for k in keys}
    for k, v in kwargs.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    try:
        yield
    finally:
        for k in keys:
            if saved[k] is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = saved[k]


class _FakeResp:
    """Stand-in for the urllib response object."""

    def __init__(self, body=b"", lines=None, status=200):
        self._body = body
        self._lines = lines or []
        self.status = status

    def read(self):
        return self._body

    def __iter__(self):
        return iter(self._lines)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


@contextmanager
def patch_urlopen(handler):
    """Replace urllib.request.urlopen with `handler(req, timeout=...)`."""
    original = urllib.request.urlopen
    urllib.request.urlopen = handler
    try:
        yield
    finally:
        urllib.request.urlopen = original


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class ParseModelRefTest(unittest.TestCase):
    def test_provider_and_model(self):
        self.assertEqual(registry.parse_model_ref("anthropic/claude-opus-4-7"),
                         ("anthropic", "claude-opus-4-7"))

    def test_bare_id_defaults_to_local(self):
        self.assertEqual(registry.parse_model_ref("gemma-3-4b"), ("local", "gemma-3-4b"))

    def test_strips_whitespace(self):
        self.assertEqual(registry.parse_model_ref("  gemini/gemini-2.0-flash  "),
                         ("gemini", "gemini-2.0-flash"))

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            registry.parse_model_ref("")
        with self.assertRaises(ValueError):
            registry.parse_model_ref("   ")

    def test_malformed_raises(self):
        with self.assertRaises(ValueError):
            registry.parse_model_ref("/model")
        with self.assertRaises(ValueError):
            registry.parse_model_ref("provider/")


class GetProviderTest(unittest.TestCase):
    def test_known_returns_provider(self):
        p = registry.get_provider("local")
        self.assertEqual(p.name, "local")

    def test_unknown_raises_with_known_listed(self):
        with self.assertRaises(ValueError) as cm:
            registry.get_provider("nope")
        msg = str(cm.exception)
        self.assertIn("nope", msg)
        self.assertIn("anthropic", msg)
        self.assertIn("gemini", msg)
        self.assertIn("local", msg)

    def test_list_providers_sorted(self):
        names = registry.list_providers()
        self.assertEqual(names, sorted(names))
        self.assertIn("local", names)

    def test_available_reflects_env(self):
        with env(GEMINI_API_KEY=None, ANTHROPIC_API_KEY=None):
            avail = registry.available_providers()
            self.assertIn("local", avail)
            self.assertNotIn("gemini", avail)
            self.assertNotIn("anthropic", avail)
        with env(GEMINI_API_KEY="x", ANTHROPIC_API_KEY="y"):
            avail = registry.available_providers()
            self.assertIn("gemini", avail)
            self.assertIn("anthropic", avail)


# ---------------------------------------------------------------------------
# Local provider
# ---------------------------------------------------------------------------


class LocalProviderTest(unittest.TestCase):
    def test_always_available(self):
        self.assertTrue(LocalProvider().available())

    def test_dispatch_chat_streams_chunks(self):
        sse = [
            b'data: {"choices":[{"delta":{"content":"hel"}}]}\n',
            b'data: {"choices":[{"delta":{"content":"lo"}}]}\n',
            b'data: [DONE]\n',
        ]
        captured = {}

        def handler(req, timeout=None):
            captured["url"] = req.full_url
            captured["headers"] = dict(req.header_items())
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return _FakeResp(lines=sse)

        out = io.StringIO()
        with patch_urlopen(handler), env(LLAMA_SWAP_URL="http://test:9999/v1", OPENAI_API_KEY=None):
            text = LocalProvider().dispatch_chat(
                [{"role": "user", "content": "hi"}],
                "gemma-3-4b",
                max_tokens=64,
                temperature=0.1,
                stream=True,
                out=out,
            )
        self.assertEqual(text, "hello")
        self.assertEqual(captured["url"], "http://test:9999/v1/chat/completions")
        self.assertEqual(captured["body"]["model"], "gemma-3-4b")
        self.assertTrue(captured["body"]["stream"])

    def test_dispatch_chat_non_stream(self):
        body = json.dumps({"choices": [{"message": {"content": "done"}}]}).encode()

        def handler(req, timeout=None):
            return _FakeResp(body=body)

        out = io.StringIO()
        with patch_urlopen(handler), env(LLAMA_SWAP_URL="http://t/v1", OPENAI_API_KEY=None):
            text = LocalProvider().dispatch_chat(
                [{"role": "user", "content": "hi"}],
                "m",
                max_tokens=64,
                temperature=0.0,
                stream=False,
                out=out,
            )
        self.assertEqual(text, "done")
        self.assertIn("done", out.getvalue())


# ---------------------------------------------------------------------------
# Gemini provider
# ---------------------------------------------------------------------------


class GeminiProviderTest(unittest.TestCase):
    def test_available_requires_key(self):
        with env(GEMINI_API_KEY=None):
            self.assertFalse(GeminiProvider().available())
        with env(GEMINI_API_KEY="x"):
            self.assertTrue(GeminiProvider().available())

    def test_list_models_nonempty(self):
        models = GeminiProvider().list_models()
        self.assertTrue(models)
        self.assertTrue(any("gemini" in m for m in models))

    def test_dispatch_uses_gemini_base_url_and_key(self):
        body = json.dumps({"choices": [{"message": {"content": "g"}}]}).encode()
        captured = {}

        def handler(req, timeout=None):
            captured["url"] = req.full_url
            captured["auth"] = req.headers.get("Authorization")
            return _FakeResp(body=body)

        with patch_urlopen(handler), env(GEMINI_API_KEY="sekret"):
            text = GeminiProvider().dispatch_chat(
                [{"role": "user", "content": "hi"}],
                "gemini-2.0-flash",
                max_tokens=64,
                temperature=0.0,
                stream=False,
                out=io.StringIO(),
            )
        self.assertEqual(text, "g")
        self.assertIn("generativelanguage.googleapis.com", captured["url"])
        self.assertEqual(captured["auth"], "Bearer sekret")

    def test_dispatch_without_key_raises(self):
        with env(GEMINI_API_KEY=None):
            with self.assertRaises(RuntimeError):
                GeminiProvider().dispatch_chat(
                    [{"role": "user", "content": "hi"}],
                    "gemini-2.0-flash",
                    max_tokens=64,
                    temperature=0.0,
                    stream=False,
                    out=io.StringIO(),
                )


# ---------------------------------------------------------------------------
# Anthropic provider
# ---------------------------------------------------------------------------


class AnthropicProviderTest(unittest.TestCase):
    def test_available_requires_key(self):
        with env(ANTHROPIC_API_KEY=None):
            self.assertFalse(AnthropicProvider().available())
        with env(ANTHROPIC_API_KEY="x"):
            self.assertTrue(AnthropicProvider().available())

    def test_dispatch_translates_system_role(self):
        """OpenAI-shape system message → top-level system field."""
        body = json.dumps({
            "content": [{"type": "text", "text": "answer"}]
        }).encode()
        captured = {}

        def handler(req, timeout=None):
            captured["url"] = req.full_url
            captured["headers"] = {k.lower(): v for k, v in req.header_items()}
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return _FakeResp(body=body)

        with patch_urlopen(handler), env(ANTHROPIC_API_KEY="sk-test"):
            text = AnthropicProvider().dispatch_chat(
                [
                    {"role": "system", "content": "be concise"},
                    {"role": "user", "content": "hi"},
                ],
                "claude-opus-4-7",
                max_tokens=64,
                temperature=0.0,
                stream=False,
                out=io.StringIO(),
            )
        self.assertEqual(text, "answer")
        self.assertEqual(captured["body"]["system"], "be concise")
        self.assertEqual(captured["body"]["messages"], [{"role": "user", "content": "hi"}])
        self.assertEqual(captured["headers"]["x-api-key"], "sk-test")
        self.assertIn("anthropic-version", captured["headers"])

    def test_dispatch_streams_text_deltas(self):
        sse = [
            b'data: {"type":"content_block_delta","delta":{"type":"text_delta","text":"hel"}}\n',
            b'data: {"type":"content_block_delta","delta":{"type":"text_delta","text":"lo"}}\n',
            b'data: {"type":"message_stop"}\n',
        ]

        def handler(req, timeout=None):
            return _FakeResp(lines=sse)

        out = io.StringIO()
        with patch_urlopen(handler), env(ANTHROPIC_API_KEY="x"):
            text = AnthropicProvider().dispatch_chat(
                [{"role": "user", "content": "hi"}],
                "claude-opus-4-7",
                max_tokens=64,
                temperature=0.0,
                stream=True,
                out=out,
            )
        self.assertEqual(text, "hello")

    def test_dispatch_without_key_raises(self):
        with env(ANTHROPIC_API_KEY=None):
            with self.assertRaises(RuntimeError):
                AnthropicProvider().dispatch_chat(
                    [{"role": "user", "content": "hi"}],
                    "claude-opus-4-7",
                    max_tokens=64,
                    temperature=0.0,
                    stream=False,
                    out=io.StringIO(),
                )


# ---------------------------------------------------------------------------
# Dispatcher routing through providers
# ---------------------------------------------------------------------------


class DispatcherProviderRoutingTest(unittest.TestCase):
    """Uses the live registry — verifies the dispatcher reaches the right provider."""

    def test_provider_slash_model_routes_to_anthropic(self):
        from services.recipe_runtime.dispatcher import dispatch_prompt
        body = json.dumps({"content": [{"type": "text", "text": "claude-said"}]}).encode()
        captured = {}

        def handler(req, timeout=None):
            captured["url"] = req.full_url
            return _FakeResp(body=body)

        with patch_urlopen(handler), env(ANTHROPIC_API_KEY="k"):
            out = io.StringIO()
            text = dispatch_prompt(
                {"model": "anthropic/claude-opus-4-7", "user_message": "hi"},
                stream=False,
                out=out,
            )
        self.assertEqual(text, "claude-said")
        self.assertIn("api.anthropic.com", captured["url"])

    def test_bare_model_falls_back_to_local(self):
        from services.recipe_runtime.dispatcher import dispatch_prompt
        body = json.dumps({"choices": [{"message": {"content": "local-said"}}]}).encode()
        captured = {}

        def handler(req, timeout=None):
            captured["url"] = req.full_url
            return _FakeResp(body=body)

        with patch_urlopen(handler), env(LLAMA_SWAP_URL="http://local:1/v1"):
            out = io.StringIO()
            text = dispatch_prompt(
                {"model": "gemma-3-4b", "user_message": "hi"},
                stream=False,
                out=out,
            )
        self.assertEqual(text, "local-said")
        self.assertIn("local:1", captured["url"])


if __name__ == "__main__":
    unittest.main()
