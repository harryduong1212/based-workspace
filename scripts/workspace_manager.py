#!/usr/bin/env python3
"""
Workspace Context Manager
=========================
Exclusive controller for the .agents/ skill/workflow symlink surface.

Usage:
    python scripts/workspace_manager.py --profile java-backend-dev
    python scripts/workspace_manager.py --skills "java-pro,api-patterns,postgresql-optimization"
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows (avoids charmap encoding errors).
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = WORKSPACE_ROOT / ".agents"
ARCHIVED_DIR = WORKSPACE_ROOT / ".archived"
SKILLS_ACTIVE = AGENTS_DIR / "skills"
WORKFLOWS_ACTIVE = AGENTS_DIR / "workflows"
SKILLS_ARCHIVE = ARCHIVED_DIR / "skills"
WORKFLOWS_ARCHIVE = ARCHIVED_DIR / "workflows"
PROFILES_PATH = Path(__file__).resolve().parent / "profiles.json"

# Directories inside .agents/skills/ that must never be removed.
PRESERVED_DIRS = {"workspace-configurator"}

DEFAULT_WORKFLOWS = [
    "env-config",
    "git-commit",
    "git-commit-group-changes",
    "git-conflict",
    "git-pr",
    "git-rebase"
]

# ──────────────────────────────────────────────
# Colour helpers (gracefully degrade on Windows)
# ──────────────────────────────────────────────
_SUPPORTS_COLOUR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _SUPPORTS_COLOUR else text


def _green(t: str) -> str:
    return _c("32", t)


def _yellow(t: str) -> str:
    return _c("33", t)


def _red(t: str) -> str:
    return _c("31", t)


def _cyan(t: str) -> str:
    return _c("36", t)


def _bold(t: str) -> str:
    return _c("1", t)


# ──────────────────────────────────────────────
# Registry helpers
# ──────────────────────────────────────────────
def _load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def build_skill_index() -> dict[str, dict]:
    """
    Walk every category registry under .archived/skills/ and return a flat
    index of  skill_id -> { category_id, category_name, path (relative to
    the category dir), description }.
    """
    top_registry = _load_json(SKILLS_ARCHIVE / "registry.json")
    index: dict[str, dict] = {}

    for cat in top_registry.get("categories", []):
        cat_registry_path = WORKSPACE_ROOT / cat["registry_path"]
        if not cat_registry_path.exists():
            continue
        cat_data = _load_json(cat_registry_path)
        cat_id = cat_data.get("category_id", cat["category_id"])
        cat_name = cat_data.get("category_name", cat.get("category_name", cat_id))

        for skill in cat_data.get("skills", []):
            sid = skill["id"]
            # Absolute path to the skill directory (not SKILL.md itself)
            skill_dir = SKILLS_ARCHIVE / cat_id / skill["path"].replace("/SKILL.md", "")
            index[sid] = {
                "category_id": cat_id,
                "category_name": cat_name,
                "description": skill.get("description", ""),
                "abs_path": skill_dir,
                "triggers": skill.get("triggers", []),
                "tags": skill.get("tags", []),
            }

    return index


def build_workflow_index() -> dict[str, dict]:
    """
    Walk every category registry under .archived/workflows/ and return a flat
    index of workflow_id -> { category_id, category_name, path, description, triggers, tags }.
    """
    top_registry = _load_json(WORKFLOWS_ARCHIVE / "registry.json")
    index: dict[str, dict] = {}

    for cat in top_registry.get("categories", []):
        cat_registry_path = WORKSPACE_ROOT / cat["registry_path"]
        if not cat_registry_path.exists():
            continue
        cat_data = _load_json(cat_registry_path)
        cat_id = cat_data.get("category_id", cat["category_id"])
        cat_name = cat_data.get("category_name", cat.get("category_name", cat_id))

        for wf in cat_data.get("workflows", []):
            wid = wf["id"]
            # If path ends in .md, use it directly (flat structure). If legacy, it cleans up "/WORKFLOW.md". 
            if wf["path"].endswith(".md") and "WORKFLOW.md" not in wf["path"]:
                wf_target = WORKFLOWS_ARCHIVE / cat_id / wf["path"]
            else:
                wf_target = WORKFLOWS_ARCHIVE / cat_id / wf["path"].replace("/WORKFLOW.md", "")
            index[wid] = {
                "category_id": cat_id,
                "category_name": cat_name,
                "description": wf.get("description", ""),
                "abs_path": wf_target,
                "triggers": wf.get("triggers", []),
                "tags": wf.get("tags", []),
            }

    return index


# ──────────────────────────────────────────────
# Symlink / junction management
# ──────────────────────────────────────────────
def _is_link(p: Path) -> bool:
    """Return True if *p* is a symlink **or** a Windows NTFS junction."""
    if p.is_symlink():
        return True
    if os.name == "nt":
        try:
            # Junction points have the ReparsePoint attribute.
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(p))
            if attrs == -1:
                return False
            FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
            return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
        except Exception:
            return False
    return False


def _remove_link(p: Path) -> None:
    """Remove a symlink or junction at *p*."""
    if p.is_symlink():
        p.unlink()
    elif os.name == "nt" and _is_link(p):
        # Junctions look like directories — use rmdir (not rmtree!)
        os.rmdir(str(p))
    else:
        p.unlink(missing_ok=True)


def wipe_symlinks(directory: Path, preserved: set[str]) -> list[str]:
    """Remove all contents in *directory* except preserved items and registry.json."""
    removed: list[str] = []
    if not directory.exists():
        return removed
    for child in list(directory.iterdir()):
        if child.name in preserved or child.name == "registry.json":
            continue
        
        try:
            if child.is_dir() and not _is_link(child):
                shutil.rmtree(child)
            else:
                # Works for files, symlinks, junctions, and hardlinks
                child.unlink()
            removed.append(child.name)
        except Exception as e:
            print(f"  {_red('ERROR')} Could not remove {child.name}: {e}")
            
    return removed


def create_deep_link(source: Path, link: Path) -> None:
    """
    Create an OS-agnostic 'deep link'.
    For directories, it creates a real directory and recursively links its contents.
    For files, it creates a symlink or a fallback hardlink (Windows).
    This ensures that folders (like skills) are correctly indexed by the environment.
    """
    # 1. Ensure the parent directory exists.
    link.parent.mkdir(parents=True, exist_ok=True)

    # 2. Handle existing items at the link path.
    if link.exists() or link.is_symlink() or _is_link(link):
        try:
            if link.is_dir() and not _is_link(link):
                shutil.rmtree(link)
            else:
                _remove_link(link)
        except Exception as e:
            print(f"  {_yellow('SKIP')} {link.name} — could not remove existing item: {e}")
            return

    # 3. If source is a directory, use the 'deep link' approach.
    if source.is_dir():
        link.mkdir(parents=True, exist_ok=True)
        for item in source.iterdir():
            create_deep_link(item, link / item.name)
        return

    # 4. If source is a file, use a simple link (Symlink or Hardlink).
    # Attempt a true symlink first (works on Unix & Windows w/ Developer Mode).
    try:
        # Use relative path if possible for portability of the workspace.
        try:
            rel_source = os.path.relpath(source, link.parent)
        except ValueError:
            rel_source = str(source)
            
        os.symlink(rel_source, str(link), target_is_directory=False)
        return
    except (OSError, ValueError):
        pass  # Fall through to OS-specific hardlink fallback.

    # Fallback: Windows NTFS hardlink (no admin rights required).
    if os.name == "nt":
        abs_source = str(source.resolve())
        abs_link = str(link.resolve()) if not link.exists() else str(link)
        # We already handled directories above, so this is always a file hardlink.
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/H", str(link), abs_source],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  {_red('FAIL')} Could not create link for {link.name}: {result.stderr.strip()}")
    else:
        # On non-Windows, if os.symlink failed, we don't have a good fallback if not root,
        # but os.symlink shouldn't fail for files unless permission denied.
        print(f"  {_red('FAIL')} os.symlink failed for {link.name}")


# ──────────────────────────────────────────────
# Core logic
# ──────────────────────────────────────────────
def resolve_ids(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    """Return flat lists of skill IDs and workflow IDs from the CLI arguments."""
    skill_ids: list[str] = []
    workflow_ids: list[str] = list(DEFAULT_WORKFLOWS)

    if args.profile:
        profiles = _load_json(PROFILES_PATH)
        for p_name in (p.strip() for p in args.profile.split(",") if p.strip()):
            entry = profiles.get("profiles", {}).get(p_name)
            if entry is None:
                available = ", ".join(profiles.get("profiles", {}).keys())
                print(f"{_red('ERROR')} Profile '{p_name}' not found.  Available: {available}")
                sys.exit(1)
            skill_ids.extend(entry.get("skills", []))
            workflow_ids.extend(entry.get("workflows", []))
            if entry.get("skills", []) or entry.get("workflows", []):
                print(f"\n{_bold('Profile')} : {_cyan(p_name)}")
                print(f"{_bold('Desc')}    : {entry.get('description', 'N/A')}\n")

    if args.skills:
        skill_ids.extend(s.strip() for s in args.skills.split(",") if s.strip())

    if args.workflows:
        workflow_ids.extend(w.strip() for w in args.workflows.split(",") if w.strip())

    if not skill_ids and not workflow_ids and not args.clear:
        print(f"{_red('ERROR')} No IDs provided. Use --profile, --skills, --workflows, or --clear.")
        sys.exit(1)

    skill_ids = list(dict.fromkeys(skill_ids))
    workflow_ids = list(dict.fromkeys(workflow_ids))

    return skill_ids, workflow_ids


def activate_skills(skill_ids: list[str], wipe_first: bool = False) -> None:
    """Create new symlinks for the given skill IDs, adding to the registry."""
    index = build_skill_index()
    SKILLS_ACTIVE.mkdir(parents=True, exist_ok=True)
    registry_path = SKILLS_ACTIVE / "registry.json"

    registry_data = {
        "category_id": "active-workspace",
        "category_name": "Active Workspace Skills",
        "skills": []
    }

    if wipe_first:
        removed = wipe_symlinks(SKILLS_ACTIVE, PRESERVED_DIRS)
        if removed:
            print(f"  {_yellow('Cleared')} {len(removed)} existing symlink(s) from .agents/skills/")
    else:
        if registry_path.exists():
            try:
                existing_data = _load_json(registry_path)
                registry_data["skills"] = existing_data.get("skills", [])
            except Exception:
                pass

    if wipe_first and not skill_ids:
        # Before returning, we must still ensure preserved skills are in the registry!
        for preserved in PRESERVED_DIRS:
            if (SKILLS_ACTIVE / preserved).exists():
                entry = index.get(preserved)
                registry_data["skills"].append({
                    "id": preserved,
                    "description": entry["description"] if entry else "Preserved workspace orchestrator",
                    "path": f"{preserved}/SKILL.md",
                    "root_category_id": entry["category_id"] if entry else "orchestration",
                    "triggers": entry.get("triggers", []) if entry else [],
                    "tags": entry.get("tags", []) if entry else []
                })

        with open(registry_path, "w", encoding="utf-8") as fh:
            json.dump(registry_data, fh, indent=2)
            
        print(f"\n{'-' * 52}")
        print(f"  {_bold('Skills Context Cleared')}")
        print(f"{'-' * 52}")
        preserved_present = [d for d in PRESERVED_DIRS if (SKILLS_ACTIVE / d).exists()]
        if preserved_present:
            print(f"  {_cyan('*')} Preserved: {', '.join(preserved_present)}")
        print(f"{'-' * 52}\n")
        return

    existing_ids = {s["id"] for s in registry_data["skills"]}

    loaded: list[dict] = []
    missing: list[str] = []

    for sid in skill_ids:
        entry = index.get(sid)
        if entry is None:
            missing.append(sid)
            continue

        source: Path = entry["abs_path"]
        if not source.exists():
            print(f"  {_red('MISS')} {sid} — archive path does not exist: {source}")
            missing.append(sid)
            continue

        link = SKILLS_ACTIVE / sid
        create_deep_link(source, link)
        loaded.append({"id": sid, **entry})

        if sid not in existing_ids:
            registry_data["skills"].append({
                "id": sid,
                "description": entry["description"],
                "path": f"{sid}/SKILL.md",
                "root_category_id": entry["category_id"],
                "triggers": entry.get("triggers", []),
                "tags": entry.get("tags", [])
            })
            existing_ids.add(sid)

    # Ensure preserved skills (like workspace-configurator) are in registry.
    for preserved in PRESERVED_DIRS:
        if preserved not in existing_ids and (SKILLS_ACTIVE / preserved).exists():
            # Try to get metadata from index or the folder itself.
            entry = index.get(preserved)
            registry_data["skills"].append({
                "id": preserved,
                "description": entry["description"] if entry else "Preserved workspace orchestrator",
                "path": f"{preserved}/SKILL.md",
                "root_category_id": entry["category_id"] if entry else "orchestration",
                "triggers": entry.get("triggers", []) if entry else [],
                "tags": entry.get("tags", []) if entry else []
            })
            existing_ids.add(preserved)

    with open(registry_path, "w", encoding="utf-8") as fh:
        json.dump(registry_data, fh, indent=2)

    # ── Summary ─────────────────────────────────
    print(f"\n{'-' * 52}")
    print(f"  {_bold('Skills Loaded')}")
    print(f"{'-' * 52}")

    if loaded:
        max_id = max(len(e["id"]) for e in loaded)
        for e in loaded:
            print(f"  {_green('+')} {e['id']:<{max_id}}  <- {e['category_name']}")
    if missing:
        for m in missing:
            print(f"  {_red('x')} {m:<20}  (not found in any registry)")

    print(f"{'-' * 52}")
    print(
        f"  Total: {_green(str(len(loaded)))} loaded"
        + (f", {_red(str(len(missing)))} missing" if missing else "")
    )

    # Preserved dirs reminder
    preserved_present = [d for d in PRESERVED_DIRS if (SKILLS_ACTIVE / d).exists()]
    if preserved_present:
        print(f"  {_cyan('*')} Preserved: {', '.join(preserved_present)}")

    print(f"{'-' * 52}\n")


def activate_workflows(workflow_ids: list[str], wipe_first: bool = False) -> None:
    """Create new symlinks for the given workflow IDs, adding to the registry."""
    index = build_workflow_index()
    WORKFLOWS_ACTIVE.mkdir(parents=True, exist_ok=True)
    registry_path = WORKFLOWS_ACTIVE / "registry.json"

    registry_data = {
        "category_id": "active-workspace-workflows",
        "category_name": "Active Workspace Workflows",
        "workflows": []
    }

    if wipe_first:
        removed = wipe_symlinks(WORKFLOWS_ACTIVE, set())
        if removed:
            print(f"  {_yellow('Cleared')} {len(removed)} existing symlink(s) from .agents/workflows/")
    else:
        if registry_path.exists():
            try:
                existing_data = _load_json(registry_path)
                registry_data["workflows"] = existing_data.get("workflows", [])
            except Exception:
                pass

    if wipe_first and not workflow_ids:
        with open(registry_path, "w", encoding="utf-8") as fh:
            json.dump(registry_data, fh, indent=2)
            
        print(f"\n{'-' * 52}")
        print(f"  {_bold('Workflows Context Cleared')}")
        print(f"{'-' * 52}\n")
        return

    existing_ids = {w["id"] for w in registry_data["workflows"]}

    loaded: list[dict] = []
    missing: list[str] = []

    for wid in workflow_ids:
        entry = index.get(wid)
        if entry is None:
            missing.append(wid)
            continue

        source: Path = entry["abs_path"]
        if not source.exists():
            print(f"  {_red('MISS')} {wid} — archive path does not exist: {source}")
            missing.append(wid)
            continue

        cat_id = entry["category_id"]
        safe_wid = f"{cat_id}-{wid}" if cat_id != "miscellaneous" else wid
        if not safe_wid.endswith(".md"): safe_wid += ".md"
        
        link = WORKFLOWS_ACTIVE / safe_wid
        create_deep_link(source, link)
        loaded.append({"id": wid, **entry})

        if wid not in existing_ids:
            registry_data["workflows"].append({
                "id": wid,
                "description": entry["description"],
                "path": safe_wid,
                "root_category_id": cat_id,
                "triggers": entry.get("triggers", []),
                "tags": entry.get("tags", [])
            })
            existing_ids.add(wid)

    with open(registry_path, "w", encoding="utf-8") as fh:
        json.dump(registry_data, fh, indent=2)

    # ── Summary ─────────────────────────────────
    print(f"\n{'-' * 52}")
    print(f"  {_bold('Workflows Loaded')}")
    print(f"{'-' * 52}")

    if loaded:
        max_id = max(len(e["id"]) for e in loaded)
        for e in loaded:
            print(f"  {_green('+')} {e['id']:<{max_id}}  <- {e['category_name']}")
    if missing:
        for m in missing:
            print(f"  {_red('x')} {m:<20}  (not found in any registry)")

    print(f"{'-' * 52}")
    print(
        f"  Total: {_green(str(len(loaded)))} loaded"
        + (f", {_red(str(len(missing)))} missing" if missing else "")
    )
    print(f"{'-' * 52}\n")


# ──────────────────────────────────────────────
# Entry-point
# ──────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Workspace Context Manager — configure which skills and workflows are active.",
        epilog="Examples:\n"
        "  python scripts/workspace_manager.py --profile java-backend-dev\n"
        '  python scripts/workspace_manager.py --skills "n8n-workflow-patterns"\n'
        '  python scripts/workspace_manager.py --workflows "feature-kickoff"\n'
        "  python scripts/workspace_manager.py --clear\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--profile",
        type=str,
        metavar="NAME1,NAME2,...",
        help="Comma-separated list of predefined profiles from profiles.json.",
    )
    parser.add_argument(
        "--skills",
        type=str,
        metavar="ID1,ID2,...",
        help="Comma-separated list of skill IDs to activate.",
    )
    parser.add_argument(
        "--workflows",
        type=str,
        metavar="ID1,ID2,...",
        help="Comma-separated list of workflow IDs to activate.",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all active skills and workflows except preserved ones.",
    )
    args = parser.parse_args()

    if not args.profile and not args.skills and not args.workflows and not args.clear:
        parser.print_help()
        sys.exit(0)

    skill_ids, workflow_ids = resolve_ids(args)
    
    if args.skills or args.profile or args.clear:
        activate_skills(skill_ids, wipe_first=args.clear)
    
    if args.workflows or args.profile or args.skills or args.clear:
        activate_workflows(workflow_ids, wipe_first=args.clear)


if __name__ == "__main__":
    main()
