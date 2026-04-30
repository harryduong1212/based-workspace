import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
PROFILES_FILE = WORKSPACE_ROOT / "scripts/profiles.json"
ORPHANS_FILE = WORKSPACE_ROOT / "tmp/orphans.json"

def cleanup_profiles():
    if not ORPHANS_FILE.exists():
        print("Orphans file not found.")
        return

    with open(ORPHANS_FILE, "r", encoding="utf-8") as f:
        orphans_data = json.load(f)
    
    orphaned_ids = {s["id"] for s in orphans_data.get("orphaned_skills", [])}
    
    if not PROFILES_FILE.exists():
        print("Profiles file not found.")
        return
        
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles_data = json.load(f)
        
    for p_name, p_data in profiles_data.get("profiles", {}).items():
        original_skills = p_data.get("skills", [])
        p_data["skills"] = [sid for sid in original_skills if sid not in orphaned_ids]
        
        removed = len(original_skills) - len(p_data["skills"])
        if removed > 0:
            print(f"Updating profile '{p_name}': removed {removed} orphaned skills.")
            
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles_data, f, indent=2)

if __name__ == "__main__":
    cleanup_profiles()
