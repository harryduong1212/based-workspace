import os
import re
import shutil
import json
from datetime import datetime

# Configuration
ROOT_DIR = r"h:\WORKSPACE\Personal\Vibe\based-workspace"
WORKFLOWS_DIR = os.path.join(ROOT_DIR, ".archived", "workflows")
STAGING_DIR = os.path.join(ROOT_DIR, ".archived", "workflows_reorganized")
WORKFLOWS_MD = os.path.join(ROOT_DIR, "WORKFLOWS.md")

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def get_workflows_mapping():
    if not os.path.exists(WORKFLOWS_MD):
        return {}
    with open(WORKFLOWS_MD, "r", encoding="utf-8") as f:
        full_content = f.read()
    
    mapping = {} 
    # Use split instead of findall for robustness, with multiline support
    sections = re.split(r'^### (.*)$', full_content, flags=re.MULTILINE)
    
    for i in range(1, len(sections), 2):
        cat_name = sections[i].strip()
        body = sections[i+1]
        
        # Regex to find links, capturing the workflow_id from the path
        # [Name](.archived/workflows/category/workflow_id/WORKFLOW.md)
        # OR [Name](.archived/workflows/filename.md)
        # We look for the part right before WORKFLOW.md OR the filename itself
        links = re.findall(r'\[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(.*?)\)', body)
        
        if links:
            ids = []
            for name, relative_path in links:
                # relative_path might be "category/id/WORKFLOW.md" or "filename.md"
                path_parts = relative_path.strip("/").split("/")
                if path_parts[-1] == "WORKFLOW.md":
                    # The ID is the folder name just above WORKFLOW.md
                    if len(path_parts) >= 2:
                        ids.append(path_parts[-2] + ".md")
                else:
                    # It's a flat filename
                    ids.append(path_parts[-1])
            mapping[cat_name] = ids
            
    return mapping

