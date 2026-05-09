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

    return app
