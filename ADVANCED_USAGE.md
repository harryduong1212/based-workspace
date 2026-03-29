# Advanced Usage

## Customization

### Reorganizing Assets
If you add new skills or workflows manually to the `.archived` directories, run the reorganization scripts to keep the structure and registries in sync:

```bash
# Maintain hierarchical structure and registry sharding
python scripts/reorganize_skills_safe.py
python scripts/reorganize_workflows_safe.py

# Extract deep operational tags based on actual content
python scripts/generate_deep_tags.py --type skills
python scripts/generate_deep_tags.py --type workflows
```

## 🏗️ Advanced Asset Management

### Registry Sharding
To maintain performance and scalability as the library grows (now 1,300+ skills), we use **Registry Sharding**. Instead of one massive `registry.json`, each category in `.archived/skills/` and `.archived/workflows/` contains its own dedicated `registry.json` file. This prevents merge conflicts and allows the AI agent to load only the relevant category context.

### Deep Tag Extraction
The `scripts/generate_deep_tags.py` script uses lightweight natural language processing to read your **SKILL.md** or **WORKFLOW.md** instruction files and extract high-signal tags:
- **Technologies** (e.g., `fastapi`, `tailwind`, `openai`)
- **Protocols** (e.g., `grpc`, `rest`, `oauth`)
- **Operations** (e.g., `scraping`, `fuzzing`, `deployment`)

These tags are automatically indexed in the `registry.json` files, helping the AI agent find the exact expertise needed for your task.

### Orphan Cleanup
The reorganization scripts automatically detect and remove "orphan" entries—skills listed in a registry that no longer have a corresponding `SKILL.md` file on disk. This ensures your library index is always 100% accurate.
