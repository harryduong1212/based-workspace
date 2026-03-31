import os
import re
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path
import tags_generator

# Configuration
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SKILLS_MD = ROOT_DIR / "SKILLS.md"
SKILLS_DIR = ROOT_DIR / ".archived" / "skills"
NEW_SKILLS_DIR = ROOT_DIR / ".archived" / "skills_reorganized"
ROOT_REGISTRY_JSON = SKILLS_DIR / "registry.json"

def get_desc(folder_path):
    md_path = Path(folder_path) / "SKILL.md"
    if md_path.exists():
        try:
            content = md_path.read_text(encoding="utf-8")
            desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
            if desc_match:
                return desc_match.group(1).strip().strip("'\"")
        except:
            pass
    return Path(folder_path).name.replace("-", " ").title()

def score_skill(skill_name, skill_desc, category):
    text = f"{skill_name.lower().replace('-', ' ')} {skill_desc.lower()}"
    words = set(re.findall(r'\b\w+\b', text))
    
    score = 0
    cat_id = category["category_id"]
    
    # Exact tag matches are weighted heavily
    for tag in category.get("domain_tags", []):
        tag_lower = tag.lower()
        if tag_lower in text:
            score += 5
        if tag_lower in words:
            score += 3
            
    # Keywords from the category name also help
    cat_words = set(re.findall(r'\b\w+\b', category["category_name"].lower()))
    for cw in cat_words:
        if len(cw) > 3 and cw in words:
            score += 2
            
    # Sub-string match for category ID just in case
    if cat_id in text or cat_id.replace("-", " ") in text:
        score += 4
        
    return score

def generate_category_registry(cat_slug, cat_name, skills, staging_path):
    registry = {
        "category_id": cat_slug,
        "category_name": cat_name,
        "skills": []
    }
    
    for skill in sorted(skills, key=lambda x: x["name"]):
        if "new_path" not in skill: continue
        
        desc = skill["desc"]
        triggers = []
        if "Triggers:" in desc:
            triggers = [t.strip().strip("'\"") for t in desc.split("Triggers:")[1].split(",")]
        elif "Use when" in desc:
            triggers = [w.strip(",") for w in desc.split() if len(w) > 4][:5]
            
        registry["skills"].append({
            "id": skill["name"],
            "description": desc,
            "path": f"{skill['name']}/SKILL.md",  # Local path within category
            "triggers": triggers,
            "tags": []  # To be filled later by generate_deep_tags.py if needed
        })
        
    registry_file = Path(staging_path) / "registry.json"
    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

def rebuild_skills_md():
    if not ROOT_REGISTRY_JSON.exists():
        print("Root registry missing, cannot rebuild SKILLS.md")
        return

    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    total_count = 0
    new_md_lines = []
    
    for cat in categories:
        cat_id = cat["category_id"]
        cat_name = cat["category_name"]
        
        cat_registry_path = SKILLS_DIR / cat_id / "registry.json"
        if not cat_registry_path.exists(): continue
        
        try:
            cat_reg = json.loads(cat_registry_path.read_text(encoding="utf-8"))
        except: continue
        
        skills = cat_reg.get("skills", [])
        if not skills: continue
        
        total_count += len(skills)
        
        new_md_lines.append(f"### {cat_name}\n\n")
        new_md_lines.append("<details>\n")
        new_md_lines.append(f"<summary><b>{cat_name} (Click to expand)</b></summary>\n\n")
        new_md_lines.append("| Skill | Description |\n")
        new_md_lines.append("|---|---|\n")
        for s in sorted(skills, key=lambda x: x.get("id", "")):
            new_path = f".archived/skills/{cat_id}/{s.get('path', '')}"
            new_md_lines.append(f"| [{s.get('id', '')}]({new_path}) | {s.get('description', '')} |\n")
        new_md_lines.append("\n</details>\n\n")

    full_text = SKILLS_MD.read_text(encoding="utf-8")
    start_match = re.search(r"## .*Skills by Category\n+", full_text)
    end_match = re.search(r"## Finding Skills\n+", full_text)
    
    if start_match and end_match:
        header = full_text[:start_match.end()]
        finding_skills = f"""## Finding Skills\n\nAll skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:\n\n**macOS / Linux:**\n```bash\nfind .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l\n```\n\n**Windows (PowerShell 7):**\n```powershell\nGet-ChildItem -Path ".archived\\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object\n```\n\n---\n\n> **Total Installed Skills:** {total_count}\n"""
        parts = full_text.split(end_match.group(0))
        post_footer = parts[1] if len(parts) > 1 else ""
        
        SKILLS_MD.write_text(header + "".join(new_md_lines) + finding_skills + post_footer, encoding="utf-8")
        print(f"Updated SKILLS.md with {total_count} skills natively.")
    else:
        print("Error: Could not find markers in SKILLS.md")

