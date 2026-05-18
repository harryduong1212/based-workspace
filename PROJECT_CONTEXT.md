# Project Context: based-workspace

## 1. Project Baseline
`based-workspace` is a development environment for AI-assisted engineering, organized around three user-facing concepts: **Recipes** (tasks invoked from chat or CLI), **Connectors** (declarations of external data sources like Jira, Bitbucket), and **Routines** (recipes wrapped in n8n cron schedules). It solves AI context bloat by keeping recipes self-contained and by treating `.archived/skills/` (159 active, 180 vaulted) as a *reference library* consulted when composing recipes, not as runtime context. Containerized infrastructure (PostgreSQL with `pgvector` + n8n) provides the embedding store and automation engine. Provider-specific bindings for Antigravity (`.agents/workflows/`) and Claude Code (`.claude/commands/`) are auto-generated from `recipes/`. See `docs/PRODUCT_PLAN.md` for the full architecture.

## 2. High-Level Architecture & Guidelines
- **Modular Context Symlinking**: AI assets (personas, rules, tools) reside centrally under `.archived/` and are selectively symlinked into the active `.agents/` footprint via profiling to keep context scope strict.
- **Strict Execution Rules**: Behavioral guards are enforced locally via `.agents/rules/`. Specifically, `terminal-environment.md` enforces safe execution limits (e.g., matching the host Windows 11 PowerShell syntax, container primacy, and OS-agnostic command preferences). 
- **Workspace Boundaries**: According to `workspace-boundaries.md`, AI agents are strictly constrained to leverage the local `based-workspace-postgres` container for all vector memory use cases, and `based-workspace-n8n` for process automation deployment.
- **Hierarchical Documentation**: Centralized guides (`SKILLS.md`, `WORKFLOWS.md`, `RULES.md`, `MCP_GUIDE.md`) form the "source of truth", while `ADVANCED_USAGE.md` provides guidance on ecosystem customization and symlinking projects dynamically into the engine.

## 3. Infrastructure & Deployment
- **Core Services**:
  - **`based-workspace-postgres`**: PostgreSQL 16 with `pgvector`, published on the host port set by `${POSTGRES_PORT}` in `.env` (default `5432`; container-internal stays `5432`). It serves as the relational backbone for both n8n state and Context Bridge embeddings.
  - **`n8n-atom-dev`**: n8n on port `5678`, pulled from `docker.io/atom8n/n8n:fork` (no source build). Uses the shared Postgres above for storage and `N8N_ENCRYPTION_KEY` from `.env` for credential encryption.
  - **MCP Inspector**: Runs **host-native** via `./scripts/mcp-inspector.sh start` (ports `6274`/`6277`) so it can read host-side IDE configs at `~/.cursor/mcp.json`, `~/.gemini/antigravity/mcp_config.json`. The compose `mcp-inspector` profile is preserved as a containerized fallback only.
- **Orchestration**: `podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d` is the canonical command. The legacy `infrastructure/n8n-quickstart/docker-compose.quickstart.yaml` exists but hardcodes credentials and does not share the workspace Postgres.
- **Control Panel UI** (`services/control_panel/`): FastAPI (`:8765`) + Next.js (`:3000`) app that wraps the install / start / verify primitives for every workspace feature (containers, MCP servers, recipes, connectors). Browsable at `http://localhost:3000` via `./scripts/dev.sh`. The backend talks directly to `podman compose` and the same registry the CLI uses; it is the user-facing entry point for installing components like the **memory** MCP (mem0 + qdrant) without memorising compose commands.
- **State Management**: Docker volumes handle state persistence. `based-workspace-postgres-data` stores the pg_data and vector embeddings; `based-workspace-n8n-data` persists automation states, workflow schemas, and engine configs.

