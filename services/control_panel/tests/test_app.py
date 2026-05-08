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

    def test_recipe_run_form_renders_inputs_and_providers(self):
        resp = self.client.get("/recipes/code-review/run")
        self.assertEqual(resp.status_code, 200)
        # Form action posts back to the same URL.
        self.assertIn('action="/recipes/code-review/run"', resp.text)
        # Each declared input renders as <textarea name="input__X">.
        self.assertIn('name="input__diff"', resp.text)
        self.assertIn('name="input__target_branch"', resp.text)
        # Provider dropdown contains the three known providers.
        self.assertIn('name="model_ref"', resp.text)
        self.assertIn("anthropic/", resp.text)
        self.assertIn("gemini/", resp.text)
        # Free-text override always present.
        self.assertIn('name="model_override"', resp.text)

    def test_recipe_edit_loads_raw_content_into_editor(self):
        resp = self.client.get("/recipes/code-review/edit")
        self.assertEqual(resp.status_code, 200)
        # The frontmatter delimiter should appear inside the textarea body.
        self.assertIn("id: code-review", resp.text)
        self.assertIn('id="cm_editor"', resp.text)
        # CodeMirror script is included.
        self.assertIn("codemirror.min.js", resp.text)

    def test_recipe_404_for_unknown_id(self):
        resp = self.client.get("/recipes/does-not-exist-xyz")
        self.assertEqual(resp.status_code, 404)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class RunFlowTest(unittest.TestCase):
    """End-to-end run flow with the dispatcher monkeypatched to a fake provider."""

    @classmethod
    def setUpClass(cls):
        import io
        from fastapi.testclient import TestClient

        from services.control_panel import runs as runs_mod
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        # Replace the worker's dispatch_prompt with a deterministic fake that
        # writes three chunks to the sink. Avoids any real network call.
        original_start = runs_mod.start_run
        cls._original_start = original_start

        def fake_start(cfg, recipe_id, fm, body, inputs, model_ref):
            run = original_start.__wrapped__(cfg, recipe_id, fm, body, inputs, model_ref) \
                if hasattr(original_start, "__wrapped__") else None
            del run

            import threading
            import uuid
            from datetime import datetime, timezone
            from services.control_panel.runs import Run, _ChunkSink, _runs, _runs_lock

            r = Run(
                id=uuid.uuid4().hex[:12],
                recipe_id=recipe_id,
                model_ref=model_ref or "fake/model",
                inputs=dict(inputs),
                started_at=datetime.now(timezone.utc),
            )
            with _runs_lock:
                _runs[r.id] = r

            def worker():
                try:
                    sink = _ChunkSink(r)
                    sink.write("hello ")
                    sink.write("world")
                    r.status = "done"
                except Exception as e:  # pragma: no cover
                    r.error = str(e)
                    r.status = "error"
                finally:
                    r._queue.put(None)
                    r._done.set()

            threading.Thread(target=worker, daemon=True).start()
            return r

        runs_mod.start_run = fake_start

        # Reimport app to pick up new start_run binding via the module-level reference.
        # create_app captures `start_run` from runs_mod at call time, but the route
        # closure captured the function object — so we need to also patch the app's
        # imported binding. Patch the bound name in app's module too.
        from services.control_panel import app as app_mod
        cls._app_original_start = app_mod.start_run
        app_mod.start_run = fake_start

        cfg = Config.from_env()
        cls.client = TestClient(create_app(cfg))

    @classmethod
    def tearDownClass(cls):
        from services.control_panel import app as app_mod
        from services.control_panel import runs as runs_mod
        app_mod.start_run = cls._app_original_start
        runs_mod.start_run = cls._original_start

    def test_post_run_redirects_to_run_view(self):
        resp = self.client.post(
            "/recipes/code-review/run",
            data={"model_ref": "anthropic/claude-haiku-4-5-20251001", "input__target_branch": "main"},
            follow_redirects=False,
        )
        self.assertEqual(resp.status_code, 303)
        self.assertRegex(resp.headers["location"], r"^/runs/[a-f0-9]{12}$")

    def test_run_view_renders_status_pill(self):
        resp = self.client.post(
            "/recipes/code-review/run",
            data={"model_ref": "anthropic/claude-haiku-4-5-20251001"},
            follow_redirects=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("run-output", resp.text)
        self.assertIn("run-status", resp.text)

    def test_sse_stream_emits_chunks_and_done_event(self):
        from services.control_panel.runs import get_run

        resp = self.client.post(
            "/recipes/code-review/run",
            data={"model_ref": "anthropic/claude-haiku-4-5-20251001"},
            follow_redirects=False,
        )
        run_id = resp.headers["location"].rsplit("/", 1)[-1]
        # Wait until the worker has finished writing its 2 chunks + sentinel.
        run = get_run(run_id)
        self.assertIsNotNone(run)
        run._done.wait(timeout=5)

        with self.client.stream("GET", f"/api/runs/{run_id}/stream") as r:
            self.assertEqual(r.status_code, 200)
            self.assertIn("text/event-stream", r.headers["content-type"])
            body = "".join(r.iter_text())

        self.assertIn("event: chunk", body)
        self.assertIn("event: done", body)
        self.assertIn("hello ", body)
        self.assertIn("world", body)

    def test_model_override_wins(self):
        from services.control_panel.runs import get_run

        resp = self.client.post(
            "/recipes/code-review/run",
            data={
                "model_ref": "anthropic/claude-opus-4-7",
                "model_override": "local/qwen2.5-coder-14b",
            },
            follow_redirects=False,
        )
        run_id = resp.headers["location"].rsplit("/", 1)[-1]
        self.assertEqual(get_run(run_id).model_ref, "local/qwen2.5-coder-14b")


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class EditFlowTest(unittest.TestCase):
    """Edit-save flow against a tmpdir-backed Config so real recipes are untouched."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        from pathlib import Path

        from fastapi.testclient import TestClient
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        cls.tmpdir = tempfile.mkdtemp(prefix="cp_edit_test_")
        root = Path(cls.tmpdir)
        (root / "recipes").mkdir()
        (root / "connectors").mkdir()
        (root / "services").mkdir()
        (root / "scripts").mkdir()

        # A minimal valid recipe.
        cls.recipe_path = root / "recipes" / "demo.md"
        cls.recipe_path.write_text(
            "---\n"
            "id: demo\n"
            "name: Demo\n"
            "description: tmp recipe used by EditFlowTest.\n"
            "audience: tech\n"
            "version: 0.1.0\n"
            "status: experimental\n"
            "tags: []\n"
            "requires_skills: []\n"
            "requires_workflows: []\n"
            "requires_connectors: []\n"
            "requires_mcp: []\n"
            "requires_env: []\n"
            "execution:\n"
            "  type: prompt\n"
            "---\n"
            "## Prompt\n\nhello\n",
            encoding="utf-8",
        )

        # Stub out the audit subprocess — recipe_manager.py isn't in the tmp tree.
        from services.control_panel import recipe_writer as rw

        cls._orig_audit = rw._audit_recipe
        rw._audit_recipe = lambda cfg, recipe_id: []

        cfg = Config(
            workspace_root=root,
            recipes_dir=root / "recipes",
            connectors_dir=root / "connectors",
            services_dir=root / "services",
            host="127.0.0.1",
            port=0,
            reload=False,
            llama_swap_url="http://localhost:11434/v1",
        )
        cls.cfg = cfg
        cls.client = TestClient(create_app(cfg))

    @classmethod
    def tearDownClass(cls):
        import shutil
        from services.control_panel import recipe_writer as rw

        rw._audit_recipe = cls._orig_audit
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def test_save_writes_file(self):
        new_body = self.recipe_path.read_text(encoding="utf-8").replace("hello", "hello world")
        resp = self.client.post("/recipes/demo/edit", data={"content": new_body})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Saved", resp.text)
        self.assertIn("hello world", self.recipe_path.read_text(encoding="utf-8"))

    def test_save_rejects_broken_yaml(self):
        before = self.recipe_path.read_text(encoding="utf-8")
        broken = "---\nid: [unclosed\n---\nbody\n"
        resp = self.client.post("/recipes/demo/edit", data={"content": broken})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Save failed", resp.text)
        self.assertIn("frontmatter", resp.text)
        # File untouched.
        self.assertEqual(self.recipe_path.read_text(encoding="utf-8"), before)

    def test_save_rejects_id_mismatch(self):
        before = self.recipe_path.read_text(encoding="utf-8")
        # Same recipe but with a different `id:` in frontmatter.
        munged = before.replace("id: demo", "id: not-demo")
        resp = self.client.post("/recipes/demo/edit", data={"content": munged})
        self.assertIn("Save failed", resp.text)
        # The apostrophe gets HTML-escaped by Jinja; match against either form.
        self.assertRegex(resp.text, r"doesn(?:'|&#39;)t match")
        self.assertEqual(self.recipe_path.read_text(encoding="utf-8"), before)

    def test_save_404_for_unknown_recipe(self):
        resp = self.client.post("/recipes/no-such-recipe/edit", data={"content": "..."})
        self.assertEqual(resp.status_code, 404)

    def test_new_form_renders(self):
        resp = self.client.get("/recipes/new")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('action="/recipes/new"', resp.text)
        self.assertIn('name="execution_type"', resp.text)

    def test_new_recipe_creates_file_and_redirects_to_edit(self):
        resp = self.client.post(
            "/recipes/new",
            data={
                "id": "fresh-recipe",
                "name": "Fresh",
                "description": "A brand-new recipe scaffolded by B5.",
                "audience": "tech",
                "execution_type": "prompt",
                "tags": "demo, b5",
            },
            follow_redirects=False,
        )
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp.headers["location"], "/recipes/fresh-recipe/edit")
        target = self.cfg.recipes_dir / "fresh-recipe.md"
        self.assertTrue(target.exists())
        body = target.read_text(encoding="utf-8")
        self.assertIn("id: fresh-recipe", body)
        self.assertIn("type: prompt", body)
        self.assertIn("- demo", body)

    def test_new_recipe_rejects_duplicate_id(self):
        # First create succeeds.
        self.client.post(
            "/recipes/new",
            data={"id": "dupe", "name": "x", "description": "x", "audience": "tech", "execution_type": "prompt"},
            follow_redirects=False,
        )
        # Second fails with 400 + form re-rendered.
        resp = self.client.post(
            "/recipes/new",
            data={"id": "dupe", "name": "y", "description": "y", "audience": "tech", "execution_type": "prompt"},
            follow_redirects=False,
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("already exists", resp.text)
        # Form re-rendered with submitted values intact.
        self.assertIn('value="dupe"', resp.text)

    def test_new_recipe_rejects_invalid_execution_type(self):
        resp = self.client.post(
            "/recipes/new",
            data={"id": "bad-type", "name": "x", "description": "x", "execution_type": "freeform"},
            follow_redirects=False,
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("execution_type", resp.text)


class RecipeSkeletonUnitTest(unittest.TestCase):
    """Direct tests for build_skeleton — no FastAPI involvement."""

    def test_prompt_skeleton_parses_as_yaml_frontmatter(self):
        from services.control_panel.recipe_skeleton import build_skeleton

        content = build_skeleton(
            recipe_id="x",
            name="X",
            description="d",
            audience="tech",
            tags=["a", "b"],
            execution_type="prompt",
        )
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("\n---\n", content[4:])
        self.assertIn("## Prompt", content)
        self.assertIn("- a", content)

    def test_agent_and_workflow_have_correct_section(self):
        from services.control_panel.recipe_skeleton import build_skeleton

        agent = build_skeleton(recipe_id="a", name="A", description="d", audience="tech", tags=[], execution_type="agent")
        self.assertIn("## Agent", agent)
        self.assertNotIn("## Prompt", agent)

        wf = build_skeleton(recipe_id="w", name="W", description="d", audience="tech", tags=[], execution_type="workflow")
        self.assertIn("## Workflow", wf)

    def test_unsupported_execution_type_raises(self):
        from services.control_panel.recipe_skeleton import build_skeleton

        with self.assertRaises(ValueError):
            build_skeleton(recipe_id="x", name="X", description="d", audience="tech", tags=[], execution_type="freeform")


class RecipeWriterUnitTest(unittest.TestCase):
    """Direct unit tests for recipe_writer — no FastAPI involvement."""

    def setUp(self):
        import tempfile
        from pathlib import Path
        from services.control_panel.config import Config

        self.tmpdir = tempfile.mkdtemp(prefix="cp_writer_test_")
        root = Path(self.tmpdir)
        (root / "recipes").mkdir()
        self.cfg = Config(
            workspace_root=root,
            recipes_dir=root / "recipes",
            connectors_dir=root / "connectors",
            services_dir=root / "services",
            host="127.0.0.1",
            port=0,
            reload=False,
            llama_swap_url="",
        )

        from services.control_panel import recipe_writer as rw
        self._orig = rw._audit_recipe
        rw._audit_recipe = lambda cfg, recipe_id: []

    def tearDown(self):
        import shutil
        from services.control_panel import recipe_writer as rw
        rw._audit_recipe = self._orig
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_atomic_write_does_not_leak_tempfile_on_success(self):
        from services.control_panel.recipe_writer import write_recipe

        result = write_recipe(self.cfg, "ok", "---\nid: ok\n---\nbody\n")
        self.assertTrue(result.ok)
        # Only the final file should exist — no leftover dotfiles.
        files = sorted(p.name for p in self.cfg.recipes_dir.iterdir())
        self.assertEqual(files, ["ok.md"])

    def test_invalid_id_rejected(self):
        from services.control_panel.recipe_writer import write_recipe

        result = write_recipe(self.cfg, "../etc/passwd", "---\nid: x\n---\n")
        self.assertFalse(result.ok)
        self.assertIn("invalid recipe id", result.message)

    def test_missing_frontmatter_rejected(self):
        from services.control_panel.recipe_writer import write_recipe

        result = write_recipe(self.cfg, "x", "no frontmatter here")
        self.assertFalse(result.ok)
        self.assertIn("frontmatter", result.message)


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
