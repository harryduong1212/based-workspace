import re
import json
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
WORKFLOWS_MD = WORKSPACE_ROOT / "docs/WORKFLOWS.md"
ORPHANS_FILE = WORKSPACE_ROOT / "tmp/workflow_orphans_data.json"

def cleanup_workflows_md():
    if not WORKFLOWS_MD.exists():
        print("WORKFLOWS.md not found.")
        return

    with open(ORPHANS_FILE, "r", encoding="utf-8") as f:
        orphans_data = json.load(f)
    
    orphaned_ids = {wf["id"] for wf in orphans_data.get("orphaned_workflows", [])}
    missing_categories = set(orphans_data.get("missing_categories", []))
    
    # Map category ID to display name in WORKFLOWS.md (human-readable)
    # The header format is "### 🎨 Creative & UI"
    cat_id_to_header_part = {
        "accessibility": "♿ Accessibility",
        "database": "🗄️ Database",
        "debugging": "🐛 Debugging",
        "deployment": "🚀 Deployment",
        "development": "🔧 Development",
        "documentation": "📚 Documentation",
        "miscellaneous": "📦 Miscellaneous",
        "security": "🔒 Security"
    }
    
    with open(WORKFLOWS_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    skip_category = False
    
    for line in lines:
        # Check for category header removal
        # e.g., "### 🎨 Creative & UI"
        found_header = False
        for cat_id, header_part in cat_id_to_header_part.items():
            if line.startswith(f"### {header_part}"):
                if cat_id in missing_categories:
                    print(f"Skipping category section: {cat_id}")
                    skip_category = True
                    found_header = True
                    break
        
        if found_header:
            continue
            
        # If we are skipping a category, skip until the next category or a horizontal rule separator
        if skip_category:
            if line.startswith("### "):
                skip_category = False
                # Fall through to process the next category
            elif line.strip() == "---" and (len(new_lines) > 0 and new_lines[-1].strip() == "</details>"):
                 skip_category = False
                 # Skip the separator too if we just skipped a category
                 continue
            else:
                continue
                
        # Check for individual workflow row
        # Pattern: | [workflow-id](path) | /command | status | description |
        match = re.search(r"\| \[(.*?)\]\(.*?\)", line)
        if match:
            wf_id = match.group(1)
            if wf_id in orphaned_ids:
                print(f"Removing workflow row: {wf_id}")
                continue
        
        new_lines.append(line)
        
    # Update count in "## 📂 Available Workflows (52)"
    # We need to count the remaining rows
    wf_count = 0
    for line in new_lines:
         if re.search(r"\| \[(.*?)\]\(.*?\)", line) and not line.startswith("| Workflow | Command |"):
             wf_count += 1
             
    final_lines = []
    for line in new_lines:
        if line.startswith("## 📂 Available Workflows ("):
            final_lines.append(f"## 📂 Available Workflows ({wf_count})\n")
        else:
            final_lines.append(line)
            
    with open(WORKFLOWS_MD, "w", encoding="utf-8") as f:
        f.writelines(final_lines)
    print(f"WORKFLOWS.md updated. New workflow count: {wf_count}")

if __name__ == "__main__":
    cleanup_workflows_md()
