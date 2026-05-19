"""Read-only loaders for recipes and connectors.

Wraps the existing scripts.recipe_manager / scripts.connector_manager helpers
so the FastAPI routes don't depend on argparse-shaped CLI internals. Pure
stdlib + PyYAML — no FastAPI imports here.
"""
from __future__ import annotations

import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, TypeVar

from .config import Config


def _ensure_scripts_on_path(cfg: Config) -> None:
    scripts_path = str(cfg.workspace_root)
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)


# --------------------------------------------------------------------------
# Stat-signature cache.
#
# `load_recipes` / `load_connectors` are hit on every Control Panel request
# and re-parsed every `*.md` each time. A real inotify watcher would mean a
# background thread + an extra dep; a directory *signature* — the sorted
# (name, mtime_ns, size) of every `*.md` — gets the same invalidation
# correctness from one `stat()` per file (no read, no YAML parse) and stays
# stdlib-only. The expensive parse only re-runs when a file is added,
# removed, or its content changes (mtime/size both move on a real edit).
# --------------------------------------------------------------------------

_T = TypeVar("_T")
_cache_lock = threading.Lock()
# key -> (signature, built list). One entry per (kind, dir).
_cache: dict[str, tuple[tuple, list]] = {}


def _dir_signature(directory: Path) -> tuple:
    if not directory.exists():
        return ()
    sig = []
    for p in sorted(directory.glob("*.md")):
        try:
            st = p.stat()
        except OSError:
            continue  # racing deletion — treat as absent
        sig.append((p.name, st.st_mtime_ns, st.st_size))
    return tuple(sig)


def _cached(key: str, directory: Path, builder: Callable[[], list[_T]]) -> list[_T]:
    """Return `builder()`'s result, reused while `directory`'s `*.md` set +
    mtimes + sizes are unchanged. The cached list holds frozen dataclasses
    and is never mutated by callers, so it's safe to hand out as-is."""
    sig = _dir_signature(directory)
    with _cache_lock:
        hit = _cache.get(key)
        if hit is not None and hit[0] == sig:
            return hit[1]
    built = builder()  # parse outside the lock — it can be slow
    with _cache_lock:
        _cache[key] = (sig, built)
    return built


def clear_cache() -> None:
    """Drop all cached parses. Test seam; also safe to call after a known
    out-of-band mutation if a caller ever wants to force a re-parse."""
    with _cache_lock:
        _cache.clear()


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

    def _build() -> list[RecipeSummary]:
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

    return _cached(f"recipes:{cfg.recipes_dir}", cfg.recipes_dir, _build)


def load_connectors(cfg: Config) -> list[ConnectorSummary]:
    _ensure_scripts_on_path(cfg)

    def _build() -> list[ConnectorSummary]:
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

    return _cached(f"connectors:{cfg.connectors_dir}", cfg.connectors_dir, _build)


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
