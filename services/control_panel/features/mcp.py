"""Tier 3 — MCP server features.

The catalog of *available* MCP servers is `.mcp.json.example` (tracked
template). The *installed* set lives in one of two scopes:

- WORKSPACE: `./.mcp.json` (gitignored, project-local). Default — covers
  servers that need project-specific config (cwd, env, requires_services).
- GLOBAL: `~/.claude.json -> mcpServers` (machine-wide). Suits servers with
  no project coupling (e.g. grep_app, public-API wrappers).

Install action copies the example entry into the chosen scope's file, then
runs a spawn-and-`list_tools` smoke via the existing `agent_tools.ToolRuntime`.
Uninstall removes from a specific scope. Status semantics:

- INSTALLED   — entry present in either scope AND spawn-test succeeds
- PARTIAL     — entry present somewhere but spawn-test fails
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


# Scope identifiers as they appear over the wire (UI ↔ API) and in inputs.
SCOPE_WORKSPACE = "workspace"
SCOPE_GLOBAL = "global"
VALID_SCOPES = (SCOPE_WORKSPACE, SCOPE_GLOBAL)


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


class CorruptConfigError(Exception):
    """A config file exists but can't be parsed. Used to *refuse* a write
    rather than clobber it — matters for `~/.claude.json`, which holds
    unrelated Claude Code state (oauth, project history, feature flags)."""


def _load_json_strict(path: Path) -> dict[str, Any]:
    """Like `_load_json`, but distinguishes "absent" (-> {}, safe to create)
    from "present but unparseable" (-> raise). `_load_json` collapses both to
    {}, which is fine for files we own outright (`.mcp.json`) but catastrophic
    for a shared file: a transient parse failure would turn a merge-write into
    a full overwrite. Use this for any file we don't exclusively own."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise CorruptConfigError(f"{path}: {e}") from e
    if not isinstance(data, dict):
        raise CorruptConfigError(
            f"{path}: top-level is {type(data).__name__}, expected a JSON object"
        )
    return data


def _normalize_scope(scope: Any, default: str = SCOPE_WORKSPACE) -> str:
    """Return a canonical scope string; falls back to `default` for unknown input.

    Accepts the values UI sends (`"workspace"` / `"global"`); anything else
    becomes `default` so a malformed inputs payload doesn't write to the wrong
    file. Bad scope strings still propagate via the per-call validator below
    when strictness matters (install/uninstall require a real scope or default).
    """
    if isinstance(scope, str) and scope in VALID_SCOPES:
        return scope
    return default


