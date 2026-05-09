"""JSON API routes for the Next.js frontend (`services/control_panel/web/`).

Mounted at `/api/v1/*`. The HTML/Jinja routes in `app.py` stay live during
the rebuild — the new frontend talks to this module exclusively via fetch,
proxied through `next.config.ts` rewrites.

Conventions:
- Responses are plain `dict` / `list[dict]` with snake_case keys.
- 404s match the HTML routes' behavior (`HTTPException(404, ...)`).
- No pagination — workspace lists are small (single-digit connectors,
  ~12 recipes). Switch to cursored when this grows past a couple hundred.
"""
from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from . import db
from .config import Config
from .connector_check import check_connector_env
from .connector_probes import has_probe, run_probe
from .env_writer import filter_to_allowed, update_env_file
from .health import all_checks
from .recipes_index import get_connector, get_recipe, load_connectors, load_recipes
from .render import render_markdown


_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _cfg(request: Request) -> Config:
    return request.app.state.cfg


def create_api_router() -> APIRouter:
    router = APIRouter(prefix="/api/v1", tags=["api-v1"])

    @router.get("/dashboard")
    def dashboard(request: Request) -> dict[str, Any]:
        cfg = _cfg(request)
        recipes = [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "audience": r.audience,
                "status": r.status,
                "tags": r.tags,
                "execution_type": r.execution_type,
                "execution_model": r.execution_model,
            }
            for r in load_recipes(cfg)
        ]
        connectors = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
            }
            for c in load_connectors(cfg)
        ]
        return {"recipes": recipes, "connectors": connectors}

    @router.get("/health")
    def health(request: Request) -> list[dict[str, Any]]:
        return [
            {"name": s.name, "ok": s.ok, "detail": s.detail}
            for s in all_checks(_cfg(request))
        ]

    @router.get("/recipes/{recipe_id}")
    def recipe_detail(request: Request, recipe_id: str) -> dict[str, Any]:
        cfg = _cfg(request)
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, body, path = result
        try:
            rel = path.relative_to(cfg.workspace_root)
        except ValueError:
            rel = path
        execution = fm.get("execution") or {}
        return {
            "id": str(fm.get("id") or path.stem),
            "name": str(fm.get("name") or fm.get("id") or path.stem),
            "description": str(fm.get("description") or ""),
            "status": fm.get("status") or "",
            "version": fm.get("version") or "",
            "audience": fm.get("audience") or "",
            "cost": fm.get("cost") or "",
            "tags": list(fm.get("tags") or []),
            "execution_type": execution.get("type") or "prompt",
            "execution_model": execution.get("model"),
            "requires_skills": list(fm.get("requires_skills") or []),
            "requires_workflows": list(fm.get("requires_workflows") or []),
            "requires_connectors": list(fm.get("requires_connectors") or []),
            "requires_mcp": list(fm.get("requires_mcp") or []),
            "requires_env": list(fm.get("requires_env") or []),
            "triggers": fm.get("triggers") or {},
            "inputs": list(fm.get("inputs") or []),
            "outputs": list(fm.get("outputs") or []),
            "rendered_body": render_markdown(body),
            "relative_path": str(rel).replace("\\", "/"),
        }

    @router.get("/connectors/{connector_id}")
    def connector_detail(request: Request, connector_id: str) -> dict[str, Any]:
        cfg = _cfg(request)
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, body, path = result
        try:
            rel = path.relative_to(cfg.workspace_root)
        except ValueError:
            rel = path
        requires_env = list(fm.get("requires_env") or [])
        return {
            "id": str(fm.get("id") or path.stem),
            "name": str(fm.get("name") or fm.get("id") or path.stem),
            "description": str(fm.get("description") or ""),
            "status": fm.get("status") or "",
            "auth_type": fm.get("auth_type") or "",
            "tags": list(fm.get("tags") or []),
            "provides": list(fm.get("provides") or []),
            "embed_collection": fm.get("embed_collection") or "",
            "n8n_workflow": fm.get("n8n_workflow") or "",
            "requires_env": [
                {"name": v, "present": bool(os.environ.get(v))} for v in requires_env
            ],
            "rendered_body": render_markdown(body),
            "relative_path": str(rel).replace("\\", "/"),
            "probe_registered": has_probe(connector_id),
            "host": cfg.host,
            "safe_to_write_env": cfg.host in _LOCAL_HOSTS,
        }

    @router.post("/connectors/{connector_id}/env")
    async def connector_env_save(request: Request, connector_id: str) -> dict[str, Any]:
        cfg = _cfg(request)
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, _body, _path = result
        if cfg.host not in _LOCAL_HOSTS:
            raise HTTPException(
                status_code=403,
                detail="env editing is only allowed on a local bind (127.0.0.1).",
            )
        body = await request.json()
        if not isinstance(body, dict):
            raise HTTPException(status_code=400, detail="body must be a JSON object")
        values = body.get("values") or {}
        if not isinstance(values, dict):
            raise HTTPException(status_code=400, detail="`values` must be an object")

        requires_env = list(fm.get("requires_env") or [])
        proposed = {
            str(k): str(v)
            for k, v in values.items()
            if isinstance(v, str) and v != ""
        }
        updates = filter_to_allowed(proposed, requires_env)
        if not updates:
            return {
                "ok": True,
                "saved_keys": [],
                "message": "Nothing to save — all fields were empty.",
            }
        try:
            update_env_file(cfg.workspace_root / ".env", updates)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"write failed: {e}")
        for k, v in updates.items():
            os.environ[k] = v
        saved_keys = sorted(updates.keys())
        return {
            "ok": True,
            "saved_keys": saved_keys,
            "message": f"Saved {len(saved_keys)} variable{'' if len(saved_keys) == 1 else 's'} to .env.",
        }

    @router.get("/runs")
    def list_runs(request: Request, limit: int = 25, recipe_id: str | None = None) -> list[dict[str, Any]]:
        del request
        rows = db.recent_runs(limit=max(1, min(limit, 200)), recipe_id=recipe_id)
        return [
            {
                "id": r.id,
                "recipe_id": r.recipe_id,
                "model_ref": r.model_ref,
                "status": r.status,
                "error": r.error,
                "started_at": r.started_at.isoformat(timespec="seconds"),
                "ended_at": r.ended_at.isoformat(timespec="seconds") if r.ended_at else None,
            }
            for r in rows
        ]

    @router.get("/runs/{run_id}")
    def get_run(request: Request, run_id: str) -> dict[str, Any]:
        del request
        row = db.get_run_row(run_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"run not found: {run_id}")
        return {
            "id": row.id,
            "recipe_id": row.recipe_id,
            "model_ref": row.model_ref,
            "inputs": row.inputs,
            "status": row.status,
            "error": row.error,
            "output": row.output,
            "started_at": row.started_at.isoformat(timespec="seconds"),
            "ended_at": row.ended_at.isoformat(timespec="seconds") if row.ended_at else None,
        }

    @router.get("/recipes/{recipe_id}/last-inputs")
    def last_inputs(request: Request, recipe_id: str) -> dict[str, str]:
        cfg = _cfg(request)
        if get_recipe(cfg, recipe_id) is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        return db.get_recipe_inputs(recipe_id)

    @router.post("/connectors/{connector_id}/test")
    def connector_test(request: Request, connector_id: str) -> dict[str, Any]:
        cfg = _cfg(request)
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, _body, _path = result
        requires_env = list(fm.get("requires_env") or [])
        check = check_connector_env(connector_id, requires_env)
        probe = run_probe(connector_id) if check.all_present else None
        return {
            "env_check": {
                "all_present": check.all_present,
                "missing": list(check.missing),
            },
            "probe": (
                None if probe is None else {"ok": probe.ok, "message": probe.message}
            ),
            "probe_registered": has_probe(connector_id),
        }

    return router
