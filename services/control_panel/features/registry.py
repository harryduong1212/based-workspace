"""Feature registry — aggregates all kind handlers + the dep-graph engine.

Single entry point for the API layer. Install operations route through
`install_with_prereq_check` which walks `Feature.requires` and refuses to
proceed if any prereq isn't INSTALLED. Uninstall and verify go straight
to the handler — those are safe regardless of dep state.

The registry is instantiated per-request (cheap; handlers are stateless).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import Feature, FeatureHandler, FeatureKind, FeatureStatus
from .connector import ConnectorFeatureHandler
from .container import ContainerFeatureHandler
from .mcp import MCPFeatureHandler
from .recipe import RecipeFeatureHandler
from .system import SystemFeatureHandler


class FeatureRegistry:
    """Maps `kind` → handler and provides graph-aware install."""

    def __init__(
        self,
        workspace_root: Path,
        handlers: dict[FeatureKind, FeatureHandler] | None = None,
    ):
        self._root = Path(workspace_root)
        if handlers is not None:
            self._handlers = dict(handlers)
        else:
            self._handlers = {
                FeatureKind.SYSTEM: SystemFeatureHandler(),
                FeatureKind.CONTAINER: ContainerFeatureHandler(workspace_root=self._root),
                FeatureKind.MCP: MCPFeatureHandler(workspace_root=self._root),
                FeatureKind.RECIPE: RecipeFeatureHandler(workspace_root=self._root),
                FeatureKind.CONNECTOR: ConnectorFeatureHandler(workspace_root=self._root),
            }

    # ---- discovery ----------------------------------------------------

    def kinds(self) -> list[FeatureKind]:
        return list(self._handlers.keys())

    def all_features(self) -> list[Feature]:
        out: list[Feature] = []
        for handler in self._handlers.values():
            try:
                out.extend(handler.list())
            except Exception:  # noqa: BLE001 — handler errors shouldn't crash the page
                continue
        return out

    def get(self, kind: FeatureKind, feature_id: str) -> Feature | None:
        h = self._handlers.get(kind)
        if h is None:
            return None
        try:
            return h.get(feature_id)
        except Exception:  # noqa: BLE001
            return None

    # ---- dep graph ----------------------------------------------------

    def _index_by_id(self) -> dict[str, Feature]:
        # Single id namespace across kinds. We rely on catalog discipline
        # (no two features with the same id even across kinds) — enforced
        # in tests on the static catalog; T3 sources are kind-segregated.
        index: dict[str, Feature] = {}
        for f in self.all_features():
            index.setdefault(f.id, f)
        return index

    def unmet_prereqs(self, feature: Feature) -> list[str]:
        """Return prereq feature ids that are NOT INSTALLED.

        An unknown prereq id (not present in any handler's listing) is also
        reported as unmet so the user sees the problem instead of a silent
        green light.
        """
        index = self._index_by_id()
        unmet: list[str] = []
        for req_id in feature.requires:
            req = index.get(req_id)
            if req is None or req.status != FeatureStatus.INSTALLED:
                unmet.append(req_id)
        return unmet

    # ---- actions ------------------------------------------------------

    def install(
        self,
        kind: FeatureKind,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Gated install: refuses when prereqs are unmet."""
        h = self._handlers.get(kind)
        if h is None:
            return {"ok": False, "error": f"unknown kind {kind.value!r}"}
        feature = self.get(kind, feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown feature {feature_id!r} (kind={kind.value})"}

        unmet = self.unmet_prereqs(feature)
        if unmet:
            return {
                "ok": False,
                "error": "prerequisites not satisfied",
                "unmet_prereqs": unmet,
                "feature": feature.to_dict(),
            }
        return h.install(feature_id, inputs)

    def uninstall(self, kind: FeatureKind, feature_id: str) -> dict[str, Any]:
        h = self._handlers.get(kind)
        if h is None:
            return {"ok": False, "error": f"unknown kind {kind.value!r}"}
        return h.uninstall(feature_id)

    def verify(self, kind: FeatureKind, feature_id: str) -> dict[str, Any]:
        h = self._handlers.get(kind)
        if h is None:
            return {"ok": False, "error": f"unknown kind {kind.value!r}"}
        return h.verify(feature_id)

    def preview(
        self,
        kind: FeatureKind,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Compose handler.preview + unmet_prereqs into one dialog-ready payload."""
        h = self._handlers.get(kind)
        if h is None:
            return {"ok": False, "error": f"unknown kind {kind.value!r}"}
        feature = self.get(kind, feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown feature {feature_id!r} (kind={kind.value})"}
        payload = h.preview(feature_id, inputs)
        if not payload.get("ok"):
            return payload
        payload["unmet_prereqs"] = self.unmet_prereqs(feature)
        payload.setdefault("warnings", [])
        if payload["unmet_prereqs"]:
            payload["warnings"].insert(
                0,
                f"Install is blocked until prereqs are installed: {', '.join(payload['unmet_prereqs'])}",
            )
        return payload
