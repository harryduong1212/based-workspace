"""Unit tests for the Tier-1 (system) feature handler.

Mocks `shutil.which` + `subprocess.run` so tests are deterministic and
don't depend on what's installed on the runner.
"""
from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

_HAS_YAML = importlib.util.find_spec("yaml") is not None


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class SystemHandlerTest(unittest.TestCase):
    def _write_catalog(self, content: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False)
        tmp.write(content)
        tmp.flush()
        return Path(tmp.name)

    def _basic_catalog(self) -> Path:
        return self._write_catalog(textwrap.dedent(
            """\
            system:
              podman:
                name: Podman
                description: runtime
                detect:
                  command: podman
                  version_flag: --version
                  min_version: "4.0"
                install_hint:
                  fedora: "sudo dnf install -y podman"
                  debian: "sudo apt install -y podman"
              barebinary:
                name: Bare
                description: no version
                detect:
                  command: bare
                install_hint:
                  fedora: "sudo dnf install -y bare"
            """
        ))

    def test_list_returns_all_declarations(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value=None):
            features = SystemFeatureHandler(catalog_path=cat, distro="fedora").list()

        ids = {f.id for f in features}
        self.assertEqual(ids, {"podman", "barebinary"})

    def test_absent_binary_is_available(self):
        from services.control_panel.features import FeatureStatus
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value=None):
            f = SystemFeatureHandler(catalog_path=cat, distro="fedora").get("podman")

        self.assertEqual(f.status, FeatureStatus.AVAILABLE)
        self.assertIsNone(f.detail.get("binary_path"))

    def test_present_binary_with_recent_version_is_installed(self):
        from services.control_panel.features import FeatureStatus
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/podman"), patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=["podman", "--version"],
                returncode=0,
                stdout="podman version 5.8.2\n",
                stderr="",
            ),
        ):
            f = SystemFeatureHandler(catalog_path=cat, distro="fedora").get("podman")

        self.assertEqual(f.status, FeatureStatus.INSTALLED)
        self.assertEqual(f.detail["version"], "5.8.2")

    def test_present_binary_with_old_version_is_partial(self):
        from services.control_panel.features import FeatureStatus
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/podman"), patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=["podman", "--version"],
                returncode=0,
                stdout="podman version 3.4.0\n",
                stderr="",
            ),
        ):
            f = SystemFeatureHandler(catalog_path=cat, distro="fedora").get("podman")

        self.assertEqual(f.status, FeatureStatus.PARTIAL)
        self.assertEqual(f.detail["version"], "3.4.0")

    def test_present_binary_no_version_flag_is_installed(self):
        from services.control_panel.features import FeatureStatus
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/bare"):
            f = SystemFeatureHandler(catalog_path=cat, distro="fedora").get("barebinary")

        self.assertEqual(f.status, FeatureStatus.INSTALLED)

    def test_install_returns_print_command_for_detected_distro(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value=None):
            result = SystemFeatureHandler(catalog_path=cat, distro="debian").install("podman")

        self.assertTrue(result["ok"])
        self.assertEqual(result["kind"], "print_command")
        self.assertIn("apt install", result["command"])
        self.assertEqual(result["distro"], "debian")

    def test_install_idempotent_when_already_installed(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/bare"):
            result = SystemFeatureHandler(catalog_path=cat, distro="fedora").install("barebinary")

        self.assertTrue(result["ok"])
        self.assertTrue(result["noop"])

    def test_install_falls_back_to_fedora_hint_for_unknown_distro(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value=None):
            result = SystemFeatureHandler(catalog_path=cat, distro="freebsd").install("podman")

        self.assertTrue(result["ok"])
        self.assertIn("dnf install", result["command"])

    def test_uninstall_refuses(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/podman"), patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=["podman", "--version"], returncode=0, stdout="podman version 5.0.0\n", stderr=""
            ),
        ):
            result = SystemFeatureHandler(catalog_path=cat).uninstall("podman")

        self.assertFalse(result["ok"])
        self.assertIn("detect-only", result["error"])

    def test_verify_ok_when_installed(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/podman"), patch(
            "subprocess.run",
            return_value=subprocess.CompletedProcess(
                args=["podman", "--version"], returncode=0, stdout="podman version 5.0.0\n", stderr=""
            ),
        ):
            result = SystemFeatureHandler(catalog_path=cat).verify("podman")

        self.assertTrue(result["ok"])

    def test_unknown_feature_id_returns_error(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        handler = SystemFeatureHandler(catalog_path=cat)
        self.assertIsNone(handler.get("does-not-exist"))
        self.assertFalse(handler.install("does-not-exist")["ok"])
        self.assertFalse(handler.uninstall("does-not-exist")["ok"])
        self.assertFalse(handler.verify("does-not-exist")["ok"])
        self.assertFalse(handler.preview("does-not-exist")["ok"])

    def test_preview_absent_shows_print_command_side_effect(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value=None):
            r = SystemFeatureHandler(catalog_path=cat, distro="debian").preview("podman")

        self.assertTrue(r["ok"])
        self.assertFalse(r["would_be_noop"])
        kinds = [s["kind"] for s in r["side_effects"]]
        self.assertIn("print_command", kinds)
        # The detail must carry the actual command so the dialog can show it.
        cmd = next(s for s in r["side_effects"] if s["kind"] == "print_command")
        self.assertIn("apt install", cmd["detail"])
        # The "never sudo" promise must be communicated to the user.
        self.assertTrue(any("never runs sudo" in w for w in r["warnings"]))

    def test_about_from_catalog_surfaces_on_feature(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._write_catalog(textwrap.dedent(
            """\
            system:
              podman:
                name: Podman
                description: runtime
                about: >-
                  Long prose explaining what podman is
                  and what installing does.
                detect:
                  command: podman
            """
        ))
        with patch("shutil.which", return_value=None):
            f = SystemFeatureHandler(catalog_path=cat, distro="fedora").get("podman")
        self.assertIn("Long prose explaining", f.about)
        self.assertIn("what installing does", f.about)

    def test_preview_already_installed_is_noop(self):
        from services.control_panel.features.system import SystemFeatureHandler

        cat = self._basic_catalog()
        with patch("shutil.which", return_value="/usr/bin/bare"):
            r = SystemFeatureHandler(catalog_path=cat, distro="fedora").preview("barebinary")

        self.assertTrue(r["ok"])
        self.assertTrue(r["would_be_noop"])
        # No print_command in side_effects when already installed — nothing to do.
        self.assertEqual(r["side_effects"], [])


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class DistroDetectionTest(unittest.TestCase):
    def _write(self, body: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".release", delete=False)
        tmp.write(body)
        tmp.flush()
        return Path(tmp.name)

    def test_fedora(self):
        from services.control_panel.features.system import _detect_distro

        p = self._write('NAME="Fedora Linux"\nID=fedora\nVERSION_ID="43"\n')
        self.assertEqual(_detect_distro(p), "fedora")

    def test_ubuntu_maps_to_debian(self):
        from services.control_panel.features.system import _detect_distro

        p = self._write('NAME="Ubuntu"\nID=ubuntu\n')
        self.assertEqual(_detect_distro(p), "debian")

    def test_arch(self):
        from services.control_panel.features.system import _detect_distro

        p = self._write('NAME="Arch Linux"\nID=arch\n')
        self.assertEqual(_detect_distro(p), "arch")

    def test_missing_file_returns_unknown(self):
        from services.control_panel.features.system import _detect_distro

        self.assertEqual(_detect_distro(Path("/nonexistent/os-release")), "unknown")


if __name__ == "__main__":
    unittest.main()
