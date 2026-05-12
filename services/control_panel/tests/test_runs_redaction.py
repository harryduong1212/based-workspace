"""Unit tests for output redaction (G2 in security-posture memory).

`_build_redactor` reads .env and returns a callable that scrubs any value
of length >= 8 from streamed/persisted output. The `_ChunkSink` applies
that redactor before persistence and before queueing the chunk for the SSE
stream — so secrets never land in SQLite or hit the browser verbatim, even
if an LLM accidentally echoes them.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

_HAS_FASTAPI = all(
    importlib.util.find_spec(m) is not None for m in ("fastapi", "jinja2")
)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class BuildRedactorTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def _env(self, body: str) -> Path:
        path = self.dir / ".env"
        path.write_text(body)
        return path

    def test_long_value_gets_redacted(self):
        from services.control_panel.runs import _build_redactor

        path = self._env("JIRA_API_TOKEN=eyJxxxxxxxxxxLOOOONGTOKEN\n")
        r = _build_redactor(path)
        out = r("the model said: eyJxxxxxxxxxxLOOOONGTOKEN is the token")
        self.assertNotIn("eyJxxxxxxxxxxLOOOONGTOKEN", out)
        self.assertIn("[REDACTED:JIRA_API_TOKEN]", out)

    def test_short_value_is_not_redacted(self):
        """Values shorter than 8 chars (e.g. ports, booleans) must not match."""
        from services.control_panel.runs import _build_redactor

        path = self._env("POSTGRES_PORT=5432\nDEBUG=true\n")
        r = _build_redactor(path)
        # Both values are short — the redactor must leave them alone.
        out = r("postgres on 5432 with debug true")
        self.assertEqual(out, "postgres on 5432 with debug true")

    def test_empty_value_is_skipped(self):
        from services.control_panel.runs import _build_redactor

        path = self._env("ANTHROPIC_API_KEY=\nOTHER_REAL_TOKEN=xxxxxxxxxxxxxxxx\n")
        r = _build_redactor(path)
        # Empty value would otherwise match every empty string in input — must be skipped.
        out = r("hello world ")
        self.assertEqual(out, "hello world ")
        # Real token still scrubs:
        self.assertIn("[REDACTED:OTHER_REAL_TOKEN]", r("see xxxxxxxxxxxxxxxx now"))

    def test_missing_env_returns_identity(self):
        from services.control_panel.runs import _build_redactor

        r = _build_redactor(self.dir / "nonexistent.env")
        sample = "anything at all, including obviously-secret-looking strings like ABC123XYZ789LONG"
        self.assertEqual(r(sample), sample)

    def test_longer_value_redacts_before_shorter_substring(self):
        """If a longer secret contains a shorter one (or vice versa), the
        longer must redact first so the inner substring doesn't leak."""
        from services.control_panel.runs import _build_redactor

        # The long token contains the short one as a substring.
        path = self._env(
            "SHORTISH=ABCDEFGHIJ\n"
            "LONGISH=ABCDEFGHIJKLMNOPQRST\n"
        )
        r = _build_redactor(path)
        out = r("payload starts ABCDEFGHIJKLMNOPQRST and continues")
        # Long token replaced — not a partial substring redaction.
        self.assertIn("[REDACTED:LONGISH]", out)
        self.assertNotIn("ABCDEFGHIJKLMNOPQRST", out)
        self.assertNotIn("[REDACTED:SHORTISH]KLMNOPQRST", out)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class ChunkSinkRedactionTest(unittest.TestCase):
    def _make_run(self):
        from services.control_panel.runs import Run
        from datetime import datetime, timezone

        return Run(
            id="t",
            recipe_id="r",
            model_ref="m",
            inputs={},
            started_at=datetime.now(timezone.utc),
        )

    def test_chunk_sink_applies_redactor_to_output_and_queue(self):
        from services.control_panel.runs import _ChunkSink

        run = self._make_run()
        sink = _ChunkSink(run, redactor=lambda s: s.replace("secret", "[REDACTED]"))
        sink.write("this is a secret value here")
        # Output buffer (persisted) is redacted.
        self.assertIn("[REDACTED]", run.output)
        self.assertNotIn("secret", run.output)
        # Queue carries the redacted chunk.
        queued = run._queue.get(timeout=1)
        self.assertIn("[REDACTED]", queued)

    def test_chunk_sink_without_redactor_is_pass_through(self):
        from services.control_panel.runs import _ChunkSink

        run = self._make_run()
        sink = _ChunkSink(run)
        sink.write("no redactor here")
        self.assertEqual(run.output, "no redactor here")

    def test_empty_chunk_short_circuits(self):
        from services.control_panel.runs import _ChunkSink

        run = self._make_run()
        calls = []

        def _track(s):
            calls.append(s)
            return s

        sink = _ChunkSink(run, redactor=_track)
        sink.write("")
        # No call → no enqueue (preserves prior behaviour where empty chunks
        # don't drive the SSE stream).
        self.assertEqual(calls, [])
        self.assertTrue(run._queue.empty())


if __name__ == "__main__":
    unittest.main()
