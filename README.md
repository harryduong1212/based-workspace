# based-workspace

**based-workspace** is a development environment designed to provide a structured context for AI-assisted engineering. It provides an orchestration layer of 330+ skills, 16 workflows, and local infrastructure (pgvector + n8n) to help you manage specialized AI assets across different projects.

## 🚀 Addressing AI Context Challenges

Most AI coding assistants face challenges with context management—either having insufficient information about your specific domain or too much irrelevant data. This workspace addresses these issues through two primary mechanisms:

-   **Modular Context Management**: The **Inheritance Engine** (`workspace_manager.py`) symlinks specific subsets of specialized assets based on role-based profiles (e.g., `backend-core`, `devops-core`).
-   **Structured Workflows**: A suite of specialized CLIs and workflows helps automate repetitive tasks like registry maintenance, tagging, and dependency resolution.
-   **Local Infrastructure**: Built-in containers for PostgreSQL (vector storage) and n8n (automation) provide a standard local backbone for integrated workflows.

---

## Documentation Hub

- **[SKILLS.md](docs/SKILLS.md)**: Browse 212+ curated **Base Skills** and 120+ archived modules.
- **[WORKFLOWS.md](docs/WORKFLOWS.md)**: Explore 16 specialized automations, now grouped by functional context.
- **[RULES.md](docs/RULES.md)**: Behavioral guardrails applied to every AI interaction.
- **[MCP_GUIDE.md](docs/MCP_GUIDE.md)**: Securely configure and manage Model Context Protocol (MCP) servers.
- **[N8N-ATOM SETUP](docs/n8n-atom/SETUP.md)**: Comprehensive guide for running n8n via quickstart or compiling from source.

## ⚙️ Core Workspace Automations

The workspace includes scripts and workflows to streamline repetitive engineering tasks:
- **`git-commit-group-changes`**: Groups uncommitted changes into logical units and generates conventional commit messages.
- **`feature-kickoff`**: Generates a standard set of initial documentation (specs, API contracts, schemas) for new features.
- **`workspace_manager.py`**: A CLI to manage your active context by symlinking required skills and workflows based on predefined role profiles.

---

## Quick Start

### 1. Prerequisites

Install the following **before** starting the workspace. 
*(If you are on Windows, avoid using the legacy Command Prompt; we recommend using **PowerShell 7** or a modern terminal for the best experience).*

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

> **Note:** The rules in this workspace default to `podman`. If you use Docker, update `.agents/rules/terminal-environment.md` (see [ADVANCED_USAGE.md](docs/ADVANCED_USAGE.md)).

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
# Developer Mode (Build from source)
python scripts/build_n8n_atom.py --all
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d --build

# User Mode (Quickstart)
podman compose -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml up -d
```

**Docker:**
```bash
# Developer Mode (Build from source)
python scripts/build_n8n_atom.py --all
docker compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d --build

# User Mode (Quickstart)
docker compose -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml up -d
```

This starts:
- `based-workspace-postgres` — PostgreSQL 16 + pgvector on port **5432** (AI Memory + n8n)
- `n8n-atom` — n8n workflow automation on port **5678** (Quickstart)
- `n8n-atom-dev` — n8n workflow automation on port **5678** (Developer Mode)

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

Use the **Profile Manager CLI** to dynamically load the context you need.

**List all profiles and their optimized weights:**
```bash
python scripts/profile_manager.py stats
```

**Load a task-focused backend context (~140 skills):**
```bash
python scripts/workspace_manager.py --profile backend-ops
```

**Load an "Ultimate" system architect context (~230 skills):**
```bash
python scripts/workspace_manager.py --profile architect-ultimate
```

**Switch to DevOps context to deploy:**
```bash
python scripts/workspace_manager.py --profile devops-core --clear
```

**Audit your profiles for broken links:**
```bash
python scripts/profile_manager.py audit
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
├── .archived/                    ← 🗃️ Library of 330+ available assets
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
│   ├── build_n8n_atom.py         ← 🐳 Docker building for n8n locally
│   ├── workspace_manager.py      ← 🕹️ Active context controller (Symlink engine)
│   ├── profile_manager.py        ← 📋 Role Context Manager (stats, audit, fix)
│   ├── asset_manager.py          ← 🛠️ Registry & Tag Manager (tags, reorganize)
│   ├── lib/                      ← 📦 Shared workspace utility library
│   ├── resources/                ← 🗃️ Shared static resources for scripts
│   ├── profiles.json             ← 📋 Modular role-based profile definitions
│   ├── grep-mcp.js               ← 🔍 Local file semantic search MCP loader
│   └── postgres-mcp.js           ← 🔑 Secure MCP credential loader
│
├── .env                          ← 🤐 Active secrets (ignored by Git)
├── docs/                         ← 📚 Centralized documentation hub
│   ├── n8n-atom/                 ←   n8n setup, architecture and CI/CD
│   ├── RULES.md                  ←   Catalogue of active rules
│   ├── SKILLS.md                 ←   Catalogue of all 330+ skills
│   ├── WORKFLOWS.md              ←   Catalogue of all 16 workflows
│   ├── MCP_GUIDE.md              ←   Comprehensive guide for MCP servers
│   ├── LOCAL_AI_SETUP.md         ←   Setup guide for local AI models
│   └── ADVANCED_USAGE.md         ←   Advanced ecosystem customization
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
