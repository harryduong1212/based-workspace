"""System health probes — best-effort, fast, never raises to the caller."""
from __future__ import annotations

import os
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass

from .config import Config


@dataclass(frozen=True)
class HealthStatus:
    name: str
    ok: bool
    detail: str


def check_llama_swap(cfg: Config, timeout: float = 1.5) -> HealthStatus:
    url = cfg.llama_swap_url + "/models"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return HealthStatus("llama-swap", True, f"reachable at {cfg.llama_swap_url} (HTTP {resp.status})")
    except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout, OSError) as e:
        return HealthStatus("llama-swap", False, f"unreachable: {e}")


def check_postgres(timeout: float = 1.5) -> HealthStatus:
    """TCP-connect probe only — avoids requiring psycopg here."""
    host = os.environ.get("POSTGRES_HOST", "localhost")
    try:
        port = int(os.environ.get("POSTGRES_PORT", "5432"))
    except ValueError:
        return HealthStatus("postgres", False, "POSTGRES_PORT not numeric")
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return HealthStatus("postgres", True, f"reachable at {host}:{port}")
    except (OSError, socket.timeout) as e:
        return HealthStatus("postgres", False, f"unreachable at {host}:{port}: {e}")


def all_checks(cfg: Config) -> list[HealthStatus]:
    return [check_llama_swap(cfg), check_postgres()]
