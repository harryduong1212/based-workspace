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
        self.assertIn("gmail", resp.text)
        self.assertIn("github", resp.text)

    def test_connector_detail_renders_body_and_env_status(self):
        resp = self.client.get("/connectors/jira")
        self.assertEqual(resp.status_code, 200)
        # Frontmatter sidebar fields surface.
        self.assertRegex(resp.text, r"<code[^>]*>jira</code>")
        self.assertIn("api_token", resp.text)
        # Required env vars are listed with status pills.
        self.assertIn("JIRA_BASE_URL", resp.text)
        self.assertIn("JIRA_EMAIL", resp.text)
        self.assertIn("JIRA_API_TOKEN", resp.text)
        # Test-connection button is present.
        self.assertIn('hx-post="/connectors/jira/test"', resp.text)

    def test_connector_detail_renders_gmail_with_basic_auth_and_env(self):
        resp = self.client.get("/connectors/gmail")
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.text, r"<code[^>]*>gmail</code>")
        self.assertIn("basic", resp.text)
        self.assertIn("GMAIL_ADDRESS", resp.text)
        self.assertIn("GMAIL_APP_PASSWORD", resp.text)
        self.assertIn('hx-post="/connectors/gmail/test"', resp.text)

    def test_connector_detail_renders_github_with_api_token_and_env(self):
        resp = self.client.get("/connectors/github")
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(resp.text, r"<code[^>]*>github</code>")
        self.assertIn("api_token", resp.text)
        self.assertIn("GITHUB_TOKEN", resp.text)
        self.assertIn('hx-post="/connectors/github/test"', resp.text)

    def test_connector_404_for_unknown_id(self):
        resp = self.client.get("/connectors/no-such-connector")
        self.assertEqual(resp.status_code, 404)

    def test_connector_test_endpoint_reports_missing_envs(self):
        import os as _os
        # Snapshot and clear all three Jira env vars to force missing.
        keys = ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN")
        saved = {k: _os.environ.pop(k, None) for k in keys}
        try:
            resp = self.client.post("/connectors/jira/test")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Missing env vars", resp.text)
            self.assertIn("JIRA_BASE_URL", resp.text)
        finally:
            for k, v in saved.items():
                if v is not None:
                    _os.environ[k] = v

    def test_connector_test_endpoint_reports_all_present(self):
        import os as _os
        keys = ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN")
        saved = {k: _os.environ.pop(k, None) for k in keys}
        for k in keys:
            _os.environ[k] = "x"
        try:
            resp = self.client.post("/connectors/jira/test")
            self.assertEqual(resp.status_code, 200)
            # Jira has no live probe registered → still shows the env-only success.
            self.assertIn("All required env vars are set", resp.text)
            self.assertIn("deferred", resp.text)
        finally:
            for k, v in saved.items():
                _os.environ.pop(k, None)
                if v is not None:
                    _os.environ[k] = v

    def test_connector_test_endpoint_runs_live_probe_for_gmail(self):
        """Gmail has a registered probe — when env is set, the probe runs and
        its outcome (success here, monkey-patched to avoid network) renders."""
        import os as _os
        from services.control_panel import connector_probes as cp

        keys = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")
        saved_env = {k: _os.environ.pop(k, None) for k in keys}
        _os.environ["GMAIL_ADDRESS"] = "tester@gmail.com"
        _os.environ["GMAIL_APP_PASSWORD"] = "abcdabcdabcdabcd"
        original_probe = cp.PROBES["gmail"]
        cp.PROBES["gmail"] = lambda: cp.ProbeOutcome(
            ok=True, message="IMAP login succeeded for tester@gmail.com."
        )
        try:
            resp = self.client.post("/connectors/gmail/test")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Live connection succeeded", resp.text)
            self.assertIn("tester@gmail.com", resp.text)
        finally:
            cp.PROBES["gmail"] = original_probe
            for k, v in saved_env.items():
                _os.environ.pop(k, None)
                if v is not None:
                    _os.environ[k] = v

    def test_connector_test_endpoint_reports_live_probe_failure(self):
        import os as _os
        from services.control_panel import connector_probes as cp

        keys = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")
        saved_env = {k: _os.environ.pop(k, None) for k in keys}
        _os.environ["GMAIL_ADDRESS"] = "tester@gmail.com"
        _os.environ["GMAIL_APP_PASSWORD"] = "wrong"
        original_probe = cp.PROBES["gmail"]
        cp.PROBES["gmail"] = lambda: cp.ProbeOutcome(
            ok=False, message="IMAP login rejected: [AUTHENTICATIONFAILED] Invalid credentials"
        )
        try:
            resp = self.client.post("/connectors/gmail/test")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Live connection failed", resp.text)
            self.assertIn("AUTHENTICATIONFAILED", resp.text)
        finally:
            cp.PROBES["gmail"] = original_probe
            for k, v in saved_env.items():
                _os.environ.pop(k, None)
                if v is not None:
                    _os.environ[k] = v

    def test_connector_test_endpoint_runs_live_probe_for_github(self):
        import os as _os
        from services.control_panel import connector_probes as cp

        saved = _os.environ.pop("GITHUB_TOKEN", None)
        _os.environ["GITHUB_TOKEN"] = "ghp_fake_token"
        original_probe = cp.PROBES["github"]
        cp.PROBES["github"] = lambda: cp.ProbeOutcome(
            ok=True, message="GitHub /user authenticated as octocat."
        )
        try:
            resp = self.client.post("/connectors/github/test")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Live connection succeeded", resp.text)
            self.assertIn("octocat", resp.text)
        finally:
            cp.PROBES["github"] = original_probe
            _os.environ.pop("GITHUB_TOKEN", None)
            if saved is not None:
                _os.environ["GITHUB_TOKEN"] = saved

    def test_connector_test_endpoint_reports_github_bad_credentials(self):
        import os as _os
        from services.control_panel import connector_probes as cp

        saved = _os.environ.pop("GITHUB_TOKEN", None)
        _os.environ["GITHUB_TOKEN"] = "ghp_invalid"
        original_probe = cp.PROBES["github"]
        cp.PROBES["github"] = lambda: cp.ProbeOutcome(
            ok=False, message="GitHub /user returned HTTP 401: Bad credentials"
        )
        try:
            resp = self.client.post("/connectors/github/test")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Live connection failed", resp.text)
            self.assertIn("Bad credentials", resp.text)
        finally:
            cp.PROBES["github"] = original_probe
            _os.environ.pop("GITHUB_TOKEN", None)
            if saved is not None:
                _os.environ["GITHUB_TOKEN"] = saved

    def test_connector_test_endpoint_skips_probe_when_env_missing(self):
        """If env vars are missing, the route must NOT invoke the live probe
        (no point hitting the network when we know creds aren't configured)."""
        import os as _os
        from services.control_panel import connector_probes as cp

        keys = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")
        saved_env = {k: _os.environ.pop(k, None) for k in keys}
        original_probe = cp.PROBES["gmail"]
        called: list[bool] = []

        def _tripwire() -> cp.ProbeOutcome:
            called.append(True)
            return cp.ProbeOutcome(ok=False, message="should not be called")

        cp.PROBES["gmail"] = _tripwire
        try:
            resp = self.client.post("/connectors/gmail/test")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Missing env vars", resp.text)
            self.assertEqual(called, [], "live probe was called even though env was missing")
        finally:
            cp.PROBES["gmail"] = original_probe
            for k, v in saved_env.items():
                if v is not None:
                    _os.environ[k] = v

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
        self.assertRegex(resp.text, r"<code[^>]*>code-review</code>")
        self.assertIn("prompt", resp.text)

    def test_recipe_overview_active_tab(self):
        resp = self.client.get("/recipes/code-review")
        # Active tab marker is an `active` token in the className list on Overview.
        self.assertRegex(
            resp.text,
            r'href="/recipes/code-review"\s+class="[^"]*\bactive\b[^"]*"',
        )

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


