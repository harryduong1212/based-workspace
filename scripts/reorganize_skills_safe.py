import os
import re
import shutil
import json
from datetime import datetime
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).resolve().parent.parent
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

def reorganize():
    if not SKILLS_DIR.exists():
        print(f"Error: Skills directory not found at {SKILLS_DIR}")
        return

    if not ROOT_REGISTRY_JSON.exists():
        print(f"Error: Root registry not found at {ROOT_REGISTRY_JSON}")
        return

    # Load Category Configuration
    registry_data = json.loads(ROOT_REGISTRY_JSON.read_text(encoding="utf-8"))
    categories = registry_data.get("categories", [])
    
    # Initialize data structures for holding skills by category
    categorized_skills = {c["category_id"]: {"details": c, "skills": []} for c in categories}
    
    # Explicit mapping for hard-to-categorize edge cases
    explicit_map = {
        "custom-debrief": "documentation-writing",
        "custom-video-analyst": "workflow-automation-platforms",
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
        "mobile-games": "game-development"
    }

    # Gather all existing skills from the filesystem
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

    # Categorize skills automatically
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

    # Build Staging Directory
    if NEW_SKILLS_DIR.exists(): shutil.rmtree(NEW_SKILLS_DIR)
    NEW_SKILLS_DIR.mkdir(parents=True)

    total_count = 0
    # Process and move skills into new categorized folders
    for cat_id, data in categorized_skills.items():
        if not data["skills"]:
            continue
            
        cat_staging_path = NEW_SKILLS_DIR / cat_id
        cat_staging_path.mkdir(parents=True, exist_ok=True)
        
        for skill in data["skills"]:
            name = skill["name"]
            if name in all_skill_folders:
                shutil.copytree(all_skill_folders[name], cat_staging_path / name, dirs_exist_ok=True)
                total_count += 1
                skill["new_path"] = f".archived/skills/{cat_id}/{name}/SKILL.md"

        # Generate Per-Category Registry
        generate_category_registry(cat_id, data["details"]["category_name"], data["skills"], cat_staging_path)

    # Copy root files
    for item in SKILLS_DIR.iterdir():
        if item.is_file():
            shutil.copy2(item, NEW_SKILLS_DIR / item.name)

    if total_count == 0:
        print("Error: No skills found. Aborting swap.")
        return

    # Update SKILLS.md
    full_text = SKILLS_MD.read_text(encoding="utf-8")
    start_match = re.search(r"## .*Skills by Category\n+", full_text)
    end_match = re.search(r"## Finding Skills\n+", full_text)
    
    if start_match and end_match:
        header = full_text[:start_match.end()]
        
        new_md_lines = []
        for cat in categories:
            cat_id = cat["category_id"]
            cat_name = cat["category_name"]
            data = categorized_skills.get(cat_id)
            
            if not data or not data["skills"]:
                continue
                
            moved_skills = [s for s in data["skills"] if "new_path" in s]
            if not moved_skills: continue
            
            new_md_lines.append(f"### {cat_name}\n\n")
            new_md_lines.append("<details>\n")
            new_md_lines.append(f"<summary><b>{cat_name} (Click to expand)</b></summary>\n\n")
            new_md_lines.append("| Skill | Description |\n")
            new_md_lines.append("|---|---|\n")
            for s in sorted(moved_skills, key=lambda x: x["name"]):
                new_md_lines.append(f"| [{s['name']}]({s['new_path']}) | {s['desc']} |\n")
            new_md_lines.append("\n</details>\n\n")
            
        finding_skills = f"""## Finding Skills

All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** {total_count}
"""
        parts = full_text.split(end_match.group(0))
        post_footer = parts[1] if len(parts) > 1 else ""
        
        SKILLS_MD.write_text(header + "".join(new_md_lines) + finding_skills + post_footer, encoding="utf-8")
    else:
        print("Error: Could not find markers in SKILLS.md")

    # Final Swap
    backup_path = SKILLS_DIR.parent / (SKILLS_DIR.name + "_safe_backup_reorg")
    if backup_path.exists(): shutil.rmtree(backup_path)
    
    os.rename(SKILLS_DIR, backup_path)
    os.rename(NEW_SKILLS_DIR, SKILLS_DIR)
    
    print(f"Success! {total_count} skills reorganized automatically via domain tags.")

if __name__ == "__main__":
    reorganize()
