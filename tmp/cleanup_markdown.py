import re
from pathlib import Path

WORKSPACE_ROOT = Path("h:/WORKSPACE/Personal/Vibe/based-workspace")
SKILLS_MD = WORKSPACE_ROOT / "docs/SKILLS.md"
ORPHANS_FILE = WORKSPACE_ROOT / "tmp/orphans.json"

def cleanup_skills_md():
    if not SKILLS_MD.exists():
        print("SKILLS.md not found.")
        return

    import json
    with open(ORPHANS_FILE, "r", encoding="utf-8") as f:
        orphans_data = json.load(f)
    
    orphaned_ids = {s["id"] for s in orphans_data.get("orphaned_skills", [])}
    
    with open(SKILLS_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    skip_category = False
    
    for line in lines:
        # Check for category header
        if line.startswith("### Security Testing"):
            skip_category = True
            continue
        
        # If we are skipping a category, skip until the next category or end of details
        if skip_category:
            if line.startswith("### "):
                skip_category = False
                # fall through to process next category
            else:
                continue
                
        # Check for skill table row
        # Pattern: | [skill-id](path) | description |
        match = re.search(r"\| \[(.*?)\]\(.*?\)", line)
        if match:
            skill_id = match.group(1)
            if skill_id in orphaned_ids:
                print(f"Removing skill row: {skill_id}")
                continue
        
        new_lines.append(line)
        
    with open(SKILLS_MD, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("SKILLS.md updated.")

if __name__ == "__main__":
    cleanup_skills_md()
