"""Entrypoint: `python -m services.control_panel`.

Reads host/port from CONTROL_PANEL_HOST / CONTROL_PANEL_PORT (defaults
127.0.0.1:8765). Set CONTROL_PANEL_HOST=0.0.0.0 inside Docker.

Auto-loads `<workspace>/.env` into `os.environ` so connector probes,
provider dispatch, and any other os.environ readers work whether or
not the user has sourced `.env` in their shell. Existing process env
wins — we never overwrite a pre-set var.
"""
from __future__ import annotations

import os
import sys

import uvicorn

from .app import create_app
from .config import Config
from .env_writer import read_env_values


def _load_dotenv(workspace_root) -> int:
    env_path = workspace_root / ".env"
    if not env_path.exists():
        return 0
    loaded = 0
    for key, value in read_env_values(env_path).items():
        if key not in os.environ:
            os.environ[key] = value
            loaded += 1
    return loaded


def main(argv: list[str] | None = None) -> int:
    del argv
    cfg = Config.from_env()
    loaded = _load_dotenv(cfg.workspace_root)
    app = create_app(cfg)
    print(f"control panel — workspace: {cfg.workspace_root}")
    print(f"control panel — loaded {loaded} var(s) from .env")
    print(f"control panel — listening on http://{cfg.host}:{cfg.port}")
    uvicorn.run(app, host=cfg.host, port=cfg.port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