def generate_registry_json(mapping, original_content):
    registry = {
        "version": "1.0.0",
        "type": "workflow_registry",
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": []
    }
    
    for cat_name in sorted(mapping.keys()):
        cat_slug = slugify(cat_name)
        category = {
            "category_id": cat_slug,
            "category_name": cat_name,
            "workflows": []
        }
        
        for filename in sorted(mapping[cat_name]):
            workflow_id = filename.replace(".md", "")
            # Robust search for description and slash command
            # Escape workflow_id for regex
            esc_id = re.escape(workflow_id)
            # Match | [Name](path/to/esc_id/...) | /slash | Status | Desc |
            row_pattern = rf'\| \[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(?:.*?){esc_id}(?:/WORKFLOW\.md|\.md)\) \| ([^|]+) \| ([^|]*?) \| ([^|]*?)? \|'
            match = re.search(row_pattern, original_content)
            
            description = ""
            triggers = []
            if match:
                # If there are 4 columns (new format) or 3 (old format)
                # We need to be careful. The format I'm generating has 4 columns.
                slash = match.group(2).strip()
                desc = match.group(4).strip() if match.group(4) else match.group(3).strip()
                triggers = [slash.replace("/", "").replace("`", "")]
                description = desc
            
            category["workflows"].append({
                "id": workflow_id,
                "description": description,
                "path": f".archived/workflows/{cat_slug}/{workflow_id}/WORKFLOW.md",
                "triggers": triggers,
                "required_skills": [],
                "entry_point": None
            })
        
        if category["workflows"]:
            registry["categories"].append(category)
            
    with open(os.path.join(STAGING_DIR, "registry.json"), "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

def reorganize():
    mapping = get_workflows_mapping()
    
    # 1. Prepare clean staging area
    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
    os.makedirs(STAGING_DIR)
    
    # 2. Index all actual physical files
    all_files = {} 
    for root, dirs, files in os.walk(WORKFLOWS_DIR):
        for f in files:
            if f.endswith(".md") and " copy" not in f:
                if f == "WORKFLOW.md":
                    wf_id = os.path.basename(root)
                    all_files[wf_id + ".md"] = os.path.join(root, f)
                else:
                    all_files[f] = os.path.join(root, f)
    
    moved_filenames = set()
    
    # 3. Copy files to category folders in staging
    for cat_name, file_list in mapping.items():
        cat_slug = slugify(cat_name)
        cat_staging_path = os.path.join(STAGING_DIR, cat_slug)
        os.makedirs(cat_staging_path, exist_ok=True)
        
        for filename in file_list:
            if filename in all_files:
                workflow_id = filename.replace(".md", "")
                wf_folder = os.path.join(cat_staging_path, workflow_id)
                os.makedirs(wf_folder, exist_ok=True)
                shutil.copy2(all_files[filename], os.path.join(wf_folder, "WORKFLOW.md"))
                moved_filenames.add(filename)
                
    # 4. Handle miscellaneous
    misc_path = os.path.join(STAGING_DIR, "miscellaneous")
    for filename, full_path in all_files.items():
        if filename not in moved_filenames:
            if not os.path.exists(misc_path): os.makedirs(misc_path)
            workflow_id = filename.replace(".md", "")
            wf_folder = os.path.join(misc_path, workflow_id)
            os.makedirs(wf_folder, exist_ok=True)
            shutil.copy2(full_path, os.path.join(wf_folder, "WORKFLOW.md"))

    # 5. Reconstruct WORKFLOWS.md content
    with open(WORKFLOWS_MD, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    generate_registry_json(mapping, original_content)
        
    total_workflows = sum(len(v) for v in mapping.values())
    
    header_part = f"""# Antigravity Workflows 🚀

**Stack-agnostic, question-driven workflows for the Antigravity IDE.**

> Sourced from [antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)

---

## ⚡ Quick Start

Trigger any workflow by typing its slash command in the chat:

| Feature | Commands |
|---|---|
| **Project Setup** | `/new-project`, `/new-component`, `/new-api` |
| **Git Automation** | `/git-commit`, `/git-pr`, `/git-conflict` |
| **Testing** | `/unit-test`, `/e2e-test`, `/playwright-test` |
| **Deployment** | `/deploy`, `/docker`, `/railway-deploy` |

---

## 🛠️ Companion Tools

Need to extend the workspace? Use these specialized creators:

| Tool | Command | Description |
|---|---|---|
| **Workflow Creator** | `/workflow-creator` | Build new multi-step developer workflows |
| **Skill Creator** | `/skill-creator` | Create specialized expert knowledge modules |

---

## 🏗️ Philosophy

| Principle | Description |
|---|---|
| **Stack-Agnostic** | Works with React, Vue, Angular, Django, or any stack |
| **Question-Driven** | Asks clarifying questions for better results |
| **Progressive Disclosure** | Loads minimal context first, expands on demand |
| **Single Responsibility** | Each workflow does ONE thing well |
| **Composable** | Combine workflows for complex tasks |

---

## 📂 Available Workflows ({total_workflows})
"""
    
    new_sections = []
    for cat_name in sorted(mapping.keys()):
        file_list = mapping[cat_name]
        cat_slug = slugify(cat_name)
        
        section = f"\n### {cat_name}\n"
        section += f"<details>\n\n"
        section += "| Workflow | Command | Status | Description |\n"
        section += "|---|---|---|---|\n"
        
        for filename in sorted(file_list):
            workflow_id = filename.replace(".md", "")
            esc_id = re.escape(workflow_id)
            row_pattern = rf'\| \[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(?:.*?){esc_id}(?:/WORKFLOW\.md|\.md)\) \| ([^|]+) \| ([^|]*?) \| ([^|]*?)? \|'
            match = re.search(row_pattern, original_content)
            
            if match:
                display_name = match.group(1).strip()
                slash = match.group(2).strip()
                desc = match.group(4).strip() if match.group(4) else match.group(3).strip()
                status = "✅ Ready" if not filename.startswith("custom-") else "🚧 Custom"
                section += f"| [{display_name}](.archived/workflows/{cat_slug}/{workflow_id}/WORKFLOW.md) | {slash} | {status} | {desc} |\n"
        
        section += "\n</details>\n"
        new_sections.append(section)
        
    footer = f"""
---

## 🤝 Contributing

To add a new workflow:
1. Stage your file in `.archived/workflows/` (root).
2. Register it in the `WORKFLOWS.md` tables.
3. Run the reorganization script: `python scripts/reorganize_workflows_safe.py`.

---

> **Repo:** [github.com/harikrishna8121999/antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)
"""

    with open(WORKFLOWS_MD, "w", encoding="utf-8") as f:
        f.write(header_part.strip() + "\n" + "".join(new_sections) + footer)
        
    total_wf_files = 0
    for r, d, files in os.walk(STAGING_DIR):
        if "WORKFLOW.md" in files: total_wf_files += 1

    if total_wf_files == 0:
        print("Error: Staging directory contains no workflows. Aborting swap.")
        return

    final_backup = WORKFLOWS_DIR + "_old_before_reorg"
    if os.path.exists(final_backup): shutil.rmtree(final_backup)
    os.rename(WORKFLOWS_DIR, final_backup)
    os.rename(STAGING_DIR, WORKFLOWS_DIR)
    print(f"Reorganization success! {total_wf_files} workflows safely synchronized.")

if __name__ == "__main__":
    reorganize()
