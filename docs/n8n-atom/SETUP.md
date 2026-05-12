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

The `infrastructure/core/` compose now pulls the upstream `docker.io/atom8n/n8n:fork` image directly — no local n8n build step is needed. (Mode 2's `build_n8n_atom.py --all` is still useful for compiling the MCP Inspector from the submodule; see "Optional: MCP Inspector" below.)

```bash
# 1. Set up secrets (one-time). The script PRINTS to stdout — paste into .env yourself.
cp .env.example .env
./scripts/gen_secrets.sh
./scripts/install-git-hooks.sh    # gitleaks pre-commit, blocks accidental secret commits

# 2. Start Postgres + n8n.
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
```

After n8n is healthy, browse to http://localhost:5678, complete owner setup (one-time), then **Settings → API → Create API Key**. Paste that value into `.env` as `N8N_API_KEY` and (separately) into the `atom8n.n8n-atom-v3` Antigravity extension's settings sidebar — the extension does **not** read `.env`.

**Optional: MCP Inspector** runs host-native (not via compose) per the [upstream readme](https://github.com/khanh-atom/cp-inspector-atom8n):

```bash
./scripts/mcp-inspector.sh start    # http://localhost:6274
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
cp .env.example .env
./scripts/gen_secrets.sh          # prints randoms — paste into .env
./scripts/install-git-hooks.sh    # gitleaks pre-commit secret scanner
```

### Stage 3: Launch
```bash
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
# Optional: build + start the MCP Inspector (host-native, not via compose)
python scripts/build_n8n_atom.py --mcp
./scripts/mcp-inspector.sh start
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
podman compose --env-file .env -f infrastructure/n8n-quickstart/docker-compose.quickstart.yaml up -d
```

### Password authentication failed for user "admin"
Postgres only reads `POSTGRES_PASSWORD` from env on the first boot of an empty volume. If you rotate the value in `.env` after that, the DB role still has the old password — n8n will fail to connect with the new one.

**Fix A (lossless — preserves Context Bridge data):** `ALTER USER` inside the running container.
```bash
set -a && source .env && set +a
podman exec -i -e NEW="$POSTGRES_PASSWORD" -e POSTGRES_USER -e POSTGRES_DB \
  based-workspace-postgres sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 <<SQL
\set newpw `echo "$NEW"`
ALTER USER "'"$POSTGRES_USER"'" WITH PASSWORD :'\''newpw'\'';
SQL'
podman restart n8n-atom-dev
```

**Fix B (destructive — wipes all data in the volume):**
```bash
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom down -v
podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d
```

### Mismatching encryption keys
Symptom: `Error: Mismatching encryption keys. The encryption key in the settings file /home/node/.n8n/config does not match the N8N_ENCRYPTION_KEY env var.`

n8n caches its encryption key in `/home/node/.n8n/config` inside the volume on first boot. If `.env`'s `N8N_ENCRYPTION_KEY` changes (or was previously unset and just got added), the two no longer match.

**Fix:** Overwrite the volume's `config` file to match `.env` (acceptable if no credentials are stored in n8n yet; otherwise restore the *original* key in `.env` instead so stored credentials remain decryptable):

```bash
set -a && source .env && set +a
podman stop n8n-atom-dev >/dev/null
podman run --rm -v infrastructure-core_based-workspace-n8n-data:/d \
  -e KEY="$N8N_ENCRYPTION_KEY" \
  alpine sh -c 'printf "{\n\t\"encryptionKey\": \"%s\"\n}\n" "$KEY" > /d/config && chown 1000:1000 /d/config'
podman start n8n-atom-dev
```

### Container fails to start due to OOM
Ensure you have successfully allowed at least **8GB of Memory** to your container engine (via `.wslconfig` on Windows or `podman machine init --memory 8192` on Mac). Node module builds are heavy.
