#!/usr/bin/env python3
"""Smoke check: confirm the prompt branch in recipe_manager dispatches via
prompt_assembler + dispatch_prompt rather than the old [STUB] path.

Runs `recipe_manager.py run test-prompt --dry-run` in a subprocess so this
check exercises the real CLI surface without ever touching the LLM endpoint.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPE_ID = "test-prompt"


def main():
    cmd = [
        sys.executable, "scripts/recipe_manager.py",
        "run", RECIPE_ID, "--dry-run",
        "--input", "phrase=ping",
    ]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")

    failures = []
    if proc.returncode != 0:
        failures.append(f"exit code {proc.returncode}")
    if "[STUB]" in out:
        failures.append("output still contains '[STUB]' — dispatch_prompt not wired")
    for needle in (
        f"EXECUTE  {RECIPE_ID}",
        "(dry-run)",
        "model        : gemma-3-4b",
        "substituted  : {'phrase': 'ping'}",
        "<ping>",
    ):
        if needle not in out:
            failures.append(f"expected fragment missing from output: {needle!r}")

    if failures:
        print("FAIL — recipe dispatcher dry-run smoke")
        for f in failures:
            print(f"  - {f}")
        print("---- captured output ----")
        print(out)
        sys.exit(1)

    print(f"OK — {RECIPE_ID} dry-run produced an assembled envelope (no [STUB]).")


if __name__ == "__main__":
    main()
