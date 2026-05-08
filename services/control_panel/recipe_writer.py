"""Safe recipe-file writes with frontmatter validation and audit subprocess.

Save policy:
  - Refuse the write if the YAML frontmatter doesn't parse.
  - Refuse the write if the frontmatter `id` doesn't match the file's stem
    (renaming via id-edit isn't supported; would orphan downstream backrefs).
  - Otherwise write atomically (tempfile + os.replace) and run the recipe
    audit as a subprocess; warnings are returned but don't block the save.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import Config


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


@dataclass(frozen=True)
class SaveResult:
    ok: bool
    message: str
    warnings: list[str]


def _parse_frontmatter(content: str) -> tuple[dict, str] | None:
    m = _FRONTMATTER_RE.match(content)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    return fm, m.group(2)


def write_recipe(cfg: Config, recipe_id: str, content: str) -> SaveResult:
    """Validate and persist a recipe file. Returns a structured SaveResult."""
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", recipe_id):
        return SaveResult(False, f"invalid recipe id: {recipe_id!r}", [])

    target = cfg.recipes_dir / f"{recipe_id}.md"

    parsed = _parse_frontmatter(content)
    if parsed is None:
        return SaveResult(
            False,
            "frontmatter is missing or unparseable; ensure the file starts with `---`, has valid YAML, and a closing `---`.",
            [],
        )
    fm, _body = parsed

    declared_id = fm.get("id")
    if declared_id and declared_id != recipe_id:
        return SaveResult(
            False,
            f"frontmatter id ({declared_id!r}) doesn't match the file id ({recipe_id!r}). "
            "Renaming via id-edit isn't supported in the UI yet — copy to a new file instead.",
            [],
        )

    cfg.recipes_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=f".{recipe_id}.", suffix=".md", dir=str(cfg.recipes_dir))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            if not content.endswith("\n"):
                f.write("\n")
        os.replace(tmp_path, target)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return SaveResult(False, f"file write failed: {e}", [])

    warnings = _audit_recipe(cfg, recipe_id)
    return SaveResult(True, f"wrote {target.name}", warnings)


def _audit_recipe(cfg: Config, recipe_id: str) -> list[str]:
    """Run `recipe_manager.py lint` for one recipe; harvest its warnings.

    The lint command runs over all recipes, so we filter the output to lines
    that mention this id. Any lint *errors* surface as warnings here too —
    we already wrote the file, so the user just needs to know what's broken
    so they can fix it on the next save.
    """
    script = cfg.workspace_root / "scripts" / "recipe_manager.py"
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "lint"],
            cwd=str(cfg.workspace_root),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return ["audit timed out after 30s"]
    output = (proc.stdout or "") + (proc.stderr or "")
    relevant = [line for line in output.splitlines() if recipe_id in line and ("ERROR" in line.upper() or "WARN" in line.upper())]
    if not relevant and proc.returncode != 0:
        return [line for line in output.splitlines() if line.strip()][:20]
    return relevant
