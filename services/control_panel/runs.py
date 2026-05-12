"""Run registry — SQLite-backed for durability across restarts, with an
in-memory cache for active streaming.

Each "run" is a single call to `dispatch_prompt`. The dispatcher writes
streamed chunks to a `_ChunkSink` which forwards them to a queue; the SSE
endpoint pulls from the queue. Active-run state lives in a process-local
dict; on completion the row is finalized in SQLite (`db.finish_run`).
After a server restart, `get_run` hydrates rows from SQLite into read-only
Run objects (`_persisted_only=True`) so the SSE stream replays the saved
output as a single chunk.

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
from typing import Any, Callable, Iterator

from . import db
from .config import Config
from .env_writer import read_env_values


# Minimum env-value length to be considered a redaction target. Below this,
# false-positive risk is too high (e.g. POSTGRES_PORT=5432 should not cause
# every "5432" in output to get scrubbed).
_REDACT_MIN_LEN = 8


def _build_redactor(env_path: Path) -> Callable[[str], str]:
    """Build a redactor that scrubs any .env value from streamed output.

    Reads .env once at run start. Sorts values by length DESC so longer
    secrets redact before any substring. Values shorter than 8 chars are
    skipped to avoid scrubbing common literals like ports and booleans.
    Returns the identity function when .env is missing or has nothing
    worth redacting.
    """
    if not env_path.exists():
        return lambda s: s
    values = read_env_values(env_path)
    items = sorted(
        ((k, v) for k, v in values.items() if v and len(v) >= _REDACT_MIN_LEN),
        key=lambda kv: -len(kv[1]),
    )
    if not items:
        return lambda s: s

    def _redact(s: str) -> str:
        if not s:
            return s
        for key, val in items:
            if val in s:
                s = s.replace(val, f"[REDACTED:{key}]")
        return s

    return _redact


@dataclass
class Run:
    id: str
    recipe_id: str
    model_ref: str
    inputs: dict[str, str]
    started_at: datetime
    status: str = "running"  # running | done | error | abandoned
    output: str = ""
    error: str | None = None
    ended_at: datetime | None = None
    _persisted_only: bool = False
    _queue: "queue.Queue[str | None]" = field(default_factory=queue.Queue)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _done: threading.Event = field(default_factory=threading.Event)


_runs: dict[str, Run] = {}
_runs_lock = threading.Lock()


class _ChunkSink:
    """File-like that fans chunks to the run's queue while accumulating output.

    The optional `redactor` is applied to every chunk before persistence
    and streaming — so any env-value that leaks into LLM output or workflow
    response never lands in SQLite or the SSE stream verbatim.
    """

    def __init__(self, run: Run, redactor: Callable[[str], str] | None = None):
        self.run = run
        self._redact = redactor or (lambda s: s)

    def write(self, s: str) -> int:
        if not s:
            return 0
        s = self._redact(s)
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
    db.insert_run(
        run_id=run.id,
        recipe_id=recipe_id,
        model_ref=model_ref,
        inputs=dict(inputs),
        started_at=run.started_at,
    )
    db.save_recipe_inputs(recipe_id, dict(inputs))
    with _runs_lock:
        _runs[run.id] = run

    # Build the redactor once per run so .env values never reach SQLite or
    # the SSE stream verbatim (G2 in the security-posture memory).
    redactor = _build_redactor(Path(cfg.workspace_root) / ".env")

    def _worker() -> None:
        is_async_workflow = False
        try:
            from scripts import recipe_manager as rm  # type: ignore
            from services.recipe_runtime.dispatcher import (
                dispatch_agent,
                dispatch_prompt,
                dispatch_workflow,
            )
            from services.recipe_runtime.prompt_assembler import assemble

            execution_type = fm.get("execution", {}).get("type", "prompt")

            if execution_type == "workflow":
                inputs_with_run_id = dict(inputs)
                inputs_with_run_id["_run_id"] = run.id
                result = dispatch_workflow(fm, inputs_with_run_id, workspace_root=str(cfg.workspace_root))

                is_async_workflow = fm.get("execution", {}).get("async", False)
                if is_async_workflow:
                    db.update_run_n8n_id(run.id, result)
                else:
                    with run._lock:
                        run.output = redactor(result)
                    run.status = "done"
            elif execution_type == "agent":
                agent_section = (
                    rm._extract_section(body, "Agent")
                    or rm._extract_section(body, "Prompt")
                    or body
                )
                skill_ids = list(fm.get("requires_skills") or [])
                skill_bodies = rm._load_skill_bodies(skill_ids)
                # Honor model_ref override from the UI/Routine layer.
                if model_ref:
                    fm = {**fm, "execution": {**(fm.get("execution") or {}), "model": model_ref}}
                dispatch_agent(
                    fm,
                    agent_section,
                    inputs,
                    workspace_root=str(cfg.workspace_root),
                    skill_bodies=skill_bodies,
                    out=_ChunkSink(run, redactor=redactor),
                )
                run.status = "done"
            else:
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
                    out=_ChunkSink(run, redactor=redactor),
                    stream=True,
                )
                run.status = "done"
        except Exception as e:  # noqa: BLE001 — surface anything to the UI
            run.error = f"{type(e).__name__}: {e}"
            run.status = "error"
            is_async_workflow = False  # If it failed to dispatch, it's not pending anymore
        finally:
            if not is_async_workflow:
                run.ended_at = datetime.now(timezone.utc)
                try:
                    db.finish_run(
                        run_id=run.id,
                        status=run.status,
                        output=run.output,
                        error=run.error,
                    )
                except Exception:
                    pass  # never let persistence break the streaming finalization
                run._queue.put(None)
                run._done.set()

    threading.Thread(target=_worker, name=f"run-{run.id}", daemon=True).start()
    return run


def get_run(run_id: str) -> Run | None:
    """Return a Run for `run_id`. Active runs come from the in-memory cache;
    older runs are hydrated from SQLite as read-only objects."""
    with _runs_lock:
        cached = _runs.get(run_id)
    if cached is not None:
        return cached
    row = db.get_run_row(run_id)
    if row is None:
        return None
    run = Run(
        id=row.id,
        recipe_id=row.recipe_id,
        model_ref=row.model_ref,
        inputs=dict(row.inputs),
        started_at=row.started_at,
        status=row.status,
        output=row.output,
        error=row.error,
        ended_at=row.ended_at,
        _persisted_only=True,
    )
    run._done.set()
    return run


def stream_chunks(run: Run) -> Iterator[str]:
    """Yield chunks as they arrive; stop when the sentinel arrives.

    For runs hydrated from the DB (`_persisted_only`), replay the full saved
    output as a single chunk and return — there's no live queue to drain."""
    if run._persisted_only:
        if run.output:
            yield run.output
        return
    while True:
        chunk = run._queue.get()
        if chunk is None:
            return
        yield chunk
