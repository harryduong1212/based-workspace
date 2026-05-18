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

    def unmet_prereqs_detail(self, feature: Feature) -> list[dict[str, Any]]:
        """Like `unmet_prereqs` but each entry carries the prereq's kind and
        status so the UI can say the *right* thing — e.g. a STOPPED container
        is "installed but not started", not "not installed"."""
        index = self._index_by_id()
        out: list[dict[str, Any]] = []
        for req_id in feature.requires:
            req = index.get(req_id)
            if req is None:
                out.append({"id": req_id, "kind": None, "status": "missing"})
            elif req.status != FeatureStatus.INSTALLED:
                out.append({"id": req_id, "kind": req.kind.value, "status": req.status.value})
        return out

    def resolve_install_plan(
        self, kind: FeatureKind, feature_id: str
    ) -> list[dict[str, Any]]:
        """Topologically ordered steps to install `feature_id`: every
        not-yet-INSTALLED prerequisite (recursive, deps first) followed by the
        target itself. Each step is `{id, kind, status}`.

        The runner installs these in order, so a target's prereqs are all
        INSTALLED by the time it runs — no gate failure, no cryptic spawn
        error. Unknown prereq ids surface as a `kind: None` step so the
        runner can report them instead of silently skipping.
        """
        index = self._index_by_id()
        target = self.get(kind, feature_id)
        if target is None:
            return []

        plan: list[dict[str, Any]] = []
        seen: set[str] = {target.id}  # guard against requires-cycles back to target

        def visit(fid: str) -> None:
            if fid in seen:
                return
            seen.add(fid)
            feat = index.get(fid)
            if feat is None:
                plan.append({"id": fid, "kind": None, "status": "missing"})
                return
            for req in feat.requires:
                visit(req)
            if feat.status != FeatureStatus.INSTALLED:
                plan.append({"id": fid, "kind": feat.kind.value, "status": feat.status.value})

        for req in target.requires:
            visit(req)
        # Target is always the final step (handler no-ops if already installed).
        plan.append({"id": target.id, "kind": target.kind.value, "status": target.status.value})
        return plan

    # ---- actions ------------------------------------------------------

    def install(
        self,
        kind: FeatureKind,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
        skip_prereq_check: bool = False,
    ) -> dict[str, Any]:
        """Install one feature. Refuses when prereqs are unmet *unless*
        `skip_prereq_check` — the cascade runner passes that because it has
        already topo-ordered the steps and installed prereqs first, so the
        per-call gate would be a redundant (and race-prone) re-check.
        """
        h = self._handlers.get(kind)
        if h is None:
            return {"ok": False, "error": f"unknown kind {kind.value!r}"}
        feature = self.get(kind, feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown feature {feature_id!r} (kind={kind.value})"}

        if not skip_prereq_check:
            unmet = self.unmet_prereqs(feature)
            if unmet:
                return {
                    "ok": False,
                    "error": "prerequisites not satisfied",
                    "unmet_prereqs": unmet,
                    "feature": feature.to_dict(),
                }
        return h.install(feature_id, inputs, log_sink=log_sink)

    def uninstall(
        self,
        kind: FeatureKind,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        h = self._handlers.get(kind)
        if h is None:
            return {"ok": False, "error": f"unknown kind {kind.value!r}"}
        return h.uninstall(feature_id, inputs)

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
        payload["unmet_prereqs_detail"] = self.unmet_prereqs_detail(feature)

        # The full cascade the runner will execute (prereqs deps-first, then
        # the target). Prereq steps = everything except the trailing target.
        plan = self.resolve_install_plan(kind, feature_id)
        payload["install_plan"] = plan
        prereq_steps = plan[:-1] if plan else []

        payload.setdefault("warnings", [])
        if prereq_steps:
            # Not a blocker any more — an explanation of the auto-cascade.
            names = ", ".join(s["id"] for s in prereq_steps)
            payload["warnings"].insert(
                0,
                f"This will also set up {len(prereq_steps)} prerequisite(s) first, "
                f"in order: {names} — then {feature_id}.",
            )
        return payload
