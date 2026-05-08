"""Read-only loaders for recipes and connectors.

Wraps the existing scripts.recipe_manager / scripts.connector_manager helpers
so the FastAPI routes don't depend on argparse-shaped CLI internals. Pure
stdlib + PyYAML — no FastAPI imports here.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import Config


def _ensure_scripts_on_path(cfg: Config) -> None:
    scripts_path = str(cfg.workspace_root)
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)


@dataclass(frozen=True)
class RecipeSummary:
    id: str
    name: str
    description: str
    audience: str
    status: str
    tags: list[str]
    execution_type: str
    execution_model: str | None
    path: Path


@dataclass(frozen=True)
class ConnectorSummary:
    id: str
    name: str
    description: str
    path: Path


def load_recipes(cfg: Config) -> list[RecipeSummary]:
    _ensure_scripts_on_path(cfg)
    from scripts import recipe_manager as rm  # type: ignore

    out: list[RecipeSummary] = []
    for path, fm, _body, parse_err in rm.load_all_recipes():
        if parse_err or not isinstance(fm, dict):
            continue
        execution = fm.get("execution") or {}
        out.append(
            RecipeSummary(
                id=str(fm.get("id") or path.stem),
                name=str(fm.get("name") or fm.get("id") or path.stem),
                description=str(fm.get("description") or ""),
                audience=str(fm.get("audience") or ""),
                status=str(fm.get("status") or ""),
                tags=list(fm.get("tags") or []),
                execution_type=str(execution.get("type") or "prompt"),
                execution_model=execution.get("model"),
                path=Path(path),
            )
        )
    out.sort(key=lambda r: r.id)
    return out


def load_connectors(cfg: Config) -> list[ConnectorSummary]:
    _ensure_scripts_on_path(cfg)
    from scripts import connector_manager as cm  # type: ignore

    out: list[ConnectorSummary] = []
    for path, fm, _body, parse_err in cm.load_all_connectors():
        if parse_err or not isinstance(fm, dict):
            continue
        out.append(
            ConnectorSummary(
                id=str(fm.get("id") or path.stem),
                name=str(fm.get("name") or fm.get("id") or path.stem),
                description=str(fm.get("description") or ""),
                path=Path(path),
            )
        )
    out.sort(key=lambda c: c.id)
    return out


def get_recipe(cfg: Config, recipe_id: str) -> tuple[dict[str, Any], str, Path] | None:
    """Return (frontmatter, body, path) or None if not found / unparseable."""
    _ensure_scripts_on_path(cfg)
    from scripts import recipe_manager as rm  # type: ignore

    path = cfg.recipes_dir / f"{recipe_id}.md"
    if not path.exists():
        return None
    try:
        fm, body = rm.parse_recipe(path)
    except Exception:
        return None
    if not isinstance(fm, dict):
        return None
    return fm, body, path


def get_connector(cfg: Config, connector_id: str) -> tuple[dict[str, Any], str, Path] | None:
    _ensure_scripts_on_path(cfg)
    from scripts import connector_manager as cm  # type: ignore

    path = cfg.connectors_dir / f"{connector_id}.md"
    if not path.exists():
        return None
    try:
        fm, body = cm.parse_connector(path)
    except Exception:
        return None
    if not isinstance(fm, dict):
        return None
    return fm, body, path
