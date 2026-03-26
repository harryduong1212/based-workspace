# based-workspace

**A portable AI-powered development workspace** — providing an archive of 1 000+ skills, 45 workflows, MCP servers, and local infrastructure (PostgreSQL + n8n) so every project you open gets the customized AI super-powers you need.

Works on **Windows 11 · macOS · Linux**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Using with Your Projects](#using-with-your-projects)
4. [Workspace Layout](#workspace-layout)
5. [Infrastructure Services](#infrastructure-services)
6. [MCP Servers](#mcp-servers)
7. [Skills, Workflows & Rules](#skills-workflows--rules)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Install the following **before** starting the workspace. 
*(If you are on Windows, ensure you are running your terminal commands in **PowerShell 7** or higher, not Command Prompt).*

| Tool | Min Version | Install |
|---|---|---|
| **Node.js** | 18+ | <https://nodejs.org> |
| **Container engine** | — | Podman or Docker (see below) |
| **Git** | 2.30+ | <https://git-scm.com> |
| **AI coding tool** | — | Antigravity, VS Code + Copilot, Cursor, etc. |

### Container Engine

This workspace uses containers for PostgreSQL (pgvector) and n8n. Choose one:

| Engine | Recommended for | Install |
|---|---|---|
| **Podman** | Windows 11, Linux | <https://podman.io/getting-started/installation> |
| **Docker** | macOS, Linux | <https://docs.docker.com/get-docker/> |

> **Windows 11 Setup Tip:** Completely fresh Windows installations do not have WSL2 enabled by default. Open an **admin** PowerShell and run `wsl --install` before installing Podman or Docker Desktop, or your background container engine will fail to start.

> **Note:** The rules in this workspace default to `podman`. If you use Docker, update `.agents/rules/terminal-environment.md` (see [Customization](#customization)).

### 🔍 Verify Your Setup
Restart your terminal after installing the tools above, then run:

```bash
node -v
git --version
podman -v # or docker -v
```

If these print versions (and not "command not found"), you are ready to proceed!

---

## Quick Start

### 1. Initial Git Setup & Clone

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

### 2. Configure Environment & Secrets

This workspace uses a secure, automated setup to manage your local database passwords and environment variables without leaking them to Git.

```bash
# Generate your personal .env file and configure MCP servers
python scripts/setup_env.py
```

This script:
- Generates a secure, random password for your local PostgreSQL.
- Creates a `.env` file at the root (ignored by Git).
- Synchronizes `.vscode/mcp.json` to use a secure loader script.

### 3. Start Infrastructure

Choose the command for your container engine:

**Podman:**
```bash
podman compose -f infrastructure/compose.yaml up -d
```

**Docker:**
```bash
docker compose -f infrastructure/compose.yaml up -d
```

This starts:
- `based-workspace-postgres` — PostgreSQL 16 + pgvector on port **5432**
- `based-workspace-n8n` — n8n workflow automation on port **5678**

> [!TIP]
> Always run `setup_env.py` **before** starting your containers for the first time or whenever you want to rotate your passwords.

### 4. Open in your AI coding tool

Open the `based-workspace` folder in **Antigravity**, **VS Code**, **Cursor**, or any editor that supports the `.agents/` convention.

The AI assistant will automatically pick up:
- Rules from `.agents/rules/`
- Agent persona from `.agents/agents.md` 
- Skills from `.agents/skills/`
- Workflows from `.agents/workflows/`
- MCP servers from `.vscode/mcp.json` (running securely via `scripts/postgres-mcp.js`)

> [!TIP]
> If you don't use `grep_app`, you can disable it by adding an underscore to its name in `.vscode/mcp.json` (e.g., `"_grep_app"`). This prevents startup errors while keeping the configuration for future use.

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
│   ├── workflows/                ←   Active slash-command workflows
│   │   └── <workflow>.md
│   ├── RULES.md                  ←   Catalogue of all rules
│   ├── SKILLS.md                 ←   Catalogue of all skills
│   └── WORKFLOWS.md              ←   Catalogue of all workflows
│
├── archieved_skills/             ← 🗃️ Library of 1000+ available skills
├── archieved_workflows/          ← 🗃️ Library of 45 available workflows
│
├── .vscode/
│   └── mcp.json                  ← 🔌 MCP server config
│
├── infrastructure/
│   └── compose.yaml              ← 🐳 PostgreSQL + n8n containers
│
├── scripts/
│   ├── setup_env.py              ← 🛠️ Env initialization script
│   └── postgres-mcp.js           ← 🔑 Secure MCP credential loader
│
├── .env                          ← 🤐 Active secrets (ignored by Git)
└── README.md                     ← 📖 This file
```

---

## Infrastructure Services

Started via `compose.yaml`:

| Service | Container Name | Port | Purpose |
|---|---|---|---|
| **PostgreSQL 16 + pgvector** | `based-workspace-postgres` | `5432` | Vector memory, embeddings, project data |
| **n8n** | `based-workspace-n8n` | `5678` | Workflow automation engine |

### Common Commands

| Action | Podman | Docker |
|---|---|---|
| **Start** | `podman compose -f infrastructure/compose.yaml up -d` | `docker compose -f infrastructure/compose.yaml up -d` |
| **Stop** | `podman compose -f infrastructure/compose.yaml down` | `docker compose -f infrastructure/compose.yaml down` |
| **Logs** | `podman logs based-workspace-postgres` | `docker logs based-workspace-postgres` |
| **Status** | `podman ps` | `docker ps` |
| **Reset data** | `podman compose -f infrastructure/compose.yaml down -v` | `docker compose -f infrastructure/compose.yaml down -v` |

### Database Credentials

All credentials are encrypted/randomized locally and stored in your root `.env` file. Do not edit these directly unless you are comfortable with container environment variables.

| Key | Value (Default) | Source |
|---|---|---|
| User | `admin` | `.env` (`POSTGRES_USER`) |
| Password | *[Randomly Generated]* | `.env` (`POSTGRES_PASSWORD`) |
| Database | `ai_memory` | `.env` (`POSTGRES_DB`) |

> [!NOTE]
> To rotate your passwords, simply run `python scripts/setup_env.py` again and restart your containers.

---

## MCP Servers & Global Setup

In the **Antigravity IDE**, MCP (Model Context Protocol) servers are managed **globally**, not per-workspace. The local `.vscode/mcp.json` file in this repository serves as a **template** that you must copy to your global configuration directory.

### 1. Global Configuration Path

Copy the contents of `.vscode/mcp.json` into the following file on your machine:

| Platform | Global Configuration Path |
|---|---|
| **Windows 11** | `%USERPROFILE%\.gemini\antigravity\mcp_config.json` |
| **macOS / Linux** | `~/.gemini/antigravity/mcp_config.json` |

### 2. Required Modifications (Absolute Paths)

Antigravity executes these servers from its own internal context, so you **must use absolute paths** to the scripts inside your `based-workspace/scripts/` folder.

#### Windows Example (`mcp_config.json`):
```json
{
  "mcpServers": {
    "postgres-memory": {
      "command": "node",
      "args": ["C:/path/to/scripts/postgres-mcp.js"]
    }
  }
}
```
> [!IMPORTANT]
> - Use **forward slashes** `/` even on Windows (e.g., `C:/path/to/script.js`).
> - Use `npx.cmd` if you are calling `npx` directly on Windows.

#### macOS / Linux Example (`mcp_config.json`):
```json
{
  "mcpServers": {
    "postgres-memory": {
      "command": "node",
      "args": ["/Users/name/based-workspace/scripts/postgres-mcp.js"]
    }
  }
}
```

### 3. Why Wrapper Scripts?

This workspace provides `scripts/grep-mcp.js` and `scripts/postgres-mcp.js`. These are "wrapper" scripts that:
1. **Manage Secrets:** Securely load credentials from your `.env` file so they aren't exposed in your JSON config.
2. **Sanitize Streams:** Prevent debug logs from polluting the JSON-RPC stream, which often causes "invalid trailing data" or protocol errors in the AI tool.
3. **Environment Setup:** Ensure the correct working directory is set before spawning the actual MCP server.

---

---

## Skills, Workflows & Rules

To keep your AI assistant focused and performant, this workspace does not load all available capabilities by default. This repository provides an extensive archive.
**You must look at the skills and workflows available, select the suitable ones for your specific project, and move them to `.agents/skills/` or `.agents/workflows/`.**

### Skills (1 000+)

Pre-installed domain expertise the AI can leverage. Browse the complete archive:

**PowerShell:**
```powershell
Get-ChildItem -Path "archieved_skills" -Directory | Measure-Object                                # Count
Get-ChildItem -Path "archieved_skills" -Directory | Where-Object { $_.Name -like "*react*" }      # Search
```

**Bash / Zsh:**
```bash
ls -d archieved_skills/*/ | wc -l          # Count
ls -d archieved_skills/*react*/            # Search
```

**How to activate a skill:**
Find a skill you need in `archieved_skills/` and copy or move its folder to `.agents/skills/`.

See [`.agents/SKILLS.md`](.agents/SKILLS.md) for the full categorised catalogue.

### Workflows (45)

Slash-command automations — type in chat to trigger.

**How to activate a workflow:**
Find a workflow you need in `archieved_workflows/` and copy or move its `.md` file to `.agents/workflows/`.

Once activated, you can trigger them:

```
/new-project     — Scaffold any project
/unit-test       — Generate unit tests
/security-audit  — Scan for vulnerabilities
/deploy          — Deploy to any platform
```

See [`.agents/WORKFLOWS.md`](.agents/WORKFLOWS.md) for the full list.

### Rules (always active)

Behavioural guardrails applied to every AI interaction:

| Rule File | What It Does |
|---|---|
| `terminal-environment.md` | Enforces correct shell syntax and container engine |
| `workspace-boundaries.md` | Restricts DB/automation to the local containers |

See [`.agents/RULES.md`](.agents/RULES.md) for the full list.

---

## Customization

### Change container engine (Podman → Docker)

Edit `.agents/rules/terminal-environment.md`:

```diff
- * Container Engine: Podman
+ * Container Engine: Docker
```

And update directive 3:

```diff
- 3. **Container Precedence:** always use `podman` and `podman compose`.
+ 3. **Container Precedence:** always use `docker` and `docker compose`.
```

### Change shell (PowerShell → Bash/Zsh)

Edit `.agents/rules/terminal-environment.md`:

```diff
- * Primary Shell: PowerShell 7
+ * Primary Shell: Zsh
```

### Add a new rule

Create a markdown file in `.agents/rules/`:

```yaml
---
trigger: always_on
---

# My Custom Rule

- Description of what the AI should always do.
```

### Add a new skill

Create a folder in `.agents/skills/my-skill/SKILL.md`:

```yaml
---
name: my-skill
description: What this skill does
---

# My Skill

Instructions for the AI when this skill is activated.
```

### Add a new workflow

Create a file in `.agents/workflows/my-workflow.md`:

```yaml
---
description: Short description of the workflow
---

1. Step one
2. Step two
3. Step three
```

Trigger it with `/my-workflow` in chat.

---

## Troubleshooting

### Containers won't start

```bash
# Check if port 5432 or 5678 is already in use:

# Windows (PowerShell)
Get-NetTCPConnection -LocalPort 5432 | Select-Object OwningProcess

# macOS / Linux
lsof -i :5432
```

### MCP Servers (Global Setup)

- **`EINVAL` or `EOF` errors:** This usually means the path to your script is incorrect or Node.js cannot find the file. Double-check your absolute paths in `mcp_config.json`.
- **"Invalid trailing data":** This happens when a script prints non-JSON text to its output. Always use our provided wrapper scripts in `scripts/` to sanitize the output.
- **Windows execution:** Ensure your wrapper scripts (like `postgres-mcp.js`) use `shell: true` when spawning child processes on Windows to handle `.cmd` files correctly.
- **Connection Refused:** Ensure your Podman/Docker containers are running (`podman ps`). The `postgres-memory` server cannot connect if the database container is down.
- **Manual Reload:** After editing your global `mcp_config.json`, you must restart Antigravity or reload the window (`Ctrl+Shift+P` -> `Developer: Reload Window`) for changes to take effect.

### Skills not loading

- Ensure the workspace root is opened in your AI tool (not a subfolder)
- Check that `.agents/` exists in the workspace root
- Verify `agents.md` exists in `.agents/`

### n8n web UI

Open <http://localhost:5678> in your browser after starting infrastructure.

---

## License

MIT — Use freely, modify as needed.
