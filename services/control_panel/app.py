"""FastAPI app factory for the Control Panel.

FastAPI / Jinja imports are local to this module; the package's __init__.py
stays import-light so the validate.py service-imports check passes whether or
not the UI deps are installed.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import Config
from .health import all_checks
from .recipes_index import load_connectors, load_recipes


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


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

    return app
