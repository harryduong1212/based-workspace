"""Tier 2 — containerised infrastructure (Postgres, n8n, Qdrant, llama-swap).

Each catalog entry maps a "feature" to a compose service: the handler runs
`podman compose -f <file> [--profile <p>] up/down <service>` and probes a
configured health endpoint to decide if it counts as INSTALLED.

Status mapping
--------------
- INSTALLED    — container running AND health check passes
- PARTIAL      — container running, health check failing
- ERROR        — container exists but in a non-running state (exited, etc.)
- AVAILABLE    — container does not exist (image may or may not be pulled)
- UNAVAILABLE  — compose file missing on disk

Test seam
---------
The handler accepts a `runner` callable so unit tests can substitute a fake
that returns canned (stdout, returncode) tuples and short-circuits HTTP.
Default runner shells out to `podman` / `urllib.request`.
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from .base import Feature, FeatureKind, FeatureStatus, load_catalog


# (command_argv) → (stdout, returncode)
CommandRunner = Callable[[list[str]], tuple[str, int]]

# (url, timeout_s) → http_status_int (or 0 on connection error)
HealthProber = Callable[[str, float], int]


def _default_command_runner(argv: list[str]) -> tuple[str, int]:
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=30, check=False)
        return (result.stdout or "") + (result.stderr or ""), result.returncode
    except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError) as e:
        return f"{type(e).__name__}: {e}", -1


def _default_http_prober(url: str, timeout_s: float = 5.0) -> int:
    try:
        with urllib.request.urlopen(url, timeout=timeout_s) as resp:  # noqa: S310 — internal URL
            return int(resp.status)
    except urllib.error.HTTPError as e:
        return int(e.code)
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return 0


def _expand_env(s: str) -> str:
    return os.path.expandvars(s)


class ContainerFeatureHandler:
    """Handler for kind=container (Tier 2 podman-compose services)."""

    kind = FeatureKind.CONTAINER

    def __init__(
        self,
        workspace_root: Path,
        catalog_path: Path | None = None,
        runner: CommandRunner | None = None,
        http_prober: HealthProber | None = None,
    ):
        self._root = workspace_root
        self._catalog_path = catalog_path
        self._run = runner or _default_command_runner
        self._probe = http_prober or _default_http_prober

    # ---- catalog access ------------------------------------------------

    def _declarations(self) -> dict[str, dict[str, Any]]:
        catalog = load_catalog(self._catalog_path)
        return catalog.get(FeatureKind.CONTAINER.value, {})

    # ---- detection -----------------------------------------------------

    def _inspect_container(self, name: str) -> dict[str, Any] | None:
        """Return parsed `podman inspect` for one container, or None if absent."""
        out, rc = self._run(["podman", "inspect", "--type=container", name])
        if rc != 0:
            return None
        try:
            data = json.loads(out)
        except json.JSONDecodeError:
            return None
        if isinstance(data, list) and data:
            return data[0]
        return None

    def _check_health(self, decl: dict[str, Any], container_name: str) -> tuple[bool, str]:
        """Return (healthy, reason). Reason is "" on success."""
        health = decl.get("health") or {}
        htype = health.get("type")
        if htype == "http":
            url = health.get("url") or ""
            status = self._probe(url, 5.0)
            if 200 <= status < 300:
                return True, ""
            return False, f"GET {url} returned {status}"
        if htype == "exec":
            argv = ["podman", "exec", container_name] + [_expand_env(a) for a in (health.get("command") or [])]
            _out, rc = self._run(argv)
            if rc == 0:
                return True, ""
            return False, f"exec returned {rc}"
        # No health declared → consider running == healthy.
        return True, ""

    def _build(self, feature_id: str, decl: dict[str, Any]) -> Feature:
        compose_file = decl.get("compose_file") or ""
        compose_path = (self._root / compose_file) if compose_file else None
        container_name = decl.get("container_name") or decl.get("compose_service") or feature_id

        detail: dict[str, Any] = {
            "compose_file": compose_file,
            "compose_service": decl.get("compose_service"),
            "container_name": container_name,
            "profile": decl.get("profile"),
            "health": dict(decl.get("health") or {}),
        }

        if compose_path is not None and not compose_path.exists():
            return Feature(
                id=feature_id,
                kind=FeatureKind.CONTAINER,
                name=decl.get("name") or feature_id,
                description=decl.get("description") or "",
                status=FeatureStatus.UNAVAILABLE,
                requires=list(decl.get("requires") or []),
                detail={**detail, "error": f"compose file not found: {compose_path}"},
            )

        inspected = self._inspect_container(container_name)
        if inspected is None:
            status = FeatureStatus.AVAILABLE
        else:
            state = (inspected.get("State") or {})
            is_running = bool(state.get("Running"))
            if not is_running:
                status = FeatureStatus.ERROR
                detail["state"] = state.get("Status", "unknown")
            else:
                healthy, reason = self._check_health(decl, container_name)
                status = FeatureStatus.INSTALLED if healthy else FeatureStatus.PARTIAL
                if not healthy:
                    detail["health_error"] = reason

        return Feature(
            id=feature_id,
            kind=FeatureKind.CONTAINER,
            name=decl.get("name") or feature_id,
            description=decl.get("description") or "",
            status=status,
            requires=list(decl.get("requires") or []),
            detail=detail,
        )

    # ---- handler protocol ----------------------------------------------

    def list(self) -> list[Feature]:
        return [self._build(fid, decl) for fid, decl in self._declarations().items()]

    def get(self, feature_id: str) -> Feature | None:
        decl = self._declarations().get(feature_id)
        if decl is None:
            return None
        return self._build(feature_id, decl)

    def _compose_argv(self, decl: dict[str, Any], action: list[str]) -> list[str]:
        argv = ["podman", "compose", "-f", str(self._root / decl["compose_file"])]
        if decl.get("profile"):
            argv += ["--profile", decl["profile"]]
        argv += action
        argv.append(decl["compose_service"])
        return argv

    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
    ) -> dict[str, Any]:
        """Bring the service up via `podman compose up -d`."""
        del inputs  # T2 has no per-install user inputs
        log = log_sink or (lambda _s: None)
        decl = self._declarations().get(feature_id)
        if decl is None:
            return {"ok": False, "error": f"unknown container feature {feature_id!r}"}

        feature = self._build(feature_id, decl)
        if feature.status == FeatureStatus.UNAVAILABLE:
            log(f"compose file missing: {feature.detail.get('error')}")
            return {"ok": False, "error": feature.detail.get("error"), "feature": feature.to_dict()}
        if feature.status == FeatureStatus.INSTALLED:
            log("already running and healthy; no-op")
            return {"ok": True, "noop": True, "feature": feature.to_dict()}

        argv = self._compose_argv(decl, ["up", "-d"])
        log(f"$ {' '.join(argv)}")
        out, rc = self._run(argv)
        # Tee subprocess output to the sink so the user can read pull progress
        # or compose errors live in the dialog.
        for line in (out or "").rstrip().splitlines():
            log(line)
        log(f"exit code: {rc}")
        if rc != 0:
            return {
                "ok": False,
                "error": f"`podman compose up` exited {rc}",
                "stdout": out[-2000:],
                "feature": feature.to_dict(),
            }
        return {
            "ok": True,
            "command": " ".join(argv),
            "feature": self._build(feature_id, decl).to_dict(),
        }

    def uninstall(self, feature_id: str) -> dict[str, Any]:
        """Stop + remove the container. Volumes preserved (data safety)."""
        decl = self._declarations().get(feature_id)
        if decl is None:
            return {"ok": False, "error": f"unknown container feature {feature_id!r}"}

        feature = self._build(feature_id, decl)
        if feature.status == FeatureStatus.AVAILABLE:
            return {"ok": True, "noop": True, "feature": feature.to_dict()}

        argv = self._compose_argv(decl, ["down"])
        # `down` with a service arg isn't supported by all versions; use stop + rm.
        stop_argv = ["podman", "compose", "-f", str(self._root / decl["compose_file"])]
        if decl.get("profile"):
            stop_argv += ["--profile", decl["profile"]]
        stop_argv += ["stop", decl["compose_service"]]
        rm_argv = stop_argv[:-2] + ["rm", "-f", decl["compose_service"]]

        out1, rc1 = self._run(stop_argv)
        if rc1 != 0:
            return {"ok": False, "error": f"stop exited {rc1}", "stdout": out1[-2000:]}
        out2, rc2 = self._run(rm_argv)
        if rc2 != 0:
            return {"ok": False, "error": f"rm exited {rc2}", "stdout": out2[-2000:]}

        del argv  # the down argv was constructed for documentation only
        return {"ok": True, "feature": self._build(feature_id, decl).to_dict()}

    def verify(self, feature_id: str) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown container feature {feature_id!r}"}
        return {"ok": feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict()}

    def _read_compose_service(self, decl: dict[str, Any]) -> dict[str, Any] | None:
        """Best-effort YAML parse of `services.<compose_service>`. None on failure
        — preview falls back to showing the command without details in that case."""
        import yaml

        compose_path = self._root / decl["compose_file"]
        try:
            doc = yaml.safe_load(compose_path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            return None
        services = (doc.get("services") or {}) if isinstance(doc, dict) else {}
        svc = services.get(decl["compose_service"])
        return svc if isinstance(svc, dict) else None

    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        del inputs
        decl = self._declarations().get(feature_id)
        if decl is None:
            return {"ok": False, "error": f"unknown container feature {feature_id!r}"}
        feature = self._build(feature_id, decl)

        if feature.status == FeatureStatus.UNAVAILABLE:
            return {
                "ok": False,
                "error": feature.detail.get("error"),
                "feature": feature.to_dict(),
            }

        argv = self._compose_argv(decl, ["up", "-d"])
        side_effects: list[dict[str, Any]] = [{
            "kind": "run_command",
            "summary": "Run compose up",
            "detail": " ".join(argv),
        }]
        warnings: list[str] = []

        svc = self._read_compose_service(decl)
        if svc is not None:
            image = svc.get("image")
            if image:
                side_effects.append({
                    "kind": "container_image",
                    "summary": "Pull image if not already present",
                    "detail": str(image),
                })
            for port in (svc.get("ports") or []):
                side_effects.append({
                    "kind": "port_bind",
                    "summary": "Bind host port",
                    "detail": str(port),
                })
            for vol in (svc.get("volumes") or []):
                side_effects.append({
                    "kind": "volume_use",
                    "summary": "Mount volume",
                    "detail": str(vol),
                })

        if decl.get("profile"):
            warnings.append(
                f"Service runs under compose profile '{decl['profile']}' — start passes --profile."
            )
        if feature.status == FeatureStatus.INSTALLED:
            warnings.append("Already running and healthy — install will be a no-op.")
        elif feature.status == FeatureStatus.ERROR:
            warnings.append(
                f"Container exists but is in state '{feature.detail.get('state', 'unknown')}'. "
                "Install will attempt to bring it back up."
            )

        return {
            "ok": True,
            "feature": feature.to_dict(),
            "would_be_noop": feature.status == FeatureStatus.INSTALLED,
            "side_effects": side_effects,
            "warnings": warnings,
        }
