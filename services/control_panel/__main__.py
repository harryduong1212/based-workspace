"""Entrypoint: `python -m services.control_panel`.

Reads host/port from CONTROL_PANEL_HOST / CONTROL_PANEL_PORT (defaults
127.0.0.1:8765). Set CONTROL_PANEL_HOST=0.0.0.0 inside Docker.
"""
from __future__ import annotations

import sys

import uvicorn

from .app import create_app
from .config import Config


def main(argv: list[str] | None = None) -> int:
    del argv
    cfg = Config.from_env()
    app = create_app(cfg)
    print(f"control panel — workspace: {cfg.workspace_root}")
    print(f"control panel — listening on http://{cfg.host}:{cfg.port}")
    uvicorn.run(app, host=cfg.host, port=cfg.port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
