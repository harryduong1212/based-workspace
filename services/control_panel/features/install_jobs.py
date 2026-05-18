"""Async install-job runtime — mirror of runs.py for feature installs.

Each call to POST /api/v1/features/{kind}/{id}/install starts a job: a
daemon thread runs `registry.install(kind, feature_id, inputs, log_sink=sink)`,
the sink fans chunks into a queue (consumed by SSE) and accumulates output
for later replay. The dict result of install() lands in `job.result`.

Threading model mirrors `runs.py`:
  - One daemon worker thread per job.
  - `output` accumulates under a per-job lock.
  - Sentinel `None` on the queue marks end-of-stream; `_done_event` lets
    SSE waiters block without polling.

Redaction
---------
The log sink is wrapped with the same `_build_redactor` used for run output
(G2 in security-posture). Any handler that accidentally logs a value from
`.env` (e.g. a Postgres password embedded in a connection-string error)
has it scrubbed before persistence and before queuing for SSE.
"""
from __future__ import annotations

import queue
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

from services.control_panel.runs import _build_redactor


@dataclass
class InstallJob:
    id: str
    kind: str
    feature_id: str
    inputs: dict[str, Any]
    started_at: datetime
    status: str = "running"  # running | done | error
    output: str = ""
    error: str | None = None
    ended_at: datetime | None = None
    result: dict[str, Any] | None = None
    _queue: "queue.Queue[str | None]" = field(default_factory=queue.Queue)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _done: threading.Event = field(default_factory=threading.Event)


_jobs: dict[str, InstallJob] = {}
_jobs_lock = threading.Lock()


class _LogSink:
    """Callable handlers invoke as `log_sink('podman compose up -d ...\\n')`.

    Auto-appends a trailing newline if absent so step lines render correctly
    in the dialog. Applies the redactor before persistence + SSE — secrets
    never reach the browser or SQLite verbatim, even if a handler logs
    something a user pasted into .env.
    """

    def __init__(self, job: InstallJob, redactor: Callable[[str], str]):
        self._job = job
        self._redact = redactor

    def __call__(self, s: str) -> None:
        if not s:
            return
        if not s.endswith("\n"):
            s = s + "\n"
        s = self._redact(s)
        with self._job._lock:
            self._job.output += s
        self._job._queue.put(s)


def start_install_job(
    registry: Any,
    kind: Any,
    feature_id: str,
    inputs: dict[str, Any] | None,
    *,
    env_path: Path | None = None,
) -> InstallJob:
    """Spawn a thread that runs `registry.install(...)` while teeing chunks.

    `env_path` enables the redactor (typically `<workspace_root>/.env`).
    """
    job = InstallJob(
        id=uuid.uuid4().hex[:12],
        kind=kind.value if hasattr(kind, "value") else str(kind),
        feature_id=feature_id,
        inputs=dict(inputs or {}),
        started_at=datetime.now(timezone.utc),
    )
    with _jobs_lock:
        _jobs[job.id] = job

    redactor = _build_redactor(env_path) if env_path else (lambda s: s)
    sink = _LogSink(job, redactor)

    def _worker() -> None:
        try:
            sink(f"[install] starting {job.kind}/{job.feature_id}")

            # Resolve the cascade: every not-yet-installed prerequisite
            # (deps-first) then the target. Falls back to a single step if the
            # registry can't plan (e.g. a fake registry in tests).
            try:
                plan = registry.resolve_install_plan(kind, feature_id)
            except AttributeError:
                plan = [{"id": feature_id, "kind": job.kind, "status": "unknown"}]
            if not plan:
                plan = [{"id": feature_id, "kind": job.kind, "status": "unknown"}]

            from .base import FeatureKind  # local import keeps __init__ light

            total = len(plan)
            if total > 1:
                ordered = " -> ".join(s["id"] for s in plan)
                sink(f"[install] plan ({total} steps): {ordered}")

            result: dict = {"ok": False, "error": "empty plan"}
            failed = False
            for i, step in enumerate(plan, 1):
                sid = step["id"]
                skind_raw = step.get("kind")
                sink(f"=== Step {i}/{total}: {skind_raw or '?'}/{sid} ===")
                if skind_raw is None:
                    job.error = f"unknown prerequisite {sid!r} — install it manually first"
                    sink(f"[install] failed: {job.error}")
                    result = {"ok": False, "error": job.error}
                    failed = True
                    break

                step_kind = FeatureKind(skind_raw)
                # Only the target receives the user's inputs (e.g. connector
                # env); auto-pulled prereqs take none.
                step_inputs = inputs if sid == feature_id else {}
                # skip_prereq_check: the plan already ordered deps-first, so
                # the per-call gate would just race the just-started service.
                result = registry.install(
                    step_kind, sid, step_inputs, log_sink=sink, skip_prereq_check=True
                )
                if not result.get("ok"):
                    job.error = result.get("error") or f"step {sid} reported ok=false"
                    sink(
                        f"[install] failed: step {i}/{total} ({sid}) — "
                        f"{job.error}; aborting cascade"
                    )
                    failed = True
                    break

            job.result = result
            if failed:
                job.status = "error"
            else:
                job.status = "done"
                sink(f"[install] done — all steps done ({total} step(s) completed)")
        except Exception as e:  # noqa: BLE001 — surface to UI
            job.status = "error"
            job.error = f"{type(e).__name__}: {e}"
            sink(f"[install] exception: {job.error}")
        finally:
            job.ended_at = datetime.now(timezone.utc)
            job._queue.put(None)
            job._done.set()

    threading.Thread(target=_worker, name=f"install-{job.id}", daemon=True).start()
    return job


def get_job(job_id: str) -> InstallJob | None:
    with _jobs_lock:
        return _jobs.get(job_id)


def stream_chunks(job: InstallJob) -> Iterator[str]:
    """Yield chunks as they arrive. For finished jobs, replay the saved
    output as a single chunk and return — there's no live queue to drain
    after the worker has signalled done."""
    if job._done.is_set():
        if job.output:
            yield job.output
        return
    while True:
        chunk = job._queue.get()
        if chunk is None:
            return
        yield chunk


def job_to_dict(job: InstallJob) -> dict[str, Any]:
    """JSON-serializable snapshot for the GET endpoint."""
    return {
        "id": job.id,
        "kind": job.kind,
        "feature_id": job.feature_id,
        "status": job.status,
        "started_at": job.started_at.isoformat(),
        "ended_at": job.ended_at.isoformat() if job.ended_at else None,
        "output": job.output,
        "error": job.error,
        "result": job.result,
    }
