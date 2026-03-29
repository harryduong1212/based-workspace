# Antigravity Workflows 🚀

**Stack-agnostic, question-driven workflows for AI coding assistants.**

> Sourced from [antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)

---

## Philosophy

| Principle | Description |
|---|---|
| **Stack-Agnostic** | Works with React, Vue, Angular, Django, or any stack |
| **Question-Driven** | Asks clarifying questions for better results |
| **Progressive Disclosure** | Loads minimal context first, expands on demand |
| **Single Responsibility** | Each workflow does ONE thing well |
| **Composable** | Combine workflows for complex tasks |

---

## Usage

Trigger any workflow by typing its slash command in the chat:

```
/git-commit
/unit-test
/deploy
```

---

## Available Workflows (45)

### 🔧 Development
<details>
<summary><b>🔧 Development (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [new-project](.archived/workflows/development/new-project.md) | `/new-project` | Scaffold any project (detects or asks for stack) |
| [new-component](.archived/workflows/development/new-component.md) | `/new-component` | Create reusable UI components (any framework) |
| [new-api](.archived/workflows/development/new-api.md) | `/new-api` | Create API endpoints (any backend) |
| [new-feature](.archived/workflows/development/new-feature.md) | `/new-feature` | Full feature implementation from design to deployment |
| [refactor](.archived/workflows/development/refactor.md) | `/refactor` | Improve code quality, extract, reduce duplication |
| [migrate](.archived/workflows/development/migrate.md) | `/migrate` | Technology migrations (JS→TS, framework upgrades) |
| [cli-tool](.archived/workflows/development/cli-tool.md) | `/cli-tool` | Build command-line applications |

</details>

### 🔀 Git & Collaboration
<details>
<summary><b>🔀 Git & Collaboration (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [git-commit](.archived/workflows/git-collaboration/git-commit.md) | `/git-commit` | Generate conventional commits from staged changes |
| [git-pr](.archived/workflows/git-collaboration/git-pr.md) | `/git-pr` | Create comprehensive PR descriptions |
| [git-conflict](.archived/workflows/git-collaboration/git-conflict.md) | `/git-conflict` | Help resolve merge conflicts |
| [git-rebase](.archived/workflows/git-collaboration/git-rebase.md) | `/git-rebase` | Interactive rebase assistance |

</details>

### 🧪 Testing & Quality
<details>
<summary><b>🧪 Testing & Quality (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [unit-test](.archived/workflows/testing-quality/unit-test.md) | `/unit-test` | Generate unit tests (detects testing framework) |
| [e2e-test](.archived/workflows/testing-quality/e2e-test.md) | `/e2e-test` | End-to-end browser tests |
| [playwright-test](.archived/workflows/testing-quality/playwright-test.md) | `/playwright-test` | Browser automation tests with Playwright |
| [test-coverage](.archived/workflows/testing-quality/test-coverage.md) | `/test-coverage` | Improve test coverage for files |
| [code-review](.archived/workflows/testing-quality/code-review.md) | `/code-review` | Comprehensive code review |

</details>

### 🐛 Debugging
<details>
<summary><b>🐛 Debugging (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [debug-error](.archived/workflows/debugging/debug-error.md) | `/debug-error` | Analyze errors and suggest fixes |
| [debug-log](.archived/workflows/debugging/debug-log.md) | `/debug-log` | Add strategic logging/debugging |
| [performance](.archived/workflows/debugging/performance.md) | `/performance` | Profile and optimize slow code |

</details>

### 🔒 Security
<details>
<summary><b>🔒 Security (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [security-audit](.archived/workflows/security/security-audit.md) | `/security-audit` | Scan for vulnerabilities and secrets |
| [dependency-check](.archived/workflows/security/dependency-check.md) | `/dependency-check` | Check for vulnerable dependencies |
| [auth-implementation](.archived/workflows/security/auth-implementation.md) | `/auth-implementation` | Implement authentication patterns |

</details>

### 📚 Documentation
<details>
<summary><b>📚 Documentation (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [readme](.archived/workflows/documentation/readme.md) | `/readme` | Generate comprehensive README |
| [api-docs](.archived/workflows/documentation/api-docs.md) | `/api-docs` | Generate API documentation (OpenAPI, JSDoc) |
| [architecture](.archived/workflows/documentation/architecture.md) | `/architecture` | Create architecture diagrams (Mermaid, C4) |

</details>

### 🚀 Deployment
<details>
<summary><b>🚀 Deployment (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [deploy](.archived/workflows/deployment/deploy.md) | `/deploy` | Deploy to any platform (detects or configures) |
| [docker](.archived/workflows/deployment/docker.md) | `/docker` | Containerize application |
| [ci-cd](.archived/workflows/deployment/ci-cd.md) | `/ci-cd` | Set up CI/CD pipelines |
| [railway-deploy](.archived/workflows/deployment/railway-deploy.md) | `/railway-deploy` | Deploy to Railway |
| [vercel-deploy](.archived/workflows/deployment/vercel-deploy.md) | `/vercel-deploy` | Deploy to Vercel |

</details>

### ⚙️ Configuration
<details>
<summary><b>⚙️ Configuration (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [env-config](.archived/workflows/configuration/env-config.md) | `/env-config` | Manage environment variables securely |

</details>

### 🗄️ Database
<details>
<summary><b>🗄️ Database (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [db-schema](.archived/workflows/database/db-schema.md) | `/db-schema` | Design database schemas (any ORM/DB) |
| [db-migrate](.archived/workflows/database/db-migrate.md) | `/db-migrate` | Create and run migrations |
| [db-seed](.archived/workflows/database/db-seed.md) | `/db-seed` | Generate seed/test data |

</details>

### 🤖 AI & LLM
<details>
<summary><b>🤖 AI & LLM (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [prompt-engineering](.archived/workflows/ai-llm/prompt-engineering.md) | `/prompt-engineering` | Design and optimize LLM prompts |
| [rag-pipeline](.archived/workflows/ai-llm/rag-pipeline.md) | `/rag-pipeline` | Build retrieval-augmented generation |
| [ai-agent](.archived/workflows/ai-llm/ai-agent.md) | `/ai-agent` | Create AI agents with tools |
| [workflow-creator](.archived/workflows/ai-llm/workflow-creator.md) | `/workflow-creator` | Create new antigravity workflows |

</details>

### 🎨 Creative & UI
<details>
<summary><b>🎨 Creative & UI (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [landing-page](.archived/workflows/creative-ui/landing-page.md) | `/landing-page` | Build landing pages (any stack) |
| [dashboard-ui](.archived/workflows/creative-ui/dashboard-ui.md) | `/dashboard-ui` | Create admin dashboards (any stack) |
| [design-system](.archived/workflows/creative-ui/design-system.md) | `/design-system` | Create and analyze design tokens |
| [email-template](.archived/workflows/creative-ui/email-template.md) | `/email-template` | Design responsive emails |

</details>

### ♿ Accessibility
<details>
<summary><b>♿ Accessibility (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [accessibility-audit](.archived/workflows/accessibility/accessibility-audit.md) | `/accessibility-audit` | Perform comprehensive accessibility audit |

</details>

### 🎯 Custom Workflows
<details>
<summary><b>🎯 Custom Workflows (Click to expand)</b></summary>

| Workflow | Slash Command | Description |
|---|---|---|
| [custom-feature-kickoff](.archived/workflows/miscellaneous/custom-feature-kickoff.md) | `/custom-feature-kickoff` | 🚀 Orchestration from Raw Idea -> SRS -> DB -> API -> Sequence -> Test Prep |
| [custom-generate-feature-spec](.archived/workflows/miscellaneous/custom-generate-feature-spec.md) | `/custom-generate-feature-spec` | 📋 Coordination to transform a raw idea into a standardized SRS |
| [custom-generate-db-schema](.archived/workflows/miscellaneous/custom-generate-db-schema.md) | `/custom-generate-db-schema` | 🗄️ Transforms SRS into a finalized database schema and ERD |
| [custom-generate-api-spec](.archived/workflows/miscellaneous/custom-generate-api-spec.md) | `/custom-generate-api-spec` | 🔌 Generates standardized API contracts based on the SRS and DB Schema |
| [custom-generate-sequence-diagram](.archived/workflows/miscellaneous/custom-generate-sequence-diagram.md) | `/custom-generate-sequence-diagram` | 🔀 Maps the interaction flow between users, system, and services |
| [git-commit-group-changes](.archived/workflows/miscellaneous/git-commit-group-changes.md) | `/git-commit-group-changes` | 📦 Automatically groups and commits changes by logical feature |
| [add-skill](.archived/workflows/miscellaneous/add-skill.md) | `/add-skill` | 📂 Automates adding and categorizing a new skill into the workspace |

</details>

## Adding New Workflows

Use the built-in workflow creator:

```
/workflow-creator
```

---

> **Source:** [github.com/harikrishna8121999/antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)
