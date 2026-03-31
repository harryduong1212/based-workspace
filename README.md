# based-workspace

**A portable AI-powered development workspace** — providing an archive of 1,300+ skills, 50 workflows, MCP servers, and local infrastructure (PostgreSQL + n8n) so every project you open gets the customized AI super-powers you need.

Works on **Windows 11 · macOS · Linux**.

### 🆕 What's New? (March 2026)

- **Registry Sharding**: Both the massive 1,300+ skill index and the 50+ workflow registry are now sharded by category for lightning-fast loading and zero merge conflicts.
- **Deep Tag Extraction**: Assets (Skills & Workflows) are now automatically tagged with technologies (`fastapi`, `tailwind`) and protocols (`grpc`, `oauth`) extracted directly from their instruction files.
- **Root-Level Indexing**: `SKILLS.md`, `WORKFLOWS.md`, and `RULES.md` are now conveniently located in the repository root for easier browsing.
- **Safe Reorganization**: Maintenance scripts (`reorganize_*.py`) now automatically maintain folder hierarchies and prune orphaned registry entries, keeping your library 100% clean.
- **MCP Security**: New `MCP_GUIDE.md` and secure wrapper scripts ensure your database passwords never touch a JSON config.

---

## Documentation Hub

To keep this guide concise, deep dives into specific areas of the workspace have been moved to dedicated documentation files:

- **[SKILLS.md](SKILLS.md)**: Browse and activate specialized AI knowledge modules (1,300+ skills).
- **[WORKFLOWS.md](WORKFLOWS.md)**: Explore slash-command automations to accelerate your development loop.
- **[RULES.md](RULES.md)**: Understand the behavioral guardrails applied to every AI interaction.
- **[MCP_GUIDE.md](MCP_GUIDE.md)**: A comprehensive guide for configuring and managing Model Context Protocol (MCP) servers.
- **[ADVANCED_USAGE.md](ADVANCED_USAGE.md)**: Details on customizing the workspace, reorganizing assets, registry sharding, and deep tag extraction.

---

## Quick Start

### 1. Prerequisites

Install the following **before** starting the workspace. 
*(If you are on Windows, ensure you are running your terminal commands in **PowerShell 7** or higher, not Command Prompt).*

| Tool | Min Version | Install |
|---|---|---|
| **Node.js** | 18+ | <https://nodejs.org> |
| **Container engine** | — | Podman or Docker (see below) |
| **Git** | 2.30+ | <https://git-scm.com> |
| **AI coding tool** | — | Antigravity, VS Code + Copilot, Cursor, etc. |

#### Container Engine

This workspace uses containers for PostgreSQL (pgvector) and n8n. Choose one:

| Engine | Recommended for | Install |
|---|---|---|
| **Podman** | Windows 11, Linux | <https://podman.io/getting-started/installation> |
| **Docker** | macOS, Linux | <https://docs.docker.com/get-docker/> |

**Quick Installation Tips:**
- **macOS:** Install via Homebrew: `brew install podman` (then run `podman machine init` and `podman machine start`), or for Docker: `brew install --cask docker`.
- **Linux:** Install via your package manager, e.g., Ubuntu/Debian: `sudo apt-get install podman` (or `docker.io`), Fedora: `sudo dnf install podman`.
- **Windows 11:** Completely fresh Windows installations do not have WSL2 enabled by default. Open an **admin** PowerShell and run `wsl --install` before installing Podman or Docker Desktop, or your background container engine will fail to start.

> **Note:** The rules in this workspace default to `podman`. If you use Docker, update `.agents/rules/terminal-environment.md` (see [ADVANCED_USAGE.md](ADVANCED_USAGE.md)).

#### 🔍 Verify Your Setup
Restart your terminal after installing the tools above, then run:

```bash
node -v
git --version
podman -v # or docker -v
```

If these print versions (and not "command not found"), you are ready to proceed!

