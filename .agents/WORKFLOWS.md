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

| Workflow | Slash Command | Description |
|---|---|---|
| [new-project](../archieved_workflows/new-project.md) | `/new-project` | Scaffold any project (detects or asks for stack) |
| [new-component](../archieved_workflows/new-component.md) | `/new-component` | Create reusable UI components (any framework) |
| [new-api](../archieved_workflows/new-api.md) | `/new-api` | Create API endpoints (any backend) |
| [new-feature](../archieved_workflows/new-feature.md) | `/new-feature` | Full feature implementation from design to deployment |
| [refactor](../archieved_workflows/refactor.md) | `/refactor` | Improve code quality, extract, reduce duplication |
| [migrate](../archieved_workflows/migrate.md) | `/migrate` | Technology migrations (JS→TS, framework upgrades) |
| [cli-tool](../archieved_workflows/cli-tool.md) | `/cli-tool` | Build command-line applications |

### 🔀 Git & Collaboration

| Workflow | Slash Command | Description |
|---|---|---|
| [git-commit](../archieved_workflows/git-commit.md) | `/git-commit` | Generate conventional commits from staged changes |
| [git-pr](../archieved_workflows/git-pr.md) | `/git-pr` | Create comprehensive PR descriptions |
| [git-conflict](../archieved_workflows/git-conflict.md) | `/git-conflict` | Help resolve merge conflicts |
| [git-rebase](../archieved_workflows/git-rebase.md) | `/git-rebase` | Interactive rebase assistance |

### 🧪 Testing & Quality

| Workflow | Slash Command | Description |
|---|---|---|
| [unit-test](../archieved_workflows/unit-test.md) | `/unit-test` | Generate unit tests (detects testing framework) |
| [e2e-test](../archieved_workflows/e2e-test.md) | `/e2e-test` | End-to-end browser tests |
| [playwright-test](../archieved_workflows/playwright-test.md) | `/playwright-test` | Browser automation tests with Playwright |
| [test-coverage](../archieved_workflows/test-coverage.md) | `/test-coverage` | Improve test coverage for files |
| [code-review](../archieved_workflows/code-review.md) | `/code-review` | Comprehensive code review |

### 🐛 Debugging

| Workflow | Slash Command | Description |
|---|---|---|
| [debug-error](../archieved_workflows/debug-error.md) | `/debug-error` | Analyze errors and suggest fixes |
| [debug-log](../archieved_workflows/debug-log.md) | `/debug-log` | Add strategic logging/debugging |
| [performance](../archieved_workflows/performance.md) | `/performance` | Profile and optimize slow code |

### 🔒 Security

| Workflow | Slash Command | Description |
|---|---|---|
| [security-audit](../archieved_workflows/security-audit.md) | `/security-audit` | Scan for vulnerabilities and secrets |
| [dependency-check](../archieved_workflows/dependency-check.md) | `/dependency-check` | Check for vulnerable dependencies |
| [auth-implementation](../archieved_workflows/auth-implementation.md) | `/auth-implementation` | Implement authentication patterns |

### 📚 Documentation

| Workflow | Slash Command | Description |
|---|---|---|
| [readme](../archieved_workflows/readme.md) | `/readme` | Generate comprehensive README |
| [api-docs](../archieved_workflows/api-docs.md) | `/api-docs` | Generate API documentation (OpenAPI, JSDoc) |
| [architecture](../archieved_workflows/architecture.md) | `/architecture` | Create architecture diagrams (Mermaid, C4) |

### 🚀 Deployment

| Workflow | Slash Command | Description |
|---|---|---|
| [deploy](../archieved_workflows/deploy.md) | `/deploy` | Deploy to any platform (detects or configures) |
| [docker](../archieved_workflows/docker.md) | `/docker` | Containerize application |
| [ci-cd](../archieved_workflows/ci-cd.md) | `/ci-cd` | Set up CI/CD pipelines |
| [railway-deploy](../archieved_workflows/railway-deploy.md) | `/railway-deploy` | Deploy to Railway |
| [vercel-deploy](../archieved_workflows/vercel-deploy.md) | `/vercel-deploy` | Deploy to Vercel |

### ⚙️ Configuration

| Workflow | Slash Command | Description |
|---|---|---|
| [env-config](../archieved_workflows/env-config.md) | `/env-config` | Manage environment variables securely |

### 🗄️ Database

| Workflow | Slash Command | Description |
|---|---|---|
| [db-schema](../archieved_workflows/db-schema.md) | `/db-schema` | Design database schemas (any ORM/DB) |
| [db-migrate](../archieved_workflows/db-migrate.md) | `/db-migrate` | Create and run migrations |
| [db-seed](../archieved_workflows/db-seed.md) | `/db-seed` | Generate seed/test data |

### 🤖 AI & LLM

| Workflow | Slash Command | Description |
|---|---|---|
| [prompt-engineering](../archieved_workflows/prompt-engineering.md) | `/prompt-engineering` | Design and optimize LLM prompts |
| [rag-pipeline](../archieved_workflows/rag-pipeline.md) | `/rag-pipeline` | Build retrieval-augmented generation |
| [ai-agent](../archieved_workflows/ai-agent.md) | `/ai-agent` | Create AI agents with tools |
| [workflow-creator](../archieved_workflows/workflow-creator.md) | `/workflow-creator` | Create new antigravity workflows |

### 🎨 Creative & UI

| Workflow | Slash Command | Description |
|---|---|---|
| [landing-page](../archieved_workflows/landing-page.md) | `/landing-page` | Build landing pages (any stack) |
| [dashboard-ui](../archieved_workflows/dashboard-ui.md) | `/dashboard-ui` | Create admin dashboards (any stack) |
| [design-system](../archieved_workflows/design-system.md) | `/design-system` | Create and analyze design tokens |
| [email-template](../archieved_workflows/email-template.md) | `/email-template` | Design responsive emails |

### ♿ Accessibility

| Workflow | Slash Command | Description |
|---|---|---|
| [accessibility-audit](../archieved_workflows/accessibility-audit.md) | `/accessibility-audit` | Perform comprehensive accessibility audit |

---

## Adding New Workflows

Use the built-in workflow creator:

```
/workflow-creator
```

---

> **Source:** [github.com/harikrishna8121999/antigravity-workflows](https://github.com/harikrishna8121999/antigravity-workflows)
