#!/usr/bin/env python3
"""Skill attrition audit — list skills not referenced by any recipe.

Phase C2 tooling: produces the watchlist of skills that have not earned
their keep through a recipe reference. Run this before each pruning pass
to see which skills are candidates for vaulting.

Usage:
    python scripts/skill_attrition_audit.py            # full bucketed list
    python scripts/skill_attrition_audit.py --summary  # counts per category
    python scripts/skill_attrition_audit.py --json     # machine-readable
"""
import argparse
import glob
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_REGISTRY = ROOT / ".archived" / "skills" / "registry.json"
RECIPES_GLOB = str(ROOT / "recipes" / "*.md")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def collect_skills():
    with open(SKILLS_REGISTRY) as f:
        top = json.load(f)
    skills = []
    for cat in top.get("categories", []):
        cid = cat.get("category_id")
        sub_path = ROOT / cat.get("registry_path", "")
        if not sub_path.exists():
            continue
        with open(sub_path) as f2:
            sub = json.load(f2)
        for s in sub.get("skills", []):
            sid = s.get("id")
            desc = (s.get("description") or "").strip()
            if sid:
                skills.append((cid, sid, desc))
    return skills


def collect_referenced():
    referenced = set()
    for recipe in glob.glob(RECIPES_GLOB):
        text = Path(recipe).read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        for sid in fm.get("requires_skills") or []:
            referenced.add(sid)
    return referenced


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--summary", action="store_true", help="Counts per category, no skill list.")
    ap.add_argument("--json", action="store_true", help="Machine-readable JSON.")
    args = ap.parse_args()

    skills = collect_skills()
    referenced = collect_referenced()
    unref = [(c, s, d) for (c, s, d) in skills if s not in referenced]

    if args.json:
        out = {
            "total": len(skills),
            "referenced": sorted(referenced),
            "unreferenced_count": len(unref),
            "unreferenced": [{"category": c, "id": s, "description": d} for (c, s, d) in unref],
        }
        print(json.dumps(out, indent=2))
        return

    print(f"Total skills: {len(skills)}")
    print(f"Referenced by recipes: {len(referenced)} -> {sorted(referenced)}")
    print(f"Unreferenced (attrition candidates): {len(unref)}")
    print()

    by_cat = defaultdict(list)
    for c, s, d in unref:
        by_cat[c].append((s, d))

    if args.summary:
        for c in sorted(by_cat):
            print(f"  {c}: {len(by_cat[c])}")
        return

    for c in sorted(by_cat):
        print(f"## {c} ({len(by_cat[c])})")
        for s, d in sorted(by_cat[c]):
            line = f"  - {s}"
            if d:
                line += f"  -- {d[:80]}"
            print(line)
        print()


if __name__ == "__main__":
    main()
