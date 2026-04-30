import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
RESOURCES_DIR = WORKSPACE_ROOT / "scripts/resources"
ORPHANS_FILE = WORKSPACE_ROOT / "tmp/orphans.json"

def cleanup_resources():
    if not ORPHANS_FILE.exists():
        print("Orphans file not found.")
        return

    with open(ORPHANS_FILE, "r", encoding="utf-8") as f:
        orphans_data = json.load(f)
    
    orphaned_ids = {s["id"] for s in orphans_data.get("orphaned_skills", [])}
    
    for resource_name in [
        "domain_to_skills_mapping.json", 
        "domain_sub_domain_to_skills_mapping.json", 
        "based_skills_registry.json"
    ]:
        resource_path = RESOURCES_DIR / resource_name
        if not resource_path.exists():
            print(f"Resource {resource_name} not found.")
            continue
            
        with open(resource_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if resource_name == "based_skills_registry.json":
            original_count = len(data.get("skills", []))
            data["skills"] = [s for s in data.get("skills", []) if s["id"] not in orphaned_ids]
            removed = original_count - len(data["skills"])
        elif resource_name == "domain_to_skills_mapping.json":
            removed = 0
            for domain, skills in data.items():
                original_count = len(skills)
                data[domain] = [s for s in skills if s not in orphaned_ids]
                removed += original_count - len(data[domain])
        elif resource_name == "domain_sub_domain_to_skills_mapping.json":
            removed = 0
            for domain, subdomains in data.items():
                for sub, skills in subdomains.items():
                    original_count = len(skills)
                    subdomains[sub] = [s for s in skills if s not in orphaned_ids]
                    removed += original_count - len(subdomains[sub])
            
        if removed > 0:
            print(f"Updating resource '{resource_name}': removed {removed} orphaned entries.")
            with open(resource_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

if __name__ == "__main__":
    cleanup_resources()