### 2. Initial Git Setup & Clone

If this is a completely fresh laptop, configure your Git identity first so you can commit and push:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Clone the repository to your machine:
```bash
git clone https://github.com/harryduong1212/based-workspace.git
cd based-workspace
```

### 3. Configure Environment & Secrets

This workspace uses a secure, automated setup to manage your local database passwords and environment variables without leaking them to Git.

```bash
# Generate your personal .env file and configure MCP servers
python scripts/setup_env.py
```

This script:
- Generates a secure, random password for your local PostgreSQL.
- Creates a `.env` file at the root (ignored by Git).
- Synchronizes `.vscode/mcp.json` to use a secure loader script.

### 4. Start Infrastructure

Choose the command for your container engine:

**Podman:**
```bash
podman compose -f infrastructure/core/docker-compose.yaml up -d
```

**Docker:**
```bash
docker compose -f infrastructure/core/docker-compose.yaml up -d
```

This starts:
- `based-workspace-postgres` — PostgreSQL 16 + pgvector on port **5432**
- `based-workspace-n8n` — n8n workflow automation on port **5678**

> [!TIP]
> Always run `setup_env.py` **before** starting your containers for the first time or whenever you want to rotate your passwords.

### 5. Open in your AI coding tool

Open the `based-workspace` folder in **Antigravity**, **VS Code**, **Cursor**, or any editor that supports the `.agents/` convention.

The AI assistant will automatically pick up:
- Rules from `.agents/rules/`
- Agent persona from `.agents/agents.md` 
- Skills from `.agents/skills/`
- Workflows from `.agents/workflows/`
- MCP servers from `.vscode/mcp.json` (running securely via `scripts/postgres-mcp.js`)

> [!TIP]
> If you don't use `grep_app`, you can disable it by adding an underscore to its name in `.vscode/mcp.json` (e.g., `"_grep_app"`). This prevents startup errors while keeping the configuration for future use.

### 6. Manage Your Workspace Context

Use the `workspace_manager.py` script to dynamically load the specific skills and workflows you need for your current task. 

**Load a developer profile:**
```bash
python scripts/workspace_manager.py --profile java-backend-dev
```

**Load multiple profiles at once:**
```bash
python scripts/workspace_manager.py --profile "n8n-orchestrator,technical-project-manager"
```

**Add specific skills or workflows on the fly:**
```bash
python scripts/workspace_manager.py --skills "postgresql-optimization" --workflows "custom-feature-kickoff"
```

**Clear your active context (removes everything except preserved skills):**
```bash
python scripts/workspace_manager.py --clear
```

---

## Using with Your Projects

### Option A: Single Project Inside the Workspace

Place your project directly inside the workspace root:

```
based-workspace/
├── .agents/            ← AI config (shared)
├── .vscode/            ← MCP config (shared)
├── infrastructure/     ← containers (shared)
├── my-app/             ← YOUR PROJECT
│   ├── src/
│   ├── package.json
│   └── ...
└── README.md
```

**How:** Just create or clone your project folder here:

```bash
# Create new
mkdir my-app && cd my-app && npm init -y

# Or clone existing
git clone https://github.com/you/my-app.git
```

### Option B: Multiple Projects Inside the Workspace

Same as above — add more folders:

```
based-workspace/
├── .agents/
├── .vscode/
├── infrastructure/
├── project-alpha/      ← Project 1
├── project-beta/       ← Project 2
├── project-gamma/      ← Project 3
└── README.md
```

All projects share the same AI skills, MCP servers, and infrastructure.

### Option C: Symlink Into an Existing Project (advanced)

If your project lives elsewhere, create symlinks so it picks up the workspace config:

**Windows (PowerShell — Run as Admin):**
```powershell
# From your project directory
New-Item -ItemType SymbolicLink -Path ".agents" -Target "H:\path\to\based-workspace\.agents"
New-Item -ItemType SymbolicLink -Path ".vscode" -Target "H:\path\to\based-workspace\.vscode"
```

