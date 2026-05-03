# Advanced Usage: The True Autonomous OS

> **⚠️ Legacy doc.** This document describes the previous symlink/profile-based architecture. Some referenced scripts (`workspace_manager.py`, `asset_manager.py`, `profile_manager.py`, `profiles.json`) **no longer exist** — they were removed when the workspace migrated to a recipe-driven model. Read [PRODUCT_PLAN.md](PRODUCT_PLAN.md) for the current architecture and [RECIPE_SPEC.md](RECIPE_SPEC.md) for the recipe format. The infrastructure and MCP sections below are still accurate.

---


If you are just writing code and asking the AI for syntactical fixes, you are only scratching the surface of **based-workspace**. 

This system is not simply an integration between an editor and an LLM; it is an **Autonomous AI Operating System**. The "Advanced" nature of this workspace is defined by three core capabilities:

1. **Agentic Context Orchestration**: Dynamically reshaping the AI's "brain" via explicit context sharding.
2. **Invisible Self-Configuration**: The AI can modify its own underlying capability set based on your natural language intent.
3. **The Local Autonomous Stack**: Hooking the AI's intelligence into a deterministic, local `n8n-atom` automation engine backed by `pgvector` memory.

---

## 🧠 1. Agentic Context Orchestration

A standard AI editor has a fixed context. Most developers try to squeeze all their documentation, prompt guidelines, and domain rules into a single `.rules` file. 

This causes **Hallucination** and **Context Dilution**. An AI acting as a DevOps engineer evaluates problems differently than an AI acting as a UI/UX designer. If you give an LLM both sets of rules at once, it compromises.

### The Sharded Capability Library
Our workspace contains a massive partitioned library in `.archived/` holding over 400+ exact methodologies, rules, and workflows (skills). Instead of dumping this into the AI, we use **Profiles** to inject only what is explicitly needed.

- **How it works:** When you switch to a profile (e.g., `backend-sec`), the workspace symlinks specific isolated shards of knowledge into the `.agents/skills/` directory. 
- **The Result:** The AI gains immediate, hyper-focused "muscle memory" for that precise domain. Unrelated disciplines are pruned from the context window, resulting in drastically higher intelligence per token.

### Contextual Sub-Roles
Profiles are grouped precisely by functional suites:
- **`-dev`**: Pure active development algorithms.
- **`-ops`**: Infrastructure, deployment, Docker compose, and network security policies.
- **`-sec`**: Fuzzing, penetrative auditing, and zero-day patch techniques.

---

## 🪄 2. Invisible Self-Configuration

You never actually have to touch Python scripts to change your profile. The workspace implements an invisible, recursive management tool: the **`workspace-configurator` skill**.

### The Flow
1. **You speak naturally**: *"Hey, I need to do a deep security audit on this Express application."*
2. **The AI intercepts**: The Agent detects the intent using its embedded `workspace-configurator` capability.
3. **The AI executes against itself**: Behind the scenes, the AI executes a terminal command against `scripts/workspace_manager.py`, requesting the `security-core` profile.
4. **Context shifts instantly**: The AI's `.agents/skills` folder flushes out existing generic coding rules, and fills up with penetration testing, OAuth, and cryptography patterns.
5. **The Audit Begins**: The AI now begins the audit using the new brain it just gave itself.

**This is what makes it advanced.** The workspace acts as a self-aware entity that can summon different "expert consultants" (itself) by reorganizing its own filesystem.

---

## ⚙️ 3. The Local Autonomous Stack

While the Sharded Capability Library acts as the AI's brain, you need a body to execute complex background tasks. This is why **n8n-atom** and the **MCP Inspector** are natively bundled into the core infrastructure.

### The n8n-atom Engine
Instead of writing hacky bash scripts to map data, you can build autonomous, infinitely-running processes locally using `n8n`.
1. **Webhook Reception**: Build local endpoints that receive GitHub webhooks, JIRA tickets, or system metrics.
2. **Model Context Protocol (MCP)**: Directly connect your `n8n` workflows to your AI assistant. The AI can trigger a n8n workflow as a specific "tool", handing off deterministic backend extraction to the automation engine while it moves on to the next task.
3. **Ghost Sync Injection**: You can test workflow designs by piping them straight from your editor's visual Webview into the `n8n-dev` container backend safely behind localhost loopbacks.

### Persistent Vector Memory
The included local PostgreSQL cluster isn't just for saving n8n states. It is compiled with `pgvector`. 
- **Usage**: You can execute scripts that index your logs, codebase structures, or even past chat transcripts locally, enabling the AI to query historical context securely without exposing proprietary architectures to the cloud.

---

## Appendix: Manual Registry & Scripts
*(Only needed if you are developing the workspace itself, or adding raw new assets)*

### Safe Reorganization (`asset_manager.py`)
When you manually drop new markdown files into `.archived/`, the system doesn't know about them yet. You must dynamically tag and shard them:

```bash
# Analyze files, extract Deep Tags (e.g. `fastapi`, `tailwind`, `grpc`), and rebuild indices.
python scripts/asset_manager.py reorganize_skills
python scripts/asset_manager.py reorganize_workflows
```

### Manual Profile Management (`workspace_manager.py`)
If you want to bypass the AI and hard-switch the symlink context yourself:
```bash
python scripts/workspace_manager.py --profile <profile-name>
```
