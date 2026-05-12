"""Unit tests for the features-module base abstractions.

Scope: Feature dataclass shape, enums, catalog YAML parsing. Handler
implementations live in their own modules and have their own test files.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

_HAS_YAML = importlib.util.find_spec("yaml") is not None


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class FeatureShapeTest(unittest.TestCase):
    def test_to_dict_roundtrips_basic_fields(self):
        from services.control_panel.features import Feature, FeatureKind, FeatureStatus

        f = Feature(
            id="podman",
            kind=FeatureKind.SYSTEM,
            name="Podman",
            description="runtime",
            status=FeatureStatus.INSTALLED,
            requires=["x"],
            detail={"foo": "bar"},
        )
        d = f.to_dict()
        self.assertEqual(d["id"], "podman")
        self.assertEqual(d["kind"], "system")
        self.assertEqual(d["status"], "installed")
        self.assertEqual(d["requires"], ["x"])
        self.assertEqual(d["detail"], {"foo": "bar"})

    def test_status_enum_values(self):
        from services.control_panel.features import FeatureStatus

        values = {s.value for s in FeatureStatus}
        # Six statuses defined; if we add/remove, this test forces a conscious update.
        self.assertEqual(
            values,
            {"available", "installed", "partial", "error", "unavailable", "unknown"},
        )

    def test_kind_enum_values(self):
        from services.control_panel.features import FeatureKind

        values = {k.value for k in FeatureKind}
        self.assertEqual(values, {"system", "container", "mcp", "recipe", "connector"})


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class LoadCatalogTest(unittest.TestCase):
    def test_repo_catalog_parses(self):
        """The shipped catalog.yaml must parse cleanly."""
        from services.control_panel.features import load_catalog

        catalog = load_catalog()
        self.assertIn("system", catalog)
        self.assertIn("container", catalog)
        # Spot-check the two non-negotiable entries.
        self.assertIn("podman", catalog["system"])
        self.assertIn("postgres", catalog["container"])

    def test_unknown_kind_rejected(self):
        from services.control_panel.features import load_catalog

        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as tmp:
            tmp.write("application:\n  foo: {name: F, description: d}\n")
            tmp.flush()
            with self.assertRaisesRegex(ValueError, "application"):
                load_catalog(Path(tmp.name))

    def test_missing_file_raises(self):
        from services.control_panel.features import load_catalog

        with self.assertRaises(FileNotFoundError):
            load_catalog(Path("/nonexistent/catalog.yaml"))

    def test_non_mapping_rejected(self):
        from services.control_panel.features import load_catalog

        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as tmp:
            tmp.write("- just\n- a\n- list\n")
            tmp.flush()
            with self.assertRaisesRegex(ValueError, "mapping"):
                load_catalog(Path(tmp.name))


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class FeatureHandlerProtocolTest(unittest.TestCase):
    def test_handler_protocol_runtime_check(self):
        """A class that implements the right methods + `kind` attr satisfies the protocol."""
        from services.control_panel.features import FeatureHandler, FeatureKind

        class _FakeHandler:
            kind = FeatureKind.SYSTEM

            def list(self): return []
            def get(self, fid): return None
            def install(self, fid, inputs=None): return {"ok": True}
            def uninstall(self, fid): return {"ok": True}
            def verify(self, fid): return {"ok": True}

        self.assertIsInstance(_FakeHandler(), FeatureHandler)


if __name__ == "__main__":
    unittest.main()
