"""Tests for Embedder — no real HTTP. The `http_post` callable seam lets us
return canned bytes (or raise canned errors) per test."""
from __future__ import annotations

import json
import unittest
import urllib.error

from services.skill_discovery_mcp.embedder import Embedder, EmbedderError


def _ok_response(vectors: list[list[float]]) -> bytes:
    return json.dumps(
        {"data": [{"embedding": v, "index": i} for i, v in enumerate(vectors)]}
    ).encode("utf-8")


class EmbedderHappyPath(unittest.TestCase):
    def test_embed_batch_returns_vectors_in_order(self) -> None:
        captured: dict[str, object] = {}

        def fake_post(url: str, body: bytes, headers: dict[str, str], timeout_s: float) -> bytes:
            captured["url"] = url
            captured["body"] = body
            captured["headers"] = headers
            captured["timeout_s"] = timeout_s
            return _ok_response([[0.1, 0.2], [0.3, 0.4]])

        emb = Embedder(base_url="http://x:1/v1", model="m", api_key="k", http_post=fake_post)
        out = emb.embed(["one", "two"])
        self.assertEqual(out, [[0.1, 0.2], [0.3, 0.4]])
        self.assertEqual(captured["url"], "http://x:1/v1/embeddings")
        body = json.loads(captured["body"])  # type: ignore[arg-type]
        self.assertEqual(body, {"model": "m", "input": ["one", "two"]})
        headers = captured["headers"]
        assert isinstance(headers, dict)
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(headers["Authorization"], "Bearer k")

    def test_embed_one_unwraps(self) -> None:
        emb = Embedder(http_post=lambda *a, **kw: _ok_response([[0.5, 0.6]]))
        self.assertEqual(emb.embed_one("hi"), [0.5, 0.6])

    def test_empty_input_no_request(self) -> None:
        called: list[None] = []

        def fake_post(*_a: object, **_kw: object) -> bytes:
            called.append(None)
            return b""

        emb = Embedder(http_post=fake_post)
        self.assertEqual(emb.embed([]), [])
        self.assertEqual(called, [])  # never hit the wire

    def test_strips_trailing_slash_on_base_url(self) -> None:
        captured: dict[str, str] = {}

        def fake_post(url: str, *_a: object, **_kw: object) -> bytes:
            captured["url"] = url
            return _ok_response([[0.0]])

        Embedder(base_url="http://x:1/v1/", http_post=fake_post).embed_one("hi")
        self.assertEqual(captured["url"], "http://x:1/v1/embeddings")


class EmbedderErrorPaths(unittest.TestCase):
    def test_http_error_is_wrapped(self) -> None:
        def fake_post(*_a: object, **_kw: object) -> bytes:
            raise urllib.error.HTTPError("u", 500, "boom", {}, None)  # type: ignore[arg-type]

        with self.assertRaises(EmbedderError):
            Embedder(http_post=fake_post).embed_one("x")

    def test_url_error_is_wrapped(self) -> None:
        def fake_post(*_a: object, **_kw: object) -> bytes:
            raise urllib.error.URLError("connection refused")

        with self.assertRaises(EmbedderError):
            Embedder(http_post=fake_post).embed_one("x")

    def test_bad_json_is_wrapped(self) -> None:
        emb = Embedder(http_post=lambda *a, **kw: b"<html>oops</html>")
        with self.assertRaises(EmbedderError):
            emb.embed_one("x")

    def test_short_data_array_is_wrapped(self) -> None:
        # Asked for 2, got 1 back — strict mismatch.
        emb = Embedder(http_post=lambda *a, **kw: _ok_response([[0.1]]))
        with self.assertRaises(EmbedderError):
            emb.embed(["a", "b"])

    def test_non_list_embedding_is_wrapped(self) -> None:
        bad = json.dumps({"data": [{"embedding": "not a list"}]}).encode()
        emb = Embedder(http_post=lambda *a, **kw: bad)
        with self.assertRaises(EmbedderError):
            emb.embed_one("x")


if __name__ == "__main__":
    unittest.main()
