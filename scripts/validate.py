#!/usr/bin/env python3
"""Run all workspace integrity checks. Exits non-zero if anything fails."""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

ROOT_DIR = Path(utils.BASE_DIR)
CONNECTORS_DIR = ROOT_DIR / "connectors"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
REQUIRED_CONNECTOR_FIELDS = ("id", "name", "description", "status", "provides", "auth_type")


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


def _check_connectors(results):
    name = "Connectors integrity"
    _banner(name)

    errors = 0

    def err(msg):
        nonlocal errors
        print(f"  ERR  {msg}")
        errors += 1

    if not CONNECTORS_DIR.exists():
        print("  No connectors/ directory; skipping.")
        results.append((name, True))
        return

    registry_path = CONNECTORS_DIR / "registry.json"
    registry_ids = set()
    if registry_path.exists():
        try:
            data = utils.load_json(str(registry_path))
        except Exception as e:
            err(f"registry.json: {e}")
            data = {}
        for entry in data.get("connectors", []):
            cid = entry.get("id")
            if cid:
                registry_ids.add(cid)
            entry_path = ROOT_DIR / entry.get("path", "")
            if not entry_path.exists():
                err(f"registry entry '{cid}' points at missing file: {entry.get('path')}")
    else:
        err("registry.json missing")

    file_ids = set()
    for f in sorted(CONNECTORS_DIR.glob("*.md")):
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            err(f"{f.name}: {e}")
            continue

        m = FRONTMATTER_RE.match(content)
        if not m:
            err(f"{f.name}: missing or malformed frontmatter")
            continue

        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except Exception as e:
            err(f"{f.name}: YAML parse failure: {e}")
            continue

        cid = fm.get("id")
        if not cid:
            err(f"{f.name}: missing 'id' field")
            continue

        file_ids.add(cid)
        if cid != f.stem:
            err(f"{f.name}: id '{cid}' does not match filename stem")
        for field in REQUIRED_CONNECTOR_FIELDS:
            if not fm.get(field):
                err(f"{f.name}: missing required field '{field}'")

    for cid in sorted(registry_ids - file_ids):
        err(f"registry has entry '{cid}' with no matching file in connectors/")
    for cid in sorted(file_ids - registry_ids):
        err(f"file '{cid}.md' is not in registry.json")

    ok = errors == 0
    print(f"  -> {'PASS' if ok else f'FAIL ({errors} error(s))'}")
    results.append((name, ok))


def main():
    parser = argparse.ArgumentParser(description="Run all workspace integrity checks")
    args = parser.parse_args()
    del args

    results = []
    py = sys.executable

    _run_check("Recipe lint", [py, "scripts/recipe_manager.py", "lint"], results)
    _run_check("Recipe registry sync", [py, "scripts/recipe_manager.py", "sync", "--check"], results)
    _run_check("Generated docs sync", [py, "scripts/docs_generator.py", "--check"], results)
    _run_check("Antigravity workflows sync", [py, "scripts/sync_antigravity.py", "--check"], results)
    _run_check("Claude Code commands sync", [py, "scripts/sync_claude_code.py", "--check"], results)
    _check_connectors(results)

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
