"""TestClient-driven tests for the /api/v1/features/* JSON endpoints.

Hits the real registry against the real workspace — so the catalog parses,
T1 detect-on-PATH runs (with whatever's actually installed), and the
filesystem state of `recipes/`, `connectors/`, and `.mcp.json.example` is
the source of truth. Tests assert SHAPE, not specific feature ids that
would drift with the codebase.
"""
from __future__ import annotations

import importlib.util
import unittest

_HAS_FASTAPI = all(
    importlib.util.find_spec(m) is not None for m in ("fastapi", "jinja2", "yaml")
)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2/yaml not installed")
class FeaturesApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        cls.cfg = Config.from_env()
        cls.client = TestClient(create_app(cls.cfg))

    def test_list_returns_features_grouped_by_kind(self):
        resp = self.client.get("/api/v1/features")
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("features", body)
        self.assertIn("kinds", body)
        kinds_in_body = set(body["kinds"])
        # All 5 kinds must be wired.
        self.assertEqual(kinds_in_body, {"system", "container", "mcp", "recipe", "connector"})
        # Spot-check shape of one feature.
        self.assertTrue(body["features"], "expected at least one feature in the registry")
        sample = body["features"][0]
        for key in ("id", "kind", "name", "description", "status", "requires", "detail"):
            self.assertIn(key, sample)

    def test_list_includes_t1_t2_t3_signals(self):
        body = self.client.get("/api/v1/features").json()
        kinds_observed = {f["kind"] for f in body["features"]}
        # T1 + T2 always present via catalog; T3 only if those sources exist.
        self.assertIn("system", kinds_observed)
        self.assertIn("container", kinds_observed)
        # T3 recipe should always be there — repo ships with recipes/
        self.assertIn("recipe", kinds_observed)

    def test_get_returns_single_feature_with_unmet_prereqs(self):
        # Pick whatever the registry shows as a system feature.
        body = self.client.get("/api/v1/features").json()
        sys_feature = next(f for f in body["features"] if f["kind"] == "system")
        resp = self.client.get(f"/api/v1/features/system/{sys_feature['id']}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["feature"]["id"], sys_feature["id"])
        self.assertIn("unmet_prereqs", data)

    def test_get_unknown_feature_returns_404(self):
        resp = self.client.get("/api/v1/features/system/does-not-exist")
        self.assertEqual(resp.status_code, 404)

    def test_get_unknown_kind_returns_404(self):
        resp = self.client.get("/api/v1/features/martian/foo")
        self.assertEqual(resp.status_code, 404)

    def test_install_system_feature_is_print_or_noop(self):
        """System install never runs sudo — always returns kind=print_command or noop."""
        body = self.client.get("/api/v1/features").json()
        sys_feature = next(f for f in body["features"] if f["kind"] == "system")
        resp = self.client.post(
            f"/api/v1/features/system/{sys_feature['id']}/install", json={}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        if data.get("ok"):
            # Either it's already installed (noop) or it's a print-command response.
            self.assertTrue(
                data.get("noop") or data.get("kind") == "print_command",
                f"unexpected install response shape: {data}",
            )

    def test_install_with_non_object_body_400s(self):
        body = self.client.get("/api/v1/features").json()
        sys_feature = next(f for f in body["features"] if f["kind"] == "system")
        resp = self.client.post(
            f"/api/v1/features/system/{sys_feature['id']}/install",
            data="not-json",
            headers={"content-type": "application/json"},
        )
        # Either accepted as {} (fallback) or 400. Both are valid shapes — assert it doesn't 5xx.
        self.assertLess(resp.status_code, 500)

    def test_uninstall_system_refuses(self):
        body = self.client.get("/api/v1/features").json()
        sys_feature = next(f for f in body["features"] if f["kind"] == "system")
        resp = self.client.post(f"/api/v1/features/system/{sys_feature['id']}/uninstall")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # System uninstall always refuses.
        self.assertFalse(data["ok"])

    def test_verify_returns_ok_bool(self):
        body = self.client.get("/api/v1/features").json()
        sys_feature = next(f for f in body["features"] if f["kind"] == "system")
        resp = self.client.post(f"/api/v1/features/system/{sys_feature['id']}/verify")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ok", resp.json())

    def test_preview_returns_shape(self):
        body = self.client.get("/api/v1/features").json()
        sys_feature = next(f for f in body["features"] if f["kind"] == "system")
        resp = self.client.post(
            f"/api/v1/features/system/{sys_feature['id']}/preview", json={}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        for key in ("ok", "feature", "would_be_noop", "side_effects", "warnings", "unmet_prereqs"):
            self.assertIn(key, data, f"preview payload missing key {key!r}")
        self.assertIsInstance(data["side_effects"], list)
        self.assertIsInstance(data["warnings"], list)
        self.assertIsInstance(data["unmet_prereqs"], list)

    def test_preview_unknown_kind_returns_404(self):
        resp = self.client.post("/api/v1/features/martian/foo/preview", json={})
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
