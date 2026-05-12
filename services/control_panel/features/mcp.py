"""Tier 3 — MCP server features.

The catalog of *available* MCP servers is `.mcp.json.example` (tracked
template). The *installed* set is `.mcp.json` (gitignored, user-local).

Install action copies the example entry into `.mcp.json` (creating the file
if needed), then runs a spawn-and-`list_tools` smoke via the existing
`agent_tools.ToolRuntime`. Uninstall removes the entry. Status:

- INSTALLED   — entry present in .mcp.json AND spawn-test succeeds
- PARTIAL     — entry present but spawn-test fails (config wrong / binary missing)
- AVAILABLE   — entry only present in .mcp.json.example
- UNAVAILABLE — example template missing entirely
"""
from __future__ import annotations

import json
from contextlib import AsyncExitStack  # re-exported for type hints in tests
from pathlib import Path
from typing import Any, Callable

from .base import Feature, FeatureKind, FeatureStatus


# A SpawnProbe takes (server_id, config) and returns (ok, error_message).
SpawnProbe = Callable[[str, dict[str, Any]], tuple[bool, str]]


def _default_spawn_probe(server_id: str, config: dict[str, Any]) -> tuple[bool, str]:
    """Try to spawn the MCP server and call list_tools. Returns (ok, error).

    Delegates to ToolRuntime so this stays consistent with the agent path.
    """
    try:
        from services.recipe_runtime.agent_tools import build_tool_runtime
    except ImportError as e:
        return False, f"agent_tools unavailable: {e}"

    # Build a synthetic fm declaring just this one MCP server. We need an
    # ad-hoc .mcp.json so ToolRuntime resolves the config. Use a temp dir.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / ".mcp.json").write_text(
            json.dumps({"mcpServers": {server_id: config}}), encoding="utf-8"
        )
        try:
            with build_tool_runtime({"requires_mcp": [server_id]}, workspace_root=str(tmp_path)) as rt:
                # Did any tool from this server make it into the catalog?
                has_tool = any(d["name"].startswith(f"{server_id}__") for d in rt.definitions)
                if not has_tool:
                    return False, "spawn succeeded but reported zero tools"
        except Exception as e:  # noqa: BLE001 — surface to UI
            return False, f"{type(e).__name__}: {e}"
    return True, ""


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


class MCPFeatureHandler:
    """Handler for kind=mcp (Tier 3)."""

    kind = FeatureKind.MCP

    def __init__(
        self,
        workspace_root: Path,
        spawn_probe: SpawnProbe | None = None,
    ):
        self._root = workspace_root
        self._probe = spawn_probe or _default_spawn_probe

    @property
    def _example_path(self) -> Path:
        return self._root / ".mcp.json.example"

    @property
    def _installed_path(self) -> Path:
        return self._root / ".mcp.json"

    # ---- catalog ------------------------------------------------------

    def _example_servers(self) -> dict[str, dict[str, Any]]:
        doc = _load_json(self._example_path)
        return dict(doc.get("mcpServers") or {})

    def _installed_servers(self) -> dict[str, dict[str, Any]]:
        doc = _load_json(self._installed_path)
        return dict(doc.get("mcpServers") or {})

    # ---- detection ---------------------------------------------------

    def _build(self, server_id: str, example: dict[str, Any] | None, installed: dict[str, Any] | None) -> Feature:
        config = installed or example or {}
        detail: dict[str, Any] = {
            "command": config.get("command"),
            "args": list(config.get("args") or []),
            "cwd": config.get("cwd"),
            "in_example": example is not None,
            "in_installed": installed is not None,
        }
        if installed is None:
            status = FeatureStatus.AVAILABLE
        else:
            ok, err = self._probe(server_id, installed)
            if ok:
                status = FeatureStatus.INSTALLED
            else:
                status = FeatureStatus.PARTIAL
                detail["probe_error"] = err
        return Feature(
            id=server_id,
            kind=FeatureKind.MCP,
            name=server_id,
            description=(example or installed or {}).get("_description")
            or f"MCP server {server_id}",
            status=status,
            requires=[],  # MCP-level requires (e.g. on Qdrant) live in a future enhancement
            detail=detail,
        )

    # ---- handler protocol --------------------------------------------

    def list(self) -> list[Feature]:
        example = self._example_servers()
        installed = self._installed_servers()
        ids = sorted(set(example.keys()) | set(installed.keys()))
        return [self._build(i, example.get(i), installed.get(i)) for i in ids]

    def get(self, feature_id: str) -> Feature | None:
        example = self._example_servers().get(feature_id)
        installed = self._installed_servers().get(feature_id)
        if example is None and installed is None:
            return None
        return self._build(feature_id, example, installed)

    # ---- install / uninstall -----------------------------------------

    def _write_installed(self, doc: dict[str, Any]) -> None:
        # Preserve formatting cues — trailing newline, sorted keys mirror example.
        self._installed_path.write_text(
            json.dumps(doc, indent=2) + "\n", encoding="utf-8"
        )

    def install(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        """Copy example entry → .mcp.json (or override via inputs.config)."""
        example = self._example_servers().get(feature_id)
        if example is None and (not inputs or not inputs.get("config")):
            return {
                "ok": False,
                "error": f"no example entry for MCP {feature_id!r}; pass inputs.config to install custom",
            }

        config: dict[str, Any]
        if inputs and isinstance(inputs.get("config"), dict):
            config = inputs["config"]
        else:
            assert example is not None
            config = dict(example)

        # Resolve relative cwd against workspace_root for stability — the user's
        # shell may not be in this dir when the server is spawned.
        if config.get("cwd") in (None, "", "."):
            config["cwd"] = str(self._root.resolve())

        doc = _load_json(self._installed_path) or {}
        servers = dict(doc.get("mcpServers") or {})
        servers[feature_id] = config
        doc["mcpServers"] = servers
        self._write_installed(doc)

        feature = self.get(feature_id)
        return {"ok": feature is not None and feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict() if feature else None}

    def uninstall(self, feature_id: str) -> dict[str, Any]:
        doc = _load_json(self._installed_path)
        servers = dict(doc.get("mcpServers") or {})
        if feature_id not in servers:
            feature = self.get(feature_id)
            return {"ok": True, "noop": True, "feature": feature.to_dict() if feature else None}
        servers.pop(feature_id)
        if servers:
            doc["mcpServers"] = servers
            self._write_installed(doc)
        else:
            # Keep the file but with an empty mcpServers — easier for `cat` debugging.
            doc["mcpServers"] = {}
            self._write_installed(doc)
        feature = self.get(feature_id)
        return {"ok": True, "feature": feature.to_dict() if feature else None}

    def verify(self, feature_id: str) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown MCP feature {feature_id!r}"}
        return {"ok": feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict()}


__all__ = ["MCPFeatureHandler", "SpawnProbe", "AsyncExitStack"]