def process_target(target_path):
    target = Path(target_path)
    if not target.exists() or not target.is_dir() or not (target / "SKILL.md").exists():
        print(f"Error: Target {target_path} is not a valid skill folder (must contain SKILL.md).")
        return

    name = target.name
    desc = get_desc(target)

    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    best_score = -1
    best_cat = None
    for cat in categories:
        score = score_skill(name, desc, cat)
        if score > best_score:
            best_score = score
            best_cat = cat["category_id"]
            
    target_cat = best_cat if best_score > 0 and best_cat else "miscellaneous-other"
    dest_path = SKILLS_DIR / target_cat / name
    
    if dest_path.exists():
        print(f"Update: Skill {name} already exists in {target_cat}. Replacing it.")
        shutil.rmtree(dest_path)
        
    shutil.move(str(target), str(dest_path))
    print(f"Moved new skill '{name}' to '{target_cat}'.")
    
    cat_registry_path = SKILLS_DIR / target_cat / "registry.json"
    if cat_registry_path.exists():
        cat_reg = json.loads(cat_registry_path.read_text(encoding="utf-8"))
        
        triggers = []
        if "Triggers:" in desc:
            triggers = [t.strip().strip("'\"") for t in desc.split("Triggers:")[1].split(",")]
        elif "Use when" in desc:
            triggers = [w.strip(",") for w in desc.split() if len(w) > 4][:5]
            
        # Remove old entry if replacing
        cat_reg["skills"] = [s for s in cat_reg.get("skills", []) if s.get("id") != name]
        
        cat_reg["skills"].append({
            "id": name,
            "description": desc,
            "path": f"{name}/SKILL.md",
            "triggers": triggers,
            "tags": []
        })
        cat_reg["skills"] = sorted(cat_reg["skills"], key=lambda x: x.get("id", ""))
        cat_registry_path.write_text(json.dumps(cat_reg, indent=2, ensure_ascii=False), encoding="utf-8")
        
    rebuild_skills_md()
    print("Targeted ingestion complete.")