class MCPFeatureHandler:
    """Handler for kind=mcp (Tier 3)."""

    kind = FeatureKind.MCP

    def __init__(
        self,
        workspace_root: Path,
        spawn_probe: SpawnProbe | None = None,
        global_config_path: Path | None = None,
        locations_config_path: Path | None = None,
    ):
        self._root = workspace_root
        self._probe = spawn_probe or _default_spawn_probe
        # `~/.claude.json` is the canonical Claude Code global config (it also
        # holds non-MCP keys like `userID`, `cachedGrowthBookFeatures`, etc.).
        # We only ever touch its `mcpServers` subtree.
        self._global_path = global_config_path or (Path.home() / ".claude.json")
        # Remembered custom install directories — so a "workspace" install can
        # target a project *other* than this one, and the UI can offer the
        # places you've used before. Pure UX memory (machine-wide, not project
        # state), so reads are lenient: a corrupt file just means "no history".
        self._locations_path = locations_config_path or (
            Path.home() / ".based-workspace" / "mcp-locations.json"
        )

    @property
    def _example_path(self) -> Path:
        return self._root / ".mcp.json.example"

    @property
    def _workspace_path(self) -> Path:
        return self._root / ".mcp.json"

    # ---- catalog ------------------------------------------------------

    def _example_servers(self) -> dict[str, dict[str, Any]]:
        doc = _load_json(self._example_path)
        return dict(doc.get("mcpServers") or {})

    def _workspace_servers(self) -> dict[str, dict[str, Any]]:
        doc = _load_json(self._workspace_path)
        return dict(doc.get("mcpServers") or {})

    def _global_servers(self) -> dict[str, dict[str, Any]]:
        doc = _load_json(self._global_path)
        return dict(doc.get("mcpServers") or {})

    # ---- custom install locations ------------------------------------

    def _read_locations(self) -> list[str]:
        """Remembered custom install dirs, newest first. Lenient on purpose —
        this is UX history, not state worth refusing a write over."""
        doc = _load_json(self._locations_path)
        items = doc.get("locations") if isinstance(doc, dict) else None
        if not isinstance(items, list):
            return []
        return [str(p) for p in items if isinstance(p, str)]

    def _remember_location(self, directory: str) -> None:
        seen = self._read_locations()
        # Move-to-front + dedupe; cap so the list stays a menu, not a log.
        ordered = [directory] + [p for p in seen if p != directory]
        ordered = ordered[:20]
        self._locations_path.parent.mkdir(parents=True, exist_ok=True)
        self._locations_path.write_text(
            json.dumps({"locations": ordered}, indent=2) + "\n", encoding="utf-8"
        )

    def _resolve_workspace_target(
        self, inputs: dict[str, Any] | None
    ) -> tuple[Path, str | None, str | None]:
        """Resolve which `.mcp.json` a workspace-scope action writes.

        Returns `(mcp_json_path, custom_dir_or_None, error_or_None)`. With no
        `inputs.path` it's this project's `.mcp.json`. With `inputs.path` it's
        `<that dir>/.mcp.json` — but only if the dir already exists; we never
        create arbitrary directories, and a bad path yields an error string
        (callers surface it instead of writing somewhere unexpected)."""
        raw = (inputs or {}).get("path")
        if not raw or not isinstance(raw, str) or not raw.strip():
            return self._workspace_path, None, None
        d = Path(raw).expanduser()
        try:
            d = d.resolve()
        except OSError as e:
            return self._workspace_path, None, f"invalid path {raw!r}: {e}"
        if not d.exists():
            return self._workspace_path, None, f"directory does not exist: {d}"
        if not d.is_dir():
            return self._workspace_path, None, f"not a directory: {d}"
        return d / ".mcp.json", str(d), None

    # ---- detection ---------------------------------------------------

    def _build(
        self,
        server_id: str,
        example: dict[str, Any] | None,
        workspace: dict[str, Any] | None,
        global_: dict[str, Any] | None,
        *,
        probe: bool = True,
    ) -> Feature:
        """Build a Feature. `probe=False` skips the (expensive) spawn smoke
        and reports configured presence only — used by `list()` so loading
        the page doesn't fork an MCP server per installed entry."""
        # Workspace wins over global for the canonical config used by the probe
        # (project-scoped is the more specific intent).
        installed = workspace or global_
        config = installed or example or {}
        # Underscore-prefixed keys are UI metadata, not MCP server config —
        # they describe the server for the Features page and never reach the
        # spawned process (install() strips them before writing).
        meta = example or workspace or global_ or {}
        docs = meta.get("_docs")
        requires = [str(r) for r in (meta.get("_requires") or [])]
        highlights = [str(h) for h in (meta.get("_highlights") or [])]
        examples = [
            {"label": str(e.get("label", "")), "code": str(e.get("code", ""))}
            for e in (meta.get("_examples") or [])
            if isinstance(e, dict)
        ]
        installed_scopes: list[str] = []
        if workspace is not None:
            installed_scopes.append(SCOPE_WORKSPACE)
        if global_ is not None:
            installed_scopes.append(SCOPE_GLOBAL)
        detail: dict[str, Any] = {
            "command": config.get("command"),
            "args": list(config.get("args") or []),
            "cwd": config.get("cwd"),
            "in_example": example is not None,
            # Back-compat for older UI/tests: "in_installed" = present anywhere.
            "in_installed": installed is not None,
            "in_workspace": workspace is not None,
            "in_global": global_ is not None,
            "installed_scopes": installed_scopes,
            # Lets the UI label the workspace pill with the real project name
            # ("based-workspace") instead of a generic word, and offer the
            # custom install dirs the user has used before.
            "workspace_dir": str(self._root.resolve()),
            "workspace_name": self._root.resolve().name,
            "known_locations": self._read_locations(),
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
            # graph so the install dialog walks prereqs deps-first instead of
            # letting the spawn-probe fail cryptically.
            requires=requires,
            detail=detail,
            about=(meta.get("_about") or "").strip(),
            highlights=highlights,
            examples=examples,
            docs=str(docs or "").strip(),
        )

    # ---- handler protocol --------------------------------------------

    def list(self) -> list[Feature]:
        """Fast listing — no spawn-probes. Status is "configured present" only;
        the detail page (`get`) and `verify` action do the real smoke."""
        example = self._example_servers()
        workspace = self._workspace_servers()
        global_ = self._global_servers()
        ids = sorted(set(example) | set(workspace) | set(global_))
        return [
            self._build(i, example.get(i), workspace.get(i), global_.get(i), probe=False)
            for i in ids
        ]

    def get(self, feature_id: str) -> Feature | None:
        """Full status — runs spawn-probe if installed. Slow but accurate."""
        example = self._example_servers().get(feature_id)
        workspace = self._workspace_servers().get(feature_id)
        global_ = self._global_servers().get(feature_id)
        if example is None and workspace is None and global_ is None:
            return None
        return self._build(feature_id, example, workspace, global_, probe=True)

    # ---- install / uninstall -----------------------------------------

    def _write_workspace(self, doc: dict[str, Any]) -> None:
        # Workspace .mcp.json is ours alone — overwrite fully.
        self._workspace_path.write_text(
            json.dumps(doc, indent=2) + "\n", encoding="utf-8"
        )

    def _write_global(self, doc: dict[str, Any]) -> None:
        """Write ~/.claude.json. Preserves all non-mcpServers keys (Claude Code
        stores unrelated state here like growth-book flags, oauth, migration
        flags) — the caller must already have merged its mcpServers update into
        the full doc."""
        self._global_path.parent.mkdir(parents=True, exist_ok=True)
        self._global_path.write_text(
            json.dumps(doc, indent=2) + "\n", encoding="utf-8"
        )

    def _strip_meta(self, config: dict[str, Any], log) -> dict[str, Any]:
        stripped = sorted(k for k in config if k.startswith("_"))
        out = {k: v for k, v in config.items() if not k.startswith("_")}
        if stripped:
            log(f"stripped UI metadata keys: {', '.join(stripped)}")
        return out

    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
    ) -> dict[str, Any]:
        """Copy example entry → the target scope's config file.

        `inputs.scope` selects "workspace" (default) or "global". Workspace
        writes `.mcp.json`; global writes `~/.claude.json.mcpServers`.
        `inputs.config` overrides the example entry entirely (used for custom
        servers without a template entry).
        """
        log = log_sink or (lambda _s: None)
        scope = _normalize_scope((inputs or {}).get("scope"))
        log(f"target scope: {scope}")

        example = self._example_servers().get(feature_id)
        if example is None and (not inputs or not inputs.get("config")):
            return {
                "ok": False,
                "error": f"no example entry for MCP {feature_id!r}; pass inputs.config to install custom",
            }

        config: dict[str, Any]
        if inputs and isinstance(inputs.get("config"), dict):
            log("using custom config from inputs.config")
            config = dict(inputs["config"])
        else:
            assert example is not None
            log("using example entry from .mcp.json.example")
            config = dict(example)

        # Drop UI-only metadata (_description/_docs/_requires) — it must not
        # land in the config file or reach the spawned server.
        config = self._strip_meta(config, log)

        # Workspace scope may target a *different* project via inputs.path.
        ws_target = self._workspace_path
        custom_dir: str | None = None
        if scope == SCOPE_WORKSPACE:
            ws_target, custom_dir, err = self._resolve_workspace_target(inputs)
            if err:
                log(f"refusing to write: {err}")
                return {"ok": False, "scope": scope, "error": err, "feature": None}
            if custom_dir:
                log(f"target location: {custom_dir} (custom)")

        # Workspace: resolve relative cwd against the target dir for stability.
        # Global: drop `cwd` entirely — a machine-wide entry shouldn't be
        # pinned to one project dir. The user can re-add it explicitly via
        # inputs.config if they really mean it.
        if scope == SCOPE_WORKSPACE:
            if config.get("cwd") in (None, "", "."):
                config["cwd"] = custom_dir or str(self._root.resolve())
        else:
            cwd_was = config.pop("cwd", None)
            if cwd_was:
                log(f"dropped cwd={cwd_was!r} from config (global scope is project-agnostic)")

        if scope == SCOPE_WORKSPACE:
            where = custom_dir or "this project"
            log(f"writing mcpServers.{feature_id} to {ws_target} ({where})")
            doc = _load_json(ws_target) or {}
            servers = dict(doc.get("mcpServers") or {})
            servers[feature_id] = config
            doc["mcpServers"] = servers
            ws_target.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

            if custom_dir:
                # Detection only inspects *this* project + global, so a custom
                # location can't be reflected as INSTALLED on the card. Judge
                # success straight from the spawn-probe and remember the dir
                # so it's a one-click pick next time.
                log("running spawn-test (list_tools)...")
                ok, perr = self._probe(feature_id, config)
                log("spawn-test ok" if ok else f"spawn-test failed: {perr}")
                self._remember_location(custom_dir)
                return {
                    "ok": ok,
                    "scope": scope,
                    "path": custom_dir,
                    "error": None if ok else perr,
                    "feature": None,
                }
        else:
            log(f"writing mcpServers.{feature_id} to ~/.claude.json (global)")
            try:
                doc = _load_json_strict(self._global_path)
            except CorruptConfigError as e:
                log(f"refusing to write: {e}")
                return {
                    "ok": False,
                    "scope": scope,
                    "error": (
                        f"{self._global_path} exists but is not valid JSON — "
                        f"refusing to overwrite it (would destroy unrelated "
                        f"Claude Code state). Fix or remove the file, then retry. "
                        f"Details: {e}"
                    ),
                    "feature": None,
                }
            servers = dict(doc.get("mcpServers") or {})
            servers[feature_id] = config
            doc["mcpServers"] = servers
            self._write_global(doc)

        log("running spawn-test (list_tools)...")
        feature = self.get(feature_id)
        ok = feature is not None and feature.status == FeatureStatus.INSTALLED
        if ok:
            log("spawn-test ok")
        elif feature is not None:
            log(f"spawn-test failed: {feature.detail.get('probe_error', '?')}")
        return {
            "ok": ok,
            "scope": scope,
            "feature": feature.to_dict() if feature else None,
        }

    def uninstall(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Remove `feature_id` from one scope's config file.

        If `inputs.scope` is given, use it. Otherwise pick the scope that
        currently holds the entry (workspace preferred if both — same priority
        as the probe). No-ops if the entry isn't in the resolved scope.
        """
        in_workspace = feature_id in self._workspace_servers()
        in_global = feature_id in self._global_servers()
        requested = (inputs or {}).get("scope")

        if isinstance(requested, str) and requested in VALID_SCOPES:
            scope = requested
        elif in_workspace:
            scope = SCOPE_WORKSPACE
        elif in_global:
            scope = SCOPE_GLOBAL
        else:
            feature = self.get(feature_id)
            return {
                "ok": True,
                "noop": True,
                "scope": None,
                "feature": feature.to_dict() if feature else None,
            }

        if scope == SCOPE_WORKSPACE:
            ws_target, custom_dir, err = self._resolve_workspace_target(inputs)
            if err:
                return {"ok": False, "scope": scope, "error": err, "feature": None}
            doc = _load_json(ws_target)
            servers = dict(doc.get("mcpServers") or {})
            if feature_id not in servers:
                feature = None if custom_dir else self.get(feature_id)
                return {
                    "ok": True, "noop": True, "scope": scope,
                    "path": custom_dir,
                    "feature": feature.to_dict() if feature else None,
                }
            servers.pop(feature_id)
            # Preserve the file even when empty — easier for `cat` debugging.
            doc["mcpServers"] = servers
            ws_target.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
            if custom_dir:
                return {"ok": True, "scope": scope, "path": custom_dir, "feature": None}
        else:
            try:
                doc = _load_json_strict(self._global_path)
            except CorruptConfigError as e:
                return {
                    "ok": False,
                    "scope": scope,
                    "error": (
                        f"{self._global_path} exists but is not valid JSON — "
                        f"refusing to rewrite it. Fix or remove the file, then "
                        f"retry. Details: {e}"
                    ),
                    "feature": None,
                }
            servers = dict(doc.get("mcpServers") or {})
            if feature_id not in servers:
                feature = self.get(feature_id)
                return {
                    "ok": True, "noop": True, "scope": scope,
                    "feature": feature.to_dict() if feature else None,
                }
            servers.pop(feature_id)
            if servers:
                doc["mcpServers"] = servers
            else:
                # Don't leave an empty mcpServers key cluttering ~/.claude.json
                # if it's the only thing we ever added there.
                doc.pop("mcpServers", None)
            self._write_global(doc)

        feature = self.get(feature_id)
        return {
            "ok": True,
            "scope": scope,
            "feature": feature.to_dict() if feature else None,
        }

    def verify(self, feature_id: str) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown MCP feature {feature_id!r}"}
        return {"ok": feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict()}

    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        scope = _normalize_scope((inputs or {}).get("scope"))
        example = self._example_servers().get(feature_id)
        workspace = self._workspace_servers().get(feature_id)
        global_ = self._global_servers().get(feature_id)
        if (
            example is None
            and workspace is None
            and global_ is None
            and not (inputs and inputs.get("config"))
        ):
            return {"ok": False, "error": f"no example or installed entry for {feature_id!r}"}

        if inputs and isinstance(inputs.get("config"), dict):
            config = dict(inputs["config"])
        else:
            # Show the config we'd actually write (matches install's preference).
            source = workspace if scope == SCOPE_WORKSPACE else global_
            config = dict(source or example or {})

        # Probe-free Feature snapshot — preview must be fast and side-effect free.
        feature = self._build(feature_id, example, workspace, global_, probe=False)

        cmd = config.get("command") or "?"
        args = list(config.get("args") or [])
        env_keys = sorted((config.get("env") or {}).keys()) if isinstance(config.get("env"), dict) else []
        spawn_line = " ".join([str(cmd), *[str(a) for a in args]])

        custom_path_error: str | None = None
        if scope == SCOPE_WORKSPACE:
            ws_target, custom_dir, custom_path_error = self._resolve_workspace_target(inputs)
            target_file = str(ws_target) if custom_dir else ".mcp.json"
        else:
            custom_dir = None
            target_file = "~/.claude.json"

        side_effects: list[dict[str, Any]] = [
            {
                "kind": "config_write",
                "summary": f"Write entry into {target_file} ({scope})",
                "detail": f"mcpServers.{feature_id}",
            },
            {
                "kind": "mcp_spawn",
                "summary": "Spawn-test the server (list_tools)",
                "detail": spawn_line,
            },
        ]
        if env_keys:
            side_effects.append({
                "kind": "env_read",
                "summary": "Read env vars at spawn time (keys only)",
                "detail": ", ".join(env_keys),
            })

        warnings: list[str] = []

        if custom_path_error:
            # Don't block preview — surface it so the dialog can warn and the
            # Confirm button still maps to an install that returns the error.
            return {
                "ok": True,
                "feature": feature.to_dict(),
                "scope": scope,
                "would_be_noop": False,
                "side_effects": side_effects,
                "warnings": [f"Custom location problem: {custom_path_error}"],
            }
        if custom_dir:
            # Project-scoped "already installed" checks below inspect *this*
            # project only, so they're meaningless for an external dir. Just
            # state where it's going and skip them.
            warnings.append(
                f"Installing into a custom location: {custom_dir}/.mcp.json. "
                f"Its status won't show on this card (detection only scans this "
                f"project + global), but the location is remembered for next time."
            )
            return {
                "ok": True,
                "feature": feature.to_dict(),
                "scope": scope,
                "would_be_noop": False,
                "side_effects": side_effects,
                "warnings": warnings,
            }

        already_in_scope = (
            workspace is not None if scope == SCOPE_WORKSPACE else global_ is not None
        )
        if already_in_scope:
            warnings.append(
                f"Already configured in {scope} scope — install will overwrite the entry and re-run the spawn-test."
            )
        # If the OTHER scope already has it, mention that — the user may not realize
        # they're about to end up with the entry in both places.
        other_has = (
            global_ is not None if scope == SCOPE_WORKSPACE else workspace is not None
        )
        if other_has:
            other_scope = SCOPE_GLOBAL if scope == SCOPE_WORKSPACE else SCOPE_WORKSPACE
            warnings.append(
                f"This server is also configured in {other_scope} scope — installing here adds a second copy."
            )
        if scope == SCOPE_GLOBAL and config.get("cwd"):
            warnings.append(
                "Global install drops `cwd` from the entry (machine-wide MCPs shouldn't be pinned to a project dir)."
            )

        return {
            "ok": True,
            "feature": feature.to_dict(),
            "scope": scope,
            "would_be_noop": False,  # mcp install always rewrites + reprobes
            "side_effects": side_effects,
            "warnings": warnings,
        }


__all__ = ["MCPFeatureHandler", "SpawnProbe", "AsyncExitStack", "SCOPE_WORKSPACE", "SCOPE_GLOBAL"]
