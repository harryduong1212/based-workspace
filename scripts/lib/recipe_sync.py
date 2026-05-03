"""Shared helpers for provider sync scripts (Antigravity, Claude Code)."""

import re
from pathlib import Path

import yaml

import utils

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
GENERATED_MARKER = "<!-- Generated from recipes/"

ROOT_DIR = Path(utils.BASE_DIR)
RECIPES_DIR = ROOT_DIR / "recipes"


def parse_recipe(path):
    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, content
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def write_or_check(path, content, check_mode):
    rel = path.relative_to(ROOT_DIR)
    if check_mode:
        if not path.exists():
            print(f"DRIFT (missing) {rel}")
            return True
        existing = path.read_text(encoding="utf-8")
        if existing != content:
            print(f"DRIFT (changed) {rel}")
            return True
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE {rel}")
    return False


def is_generated(path):
    if not path.exists():
        return False
    try:
        return GENERATED_MARKER in path.read_text(encoding="utf-8")
    except Exception:
        return False


def prune_stale(target_dir, valid_ids, check_mode):
    """Remove generated files for recipe IDs that no longer exist. Skip hand-authored files."""
    if not target_dir.exists():
        return False
    drifted = False
    valid = set(valid_ids)
    for f in sorted(target_dir.glob("*.md")):
        if f.stem in valid:
            continue
        if not is_generated(f):
            continue
        rel = f.relative_to(ROOT_DIR)
        if check_mode:
            print(f"DRIFT (orphan) {rel}")
            drifted = True
        else:
            f.unlink()
            print(f"REMOVED {rel}")
    return drifted


def sync_recipes(target_dir, render_fn, check_mode):
    """Walk recipes/, render via render_fn(fm, body), write to target_dir/<id>.md."""
    if not RECIPES_DIR.exists():
        print(f"No recipes/ directory at {RECIPES_DIR}")
        return False

    drifted = False
    valid_ids = []
    for path in sorted(RECIPES_DIR.glob("*.md")):
        fm, body = parse_recipe(path)
        if not fm:
            continue
        rid = fm.get("id") or path.stem
        valid_ids.append(rid)
        out_path = target_dir / f"{rid}.md"
        drifted |= write_or_check(out_path, render_fn(fm, body), check_mode)

    drifted |= prune_stale(target_dir, valid_ids, check_mode)
    return drifted
