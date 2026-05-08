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

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from .config import Config
from .health import all_checks
from .provider_options import default_model_ref, list_provider_options
from .recipe_writer import write_recipe
from .recipes_index import get_recipe, load_connectors, load_recipes
from .render import render_markdown
from .runs import get_run, start_run, stream_chunks


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


@dataclass(frozen=True)
class _RecipeRef:
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
        result = get_recipe(cfg, recipe_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"recipe not found: {recipe_id}")
        fm, _body, path = result
        ctx = _build_recipe_context(cfg, fm, path, active_tab="run")
        recipe_default = fm.get("execution", {}).get("model")
        opts = list_provider_options(recipe_default)
        ctx["provider_options"] = opts
        ctx["default_model"] = default_model_ref(opts, recipe_default)
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
