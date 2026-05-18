"""FastAPI app factory for the Control Panel.

FastAPI imports are local to this module; the package's __init__.py
stays import-light so the validate.py service-imports check passes.
"""
from __future__ import annotations

import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from .api import create_api_router
from .config import Config
from .features.install_jobs import get_job as get_install_job
from .features.install_jobs import stream_chunks as stream_install_chunks
from .runs import get_run, stream_chunks


def create_app(cfg: Config | None = None) -> FastAPI:
    cfg = cfg or Config.from_env()
    app = FastAPI(title="based-workspace control panel")
    app.state.cfg = cfg
    
    # Initialize SQLite — must run before any route can call into runs/db.
    from . import db as _db
    _db.init(cfg.workspace_root)
    
    # Initialize background scheduler
    from . import scheduler as _scheduler
    _scheduler.init(cfg)
    
    app.include_router(create_api_router())

    @app.get("/api/runs/{run_id}/stream")
    def run_stream(run_id: str) -> StreamingResponse:
        run = get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"run not found: {run_id}")

        def _iter():
            for chunk in stream_chunks(run):
                yield f"event: chunk\ndata: {json.dumps(chunk)}\n\n"
            payload = {"status": run.status, "error": run.error}
            yield f"event: done\ndata: {json.dumps(payload)}\n\n"

        return StreamingResponse(
            _iter(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @app.get("/api/v1/features/install/{job_id}/stream")
    def install_stream(job_id: str) -> StreamingResponse:
        """SSE stream of install-job log chunks. The terminal `done` event
        carries the final job status + result dict so the UI can stop
        streaming and render the outcome without a follow-up GET."""
        job = get_install_job(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail=f"install job not found: {job_id}")

        def _iter():
            for chunk in stream_install_chunks(job):
                yield f"event: chunk\ndata: {json.dumps(chunk)}\n\n"
            payload = {
                "status": job.status,
                "error": job.error,
                "result": job.result,
            }
            yield f"event: done\ndata: {json.dumps(payload)}\n\n"

        return StreamingResponse(
            _iter(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    @app.get("/api/v1/features/container/{feature_id}/logs/stream")
    def container_logs_stream(feature_id: str, tail: int = 200) -> StreamingResponse:
        """Live `podman logs -f` for a container feature, framed exactly like
        the install stream (`chunk` events + a terminal `done`) so the UI can
        reuse the same LogViewer. The follow process is killed when the client
        disconnects, with a 10-minute hard cap so a forgotten tab can't leak a
        worker forever."""
        import subprocess
        import time

        from .features import FeatureKind, FeatureRegistry

        reg = FeatureRegistry(cfg.workspace_root)
        feat = reg.get(FeatureKind.CONTAINER, feature_id)
        if feat is None:
            raise HTTPException(
                status_code=404, detail=f"container feature not found: {feature_id}"
            )
        name = str(feat.detail.get("container_name") or feature_id)

        def _iter():
            proc = subprocess.Popen(
                ["podman", "logs", "--tail", str(tail), "-f", name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            deadline = time.time() + 600
            try:
                assert proc.stdout is not None
                for line in proc.stdout:
                    yield f"event: chunk\ndata: {json.dumps(line)}\n\n"
                    if time.time() > deadline:
                        break
                yield (
                    "event: done\n"
                    f"data: {json.dumps({'status': 'done', 'error': None, 'result': None})}\n\n"
                )
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except Exception:  # noqa: BLE001
                    proc.kill()

        return StreamingResponse(
            _iter(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    return app
