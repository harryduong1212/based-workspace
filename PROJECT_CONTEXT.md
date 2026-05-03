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
  - **`based-workspace-postgres`**: PostgreSQL 16 packed with `pgvector` serving on port `5432`. It forms the backbone for AI memory storage and acts as the relational database engine for n8n.
  - **`n8n-atom` (`n8n-atom-dev`)**: An n8n automation workflow engine serving on port `5678`. It executes custom automations and exposes workflow webhooks.
  - **`mcp-inspector-dev`**: Tooling for configuring and inspecting Model Context Protocol (MCP) interactions locally, typically operating on ports `6274`/`6277`.
- **Orchestration**: Infrastructure is spun up via Docker/Podman compose configurations. Specifically, `infrastructure/core/docker-compose.yaml` (developer source build mode) triggers the full stack, while `infrastructure/n8n-quickstart/docker-compose.quickstart.yaml` can be used for streamlined baseline activation.
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
  2. Instantiate local configurations: `python scripts/setup_env.py` generates deterministic secure passwords, updates `.env`, and configures MCP bridging endpoints.
  3. Spin up orchestration: Leverage `podman compose --env-file .env -f infrastructure/core/docker-compose.yaml --profile n8n-atom up -d --build`.
  4. Browse available recipes: `python scripts/recipe_manager.py list`. Run one: `python scripts/recipe_manager.py run <id>`.

## 7. Known Edges & Dependencies
1. **Missing Requisite Source Code Context in `core/docker-compose.yaml`**: Since the `external/` sub-repository (`n8n-atom` and `mcp-inspector-atom8n`) was recently removed in favor of GHCR remote images (and CI/CD pipelines), the builder references in `infrastructure/core/docker-compose.yaml` (e.g., `context: ../../external/n8n-atom/build_context`) exist but correctly link to removed folders. Developers executing source builds may hit absent submodules if relying exclusively on native builds locally unless using the Quickstart compose files or standard image pulls.
2. **Environment Variable Generation**: Using Git tracking requires strictly enforcing `.gitignore` bounds around `.env` and `.agents/` logic overrides because `scripts/setup_env.py` mutates local variables securely.
3. **Implicit Container Engines**: Workspace instructions default strictly to Podman mechanics unless an end-user intervenes via manually mutating `terminal-environment.md`.
