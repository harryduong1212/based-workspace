"""Unit tests for FeatureRegistry — aggregation + dep-graph gating."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_HAS_YAML = importlib.util.find_spec("yaml") is not None


# Synthetic handler builder — produces FeatureHandler-shaped fakes
# without hitting the real subprocess/filesystem code paths.

def _fake_handler(kind, features_by_id, install_result=None):
    class _Fake:
        def __init__(self):
            self.kind = kind
            self.installed: list[str] = []
            self.uninstalled: list[str] = []
            self.verified: list[str] = []

        def list(self):
            return list(features_by_id.values())

        def get(self, fid):
            return features_by_id.get(fid)

        def install(self, fid, inputs=None):
            self.installed.append(fid)
            return install_result or {"ok": True, "feature": (features_by_id.get(fid).to_dict() if fid in features_by_id else None)}

        def uninstall(self, fid):
            self.uninstalled.append(fid)
            return {"ok": True}

        def verify(self, fid):
            self.verified.append(fid)
            feat = features_by_id.get(fid)
            from services.control_panel.features import FeatureStatus
            return {"ok": feat is not None and feat.status == FeatureStatus.INSTALLED}

        def preview(self, fid, inputs=None):
            feat = features_by_id.get(fid)
            if feat is None:
                return {"ok": False, "error": f"unknown {fid!r}"}
            return {
                "ok": True,
                "feature": feat.to_dict(),
                "would_be_noop": False,
                "side_effects": [{"kind": "stub", "summary": "x", "detail": "y"}],
                "warnings": [],
            }

    return _Fake()


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class FeatureRegistryTest(unittest.TestCase):
    def _make(self, kinds):
        from services.control_panel.features import FeatureRegistry

        return FeatureRegistry(workspace_root=Path("/tmp"), handlers=kinds)

    def _feat(self, kind_str, fid, status_str="available", requires=None):
        from services.control_panel.features import Feature, FeatureKind, FeatureStatus

        return Feature(
            id=fid,
            kind=FeatureKind(kind_str),
            name=fid,
            description="",
            status=FeatureStatus(status_str),
            requires=requires or [],
        )

    def test_all_features_aggregates_across_handlers(self):
        from services.control_panel.features import FeatureKind

        h_sys = _fake_handler(FeatureKind.SYSTEM, {"podman": self._feat("system", "podman")})
        h_con = _fake_handler(FeatureKind.CONTAINER, {"postgres": self._feat("container", "postgres")})
        reg = self._make({FeatureKind.SYSTEM: h_sys, FeatureKind.CONTAINER: h_con})

        ids = {f.id for f in reg.all_features()}
        self.assertEqual(ids, {"podman", "postgres"})

    def test_unmet_prereqs_returns_uninstalled_requirements(self):
        from services.control_panel.features import FeatureKind

        h_sys = _fake_handler(
            FeatureKind.SYSTEM,
            {"podman": self._feat("system", "podman", "installed")},
        )
        h_con = _fake_handler(
            FeatureKind.CONTAINER,
            {
                "postgres": self._feat("container", "postgres", "available", requires=["podman"]),
                "n8n": self._feat("container", "n8n", "available", requires=["podman", "postgres"]),
            },
        )
        reg = self._make({FeatureKind.SYSTEM: h_sys, FeatureKind.CONTAINER: h_con})

        postgres = reg.get(FeatureKind.CONTAINER, "postgres")
        self.assertEqual(reg.unmet_prereqs(postgres), [])  # podman installed

        n8n = reg.get(FeatureKind.CONTAINER, "n8n")
        self.assertEqual(reg.unmet_prereqs(n8n), ["postgres"])  # podman ok, postgres pending

    def test_unmet_prereqs_unknown_requirement_reported(self):
        from services.control_panel.features import FeatureKind

        h = _fake_handler(
            FeatureKind.CONTAINER,
            {"thing": self._feat("container", "thing", "available", requires=["bogus"])},
        )
        reg = self._make({FeatureKind.CONTAINER: h})

        thing = reg.get(FeatureKind.CONTAINER, "thing")
        self.assertEqual(reg.unmet_prereqs(thing), ["bogus"])

    def test_install_refuses_when_prereq_missing(self):
        from services.control_panel.features import FeatureKind

        h_sys = _fake_handler(
            FeatureKind.SYSTEM, {"podman": self._feat("system", "podman", "available")}
        )
        h_con = _fake_handler(
            FeatureKind.CONTAINER,
            {"postgres": self._feat("container", "postgres", "available", requires=["podman"])},
        )
        reg = self._make({FeatureKind.SYSTEM: h_sys, FeatureKind.CONTAINER: h_con})

        result = reg.install(FeatureKind.CONTAINER, "postgres")
        self.assertFalse(result["ok"])
        self.assertEqual(result["unmet_prereqs"], ["podman"])
        # Handler's install was never invoked.
        self.assertEqual(h_con.installed, [])

    def test_install_allowed_when_prereqs_met(self):
        from services.control_panel.features import FeatureKind

        h_sys = _fake_handler(
            FeatureKind.SYSTEM, {"podman": self._feat("system", "podman", "installed")}
        )
        h_con = _fake_handler(
            FeatureKind.CONTAINER,
            {"postgres": self._feat("container", "postgres", "available", requires=["podman"])},
        )
        reg = self._make({FeatureKind.SYSTEM: h_sys, FeatureKind.CONTAINER: h_con})

        result = reg.install(FeatureKind.CONTAINER, "postgres")
        self.assertTrue(result["ok"])
        self.assertEqual(h_con.installed, ["postgres"])

    def test_uninstall_unconditional(self):
        from services.control_panel.features import FeatureKind

        h = _fake_handler(
            FeatureKind.CONTAINER, {"postgres": self._feat("container", "postgres", "installed")}
        )
        reg = self._make({FeatureKind.CONTAINER: h})
        result = reg.uninstall(FeatureKind.CONTAINER, "postgres")
        self.assertTrue(result["ok"])
        self.assertEqual(h.uninstalled, ["postgres"])

    def test_verify_passes_to_handler(self):
        from services.control_panel.features import FeatureKind

        h = _fake_handler(
            FeatureKind.CONTAINER, {"postgres": self._feat("container", "postgres", "installed")}
        )
        reg = self._make({FeatureKind.CONTAINER: h})
        result = reg.verify(FeatureKind.CONTAINER, "postgres")
        self.assertTrue(result["ok"])

    def test_handler_errors_are_swallowed_in_listings(self):
        """A broken handler's list() must not crash the page."""
        from services.control_panel.features import FeatureKind

        class _Broken:
            kind = FeatureKind.SYSTEM
            def list(self): raise RuntimeError("boom")
            def get(self, fid): raise RuntimeError("boom")
            def install(self, fid, inputs=None): return {"ok": False}
            def uninstall(self, fid): return {"ok": False}
            def verify(self, fid): return {"ok": False}

        h = _fake_handler(FeatureKind.CONTAINER, {"postgres": self._feat("container", "postgres", "installed")})
        reg = self._make({FeatureKind.SYSTEM: _Broken(), FeatureKind.CONTAINER: h})

        features = reg.all_features()
        # Only postgres should appear — the broken handler is skipped.
        self.assertEqual([f.id for f in features], ["postgres"])

    def test_unknown_kind_in_install_errors(self):
        from services.control_panel.features import FeatureKind

        h = _fake_handler(FeatureKind.SYSTEM, {})
        reg = self._make({FeatureKind.SYSTEM: h})
        # Use CONTAINER kind, not registered → kind unknown.
        result = reg.install(FeatureKind.CONTAINER, "anything")
        self.assertFalse(result["ok"])

    def test_preview_attaches_unmet_prereqs(self):
        """Registry.preview must surface unmet prereqs alongside the handler's
        side-effects so the dialog can warn before the user confirms — without
        the handler having to walk the dep graph itself."""
        from services.control_panel.features import FeatureKind

        h_sys = _fake_handler(
            FeatureKind.SYSTEM, {"podman": self._feat("system", "podman", "available")}
        )
        h_con = _fake_handler(
            FeatureKind.CONTAINER,
            {"postgres": self._feat("container", "postgres", "available", requires=["podman"])},
        )
        reg = self._make({FeatureKind.SYSTEM: h_sys, FeatureKind.CONTAINER: h_con})

        r = reg.preview(FeatureKind.CONTAINER, "postgres")
        self.assertTrue(r["ok"])
        self.assertEqual(r["unmet_prereqs"], ["podman"])
        # The first warning must call out the prereq so the dialog leads with it.
        self.assertIn("podman", r["warnings"][0])
        self.assertIn("blocked", r["warnings"][0])

    def test_preview_no_prereqs_unblocked(self):
        from services.control_panel.features import FeatureKind

        h = _fake_handler(
            FeatureKind.SYSTEM, {"podman": self._feat("system", "podman", "available")}
        )
        reg = self._make({FeatureKind.SYSTEM: h})
        r = reg.preview(FeatureKind.SYSTEM, "podman")
        self.assertTrue(r["ok"])
        self.assertEqual(r["unmet_prereqs"], [])

    def test_preview_unknown_feature_errors(self):
        from services.control_panel.features import FeatureKind

        h = _fake_handler(FeatureKind.SYSTEM, {})
        reg = self._make({FeatureKind.SYSTEM: h})
        r = reg.preview(FeatureKind.SYSTEM, "does-not-exist")
        self.assertFalse(r["ok"])


if __name__ == "__main__":
    unittest.main()
