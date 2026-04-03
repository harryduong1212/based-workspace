# n8n-atom Setup Guide

Welcome to the unified setup guide for `n8n-atom` and the `MCP Inspector`. Depending on your goals, choose the mode that fits your needs:

- **[Mode 1: Quickstart (User Mode)](#mode-1-quickstart)**: The fastest way to run n8n-atom using pre-built images. No coding required.
- **[Mode 2: Developer Mode](#mode-2-developer-mode)**: Build the containers from source locally. Essential for modifying the codebase.
- **[Mode 3: Zero-to-Hero Test Plan](#mode-3-zero-to-hero-global-test-plan)**: Step-by-step instructions for deploying from scratch on a brand new laptop (Windows/macOS/Linux).

---

## Mode 1: Quickstart

Get **n8n-atom** and the **MCP Inspector** running locally with a single command.

### 1. Prerequisites
You only need a container engine. Pick one:

| Engine | Install |
|---|---|
| **Podman** (recommended) | [podman.io](https://podman.io/getting-started/installation) |
| **Docker** | [docker.com](https://docs.docker.com/get-docker/) |

### 2. Start
```bash
# Podman
podman compose -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml up -d

# Docker
docker compose -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml up -d
```

This starts three containers:
| Service | URL | Description |
|---|---|---|
| **n8n-atom** | [http://localhost:5678](http://localhost:5678) | Workflow automation engine (upstream `atom8n/n8n:fork`) |
| **MCP Inspector** | [http://localhost:6274](http://localhost:6274) | Official MCP diagnostics UI |
| **PostgreSQL** | `localhost:5432` | Database backend (pgvector-enabled) |

### 3. Stop
```bash
podman compose -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml down
```

---

## Mode 2: Developer Mode

This mode is for **developers** who want to build the ecosystem from source using our Ephemeral Git-Archive Builder pipeline.

### 1. Advanced Prerequisites
In addition to a container engine, you need **Python 3.8+** to orchestrate the builds and **Git** to package the source code. Make sure you allocate **8GB+ RAM** to your container engine to handle native Node module compilation.

### 2. Build Pipeline
We use an isolated Linux container to compile the source code, eliminating Windows NTFS file path issues and cross-platform native compilation errors.

```bash
# Build everything (n8n-atom + MCP Inspector)
python scripts/build_n8n_atom.py --all

# Clean rebuild (wipes everything including persistent volumes)
python scripts/build_n8n_atom.py --clean --all
```

**Verify the build via:**
```bash
python scripts/build_n8n_atom.py --check
```

### 3. Launching
You must generate database credentials first, and pass the `.env` file into compose so variables interpolate correctly:

```bash
# 1. Generate secrets (creates .env)
python scripts/setup_env.py

# 2. Start the Dev runtime
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d --build
```

---

## Mode 3: Zero-to-Hero Global Test Plan

This section serves as a step-by-step tutorial to validating the full development environment on any brand new machine.

### Stage 1: Environment Preparation

<details>
<summary><strong>🪟 Windows</strong></summary>

1.  **Enable WSL2**: Open PowerShell as Admin and run `wsl --install`. Restart if prompted.
2.  **Memory Allocation**: Create `%USERPROFILE%\.wslconfig` and add:
    ```ini
    [wsl2]
    memory=8GB
    ```
    (Run `wsl --shutdown` to apply).
3.  **Install Tools**:
    ```powershell
    winget install --id Git.Git -e --source winget
    winget install -e --id Python.Python.3.11
    winget install -e --id RedHat.Podman-Desktop
    ```
</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

1.  **Install Homebrew**: See [brew.sh](https://brew.sh).
2.  **Install Tools**:
    ```bash
    brew install git python podman podman-desktop
    ```
3.  **Initialize Podman VM**:
    ```bash
    podman machine init --memory 8192
    podman machine start
    ```
</details>

<details>
<summary><strong>🐧 Linux (Ubuntu/Debian)</strong></summary>

1.  **Install Tools**:
    ```bash
    sudo apt update && sudo apt install git python3 podman
    ```
2.  **Rootless Setup**: Ensure your user has subuid/subgid mapping.
</details>

### Stage 2: Clone & Init
```bash
git clone --recurse-submodules https://github.com/harryduong1212/based-workspace.git
cd based-workspace
python scripts/setup_env.py
```

### Stage 3: Build & Launch
```bash
python scripts/build_n8n_atom.py --all
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d --build
```

### Stage 4: Verify Health
Wait 30-60 seconds for initialization:
- **n8n Backend Health**: [http://localhost:5678/healthz](http://localhost:5678/healthz) → `{"status":"ok"}`
- **MCP Inspector UI**: [http://localhost:6274](http://localhost:6274) → UI loads successfully.

---

## FAQ & Troubleshooting

### Where is my data stored?
Your workflows, credentials, and database are stored in Docker/Podman **volumes**. They persist across container restarts and even across `down` / `up` cycles.

### How do I update the quickstart pre-built images?
```bash
podman pull atom8n/n8n:fork
podman pull ghcr.io/modelcontextprotocol/inspector:latest
podman compose -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml up -d
```

### Password authentication failed for user "admin"
If you run `scripts/setup_env.py` again, it generates a new PostgreSQL password. However, if your database volume (`infrastructure-core_based-workspace-postgres-data`) was already created with the *old* password, n8n will crash loop.

**Fix:** Delete the persistent volume to restart fresh:
```bash
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom down -v
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
```

### Container fails to start due to OOM
Ensure you have successfully allowed at least **8GB of Memory** to your container engine (via `.wslconfig` on Windows or `podman machine init --memory 8192` on Mac). Node module builds are heavy.
