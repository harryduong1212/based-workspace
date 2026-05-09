"""FastAPI app factory for the Control Panel.

FastAPI / Jinja imports are local to this module; the package's __init__.py
stays import-light so the validate.py service-imports check passes whether or
not the UI deps are installed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import json
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from .api import create_api_router
from .config import Config
from .connector_check import check_connector_env
from .connector_probes import has_probe, run_probe
from .env_writer import filter_to_allowed, update_env_file
from .health import all_checks
from .provider_options import default_model_ref, list_provider_options
from .recipe_skeleton import SUPPORTED_EXECUTION_TYPES, build_skeleton
from .recipe_writer import write_recipe
from .recipes_index import get_connector, get_recipe, load_connectors, load_recipes
from .render import render_markdown
from .runs import get_run, start_run, stream_chunks


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Hosts trusted for `.env` writes — same-machine only by policy. Public binds
# (Docker port-forward, 0.0.0.0) get the env editor disabled.
_LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _build_env_form_context(cfg: Config, fm: dict[str, Any], **extra: Any) -> dict[str, Any]:
    requires_env = list(fm.get("requires_env") or [])
    env_status = {v: bool(os.environ.get(v)) for v in requires_env}
    connector_id = str(fm.get("id") or "")
    connector_name = str(fm.get("name") or connector_id)
    env_path = cfg.workspace_root / ".env"
    try:
        env_path_relative = str(env_path.relative_to(cfg.workspace_root))
    except ValueError:
        env_path_relative = str(env_path)
    ctx: dict[str, Any] = {
        "connector": _ConnectorRef(id=connector_id, name=connector_name, description=str(fm.get("description") or "")),
        "requires_env": requires_env,
        "env_status": env_status,
        "env_path_relative": env_path_relative,
        "host": cfg.host,
        "safe_to_write": cfg.host in _LOCAL_HOSTS,
        "save_message": None,
        "save_ok": False,
        "saved_keys": [],
    }
    ctx.update(extra)
    return ctx


@dataclass(frozen=True)
class _RecipeRef:
    id: str
    name: str
    description: str


@dataclass(frozen=True)
class _ConnectorRef:
    id: str
    name: str
    description: str


def _build_recipe_context(cfg: Config, fm: dict[str, Any], path: Path, active_tab: str) -> dict[str, Any]:
    execution = fm.get("execution") or {}
    try:
        rel = path.relative_to(cfg.workspace_root)
    except ValueError:
        rel = path
    return {
        "recipe": _RecipeRef(
            id=str(fm.get("id") or path.stem),
            name=str(fm.get("name") or fm.get("id") or path.stem),
            description=str(fm.get("description") or ""),
        ),
        "active_tab": active_tab,
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
        "inputs": fm.get("inputs") or [],
        "outputs": fm.get("outputs") or [],
        "relative_path": str(rel).replace("\\", "/"),
    }


def create_app(cfg: Config | None = None) -> FastAPI:
    cfg = cfg or Config.from_env()
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
    app = FastAPI(title="based-workspace control panel")
    app.state.cfg = cfg
    # Initialize SQLite — must run before any route can call into runs/db.
    from . import db as _db
    _db.init(cfg.workspace_root)
    app.include_router(create_api_router())

    @app.get("/", response_class=HTMLResponse)
    def dashboard(request: Request) -> HTMLResponse:
        recipes = load_recipes(cfg)
        connectors = load_connectors(cfg)
        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "recipes": recipes,
                "connectors": connectors,
                "recipes_dir": cfg.recipes_dir,
                "connectors_dir": cfg.connectors_dir,
            },
        )

    @app.get("/api/health", response_class=HTMLResponse)
    def health(request: Request) -> HTMLResponse:
        statuses = all_checks(cfg)
        return templates.TemplateResponse(
            request=request,
            name="_health_fragment.html",
            context={"statuses": statuses},
        )

    @app.get("/recipes/new", response_class=HTMLResponse)
    def recipe_new_form(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request,
            name="recipe_new.html",
            context={"values": {}, "error": None},
        )

    @app.post("/recipes/new")
    async def recipe_new_submit(request: Request):
        form = await request.form()
        values = {
            "id": str(form.get("id") or "").strip(),
            "name": str(form.get("name") or "").strip(),
            "description": str(form.get("description") or "").strip(),
            "audience": str(form.get("audience") or "tech").strip(),
            "execution_type": str(form.get("execution_type") or "prompt").strip(),
            "tags": str(form.get("tags") or "").strip(),
        }

        def _render_form(error: str) -> HTMLResponse:
            return templates.TemplateResponse(
                request=request,
                name="recipe_new.html",
                context={"values": values, "error": error},
                status_code=400,
            )

        if not values["id"]:
            return _render_form("id is required")
        if values["execution_type"] not in SUPPORTED_EXECUTION_TYPES:
            return _render_form(f"execution_type must be one of {SUPPORTED_EXECUTION_TYPES}")
        if (cfg.recipes_dir / f"{values['id']}.md").exists():
            return _render_form(f"recipe {values['id']!r} already exists")

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
            return _render_form(str(e))

        result = write_recipe(cfg, values["id"], content)
        if not result.ok:
            return _render_form(result.message)
        return RedirectResponse(url=f"/recipes/{values['id']}/edit", status_code=303)

    @app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
    def recipe_overview(request: Request, recipe_id: str) -> HTMLResponse:
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, body, path = result
        ctx = _build_recipe_context(cfg, fm, path, active_tab="overview")
        ctx["rendered_body"] = render_markdown(body)
        return templates.TemplateResponse(request=request, name="recipe_overview.html", context=ctx)

    @app.get("/recipes/{recipe_id}/run", response_class=HTMLResponse)
    def recipe_run(request: Request, recipe_id: str) -> HTMLResponse:
        from . import db as _db
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, _body, path = result
        ctx = _build_recipe_context(cfg, fm, path, active_tab="run")
        recipe_default = fm.get("execution", {}).get("model")
        opts = list_provider_options(recipe_default)
        ctx["provider_options"] = opts
        ctx["default_model"] = default_model_ref(opts, recipe_default)
        ctx["last_inputs"] = _db.get_recipe_inputs(recipe_id)
        return templates.TemplateResponse(request=request, name="recipe_run.html", context=ctx)

    @app.post("/recipes/{recipe_id}/run")
    async def recipe_run_submit(request: Request, recipe_id: str) -> RedirectResponse:
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, body, _path = result
        form = await request.form()
        override = str(form.get("model_override") or "").strip()
        model_ref = override or str(form.get("model_ref") or "").strip()
        inputs: dict[str, str] = {}
        for key, value in form.multi_items():
            if key.startswith("input__"):
                inputs[key[len("input__"):]] = str(value)
        run = start_run(cfg, recipe_id, fm, body, inputs, model_ref)
        return RedirectResponse(url=f"/runs/{run.id}", status_code=303)

    @app.get("/runs/{run_id}", response_class=HTMLResponse)
    def run_view(request: Request, run_id: str) -> HTMLResponse:
        run = get_run(run_id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"run not found: {run_id}")
        return templates.TemplateResponse(request=request, name="run_view.html", context={"run": run})

    @app.get("/connectors/{connector_id}", response_class=HTMLResponse)
    def connector_detail(request: Request, connector_id: str) -> HTMLResponse:
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, body, path = result
        try:
            rel = path.relative_to(cfg.workspace_root)
        except ValueError:
            rel = path
        requires_env = list(fm.get("requires_env") or [])
        env_status = {v: bool(os.environ.get(v)) for v in requires_env}
        ctx = {
            "connector": _ConnectorRef(
                id=str(fm.get("id") or path.stem),
                name=str(fm.get("name") or fm.get("id") or path.stem),
                description=str(fm.get("description") or ""),
            ),
            "status": fm.get("status") or "",
            "auth_type": fm.get("auth_type") or "",
            "tags": list(fm.get("tags") or []),
            "provides": list(fm.get("provides") or []),
            "embed_collection": fm.get("embed_collection") or "",
            "n8n_workflow": fm.get("n8n_workflow") or "",
            "requires_env": requires_env,
            "env_status": env_status,
            "relative_path": str(rel).replace("\\", "/"),
            "rendered_body": render_markdown(body),
        }
        return templates.TemplateResponse(request=request, name="connector_detail.html", context=ctx)

    @app.get("/connectors/{connector_id}/env", response_class=HTMLResponse)
    def connector_env_form(request: Request, connector_id: str) -> HTMLResponse:
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, _body, _path = result
        ctx = _build_env_form_context(cfg, fm)
        return templates.TemplateResponse(request=request, name="connector_env_edit.html", context=ctx)

    @app.post("/connectors/{connector_id}/env", response_class=HTMLResponse)
    async def connector_env_save(request: Request, connector_id: str) -> HTMLResponse:
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, _body, _path = result
        if cfg.host not in _LOCAL_HOSTS:
            ctx = _build_env_form_context(
                cfg, fm,
                save_message="Refused: env editing is only allowed on a local bind.",
                save_ok=False,
            )
            return templates.TemplateResponse(request=request, name="_connector_env_form.html", context=ctx)

        form = await request.form()
        requires_env = list(fm.get("requires_env") or [])
        proposed: dict[str, str] = {}
        for var in requires_env:
            value = str(form.get(f"env__{var}") or "")
            if value:
                proposed[var] = value
        updates = filter_to_allowed(proposed, requires_env)

        save_ok = True
        saved_keys: list[str] = []
        if updates:
            try:
                update_env_file(cfg.workspace_root / ".env", updates)
                for k, v in updates.items():
                    os.environ[k] = v
                saved_keys = sorted(updates.keys())
                save_message = f"Saved {len(saved_keys)} variable{'' if len(saved_keys) == 1 else 's'} to .env."
            except OSError as e:
                save_ok = False
                save_message = f"Write failed: {e}"
        else:
            save_message = "Nothing to save — all fields were empty."

        ctx = _build_env_form_context(
            cfg, fm,
            save_message=save_message,
            save_ok=save_ok,
            saved_keys=saved_keys,
        )
        return templates.TemplateResponse(request=request, name="_connector_env_form.html", context=ctx)

    @app.post("/connectors/{connector_id}/test", response_class=HTMLResponse)
    def connector_test(request: Request, connector_id: str) -> HTMLResponse:
        result = get_connector(cfg, connector_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"connector not found: {connector_id}")
        fm, _body, _path = result
        check = check_connector_env(connector_id, list(fm.get("requires_env") or []))
        # Only run the live probe once env presence passes — no point hitting
        # the network if we already know creds are missing.
        probe = run_probe(connector_id) if check.all_present else None
        return templates.TemplateResponse(
            request=request,
            name="_connector_test_result.html",
            context={
                "result": check,
                "probe": probe,
                "probe_registered": has_probe(connector_id),
            },
        )

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

    @app.get("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
    def recipe_edit(request: Request, recipe_id: str) -> HTMLResponse:
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, _body, path = result
        ctx = _build_recipe_context(cfg, fm, path, active_tab="edit")
        ctx["raw_content"] = path.read_text(encoding="utf-8")
        return templates.TemplateResponse(request=request, name="recipe_edit.html", context=ctx)

    @app.post("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
    async def recipe_edit_save(request: Request, recipe_id: str) -> HTMLResponse:
        if get_recipe(cfg, recipe_id) is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        form = await request.form()
        content = str(form.get("content") or "")
        result = write_recipe(cfg, recipe_id, content)
        return templates.TemplateResponse(
            request=request,
            name="_save_result.html",
            context={"ok": result.ok, "message": result.message, "warnings": result.warnings},
        )

    return app
