"""Smoke tests for the control panel.

Skips entirely when the UI deps (FastAPI, Jinja2) aren't installed, so this
test suite is safe to register in validate.py against a checkout that hasn't
run `pip install -r services/control_panel/requirements.txt` yet.
"""
from __future__ import annotations

import importlib.util
import unittest

_HAS_FASTAPI = all(importlib.util.find_spec(m) is not None for m in ("fastapi", "jinja2"))


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

    def test_schema_init_idempotent(self):
        from pathlib import Path
        from services.control_panel import db
        # It's already inited in setUp
        db.init(Path(self.tmpdir)) # Call again
        db.init(Path(self.tmpdir)) # Call a third time
        # Should not raise any operational errors about duplicate columns.


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


def _sandbox_cfg(tmpdir: str):
    """Build a Config rooted in a tmpdir that symlinks to the real recipes/
    connectors so get_recipe still resolves while the SQLite DB stays
    isolated under <tmpdir>/.cache/."""
    from pathlib import Path
    from services.control_panel.config import Config

    real_root = Config.from_env().workspace_root
    root = Path(tmpdir)
    (root / "recipes").symlink_to(real_root / "recipes", target_is_directory=True)
    (root / "connectors").symlink_to(real_root / "connectors", target_is_directory=True)
    (root / "services").symlink_to(real_root / "services", target_is_directory=True)
    return Config(
        workspace_root=root,
        recipes_dir=root / "recipes",
        connectors_dir=root / "connectors",
        services_dir=root / "services",
        host="127.0.0.1", port=0, reload=False, llama_swap_url="",
    )


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiRoutinesTest(unittest.TestCase):
    """`/api/v1/routines` CRUD + scheduler sync."""

    def setUp(self):
        import tempfile
        from fastapi.testclient import TestClient
        from services.control_panel import scheduler
        from services.control_panel.app import create_app

        self.tmpdir = tempfile.mkdtemp(prefix="cp_routines_")
        self.cfg = _sandbox_cfg(self.tmpdir)
        # create_app calls db.init + scheduler.init.
        self.client = TestClient(create_app(self.cfg))
        self._scheduler = scheduler

    def tearDown(self):
        import shutil
        from services.control_panel import db, scheduler
        scheduler.shutdown()
        db.close()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_create_lists_and_deletes_routine(self):
        # Create.
        resp = self.client.post(
            "/api/v1/routines",
            json={
                "recipe_id": "code-review",
                "schedule": "0 8 * * *",
                "model_ref": "anthropic/claude-haiku-4-5-20251001",
                "inputs": {"target_branch": "main"},
                "enabled": True,
            },
        )
        self.assertEqual(resp.status_code, 200)
        routine_id = resp.json()["id"]
        self.assertTrue(routine_id)

        # Scheduler picked it up.
        self.assertIsNotNone(self._scheduler._scheduler.get_job(routine_id))

        # List.
        listed = self.client.get("/api/v1/routines").json()
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["id"], routine_id)
        self.assertEqual(listed[0]["recipe_id"], "code-review")
        self.assertTrue(listed[0]["enabled"])
        self.assertEqual(listed[0]["inputs"], {"target_branch": "main"})

        # Delete.
        resp = self.client.delete(f"/api/v1/routines/{routine_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["ok"])
        # Scheduler dropped the job.
        self.assertIsNone(self._scheduler._scheduler.get_job(routine_id))
        # DB row gone.
        self.assertEqual(self.client.get("/api/v1/routines").json(), [])

    def test_update_via_post_with_existing_id_does_not_duplicate(self):
        first = self.client.post(
            "/api/v1/routines",
            json={"recipe_id": "code-review", "schedule": "0 8 * * *", "enabled": True},
        ).json()
        rid = first["id"]
        # POST again with same id but different schedule + enabled=False.
        second = self.client.post(
            "/api/v1/routines",
            json={"id": rid, "recipe_id": "code-review", "schedule": "*/15 * * * *", "enabled": False},
        )
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.json()["id"], rid)

        listed = self.client.get("/api/v1/routines").json()
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["schedule"], "*/15 * * * *")
        self.assertFalse(listed[0]["enabled"])
        # Disabled routine should have no scheduled job.
        self.assertIsNone(self._scheduler._scheduler.get_job(rid))

    def test_invalid_cron_returns_400(self):
        resp = self.client.post(
            "/api/v1/routines",
            json={"recipe_id": "code-review", "schedule": "not-a-cron"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("cron", resp.json()["detail"].lower())

    def test_unknown_recipe_returns_400(self):
        resp = self.client.post(
            "/api/v1/routines",
            json={"recipe_id": "no-such-recipe", "schedule": "0 8 * * *"},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("recipe not found", resp.json()["detail"])

    def test_missing_required_fields_returns_400(self):
        # No recipe_id.
        r1 = self.client.post("/api/v1/routines", json={"schedule": "0 8 * * *"})
        self.assertEqual(r1.status_code, 400)
        # No schedule.
        r2 = self.client.post("/api/v1/routines", json={"recipe_id": "code-review"})
        self.assertEqual(r2.status_code, 400)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiRecipeRunTest(unittest.TestCase):
    """`POST /api/v1/recipes/{id}/run` — start a run via JSON, dispatcher mocked."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        from fastapi.testclient import TestClient
        from services.control_panel import runs as runs_mod, db, scheduler
        from services.control_panel.app import create_app

        cls.tmpdir = tempfile.mkdtemp(prefix="cp_jsonrun_")
        cls.cfg = _sandbox_cfg(cls.tmpdir)

        # Replace start_run with a deterministic fake. The api route imports
        # start_run inside the handler (`from .runs import start_run`) so we
        # patch at the module level only.
        cls._original_start = runs_mod.start_run

        def fake_start(cfg, recipe_id, fm, body, inputs, model_ref):
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
            db.insert_run(
                run_id=r.id, recipe_id=recipe_id, model_ref=r.model_ref,
                inputs=dict(inputs), started_at=r.started_at,
            )
            with _runs_lock:
                _runs[r.id] = r

            def worker():
                try:
                    sink = _ChunkSink(r)
                    sink.write("hello ")
                    sink.write("world")
                    r.status = "done"
                    db.finish_run(run_id=r.id, status="done", output=r.output, error=None)
                finally:
                    r._queue.put(None)
                    r._done.set()

            threading.Thread(target=worker, daemon=True).start()
            return r

        runs_mod.start_run = fake_start
        cls._fake_start = fake_start

        cls.client = TestClient(create_app(cls.cfg))
        cls._scheduler = scheduler

    @classmethod
    def tearDownClass(cls):
        import shutil
        from services.control_panel import runs as runs_mod, db, scheduler
        runs_mod.start_run = cls._original_start
        scheduler.shutdown()
        db.close()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def test_post_run_returns_run_id_and_persists(self):
        resp = self.client.post(
            "/api/v1/recipes/code-review/run",
            json={"model_ref": "anthropic/claude-haiku-4-5-20251001",
                  "inputs": {"target_branch": "main"}},
        )
        self.assertEqual(resp.status_code, 200)
        run_id = resp.json()["id"]
        self.assertRegex(run_id, r"^[a-f0-9]{12}$")

        # Wait for the worker, then fetch via JSON.
        from services.control_panel.runs import get_run
        run = get_run(run_id)
        self.assertIsNotNone(run)
        run._done.wait(timeout=5)

        detail = self.client.get(f"/api/v1/runs/{run_id}").json()
        self.assertEqual(detail["status"], "done")
        self.assertIn("hello", detail["output"])
        self.assertEqual(detail["inputs"], {"target_branch": "main"})

    def test_post_run_with_unknown_recipe_404(self):
        resp = self.client.post(
            "/api/v1/recipes/no-such-recipe/run",
            json={"model_ref": "x", "inputs": {}},
        )
        self.assertEqual(resp.status_code, 404)

    def test_post_run_with_non_dict_inputs_400(self):
        resp = self.client.post(
            "/api/v1/recipes/code-review/run",
            json={"model_ref": "x", "inputs": ["not", "a", "dict"]},
        )
        self.assertEqual(resp.status_code, 400)


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiRecipeWriteTest(unittest.TestCase):
    """`POST /api/v1/recipes/new` and `/api/v1/recipes/{id}/edit`."""

    def setUp(self):
        import tempfile
        from pathlib import Path
        from fastapi.testclient import TestClient
        from services.control_panel import recipe_writer
        from services.control_panel.app import create_app
        from services.control_panel.config import Config

        # Self-contained sandbox — no symlink to real recipes/, so writes
        # don't touch the workspace.
        self.tmpdir = tempfile.mkdtemp(prefix="cp_recipewrite_")
        root = Path(self.tmpdir)
        (root / "recipes").mkdir()
        (root / "connectors").mkdir()
        (root / "services").mkdir()
        (root / "scripts").mkdir()
        self.cfg = Config(
            workspace_root=root,
            recipes_dir=root / "recipes",
            connectors_dir=root / "connectors",
            services_dir=root / "services",
            host="127.0.0.1", port=0, reload=False, llama_swap_url="",
        )
        self._orig_audit = recipe_writer._audit_recipe
        recipe_writer._audit_recipe = lambda cfg, recipe_id: []
        self.client = TestClient(create_app(self.cfg))

    def tearDown(self):
        import shutil
        from services.control_panel import db, scheduler, recipe_writer
        recipe_writer._audit_recipe = self._orig_audit
        scheduler.shutdown()
        db.close()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_post_new_creates_recipe_file(self):
        resp = self.client.post(
            "/api/v1/recipes/new",
            json={"id": "fresh", "name": "Fresh", "description": "A freshly minted recipe.",
                  "audience": "tech", "execution_type": "prompt", "tags": "demo, json"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["id"], "fresh")
        path = self.cfg.recipes_dir / "fresh.md"
        self.assertTrue(path.exists())
        body = path.read_text(encoding="utf-8")
        self.assertIn("id: fresh", body)
        self.assertIn("- demo", body)

    def test_post_new_rejects_duplicate_id(self):
        first = self.client.post(
            "/api/v1/recipes/new",
            json={"id": "dupe", "name": "x", "description": "x",
                  "audience": "tech", "execution_type": "prompt"},
        )
        self.assertEqual(first.status_code, 200)
        second = self.client.post(
            "/api/v1/recipes/new",
            json={"id": "dupe", "name": "y", "description": "y",
                  "audience": "tech", "execution_type": "prompt"},
        )
        self.assertEqual(second.status_code, 400)
        self.assertIn("already exists", second.json()["detail"])

    def test_post_new_rejects_invalid_execution_type(self):
        resp = self.client.post(
            "/api/v1/recipes/new",
            json={"id": "bad-exec", "execution_type": "freeform"},
        )
        self.assertEqual(resp.status_code, 400)

    def test_post_edit_round_trip(self):
        # Seed a minimal recipe.
        path = self.cfg.recipes_dir / "demo.md"
        path.write_text(
            "---\nid: demo\nname: Demo\ndescription: x\naudience: tech\nversion: 0.1.0\n"
            "status: experimental\ntags: []\nrequires_skills: []\nrequires_workflows: []\n"
            "requires_connectors: []\nrequires_mcp: []\nrequires_env: []\n"
            "execution:\n  type: prompt\n---\n## Prompt\n\nhello\n",
            encoding="utf-8",
        )
        new_body = path.read_text(encoding="utf-8").replace("hello", "hello world")
        resp = self.client.post(
            "/api/v1/recipes/demo/edit",
            json={"content": new_body},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["ok"])
        self.assertIn("hello world", path.read_text(encoding="utf-8"))

    def test_post_edit_404_for_unknown(self):
        resp = self.client.post(
            "/api/v1/recipes/no-such/edit",
            json={"content": "x"},
        )
        self.assertEqual(resp.status_code, 404)


class TestDispatchWorkflow(unittest.TestCase):
    def test_dispatch_workflow_sync(self):
        from services.recipe_runtime.dispatcher import dispatch_workflow
        from unittest.mock import patch, MagicMock
        import json

        fm = {"execution": {"type": "workflow", "entrypoint": "n8n-workflows/daily-briefing.n8n"}}
        inputs = {"focus_project": "PROJ"}

        with patch.dict("os.environ", {"N8N_WEBHOOK_BASE": "http://test-base", "N8N_API_KEY": "test-key"}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_resp = MagicMock()
                mock_resp.read.return_value = b"sync-output"
                mock_urlopen.return_value.__enter__.return_value = mock_resp

                result = dispatch_workflow(fm, inputs)

                self.assertEqual(result, "sync-output")
                mock_urlopen.assert_called_once()
                req = mock_urlopen.call_args[0][0]
                self.assertEqual(req.full_url, "http://test-base/webhook/daily-briefing")
                self.assertEqual(req.get_header("Authorization"), "Bearer test-key")

                payload = json.loads(req.data.decode("utf-8"))
                self.assertEqual(payload["inputs"], {"focus_project": "PROJ"})


@unittest.skipUnless(_HAS_FASTAPI, "fastapi/jinja2 not installed")
class JsonApiN8nCallbackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile
        from fastapi.testclient import TestClient
        from services.control_panel.app import create_app

        cls.tmpdir = tempfile.mkdtemp(prefix="cp_n8n_")
        cls.cfg = _sandbox_cfg(cls.tmpdir)
        # client=("127.0.0.1", ...) so request.client.host matches the localhost
        # check in /api/v1/n8n/callback (TestClient defaults to "testclient").
        cls.client = TestClient(create_app(cls.cfg), client=("127.0.0.1", 50000))

    @classmethod
    def tearDownClass(cls):
        import shutil
        from services.control_panel import db, scheduler
        scheduler.shutdown()
        db.close()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def _seed_running_run(self, run_id: str) -> None:
        from services.control_panel import db
        from datetime import datetime, timezone
        db.insert_run(
            run_id=run_id,
            recipe_id="daily-briefing",
            model_ref="x",
            inputs={},
            started_at=datetime.now(timezone.utc),
        )

    def test_callback_updates_run(self):
        from services.control_panel import db
        run_id = "test-n8n-callback"
        self._seed_running_run(run_id)

        resp = self.client.post(
            f"/api/v1/n8n/callback/{run_id}",
            json={"output": "hello from n8n"},
        )
        self.assertEqual(resp.status_code, 200)

        run_row = db.get_run_row(run_id)
        self.assertEqual(run_row.status, "done")
        self.assertEqual(run_row.output, "hello from n8n")

    def test_callback_idempotent_on_retry(self):
        """A retried callback must NOT overwrite the finalized run."""
        from services.control_panel import db
        run_id = "test-n8n-retry"
        self._seed_running_run(run_id)

        first = self.client.post(
            f"/api/v1/n8n/callback/{run_id}",
            json={"output": "first"},
        )
        self.assertEqual(first.status_code, 200)
        self.assertFalse(first.json().get("noop"))

        second = self.client.post(
            f"/api/v1/n8n/callback/{run_id}",
            json={"output": "second-should-be-ignored"},
        )
        self.assertEqual(second.status_code, 200)
        self.assertTrue(second.json().get("noop"))

        row = db.get_run_row(run_id)
        self.assertEqual(row.output, "first")

    def test_callback_404_for_unknown_run(self):
        resp = self.client.post(
            "/api/v1/n8n/callback/does-not-exist",
            json={"output": "x"},
        )
        self.assertEqual(resp.status_code, 404)

    def test_callback_rejects_non_localhost_client(self):
        """Request from a non-loopback peer must be rejected before any DB work."""
        from fastapi.testclient import TestClient
        from services.control_panel.app import create_app

        run_id = "test-n8n-non-local"
        self._seed_running_run(run_id)
        # Spoof the Host header to "127.0.0.1" — the old (broken) check trusted
        # this. With the fix, the peer IP is what matters; this should 403.
        # 8.8.8.8 is a real public address (Python's ipaddress flags some
        # documentation ranges like 203.0.113.0/24 as is_private — avoid those).
        remote_client = TestClient(create_app(self.cfg), client=("8.8.8.8", 12345))
        resp = remote_client.post(
            f"/api/v1/n8n/callback/{run_id}",
            json={"output": "should-not-apply"},
            headers={"Host": "127.0.0.1"},
        )
        self.assertEqual(resp.status_code, 403)

        from services.control_panel import db
        row = db.get_run_row(run_id)
        self.assertEqual(row.status, "running")
        self.assertEqual(row.output, "")


if __name__ == "__main__":
    unittest.main()
