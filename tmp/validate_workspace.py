import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
PROFILES_FILE = WORKSPACE_ROOT / "scripts/profiles.json"
SKILLS_ARCHIVE = WORKSPACE_ROOT / ".archived/skills"
WORKFLOWS_ARCHIVE = WORKSPACE_ROOT / ".archived/workflows"

def load_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def check_sync():
    # 1. Load all known skills from registries
    all_skills = set()
    for cat_dir in SKILLS_ARCHIVE.iterdir():
        if cat_dir.is_dir():
            reg_file = cat_dir / "registry.json"
            if reg_file.exists():
                cat_data = load_json(reg_file)
                for s in cat_data.get("skills", []):
                    all_skills.add(s["id"])

    # 2. Load all known workflows from registries
    all_workflows = set()
    if WORKFLOWS_ARCHIVE.exists():
        for cat_dir in WORKFLOWS_ARCHIVE.iterdir():
            if cat_dir.is_dir():
                reg_file = cat_dir / "registry.json"
                if reg_file.exists():
                    cat_data = load_json(reg_file)
                    for w in cat_data.get("workflows", []):
                        all_workflows.add(w["id"])

    # 3. Check profiles.json references
    if not PROFILES_FILE.exists():
        print("profiles.json not found!")
        return

    profiles_data = load_json(PROFILES_FILE)
    profiles = profiles_data.get("profiles", {})
    
    missing_skills_in_profiles = set()
    missing_workflows_in_profiles = set()
    missing_extends = set()
    
    for p_name, p_data in profiles.items():
        for skill in p_data.get("skills", []):
            if skill not in all_skills:
                print(f"Profile '{p_name}' references missing skill: {skill}")
                missing_skills_in_profiles.add(skill)
                
        for wf in p_data.get("workflows", []):
            if wf not in all_workflows:
                print(f"Profile '{p_name}' references missing workflow: {wf}")
                missing_workflows_in_profiles.add(wf)
                
        for ext in p_data.get("extends", []):
            if ext not in profiles:
                print(f"Profile '{p_name}' extends missing profile: {ext}")
                missing_extends.add(ext)

    if not missing_skills_in_profiles and not missing_workflows_in_profiles and not missing_extends:
        print("profiles.json is FULLY SYNCED with registries.")
        
    # Check domain_to_skills_mapping
    mapping_files = [
        "scripts/resources/domain_to_skills_mapping.json",
        "scripts/resources/domain_sub_domain_to_skills_mapping.json",
        "scripts/resources/based_skills_registry.json"
    ]
    
    for file in mapping_files:
        p = WORKSPACE_ROOT / file
        if p.exists():
            data = load_json(p)
            found_missing = False
            # Quick scanning logic depending on file struct
            if "based" in file:
                for s in data.get("skills", []):
                    if s["id"] not in all_skills:
                        print(f"{file} references missing skill: {s['id']}")
                        found_missing = True
            elif "sub_domain" in file: # nested dict
                for d, subs in data.items():
                    for s, skills in subs.items():
                        for sk in skills:
                            if sk not in all_skills:
                                print(f"{file} references missing skill: {sk}")
                                found_missing = True
            else: # flat dict
                for d, skills in data.items():
                    for sk in skills:
                        if sk not in all_skills:
                            print(f"{file} references missing skill: {sk}")
                            found_missing = True
                            
            if not found_missing:
                print(f"{file} is FULLY SYNCED.")

if __name__ == "__main__":
    check_sync()
