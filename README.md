# based-workspace

**based-workspace** is a development environment designed to provide a structured context for AI-assisted engineering. It provides an orchestration layer of 159 active skills (plus 180 vaulted for reference), 16 workflows, and local infrastructure (pgvector + n8n) to help you manage specialized AI assets across different projects.

> A user-facing product layer — Recipes, Connectors, Routines — is being layered on top of this engine. See [docs/PRODUCT_PLAN.md](docs/PRODUCT_PLAN.md) for the design and current status.

## 🚀 Addressing AI Context Challenges

Most AI coding assistants face challenges with context management—either having insufficient information about your specific domain or too much irrelevant data. This workspace addresses these issues through two primary mechanisms:

-   **Recipe-driven tasks**: Users invoke AI tasks through **Recipes** (`recipes/<id>.md`) — self-contained units that work in both Antigravity and Claude Code via auto-generated provider bindings.
-   **Reference library**: `.archived/skills/` and `.archived/workflows/` are consulted when *composing* recipes — they're knowledge sources, not loaded as runtime context.
-   **Local Infrastructure**: Built-in containers for PostgreSQL (vector storage) and n8n (automation) provide a standard local backbone for integrated workflows.

---

## Documentation Hub

- **[SKILLS.md](docs/SKILLS.md)**: Browse the **Base Skills** catalog (159 active skills across 37 categories; 180 additional skills are vaulted at `.archived/_vault/skills/`).
- **[WORKFLOWS.md](docs/WORKFLOWS.md)**: Explore 16 specialized automations, now grouped by functional context.
- **[RULES.md](docs/RULES.md)**: Behavioral guardrails applied to every AI interaction.
- **[MCP_GUIDE.md](docs/MCP_GUIDE.md)**: Securely configure and manage Model Context Protocol (MCP) servers.
- **[N8N-ATOM SETUP](docs/n8n-atom/SETUP.md)**: Comprehensive guide for running n8n via quickstart or compiling from source.

## ⚙️ Core Workspace Automations

The workspace includes scripts and workflows to streamline repetitive engineering tasks:
- **`git-commit-group-changes`**: Groups uncommitted changes into logical units and generates conventional commit messages.
- **`feature-kickoff`**: Generates a standard set of initial documentation (specs, API contracts, schemas) for new features.
- **`recipe_manager.py`**: List, lint, sync, and run Recipes. Recipes are the user-facing unit of work.
- **`sync_antigravity.py` / `sync_claude_code.py`**: Generate provider-specific bindings (`.agents/workflows/`, `.claude/commands/`) from `recipes/`.
- **`validate.py`**: Run all integrity checks (recipe lint, registry sync, generated docs sync, provider sync, connector integrity).

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

`.env` at the repo root is the single source of truth for secrets and is gitignored. Bootstrap is three steps:

```bash
cp .env.example .env                  # template with all keys + paste-from URLs
./scripts/gen_secrets.sh              # prints fresh randoms — paste into .env
./scripts/install-git-hooks.sh        # installs gitleaks + pre-commit hook
```

`gen_secrets.sh` prints to stdout only — it never writes `.env` automatically, so it can't clobber existing values.