def reorganize_full():
    if not SKILLS_DIR.exists():
        print(f"Error: Skills directory not found at {SKILLS_DIR}")
        return

    if not ROOT_REGISTRY_JSON.exists():
        print(f"Error: Root registry not found at {ROOT_REGISTRY_JSON}")
        return

    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    categorized_skills = {c["category_id"]: {"details": c, "skills": []} for c in categories}
    
    explicit_map = {
        "debrief-teacher": "custom-skills",
        "exhaustive-video-note-taker": "custom-skills",
        "senior-architect": "architecture-patterns",
        "skill-creator": "ai-llm-agent-development",
        "advogado-criminal": "custom-skills",
        "leiloeiro-edital": "custom-skills",
        "leiloeiro-risco": "custom-skills",
        "leiloeiro-mercado": "custom-skills",
        "leiloeiro-avaliacao": "custom-skills",
        "leiloeiro-ia": "custom-skills",
        "junta-leiloeiros": "custom-skills",
        "carrier-relationship-management": "business-product-marketing",
        "backtesting-frameworks": "data-ml-engineering",
        "2d-games": "game-development",
        "3d-games": "game-development",
        "pc-games": "game-development",
        "web-games": "game-development",
        "mobile-games": "game-development",
        "workspace-analyzer": "custom-skills",
        "senior-architect-v2": "custom-skills"
    }

    all_skill_folders = {}
    for item in SKILLS_DIR.iterdir():
        if not item.is_dir() or item.name in [".git", "node_modules"]:
            continue
            
        if (item / "SKILL.md").exists():
            all_skill_folders[item.name] = item
        else:
            for sub in item.iterdir():
                if sub.is_dir() and (sub / "SKILL.md").exists():
                    all_skill_folders[sub.name] = sub

    for name, path in all_skill_folders.items():
        desc = get_desc(path)
        target_cat = "miscellaneous-other"
        
        if name in explicit_map and explicit_map[name] in categorized_skills:
            target_cat = explicit_map[name]
        else:
            best_score = -1
            best_cat = None
            for cat in categories:
                score = score_skill(name, desc, cat)
                if score > best_score:
                    best_score = score
                    best_cat = cat["category_id"]
                    
            if best_score > 0 and best_cat:
                target_cat = best_cat
                
        categorized_skills[target_cat]["skills"].append({"name": name, "desc": desc})

    if NEW_SKILLS_DIR.exists(): shutil.rmtree(NEW_SKILLS_DIR)
    NEW_SKILLS_DIR.mkdir(parents=True)

    total_count = 0
    reorganized_count = 0
    for cat_id, data in categorized_skills.items():
        if not data["skills"]:
            continue
            
        cat_staging_path = NEW_SKILLS_DIR / cat_id
        cat_staging_path.mkdir(parents=True, exist_ok=True)
        
        for skill in data["skills"]:
            name = skill["name"]
            if name in all_skill_folders:
                current_path = all_skill_folders[name]
                # Determine current category: relative to SKILLS_DIR, first parent
                try:
                    rel_parent = current_path.parent.relative_to(SKILLS_DIR)
                    current_cat = rel_parent.parts[0] if rel_parent.parts else None
                except ValueError:
                    current_cat = None # Skill was likely at root or outside SKILLS_DIR
                
                if current_cat != cat_id:
                    print(f"  [MOVE] {name:<40} {current_cat or 'ROOT'} -> {cat_id}")
                    reorganized_count += 1
                
                shutil.copytree(current_path, cat_staging_path / name, dirs_exist_ok=True)
                total_count += 1
                skill["new_path"] = f".archived/skills/{cat_id}/{name}/SKILL.md"

        generate_category_registry(cat_id, data["details"]["category_name"], data["skills"], cat_staging_path)

    for item in SKILLS_DIR.iterdir():
        if item.is_file():
            shutil.copy2(item, NEW_SKILLS_DIR / item.name)

    if total_count == 0:
        print("Error: No skills found. Aborting swap.")
        return

    backup_path = ROOT_DIR / "tmp" / "skills_backup"
    if backup_path.exists(): shutil.rmtree(backup_path)
    
    os.rename(SKILLS_DIR, backup_path)
    os.rename(NEW_SKILLS_DIR, SKILLS_DIR)
    
    print(f"Success! {total_count} skills processed, {reorganized_count} newly reallocated. Now rebuilding MD.")
    rebuild_skills_md()
    
    # Automatically restore tags
    print("\nRunning Deep Tag Extraction...")
    tags_generator.run_tag_extraction("skills", argparse.Namespace(dry_run=False, category=None, type="skills"))

def main():
    parser = argparse.ArgumentParser(description="Reorganize skills safely.")
    parser.add_argument("--target", type=str, help="Path to a single skill folder inside /tmp/ to ingest and insert without reorganizing the whole ecosystem.")
    args = parser.parse_args()
    
    if args.target:
        process_target(args.target)
    else:
        reorganize_full()

if __name__ == "__main__":
    main()
