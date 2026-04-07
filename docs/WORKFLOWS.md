# Antigravity Workflows 🚀

**Stack-agnostic, question-driven workflows for the Antigravity IDE.**

> Sourced from [antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)

---

## ⚡ Quick Start

Trigger any workflow by typing its slash command in the chat:

| Feature | Commands |
|---|---|
| **Project Setup** | `/new-project`, `/new-component`, `/new-api` |
| **Git Automation** | `/git-commit`, `/git-pr`, `/git-conflict` |
| **Testing** | `/unit-test`, `/e2e-test`, `/playwright-test` |
| **Deployment** | `/deploy`, `/docker`, `/railway-deploy` |

---

---

## 🛠️ Companion Tools

Need to extend the workspace? Use these specialized creators:

| Tool | Command | Description |
|---|---|---|
| **Workflow Creator** | `/workflow-creator` | Build new multi-step developer workflows |
| **Skill Creator** | `/skill-creator` | Create specialized expert knowledge modules |

---

## 🏗️ Philosophy

| Principle | Description |
|---|---|
| **Stack-Agnostic** | Works with React, Vue, Angular, Django, or any stack |
| **Question-Driven** | Asks clarifying questions for better results |
| **Progressive Disclosure** | Loads minimal context first, expands on demand |
| **Single Responsibility** | Each workflow does ONE thing well |
| **Composable** | Combine workflows for complex tasks |

---

## 📂 Available Workflows (19)

### ⚙️ Configuration
<details>

| Workflow | Command | Status | Description |
|---|---|---|---|
| [env-config](.archived/workflows/configuration/env-config.md) | /env-config | ✅ Ready | Manage environment variables securely |

</details>

### 🎨 Creative & UI
<details>

| Workflow | Command | Status | Description |
|---|---|---|---|
| [dashboard-ui](.archived/workflows/creative-ui/dashboard-ui.md) | /dashboard-ui | ✅ Ready | Create admin dashboards (any stack) |
| [email-template](.archived/workflows/creative-ui/email-template.md) | /email-template | ✅ Ready | Design responsive emails |

</details>

### 🎯 Custom Workflows
<details>

| Workflow | Command | Status | Description |
|---|---|---|---|
| [feature-deep-dive](.archived/workflows/custom-workflows/feature-deep-dive.md) | /feature-deep-dive | ✅ Ready | ✅ Ready |
| [feature-kickoff](.archived/workflows/custom-workflows/feature-kickoff.md) | /feature-kickoff | ✅ Ready | 🚀 Orchestration from Raw Idea -> SRS -> DB -> API -> Sequence -> Test Prep |
| [generate-api-spec](.archived/workflows/custom-workflows/generate-api-spec.md) | /generate-api-spec | ✅ Ready | 🔌 Generates standardized API contracts based on the SRS and DB Schema |
| [generate-db-schema](.archived/workflows/custom-workflows/generate-db-schema.md) | /generate-db-schema | ✅ Ready | 🗄️ Transforms SRS into a finalized database schema and ERD |
| [generate-feature-spec](.archived/workflows/custom-workflows/generate-feature-spec.md) | /generate-feature-spec | ✅ Ready | 📋 Coordination to transform a raw idea into a standardized SRS |
| [generate-sequence-diagram](.archived/workflows/custom-workflows/generate-sequence-diagram.md) | /generate-sequence-diagram | ✅ Ready | 🔀 Maps the interaction flow between users, system, and services |
| [git-commit-group-changes](.archived/workflows/custom-workflows/git-commit-group-changes.md) | /git-commit-group-changes | ✅ Ready | 📦 Automatically groups and commits changes by logical feature |
| [prepare-test-environment](.archived/workflows/custom-workflows/prepare-test-environment.md) | /prepare-test-environment | ✅ Ready | ✅ Ready |

</details>

### 🔀 Git & Collaboration
<details>

| Workflow | Command | Status | Description |
|---|---|---|---|
| [git-commit](.archived/workflows/git-collaboration/git-commit.md) | /git-commit | ✅ Ready | Generate conventional commits from staged changes |
| [git-conflict](.archived/workflows/git-collaboration/git-conflict.md) | /git-conflict | ✅ Ready | Help resolve merge conflicts |
| [git-pr](.archived/workflows/git-collaboration/git-pr.md) | /git-pr | ✅ Ready | Create comprehensive PR descriptions |
| [git-rebase](.archived/workflows/git-collaboration/git-rebase.md) | /git-rebase | ✅ Ready | Interactive rebase assistance |

</details>

### 🤖 AI & LLM
<details>

| Workflow | Command | Status | Description |
|---|---|---|---|
| [prompt-engineering](.archived/workflows/ai-llm/prompt-engineering.md) | /ai-llm-prompt-engineering | ✅ Ready | ✅ Ready |
| [rag-pipeline](.archived/workflows/ai-llm/rag-pipeline.md) | /ai-llm-rag-pipeline | ✅ Ready | ✅ Ready |
| [workflow-creator](.archived/workflows/ai-llm/workflow-creator.md) | /workflow-creator | ✅ Ready | Create new antigravity workflows |

</details>

### 🧪 Testing & Quality
<details>

| Workflow | Command | Status | Description |
|---|---|---|---|
| [code-review](.archived/workflows/testing-quality/code-review.md) | /code-review | ✅ Ready | Comprehensive code review |

</details>

---

## 🤝 Contributing

To add a new workflow:
1. Develop it in `/tmp/my-workflow.md`
2. Run `python scripts/reorganize_workflows_safe.py --target /tmp/my-workflow.md` to auto-categorize.

---

> **Repo:** [github.com/harikrishna8121999/antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)
