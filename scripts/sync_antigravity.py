#!/usr/bin/env python3
"""Generate Antigravity workflow files at .agents/workflows/<id>.md from recipes/."""

import argparse
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils
import recipe_sync

TARGET_DIR = Path(utils.BASE_DIR) / ".agents" / "workflows"


def render(fm, body):
    rid = fm.get("id", "?")
    name = fm.get("name", rid)
    desc = fm.get("description", "")
    triggers = fm.get("triggers") or {}

    chat = triggers.get("chat") or []
    if isinstance(chat, str):
        chat = [chat]

    invocation = [f"- CLI: `python scripts/recipe_manager.py run {rid}`"]
    if chat:
        invocation.append("- Chat: " + ", ".join(f'"{c}"' for c in chat))
    if triggers.get("schedule"):
        invocation.append(f"- Schedule: `{triggers['schedule']}`")

    return "\n".join([
        f"# {name}",
        "",
        f"> {desc}",
        "",
        f"{recipe_sync.GENERATED_MARKER}{rid}.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_antigravity.py`. -->",
        "",
        "## How to invoke",
        "",
        *invocation,
        "",
        "---",
        "",
        body.strip(),
        "",
    ])


def main():
    parser = argparse.ArgumentParser(description="Generate Antigravity workflows from recipes/")
    parser.add_argument("--check", action="store_true", help="Verify generated files match sources; exit non-zero on drift")
    args = parser.parse_args()

    drifted = recipe_sync.sync_recipes(TARGET_DIR, render, args.check)
    if args.check and drifted:
        print()
        print("Antigravity workflows out of sync. Re-run without --check to regenerate.")
        sys.exit(1)


if __name__ == "__main__":
    main()
