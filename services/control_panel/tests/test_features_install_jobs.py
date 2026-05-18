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
    returns a synthetic result. No resolve_install_plan → exercises the
    worker's single-step fallback path. Avoids touching the real catalog."""

    def __init__(self, lines, result):
        self.lines = list(lines)
        self.result = dict(result)
        self.received_log_sink = None

    def install(self, kind, feature_id, inputs, log_sink=None, skip_prereq_check=False):
        self.received_log_sink = log_sink
        for line in self.lines:
            if log_sink:
                log_sink(line)
        return self.result


class _PlanRegistry:
    """Stub registry WITH resolve_install_plan — exercises the cascade path.
    Records the order install() was called in so tests can assert deps-first."""

    def __init__(self, plan, results):
        self._plan = plan  # list[{id, kind, status}]
        self._results = results  # {id: result_dict}
        self.calls: list[str] = []

    def resolve_install_plan(self, kind, feature_id):
        return list(self._plan)

    def install(self, kind, feature_id, inputs, log_sink=None, skip_prereq_check=False):
        self.calls.append(feature_id)
        if log_sink:
            log_sink(f"installing {feature_id}")
        return self._results[feature_id]


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
class CascadeTest(unittest.TestCase):
    def _wait_done(self, job, timeout=2.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if job._done.is_set():
                return
            time.sleep(0.02)
        self.fail("job never finished")

    def test_cascade_installs_prereqs_deps_first_then_target(self):
        from services.control_panel.features.install_jobs import start_install_job

        plan = [
            {"id": "qdrant", "kind": "container", "status": "available"},
            {"id": "llama-swap", "kind": "container", "status": "stopped"},
            {"id": "memory", "kind": "mcp", "status": "available"},
        ]
        reg = _PlanRegistry(plan, {
            "qdrant": {"ok": True},
            "llama-swap": {"ok": True},
            "memory": {"ok": True, "feature": {"id": "memory"}},
        })
        job = start_install_job(reg, "mcp", "memory", inputs={})
        self._wait_done(job)

        self.assertEqual(job.status, "done")
        # Prereqs ran first, in plan order, target last.
        self.assertEqual(reg.calls, ["qdrant", "llama-swap", "memory"])
        # Step headers give the user a progress signal.
        self.assertIn("Step 1/3", job.output)
        self.assertIn("Step 3/3", job.output)
        self.assertIn("all steps done", job.output)
        # Final result is the target's.
        self.assertEqual(job.result["feature"]["id"], "memory")

    def test_cascade_aborts_on_prereq_failure(self):
        from services.control_panel.features.install_jobs import start_install_job

        plan = [
            {"id": "qdrant", "kind": "container", "status": "available"},
            {"id": "memory", "kind": "mcp", "status": "available"},
        ]
        reg = _PlanRegistry(plan, {
            "qdrant": {"ok": False, "error": "compose up failed"},
            "memory": {"ok": True},
        })
        job = start_install_job(reg, "mcp", "memory", inputs={})
        self._wait_done(job)

        self.assertEqual(job.status, "error")
        self.assertIn("compose up failed", job.error)
        # Target never attempted once a prereq failed.
        self.assertEqual(reg.calls, ["qdrant"])
        self.assertIn("aborting cascade", job.output)

    def test_unknown_prereq_step_errors_clearly(self):
        from services.control_panel.features.install_jobs import start_install_job

        plan = [
            {"id": "ghost", "kind": None, "status": "missing"},
            {"id": "memory", "kind": "mcp", "status": "available"},
        ]
        reg = _PlanRegistry(plan, {"memory": {"ok": True}})
        job = start_install_job(reg, "mcp", "memory", inputs={})
        self._wait_done(job)

        self.assertEqual(job.status, "error")
        self.assertIn("ghost", job.error)
        self.assertEqual(reg.calls, [])  # nothing installable was attempted

    def test_only_target_receives_inputs(self):
        from services.control_panel.features.install_jobs import start_install_job

        seen: dict[str, dict] = {}

        class _Recorder(_PlanRegistry):
            def install(self, kind, feature_id, inputs, log_sink=None, skip_prereq_check=False):
                seen[feature_id] = inputs
                return super().install(kind, feature_id, inputs, log_sink, skip_prereq_check)

        plan = [
            {"id": "qdrant", "kind": "container", "status": "available"},
            {"id": "jira", "kind": "connector", "status": "available"},
        ]
        reg = _Recorder(plan, {"qdrant": {"ok": True}, "jira": {"ok": True}})
        start_install_job(reg, "connector", "jira", inputs={"env": {"JIRA_API_TOKEN": "x"}})
        deadline = time.time() + 2.0
        while time.time() < deadline and "jira" not in seen:
            time.sleep(0.02)
        # Target gets the user inputs; auto-pulled prereq gets none.
        self.assertEqual(seen["jira"], {"env": {"JIRA_API_TOKEN": "x"}})
        self.assertEqual(seen["qdrant"], {})


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
