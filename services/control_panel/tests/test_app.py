"""Smoke tests for the control panel.

Skips entirely when the UI deps (FastAPI, Jinja2) aren't installed, so this
test suite is safe to register in validate.py against a checkout that hasn't
run `pip install -r services/control_panel/requirements.txt` yet.
"""
from __future__ import annotations

import importlib.util
import unittest

_HAS_FASTAPI = all(importlib.util.find_spec(m) is not None for m in ("fastapi", "jinja2"))


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed; install services/control_panel/requirements.txt")
class DashboardSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient

        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        cfg = Config.from_env()
        cls.cfg = cfg
        cls.client = TestClient(create_app(cfg))

    def test_dashboard_returns_200(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Recipes", resp.text)

    def test_dashboard_lists_known_recipe(self):
        """The 'code-review' recipe should be registered and visible."""
        resp = self.client.get("/")
        self.assertIn("code-review", resp.text)

    def test_dashboard_lists_known_connector(self):
        resp = self.client.get("/")
        self.assertIn("bitbucket", resp.text)
        self.assertIn("jira", resp.text)

    def test_health_endpoint_renders_html_fragment(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        # Health probes are best-effort — both states are valid here.
        self.assertIn("llama-swap", resp.text)
        self.assertIn("postgres", resp.text)

    def test_recipe_overview_renders_body_as_html(self):
        resp = self.client.get("/recipes/code-review")
        self.assertEqual(resp.status_code, 200)
        # Headings in the body should become <h2>/<h3> after markdown render.
        self.assertRegex(resp.text, r"<h[23][^>]*>.*What this does")
        # Frontmatter sidebar should surface the id and execution type.
        self.assertIn("<code>code-review</code>", resp.text)
        self.assertIn("prompt", resp.text)

    def test_recipe_overview_active_tab(self):
        resp = self.client.get("/recipes/code-review")
        # Active tab marker is the `class="active"` attribute on Overview.
        self.assertRegex(resp.text, r'href="/recipes/code-review"\s+class="\s*active\s*"')

    def test_recipe_run_placeholder(self):
        resp = self.client.get("/recipes/code-review/run")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Phase B3", resp.text)

    def test_recipe_edit_placeholder(self):
        resp = self.client.get("/recipes/code-review/edit")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Phase B4", resp.text)

    def test_recipe_404_for_unknown_id(self):
        resp = self.client.get("/recipes/does-not-exist-xyz")
        self.assertEqual(resp.status_code, 404)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi not installed")
class ConfigDefaultsTest(unittest.TestCase):
    def test_workspace_root_resolves(self):
        from services.control_panel.config import Config

        cfg = Config.from_env()
        self.assertTrue((cfg.workspace_root / "recipes").is_dir(),
                        f"recipes/ not found under detected root {cfg.workspace_root}")
        self.assertTrue((cfg.workspace_root / "connectors").is_dir())

    def test_default_host_and_port(self):
        from services.control_panel.config import Config

        cfg = Config.from_env()
        # If the user has overridden via env we don't assert specific values —
        # just that they're sane.
        self.assertIsInstance(cfg.host, str)
        self.assertGreater(cfg.port, 0)


class IndexLoadersStdlibOnlyTest(unittest.TestCase):
    """Load recipes & connectors *without* any FastAPI deps. Ensures the
    package's read-only path stays import-light."""

    def test_load_recipes_returns_summaries(self):
        from services.control_panel.config import Config
        from services.control_panel.recipes_index import load_recipes

        recipes = load_recipes(Config.from_env())
        self.assertGreater(len(recipes), 0)
        ids = {r.id for r in recipes}
        self.assertIn("code-review", ids)

    def test_load_connectors_returns_summaries(self):
        from services.control_panel.config import Config
        from services.control_panel.recipes_index import load_connectors

        connectors = load_connectors(Config.from_env())
        ids = {c.id for c in connectors}
        self.assertIn("bitbucket", ids)
        self.assertIn("jira", ids)

    def test_get_recipe_by_id(self):
        from services.control_panel.config import Config
        from services.control_panel.recipes_index import get_recipe

        result = get_recipe(Config.from_env(), "code-review")
        self.assertIsNotNone(result)
        fm, body, path = result
        self.assertEqual(fm["id"], "code-review")
        self.assertTrue(body)
        self.assertTrue(path.exists())

    def test_get_recipe_unknown_returns_none(self):
        from services.control_panel.config import Config
        from services.control_panel.recipes_index import get_recipe

        self.assertIsNone(get_recipe(Config.from_env(), "does-not-exist-xyz"))


if __name__ == "__main__":
    unittest.main()
