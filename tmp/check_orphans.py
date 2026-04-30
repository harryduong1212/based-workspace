import json
import os
from pathlib import Path

# Use relative paths from the workspace root
ARCHIVED_SKILLS = Path(".archived/skills")
REGISTRY_PATH = ARCHIVED_SKILLS / "registry.json"
PROFILES_PATH = Path("scripts/profiles.json")

def check_skills():
    if not REGISTRY_PATH.exists():
        print(f"Top-level registry not found: {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        top_registry = json.load(f)

    orphaned_skills = []
    missing_categories = []
    
    for cat in top_registry.get("categories", []):
        cat_id = cat["category_id"]
        cat_reg_path = Path(cat["registry_path"])
        cat_dir = ARCHIVED_SKILLS / cat_id
        
        if not cat_dir.exists():
            missing_categories.append(cat_id)
            continue
            
        if not cat_reg_path.exists():
            print(f"Category registry missing for {cat_id}")
            continue
            
        with open(cat_reg_path, "r", encoding="utf-8") as f:
            cat_registry = json.load(f)
            
        for skill in cat_registry.get("skills", []):
            # Paths in registry are usually like "skill-id/SKILL.md" or relative to the cat dir
            relative_skill_path = Path(skill["path"].replace("/SKILL.md", ""))
            skill_dir = cat_dir / relative_skill_path
            
            if not skill_dir.exists():
                orphaned_skills.append({
                    "id": skill["id"],
                    "category": cat_id,
                    "path": str(skill_dir)
                })

    results = {
        "orphaned_skills": orphaned_skills,
        "missing_categories": missing_categories
    }
    
    # Profile check
    if PROFILES_PATH.exists():
        with open(PROFILES_PATH, "r", encoding="utf-8") as f:
            profiles = json.load(f)
            
        orphan_ids = {s["id"] for s in orphaned_skills}
        found_in_profiles = {}
        
        for p_name, p_data in profiles.get("profiles", {}).items():
            for sid in p_data.get("skills", []):
                if sid in orphan_ids:
                    if p_name not in found_in_profiles:
                        found_in_profiles[p_name] = []
                    found_in_profiles[p_name].append(sid)
        
        results["found_in_profiles"] = found_in_profiles
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    check_skills()
