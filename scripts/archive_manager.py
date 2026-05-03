#!/usr/bin/env python3
"""Archive lifecycle CLI — prune-report, vault, unvault, vault-orphans for `.archived/skills/`."""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

try:
    import yaml
except ImportError:
    yaml = None

import skills_vault

SKIP_DIR_NAMES = {"skills_reorganized", "_vault"}
RECIPE_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def _gather_skills_on_disk():
    skills_root = Path(utils.BASE_DIR) / ".archived" / "skills"
    if not skills_root.exists():
        return []
    found = []
    for cat_dir in sorted(skills_root.iterdir()):
        if not cat_dir.is_dir():
            continue
        if cat_dir.name.startswith((".", "_")) or cat_dir.name in SKIP_DIR_NAMES:
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            stat = skill_md.stat()
            desc = ""
            try:
                content = skill_md.read_text(encoding="utf-8", errors="replace")
                m = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
                if m:
                    desc = m.group(1).strip().strip("'\"")[:80]
            except Exception:
                pass
            found.append({
                "id": skill_dir.name,
                "category": cat_dir.name,
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
                "description": desc,
            })
    return found


def _count_recipe_refs():
    recipes_dir = Path(utils.BASE_DIR) / "recipes"
    counts = {}
    if not recipes_dir.exists() or yaml is None:
        return counts
    for rpath in recipes_dir.glob("*.md"):
        try:
            text = rpath.read_text(encoding="utf-8")
            m = RECIPE_FRONTMATTER_RE.match(text)
            if not m:
                continue
            fm = yaml.safe_load(m.group(1)) or {}
            for sid in fm.get("requires_skills") or []:
                counts[sid] = counts.get(sid, 0) + 1
        except Exception:
            pass
    return counts


def cmd_prune_report(args):
    skills = _gather_skills_on_disk()
    if not skills:
        print("No skills found under .archived/skills/")
        return

    recipe_refs = _count_recipe_refs()

    for s in skills:
        s["recipe_refs"] = recipe_refs.get(s["id"], 0)
        # Composite score — recipes weigh most; small content-depth bump capped at 20.
        s["score"] = s["recipe_refs"] * 10 + min(s["size_bytes"] // 1024, 20)

    skills.sort(key=lambda s: (s["score"], s["category"], s["id"]))

    total = len(skills)
    orphans = [s for s in skills if s["recipe_refs"] == 0]
    by_cat = {}
    for s in skills:
        by_cat[s["category"]] = by_cat.get(s["category"], 0) + 1

    print(f"Total skills on disk : {total}")
    print(f"Orphans (no recipe refs): {len(orphans)}")
    print(f"Categories           : {len(by_cat)}")
    print()

    limit = args.limit or 30
    print(f"Bottom {min(limit, total)} by score (vault candidates first):")
    print()
    print(f"{'SCORE':<6} {'REC':<4} {'SIZE':<6} {'MODIFIED':<11} {'CATEGORY':<22} ID")
    print("-" * 90)
    for s in skills[:limit]:
        size_kb = f"{s['size_bytes'] // 1024}K"
        print(f"{s['score']:<6} {s['recipe_refs']:<4} {size_kb:<6} {s['modified']:<11} {s['category']:<22} {s['id']}")

    print()
    print("Per-category orphan summary:")
    cat_orphans = {}
    for s in orphans:
        cat_orphans[s["category"]] = cat_orphans.get(s["category"], 0) + 1
    for cat in sorted(cat_orphans, key=lambda c: -cat_orphans[c]):
        total_in_cat = by_cat[cat]
        print(f"  {cat:<28} {cat_orphans[cat]:>3} / {total_in_cat:<3} orphaned")

    os.makedirs(utils.TMP_DIR, exist_ok=True)
    csv_path = os.path.join(utils.TMP_DIR, "prune_report.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("score,recipe_refs,size_bytes,modified,category,id,description\n")
        for s in skills:
            desc = s["description"].replace('"', '""')
            f.write(
                f'{s["score"]},{s["recipe_refs"]},{s["size_bytes"]},'
                f'{s["modified"]},{s["category"]},{s["id"]},"{desc}"\n'
            )
    print()
    print(f"Full report ({total} rows) saved to {csv_path}")


def cmd_vault(args):
    ok, msg = skills_vault.vault_skill(args.id)
    print(("VAULTED  " if ok else "FAIL     ") + msg)
    sys.exit(0 if ok else 1)


def cmd_unvault(args):
    ok, msg = skills_vault.unvault_skill(args.id)
    print(("UNVAULTED " if ok else "FAIL      ") + msg)
    sys.exit(0 if ok else 1)


def cmd_vault_orphans(args):
    orphans = skills_vault.read_orphans_from_report()
    if orphans is None:
        print("No prune report found at tmp/prune_report.csv.")
        print("Run 'python scripts/archive_manager.py prune-report' first.")
        sys.exit(1)
    if not orphans:
        print("No orphans to vault.")
        return

    if args.limit:
        orphans = orphans[: args.limit]

    print(f"Orphans to vault: {len(orphans)}")
    if args.dry_run:
        for o in orphans:
            print(f"DRY-RUN  {o['category']}/{o['id']}")
        print()
        print("Re-run without --dry-run to vault.")
        return

    succeeded = failed = 0
    for o in orphans:
        ok, msg = skills_vault.vault_skill(o["id"])
        if ok:
            print(f"VAULTED  {msg}")
            succeeded += 1
        else:
            print(f"FAIL     {msg}")
            failed += 1
    print()
    print(f"Done. {succeeded} vaulted, {failed} failed.")
    sys.exit(0 if failed == 0 else 1)


def main():
    parser = argparse.ArgumentParser(description="Archive lifecycle CLI for .archived/skills/")
    subparsers = parser.add_subparsers(dest="command")

    p_prune = subparsers.add_parser(
        "prune-report",
        help="Score every skill on disk by recipe usage and size; identify vault candidates",
    )
    p_prune.add_argument("--limit", type=int, default=30, help="How many bottom-scored skills to print (default 30)")

    p_vault = subparsers.add_parser("vault", help="Vault a single skill (move to .archived/_vault/skills/)")
    p_vault.add_argument("id")

    p_unvault = subparsers.add_parser("unvault", help="Restore a vaulted skill to the active library")
    p_unvault.add_argument("id")

    p_orphans = subparsers.add_parser(
        "vault-orphans",
        help="Vault every orphan skill from the latest prune-report",
    )
    p_orphans.add_argument("--dry-run", action="store_true", help="Print what would be vaulted without moving anything")
    p_orphans.add_argument("--limit", type=int, help="Cap the number of orphans to vault")

    args = parser.parse_args()

    if args.command == "prune-report":
        cmd_prune_report(args)
    elif args.command == "vault":
        cmd_vault(args)
    elif args.command == "unvault":
        cmd_unvault(args)
    elif args.command == "vault-orphans":
        cmd_vault_orphans(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
