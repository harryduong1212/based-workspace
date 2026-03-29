import os
import re
import shutil
import json
from datetime import datetime
from pathlib import Path

# Configuration
ROOT_DIR = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = ROOT_DIR / ".archived" / "workflows"
STAGING_DIR = ROOT_DIR / ".archived" / "workflows_reorganized"
WORKFLOWS_MD = ROOT_DIR / "WORKFLOWS.md"

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def get_workflows_mapping():
    if not WORKFLOWS_MD.exists():
        return {}
    
    full_content = WORKFLOWS_MD.read_text(encoding="utf-8")
    
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
        # Slashes can be / or \\ in markdown links depending on who wrote them
        links = re.findall(r'\[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(.*?)\)', body)
        
        if links:
            ids = []
            for name, relative_path in links:
                # relative_path might be "category/id/WORKFLOW.md" or "filename.md"
                path_parts = relative_path.strip("/\\").replace("\\", "/").split("/")
                if path_parts[-1] == "WORKFLOW.md":
                    # The ID is the folder name just above WORKFLOW.md
                    if len(path_parts) >= 2:
                        ids.append(path_parts[-2] + ".md")
                else:
                    # It's a flat filename
                    ids.append(path_parts[-1])
            mapping[cat_name] = ids
            
    return mapping

def generate_category_registry(cat_slug, cat_name, file_list, staging_path, original_content):
    registry = {
        "category_id": cat_slug,
        "category_name": cat_name,
        "workflows": []
    }
    
    for filename in sorted(file_list):
        workflow_id = filename.replace(".md", "")
        # Robust search for description and slash command
        esc_id = re.escape(workflow_id)
        # Handle both forward and backward slashes in content search
        row_pattern = rf'\| \[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(?:.*?){esc_id}(?:[/\\]WORKFLOW\.md|\.md)\) \| ([^|]+) \| ([^|]*?) \| ([^|]*?)? \|'
        match = re.search(row_pattern, original_content)
        
        description = ""
        triggers = []
        if match:
            slash = match.group(2).strip()
            desc = match.group(4).strip() if match.group(4) else match.group(3).strip()
            triggers = [slash.replace("/", "").replace("`", "")]
            description = desc
        
        registry["workflows"].append({
            "id": workflow_id,
            "description": description,
            "path": f"{workflow_id}/WORKFLOW.md",  # Local path
            "triggers": triggers,
            "required_skills": [],
            "entry_point": None
        })
    
    registry_file = Path(staging_path) / "registry.json"
    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

def reorganize():
    mapping = get_workflows_mapping()
    
    # 1. Prepare clean staging area
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True)
    
    # 2. Index all actual physical files
    all_files = {} 
    for r, d, files in os.walk(WORKFLOWS_DIR):
        root = Path(r)
        for f in files:
            if f.endswith(".md") and " copy" not in f:
                if f == "WORKFLOW.md":
                    wf_id = root.name
                    all_files[wf_id + ".md"] = root / f
                else:
                    all_files[f] = root / f
    
    original_content = WORKFLOWS_MD.read_text(encoding="utf-8")
    moved_filenames = set()
    
    # 3. Process categories and generate sharded registries
    for cat_name, file_list in mapping.items():
        cat_slug = slugify(cat_name)
        cat_staging_path = STAGING_DIR / cat_slug
        cat_staging_path.mkdir(parents=True, exist_ok=True)
        
        valid_files_in_cat = []
        for filename in file_list:
            if filename in all_files:
                workflow_id = filename.replace(".md", "")
                wf_folder = cat_staging_path / workflow_id
                wf_folder.mkdir(parents=True, exist_ok=True)
                shutil.copy2(all_files[filename], wf_folder / "WORKFLOW.md")
                moved_filenames.add(filename)
                valid_files_in_cat.append(filename)
        
        # Generate Registry for this category
        if valid_files_in_cat:
            generate_category_registry(cat_slug, cat_name, valid_files_in_cat, cat_staging_path, original_content)
                
    # 4. Handle miscellaneous
    misc_path = STAGING_DIR / "miscellaneous"
    misc_files = []
    for filename, full_path in all_files.items():
        if filename not in moved_filenames:
            if not misc_path.exists(): misc_path.mkdir(parents=True)
            workflow_id = filename.replace(".md", "")
            wf_folder = misc_path / workflow_id
            wf_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(full_path, wf_folder / "WORKFLOW.md")
            misc_files.append(filename)
    
    if misc_files:
        generate_category_registry("miscellaneous", "📦 Miscellaneous", misc_files, misc_path, original_content)

    # 5. Reconstruct WORKFLOWS.md content
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
            # Match current paths correctly
            row_pattern = rf'\| \[([^\]]+)\]\(\.(?:archived/workflows/|archived_workflows/)(?:.*?){esc_id}(?:[/\\]WORKFLOW\.md|\.md)\) \| ([^|]+) \| ([^|]*?) \| ([^|]*?)? \|'
            match = re.search(row_pattern, original_content)
            
            if match:
                display_name = match.group(1).strip()
                slash = match.group(2).strip()
                desc = match.group(4).strip() if match.group(4) else match.group(3).strip()
                status = "✅ Ready" if not filename.startswith("custom-") else "🚧 Custom"
                # Standardize links to use forward slashes for Markdown/Web compatibility
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

    WORKFLOWS_MD.write_text(header_part.strip() + "\n" + "".join(new_sections) + footer, encoding="utf-8")
        
    total_wf_files = 0
    for r, d, files in os.walk(STAGING_DIR):
        if "WORKFLOW.md" in files: total_wf_files += 1

    if total_wf_files == 0:
        print("Error: Staging directory contains no workflows. Aborting swap.")
        return

    final_backup = WORKFLOWS_DIR.parent / (WORKFLOWS_DIR.name + "_old_before_reorg")
    if final_backup.exists(): shutil.rmtree(final_backup)
    
    # Perform atomic-ish swap
    os.rename(WORKFLOWS_DIR, final_backup)
    os.rename(STAGING_DIR, WORKFLOWS_DIR)
    print(f"Reorganization success! {total_wf_files} workflows safely synchronized.")

if __name__ == "__main__":
    reorganize()
