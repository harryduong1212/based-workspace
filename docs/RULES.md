# Antigravity Rules 📐

**Active behavioral rules enforced across all AI agent interactions.**

---

## How Rules Work

| Layer | File | Scope | Priority |
|---|---|---|---|
| **Global** | `terminal-environment.md` | All projects, all conversations | Highest — always enforced |
| **Project** | `.agents/agents.md` | This workspace only | Applied when working in `based-workspace` |

---

## Global Rules (User Rules)

> **Source:** `terminal-environment.md`

| # | Rule | Purpose |
|---|---|---|
| 1 | Use the syntax of the Primary Shell defined in metadata | OS compliance — avoid shell-specific aliases |
| 2 | Probe command availability before complex chains | Safety — avoid broken execution |
| 3 | Use the Container Engine defined in metadata | Container engine preference (Podman/Docker) |
| 4 | Prefer `npx` or Python scripts for OS-dependent file operations | Cross-platform reliability |

---

## Project Rules (agents.md)

> **Source:** [agents.md](.agents/agents.md)
>
> **Persona:** AI Integration Architect

| # | Rule | Category |
|---|---|---|
| 1 | Always invoke `context7` for the latest documentation before writing code | 📖 Research First |
| 2 | Use `grep_app` to discover open-source implementation patterns for new architectures | 🔍 Pattern Discovery |
| 3 | Store persistent project context and vector embeddings in the `postgres-memory` database | 🧠 Memory |
| 4 | Design integration workflows to be executed on the local `n8n-atom` (Quickstart) or `n8n-atom-dev` (Developer) instance | ⚙️ Workflow Engine |
| 5 | Before building any feature, check `.agents/skills/` for an existing skill that covers the domain | 🎯 Skill Reuse |
| 6 | Consult `.agents/WORKFLOWS.md` when a task matches a repeatable workflow | 📋 Workflow Reuse |
| 7 | Always verify changes compile/lint/pass tests before reporting completion | ✅ Verification |
| 8 | Use syntax appropriate for the Primary Shell of the current environment | 💻 Environment |

---

## Adding New Rules

Edit [agents.md](.agents/agents.md) and add a new bullet under `## Rules`:

```markdown
## Rules
- Your new rule here.
```

Rules are enforced automatically on every interaction within this workspace.

---

> **Total Active Rules:** 13 (4 global + 9 project)
