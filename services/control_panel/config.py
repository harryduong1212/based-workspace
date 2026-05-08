"""Runtime configuration — env-driven, cross-platform paths.

Stdlib-only so this module imports cleanly even without the FastAPI deps.
Used by the app factory and the entrypoint to resolve workspace paths,
host/port binding, and feature flags.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _detect_workspace_root() -> Path:
    """Walk upward from this file until we find the repo root.

    Markers we trust: a `.git/` dir, or both `recipes/` and `services/`.
    Falls back to env override or three-levels-up.
    """
    override = os.environ.get("WORKSPACE_ROOT")
    if override:
        return Path(override).resolve()

    here = Path(__file__).resolve()
    for ancestor in [here.parent, *here.parents]:
        if (ancestor / ".git").exists():
            return ancestor
        if (ancestor / "recipes").is_dir() and (ancestor / "services").is_dir():
            return ancestor
    return here.parents[2]


@dataclass(frozen=True)
class Config:
    workspace_root: Path
    recipes_dir: Path
    connectors_dir: Path
    services_dir: Path

    host: str
    port: int
    reload: bool

    llama_swap_url: str

    @classmethod
    def from_env(cls) -> "Config":
        root = _detect_workspace_root()
        return cls(
            workspace_root=root,
            recipes_dir=root / "recipes",
            connectors_dir=root / "connectors",
            services_dir=root / "services",
            host=os.environ.get("CONTROL_PANEL_HOST", "127.0.0.1"),
            port=int(os.environ.get("CONTROL_PANEL_PORT", "8765")),
            reload=os.environ.get("CONTROL_PANEL_RELOAD", "0") == "1",
            llama_swap_url=(
                os.environ.get("LLAMA_SWAP_URL")
                or os.environ.get("OPENAI_API_BASE")
                or "http://localhost:11434/v1"
            ).rstrip("/"),
        )
