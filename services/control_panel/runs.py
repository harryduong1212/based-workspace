"""In-memory run registry + threaded dispatch.

Each "run" is a single call to `dispatch_prompt`. The dispatcher writes
streamed chunks to a `_ChunkSink` which forwards them to a queue; the SSE
endpoint pulls from the queue. Run state is kept in a process-local dict —
the panel is single-user / localhost so this is fine; switch to Redis or a
DB if we ever multi-tenant.

Threading model:
  - One worker thread per run, daemon=True so the process can exit cleanly.
  - `output` accumulates the full text under a per-run lock.
  - Sentinel `None` on the queue signals end-of-stream; `_done_event` lets
    waiters block without polling.
"""
from __future__ import annotations

import queue
import sys
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .config import Config


@dataclass
class Run:
    id: str
    recipe_id: str
    model_ref: str
    inputs: dict[str, str]
    started_at: datetime
    status: str = "running"  # running | done | error
    output: str = ""
    error: str | None = None
    _queue: "queue.Queue[str | None]" = field(default_factory=queue.Queue)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _done: threading.Event = field(default_factory=threading.Event)


_runs: dict[str, Run] = {}
_runs_lock = threading.Lock()


class _ChunkSink:
    """File-like that fans chunks to the run's queue while accumulating output."""

    def __init__(self, run: Run):
        self.run = run

    def write(self, s: str) -> int:
        if not s:
            return 0
        with self.run._lock:
            self.run.output += s
        self.run._queue.put(s)
        return len(s)

    def flush(self) -> None:
        pass


def _ensure_workspace_on_path(cfg: Config) -> None:
    p = str(cfg.workspace_root)
    if p not in sys.path:
        sys.path.insert(0, p)


def start_run(
    cfg: Config,
    recipe_id: str,
    fm: dict[str, Any],
    body: str,
    inputs: dict[str, str],
    model_ref: str,
) -> Run:
    """Spawn a worker that dispatches the recipe and streams chunks."""
    _ensure_workspace_on_path(cfg)

    run = Run(
        id=uuid.uuid4().hex[:12],
        recipe_id=recipe_id,
        model_ref=model_ref,
        inputs=dict(inputs),
        started_at=datetime.now(timezone.utc),
    )
    with _runs_lock:
        _runs[run.id] = run

    def _worker() -> None:
        try:
            from scripts import recipe_manager as rm  # type: ignore
            from services.recipe_runtime.dispatcher import dispatch_prompt
            from services.recipe_runtime.prompt_assembler import assemble

            prompt_section = (
                rm._extract_section(body, "Prompt")
                or rm._extract_section(body, "Agent")
                or body
            )
            envelope = assemble(fm, prompt_section, inputs)
            if model_ref:
                envelope["model"] = model_ref

            skill_bodies = rm._load_skill_bodies(envelope.get("skill_ids") or [])
            dispatch_prompt(
                envelope,
                skill_bodies=skill_bodies,
                out=_ChunkSink(run),
                stream=True,
            )
            run.status = "done"
        except Exception as e:  # noqa: BLE001 — surface anything to the UI
            run.error = f"{type(e).__name__}: {e}"
            run.status = "error"
        finally:
            run._queue.put(None)
            run._done.set()

    threading.Thread(target=_worker, name=f"run-{run.id}", daemon=True).start()
    return run


def get_run(run_id: str) -> Run | None:
    with _runs_lock:
        return _runs.get(run_id)


def stream_chunks(run: Run) -> Iterator[str]:
    """Yield chunks as they arrive; stop when the sentinel arrives."""
    while True:
        chunk = run._queue.get()
        if chunk is None:
            return
        yield chunk
