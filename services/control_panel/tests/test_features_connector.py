"""Unit tests for the Tier-3 connector handler.

Uses a tempdir workspace with a synthetic registry + connector .md files +
.env file — no env_writer mocking needed since update_env_file is the right
primitive to exercise here.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import textwrap
import unittest
from pathlib import Path

_HAS_YAML = importlib.util.find_spec("yaml") is not None


def _connector_md(requires_env: list[str]) -> str:
    env_yaml = "\n".join(f"  - {v}" for v in requires_env) or "  []"
    return textwrap.dedent(f"""\
        ---
        id: x
        name: X
        description: a connector
        status: experimental
        requires_env:
{env_yaml if requires_env else "        []"}
        tags: []
        ---
        body
        """)


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class ConnectorHandlerTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "connectors").mkdir()
        # Two connectors: jira shares POSTGRES_PASSWORD with bitbucket (synthetic
        # for the reverse-dep test).
        registry = {
            "connectors": [
                {"id": "jira", "name": "Jira", "description": "tickets", "path": "connectors/jira.md", "status": "experimental", "tags": []},
                {"id": "bitbucket", "name": "Bitbucket", "description": "code", "path": "connectors/bitbucket.md", "status": "experimental", "tags": []},
                {"id": "n8n", "name": "n8n", "description": "workflows", "path": "connectors/n8n.md", "status": "experimental", "tags": []},
            ]
        }
        (self.root / "connectors" / "registry.json").write_text(json.dumps(registry))
        (self.root / "connectors" / "jira.md").write_text(textwrap.dedent("""\
            ---
            id: jira
            name: Jira
            description: tickets
            requires_env:
              - JIRA_BASE_URL
              - JIRA_API_TOKEN
            ---
            """))
        (self.root / "connectors" / "bitbucket.md").write_text(textwrap.dedent("""\
            ---
            id: bitbucket
            name: Bitbucket
            description: code
            requires_env:
              - BITBUCKET_BASE_URL
              - BITBUCKET_API_TOKEN
              - JIRA_API_TOKEN
            ---
            """))
        (self.root / "connectors" / "n8n.md").write_text(textwrap.dedent("""\
            ---
            id: n8n
            name: n8n
            description: workflows
            requires_env:
              - N8N_WEBHOOK_BASE
            ---
            """))

    def _write_env(self, values: dict[str, str]):
        text = "\n".join(f"{k}={v}" for k, v in values.items()) + "\n"
        (self.root / ".env").write_text(text)

    def _handler(self):
        from services.control_panel.features.connector import ConnectorFeatureHandler

        return ConnectorFeatureHandler(workspace_root=self.root)

    def test_list_returns_all_registry_entries(self):
        ids = {f.id for f in self._handler().list()}
        self.assertEqual(ids, {"jira", "bitbucket", "n8n"})

    def test_no_env_set_is_available(self):
        from services.control_panel.features import FeatureStatus

        f = self._handler().get("jira")
        self.assertEqual(f.status, FeatureStatus.AVAILABLE)
        self.assertEqual(f.detail["env_missing"], ["JIRA_BASE_URL", "JIRA_API_TOKEN"])

    def test_all_env_set_is_installed(self):
        from services.control_panel.features import FeatureStatus

        self._write_env({"JIRA_BASE_URL": "https://x", "JIRA_API_TOKEN": "t"})
        f = self._handler().get("jira")
        self.assertEqual(f.status, FeatureStatus.INSTALLED)
        self.assertEqual(f.detail["env_missing"], [])

    def test_some_env_set_is_partial(self):
        from services.control_panel.features import FeatureStatus

        self._write_env({"JIRA_BASE_URL": "https://x"})
        f = self._handler().get("jira")
        self.assertEqual(f.status, FeatureStatus.PARTIAL)

    def test_install_writes_supplied_env_to_dotenv(self):
        result = self._handler().install(
            "jira", inputs={"env": {"JIRA_BASE_URL": "https://x", "JIRA_API_TOKEN": "secret"}}
        )
        self.assertTrue(result["ok"])
        text = (self.root / ".env").read_text()
        self.assertIn("JIRA_BASE_URL=", text)
        self.assertIn("JIRA_API_TOKEN=", text)
        # Secret value is now in .env (where it should be); response does NOT echo it.
        self.assertNotIn("secret", json.dumps(result))

    def test_install_rejects_unknown_keys(self):
        result = self._handler().install(
            "jira", inputs={"env": {"NOT_IN_REQUIRES": "x"}}
        )
        self.assertFalse(result["ok"])
        self.assertIn("NOT_IN_REQUIRES", result["rejected"])
        # .env never written.
        self.assertFalse((self.root / ".env").exists())

    def test_install_filters_unknown_when_mixed(self):
        result = self._handler().install(
            "jira",
            inputs={"env": {"JIRA_BASE_URL": "https://x", "JUNK": "1"}},
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["wrote_keys"], ["JIRA_BASE_URL"])
        self.assertEqual(result["rejected"], ["JUNK"])

    def test_install_empty_value_treated_as_unset(self):
        result = self._handler().install(
            "jira", inputs={"env": {"JIRA_BASE_URL": ""}}
        )
        # ok=True but nothing was actually written — empty values are dropped.
        self.assertTrue(result["ok"])
        self.assertEqual(result["wrote_keys"], [])
        self.assertFalse((self.root / ".env").exists())

    def test_uninstall_clears_unshared_vars(self):
        self._write_env({"JIRA_BASE_URL": "x", "JIRA_API_TOKEN": "y", "BITBUCKET_BASE_URL": "z"})
        # Bitbucket NOT installed (only BITBUCKET_BASE_URL set, missing _API_TOKEN)
        result = self._handler().uninstall("jira")
        self.assertTrue(result["ok"])
        # JIRA_API_TOKEN is referenced by bitbucket but bitbucket isn't installed
        # → not protected → cleared.
        self.assertEqual(set(result["cleared"]), {"JIRA_BASE_URL", "JIRA_API_TOKEN"})

    def test_uninstall_protects_vars_shared_with_installed_connector(self):
        # Both jira and bitbucket fully installed; JIRA_API_TOKEN is shared.
        self._write_env({
            "JIRA_BASE_URL": "x",
            "JIRA_API_TOKEN": "y",
            "BITBUCKET_BASE_URL": "z",
            "BITBUCKET_API_TOKEN": "w",
        })
        result = self._handler().uninstall("jira")
        self.assertTrue(result["ok"])
        self.assertIn("JIRA_API_TOKEN", result["kept_shared"])
        self.assertIn("JIRA_BASE_URL", result["cleared"])
        # The shared var must remain in .env.
        text = (self.root / ".env").read_text()
        self.assertIn("JIRA_API_TOKEN=y", text)

    def test_uninstall_noop_when_no_env_file(self):
        result = self._handler().uninstall("n8n")
        self.assertTrue(result["ok"])
        self.assertEqual(result["cleared"], [])

    def test_unknown_connector_id_errors(self):
        h = self._handler()
        self.assertIsNone(h.get("does-not-exist"))
        self.assertFalse(h.install("does-not-exist")["ok"])
        self.assertFalse(h.uninstall("does-not-exist")["ok"])
        self.assertFalse(h.verify("does-not-exist")["ok"])

    def test_install_unknown_connector_does_not_touch_env(self):
        self._handler().install("does-not-exist", inputs={"env": {"X": "y"}})
        self.assertFalse((self.root / ".env").exists())

    def test_verify_passes_when_all_env_present(self):
        self._write_env({"JIRA_BASE_URL": "x", "JIRA_API_TOKEN": "y"})
        result = self._handler().verify("jira")
        self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
