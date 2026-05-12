"""Tier 1 — system runtime features (Podman, Python, Node, Git, git-hooks).

Detect-only. Install action does NOT run anything privileged — it returns
the catalog's install_hint for the detected distro so the user can copy /
paste manually. Uninstall is a no-op for safety (we don't yank host
binaries out from under the user). Verify just re-runs detect.

Status mapping
--------------
- INSTALLED  — binary present AND (no min_version OR detected ≥ min)
- PARTIAL    — binary present but version below min_version
- AVAILABLE  — binary absent
- UNKNOWN    — detection threw (rare; surfaces in the UI as actionable)
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .base import Feature, FeatureKind, FeatureStatus, load_catalog


_VERSION_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")
_DETECT_TIMEOUT_S = 5


def _parse_version(text: str) -> tuple[int, int, int] | None:
    m = _VERSION_RE.search(text or "")
    if m is None:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))


def _detect_distro(os_release_path: Path | None = None) -> str:
    """Return one of {"fedora", "debian", "arch", "unknown"} from /etc/os-release."""
    path = os_release_path or Path("/etc/os-release")
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return "unknown"
    for line in text.splitlines():
        if line.startswith("ID="):
            val = line[3:].strip().strip('"').strip("'").lower()
            if val in ("fedora", "rhel", "centos", "rocky", "almalinux"):
                return "fedora"
            if val in ("debian", "ubuntu", "linuxmint", "pop"):
                return "debian"
            if val in ("arch", "manjaro", "endeavouros"):
                return "arch"
            return val
    return "unknown"


def _detect_one(decl: dict[str, Any]) -> tuple[FeatureStatus, dict[str, Any]]:
    """Return (status, detail) for a single system feature.

    `detail` always carries `binary`, `min_version`, the `install_hint` dict
    for the detected distro, and (when found) `version`. Detection failure
    surfaces as status=UNKNOWN with `error` in detail.
    """
    detect = decl.get("detect") or {}
    cmd = detect.get("command")
    detail: dict[str, Any] = {
        "binary": cmd,
        "min_version": detect.get("min_version"),
        "install_hint": dict(decl.get("install_hint") or {}),
    }
    if not cmd:
        return FeatureStatus.UNKNOWN, {**detail, "error": "no detect.command in catalog"}

    found_path = shutil.which(cmd)
    if found_path is None:
        return FeatureStatus.AVAILABLE, detail
    detail["binary_path"] = found_path

    version_flag = detect.get("version_flag")
    if not version_flag:
        return FeatureStatus.INSTALLED, detail

    try:
        result = subprocess.run(
            [cmd, version_flag],
            capture_output=True,
            text=True,
            timeout=_DETECT_TIMEOUT_S,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError) as e:
        return FeatureStatus.UNKNOWN, {**detail, "error": f"{type(e).__name__}: {e}"}

    # Some tools (e.g. node) print to stdout; others (e.g. git) too; gitleaks
    # prints to stdout for `version` subcommand. Combine both streams.
    version_text = (result.stdout or "") + (result.stderr or "")
    parsed = _parse_version(version_text)
    if parsed is None:
        # Found the binary, couldn't parse version — treat as INSTALLED rather
        # than fail. The min_version gate is a soft warning, not a blocker.
        return FeatureStatus.INSTALLED, {**detail, "version_raw": version_text.strip()[:200]}

    detail["version"] = ".".join(str(n) for n in parsed)

    min_v = detect.get("min_version")
    if min_v:
        min_parsed = _parse_version(min_v)
        if min_parsed is not None and parsed < min_parsed:
            return FeatureStatus.PARTIAL, detail
    return FeatureStatus.INSTALLED, detail


class SystemFeatureHandler:
    """Handler for kind=system (Tier 1 host binaries)."""

    kind = FeatureKind.SYSTEM

    def __init__(self, catalog_path: Path | None = None, distro: str | None = None):
        self._catalog_path = catalog_path
        self._distro = distro or _detect_distro()

    # ---- catalog access -------------------------------------------------

    def _declarations(self) -> dict[str, dict[str, Any]]:
        catalog = load_catalog(self._catalog_path)
        return catalog.get(FeatureKind.SYSTEM.value, {})

    def _build(self, feature_id: str, decl: dict[str, Any]) -> Feature:
        status, detail = _detect_one(decl)
        detail["distro"] = self._distro
        detail["install_command"] = detail.get("install_hint", {}).get(self._distro) or detail.get(
            "install_hint", {}
        ).get("fedora")
        return Feature(
            id=feature_id,
            kind=FeatureKind.SYSTEM,
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

    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
    ) -> dict[str, Any]:
        """Print-only — never sudo. Returns the command the user should run."""
        del inputs  # T1 has no per-install user inputs
        log = log_sink or (lambda _s: None)
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown system feature {feature_id!r}"}
        if feature.status == FeatureStatus.INSTALLED:
            log(f"already installed (version {feature.detail.get('version', '?')}); no-op")
            return {"ok": True, "noop": True, "feature": feature.to_dict()}
        cmd = feature.detail.get("install_command")
        if not cmd:
            log(f"no install hint for distro {self._distro!r}")
            return {
                "ok": False,
                "error": f"no install hint for distro {self._distro!r}; install {feature.name} manually",
                "feature": feature.to_dict(),
            }
        log(f"system features are detect-only; copy the command and run it yourself:")
        log(f"  {cmd}")
        return {
            "ok": True,
            "kind": "print_command",
            "command": cmd,
            "distro": self._distro,
            "feature": feature.to_dict(),
            "message": f"Run this command, then click Verify: {cmd}",
        }

    def uninstall(self, feature_id: str) -> dict[str, Any]:
        """Refuses — we don't yank host binaries. UI should hide the button for T1."""
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown system feature {feature_id!r}"}
        return {
            "ok": False,
            "error": "system features are detect-only — uninstall via your distro package manager",
            "feature": feature.to_dict(),
        }

    def verify(self, feature_id: str) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown system feature {feature_id!r}"}
        return {
            "ok": feature.status == FeatureStatus.INSTALLED,
            "feature": feature.to_dict(),
        }

    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        del inputs
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown system feature {feature_id!r}"}

        already_installed = feature.status == FeatureStatus.INSTALLED
        side_effects: list[dict[str, Any]] = []
        warnings: list[str] = []
        cmd = feature.detail.get("install_command")

        if already_installed:
            ver = feature.detail.get("version") or "?"
            warnings.append(f"Already installed (version {ver}). Install will be a no-op.")
        elif cmd:
            side_effects.append({
                "kind": "print_command",
                "summary": f"Print install command for distro '{self._distro}'",
                "detail": cmd,
            })
            warnings.append(
                "System features are detect-only — Control Panel never runs sudo. "
                "Copy the printed command, run it yourself, then click Verify."
            )
        else:
            warnings.append(
                f"No install hint for distro '{self._distro}'. Install {feature.name} manually."
            )

        return {
            "ok": True,
            "feature": feature.to_dict(),
            "would_be_noop": already_installed,
            "side_effects": side_effects,
            "warnings": warnings,
        }
