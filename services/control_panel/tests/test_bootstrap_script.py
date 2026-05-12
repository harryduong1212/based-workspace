"""Light verification of scripts/bootstrap.sh — does NOT execute it.

Confirms the script exists, is executable, parses cleanly under bash -n,
and references the steps documented in the Features-page design memory.
"""
from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

from services.control_panel.config import Config


REPO_ROOT = Config.from_env().workspace_root
SCRIPT = REPO_ROOT / "scripts" / "bootstrap.sh"


class BootstrapScriptTest(unittest.TestCase):
    def test_script_exists_and_is_executable(self):
        self.assertTrue(SCRIPT.exists(), f"bootstrap.sh missing at {SCRIPT}")
        import os
        mode = SCRIPT.stat().st_mode
        self.assertTrue(mode & 0o111, "bootstrap.sh must be executable")

    def test_script_starts_with_bash_shebang(self):
        first = SCRIPT.read_text(encoding="utf-8").splitlines()[0]
        self.assertTrue(
            first.startswith("#!") and "bash" in first,
            f"expected bash shebang; got {first!r}",
        )

    @unittest.skipUnless(shutil.which("bash"), "bash not on PATH")
    def test_script_parses_under_bash(self):
        result = subprocess.run(
            ["bash", "-n", str(SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_script_uses_set_strict_mode(self):
        body = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("set -euo pipefail", body)

    def test_script_references_expected_steps(self):
        body = SCRIPT.read_text(encoding="utf-8")
        # Each of these strings means the corresponding step is wired:
        for marker in (
            "python3 -m venv",
            "services/control_panel/requirements.txt",
            "services/control_panel/web",  # frontend dir
            ".env.example",
            ".mcp.json.example",
            "python -m services.control_panel",  # backend start command in the final hint
            "npm run dev",  # frontend start command in the final hint
        ):
            self.assertIn(marker, body, f"expected bootstrap.sh to reference {marker!r}")

    def test_script_never_runs_sudo(self):
        """The script must NOT invoke sudo — only print hints. Security rule."""
        body = SCRIPT.read_text(encoding="utf-8")
        # `sudo` appears in the print-only install hints; check there's no `sudo X` actually executed.
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if stripped.startswith("echo") or stripped.startswith('echo "') or "echo " in stripped:
                continue  # echo-string mentions are documentation
            # Ban a bare `sudo ...` command outside echo / cat / printf.
            self.assertNotRegex(
                stripped,
                r"^\s*sudo\b",
                msg=f"bootstrap.sh appears to execute sudo on line: {line!r}",
            )


if __name__ == "__main__":
    unittest.main()
