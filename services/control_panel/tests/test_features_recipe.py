"""Unit tests for the Tier-3 recipe handler.

Fake runner substitutes for the sync scripts; tests verify status mapping
and uninstall semantics against a tempdir-shaped workspace.
"""
from __future__ import annotations

import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path

_HAS_YAML = importlib.util.find_spec("yaml") is not None


def _make_runner(success=True, output=""):
    calls = []

    def _runner(argv):
        calls.append(list(argv))
        return output, (0 if success else 1)

    _runner.calls = calls  # type: ignore[attr-defined]
    return _runner


def _write_recipe(root: Path, recipe_id: str, body_extra: str = "") -> Path:
    """Drop a minimal but valid recipe at recipes/<id>.md."""
    p = root / "recipes" / f"{recipe_id}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(f"""\
        ---
        id: {recipe_id}
        name: Test {recipe_id}
        description: test
        audience: tech
        status: experimental
        tags: []
        requires_skills: []
        requires_workflows: []
        requires_connectors: []
        requires_mcp: []
        requires_env: []
        execution:
          type: prompt
          model: local/test
        ---
        {body_extra}
        """))
    return p


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class RecipeHandlerTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        _write_recipe(self.root, "smoke")
        _write_recipe(self.root, "code-review")
        # The sync scripts paths just need to be importable as files; not invoked.
        (self.root / "scripts").mkdir(exist_ok=True)
        (self.root / "scripts" / "sync_claude_code.py").write_text("# stub")
        (self.root / "scripts" / "sync_antigravity.py").write_text("# stub")

    def _handler(self, runner=None):
        from services.control_panel.features.recipe import RecipeFeatureHandler

        return RecipeFeatureHandler(workspace_root=self.root, runner=runner or _make_runner())

    def _activate(self, recipe_id: str, claude=True, agents=True):
        if claude:
            (self.root / ".claude" / "commands").mkdir(parents=True, exist_ok=True)
            (self.root / ".claude" / "commands" / f"{recipe_id}.md").write_text("# synced")
        if agents:
            (self.root / ".agents" / "workflows").mkdir(parents=True, exist_ok=True)
            (self.root / ".agents" / "workflows" / f"{recipe_id}.md").write_text("# synced")

    def test_list_returns_all_recipes(self):
        ids = {f.id for f in self._handler().list()}
        self.assertEqual(ids, {"smoke", "code-review"})

    def test_unsynced_recipe_is_available(self):
        from services.control_panel.features import FeatureStatus

        f = self._handler().get("smoke")
        self.assertEqual(f.status, FeatureStatus.AVAILABLE)
        self.assertFalse(f.detail["in_claude"])
        self.assertFalse(f.detail["in_agents"])

    def test_both_provider_files_present_is_installed(self):
        from services.control_panel.features import FeatureStatus

        self._activate("smoke")
        f = self._handler().get("smoke")
        self.assertEqual(f.status, FeatureStatus.INSTALLED)

    def test_one_provider_file_is_partial(self):
        from services.control_panel.features import FeatureStatus

        self._activate("smoke", agents=False)
        f = self._handler().get("smoke")
        self.assertEqual(f.status, FeatureStatus.PARTIAL)

    def test_install_runs_both_sync_scripts(self):
        # Pre-create provider files so the post-install build sees INSTALLED;
        # the runner is a stub that doesn't actually do the writes.
        self._activate("smoke")
        runner = _make_runner()
        result = self._handler(runner).install("smoke")
        self.assertTrue(result["ok"])
        # Both sync scripts invoked.
        names = [c[1].split("/")[-1] for c in runner.calls if "python3" in c[0]]
        self.assertEqual(sorted(names), ["sync_antigravity.py", "sync_claude_code.py"])

    def test_install_surfaces_sync_failure(self):
        runner = _make_runner(success=False, output="boom")
        result = self._handler(runner).install("smoke")
        self.assertFalse(result["ok"])
        self.assertIn("failed", result["error"])

    def test_install_unknown_recipe_errors(self):
        result = self._handler().install("does-not-exist")
        self.assertFalse(result["ok"])
        self.assertIn("no recipe", result["error"])

    def test_uninstall_removes_provider_files(self):
        from services.control_panel.features import FeatureStatus

        self._activate("smoke")
        result = self._handler().uninstall("smoke")
        self.assertTrue(result["ok"])
        self.assertFalse(result.get("noop"))
        self.assertFalse((self.root / ".claude" / "commands" / "smoke.md").exists())
        self.assertFalse((self.root / ".agents" / "workflows" / "smoke.md").exists())
        # Source preserved.
        self.assertTrue((self.root / "recipes" / "smoke.md").exists())
        # New status is AVAILABLE (deactivated).
        self.assertEqual(result["feature"]["status"], FeatureStatus.AVAILABLE.value)

    def test_uninstall_noop_when_already_deactivated(self):
        result = self._handler().uninstall("smoke")
        self.assertTrue(result["ok"])
        self.assertTrue(result["noop"])

    def test_uninstall_unknown_recipe_errors(self):
        result = self._handler().uninstall("does-not-exist")
        self.assertFalse(result["ok"])

    def test_unparseable_recipe_is_error(self):
        from services.control_panel.features import FeatureStatus

        (self.root / "recipes" / "bad.md").write_text("---\nnot: [valid: yaml: at: all\n---\n")
        # bad.md has no parseable id, so it's silently skipped — verify list ignores it.
        ids = {f.id for f in self._handler().list()}
        self.assertNotIn("bad", ids)

    def test_partial_yaml_recipe_with_id_only_keeps_running(self):
        """A recipe with id: but no other fields shouldn't crash the handler."""
        (self.root / "recipes" / "minimal.md").write_text("---\nid: minimal\n---\n")
        feat = self._handler().get("minimal")
        self.assertIsNotNone(feat)
        # No name in fm → name falls back to id.
        self.assertEqual(feat.name, "minimal")

    def test_requires_passed_through_to_detail(self):
        recipe = _write_recipe(self.root, "wired")
        # Append requires fields by rewriting the file.
        recipe.write_text(textwrap.dedent("""\
            ---
            id: wired
            name: Wired
            description: connected
            audience: tech
            status: experimental
            tags: []
            requires_skills: [skill-a, skill-b]
            requires_workflows: []
            requires_connectors: [jira]
            requires_mcp: [memory]
            requires_env: [JIRA_API_TOKEN]
            execution:
              type: agent
              model: anthropic/claude-haiku-4-5-20251001
            ---
            """))
        f = self._handler().get("wired")
        self.assertEqual(f.detail["requires_skills"], ["skill-a", "skill-b"])
        self.assertEqual(f.detail["requires_connectors"], ["jira"])
        self.assertEqual(f.detail["requires_mcp"], ["memory"])
        self.assertEqual(f.detail["execution_type"], "agent")

    def test_verify_succeeds_when_installed(self):
        self._activate("smoke")
        result = self._handler().verify("smoke")
        self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
