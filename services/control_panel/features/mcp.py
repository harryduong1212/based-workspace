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

    def _build(
        self,
        server_id: str,
        example: dict[str, Any] | None,
        installed: dict[str, Any] | None,
        *,
        probe: bool = True,
    ) -> Feature:
        """Build a Feature. `probe=False` skips the (expensive) spawn smoke
        and reports configured presence only — used by `list()` so loading
        the page doesn't fork an MCP server per installed entry."""
        config = installed or example or {}
        # Underscore-prefixed keys are UI metadata, not MCP server config —
        # they describe the server for the Features page and never reach the
        # spawned process (install() strips them before writing .mcp.json).
        meta = example or installed or {}
        docs = meta.get("_docs")
        requires = [str(r) for r in (meta.get("_requires") or [])]
        detail: dict[str, Any] = {
            "command": config.get("command"),
            "args": list(config.get("args") or []),
            "cwd": config.get("cwd"),
            "in_example": example is not None,
            "in_installed": installed is not None,
            "probed": probe,
            "docs": docs,
            "requires_services": requires,
        }
        if installed is None:
            status = FeatureStatus.AVAILABLE
        elif not probe:
            # Configured-only signal: treat as installed (the user explicitly added it);
            # if config is broken, /verify on the detail page surfaces it.
            status = FeatureStatus.INSTALLED
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
            description=meta.get("_description") or f"MCP server {server_id}",
            status=status,
            # `_requires` (e.g. memory → qdrant + llama-swap) feeds the dep
            # graph so the install dialog blocks + explains instead of letting
            # the spawn-probe fail cryptically.
            requires=requires,
            detail=detail,
            about=(meta.get("_about") or "").strip(),
        )

    # ---- handler protocol --------------------------------------------

    def list(self) -> list[Feature]:
        """Fast listing — no spawn-probes. Status is "configured present" only;
        the detail page (`get`) and `verify` action do the real smoke."""
        example = self._example_servers()
        installed = self._installed_servers()
        ids = sorted(set(example.keys()) | set(installed.keys()))
        return [self._build(i, example.get(i), installed.get(i), probe=False) for i in ids]

    def get(self, feature_id: str) -> Feature | None:
        """Full status — runs spawn-probe if installed. Slow but accurate."""
        example = self._example_servers().get(feature_id)
        installed = self._installed_servers().get(feature_id)
        if example is None and installed is None:
            return None
        return self._build(feature_id, example, installed, probe=True)

    # ---- install / uninstall -----------------------------------------

    def _write_installed(self, doc: dict[str, Any]) -> None:
        # Preserve formatting cues — trailing newline, sorted keys mirror example.
        self._installed_path.write_text(
            json.dumps(doc, indent=2) + "\n", encoding="utf-8"
        )

    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
    ) -> dict[str, Any]:
        """Copy example entry → .mcp.json (or override via inputs.config)."""
        log = log_sink or (lambda _s: None)
        example = self._example_servers().get(feature_id)
        if example is None and (not inputs or not inputs.get("config")):
            return {
                "ok": False,
                "error": f"no example entry for MCP {feature_id!r}; pass inputs.config to install custom",
            }

        config: dict[str, Any]
        if inputs and isinstance(inputs.get("config"), dict):
            log("using custom config from inputs.config")
            config = inputs["config"]
        else:
            assert example is not None
            log(f"using example entry from .mcp.json.example")
            config = dict(example)

        # Drop UI-only metadata (_description/_docs/_requires) — it must not
        # land in .mcp.json or reach the spawned server's config.
        stripped = sorted(k for k in config if k.startswith("_"))
        config = {k: v for k, v in config.items() if not k.startswith("_")}
        if stripped:
            log(f"stripped UI metadata keys: {', '.join(stripped)}")

        # Resolve relative cwd against workspace_root for stability — the user's
        # shell may not be in this dir when the server is spawned.
        if config.get("cwd") in (None, "", "."):
            config["cwd"] = str(self._root.resolve())

        log(f"writing mcpServers.{feature_id} to .mcp.json")
        doc = _load_json(self._installed_path) or {}
        servers = dict(doc.get("mcpServers") or {})
        servers[feature_id] = config
        doc["mcpServers"] = servers
        self._write_installed(doc)

        log("running spawn-test (list_tools)...")
        feature = self.get(feature_id)
        ok = feature is not None and feature.status == FeatureStatus.INSTALLED
        if ok:
            log("spawn-test ok")
        elif feature is not None:
            log(f"spawn-test failed: {feature.detail.get('probe_error', '?')}")
        return {"ok": ok, "feature": feature.to_dict() if feature else None}

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

    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        example = self._example_servers().get(feature_id)
        installed = self._installed_servers().get(feature_id)
        if example is None and installed is None and not (inputs and inputs.get("config")):
            return {"ok": False, "error": f"no example or installed entry for {feature_id!r}"}

        if inputs and isinstance(inputs.get("config"), dict):
            config = inputs["config"]
        else:
            config = dict(installed or example or {})

        # Probe-free Feature snapshot — preview must be fast and side-effect free.
        feature = self._build(feature_id, example, installed, probe=False)

        cmd = config.get("command") or "?"
        args = list(config.get("args") or [])
        env_keys = sorted((config.get("env") or {}).keys()) if isinstance(config.get("env"), dict) else []
        spawn_line = " ".join([str(cmd), *[str(a) for a in args]])

        side_effects: list[dict[str, Any]] = [{
            "kind": "config_write",
            "summary": "Write entry into .mcp.json",
            "detail": f"mcpServers.{feature_id}",
        }, {
            "kind": "mcp_spawn",
            "summary": "Spawn-test the server (list_tools)",
            "detail": spawn_line,
        }]
        if env_keys:
            side_effects.append({
                "kind": "env_read",
                "summary": "Read env vars at spawn time (keys only)",
                "detail": ", ".join(env_keys),
            })

        warnings: list[str] = []
        if installed is not None and example is None:
            warnings.append("Already installed and no example template — install will refresh from .mcp.json.")
        if feature.status == FeatureStatus.INSTALLED:
            warnings.append("Already configured — install will overwrite the entry and re-run the spawn-test.")

        return {
            "ok": True,
            "feature": feature.to_dict(),
            "would_be_noop": False,  # mcp install always rewrites + reprobes
            "side_effects": side_effects,
            "warnings": warnings,
        }


__all__ = ["MCPFeatureHandler", "SpawnProbe", "AsyncExitStack"]
