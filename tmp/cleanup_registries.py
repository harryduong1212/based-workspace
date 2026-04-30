import json
import os
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
ARCHIVED_SKILLS = WORKSPACE_ROOT / ".archived/skills"
ORPHANS_FILE = WORKSPACE_ROOT / "tmp/orphans.json"

def cleanup_registries():
    if not ORPHANS_FILE.exists():
        print("Orphans file not found.")
        return

    with open(ORPHANS_FILE, "r", encoding="utf-8") as f:
        orphans_data = json.load(f)
    
    orphaned_ids = {s["id"] for s in orphans_data.get("orphaned_skills", [])}
    
    # Update category registries
    for cat_dir in ARCHIVED_SKILLS.iterdir():
        if not cat_dir.is_dir():
            continue
            
        reg_path = cat_dir / "registry.json"
        if not reg_path.exists():
            continue
            
        with open(reg_path, "r", encoding="utf-8") as f:
            reg = json.load(f)
            
        original_count = len(reg.get("skills", []))
        reg["skills"] = [s for s in reg.get("skills", []) if s["id"] not in orphaned_ids]
        new_count = len(reg["skills"])
        
        if original_count != new_count:
            print(f"Updating {reg_path.relative_to(WORKSPACE_ROOT)}: removed {original_count - new_count} skills.")
            with open(reg_path, "w", encoding="utf-8") as f:
                json.dump(reg, f, indent=2)

if __name__ == "__main__":
    cleanup_registries()
