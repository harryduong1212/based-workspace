#!/usr/bin/env python3
"""Generate Claude Code slash commands at .claude/commands/<id>.md from recipes/."""

import argparse
import os
import sys
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils
import recipe_sync

TARGET_DIR = Path(utils.BASE_DIR) / ".claude" / "commands"


def render(fm, body):
    rid = fm.get("id", "?")
    desc = fm.get("description", "")
    inputs = fm.get("inputs") or []

    arg_hints = []
    for inp in inputs:
        name = inp.get("name", "?")
        if inp.get("required", False):
            arg_hints.append(f"--input {name}=<value>")
        else:
            arg_hints.append(f"[--input {name}=<value>]")

    out = ["---", f"description: {desc}"]
    if arg_hints:
        out.append(f"argument-hint: {' '.join(arg_hints)}")
    out.append("---")
    out.append("")
    out.append(f"{recipe_sync.GENERATED_MARKER}{rid}.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_claude_code.py`. -->")
    out.append("")
    out.append(body.strip())
    out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Generate Claude Code slash commands from recipes/")
    parser.add_argument("--check", action="store_true", help="Verify generated files match sources; exit non-zero on drift")
    args = parser.parse_args()

    drifted = recipe_sync.sync_recipes(TARGET_DIR, render, args.check)
    if args.check and drifted:
        print()
        print("Claude Code commands out of sync. Re-run without --check to regenerate.")
        sys.exit(1)


if __name__ == "__main__":
    main()
