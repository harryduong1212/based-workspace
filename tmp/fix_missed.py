import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
RESOURCES_DIR = WORKSPACE_ROOT / "scripts/resources"
PROFILES_FILE = WORKSPACE_ROOT / "scripts/profiles.json"
SKILLS_MD = WORKSPACE_ROOT / "docs/SKILLS.md"

TO_REMOVE = {"scanning-tools", "cc-skill-continuous-learning"}

def fix_missed():
    # 1. profiles.json
    if PROFILES_FILE.exists():
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            profiles_data = json.load(f)
        for p_name, p_data in profiles_data.get("profiles", {}).items():
            original_skills = p_data.get("skills", [])
            p_data["skills"] = [sid for sid in original_skills if sid not in TO_REMOVE]
        with open(PROFILES_FILE, "w", encoding="utf-8") as f:
            json.dump(profiles_data, f, indent=2)
            
    # 2. Resources mappings
    mapping_files = [
        "domain_to_skills_mapping.json", 
        "domain_sub_domain_to_skills_mapping.json", 
        "based_skills_registry.json"
    ]
    for resource_name in mapping_files:
        resource_path = RESOURCES_DIR / resource_name
        if not resource_path.exists():
            continue
            
        with open(resource_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if resource_name == "based_skills_registry.json":
            data["skills"] = [s for s in data.get("skills", []) if s["id"] not in TO_REMOVE]
        elif resource_name == "domain_to_skills_mapping.json":
            for domain, skills in data.items():
                data[domain] = [s for s in skills if s not in TO_REMOVE]
        elif resource_name == "domain_sub_domain_to_skills_mapping.json":
            for domain, subdomains in data.items():
                for sub, skills in subdomains.items():
                    subdomains[sub] = [s for s in skills if s not in TO_REMOVE]
                    
        with open(resource_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # 3. docs/SKILLS.md
    if SKILLS_MD.exists():
        with open(SKILLS_MD, "r", encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        import re
        for line in lines:
            match = re.search(r"\| \[(.*?)\]\(.*?\)", line)
            if match and match.group(1) in TO_REMOVE:
                continue
            new_lines.append(line)
        with open(SKILLS_MD, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
if __name__ == "__main__":
    fix_missed()
