"""Tier 3 — Connector features.

Connector catalog is sourced from `connectors/registry.json` (tracked); the
per-connector `requires_env` declaration comes from the YAML frontmatter of
`connectors/<id>.md`. Install means: all required env vars are present in
the user's `.env`. The handler routes secret entry through `env_writer` —
write-only, never echoes values back.

Status mapping
--------------
- INSTALLED   — all `requires_env` vars present (non-empty) in `.env`
- PARTIAL     — some required vars present, some missing
- AVAILABLE   — none of the required vars set
- ERROR       — registry references a connector file that doesn't exist /
                fails to parse

Reverse-dependency safety
-------------------------
Uninstall removes only env vars that are NOT also required by another
installed connector or MCP. Shared variables (e.g. `POSTGRES_PASSWORD`)
are skipped with a note in the result.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import Feature, FeatureKind, FeatureStatus


def _parse_connector_frontmatter(path: Path) -> dict[str, Any] | None:
    """Read `requires_env` and friends from connectors/<id>.md frontmatter."""
    import yaml

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


class ConnectorFeatureHandler:
    """Handler for kind=connector (Tier 3)."""

    kind = FeatureKind.CONNECTOR

    def __init__(self, workspace_root: Path):
        self._root = Path(workspace_root)

    # ---- catalog ------------------------------------------------------

    @property
    def _registry_path(self) -> Path:
        return self._root / "connectors" / "registry.json"

    @property
    def _env_path(self) -> Path:
        return self._root / ".env"

    def _registry_entries(self) -> list[dict[str, Any]]:
        if not self._registry_path.exists():
            return []
        try:
            doc = json.loads(self._registry_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        return list(doc.get("connectors") or [])

    def _env_values(self) -> dict[str, str]:
        # Use the existing reader so .env semantics (quoting, comments) match.
        from services.control_panel.env_writer import read_env_values

        if not self._env_path.exists():
            return {}
        return read_env_values(self._env_path)

    def _requires_env_for(self, connector_md_path: Path) -> list[str]:
        fm = _parse_connector_frontmatter(connector_md_path)
        if fm is None:
            return []
        return [str(v) for v in (fm.get("requires_env") or [])]

    # ---- detection ----------------------------------------------------

    def _build(self, entry: dict[str, Any]) -> Feature:
        cid = entry["id"]
        rel_path = entry.get("path") or f"connectors/{cid}.md"
        md_path = self._root / rel_path
        requires_env = self._requires_env_for(md_path) if md_path.exists() else []

        env_values = self._env_values()
        present = [k for k in requires_env if env_values.get(k)]
        missing = [k for k in requires_env if not env_values.get(k)]

        if not md_path.exists() or _parse_connector_frontmatter(md_path) is None:
            status = FeatureStatus.ERROR
        elif not requires_env:
            # No env required → treat as "INSTALLED" once defined.
            status = FeatureStatus.INSTALLED
        elif not missing:
            status = FeatureStatus.INSTALLED
        elif not present:
            status = FeatureStatus.AVAILABLE
        else:
            status = FeatureStatus.PARTIAL

        return Feature(
            id=cid,
            kind=FeatureKind.CONNECTOR,
            name=str(entry.get("name") or cid),
            description=str(entry.get("description") or ""),
            status=status,
            requires=[],
            detail={
                "path": rel_path,
                "tags": list(entry.get("tags") or []),
                "provides": list(entry.get("provides") or []),
                "status_field": entry.get("status"),
                "requires_env": requires_env,
                "env_present": present,
                "env_missing": missing,
            },
            # Connectors also render their full markdown docs on the detail
            # page; `about` is the short editorial blurb for the card + index.
            about=str(entry.get("about") or "").strip(),
        )

    # ---- handler protocol --------------------------------------------

    def list(self) -> list[Feature]:
        return [self._build(e) for e in self._registry_entries()]

    def get(self, feature_id: str) -> Feature | None:
        for entry in self._registry_entries():
            if entry.get("id") == feature_id:
                return self._build(entry)
        return None

    # ---- install / uninstall -----------------------------------------

    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
    ) -> dict[str, Any]:
        """Write the supplied env values into .env.

        `inputs.env` is a `{KEY: value}` dict — write-only, values are never
        echoed back in any response. The handler refuses unknown keys to
        prevent typos from polluting .env.
        """
        log = log_sink or (lambda _s: None)
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown connector {feature_id!r}"}

        proposed = (inputs or {}).get("env") or {}
        if not isinstance(proposed, dict):
            return {"ok": False, "error": "inputs.env must be a {key: value} dict"}

        allowed = set(feature.detail.get("requires_env") or [])
        rejected = sorted(k for k in proposed.keys() if k not in allowed)
        accepted = {k: str(v) for k, v in proposed.items() if k in allowed and v != ""}

        if not accepted and rejected:
            log(f"rejected unknown keys: {', '.join(rejected)}")
            return {
                "ok": False,
                "error": f"none of the supplied keys are part of this connector's requires_env",
                "rejected": rejected,
            }

        if accepted:
            from services.control_panel.env_writer import update_env_file

            self._env_path.touch(exist_ok=True)
            log(f"writing {len(accepted)} key(s) to .env: {', '.join(sorted(accepted.keys()))}")
            update_env_file(self._env_path, accepted)
        else:
            log("no env values supplied; nothing to write")

        if rejected:
            log(f"rejected unknown keys: {', '.join(rejected)}")

        return {
            "ok": True,
            "wrote_keys": sorted(accepted.keys()),
            "rejected": rejected,
            "feature": self.get(feature_id).to_dict(),
        }

    def _shared_with_other_installed(self, var: str, exclude_connector: str) -> bool:
        """Return True if `var` is required by another connector that is
        currently INSTALLED. (MCP-level reverse-dep check is a future hook.)
        """
        for entry in self._registry_entries():
            if entry.get("id") == exclude_connector:
                continue
            other_path = self._root / (entry.get("path") or f"connectors/{entry['id']}.md")
            if not other_path.exists():
                continue
            other_requires = self._requires_env_for(other_path)
            if var not in other_requires:
                continue
            # Build the other connector to check its status.
            other_feature = self._build(entry)
            if other_feature.status == FeatureStatus.INSTALLED:
                return True
        return False

    def uninstall(self, feature_id: str) -> dict[str, Any]:
        """Clear the connector's env vars from .env, skipping any var that
        another installed connector still depends on."""
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown connector {feature_id!r}"}

        from services.control_panel.env_writer import update_env_file

        requires_env = feature.detail.get("requires_env") or []
        cleared: list[str] = []
        kept_shared: list[str] = []
        to_clear: dict[str, str] = {}

        for var in requires_env:
            if self._shared_with_other_installed(var, exclude_connector=feature_id):
                kept_shared.append(var)
            else:
                to_clear[var] = ""

        if to_clear and self._env_path.exists():
            update_env_file(self._env_path, to_clear)
            cleared = sorted(to_clear.keys())

        return {
            "ok": True,
            "cleared": cleared,
            "kept_shared": kept_shared,
            "feature": self.get(feature_id).to_dict(),
        }

    def verify(self, feature_id: str) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown connector {feature_id!r}"}
        return {"ok": feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict()}

    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown connector {feature_id!r}"}

        allowed = set(feature.detail.get("requires_env") or [])
        proposed = (inputs or {}).get("env") or {}
        if not isinstance(proposed, dict):
            proposed = {}
        accepted_keys = sorted(k for k, v in proposed.items() if k in allowed and v not in (None, ""))
        rejected_keys = sorted(k for k in proposed.keys() if k not in allowed)

        side_effects: list[dict[str, Any]] = []
        if accepted_keys:
            side_effects.append({
                "kind": "env_write",
                "summary": "Write keys to .env (values never echoed back)",
                "detail": ", ".join(accepted_keys),
            })
        else:
            side_effects.append({
                "kind": "noop",
                "summary": "Nothing to write",
                "detail": "No env values supplied — install would be a no-op.",
            })

        warnings: list[str] = []
        if rejected_keys:
            warnings.append(
                f"Unknown keys will be rejected (not in requires_env): {', '.join(rejected_keys)}"
            )
        env_missing = feature.detail.get("env_missing") or []
        if env_missing:
            still_missing = sorted(k for k in env_missing if k not in accepted_keys)
            if still_missing:
                warnings.append(
                    f"After this install, the connector will still be missing: {', '.join(still_missing)}"
                )

        return {
            "ok": True,
            "feature": feature.to_dict(),
            "would_be_noop": not accepted_keys,
            "side_effects": side_effects,
            "warnings": warnings,
        }