## 4. Automation & AI Integration (MCP/Agents)
- **Agent Registry**: Skills are indexed efficiently via Machine-readable definitions like `registry.json` (such as `.archived/skills/*/registry.json` and active ones). The engine currently ships 159 active skills across 37 architectural domains (from APIs to TDD); an additional 180 skills are vaulted at `.archived/_vault/skills/` for reference.
- **Automation Engine**: `n8n` acts as the underlying execution automation engine, driving repetitive processes (like `feature-kickoff` setups, registry maintenance, or `git-commit-group-changes` structuring).
- **MCP Bridges**: The `.vscode/mcp.json` manage the tool communication layer for the IDE. Supported plugins include:
  - `postgres-memory`: A bridge mapping local LLM context against the `pgvector` container.
  - `atom8n`: MCP-driven execution of specific `.n8n` workflows (e.g., generic CURL agents and HTTP logging via the local automation engine).
  - `context7` (docs retrieval) and `grep_app` (local and semantic syntax queries).

## 5. Workspace Profiles
- **`base-core`**: The foundational suite enabling core development capabilities, documentation autogeneration tooling, test automation setups, and essential workflows like `git-commit-group-changes`.
- **`project-manager-pro`**: Technical leadership contextualization; loaded with structural analysis skills, architectural diagrams, market sizing evaluation, feature spec kickoffs, and PM orchestration toolkits.
- **`backend-ultimate`**: An exhaustive context package for full backend engineering. It incorporates core dependencies, AI generation toolkits, DevOps ops pipelines, security hardening patterns, and deep database configuration capacities.
- **`creator-pro`**: Built for workspace automation & AI Capability Engineering—equips the IDE with MCP builders, skill generation logic, environment analyzer workflows, and AI sub-agent builders.
- **`devops-ultimate`**: Concentrated on infrastructure-as-code and operations context (Kubernetes deployments, ISTIO meshes, CI/CD, Docker configurations).

## 6. Environment & Tooling
- **Languages/Frameworks**: Node.js 18+ (core ecosystem requirements and CLI), Python 3.x (scripts runtime), Podman/Docker (container engines), and PowerShell 7.
- **Bootstrapping**:
  1. Validate prerequisites (Node, Python, Podman, Git).
  2. Configure secrets:
     - `cp .env.example .env` (template covers every in-use key with comments + paste-from-URL hints).
     - `./scripts/gen_secrets.sh` prints fresh `POSTGRES_PASSWORD` and `N8N_ENCRYPTION_KEY` to stdout for paste-into-`.env`.
     - `./scripts/install-git-hooks.sh` installs gitleaks + a pre-commit hook that blocks staged secrets.
     - `N8N_API_KEY` is paste-from-source only: create it in the n8n UI (Settings → API → Create API Key) after owner setup.
  3. Spin up orchestration: `podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d`.
  4. (Optional) Start the host-native MCP Inspector: `./scripts/mcp-inspector.sh start`.
  5. Browse available recipes: `python scripts/recipe_manager.py list`. Run one: `python scripts/recipe_manager.py run <id>`.

## 7. Known Edges & Dependencies
1. **`infrastructure/core/` n8n image is pulled, not built**: the compose pulls `docker.io/atom8n/n8n:fork`; there is no build step in the workspace. The MCP Inspector now runs **host-native** via `./scripts/mcp-inspector.sh`. The legacy `mcp-inspector` compose profile and `scripts/build_n8n_atom.py` reference deleted submodule paths (`external/n8n-atom/`, `external/mcp-inspector-atom8n/`) and are non-functional; clone the upstream repos manually if you need to build either image.
2. **Postgres password rotation pitfall**: Postgres init only reads `POSTGRES_PASSWORD` on the first boot of an empty volume. Rotating the env value later does not update the DB role — n8n will fail to connect with the new password. Either delete the volume (`down -v`) or `ALTER USER` inside the running container.
3. **Implicit Container Engines**: Workspace instructions default strictly to Podman mechanics unless an end-user intervenes via manually mutating `terminal-environment.md`.
4. **Antigravity n8n extension API key**: `atom8n.n8n-atom-v3` stores its API key in Antigravity's per-user state (separate from `.env`). Paste the value into the extension's settings sidebar after creating it in the n8n UI; the value in `.env` is for server-side consumers (Control Panel, MCP Inspector), not the IDE extension.
