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
import uuid

from . import db
from . import scheduler
from .config import Config
from .connector_check import check_connector_env
from .connector_probes import has_probe, run_probe
from .env_writer import filter_to_allowed, update_env_file
from .health import all_checks
from .recipes_index import get_connector, get_recipe, load_connectors, load_recipes
from .render import render_markdown


_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _is_trusted_callback_peer(peer: str) -> bool:
    """Return True when the peer IP is loopback or RFC 1918 / link-local — the
    legitimate origins for an n8n container talking to the host. We do NOT trust
    the Host header (client-controllable); only the actual TCP peer."""
    if peer in _LOCAL_HOSTS:
        return True
    try:
        import ipaddress
        ip = ipaddress.ip_address(peer)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except (ValueError, ImportError):
        return False


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
            "raw_content": path.read_text(encoding="utf-8"),
        }

    @router.post("/recipes/new")
    async def recipe_new_submit(request: Request) -> dict[str, Any]:
        from .recipe_skeleton import SUPPORTED_EXECUTION_TYPES, build_skeleton
        from .recipe_writer import write_recipe
        cfg = _cfg(request)
        
        req_json = await request.json()
        values = {
            "id": str(req_json.get("id") or "").strip(),
            "name": str(req_json.get("name") or "").strip(),
            "description": str(req_json.get("description") or "").strip(),
            "audience": str(req_json.get("audience") or "tech").strip(),
            "execution_type": str(req_json.get("execution_type") or "prompt").strip(),
            "tags": str(req_json.get("tags") or "").strip(),
        }

        if not values["id"]:
            raise HTTPException(status_code=400, detail="id is required")
        if values["execution_type"] not in SUPPORTED_EXECUTION_TYPES:
            raise HTTPException(status_code=400, detail=f"execution_type must be one of {SUPPORTED_EXECUTION_TYPES}")
        if (cfg.recipes_dir / f"{values['id']}.md").exists():
            raise HTTPException(status_code=400, detail=f"recipe {values['id']!r} already exists")

        tags = [t.strip() for t in values["tags"].split(",") if t.strip()]
        try:
            content = build_skeleton(
                recipe_id=values["id"],
                name=values["name"] or values["id"],
                description=values["description"] or "TODO: describe what this recipe does.",
                audience=values["audience"] or "tech",
                tags=tags,
                execution_type=values["execution_type"],
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        result = write_recipe(cfg, values["id"], content)
        if not result.ok:
            raise HTTPException(status_code=400, detail=result.message)
        return {"id": values["id"]}

    @router.post("/recipes/{recipe_id}/edit")
    async def recipe_edit_save(request: Request, recipe_id: str) -> dict[str, Any]:
        from .recipe_writer import write_recipe
        cfg = _cfg(request)
        if get_recipe(cfg, recipe_id) is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
            
        req_json = await request.json()
        content = str(req_json.get("content") or "")
        result = write_recipe(cfg, recipe_id, content)
        return {
            "ok": result.ok,
            "message": result.message,
            "warnings": result.warnings,
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

    @router.get("/routines")
    def list_routines(request: Request) -> list[dict[str, Any]]:
        del request
        rows = db.list_routines()
        return [
            {
                "id": r.id,
                "recipe_id": r.recipe_id,
                "model_ref": r.model_ref,
                "inputs": r.inputs,
                "schedule": r.schedule,
                "enabled": r.enabled,
                "created_at": r.created_at.isoformat(timespec="seconds"),
                "updated_at": r.updated_at.isoformat(timespec="seconds"),
            }
            for r in rows
        ]

    @router.post("/routines")
    async def save_routine(request: Request) -> dict[str, Any]:
        cfg = _cfg(request)
        req_json = await request.json()
        
        routine_id = str(req_json.get("id") or "").strip() or uuid.uuid4().hex[:12]
        recipe_id = str(req_json.get("recipe_id") or "").strip()
        model_ref = str(req_json.get("model_ref") or "").strip()
        schedule = str(req_json.get("schedule") or "").strip()
        enabled = bool(req_json.get("enabled", True))
        inputs = req_json.get("inputs") or {}
        
        if not recipe_id or not schedule:
            raise HTTPException(status_code=400, detail="recipe_id and schedule are required")
            
        try:
            from apscheduler.triggers.cron import CronTrigger
            CronTrigger.from_crontab(schedule)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid cron schedule: {e}")
            
        if get_recipe(cfg, recipe_id) is None:
            raise HTTPException(status_code=400, detail=f"recipe not found: {recipe_id}")
            
        db.upsert_routine(
            id=routine_id,
            recipe_id=recipe_id,
            model_ref=model_ref,
            inputs=inputs,
            schedule=schedule,
            enabled=enabled,
        )
        scheduler.sync_routine(cfg, routine_id)
        return {"id": routine_id}

    @router.delete("/routines/{routine_id}")
    def delete_routine(request: Request, routine_id: str) -> dict[str, Any]:
        cfg = _cfg(request)
        db.delete_routine(routine_id)
        scheduler.sync_routine(cfg, routine_id)
        return {"ok": True}

    @router.post("/n8n/callback/{run_id}")
    async def n8n_callback(request: Request, run_id: str) -> dict[str, Any]:
        # Use the underlying TCP peer — the Host header is client-controllable.
        # We accept loopback + RFC 1918 / link-local so an n8n container on a
        # docker/podman bridge can reach the host (peer IP is the container's
        # bridge address, e.g. 10.x.y.z).
        client_host = request.client.host if request.client else ""
        if not _is_trusted_callback_peer(client_host):
            raise HTTPException(status_code=403, detail="callback restricted to private networks")

        # Idempotency: n8n retries a callback if it doesn't see a 2xx. Without this
        # guard a retry would overwrite a finished run (or worse, stomp on a hydrated
        # _persisted_only=True Run that lacks a live queue).
        existing = db.get_run_row(run_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"run not found: {run_id}")
        if existing.status != "running":
            return {"ok": True, "noop": True}

        req_json = await request.json()
        output = req_json.get("output", "")
        error = req_json.get("error")
        status = "error" if error else "done"

        db.finish_run(run_id=run_id, status=status, output=output, error=error)

        # Update the in-memory run if it's still live in this process.
        from .runs import get_run
        run = get_run(run_id)
        if run and not run._persisted_only:
            with run._lock:
                run.output = output
            run.error = error
            run.status = status
            run.ended_at = db._parse_iso(db._now_iso())
            run._queue.put(output)
            run._queue.put(None)
            run._done.set()

        return {"ok": True}

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

    @router.get("/providers")
    def list_providers(request: Request, recipe_default: str | None = None) -> dict[str, Any]:
        from .provider_options import list_provider_options, default_model_ref
        opts = list_provider_options(recipe_default)
        return {
            "options": [
                {"provider": o.provider, "models": o.models, "available": o.available}
                for o in opts
            ],
            "default_model": default_model_ref(opts, recipe_default)
        }

    @router.post("/recipes/{recipe_id}/run")
    async def recipe_run_submit(request: Request, recipe_id: str) -> dict[str, Any]:
        from .runs import start_run
        cfg = _cfg(request)
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, body, _path = result
        
        req_json = await request.json()
        model_ref = str(req_json.get("model_ref") or "").strip()
        inputs = req_json.get("inputs") or {}
        if not isinstance(inputs, dict):
            raise HTTPException(status_code=400, detail="`inputs` must be a dictionary")
            
        run = start_run(cfg, recipe_id, fm, body, {str(k): str(v) for k, v in inputs.items()}, model_ref)
        return {"id": run.id}

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

    # ---- features (the install/uninstall/verify page) ------------------

    def _registry(request: Request):
        from .features import FeatureRegistry

        return FeatureRegistry(_cfg(request).workspace_root)

    def _kind_or_404(kind: str):
        from .features import FeatureKind

        try:
            return FeatureKind(kind)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"unknown feature kind {kind!r}")

    @router.get("/features")
    def features_list(request: Request):
        registry = _registry(request)
        features = registry.all_features()
        return {
            "features": [f.to_dict() for f in features],
            "kinds": [k.value for k in registry.kinds()],
        }

    @router.get("/features/{kind}/{feature_id}")
    def features_get(request: Request, kind: str, feature_id: str):
        k = _kind_or_404(kind)
        registry = _registry(request)
        feature = registry.get(k, feature_id)
        if feature is None:
            raise HTTPException(status_code=404, detail=f"feature {feature_id!r} not found in {kind}")
        return {
            "feature": feature.to_dict(),
            "unmet_prereqs": registry.unmet_prereqs(feature),
        }

    @router.post("/features/{kind}/{feature_id}/install")
    async def features_install(request: Request, kind: str, feature_id: str):
        k = _kind_or_404(kind)
        try:
            body = await request.json()
        except Exception:
            body = {}
        if not isinstance(body, dict):
            raise HTTPException(status_code=400, detail="body must be a JSON object")
        registry = _registry(request)
        return registry.install(k, feature_id, body)

    @router.post("/features/{kind}/{feature_id}/uninstall")
    def features_uninstall(request: Request, kind: str, feature_id: str):
        k = _kind_or_404(kind)
        registry = _registry(request)
        return registry.uninstall(k, feature_id)

    @router.post("/features/{kind}/{feature_id}/verify")
    def features_verify(request: Request, kind: str, feature_id: str):
        k = _kind_or_404(kind)
        registry = _registry(request)
        return registry.verify(k, feature_id)

    @router.post("/features/{kind}/{feature_id}/preview")
    async def features_preview(request: Request, kind: str, feature_id: str):
        """Describe what install(inputs) would do, without side effects.

        Drives the pre-install confirmation dialog: the UI calls preview with
        the exact inputs it would POST to /install, renders the returned
        side_effects + warnings, then either confirms (→ POST /install) or
        cancels (no-op).
        """
        k = _kind_or_404(kind)
        try:
            body = await request.json()
        except Exception:
            body = {}
        if not isinstance(body, dict):
            raise HTTPException(status_code=400, detail="body must be a JSON object")
        registry = _registry(request)
        return registry.preview(k, feature_id, body)

    return router
