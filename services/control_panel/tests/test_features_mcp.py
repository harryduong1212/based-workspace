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

        # Pin the global config path to a tmp file so tests never touch the
        # real ~/.claude.json on this machine.
        return MCPFeatureHandler(
            workspace_root=self.root,
            spawn_probe=probe,
            global_config_path=self.root / "fake-home-claude.json",
            locations_config_path=self.root / "fake-mcp-locations.json",
        )

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

    def test_global_install_refuses_to_clobber_corrupt_claude_json(self):
        # ~/.claude.json holds unrelated Claude Code state. If it's present
        # but unparseable we must NOT overwrite it with just mcpServers.
        fake_home = self.root / "fake-home-claude.json"
        fake_home.write_text('{"userID": "abc", this is not json')
        result = self._handler().install("memory", inputs={"scope": "global"})
        self.assertFalse(result["ok"])
        self.assertIn("not valid JSON", result["error"])
        # The corrupt file is left exactly as-is — nothing destroyed.
        self.assertEqual(fake_home.read_text(), '{"userID": "abc", this is not json')

    def test_global_install_preserves_unrelated_claude_json_keys(self):
        fake_home = self.root / "fake-home-claude.json"
        fake_home.write_text(json.dumps({"userID": "abc", "oauth": {"t": 1}}))
        result = self._handler().install("memory", inputs={"scope": "global"})
        self.assertTrue(result["ok"])
        doc = json.loads(fake_home.read_text())
        self.assertEqual(doc["userID"], "abc")
        self.assertEqual(doc["oauth"], {"t": 1})
        self.assertIn("memory", doc["mcpServers"])

    def test_global_uninstall_refuses_to_clobber_corrupt_claude_json(self):
        fake_home = self.root / "fake-home-claude.json"
        fake_home.write_text("definitely not json")
        result = self._handler().uninstall("memory", inputs={"scope": "global"})
        self.assertFalse(result["ok"])
        self.assertEqual(fake_home.read_text(), "definitely not json")

    def test_custom_location_install_writes_there_and_remembers(self):
        import json as _json

        other = self.root / "other-project"
        other.mkdir()
        result = self._handler().install("memory", inputs={"path": str(other)})
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["path"], str(other.resolve()))
        # Wrote into the *custom* dir, not this project's .mcp.json.
        self.assertFalse((self.root / ".mcp.json").exists())
        doc = _json.loads((other / ".mcp.json").read_text())
        self.assertIn("memory", doc["mcpServers"])
        # cwd defaulted to the custom dir, not workspace_root.
        self.assertEqual(doc["mcpServers"]["memory"]["cwd"], str(other.resolve()))
        # Location remembered for next time.
        loc = _json.loads((self.root / "fake-mcp-locations.json").read_text())
        self.assertEqual(loc["locations"], [str(other.resolve())])

    def test_custom_location_nonexistent_dir_is_rejected(self):
        result = self._handler().install(
            "memory", inputs={"path": str(self.root / "nope")}
        )
        self.assertFalse(result["ok"])
        self.assertIn("does not exist", result["error"])
        self.assertFalse((self.root / "nope").exists())  # never created

    def test_custom_location_uninstall_removes_entry(self):
        import json as _json

        other = self.root / "proj2"
        other.mkdir()
        h = self._handler()
        h.install("memory", inputs={"path": str(other)})
        result = h.uninstall("memory", inputs={"scope": "workspace", "path": str(other)})
        self.assertTrue(result["ok"])
        doc = _json.loads((other / ".mcp.json").read_text())
        self.assertNotIn("memory", doc.get("mcpServers", {}))

    def test_known_locations_surface_in_detail(self):
        other = self.root / "proj3"
        other.mkdir()
        h = self._handler()
        h.install("memory", inputs={"path": str(other)})
        f = h.get("memory")
        self.assertIn(str(other.resolve()), f.detail["known_locations"])
        self.assertEqual(f.detail["workspace_name"], self.root.resolve().name)

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

    def test_preview_describes_config_write_and_spawn(self):
        r = self._handler().preview("memory")
        self.assertTrue(r["ok"])
        kinds = [s["kind"] for s in r["side_effects"]]
        self.assertIn("config_write", kinds)
        self.assertIn("mcp_spawn", kinds)
        spawn = next(s for s in r["side_effects"] if s["kind"] == "mcp_spawn")
        # Detail must contain the command we'd actually spawn.
        self.assertIn("with-env.sh", spawn["detail"])

    def test_preview_unknown_errors(self):
        r = self._handler().preview("does-not-exist")
        self.assertFalse(r["ok"])

    def test_preview_already_installed_warns_of_overwrite(self):
        # Installed AND probe-passes → status will be INSTALLED in preview's snapshot
        # (but preview itself runs probe=False, so we test via the warning instead).
        (self.root / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"memory": {"command": "x"}}})
        )
        r = self._handler().preview("memory")
        self.assertTrue(r["ok"])
        # An installed-but-being-reinstalled entry must produce a "will overwrite" hint.
        self.assertTrue(any("overwrite" in w for w in r["warnings"]))

    def test_underscore_metadata_drives_feature_fields(self):
        """_description/_docs/_requires from the example surface on the Feature
        and feed the dep graph — without leaking into spawned config."""
        (self.root / ".mcp.json.example").write_text(json.dumps({
            "mcpServers": {
                "memory": {
                    "command": "./scripts/with-env.sh",
                    "args": ["python3", "-m", "services.memory_mcp"],
                    "_description": "Persistent semantic memory via mem0.",
                    "_docs": "https://github.com/mem0ai/mem0",
                    "_requires": ["qdrant", "llama-swap"],
                }
            }
        }))
        f = self._handler().get("memory")
        self.assertEqual(f.description, "Persistent semantic memory via mem0.")
        self.assertEqual(f.detail["docs"], "https://github.com/mem0ai/mem0")
        self.assertEqual(f.detail["requires_services"], ["qdrant", "llama-swap"])
        # The dep graph must see these so the install dialog can gate + explain.
        self.assertEqual(f.requires, ["qdrant", "llama-swap"])

    def test_about_metadata_surfaces_and_is_stripped_on_install(self):
        (self.root / ".mcp.json.example").write_text(json.dumps({
            "mcpServers": {
                "memory": {
                    "command": "x",
                    "_about": "Full explanation of the memory server.",
                }
            }
        }))
        f = self._handler().get("memory")
        self.assertEqual(f.about, "Full explanation of the memory server.")
        self._handler().install("memory")
        written = json.loads((self.root / ".mcp.json").read_text())["mcpServers"]["memory"]
        self.assertNotIn("_about", written)

    def test_install_strips_underscore_metadata_from_mcp_json(self):
        """Metadata keys must never reach .mcp.json (and thus the spawned
        server's config) — only real MCP fields get written."""
        (self.root / ".mcp.json.example").write_text(json.dumps({
            "mcpServers": {
                "memory": {
                    "command": "x",
                    "args": ["y"],
                    "_description": "desc",
                    "_docs": "url",
                    "_requires": ["qdrant"],
                }
            }
        }))
        self._handler().install("memory")
        written = json.loads((self.root / ".mcp.json").read_text())["mcpServers"]["memory"]
        self.assertNotIn("_description", written)
        self.assertNotIn("_docs", written)
        self.assertNotIn("_requires", written)
        self.assertEqual(written["command"], "x")
        self.assertEqual(written["args"], ["y"])


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class MCPHandlerScopeTest(unittest.TestCase):
    """Scope-aware install/uninstall: workspace vs global."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.global_path = self.root / "fake-home-claude.json"
        (self.root / ".mcp.json.example").write_text(
            json.dumps({
                "mcpServers": {
                    "memory": {
                        "command": "./scripts/with-env.sh",
                        "args": ["python3", "-m", "services.memory_mcp"],
                        "cwd": ".",
                    },
                    "grep_app": {"command": "uvx", "args": ["grep-mcp"]},
                }
            })
        )

    def _handler(self, probe=_good_probe):
        from services.control_panel.features.mcp import MCPFeatureHandler

        return MCPFeatureHandler(
            workspace_root=self.root,
            spawn_probe=probe,
            global_config_path=self.global_path,
        )

    def test_install_workspace_writes_mcp_json_not_global(self):
        self._handler().install("memory", inputs={"scope": "workspace"})
        ws = json.loads((self.root / ".mcp.json").read_text())["mcpServers"]
        self.assertIn("memory", ws)
        self.assertFalse(self.global_path.exists())

    def test_install_global_writes_user_file_not_workspace(self):
        self._handler().install("grep_app", inputs={"scope": "global"})
        self.assertFalse((self.root / ".mcp.json").exists())
        gl = json.loads(self.global_path.read_text())["mcpServers"]
        self.assertIn("grep_app", gl)

    def test_install_global_drops_cwd_from_entry(self):
        """A machine-wide MCP shouldn't be pinned to one project dir —
        the handler must strip `cwd` when scope=global."""
        self._handler().install("memory", inputs={"scope": "global"})
        entry = json.loads(self.global_path.read_text())["mcpServers"]["memory"]
        self.assertNotIn("cwd", entry)

    def test_install_global_preserves_existing_non_mcp_keys(self):
        """~/.claude.json holds unrelated Claude Code state (userID, growth-book
        flags). Install must merge into mcpServers, not clobber the rest."""
        self.global_path.write_text(json.dumps({"userID": "abc-123", "mcpServers": {}}))
        self._handler().install("grep_app", inputs={"scope": "global"})
        doc = json.loads(self.global_path.read_text())
        self.assertEqual(doc["userID"], "abc-123")
        self.assertIn("grep_app", doc["mcpServers"])

    def test_install_default_scope_is_workspace(self):
        self._handler().install("memory", inputs={})  # no scope key
        self.assertTrue((self.root / ".mcp.json").exists())
        self.assertFalse(self.global_path.exists())

    def test_install_unknown_scope_falls_back_to_workspace(self):
        """Defensive: garbage scope from a future client shouldn't write
        somewhere unexpected — fall back to the safe default."""
        self._handler().install("memory", inputs={"scope": "martian"})
        self.assertTrue((self.root / ".mcp.json").exists())

    def test_install_can_live_in_both_scopes(self):
        h = self._handler()
        h.install("memory", inputs={"scope": "workspace"})
        h.install("memory", inputs={"scope": "global"})
        feature = h.get("memory")
        self.assertIn("workspace", feature.detail["installed_scopes"])
        self.assertIn("global", feature.detail["installed_scopes"])

    def test_get_reports_installed_scopes(self):
        h = self._handler()
        h.install("grep_app", inputs={"scope": "global"})
        feature = h.get("grep_app")
        self.assertEqual(feature.detail["installed_scopes"], ["global"])
        self.assertTrue(feature.detail["in_global"])
        self.assertFalse(feature.detail["in_workspace"])

    def test_uninstall_default_picks_existing_scope(self):
        """When scope isn't given, uninstall removes from whichever scope
        currently has the entry (workspace first if both)."""
        h = self._handler()
        h.install("grep_app", inputs={"scope": "global"})
        # No scope passed — should remove from global since that's the only one.
        result = h.uninstall("grep_app")
        self.assertTrue(result["ok"])
        self.assertEqual(result["scope"], "global")
        feature = h.get("grep_app")
        # `grep_app` is still in .mcp.json.example so it remains available.
        self.assertEqual(feature.detail["installed_scopes"], [])

    def test_uninstall_specific_scope_leaves_other_intact(self):
        h = self._handler()
        h.install("memory", inputs={"scope": "workspace"})
        h.install("memory", inputs={"scope": "global"})
        h.uninstall("memory", inputs={"scope": "workspace"})
        feature = h.get("memory")
        self.assertEqual(feature.detail["installed_scopes"], ["global"])

    def test_uninstall_removes_mcpservers_key_when_emptied_globally(self):
        """If the user's global file only had mcpServers because we added it,
        leave a clean file when we remove the last entry — don't litter the
        user's home config with an empty mcpServers object."""
        self.global_path.write_text(json.dumps({"userID": "abc-123"}))
        h = self._handler()
        h.install("grep_app", inputs={"scope": "global"})
        h.uninstall("grep_app", inputs={"scope": "global"})
        doc = json.loads(self.global_path.read_text())
        self.assertEqual(doc.get("userID"), "abc-123")
        self.assertNotIn("mcpServers", doc)

    def test_preview_global_warns_about_dropping_cwd(self):
        r = self._handler().preview("memory", inputs={"scope": "global"})
        self.assertTrue(r["ok"])
        self.assertEqual(r["scope"], "global")
        self.assertTrue(any("drops `cwd`" in w for w in r["warnings"]))

    def test_preview_warns_about_other_scope(self):
        """Helps the user see they're about to end up with a copy in both
        scopes — easy to do by accident."""
        h = self._handler()
        h.install("grep_app", inputs={"scope": "global"})
        r = h.preview("grep_app", inputs={"scope": "workspace"})
        self.assertTrue(r["ok"])
        self.assertTrue(any("also configured in global" in w for w in r["warnings"]))

    def test_preview_side_effects_name_the_target_file(self):
        ws = self._handler().preview("memory", inputs={"scope": "workspace"})
        gl = self._handler().preview("memory", inputs={"scope": "global"})
        ws_write = next(s for s in ws["side_effects"] if s["kind"] == "config_write")
        gl_write = next(s for s in gl["side_effects"] if s["kind"] == "config_write")
        self.assertIn(".mcp.json", ws_write["summary"])
        self.assertIn("~/.claude.json", gl_write["summary"])


if __name__ == "__main__":
    unittest.main()
