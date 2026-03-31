# Advanced Usage

This guide covers advanced customization, asset management, and the technical underpinnings of the **based-workspace** asset library.

---

## 🏗️ Advanced Asset Management

The workspace infrastructure is designed to handle thousands of AI assets efficiently using **Registry Sharding**, **Deep Tag Extraction**, and **Safe Reorganization** scripts.

### 1. Registry Sharding
To maintain performance and scalability as the library grows (now 1,300+ skills and 50+ workflows), we use **Registry Sharding**. 

- **How it works:** Instead of one massive, monolithic `registry.json`, each category in `.archived/skills/` and `.archived/workflows/` contains its own dedicated `registry.json`.
- **Benefits:** 
  - **Performance:** The AI agent only loads the specific category context it needs, reducing token overhead.
  - **Collaborative Flow:** Minimizes Git merge conflicts by isolating registry updates to specific folders.
  - **Modularity:** Easy to add or remove entire categories without breaking the global index.

### 2. Deep Tag Extraction
Searchability is powered by the `scripts/asset_manager.py tags` command. This utility performs a "deep read" of every **SKILL.md** and **WORKFLOW.md** to extract high-signal operational tags.

- **Technology Tags:** `fastapi`, `postgresql`, `tailwind`, `langchain`
- **Protocol Tags:** `grpc`, `rest`, `oauth2`, `websocket`
- **Capability Tags:** `scraping`, `fuzzing`, `deployment`, `migration`

These tags are automatically injected into the sharded registries, allowing the AI to find the perfect expertise for your specific tech stack.

### 3. Safe Reorganization Scripts
Whenever you manually add, move, or delete assets in the `.archived/` directories, you must synchronize the registries using the reorganization suite.

```bash
# 1. Maintain folder hierarchies and update sharded registries
# This now AUTOMATICALLY performs deep tag extraction as well!
python scripts/asset_manager.py reorganize_skills
python scripts/asset_manager.py reorganize_workflows

# 2. Extract deep tags manually (only if needed for partial updates)
python scripts/asset_manager.py tags --type skills
python scripts/asset_manager.py tags --type workflows
```

**What these scripts do:**
- **Hierarchical Balancing:** Ensures skills are placed in the correct category folders based on their IDs.
- **Orphan Cleanup:** Automatically detects and removes registry entries that no longer have a corresponding file on disk.
- **Registry Synchronization:** Rebuilds the sharded indices in `.archived/` to match the current filesystem state.

---

## 🕹️ Workspace Context Management (Profiles & Assets)

The `scripts/workspace_manager.py` tool is the main orchestration point for configuring the active AI persona for your specific tasks. 

### 1. Active Asset Loading (Symlinking)
Instead of copying 1,300+ skills into every project, the workspace uses **symlinks** (and Windows junctions) to map assets from the `.archived/` library into your active `.agents/skills/` and `.agents/workflows/` directories. 

- **Benefits:**
  - **Single Source of Truth:** Edits to a skill within your project are reflected back into the central `.archived/` library.
  - **Zero Bloat:** Only the assets you need are "mounted" in your project.
  - **Instant Switching:** Swapping profiles only takes a fraction of a second.

### 2. Role-Based Profiles (`profiles.json`)
The `scripts/profiles.json` file contains bundles of skills and workflows categorized by developer roles. 

- **How it works:** When you run `python scripts/workspace_manager.py --profile java-backend-dev`, the script looks up the `java-backend-dev` definition and automatically symlinks all listed skills and workflows into your workspace.
- **Customization:** You can easily add your own profiles or modify existing ones to include your favorite tools.

### 🧩 Contextual Profiles (Sub-Roles)
To keep your AI context lean and focused, major roles are split into **Contextual Sub-Roles**. These use a naming convention that prioritizes specific functional suites:

| Context | Purpose | Extended Suites |
| :--- | :--- | :--- |
| **`-dev`** | Pure Development | `base-core`, `base-dev`, `base-ai` |
| **`-ops`** | Infrastructure / Deploy | `base-core`, `base-dev`, `base-infra-ops` |
| **`-sec`** | Security / Hardening | `base-core`, `base-dev`, `base-security` |
| **`-biz`** | Product / Growth / CRO | `base-core`, `base-dev`, `base-product-cro` |
| **`-ultimate`** | Full Suite (Kitchen Sink)| All `base-*` suites |

**Why use sub-roles?** 
Loading only relevant skills (e.g., just `backend-ops` instead of a full stack) reduces "hallucination surface area" and keeps the AI focused on the task at hand. Workflows are also filtered based on these contexts.

### 3. Dynamic Registry & Metadata
Every time you run `workspace_manager.py`, it automatically generates (or appends to) a `registry.json` file inside your active `.agents/skills/` and `.agents/workflows/` folders. 

- **LLM Discovery:** These active registries follow the **Agent Skill Registry** schema, providing the AI with descriptions, triggers, and tags it needs to discover and use the skills you've activated. 
- **Default Workflows:** Certain critical workflows (like `git-rebase`, `git-commit`, etc.) are defined as **Default Workflows** in the script and will always be activated whenever you load a profile.

---

## 🛠️ Customization

### Adding New Skills/Workflows
1. Create a new folder in `.archived/skills/custom-skills/` or `.archived/workflows/custom-workflows/`.
2. Add your **SKILL.md** or **WORKFLOW.md** (use existing assets as templates).
3. Run the **Safe Reorganization Scripts** listed above to register and tag your new asset.

### Adjusting Terminal Rules
If you use **Docker** instead of **Podman**, or a different shell, update the following files:
- `.agents/rules/terminal-environment.md`
- `.agents/rules/workspace-boundaries.md`
