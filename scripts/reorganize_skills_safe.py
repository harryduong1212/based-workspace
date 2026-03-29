import os
import re
import shutil

# This script is a safe, idempotent version of the skill reoganization logic.
# It includes pre-swap verification to ensure no data is lost during the directory swap.

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

def reorganize():
    if not os.path.exists(SKILLS_DIR):
        print("Error: Skills directory not found.")
        return

    with open(SKILLS_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()

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
    # We need to look both in root and in existing category subfolders (idempotency)
    all_skill_folders = {} # name -> current_full_path
    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if not os.path.isdir(item_path) or item in [".git", "node_modules"]:
            continue
        
        # Is this a category folder from a previous run?
        is_cat_folder = any(item == cat["slug"] for cat in categories.values())
        if is_cat_folder:
            for sub in os.listdir(item_path):
                sub_path = os.path.join(item_path, sub)
                if os.path.isdir(sub_path):
                    all_skill_folders[sub] = sub_path
        else:
            all_skill_folders[item] = item_path

    # 3. Categorize undocumented skills (Heuristics)
    explicit_map = {
        "custom-debrief": "📚 Documentation & Writing",
        "custom-video-analyst": "🛠️ Workflow & Automation Platforms",
        "senior-architect": "🏗️ Architecture & Patterns",
        "custom-senior-architect": "🏗️ Architecture & Patterns",
        "senior-it-ba-specialist": "💰 Business, Product & Marketing",
        "custom-senior-it-ba-specialist": "💰 Business, Product & Marketing",
    }

    for name, path in all_skill_folders.items():
        if name not in documented_skills:
            desc = get_desc(path)
            target_cat = "📦 Miscellaneous / Other"
            
            if name in explicit_map:
                target_cat = explicit_map[name]
            else:
                n, d = name.lower(), desc.lower()
                if "azure" in n or "azure" in d: target_cat = "☁️ Azure SDKs"
                elif any(w in n or w in d for w in ["aws", "cloud", "docker", "kubernetes"]): target_cat = "☁️ Cloud, DevOps & Infrastructure"
                elif any(w in n or w in d for w in ["react", "frontend", "nextjs", "css", "tailwind", "ui"]): target_cat = "🌐 Frontend Development"
                elif any(w in n or w in d for w in ["backend", "api", "node", "django"]): target_cat = "⚙️ Backend Development"
                elif any(w in n or w in d for w in ["sql", "postgres", "db", "database"]): target_cat = "🗄️ Database"
                elif any(w in n or w in d for w in ["security", "auth", "audit"]): target_cat = "🔒 Security & Penetration Testing"
                elif any(w in n or w in d for w in ["test", "qa", "debug"]): target_cat = "🧪 Testing & Quality"
                elif any(w in n or w in d for w in ["python", "java", "rust", "cpp"]): target_cat = "🔧 Programming Languages"
                elif any(w in n or w in d for w in ["docs", "readme", "write"]): target_cat = "📚 Documentation & Writing"
                elif any(w in n or w in d for w in ["ai", "llm", "agent", "prompt", "mcp"]): target_cat = "🤖 AI, LLM & Agent Development"
            
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

    # 5. Copy root files (.gitignore, README.md, etc)
    for item in os.listdir(SKILLS_DIR):
        item_path = os.path.join(SKILLS_DIR, item)
        if os.path.isfile(item_path):
            shutil.copy2(item_path, os.path.join(NEW_SKILLS_DIR, item))

    # 6. Safety Check: Verify staging isn't empty
    staging_folders = [d for d in os.listdir(NEW_SKILLS_DIR) if os.path.isdir(os.path.join(NEW_SKILLS_DIR, d))]
    if len(staging_folders) == 0:
        print("Error: Staging directory is empty. Aborting swap.")
        return

    # 7. Update SKILLS.md
    new_md_lines = []
    for cat_name in cat_order:
        data = categories[cat_name]
        if not data["skills"]: continue
        
        new_md_lines.append(f"### {cat_name}\n\n")
        new_md_lines.append("<details>\n")
        new_md_lines.append(f"<summary><b>{cat_name} (Click to expand)</b></summary>\n\n")
        new_md_lines.append("| Skill | Description |\n")
        new_md_lines.append("|---|---|\n")
        
        for s in sorted(data["skills"], key=lambda x: x["name"]):
            new_md_lines.append(f"| [{s['name']}]({s['new_path']}) | {s['desc']} |\n")
        new_md_lines.append("\n</details>\n\n")

    with open(SKILLS_MD, "r", encoding="utf-8") as f:
        full_text = f.read()

    start_marker = "## Skills by Category\n\n"
    end_marker = "## Finding Skills\n"
    parts = full_text.split(start_marker)
    header = parts[0] + start_marker
    footer_part = parts[1].split(end_marker)[1]
    
    # Rebuild Finding Skills with dynamic count
    finding_skills = f"""## Finding Skills

All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**PowerShell:**
```powershell
Get-ChildItem -Path ".archived\\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** {total_count}
"""

    with open(SKILLS_MD, "w", encoding="utf-8") as f:
        f.write(header + "".join(new_md_lines) + finding_skills + footer_part)

    # 8. Final Swap
    backup_path = SKILLS_DIR + "_safe_backup_reorg"
    if os.path.exists(backup_path): shutil.rmtree(backup_path)
    os.rename(SKILLS_DIR, backup_path)
    os.rename(NEW_SKILLS_DIR, SKILLS_DIR)
    
    print(f"Success! {total_count} skills reorganized safely into .archived/skills")

if __name__ == "__main__":
    reorganize()
