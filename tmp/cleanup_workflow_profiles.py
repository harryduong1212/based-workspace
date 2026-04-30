import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
PROFILES_FILE = WORKSPACE_ROOT / "scripts/profiles.json"
WORKFLOWS_ARCHIVE = WORKSPACE_ROOT / ".archived/workflows"

def get_valid_workflows():
    valid_wf_ids = set()
    top_registry_path = WORKFLOWS_ARCHIVE / "registry.json"
    if not top_registry_path.exists():
        return valid_wf_ids
        
    with open(top_registry_path, "r", encoding="utf-8") as f:
        top_reg = json.load(f)
        
    for cat in top_reg.get("categories", []):
        cat_reg_path = WORKSPACE_ROOT / cat["registry_path"]
        if not cat_reg_path.exists():
            continue
            
        with open(cat_reg_path, "r", encoding="utf-8") as f:
            cat_reg = json.load(f)
            
        cat_dir = cat_reg_path.parent
        for wf in cat_reg.get("workflows", []):
            wf_path = cat_dir / wf["id"] if not wf["path"].endswith(".md") else cat_dir / wf["path"]
            if wf_path.exists():
                valid_wf_ids.add(wf["id"])
    return valid_wf_ids

def cleanup_profiles():
    valid_wf_ids = get_valid_workflows()
    print(f"Found {len(valid_wf_ids)} valid workflows in registries.")
    
    if not PROFILES_FILE.exists():
        return
        
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        profiles_data = json.load(f)
        
    for p_name, p_data in profiles_data.get("profiles", {}).items():
        original_workflows = p_data.get("workflows", [])
        new_workflows = [wid for wid in original_workflows if wid in valid_wf_ids]
        
        if len(new_workflows) != len(original_workflows):
            p_data["workflows"] = new_workflows
            print(f"Updated profile '{p_name}': removed {len(original_workflows) - len(new_workflows)} missing workflows.")
            
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles_data, f, indent=2)
    print("profiles.json updated.")

if __name__ == "__main__":
    cleanup_profiles()
