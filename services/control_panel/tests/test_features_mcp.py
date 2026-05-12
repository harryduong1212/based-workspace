"""Unit tests for the Tier-3 MCP feature handler.

A fake `spawn_probe` substitutes for the real spawn-and-list_tools smoke,
so tests don't need MCP server binaries on PATH.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

_HAS_YAML = importlib.util.find_spec("yaml") is not None


def _good_probe(server_id, config):
    del server_id, config
    return True, ""


def _bad_probe(server_id, config):
    del config
    return False, f"could not spawn {server_id}"


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class MCPHandlerTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / ".mcp.json.example").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "memory": {
                            "command": "./scripts/with-env.sh",
                            "args": ["python3", "-m", "services.memory_mcp"],
                        },
                        "notebooklm": {
                            "command": "/usr/local/bin/notebooklm-mcp",
                            "args": [],
                        },
                    }
                }
            )
        )

    def _handler(self, probe=_good_probe):
        from services.control_panel.features.mcp import MCPFeatureHandler

        return MCPFeatureHandler(workspace_root=self.root, spawn_probe=probe)

    def test_list_lists_example_and_installed(self):
        # Example has two; installed has one extra.
        (self.root / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"memory": {"command": "x"}, "extra": {"command": "y"}}})
        )
        features = self._handler().list()
        self.assertEqual({f.id for f in features}, {"memory", "notebooklm", "extra"})

    def test_only_example_is_available(self):
        from services.control_panel.features import FeatureStatus

        f = self._handler().get("memory")
        self.assertEqual(f.status, FeatureStatus.AVAILABLE)
        self.assertFalse(f.detail["in_installed"])

    def test_installed_with_passing_probe_is_installed(self):
        from services.control_panel.features import FeatureStatus

        (self.root / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"memory": {"command": "x"}}})
        )
        f = self._handler(_good_probe).get("memory")
        self.assertEqual(f.status, FeatureStatus.INSTALLED)

    def test_installed_with_failing_probe_is_partial(self):
        from services.control_panel.features import FeatureStatus

        (self.root / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"memory": {"command": "x"}}})
        )
        f = self._handler(_bad_probe).get("memory")
        self.assertEqual(f.status, FeatureStatus.PARTIAL)
        self.assertIn("could not spawn", f.detail["probe_error"])

    def test_install_copies_from_example_and_creates_mcp_json(self):
        result = self._handler().install("memory")
        self.assertTrue(result["ok"])
        doc = json.loads((self.root / ".mcp.json").read_text())
        self.assertIn("memory", doc["mcpServers"])
        # cwd should be absolute (resolved to workspace_root).
        self.assertEqual(doc["mcpServers"]["memory"]["cwd"], str(self.root.resolve()))

    def test_install_preserves_other_existing_entries(self):
        (self.root / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"already-there": {"command": "z"}}})
        )
        self._handler().install("memory")
        doc = json.loads((self.root / ".mcp.json").read_text())
        self.assertEqual(set(doc["mcpServers"].keys()), {"already-there", "memory"})

    def test_install_with_custom_config_uses_it(self):
        custom = {"command": "/opt/custom-mcp", "args": ["--flag"]}
        self._handler().install("from-scratch", inputs={"config": custom})
        doc = json.loads((self.root / ".mcp.json").read_text())
        self.assertEqual(doc["mcpServers"]["from-scratch"]["command"], "/opt/custom-mcp")
        self.assertEqual(doc["mcpServers"]["from-scratch"]["args"], ["--flag"])

    def test_install_without_example_or_config_errors(self):
        result = self._handler().install("not-in-example")
        self.assertFalse(result["ok"])
        self.assertIn("no example entry", result["error"])

    def test_uninstall_removes_entry(self):
        (self.root / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"memory": {"command": "x"}, "keepme": {"command": "y"}}})
        )
        result = self._handler().uninstall("memory")
        self.assertTrue(result["ok"])
        doc = json.loads((self.root / ".mcp.json").read_text())
        self.assertEqual(list(doc["mcpServers"].keys()), ["keepme"])

    def test_uninstall_noop_when_not_installed(self):
        result = self._handler().uninstall("memory")
        self.assertTrue(result["ok"])
        self.assertTrue(result["noop"])

    def test_get_unknown_returns_none(self):
        self.assertIsNone(self._handler().get("does-not-exist"))

    def test_verify_unknown_errors(self):
        result = self._handler().verify("does-not-exist")
        self.assertFalse(result["ok"])

    def test_to_dict_via_get(self):
        f = self._handler().get("notebooklm")
        d = f.to_dict()
        self.assertEqual(d["kind"], "mcp")
        self.assertEqual(d["status"], "available")


if __name__ == "__main__":
    unittest.main()
