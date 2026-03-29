---
description: Automates adding and categorizing a new skill into the workspace
---

# Workflow: Add New Skill

Whenever you acquire or create a new skill that needs to be permanently added to the repository's knowledge base, use this workflow to automatically categorize, move, and formally document it in the skill map (`SKILLS.md`).

1. **Place the Skill Folder**: Drop your newly acquired skill folder directly into the root of `.archived/skills/` (e.g., `.archived/skills/my-new-skill/`). Make sure it has a `SKILL.md` file with a proper YAML frontmatter description inside it.

// turbo
2. **Run the Categorization Script**: Execute the automated categorization and migration script. This script will scan the folder, read the description, match it to the correct category using keyword heuristics, move it to the appropriate subfolder, and update the `SKILLS.md` registry.
```powershell
python scripts/reorganize_skills.py
```

3. **Verify**: Check `SKILLS.md` to ensure the skill was added to the correct category table and that the relative link works. If the heuristic categorization placed it in `📦 Miscellaneous / Other` or the wrong category, you can manually move the Markdown table row in `SKILLS.md` to the correct category, and re-run the script in the future to enforce physical folder synchronization (if the script gets updated to sync from MD to folders).

4. **Activate**: If you're ready to use the skill immediately for an active project, copy the specific skill folder from `.archived/skills/<category>/<skill-name>` into the active `.agents/skills/` directory.
