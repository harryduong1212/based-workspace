import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
WORKFLOWS_ARCHIVE = WORKSPACE_ROOT / ".archived/workflows"
PROFILES_FILE = WORKSPACE_ROOT / "scripts/profiles.json"

def get_discrepancies():
    top_registry_path = WORKFLOWS_ARCHIVE / "registry.json"
    if not top_registry_path.exists():
        return {"error": "Top level registry not found"}
        
    with open(top_registry_path, "r", encoding="utf-8") as f:
        top_reg = json.load(f)
        
    orphaned_workflows = []
    missing_categories = []
    
    for cat in top_reg.get("categories", []):
        cat_reg_path = WORKSPACE_ROOT / cat["registry_path"]
        if not cat_reg_path.exists():
            missing_categories.append(cat["category_id"])
            continue
            
        with open(cat_reg_path, "r", encoding="utf-8") as f:
            cat_reg = json.load(f)
            
        cat_dir = cat_reg_path.parent
        for wf in cat_reg.get("workflows", []):
            wf_path = cat_dir / wf["id"] if not wf["path"].endswith(".md") else cat_dir / wf["path"]
            if not wf_path.exists():
                orphaned_workflows.append({
                    "id": wf["id"],
                    "category": cat["category_id"],
                    "registry_path": str(cat_reg_path.relative_to(WORKSPACE_ROOT))
                })
                
    return {
        "orphaned_workflows": orphaned_workflows,
        "missing_categories": missing_categories
    }

if __name__ == "__main__":
    results = get_discrepancies()
    print(json.dumps(results, indent=2))