- **Auto-generatable** (printed by the script): `POSTGRES_PASSWORD`, `N8N_ENCRYPTION_KEY` (this last one is critical — losing it breaks every credential stored in n8n).
- **Paste from source** (URLs in `.env.example`): `N8N_API_KEY` (from the n8n UI after owner setup), `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `JIRA_*`, `BITBUCKET_*`, `GMAIL_APP_PASSWORD`.

MCP servers read `.env` via `./scripts/with-env.sh`. The local `.mcp.json` is gitignored; `.mcp.json.example` is the committed template.

### 4. Start Infrastructure

The canonical setup uses [`infrastructure/core/docker-compose.yaml`](infrastructure/core/docker-compose.yaml) with `.env` providing every credential and `POSTGRES_PORT` (publish port — defaults to 5432; set to a free value if port 5432 is occupied by another Postgres). The n8n image is pulled as `docker.io/atom8n/n8n:fork` — no local build step is needed.

**Podman:**
```bash
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
```

**Docker:**
```bash
docker compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
```

This starts:
- `based-workspace-postgres` — PostgreSQL 16 + pgvector on the host port set by `${POSTGRES_PORT}` (default 5432; container-internal stays 5432).
- `n8n-atom-dev` — n8n workflow automation on port **5678** (image `atom8n/n8n:fork`, Postgres-backed).

The optional MCP Inspector runs **host-native** (not via compose) per the [upstream readme](https://github.com/khanh-atom/mcp-inspector-atom8n):

```bash
./scripts/mcp-inspector.sh start   # http://localhost:6274
./scripts/mcp-inspector.sh stop
```

Running on host (rather than in a container) lets the inspector read your IDE's MCP profiles at `~/.cursor/mcp.json`, `~/.gemini/antigravity/mcp_config.json`, etc.

#### Control Panel (UI for installs, logs, runs)

A FastAPI + Next.js app at `services/control_panel/` exposes the workspace as a browsable "package manager" — install/start/uninstall containers, MCP servers, recipes, and connectors from a UI; tail container logs live; trigger recipe runs. It calls the same install primitives as the CLI, so the UI and `podman compose` paths are kept in sync.

```bash
./scripts/dev.sh                       # backend on :8765, frontend on :3000
# then open http://localhost:3000
```

`scripts/dev.sh --no-backend` / `--no-frontend` runs just one side. The backend has no hot-reload; restart it after editing `services/control_panel/*.py`.

> [!TIP]
> If your `.env` rotates `POSTGRES_PASSWORD` **after** Postgres has been initialized once, the password in the volume is already baked in — n8n will fail to connect with the new one. Either delete the volume (`down -v`) or `ALTER USER` inside the running container.

### 5. Open in your AI coding tool

Open the `based-workspace` folder in **Antigravity**, **VS Code**, **Cursor**, or any editor that supports the `.agents/` convention.

The AI assistant will automatically pick up:
- Rules from `.agents/rules/`
- Agent persona from `.agents/agents.md` 
- Skills from `.agents/skills/`
- Workflows from `.agents/workflows/`
- MCP servers from `.vscode/mcp.json` (IDE-side) and `.mcp.json` (Claude Code), both using wrapper scripts that source `.env` so secrets never appear inline

> [!TIP]
> If you don't use `grep_app`, you can disable it by adding an underscore to its name in `.vscode/mcp.json` (e.g., `"_grep_app"`). This prevents startup errors while keeping the configuration for future use.

### 6. Browse and Run Recipes

**List available recipes:**
```bash
python scripts/recipe_manager.py list
```

**Run a recipe (currently stubbed; real dispatchers pending):**
```bash
python scripts/recipe_manager.py run daily-briefing --dry-run
```

**Generate provider-specific bindings from `recipes/`:**
```bash
python scripts/sync_antigravity.py     # writes .agents/workflows/<id>.md
python scripts/sync_claude_code.py     # writes .claude/commands/<id>.md
python scripts/docs_generator.py       # writes docs/recipes/, docs/connectors/
```

**Run all integrity checks (recipe lint, registries, generated docs):**
```bash
python scripts/validate.py
```

**Manage the skill reference library (`.archived/skills/`):**
```bash
python scripts/archive_manager.py prune-report           # report unused skills
python scripts/archive_manager.py vault <skill-id>        # move out of registry
python scripts/archive_manager.py unvault <skill-id>      # restore
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
├── .archived/                    ← 🗃️ Library of available assets (159 active skills + 180 vaulted)
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
├── services/
│   └── control_panel/               ← 🖥️ FastAPI + Next.js UI for install/start/verify, container logs, recipe runs (see `./scripts/dev.sh`)
│
├── scripts/
│   ├── dev.sh                    ← 🖥️ Run Control Panel backend (:8765) + frontend (:3000)
│   ├── gen_secrets.sh            ← 🔐 Print fresh randoms for .env (POSTGRES_PASSWORD, N8N_ENCRYPTION_KEY)
│   ├── with-env.sh               ← 🔐 Source .env then exec — used by .mcp.json wrappers
│   ├── install-git-hooks.sh      ← 🔐 Install gitleaks + pre-commit hook
│   ├── mcp-inspector.sh          ← 🔍 Host-native MCP Inspector lifecycle (start/stop/status)
│   ├── recipe_manager.py         ← 🧾 Recipe lifecycle (list/show/lint/sync/run)
│   ├── docs_generator.py         ← 📚 Generate docs/recipes/, docs/connectors/
│   ├── sync_antigravity.py       ← 🔌 Render recipes → .agents/workflows/
│   ├── sync_claude_code.py       ← 🔌 Render recipes → .claude/commands/
│   ├── validate.py               ← ✅ Umbrella integrity check
│   ├── archive_manager.py        ← 🗃️ Skill library lifecycle (prune/vault)
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
│   ├── SKILLS.md                 ←   Catalogue of active skills
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
