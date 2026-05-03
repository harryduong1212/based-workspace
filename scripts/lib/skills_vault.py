"""Skills vault — move skills between active library and an out-of-registry vault."""

import shutil
from datetime import datetime, timezone
from pathlib import Path

import utils

ROOT = Path(utils.BASE_DIR)
SKILLS_ROOT = ROOT / ".archived" / "skills"
VAULT_ROOT = ROOT / ".archived" / "_vault" / "skills"
TOP_REGISTRY = SKILLS_ROOT / "registry.json"


def _category_registry_path(base, category):
    return base / category / "registry.json"


def _find_in(base, skill_id):
    if not base.exists():
        return None
    for cat_dir in base.iterdir():
        if not cat_dir.is_dir() or cat_dir.name.startswith((".", "_")):
            continue
        if (cat_dir / skill_id).is_dir():
            return cat_dir.name
    return None


def _move_dir(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise FileExistsError(f"Destination already exists: {dst}")
    shutil.move(str(src), str(dst))


def _registry_pop_skill(reg_path, skill_id):
    """Remove a skill entry; return the popped entry or None."""
    if not reg_path.exists():
        return None
    data = utils.load_json(str(reg_path))
    skills = data.get("skills", [])
    popped = None
    kept = []
    for s in skills:
        if s.get("id") == skill_id and popped is None:
            popped = s
        else:
            kept.append(s)
    if popped is None:
        return None
    data["skills"] = kept
    utils.save_json(str(reg_path), data)
    return popped


def _registry_add_skill(reg_path, skill_entry, category):
    if reg_path.exists():
        data = utils.load_json(str(reg_path))
    else:
        data = {
            "category_id": category,
            "category_name": category,
            "skills": [],
        }
    skills = data.setdefault("skills", [])
    if any(s.get("id") == skill_entry.get("id") for s in skills):
        return False
    skills.append(skill_entry)
    skills.sort(key=lambda s: s.get("id", ""))
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    utils.save_json(str(reg_path), data)
    return True


def _bump_top_registry():
    if not TOP_REGISTRY.exists():
        return
    data = utils.load_json(str(TOP_REGISTRY))
    data["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000Z")
    utils.save_json(str(TOP_REGISTRY), data)


def vault_skill(skill_id):
    category = _find_in(SKILLS_ROOT, skill_id)
    if not category:
        return False, f"Not in active library: {skill_id}"

    src = SKILLS_ROOT / category / skill_id
    dst = VAULT_ROOT / category / skill_id

    active_reg = _category_registry_path(SKILLS_ROOT, category)
    vault_reg = _category_registry_path(VAULT_ROOT, category)

    entry = _registry_pop_skill(active_reg, skill_id)
    try:
        _move_dir(src, dst)
    except Exception as e:
        if entry is not None:
            _registry_add_skill(active_reg, entry, category)
        return False, f"Move failed: {e}"

    if entry is not None:
        _registry_add_skill(vault_reg, entry, category)
    _bump_top_registry()
    return True, f"{category}/{skill_id}"


def unvault_skill(skill_id):
    category = _find_in(VAULT_ROOT, skill_id)
    if not category:
        return False, f"Not in vault: {skill_id}"

    src = VAULT_ROOT / category / skill_id
    dst = SKILLS_ROOT / category / skill_id

    vault_reg = _category_registry_path(VAULT_ROOT, category)
    active_reg = _category_registry_path(SKILLS_ROOT, category)

    entry = _registry_pop_skill(vault_reg, skill_id)
    try:
        _move_dir(src, dst)
    except Exception as e:
        if entry is not None:
            _registry_add_skill(vault_reg, entry, category)
        return False, f"Move failed: {e}"

    if entry is not None:
        _registry_add_skill(active_reg, entry, category)
    _bump_top_registry()
    return True, f"{category}/{skill_id}"


def read_orphans_from_report():
    """Read orphan rows (atomic+effective+recipe == 0) from the latest prune report."""
    csv_path = Path(utils.TMP_DIR) / "prune_report.csv"
    if not csv_path.exists():
        return None
    orphans = []
    with open(csv_path, "r", encoding="utf-8") as f:
        f.readline()  # skip header
        for line in f:
            parts = line.rstrip("\n").split(",", 8)
            if len(parts) < 8:
                continue
            try:
                atomic, effective, recipe = int(parts[1]), int(parts[2]), int(parts[3])
            except ValueError:
                continue
            if atomic == 0 and effective == 0 and recipe == 0:
                orphans.append({"category": parts[6], "id": parts[7]})
    return orphans
