#!/usr/bin/env python3
"""Run all workspace integrity checks. Exits non-zero if anything fails."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

ROOT_DIR = Path(utils.BASE_DIR)


def _banner(name):
    print()
    print(f"--- {name} " + "-" * (54 - len(name)))


def _run_check(name, cmd, results):
    _banner(name)
    print(f"  $ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    for line in output.rstrip().splitlines():
        print(f"  {line}")
    ok = proc.returncode == 0
    print(f"  -> {'PASS' if ok else 'FAIL'}")
    results.append((name, ok))


def main():
    parser = argparse.ArgumentParser(description="Run all workspace integrity checks")
    args = parser.parse_args()
    del args

    results = []
    py = sys.executable

    _run_check("Recipe lint", [py, "scripts/recipe_manager.py", "lint"], results)
    _run_check("Recipe audit", [py, "scripts/recipe_manager.py", "audit"], results)
    _run_check("Recipe registry sync", [py, "scripts/recipe_manager.py", "sync", "--check"], results)
    _run_check("Generated docs sync", [py, "scripts/docs_generator.py", "--check"], results)
    _run_check("Antigravity workflows sync", [py, "scripts/sync_antigravity.py", "--check"], results)
    _run_check("Claude Code commands sync", [py, "scripts/sync_claude_code.py", "--check"], results)
    _run_check("Connector lint", [py, "scripts/connector_manager.py", "lint"], results)
    _run_check("Connector registry sync", [py, "scripts/connector_manager.py", "sync", "--check"], results)
    _run_check("Cross-link backrefs sync", [py, "scripts/cross_link.py", "--check"], results)
    _run_check(
        "Service package imports",
        [
            py,
            "-c",
            "import services.context_bridge.cli, "
            "services.context_bridge.embedder, "
            "services.context_bridge.store, "
            "services.context_bridge.chunkers.sentence, "
            "services.context_bridge.connectors.jira, "
            "services.context_bridge.connectors.bitbucket, "
            "services.recipe_runtime.dispatcher, "
            "services.recipe_runtime.prompt_assembler",
        ],
        results,
    )
    _run_check(
        "Recipe runtime tests",
        [py, "-m", "unittest", "services.recipe_runtime.tests.test_assembler"],
        results,
    )
    _run_check(
        "Recipe manager tests",
        [py, "-m", "unittest", "scripts.tests.test_recipe_manager"],
        results,
    )

    print()
    print("=" * 60)
    print(" Summary")
    print("=" * 60)
    for name, ok in results:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}]  {name}")

    failed = sum(1 for _, ok in results if not ok)
    print()
    if failed:
        print(f"FAIL — {failed} of {len(results)} check(s) failed.")
        sys.exit(1)
    print(f"OK — all {len(results)} checks passed.")


if __name__ == "__main__":
    main()