class EnvWriterUnitTest(unittest.TestCase):
    """Direct unit tests for env_writer — no FastAPI involvement."""

    def setUp(self):
        import tempfile
        from pathlib import Path

        self.tmpdir = tempfile.mkdtemp(prefix="cp_env_test_")
        self.env_path = Path(self.tmpdir) / ".env"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_write_to_empty_creates_file(self):
        from services.control_panel.env_writer import update_env_file, read_env_values

        update_env_file(self.env_path, {"FOO": "bar", "BAZ": "qux"})
        values = read_env_values(self.env_path)
        self.assertEqual(values, {"FOO": "bar", "BAZ": "qux"})

    def test_update_preserves_unrelated_lines_and_comments(self):
        from services.control_panel.env_writer import update_env_file

        self.env_path.write_text(
            "# header comment\nFOO=old\n\n# section\nKEEP=intact\n",
            encoding="utf-8",
        )
        update_env_file(self.env_path, {"FOO": "new"})
        text = self.env_path.read_text(encoding="utf-8")
        self.assertIn("# header comment", text)
        self.assertIn("# section", text)
        self.assertIn("KEEP=intact", text)
        self.assertIn("FOO=new", text)
        self.assertNotIn("FOO=old", text)

    def test_quoting_of_values_with_whitespace_or_hash(self):
        from services.control_panel.env_writer import update_env_file, read_env_values

        update_env_file(self.env_path, {"WS": "has spaces", "HASH": "a#b", "PLAIN": "simple"})
        values = read_env_values(self.env_path)
        self.assertEqual(values["WS"], "has spaces")
        self.assertEqual(values["HASH"], "a#b")
        # Plain values aren't wrapped in quotes.
        text = self.env_path.read_text(encoding="utf-8")
        self.assertIn("PLAIN=simple\n", text)

    def test_filter_to_allowed_drops_unknown_keys(self):
        from services.control_panel.env_writer import filter_to_allowed

        filtered = filter_to_allowed(
            {"GOOD": "1", "BAD": "2", "ALSO_GOOD": "3"},
            allowed=["GOOD", "ALSO_GOOD"],
        )
        self.assertEqual(filtered, {"GOOD": "1", "ALSO_GOOD": "3"})


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class ConnectorEnvFlowTest(unittest.TestCase):
    """Round-trip test for the env editor route — writes through to a tmp .env."""

    def setUp(self):
        import os
        import tempfile
        from pathlib import Path
        from fastapi.testclient import TestClient

        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        # Point WORKSPACE_ROOT at a tmpdir that mirrors the real workspace's
        # connectors/ + recipes/, so we can test against a real fixture but
        # write to a sandboxed .env.
        real_root = Config.from_env().workspace_root
        self.tmpdir = tempfile.mkdtemp(prefix="cp_env_route_")
        root = Path(self.tmpdir)
        (root / "connectors").symlink_to(real_root / "connectors", target_is_directory=True)
        (root / "recipes").symlink_to(real_root / "recipes", target_is_directory=True)
        (root / "services").symlink_to(real_root / "services", target_is_directory=True)
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
        self._snapshot_env = os.environ.copy()
        self.client = TestClient(create_app(self.cfg))

    def tearDown(self):
        import os
        import shutil
        os.environ.clear()
        os.environ.update(self._snapshot_env)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_env_form_has_native_action_and_method_fallback(self):
        """If htmx fails to wire up (e.g. dynamically injected content not
        processed), the <form> must still POST natively to the right URL —
        otherwise the browser falls back to GET on the page URL and the
        password ends up in the access log. Regression guard for that."""
        resp = self.client.get("/connectors/gmail/env")
        self.assertEqual(resp.status_code, 200)
        self.assertRegex(
            resp.text,
            r'<form[^>]+action="/connectors/gmail/env"[^>]+method="post"',
        )

    def test_get_form_renders_with_disabled_inputs_for_unknown_host(self):
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        # Bind to a non-local host → form should render but inputs disabled.
        cfg = Config(**{**self.cfg.__dict__, "host": "0.0.0.0"})
        from fastapi.testclient import TestClient
        client = TestClient(create_app(cfg))
        resp = client.get("/connectors/jira/env")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Disabled:", resp.text)
        self.assertRegex(resp.text, r'<input[^>]*name="env__JIRA_BASE_URL"[^>]*\bdisabled\b')

    def test_post_writes_env_and_updates_process_environ(self):
        import os
        from services.control_panel.env_writer import read_env_values

        resp = self.client.post(
            "/connectors/jira/env",
            data={
                "env__JIRA_BASE_URL": "https://example.atlassian.net",
                "env__JIRA_EMAIL": "tester@example.com",
                "env__JIRA_API_TOKEN": "tok-secret-123",
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Saved 3 variables", resp.text)
        # File written.
        env_file = self.cfg.workspace_root / ".env"
        self.assertTrue(env_file.exists())
        values = read_env_values(env_file)
        self.assertEqual(values["JIRA_BASE_URL"], "https://example.atlassian.net")
        self.assertEqual(values["JIRA_EMAIL"], "tester@example.com")
        self.assertEqual(values["JIRA_API_TOKEN"], "tok-secret-123")
        # Process env updated so status pills refresh without restart.
        self.assertEqual(os.environ["JIRA_BASE_URL"], "https://example.atlassian.net")

    def test_post_ignores_keys_outside_requires_env(self):
        from services.control_panel.env_writer import read_env_values

        resp = self.client.post(
            "/connectors/jira/env",
            data={
                "env__JIRA_BASE_URL": "https://x.atlassian.net",
                "env__SOMETHING_ELSE": "should-not-write",
            },
        )
        self.assertEqual(resp.status_code, 200)
        env_file = self.cfg.workspace_root / ".env"
        values = read_env_values(env_file)
        self.assertIn("JIRA_BASE_URL", values)
        self.assertNotIn("SOMETHING_ELSE", values)

    def test_post_with_all_empty_inputs_is_a_noop(self):
        resp = self.client.post(
            "/connectors/jira/env",
            data={"env__JIRA_BASE_URL": "", "env__JIRA_EMAIL": "", "env__JIRA_API_TOKEN": ""},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Nothing to save", resp.text)
        # File not created — nothing was written.
        self.assertFalse((self.cfg.workspace_root / ".env").exists())


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


class ConnectorProbeUnitTest(unittest.TestCase):
    """Probe module is pure stdlib — exercise it without any FastAPI deps."""

    def test_gmail_probe_returns_failure_when_env_missing(self):
        import os as _os
        from services.control_panel.connector_probes import PROBES

        keys = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")
        saved = {k: _os.environ.pop(k, None) for k in keys}
        try:
            outcome = PROBES["gmail"]()
            self.assertFalse(outcome.ok)
            self.assertIn("GMAIL_ADDRESS", outcome.message)
        finally:
            for k, v in saved.items():
                if v is not None:
                    _os.environ[k] = v

    def test_run_probe_returns_none_for_unregistered(self):
        from services.control_panel.connector_probes import run_probe, has_probe

        self.assertFalse(has_probe("nonexistent-connector"))
        self.assertIsNone(run_probe("nonexistent-connector"))

    def test_has_probe_true_for_gmail(self):
        from services.control_panel.connector_probes import has_probe

        self.assertTrue(has_probe("gmail"))

    def test_has_probe_true_for_github(self):
        from services.control_panel.connector_probes import has_probe

        self.assertTrue(has_probe("github"))

    def test_github_probe_returns_failure_when_token_missing(self):
        import os as _os
        from services.control_panel.connector_probes import PROBES

        saved = _os.environ.pop("GITHUB_TOKEN", None)
        try:
            outcome = PROBES["github"]()
            self.assertFalse(outcome.ok)
            self.assertIn("GITHUB_TOKEN", outcome.message)
        finally:
            if saved is not None:
                _os.environ["GITHUB_TOKEN"] = saved


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiTest(unittest.TestCase):
    """`/api/v1/*` JSON routes consumed by the Next.js frontend."""

    @classmethod
    def setUpClass(cls):
        from fastapi.testclient import TestClient
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        cls.cfg = Config.from_env()
        cls.client = TestClient(create_app(cls.cfg))

    def test_dashboard_returns_recipes_and_connectors(self):
        resp = self.client.get("/api/v1/dashboard")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("recipes", data)
        self.assertIn("connectors", data)
        recipe_ids = {r["id"] for r in data["recipes"]}
        connector_ids = {c["id"] for c in data["connectors"]}
        self.assertIn("code-review", recipe_ids)
        self.assertIn("gmail", connector_ids)
        self.assertIn("github", connector_ids)
        # Recipes carry the fields the UI cards render.
        sample = next(r for r in data["recipes"] if r["id"] == "code-review")
        self.assertIn("name", sample)
        self.assertIn("execution_type", sample)

    def test_health_returns_array_of_status_objects(self):
        resp = self.client.get("/api/v1/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        names = {item["name"] for item in data}
        self.assertIn("llama-swap", names)
        self.assertIn("postgres", names)
        for item in data:
            self.assertIn("ok", item)
            self.assertIn("detail", item)

    def test_recipe_detail_returns_full_shape(self):
        resp = self.client.get("/api/v1/recipes/code-review")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["id"], "code-review")
        self.assertIn("rendered_body", data)
        self.assertIn("<", data["rendered_body"])
        self.assertIsInstance(data["inputs"], list)
        self.assertIsInstance(data["requires_skills"], list)
        self.assertIn("execution_type", data)

    def test_recipe_detail_404_for_unknown(self):
        resp = self.client.get("/api/v1/recipes/no-such-recipe")
        self.assertEqual(resp.status_code, 404)

    def test_connector_detail_returns_full_shape(self):
        resp = self.client.get("/api/v1/connectors/gmail")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["id"], "gmail")
        self.assertEqual(data["auth_type"], "basic")
        self.assertTrue(data["probe_registered"])
        env_names = {e["name"] for e in data["requires_env"]}
        self.assertEqual(env_names, {"GMAIL_ADDRESS", "GMAIL_APP_PASSWORD"})
        # rendered_body should be HTML, not raw markdown.
        self.assertIn("<", data["rendered_body"])

    def test_connector_detail_404_for_unknown(self):
        resp = self.client.get("/api/v1/connectors/no-such")
        self.assertEqual(resp.status_code, 404)

    def test_connector_test_json_returns_env_and_probe_outcome(self):
        import os as _os
        from services.control_panel import connector_probes as cp

        keys = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")
        saved = {k: _os.environ.pop(k, None) for k in keys}
        _os.environ["GMAIL_ADDRESS"] = "tester@gmail.com"
        _os.environ["GMAIL_APP_PASSWORD"] = "abcdabcdabcdabcd"
        original_probe = cp.PROBES["gmail"]
        cp.PROBES["gmail"] = lambda: cp.ProbeOutcome(ok=True, message="IMAP login succeeded for tester@gmail.com.")
        try:
            resp = self.client.post("/api/v1/connectors/gmail/test")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertTrue(data["env_check"]["all_present"])
            self.assertEqual(data["env_check"]["missing"], [])
            self.assertIsNotNone(data["probe"])
            self.assertTrue(data["probe"]["ok"])
            self.assertIn("tester@gmail.com", data["probe"]["message"])
            self.assertTrue(data["probe_registered"])
        finally:
            cp.PROBES["gmail"] = original_probe
            for k, v in saved.items():
                _os.environ.pop(k, None)
                if v is not None:
                    _os.environ[k] = v

    def test_connector_test_json_skips_probe_when_env_missing(self):
        import os as _os

        keys = ("GMAIL_ADDRESS", "GMAIL_APP_PASSWORD")
        saved = {k: _os.environ.pop(k, None) for k in keys}
        try:
            resp = self.client.post("/api/v1/connectors/gmail/test")
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertFalse(data["env_check"]["all_present"])
            self.assertEqual(set(data["env_check"]["missing"]), set(keys))
            self.assertIsNone(data["probe"])
        finally:
            for k, v in saved.items():
                if v is not None:
                    _os.environ[k] = v


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiEnvSaveTest(unittest.TestCase):
    """Round-trip the JSON env editor against a tmpdir-backed Config."""

    def setUp(self):
        import os
        import tempfile
        from pathlib import Path
        from fastapi.testclient import TestClient

        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        real_root = Config.from_env().workspace_root
        self.tmpdir = tempfile.mkdtemp(prefix="cp_api_env_")
        root = Path(self.tmpdir)
        (root / "connectors").symlink_to(real_root / "connectors", target_is_directory=True)
        (root / "recipes").symlink_to(real_root / "recipes", target_is_directory=True)
        (root / "services").symlink_to(real_root / "services", target_is_directory=True)
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
        self._snapshot_env = os.environ.copy()
        self.client = TestClient(create_app(self.cfg))

    def tearDown(self):
        import os
        import shutil
        os.environ.clear()
        os.environ.update(self._snapshot_env)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_post_env_writes_only_allowed_keys_and_returns_saved(self):
        from services.control_panel.env_writer import read_env_values

        resp = self.client.post(
            "/api/v1/connectors/gmail/env",
            json={
                "values": {
                    "GMAIL_ADDRESS": "tester@gmail.com",
                    "GMAIL_APP_PASSWORD": "abcdabcdabcdabcd",
                    "EVIL_KEY": "should-not-write",
                }
            },
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["ok"])
        self.assertEqual(set(data["saved_keys"]), {"GMAIL_ADDRESS", "GMAIL_APP_PASSWORD"})
        values = read_env_values(self.cfg.workspace_root / ".env")
        self.assertEqual(values["GMAIL_ADDRESS"], "tester@gmail.com")
        self.assertNotIn("EVIL_KEY", values)

    def test_post_env_empty_values_is_a_noop(self):
        resp = self.client.post(
            "/api/v1/connectors/gmail/env",
            json={"values": {"GMAIL_ADDRESS": "", "GMAIL_APP_PASSWORD": ""}},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["saved_keys"], [])
        self.assertFalse((self.cfg.workspace_root / ".env").exists())

    def test_post_env_rejected_for_non_local_bind(self):
        from fastapi.testclient import TestClient
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        cfg = Config(**{**self.cfg.__dict__, "host": "0.0.0.0"})
        client = TestClient(create_app(cfg))
        resp = client.post(
            "/api/v1/connectors/gmail/env",
            json={"values": {"GMAIL_ADDRESS": "tester@gmail.com"}},
        )
        self.assertEqual(resp.status_code, 403)


class DbUnitTest(unittest.TestCase):
    """Direct unit tests for the SQLite layer — no FastAPI needed."""

    def setUp(self):
        import tempfile
        from pathlib import Path
        from services.control_panel import db

        self.tmpdir = tempfile.mkdtemp(prefix="cp_db_")
        db.close()
        db.init(Path(self.tmpdir))

    def tearDown(self):
        import shutil
        from services.control_panel import db
        db.close()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_insert_then_finish_run_round_trip(self):
        from datetime import datetime, timezone
        from services.control_panel import db

        db.insert_run(
            run_id="abc123def456",
            recipe_id="code-review",
            model_ref="anthropic/claude-haiku-4-5",
            inputs={"target_branch": "main"},
            started_at=datetime(2026, 5, 9, 10, 0, tzinfo=timezone.utc),
        )
        row = db.get_run_row("abc123def456")
        self.assertIsNotNone(row)
        self.assertEqual(row.status, "running")
        self.assertEqual(row.inputs, {"target_branch": "main"})

        db.finish_run(run_id="abc123def456", status="done", output="hello world", error=None)
        row = db.get_run_row("abc123def456")
        self.assertEqual(row.status, "done")
        self.assertEqual(row.output, "hello world")
        self.assertIsNotNone(row.ended_at)

    def test_recent_runs_orders_by_started_desc_and_filters_by_recipe(self):
        from datetime import datetime, timezone, timedelta
        from services.control_panel import db

        base = datetime(2026, 5, 9, 10, 0, tzinfo=timezone.utc)
        for i, recipe in enumerate(["code-review", "daily-briefing", "code-review"]):
            db.insert_run(
                run_id=f"run{i:08x}",
                recipe_id=recipe,
                model_ref="x",
                inputs={},
                started_at=base + timedelta(minutes=i),
            )
        all_runs = db.recent_runs(limit=10)
        self.assertEqual([r.id for r in all_runs], ["run00000002", "run00000001", "run00000000"])
        cr = db.recent_runs(recipe_id="code-review")
        self.assertEqual([r.recipe_id for r in cr], ["code-review", "code-review"])

    def test_recipe_inputs_upsert_and_clear_on_empty(self):
        from services.control_panel import db

        db.save_recipe_inputs("code-review", {"target_branch": "main", "diff": "x"})
        self.assertEqual(
            db.get_recipe_inputs("code-review"),
            {"target_branch": "main", "diff": "x"},
        )
        # Updating one and clearing another.
        db.save_recipe_inputs("code-review", {"target_branch": "feat/y", "diff": ""})
        self.assertEqual(db.get_recipe_inputs("code-review"), {"target_branch": "feat/y"})

    def test_init_marks_orphaned_running_rows_as_abandoned(self):
        import tempfile
        from datetime import datetime, timezone
        from pathlib import Path
        from services.control_panel import db

        # Use a fresh tmpdir for this test so the abandonment runs once.
        db.close()
        d = tempfile.mkdtemp(prefix="cp_db_orphan_")
        db.init(Path(d))
        db.insert_run(
            run_id="orphan01",
            recipe_id="code-review",
            model_ref="x",
            inputs={},
            started_at=datetime.now(timezone.utc),
        )
        # Simulate a server restart by closing and re-initing.
        db.close()
        db.init(Path(d))
        row = db.get_run_row("orphan01")
        self.assertEqual(row.status, "abandoned")
        self.assertIsNotNone(row.ended_at)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiRunsTest(unittest.TestCase):
    """`/api/v1/runs*` and `/api/v1/recipes/{id}/last-inputs`."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        from pathlib import Path
        from datetime import datetime, timezone
        from fastapi.testclient import TestClient

        from services.control_panel import db
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        # Sandbox the DB by using a tmpdir as workspace_root, but symlink in
        # the real recipes/connectors so get_recipe still resolves.
        real_root = Config.from_env().workspace_root
        cls.tmpdir = tempfile.mkdtemp(prefix="cp_runs_api_")
        root = Path(cls.tmpdir)
        (root / "recipes").symlink_to(real_root / "recipes", target_is_directory=True)
        (root / "connectors").symlink_to(real_root / "connectors", target_is_directory=True)
        (root / "services").symlink_to(real_root / "services", target_is_directory=True)
        cls.cfg = Config(
            workspace_root=root,
            recipes_dir=root / "recipes",
            connectors_dir=root / "connectors",
            services_dir=root / "services",
            host="127.0.0.1", port=0, reload=False, llama_swap_url="",
        )
        cls.client = TestClient(create_app(cls.cfg))

        # Seed two runs directly via the db module so tests don't need to
        # actually invoke the dispatcher.
        db.insert_run(
            run_id="seedrun0001", recipe_id="code-review", model_ref="anthropic/claude-haiku-4-5",
            inputs={"target_branch": "main"},
            started_at=datetime(2026, 5, 9, 10, 0, tzinfo=timezone.utc),
        )
        db.finish_run(run_id="seedrun0001", status="done", output="seeded output", error=None)
        db.insert_run(
            run_id="seedrun0002", recipe_id="daily-briefing", model_ref="local/qwen2.5",
            inputs={"focus_project": "PROJ"},
            started_at=datetime(2026, 5, 9, 10, 5, tzinfo=timezone.utc),
        )
        db.finish_run(run_id="seedrun0002", status="error", output="", error="boom")

    @classmethod
    def tearDownClass(cls):
        import shutil
        from services.control_panel import db
        db.close()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def test_list_runs_returns_recent_first(self):
        resp = self.client.get("/api/v1/runs?limit=10")
        self.assertEqual(resp.status_code, 200)
        runs = resp.json()
        ids = [r["id"] for r in runs]
        self.assertEqual(ids[:2], ["seedrun0002", "seedrun0001"])
        first = next(r for r in runs if r["id"] == "seedrun0002")
        self.assertEqual(first["status"], "error")
        self.assertEqual(first["error"], "boom")

    def test_list_runs_filters_by_recipe(self):
        resp = self.client.get("/api/v1/runs?recipe_id=code-review")
        self.assertEqual(resp.status_code, 200)
        recipes = {r["recipe_id"] for r in resp.json()}
        self.assertEqual(recipes, {"code-review"})

    def test_get_run_returns_full_output_and_inputs(self):
        resp = self.client.get("/api/v1/runs/seedrun0001")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["output"], "seeded output")
        self.assertEqual(data["inputs"], {"target_branch": "main"})

    def test_get_run_404_for_unknown(self):
        resp = self.client.get("/api/v1/runs/nope")
        self.assertEqual(resp.status_code, 404)

    def test_last_inputs_round_trip(self):
        from services.control_panel import db
        db.save_recipe_inputs("code-review", {"target_branch": "feat/x", "diff": "..."})
        resp = self.client.get("/api/v1/recipes/code-review/last-inputs")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"target_branch": "feat/x", "diff": "..."})

    def test_last_inputs_404_for_unknown_recipe(self):
        resp = self.client.get("/api/v1/recipes/no-such/last-inputs")
        self.assertEqual(resp.status_code, 404)


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
        self.assertIn("gmail", ids)
        self.assertIn("github", ids)

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
