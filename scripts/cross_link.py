#!/usr/bin/env python3
"""Cross-link backreferences — regenerate `## Used by recipes` sections.

Walks recipes/*.md, builds connector_id -> [recipe_id] and
skill_id -> [recipe_id] maps from `requires_connectors` and
`requires_skills`, then rewrites the corresponding section in each
referenced connector and skill file.

Connector files already carry a `## Used by recipes` section — we
replace its body. Skill files typically don't — we append the section
at the end of the file (only for skills actually referenced by a
recipe; we never touch unreferenced skills).
"""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

ROOT_DIR = Path(utils.BASE_DIR)
RECIPES_DIR = ROOT_DIR / "recipes"
CONNECTORS_DIR = ROOT_DIR / "connectors"
SKILLS_REGISTRY = ROOT_DIR / ".archived" / "skills" / "registry.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)
SECTION_RE = re.compile(
    r"(?P<header>^##\s+Used by recipes\s*$\n)(?P<body>.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)


def collect_backrefs():
    """Walk recipes and return (connector_map, skill_map)."""
    conn_map: dict[str, list[str]] = {}
    skill_map: dict[str, list[str]] = {}
    if not RECIPES_DIR.exists():
        return conn_map, skill_map
    for path in sorted(RECIPES_DIR.glob("*.md")):
        m = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        rid = fm.get("id")
        if not rid:
            continue
        for c in fm.get("requires_connectors") or []:
            conn_map.setdefault(c, []).append(rid)
        for s in fm.get("requires_skills") or []:
            skill_map.setdefault(s, []).append(rid)
    for v in conn_map.values():
        v.sort()
    for v in skill_map.values():
        v.sort()
    return conn_map, skill_map


def resolve_skill_paths():
    """Return {skill_id: absolute Path} from the split skill registry."""
    paths: dict[str, Path] = {}
    if not SKILLS_REGISTRY.exists():
        return paths
    root = utils.load_json(str(SKILLS_REGISTRY))
    for cat in root.get("categories", []):
        cat_reg = ROOT_DIR / cat.get("registry_path", "")
        if not cat_reg.exists():
            continue
        cat_data = utils.load_json(str(cat_reg))
        cat_root = cat_reg.parent
        for skill in cat_data.get("skills", []):
            sid = skill.get("id") or skill.get("skill_id")
            spath = skill.get("path")
            if sid and spath:
                paths[sid] = cat_root / spath
    return paths


def render_section_body(recipe_ids):
    if not recipe_ids:
        return "_(none — not referenced by any recipe.)_\n"
    return "".join(f"- `{rid}`\n" for rid in recipe_ids)


def update_existing_section(content, recipe_ids):
    """Replace the body of an existing `## Used by recipes` section."""
    new_body = render_section_body(recipe_ids)

    def _repl(m):
        return m.group("header") + new_body

    new_content, n = SECTION_RE.subn(_repl, content, count=1)
    return new_content, n > 0


def append_section(content, recipe_ids):
    """Append `## Used by recipes` at the end of the file."""
    body = render_section_body(recipe_ids)
    sep = "" if content.endswith("\n\n") else ("\n" if content.endswith("\n") else "\n\n")
    return content + sep + "## Used by recipes\n" + body


def process_connectors(conn_map, check_only):
    """Returns list of (path, status) where status in {'ok','updated','drift'}."""
    results = []
    if not CONNECTORS_DIR.exists():
        return results
    for path in sorted(CONNECTORS_DIR.glob("*.md")):
        cid = path.stem
        recipe_ids = conn_map.get(cid, [])
        original = path.read_text(encoding="utf-8")
        new_content, replaced = update_existing_section(original, recipe_ids)
        if not replaced:
            new_content = append_section(original, recipe_ids)
        if new_content == original:
            results.append((path, "ok"))
            continue
        if check_only:
            results.append((path, "drift"))
        else:
            path.write_text(new_content, encoding="utf-8")
            results.append((path, "updated"))
    return results


def process_skills(skill_map, skill_paths, check_only):
    results = []
    for sid, recipe_ids in sorted(skill_map.items()):
        path = skill_paths.get(sid)
        if not path or not path.exists():
            results.append((sid, "missing"))
            continue
        original = path.read_text(encoding="utf-8")
        new_content, replaced = update_existing_section(original, recipe_ids)
        if not replaced:
            new_content = append_section(original, recipe_ids)
        if new_content == original:
            results.append((path, "ok"))
            continue
        if check_only:
            results.append((path, "drift"))
        else:
            path.write_text(new_content, encoding="utf-8")
            results.append((path, "updated"))
    return results


def main():
    parser = argparse.ArgumentParser(description="Regenerate 'Used by recipes' backreferences in connector and skill files.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if any file would change")
    args = parser.parse_args()

    conn_map, skill_map = collect_backrefs()
    skill_paths = resolve_skill_paths()

    conn_results = process_connectors(conn_map, args.check)
    skill_results = process_skills(skill_map, skill_paths, args.check)

    drift = 0
    missing = 0
    updated = 0

    for entry, status in conn_results + skill_results:
        rel = entry.relative_to(ROOT_DIR) if isinstance(entry, Path) else entry
        if status == "drift":
            print(f"DRIFT  {rel}")
            drift += 1
        elif status == "updated":
            print(f"WROTE  {rel}")
            updated += 1
        elif status == "missing":
            print(f"MISS   skill '{rel}' referenced by a recipe but not in the skill registry")
            missing += 1
        # 'ok' is silent

    print()
    if args.check:
        if drift or missing:
            print(f"Out of sync: {drift} file(s) drifted, {missing} skill ref(s) missing.")
            sys.exit(1)
        print("Backreferences in sync.")
        return

    print(f"Done: {updated} file(s) updated, {missing} skill ref(s) missing.")
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
