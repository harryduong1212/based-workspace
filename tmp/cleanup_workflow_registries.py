import json
import os
from pathlib import Path
from datetime import datetime

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
WORKFLOWS_ARCHIVE = WORKSPACE_ROOT / ".archived/workflows"
TOP_REGISTRY = WORKFLOWS_ARCHIVE / "registry.json"

def cleanup_registries():
    # 1. Load orphaned data
    with open(WORKSPACE_ROOT / "tmp/workflow_orphans_data.json", "r", encoding="utf-8") as f:
        orphans_data = json.load(f)
    
    orphaned_ids = {wf["id"] for wf in orphans_data.get("orphaned_workflows", [])}
    missing_categories = set(orphans_data.get("missing_categories", []))
    
    # 2. Update top-level registry
    if TOP_REGISTRY.exists():
        with open(TOP_REGISTRY, "r", encoding="utf-8") as f:
            top_reg = json.load(f)
        
        original_count = len(top_reg.get("categories", []))
        top_reg["categories"] = [c for c in top_reg["categories"] if c["category_id"] not in missing_categories]
        top_reg["last_updated"] = datetime.utcnow().isoformat() + "Z"
        
        with open(TOP_REGISTRY, "w", encoding="utf-8") as f:
            json.dump(top_reg, f, indent=2)
        print(f"Updated top-level registry: removed {original_count - len(top_reg['categories'])} categories.")

    # 3. Update category-level registries
    for cat_dir in WORKFLOWS_ARCHIVE.iterdir():
        if not cat_dir.is_dir() or cat_dir.name in missing_categories:
            continue
            
        reg_path = cat_dir / "registry.json"
        if not reg_path.exists():
            continue
            
        with open(reg_path, "r", encoding="utf-8") as f:
            cat_reg = json.load(f)
            
        original_wf_count = len(cat_reg.get("workflows", []))
        cat_reg["workflows"] = [wf for wf in cat_reg["workflows"] if wf["id"] not in orphaned_ids]
        
        if len(cat_reg["workflows"]) != original_wf_count:
            with open(reg_path, "w", encoding="utf-8") as f:
                json.dump(cat_reg, f, indent=2)
            print(f"Updated {cat_dir.name}/registry.json: removed {original_wf_count - len(cat_reg['workflows'])} workflows.")

if __name__ == "__main__":
    cleanup_registries()
