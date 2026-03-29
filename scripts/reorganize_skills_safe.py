import os
import re
import shutil
import json
from datetime import datetime

# Configuration
ROOT_DIR = r"h:\WORKSPACE\Personal\Vibe\based-workspace"
SKILLS_MD = os.path.join(ROOT_DIR, "SKILLS.md")
SKILLS_DIR = os.path.join(ROOT_DIR, ".archived", "skills")
NEW_SKILLS_DIR = os.path.join(ROOT_DIR, ".archived", "skills_reorganized")

def slugify(text):
    text = re.sub(r"[\U00010000-\U0010ffff]", "", text) # Remove emojis
    text = text.lower().replace(" & ", "-").replace(",", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")

def get_desc(folder_path):
    md_path = os.path.join(folder_path, "SKILL.md")
    if os.path.exists(md_path):
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
            if desc_match:
                return desc_match.group(1).strip().strip("'\"")
        except:
            pass
    return os.path.basename(folder_path).replace("-", " ").title()

def generate_registry_json(categories, total_count):
    registry = {
        "version": "1.0.0",
        "type": "skill_registry",
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": []
    }
    
    for cat_header, data in categories.items():
        if not data["skills"]: continue
        
        category = {
            "category_id": data["slug"],
            "category_name": cat_header,
            "skills": []
        }
        
        for skill in sorted(data["skills"], key=lambda x: x["name"]):
            if "new_path" not in skill: continue
            
            desc = skill["desc"]
            triggers = []
            if "Triggers:" in desc:
                triggers = [t.strip().strip("'\"") for t in desc.split("Triggers:")[1].split(",")]
            elif "Use when" in desc:
                triggers = [w.strip(",") for w in desc.split() if len(w) > 4][:5]
                
            category["skills"].append({
                "id": skill["name"],
                "description": desc,
                "path": skill["new_path"],
                "triggers": triggers,
                "dependencies": []
            })
            
        if category["skills"]:
            registry["categories"].append(category)
        
    with open(os.path.join(NEW_SKILLS_DIR, "registry.json"), "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

def reorganize():
    if not os.path.exists(SKILLS_DIR):
        print("Error: Skills directory not found.")
        return

    with open(SKILLS_MD, "r", encoding="utf-8") as f:
        full_text = f.read()
    
    lines = full_text.splitlines()

    categories = {}
    current_cat = None
    cat_order = []

    # 1. Parse existing categories and skills from SKILLS.md
    for line in lines:
        cat_match = re.match(r"^###(?:[^\w]*)(.*)$", line)
        if cat_match:
            cat_name_raw = cat_match.group(1).strip()
            original_header = line.replace("###", "").strip()
            current_cat = original_header
            categories[current_cat] = {"slug": slugify(cat_name_raw), "skills": []}
            cat_order.append(current_cat)
        
        if current_cat:
            row_match = re.match(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*(.*?)\s*\|$", line)
            if row_match:
                skill_name = row_match.group(1).strip()
                categories[current_cat]["skills"].append({"name": skill_name, "desc": row_match.group(3).strip()})

    if "📦 Miscellaneous / Other" not in categories:
        categories["📦 Miscellaneous / Other"] = {"slug": "miscellaneous-other", "skills": []}
        cat_order.append("📦 Miscellaneous / Other")

    documented_skills = {s["name"] for cat in categories.values() for s in cat["skills"]}

    # 2. Index all actual physical folders
    all_skill_folders = {} 
    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(item_path) or item in [".git", "node_modules"]:
            continue
        
        # Check if it's already a category folder (slug)
        is_slug = any(item == cat["slug"] for cat in categories.values())
        if is_slug:
            for sub in os.listdir(item_path):
                sub_path = os.path.join(item_path, sub)
                if os.path.isdir(sub_path):
                    all_skill_folders[sub] = sub_path
        else:
            all_skill_folders[item] = item_path

    # 3. Categorize undocumented skills
    explicit_map = {
        "custom-debrief": "📚 Documentation & Writing",
        "custom-video-analyst": "🛠️ Workflow & Automation Platforms",
        "senior-architect": "🏗️ Architecture & Patterns",
        "skill-creator": "🤖 AI, LLM & Agent Development",
    }

    for name, path in all_skill_folders.items():
        if name not in documented_skills:
            desc = get_desc(path)
            target_cat = "📦 Miscellaneous / Other"
            if name in explicit_map: target_cat = explicit_map[name]
            categories[target_cat]["skills"].append({"name": name, "desc": desc})

    # 4. Build Staging Directory
    if os.path.exists(NEW_SKILLS_DIR): shutil.rmtree(NEW_SKILLS_DIR)
    os.makedirs(NEW_SKILLS_DIR)

    total_count = 0
    for cat_name in cat_order:
        data = categories[cat_name]
        cat_staging_path = os.path.join(NEW_SKILLS_DIR, data["slug"])
        os.makedirs(cat_staging_path, exist_ok=True)
        
        for skill in data["skills"]:
            name = skill["name"]
            if name in all_skill_folders:
                shutil.copytree(all_skill_folders[name], os.path.join(cat_staging_path, name), dirs_exist_ok=True)
                total_count += 1
                skill["new_path"] = f".archived/skills/{data['slug']}/{name}/SKILL.md"

    # Generate Registry JSON
    generate_registry_json(categories, total_count)

    # 5. Copy root files
    for item in os.listdir(SKILLS_DIR):
        if os.path.isfile(os.path.join(SKILLS_DIR, item)):
            shutil.copy2(os.path.join(SKILLS_DIR, item), os.path.join(NEW_SKILLS_DIR, item))

    # 6. Safety Check
    if total_count == 0:
        print("Error: No skills found. Aborting swap.")
        return

    # 7. Update SKILLS.md
    new_md_lines = []
    for cat_name in cat_order:
        data = categories[cat_name]
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

    # Flexible Markers
    start_match = re.search(r"## .*Skills by Category\n+", full_text)
    end_match = re.search(r"## Finding Skills\n+", full_text)
    
    if start_match and end_match:
        header = full_text[:start_match.end()]
        footer_start = end_match.start()
        
        finding_skills = f"""## Finding Skills

All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**PowerShell:**
```powershell
Get-ChildItem -Path ".archived\\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** {total_count}
"""
        # We replace the whole block from end of start_match to end of file (or footer)
        # But we need to preserve whatever was after Finding Skills?
        # Actually the script previously used split(end_marker)[1]
        
        parts = full_text.split(end_match.group(0))
        post_footer = parts[1] if len(parts) > 1 else ""
        
        with open(SKILLS_MD, "w", encoding="utf-8") as f:
            f.write(header + "".join(new_md_lines) + finding_skills + post_footer)
    else:
        print("Error: Could not find markers in SKILLS.md")

    # 8. Final Swap
    backup_path = SKILLS_DIR + "_safe_backup_reorg"
    if os.path.exists(backup_path): shutil.rmtree(backup_path)
    os.rename(SKILLS_DIR, backup_path)
    os.rename(NEW_SKILLS_DIR, SKILLS_DIR)
    
    print(f"Success! {total_count} skills reorganized safely.")

if __name__ == "__main__":
    reorganize()