**macOS / Linux:**
```bash
# From your project directory
ln -s /path/to/based-workspace/.agents .agents
ln -s /path/to/based-workspace/.vscode .vscode
```

> **Tip:** Add `.agents` and `.vscode` to your project's `.gitignore` if you don't want to commit the symlinks.

### Option D: Copy `.agents/` Into Any Project (portable)

For a fully self-contained project, just copy the folder:

**Windows (PowerShell):**
```powershell
Copy-Item -Recurse "H:\path\to\based-workspace\.agents" -Destination ".\your-project\.agents"
```

**macOS / Linux:**
```bash
cp -r /path/to/based-workspace/.agents ./your-project/.agents
```

---

## Workspace Layout

```
based-workspace/
│
├── .agents/                      ← 🤖 AI assistant configuration
│   ├── agents.md                 ←   Agent persona & rules
│   ├── rules/                    ←   Behavioural rules (always active)
│   │   ├── terminal-environment.md
│   │   └── workspace-boundaries.md
│   ├── skills/                   ←   Active domain skills tailored for your project
│   │   └── <skill-name>/SKILL.md
│   └── workflows/                ←   Active slash-command workflows
│       └── <workflow>/WORKFLOW.md
│
├── .archived/                    ← 🗃️ Library of 1,300+ available assets
│   ├── skills/                   ←   Hierarchical expertise modules
│   │   ├── <category>/
│   │   │   └── <skill-name>/SKILL.md
│   │   └── registry.json         ←   Machine-readable skill index (per-category)
│   └── workflows/                ←   Hierarchical workflow automations
│       ├── <category>/
│       │   └── <wf-name>/WORKFLOW.md
│       └── registry.json         ←   Machine-readable workflow index (per-category)
│
├── .vscode/
│   └── mcp.json                  ← 🔌 MCP server template
│
├── infrastructure/
│   ├── core/
│   │   └── docker-compose.yaml   ← 🐳 PostgreSQL + n8n containers
│   └── ai/
│       └── docker-compose.yaml   ← 🤖 Local AI inference + automatic model pull
│
├── scripts/
│   ├── setup_env.py              ← 🛠️ Env initialization script
│   ├── workspace_manager.py      ← 🕹️ Active context controller (Profiles & Assets)
│   ├── profiles.json             ← 📋 Predefined role-based profile definitions
│   ├── reorganize_skills_safe.py ← 🔄 Skill reorganization & registry sync
│   ├── reorganize_workflows_safe.py ← 🔄 Workflow reorganization & registry sync
│   ├── generate_deep_tags.py     ← 🧠 Deep Tag Extraction for Registered Assets
│   └── postgres-mcp.js           ← 🔑 Secure MCP credential loader
│
├── .env                          ← 🤐 Active secrets (ignored by Git)
├── RULES.md                      ← 📐 Catalogue of active rules
├── SKILLS.md                     ← 🧠 Catalogue of all 1,300+ skills
├── WORKFLOWS.md                  ← 🚀 Catalogue of all 50+ workflows
├── MCP_GUIDE.md                  ← 🔌 Comprehensive guide for MCP servers
├── ADVANCED_USAGE.md             ← ⚙️ Advanced customization guide
└── README.md                     ← 📖 This file
```

---

## Troubleshooting & License

### Troubleshooting

#### MCP & Connectivity
- **"Invalid trailing data":** Always use the wrapper scripts in `scripts/`.
- **"Connection Refused":** Ensure containers are running (`podman ps`).
- **Path Issues:** Ensure absolute paths with forward slashes in `mcp_config.json`.

#### Asset Loading
- Ensure the workspace root is opened (not a subfolder).
- Ensure `.agents/` and `.agents/agents.md` are present.

### License

MIT — Use freely, modify as needed.
