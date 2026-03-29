import os
import re
import shutil

# Safe, Idempotent Workshop/Workflow Reorganization script.
# Fixed to handle already-categorized subfolders.

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
    sections = re.split(r'\n### (.*)\n', full_content)
    
    for i in range(1, len(sections), 2):
        cat_name = sections[i].strip()
        body = sections[i+1]
        # Match filenames in various link formats
        links = re.findall(r'\[([^\]]+)\]\(\.archived/(?:archived_)?workflows/(?:[^/]+/)?([^\)]+\.md)\)', body)
        if links:
            mapping[cat_name] = [l[1] for l in links]
    return mapping

def reorganize():
    mapping = get_workflows_mapping()
    
    # 1. Prepare clean staging area
    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
    os.makedirs(STAGING_DIR)
    
    # 2. Index all actual physical files (including those already in subfolders)
    all_files = {} # filename -> current_full_path
    for root, dirs, files in os.walk(WORKFLOWS_DIR):
        for f in files:
            if f.endswith(".md") and " copy" not in f:
                # If there are duplicates, the first one found wins or we just overwrite
                all_files[f] = os.path.join(root, f)
    
    moved_filenames = set()
    
    # 3. Copy files to category folders in staging
    for cat_name, file_list in mapping.items():
        cat_slug = slugify(cat_name)
        cat_staging_path = os.path.join(STAGING_DIR, cat_slug)
        os.makedirs(cat_staging_path, exist_ok=True)
        
        for filename in file_list:
            if filename in all_files:
                shutil.copy2(all_files[filename], os.path.join(cat_staging_path, filename))
                moved_filenames.add(filename)
            else:
                print(f"Warning: {filename} not found on disk.")
                
    # 4. Handle miscellaneous
    misc_path = os.path.join(STAGING_DIR, "miscellaneous")
    for filename, full_path in all_files.items():
        if filename not in moved_filenames:
            if not os.path.exists(misc_path): os.makedirs(misc_path)
            shutil.copy2(full_path, os.path.join(misc_path, filename))

    # 5. Reconstruct WORKFLOWS.md content
    with open(WORKFLOWS_MD, "r", encoding="utf-8") as f:
        original_content = f.read()
        
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
    # Sort categories to ensure a stable output
    for cat_name in sorted(mapping.keys()):
        file_list = mapping[cat_name]
        cat_slug = slugify(cat_name)
        
        section = f"\n### {cat_name}\n"
        section += f"<details>\n\n"
        section += "| Workflow | Command | Status | Description |\n"
        section += "|---|---|---|---|\n"
        
        # Sort files within category
        for filename in sorted(file_list):
            row_pattern = rf'\| \[([^\]]+)\]\(\.archived/(?:archived_)?workflows/(?:[^/]+/)?{re.escape(filename)}\) \| ([^|]+) \| ([^|]+) \|'
            match = re.search(row_pattern, original_content)
            if match:
                display_name = match.group(1)
                slash = match.group(2).strip()
                desc = match.group(3).strip()
                # Status heuristic: core workflows are "Ready", others "Beta"
                status = "✅ Ready" if not filename.startswith("custom-") else "🚧 Custom"
                section += f"| [{display_name}](.archived/workflows/{cat_slug}/{filename}) | `{slash}` | {status} | {desc} |\n"
        
        section += "\n</details>\n"
        new_sections.append(section)
        
    footer = """
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
        f.write(header_part + "".join(new_sections) + footer)
        
    # 6. Safety Verification
    files_in_staging = sum([len(files) for r, d, files in os.walk(STAGING_DIR)])
    if files_in_staging == 0:
        print("Error: Staging directory is empty. Aborting swap.")
        return

    # 7. Final Swap (Safe)
    final_backup = WORKFLOWS_DIR + "_old_before_reorg"
    if os.path.exists(final_backup): shutil.rmtree(final_backup)
    
    os.rename(WORKFLOWS_DIR, final_backup)
    os.rename(STAGING_DIR, WORKFLOWS_DIR)
    
    print(f"Reorganization success! {files_in_staging} files synchronized into .archived/workflows")

if __name__ == "__main__":
    reorganize()
