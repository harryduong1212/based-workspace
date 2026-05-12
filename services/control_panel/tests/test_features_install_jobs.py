"""Unit tests for the async install-job runtime.

Targets `services/control_panel/features/install_jobs.py`:
  - start_install_job spawns a worker that calls registry.install and tees
    chunks to the job's queue
  - stream_chunks yields chunks until the sentinel
  - finished jobs replay output once and exit
  - redactor is applied when env_path is provided (G2 — secrets must not
    leak into the SSE stream or persisted log even if a handler logs them)
"""
from __future__ import annotations

import importlib.util
import tempfile
import time
import unittest
from pathlib import Path

_HAS_FASTAPI = all(
    importlib.util.find_spec(m) is not None for m in ("fastapi", "jinja2")
)


class _FakeRegistry:
    """Stub registry whose install() invokes log_sink with canned lines then
    returns a synthetic result. Avoids touching the real catalog."""

    def __init__(self, lines, result):
        self.lines = list(lines)
        self.result = dict(result)
        self.received_log_sink = None

    def install(self, kind, feature_id, inputs, log_sink=None):
        self.received_log_sink = log_sink
        for line in self.lines:
            if log_sink:
                log_sink(line)
        return self.result


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class StartInstallJobTest(unittest.TestCase):
    def _wait_done(self, job, timeout=2.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if job._done.is_set():
                return
            time.sleep(0.02)
        self.fail("job never finished")

    def test_success_path_captures_result_and_sets_status_done(self):
        from services.control_panel.features.install_jobs import start_install_job

        reg = _FakeRegistry(
            lines=["step 1", "step 2"],
            result={"ok": True, "feature": {"id": "x"}},
        )
        job = start_install_job(reg, "system", "x", inputs={})
        self._wait_done(job)
        self.assertEqual(job.status, "done")
        self.assertEqual(job.result["feature"]["id"], "x")
        # Both lines + the bracketed start/end framing land in output.
        self.assertIn("step 1", job.output)
        self.assertIn("step 2", job.output)
        self.assertIn("[install] starting", job.output)
        self.assertIn("[install] done", job.output)

    def test_handler_returning_ok_false_marks_error(self):
        from services.control_panel.features.install_jobs import start_install_job

        reg = _FakeRegistry(
            lines=["something went wrong"],
            result={"ok": False, "error": "compose exit 1"},
        )
        job = start_install_job(reg, "container", "postgres", inputs={})
        self._wait_done(job)
        self.assertEqual(job.status, "error")
        self.assertIn("compose exit 1", job.error)
        self.assertIn("[install] failed", job.output)

    def test_exception_during_install_recorded_as_error(self):
        from services.control_panel.features.install_jobs import start_install_job

        class _Boom:
            def install(self, *a, **kw):
                raise RuntimeError("kaboom")

        job = start_install_job(_Boom(), "system", "x", inputs={})
        self._wait_done(job)
        self.assertEqual(job.status, "error")
        self.assertIn("kaboom", job.error)
        self.assertIn("[install] exception", job.output)

    def test_redactor_scrubs_env_values_from_logs(self):
        """A handler that accidentally logs a value from .env must not leak
        it into the persisted log or the queue (G2)."""
        from services.control_panel.features.install_jobs import start_install_job

        tmp = Path(tempfile.mkdtemp())
        env_path = tmp / ".env"
        env_path.write_text("JIRA_API_TOKEN=eyJxxxxxxxxxxLONGTOKEN\n")

        reg = _FakeRegistry(
            lines=["see token eyJxxxxxxxxxxLONGTOKEN in error"],
            result={"ok": True},
        )
        job = start_install_job(reg, "connector", "jira", inputs={}, env_path=env_path)
        self._wait_done(job)
        self.assertNotIn("eyJxxxxxxxxxxLONGTOKEN", job.output)
        self.assertIn("[REDACTED:JIRA_API_TOKEN]", job.output)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class StreamChunksTest(unittest.TestCase):
    def test_finished_job_replays_output_once(self):
        from services.control_panel.features.install_jobs import (
            start_install_job,
            stream_chunks,
        )

        reg = _FakeRegistry(lines=["a", "b"], result={"ok": True})
        job = start_install_job(reg, "system", "x", inputs={})
        # Wait for completion before streaming so we hit the replay branch.
        deadline = time.time() + 2.0
        while time.time() < deadline and not job._done.is_set():
            time.sleep(0.02)
        self.assertTrue(job._done.is_set())

        chunks = list(stream_chunks(job))
        # Replay yields the whole output as one chunk and then exits.
        self.assertEqual(len(chunks), 1)
        self.assertIn("a", chunks[0])
        self.assertIn("b", chunks[0])


if __name__ == "__main__":
    unittest.main()
