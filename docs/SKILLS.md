# 🧠 Antigravity Skills

**330+ specialized AI skills to give your coding agent domain expertise — automatically.**

> Sourced from [antigravity-awesome-skills](https://github.com/anthropics/awesome-claude-code-skills)

---

## 🤔 What Are Skills?

Skills are specialized instruction sets that teach AI assistants how to handle specific tasks. Think of them as **expert knowledge modules** that your AI can load on-demand.

**Simple analogy:** Just like you might consult different experts (a designer, a security expert, a marketer), skills let your AI become an expert in different areas exactly when you need them.

| Efficiency | 📉 Minimal context is loaded first; details are only added as needed. |

---

## 🏗️ Modular Base Suites

To reduce context overhead, 212+ core skills are now grouped into **Base Suites**. These functional foundations form the heart of all role-based profiles.

| Suite | Description | Key Capabilities |
| :--- | :--- | :--- |
| **`base-core`** | ✨ Foundations | Planning, documentation, testing, and tool design. |
| **`base-ai`** | 🤖 Intelligence | RAG, agent orchestration, and LLM patterns. |
| **`base-dev`** | ⚙️ Engineering | API design, architecture, and framework expertise. |
| **`base-infra-ops`** | 📦 Operations | Docker, K8s, CI/CD, and cloud infrastructure. |
| **`base-security`** | 🛡️ Hardening | Security audits, JWT, and penetration testing. |
| **`base-product-cro`**| 📈 Growth | Payments, A/B testing, and SEO patterns. |

---

---

## 📂 Folder Structure

Each skill is organized for both human browsing and AI context:

```
../../../.archived/skills/
└── <category>/
    └── <skill-name>/
        ├── SKILL.md             # Main definition (the "brain")
        ├── scripts/             # Helper code (optional)
        ├── examples/            # How to use (optional)
        └── resources/           # Templates (optional)
```

---

## 🏗️ Skills by Category

### Ai Ml Agents

<details>
<summary><b>Ai Ml Agents (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [agents-md](../.archived/skills/ai-ml-agents/agents-md/SKILL.md) | A skill for creating concise, research-backed AGENTS.md documentation to maintain agent instructions and best practices. |
| [ai-engineer](../.archived/skills/ai-ml-agents/ai-engineer/SKILL.md) | Expert AI engineer specializing in production-grade LLM applications, generative AI systems, and intelligent agent architectures. |
| [ai-engineering-toolkit](../.archived/skills/ai-ml-agents/ai-engineering-toolkit/SKILL.md) | A collection of 6 structured, expert-level workflows that turn your AI coding assistant into a senior AI engineering partner. |
| [brainstorming](../.archived/skills/ai-ml-agents/brainstorming/SKILL.md) | A structured approach to transforming vague ideas into validated designs through disciplined reasoning and collaboration, ensuring that no creative implementation occurs while this skill is active. |
| [claude-code-guide](../.archived/skills/ai-ml-agents/claude-code-guide/SKILL.md) | A comprehensive guide for configuring and using Claude Code, an agentic coding tool, with best practices, configuration templates, and advanced usage patterns. |
| [claude-settings-audit](../.archived/skills/ai-ml-agents/claude-settings-audit/SKILL.md) | Analyze a repository to generate recommended Claude Code settings.json permissions. Detects tech stack, build tools, and monorepo structure. |
| [context7-auto-research](../.archived/skills/ai-ml-agents/context7-auto-research/SKILL.md) | Automatically fetch latest library/framework documentation for Claude Code via Context7 API. Use when you need up-to-date documentation for libraries and frameworks or asking about React, Next.js, Prisma, or any other popular library. |
| [devcontainer-setup](../.archived/skills/ai-ml-agents/devcontainer-setup/SKILL.md) | Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. |
| [diary](../.archived/skills/ai-ml-agents/diary/SKILL.md) | A context-preserving automated logger for multi-project development that summarizes progress, writes a daily dev log, and performs a daily review while keeping project contexts isolated and synced to Notion/Obsidian. |
| [embedding-strategies](../.archived/skills/ai-ml-agents/embedding-strategies/SKILL.md) | A guide to selecting and optimizing embedding models for vector search applications, including templates for OpenAI embeddings, local embeddings with Sentence Transformers, chunking strategies, domain-specific pipelines, and quality evaluation. |
| [filesystem-context](../.archived/skills/ai-ml-agents/filesystem-context/SKILL.md) | Use filesystem context management to offload large outputs, persist state, and dynamically load skills. |
| [langchain-architecture](../.archived/skills/ai-ml-agents/langchain-architecture/SKILL.md) | Master the LangChain framework for building sophisticated LLM applications with agents, chains, memory, and tool integration. |
| [langgraph](../.archived/skills/ai-ml-agents/langgraph/SKILL.md) | You are an expert in building production-grade AI agents with LangGraph by structuring them as graphs, making the flow visible and debuggable. |
| [last30days](../.archived/skills/ai-ml-agents/last30days/SKILL.md) | Research any topic from the last 30 days across Reddit, X, and the web, then synthesize copy-paste-ready prompts for the user's target tool. |
| [llm-ops](../.archived/skills/ai-ml-agents/llm-ops/SKILL.md) | LLM Operations -- RAG, embeddings, vector databases, fine-tuning, prompt engineering advanced, LLM costs, quality evals and AI architectures for production. |
| [mcp-builder](../.archived/skills/ai-ml-agents/mcp-builder/SKILL.md) | Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks. |
| [memory-systems](../.archived/skills/ai-ml-agents/memory-systems/SKILL.md) | Design short-term, long-term, and graph-based memory architectures to maintain entity consistency across conversations and enable reasoning over accumulated knowledge. |
| [moyu](../.archived/skills/ai-ml-agents/moyu/SKILL.md) | An AI coding agent skill that enforces restraint and avoids over-engineering by only making changes explicitly requested by the user. |
| [multi-agent-patterns](../.archived/skills/ai-ml-agents/multi-agent-patterns/SKILL.md) | This skill provides guidance on designing and implementing multi-agent systems, including patterns like supervisor/orchestrator, peer-to-peer/swarm, and hierarchical structures, with a focus on context isolation and effective coordination. |
| [notebooklm](../.archived/skills/ai-ml-agents/notebooklm/SKILL.md) | Interact with Google NotebookLM to query documentation using Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes. |
| [tool-design](../.archived/skills/ai-ml-agents/tool-design/SKILL.md) | Build tools that agents can use effectively, including architectural reduction patterns. |
| [workspace-configurator](../.archived/skills/ai-ml-agents/workspace-configurator/SKILL.md) | Invisible orchestrator that configures the active workspace context based on the user's natural language intent. |

</details>

### Ai Ml Evaluation

<details>
<summary><b>Ai Ml Evaluation (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [analyze-project](../.archived/skills/ai-ml-evaluation/analyze-project/SKILL.md) | Forensic root cause analyzer for Antigravity sessions that classifies scope deltas, rework patterns, root causes, hotspots, and auto-improves prompts/health. |
| [langfuse](../.archived/skills/ai-ml-evaluation/langfuse/SKILL.md) | An expert in LLM observability and evaluation, focusing on traces, spans, and metrics for monitoring LLM applications. |
| [llm-evaluation](../.archived/skills/ai-ml-evaluation/llm-evaluation/SKILL.md) | Master comprehensive evaluation strategies for LLM applications, from automated metrics to human evaluation and A/B testing. |

</details>

### Ai Ml Mcp

<details>
<summary><b>Ai Ml Mcp (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ai-native-cli](../.archived/skills/ai-ml-mcp/ai-native-cli/SKILL.md) | Design specification for building CLI tools that AI agents can safely use, covering structured JSON output, error handling, input contracts, safety guardrails, exit codes, and agent self-description. |
| [skill-check](../.archived/skills/ai-ml-mcp/skill-check/SKILL.md) | Validate SKILL.md files against the agentskills specification and Anthropic best practices, catching structural errors, semantic contradictions, naming anti-patterns, and quality gaps in a single read-only pass. |
| [skill-creator](../.archived/skills/ai-ml-mcp/skill-creator/SKILL.md) | Automates the creation of new CLI skills following Anthropic's best practices with zero manual configuration, including brainstorming, template application, validation, and installation processes. |
| [skill-improver](../.archived/skills/ai-ml-mcp/skill-improver/SKILL.md) | Iteratively improve a Claude Code skill using the skill-reviewer agent until it meets quality standards. |
| [skill-scanner](../.archived/skills/ai-ml-mcp/skill-scanner/SKILL.md) | Scan agent skills for security issues before adoption. Detects prompt injection, malicious code, excessive permissions, secret exposure, and supply chain risks. |
| [skill-seekers](../.archived/skills/ai-ml-mcp/skill-seekers/SKILL.md) | Automatically convert documentation websites, GitHub repositories, and PDFs into Claude AI skills in minutes. |
| [skill-writer](../.archived/skills/ai-ml-mcp/skill-writer/SKILL.md) | A comprehensive workflow for creating, improving and updating agent skills following the Agent Skills specification. |

</details>

### Ai Ml Memory

<details>
<summary><b>Ai Ml Memory (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [context-driven-development](../.archived/skills/ai-ml-memory/context-driven-development/SKILL.md) | Guide for implementing and maintaining context as a managed artifact alongside code, enabling consistent AI interactions and team alignment through structured project documentation. |
| [context-fundamentals](../.archived/skills/ai-ml-memory/context-fundamentals/SKILL.md) | Context engineering fundamentals, including system prompts, tool definitions, retrieved documents, message history, and tool outputs. |
| [context-manager](../.archived/skills/ai-ml-memory/context-manager/SKILL.md) | An elite AI context engineering specialist focused on dynamic context management, intelligent memory systems, and multi-agent workflow orchestration. |
| [context-optimization](../.archived/skills/ai-ml-memory/context-optimization/SKILL.md) | Context optimization extends the effective capacity of limited context windows through strategic compression, masking, caching, and partitioning. |
| [hierarchical-agent-memory](../.archived/skills/ai-ml-memory/hierarchical-agent-memory/SKILL.md) | Scoped CLAUDE.md memory system that reduces context token spend by creating directory-level context files, tracking savings via dashboard, and routing agents to the right sub-context. |
| [rag-engineer](../.archived/skills/ai-ml-memory/rag-engineer/SKILL.md) | RAG Engineer bridges the gap between raw documents and LLM understanding, focusing on retrieval quality to determine generation quality. |
| [recallmax](../.archived/skills/ai-ml-memory/recallmax/SKILL.md) | RecallMax enhances AI agent memory capabilities by injecting large amounts of clean context, auto-summarizing conversations while preserving tone and intent, and compressing multi-turn histories into high-density token sequences. |

</details>

### Ai Ml Prompting

<details>
<summary><b>Ai Ml Prompting (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [avoid-ai-writing](../.archived/skills/ai-ml-prompting/avoid-ai-writing/SKILL.md) | Detects and fixes AI writing patterns (AI-isms) that make text sound machine-generated, covering 21 pattern categories with a 43-entry word/phrase replacement table. |
| [explain-like-socrates](../.archived/skills/ai-ml-prompting/explain-like-socrates/SKILL.md) | Explains concepts using Socratic-style dialogue, guiding users toward understanding through reflective reasoning and analogies. |
| [llm-application-dev-prompt-optimize](../.archived/skills/ai-ml-prompting/llm-application-dev-prompt-optimize/SKILL.md) | Expert guidance in crafting effective prompts for LLMs through advanced techniques including constitutional AI, chain-of-thought reasoning, and model-specific optimization. |
| [prompt-engineer](../.archived/skills/ai-ml-prompting/prompt-engineer/SKILL.md) | Transforms raw user prompts into optimized prompts using established prompting frameworks. |

</details>

### Ai Ml Science

<details>
<summary><b>Ai Ml Science (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [astropy](../.archived/skills/ai-ml-science/astropy/SKILL.md) | Astropy is a Python package for astronomy, providing essential functionality for coordinate transformations, unit and quantity calculations, FITS file operations, cosmological calculations, precise time handling, tabular data manipulation, and astronomical image processing. |
| [deep-research](../.archived/skills/ai-ml-science/deep-research/SKILL.md) | Run autonomous research tasks that plan, search, read, and synthesize information into comprehensive reports. |
| [matplotlib](../.archived/skills/ai-ml-science/matplotlib/SKILL.md) | Matplotlib is Python's foundational visualization library for creating static, animated, and interactive plots. |
| [plotly](../.archived/skills/ai-ml-science/plotly/SKILL.md) | Plotly is a Python library for creating interactive, publication-quality visualizations with over 40 chart types. It supports various APIs like Plotly Express and Graph Objects, and offers extensive customization options. |
| [scanpy](../.archived/skills/ai-ml-science/scanpy/SKILL.md) | Scanpy is a scalable Python toolkit for analyzing single-cell RNA-seq data, built on AnnData. It supports complete workflows including quality control, normalization, dimensionality reduction, clustering, marker gene identification, visualization, and trajectory analysis. |
| [seaborn](../.archived/skills/ai-ml-science/seaborn/SKILL.md) | Seaborn is a Python library for creating publication-quality statistical graphics. It provides a high-level interface for drawing attractive and informative statistical graphics. |
| [sympy](../.archived/skills/ai-ml-science/sympy/SKILL.md) | SymPy is a Python library for symbolic mathematics that enables exact computation using mathematical symbols rather than numerical approximations. |
| [wiki-researcher](../.archived/skills/ai-ml-science/wiki-researcher/SKILL.md) | You are an expert software engineer and systems analyst. Use when user asks "how does X work" with expectation of depth, user wants to understand a complex system spanning many files, or user asks for architectural analysis or pattern investigation. |

</details>

### Automation Bots

<details>
<summary><b>Automation Bots (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [telegram-bot-builder](../.archived/skills/automation-bots/telegram-bot-builder/SKILL.md) | You build bots that feel like helpful assistants, understanding the Telegram ecosystem deeply and designing natural conversations. |

</details>

### Automation N8N

<details>
<summary><b>Automation N8N (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [n8n-code-javascript](../.archived/skills/automation-n8n/n8n-code-javascript/SKILL.md) | Expert guidance for writing JavaScript code in n8n Code nodes, covering best practices, essential rules, and common patterns. |
| [n8n-code-python](../.archived/skills/automation-n8n/n8n-code-python/SKILL.md) | Expert guidance for writing Python code in n8n Code nodes, including best practices, data access patterns, and return format requirements. |
| [n8n-expression-syntax](../.archived/skills/automation-n8n/n8n-expression-syntax/SKILL.md) | A guide for writing correct n8n expressions in workflows, covering syntax, variables, and common pitfalls. |
| [n8n-mcp-tools-expert](../.archived/skills/automation-n8n/n8n-mcp-tools-expert/SKILL.md) | Expert guide for using n8n-mcp MCP tools effectively, covering node discovery, configuration validation, and workflow management with detailed workflows, common patterns, and best practices. |
| [n8n-node-configuration](../.archived/skills/automation-n8n/n8n-node-configuration/SKILL.md) | This skill provides expert guidance for operation-aware node configuration in n8n, focusing on property dependencies and progressive disclosure. It covers common configuration patterns by node type and offers a step-by-step workflow to configure nodes effectively. |
| [n8n-validation-expert](../.archived/skills/automation-n8n/n8n-validation-expert/SKILL.md) | Expert guide for interpreting and fixing n8n validation errors, emphasizing iterative validation, error severity levels, common error types, and best practices. |
| [n8n-workflow-patterns](../.archived/skills/automation-n8n/n8n-workflow-patterns/SKILL.md) | Proven architectural patterns for building n8n workflows, covering common use cases such as webhook processing, HTTP API integration, database operations, AI agent workflows, and scheduled tasks. |

</details>

### Automation Scraping

<details>
<summary><b>Automation Scraping (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [daily-news-report](../.archived/skills/automation-scraping/daily-news-report/SKILL.md) | Scrapes content based on a preset URL list, filters high-quality technical information, and generates daily Markdown reports. |
| [x-twitter-scraper](../.archived/skills/automation-scraping/x-twitter-scraper/SKILL.md) | The X (Twitter) Scraper skill provides access to Twitter data through the Xquik platform, allowing users to search for tweets, look up user profiles, extract engagement metrics, and perform bulk extractions using REST API or MCP server. |

</details>

### Automation Workflows

<details>
<summary><b>Automation Workflows (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [billing-automation](../.archived/skills/automation-workflows/billing-automation/SKILL.md) | Master automated billing systems including recurring billing, invoice generation, dunning management, proration, and tax calculation. |

</details>

### Backend Api

<details>
<summary><b>Backend Api (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ad-creative](../.archived/skills/backend-api/ad-creative/SKILL.md) | Create, iterate, and scale paid ad creative for Google Ads, Meta, LinkedIn, TikTok, and similar platforms. Use when generating headlines, descriptions, primary text, or large sets of ad variations for testing and performance optimization. |
| [api-documentation-generator](../.archived/skills/backend-api/api-documentation-generator/SKILL.md) | Generate comprehensive, developer-friendly API documentation from code, including endpoints, parameters, examples, and best practices |
| [api-documenter](../.archived/skills/backend-api/api-documenter/SKILL.md) | Master API documentation with OpenAPI 3.1, AI-powered tools, and modern developer experience practices. Create interactive docs, generate SDKs, and build comprehensive developer portals. |
| [api-endpoint-builder](../.archived/skills/backend-api/api-endpoint-builder/SKILL.md) | Builds production-ready REST API endpoints with validation, error handling, authentication, and documentation. Follows best practices for security and scalability. |
| [api-patterns](../.archived/skills/backend-api/api-patterns/SKILL.md) | API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. |
| [fastapi-pro](../.archived/skills/backend-api/fastapi-pro/SKILL.md) | This skill provides comprehensive guidance on building high-performance, async APIs using FastAPI, SQLAlchemy 2.0, and Pydantic V2, covering best practices, architecture patterns, and advanced features. |
| [fastapi-router-py](../.archived/skills/backend-api/fastapi-router-py/SKILL.md) | Create FastAPI routers following established patterns with proper authentication, response models, and HTTP status codes. |
| [fastapi-templates](../.archived/skills/backend-api/fastapi-templates/SKILL.md) | Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects. |
| [gemini-api-integration](../.archived/skills/backend-api/gemini-api-integration/SKILL.md) | This skill provides a comprehensive guide for integrating the Google Gemini API into various applications, covering setup, text generation, streaming, multimodal inputs, function calling, model selection, and best practices. |
| [graphql](../.archived/skills/backend-api/graphql/SKILL.md) | A developer skilled in GraphQL API design and optimization, addressing common pitfalls like N+1 queries and deep nested queries. |
| [python-fastapi-development](../.archived/skills/backend-api/python-fastapi-development/SKILL.md) | A specialized workflow for building production-ready Python backends with FastAPI, featuring async patterns, SQLAlchemy ORM, Pydantic validation, and comprehensive API patterns. |
| [similarity-search-patterns](../.archived/skills/backend-api/similarity-search-patterns/SKILL.md) | Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance. |
| [trpc-fullstack](../.archived/skills/backend-api/trpc-fullstack/SKILL.md) | Build end-to-end type-safe APIs with tRPC, focusing on routers, procedures, middleware, subscriptions, and Next.js/React integration patterns. |

</details>

### Backend Arch

<details>
<summary><b>Backend Arch (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [architect-review](../.archived/skills/backend-arch/architect-review/SKILL.md) | A master software architect specializing in modern architecture patterns, clean architecture principles, and distributed systems design. |
| [auth-implementation-patterns](../.archived/skills/backend-arch/auth-implementation-patterns/SKILL.md) | Build secure, scalable authentication and authorization systems using industry-standard patterns and modern best practices. |
| [backend-architect](../.archived/skills/backend-arch/backend-architect/SKILL.md) | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. |
| [backend-dev-guidelines](../.archived/skills/backend-arch/backend-dev-guidelines/SKILL.md) | A comprehensive guide for senior backend engineers on writing production-grade, maintainable, and observable backend systems using Node.js, Express, TypeScript, and microservices architecture. |
| [binary-analysis-patterns](../.archived/skills/backend-arch/binary-analysis-patterns/SKILL.md) | Comprehensive patterns and techniques for analyzing compiled binaries, understanding assembly code, and reconstructing program logic. |
| [c4-architecture-c4-architecture](../.archived/skills/backend-arch/c4-architecture-c4-architecture/SKILL.md) | Generate comprehensive C4 architecture documentation for an existing repository/codebase using a bottom-up analysis approach. |
| [chrome-extension-developer](../.archived/skills/backend-arch/chrome-extension-developer/SKILL.md) | Expert in building Chrome Extensions using Manifest V3, focusing on modern architecture and production-ready security practices. |
| [codebase-cleanup-refactor-clean](../.archived/skills/backend-arch/codebase-cleanup-refactor-clean/SKILL.md) | A code refactoring skill that helps improve the quality, maintainability, and performance of large codebases by applying clean code principles and SOLID design patterns. |
| [docs-architect](../.archived/skills/backend-arch/docs-architect/SKILL.md) | Creates comprehensive technical documentation from existing codebases by analyzing architecture, design patterns, and implementation details. |
| [domain-driven-design](../.archived/skills/backend-arch/domain-driven-design/SKILL.md) | Plan and route Domain-Driven Design work from strategic modeling to tactical implementation and evented architecture patterns. |
| [error-detective](../.archived/skills/backend-arch/error-detective/SKILL.md) | Search logs and codebases for error patterns, stack traces, and anomalies. Correlates errors across systems and identifies root causes. |
| [event-store-design](../.archived/skills/backend-arch/event-store-design/SKILL.md) | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns. |
| [framework-migration-code-migrate](../.archived/skills/backend-arch/framework-migration-code-migrate/SKILL.md) | A code migration expert specializing in transitioning codebases between frameworks, languages, versions, and platforms. Generates comprehensive migration plans, automated scripts, and ensures smooth transitions with minimal disruption. |
| [framework-migration-legacy-modernize](../.archived/skills/backend-arch/framework-migration-legacy-modernize/SKILL.md) | Orchestrate a comprehensive legacy system modernization using the strangler fig pattern, enabling gradual replacement of outdated components while maintaining continuous business operations through expert agent coordination. |
| [full-stack-orchestration-full-stack-feature](../.archived/skills/backend-arch/full-stack-orchestration-full-stack-feature/SKILL.md) | A comprehensive workflow for orchestrating full-stack feature development using an API-first approach, covering architecture design, implementation, testing, security, deployment, and observability. |
| [graphql-architect](../.archived/skills/backend-arch/graphql-architect/SKILL.md) | Master modern GraphQL with federation, performance optimization, and enterprise security. Build scalable schemas, implement advanced caching, and design real-time systems. |
| [legacy-modernizer](../.archived/skills/backend-arch/legacy-modernizer/SKILL.md) | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, dependency updates, and backward compatibility. |
| [memory-safety-patterns](../.archived/skills/backend-arch/memory-safety-patterns/SKILL.md) | Cross-language patterns for memory-safe programming including RAII, ownership, smart pointers, and resource management. |
| [microservices-patterns](../.archived/skills/backend-arch/microservices-patterns/SKILL.md) | Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems. |
| [network-engineer](../.archived/skills/backend-arch/network-engineer/SKILL.md) | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization. |
| [performance-engineer](../.archived/skills/backend-arch/performance-engineer/SKILL.md) | Expert performance engineer specializing in modern observability, application profiling, and system optimization. |
| [projection-patterns](../.archived/skills/backend-arch/projection-patterns/SKILL.md) | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems. |
| [risk-metrics-calculation](../.archived/skills/backend-arch/risk-metrics-calculation/SKILL.md) | Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implementing risk limits, or building risk monitoring systems. |
| [rust-async-patterns](../.archived/skills/backend-arch/rust-async-patterns/SKILL.md) | Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust applications, implementing concurrent systems, or debugging async code. |
| [senior-architect](../.archived/skills/backend-arch/senior-architect/SKILL.md) | A comprehensive toolkit for senior architects, providing automated scripts and best practices for architecture diagram generation, project analysis, and dependency management. |
| [senior-architect-v2](../.archived/skills/backend-arch/senior-architect-v2/SKILL.md) | Expert system architect specializing in visualizing complex system interactions and translating business logic into technical workflows. |
| [senior-fullstack](../.archived/skills/backend-arch/senior-fullstack/SKILL.md) | A comprehensive toolkit for senior fullstack development with modern tools and best practices, including automated scripts for fullstack scaffolding, project analysis, and code quality checks. |
| [software-architecture](../.archived/skills/backend-arch/software-architecture/SKILL.md) | Guide for quality-focused software architecture, providing principles and best practices for clean code and domain-driven design. |

</details>

### Backend Core

<details>
<summary><b>Backend Core (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [backend-development-feature-development](../.archived/skills/backend-core/backend-development-feature-development/SKILL.md) | Orchestrate end-to-end backend feature development from requirements to deployment, supporting multiple methodologies and complex scenarios. |
| [biopython](../.archived/skills/backend-core/biopython/SKILL.md) | Biopython is a comprehensive set of Python tools for biological computation, supporting sequence manipulation, database access, BLAST operations, structural bioinformatics, and more. |
| [code-review-checklist](../.archived/skills/backend-core/code-review-checklist/SKILL.md) | Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability. |
| [database-migration](../.archived/skills/backend-core/database-migration/SKILL.md) | Master database schema and data migrations across ORMs (Sequelize, TypeORM, Prisma), including rollback strategies and zero-downtime deployments. |
| [database-optimizer](../.archived/skills/backend-core/database-optimizer/SKILL.md) | Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures. |
| [fp-backend](../.archived/skills/backend-core/fp-backend/SKILL.md) | A collection of functional programming patterns for Node.js/Deno backend development using fp-ts, ReaderTaskEither, and functional dependency injection. |
| [fp-data-transforms](../.archived/skills/backend-core/fp-data-transforms/SKILL.md) | This skill covers practical data transformations using functional programming patterns in TypeScript, including array operations, object transformations, data normalization, grouping and aggregation, and null-safe access. |
| [go-concurrency-patterns](../.archived/skills/backend-core/go-concurrency-patterns/SKILL.md) | Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions. |
| [golang-pro](../.archived/skills/backend-core/golang-pro/SKILL.md) | Master Go 1.21+ development with advanced concurrency, performance optimization, and production-ready microservices. |
| [grpc-golang](../.archived/skills/backend-core/grpc-golang/SKILL.md) | A comprehensive guide for designing and implementing production-grade gRPC services in Go, covering contract standardization with Buf, transport layer security via mTLS, and deep observability with OpenTelemetry interceptors. |
| [java-pro](../.archived/skills/backend-core/java-pro/SKILL.md) | Master Java 21+ with modern features like virtual threads, pattern matching, and Spring Boot 3.x. Expert in the latest Java ecosystem including GraalVM, Project Loom, and cloud-native patterns. |
| [nextjs-best-practices](../.archived/skills/backend-core/nextjs-best-practices/SKILL.md) | Next.js App Router principles including server components, data fetching, routing patterns, API routes, performance optimization, metadata, caching strategy, and server actions. |
| [postgres-best-practices](../.archived/skills/backend-core/postgres-best-practices/SKILL.md) | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations. |
| [python-development-python-scaffold](../.archived/skills/backend-core/python-development-python-scaffold/SKILL.md) | A skill for generating complete production-ready Python project structures using modern tools like uv, FastAPI, Django, and type hints. |
| [python-packaging](../.archived/skills/backend-core/python-packaging/SKILL.md) | Comprehensive guide to creating, structuring, and distributing Python packages using modern packaging tools, pyproject.toml, and publishing to PyPI. |
| [python-patterns](../.archived/skills/backend-core/python-patterns/SKILL.md) | Teaches Python development principles and decision-making, including framework selection, async patterns, type hints, and project structure. |
| [python-performance-optimization](../.archived/skills/backend-core/python-performance-optimization/SKILL.md) | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance. |
| [python-pro](../.archived/skills/backend-core/python-pro/SKILL.md) | Master Python 3.12+ development with advanced features, async programming, performance optimization, and production-ready practices using cutting-edge tools like uv, ruff, pydantic, and FastAPI. |
| [receiving-code-review](../.archived/skills/backend-core/receiving-code-review/SKILL.md) | A structured approach for receiving and responding to code review feedback, emphasizing technical evaluation over emotional reactions. |
| [rust-pro](../.archived/skills/backend-core/rust-pro/SKILL.md) | Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems programming. |
| [seo-audit](../.archived/skills/backend-core/seo-audit/SKILL.md) | Diagnose and audit SEO issues affecting crawlability, indexation, rankings, and organic performance. |
| [systems-programming-rust-project](../.archived/skills/backend-core/systems-programming-rust-project/SKILL.md) | This skill provides guidance for scaffolding production-ready Rust applications using Cargo tooling, proper module organization, testing, and configuration following Rust best practices. |
| [temporal-golang-pro](../.archived/skills/backend-core/temporal-golang-pro/SKILL.md) | Expert-level guide for building resilient, scalable, and deterministic distributed systems using the Temporal Go SDK. Covers durable execution, strict determinism, and enterprise-scale worker configuration. |
| [typescript-expert](../.archived/skills/backend-core/typescript-expert/SKILL.md) | A TypeScript and JavaScript expert with deep knowledge of type-level programming, performance optimization, monorepo management, migration strategies, and modern tooling. |
| [typescript-pro](../.archived/skills/backend-core/typescript-pro/SKILL.md) | Master TypeScript with advanced types, generics, and strict type safety. Handles complex type systems, decorators, and enterprise-grade patterns. |

</details>

### Business Content

<details>
<summary><b>Business Content (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [competitor-alternatives](../.archived/skills/business-content/competitor-alternatives/SKILL.md) | Create effective competitor comparison and alternative pages that rank for competitive search terms, provide genuine value to evaluators, and position your product effectively. |
| [copy-editing](../.archived/skills/business-content/copy-editing/SKILL.md) | You are an expert copy editor specializing in marketing and conversion copy. Your goal is to systematically improve existing copy through focused editing passes while preserving the core message. |
| [copywriting](../.archived/skills/business-content/copywriting/SKILL.md) | Write rigorous, conversion-focused marketing copy for landing pages and emails. Enforces brief confirmation and strict no-fabrication rules. |
| [marketing-ideas](../.archived/skills/business-content/marketing-ideas/SKILL.md) | A skill that provides proven marketing strategies and growth ideas for SaaS and software products, prioritized using a marketing feasibility scoring system. |
| [marketing-psychology](../.archived/skills/business-content/marketing-psychology/SKILL.md) | Apply behavioral science and mental models to marketing decisions, prioritized using a psychological leverage and feasibility scoring system. |
| [product-marketing-context](../.archived/skills/business-content/product-marketing-context/SKILL.md) | Create or update a reusable product marketing context document with positioning, audience, ICP, use cases, and messaging. Use at the start of a project to avoid repeating core marketing context across tasks. |

</details>

### Business Health

<details>
<summary><b>Business Health (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [goal-analyzer](../.archived/skills/business-health/goal-analyzer/SKILL.md) | A skill that analyzes health goal data, identifies patterns and progress, evaluates goal achievement, and provides personalized goal management advice. |
| [health-trend-analyzer](../.archived/skills/business-health/health-trend-analyzer/SKILL.md) | A tool to analyze health data trends and patterns over a period of time, identifying changes, correlations, and providing data-driven insights into health. |

</details>

### Business Product

<details>
<summary><b>Business Product (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [analytics-product](../.archived/skills/business-product/analytics-product/SKILL.md) | A skill that provides specialized assistance with analytics product, including PostHog, Mixpanel, events, funnels, cohorts, retention, north star metric, OKRs and product dashboards. |
| [market-sizing-analysis](../.archived/skills/business-product/market-sizing-analysis/SKILL.md) | Comprehensive market sizing methodologies for calculating Total Addressable Market (TAM), Serviceable Available Market (SAM), and Serviceable Obtainable Market (SOM) for startup opportunities. |
| [product-manager-toolkit](../.archived/skills/business-product/product-manager-toolkit/SKILL.md) | A comprehensive product management toolkit with essential tools and frameworks for discovery, prioritization, PRD creation, and execution. |
| [senior-product-manager](../.archived/skills/business-product/senior-product-manager/SKILL.md) | Act as a senior product manager for active software projects, providing decision-oriented product reviews grounded in current project artifacts and focusing on what to build next, why it matters, and what to defer. |

</details>

### Business Seo

<details>
<summary><b>Business Seo (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [keyword-extractor](../.archived/skills/business-seo/keyword-extractor/SKILL.md) | Extracts up to 50 SEO-friendly, relevant keywords from text for use in keyword generation or extraction requests. |
| [seo](../.archived/skills/business-seo/seo/SKILL.md) | Comprehensive SEO analysis across all industries, orchestrating 12 specialized sub-skills and 7 subagents for technical SEO, content quality, schema, sitemaps, AI search readiness, and GEO. |
| [seo-cannibalization-detector](../.archived/skills/business-seo/seo-cannibalization-detector/SKILL.md) | Analyzes multiple provided pages to identify keyword overlap and potential cannibalization issues, suggesting differentiation strategies. |
| [seo-competitor-pages](../.archived/skills/business-seo/seo-competitor-pages/SKILL.md) | Generate SEO-optimized competitor comparison and alternatives pages with 'X vs Y' layouts, schema markup, and conversion optimization. |
| [seo-content-planner](../.archived/skills/business-seo/seo-content-planner/SKILL.md) | Creates comprehensive content outlines and topic clusters for SEO, plans content calendars, and identifies topic gaps. |
| [seo-content-refresher](../.archived/skills/business-seo/seo-content-refresher/SKILL.md) | Identifies outdated elements in provided content and suggests updates to maintain freshness. |
| [seo-content-writer](../.archived/skills/business-seo/seo-content-writer/SKILL.md) | Writes SEO-optimized content based on provided keywords and topic briefs, creating engaging, comprehensive content following best practices. |
| [seo-image-gen](../.archived/skills/business-seo/seo-image-gen/SKILL.md) | Generate SEO-focused images such as OG cards, hero images, schema assets, product visuals, and infographics using Gemini's image generation via the banana Creative Director pipeline. |
| [seo-images](../.archived/skills/business-seo/seo-images/SKILL.md) | Image optimization analysis for SEO and performance, checking alt text, file sizes, formats, responsive images, lazy loading, and CLS prevention. |
| [seo-keyword-strategist](../.archived/skills/business-seo/seo-keyword-strategist/SKILL.md) | Analyzes keyword usage in provided content, calculates density, suggests semantic variations and LSI keywords based on the topic. Prevents over-optimization. |
| [seo-meta-optimizer](../.archived/skills/business-seo/seo-meta-optimizer/SKILL.md) | Creates optimized meta titles, descriptions, and URL suggestions based on character limits and best practices. |
| [seo-sitemap](../.archived/skills/business-seo/seo-sitemap/SKILL.md) | Analyze existing XML sitemaps or generate new ones using industry templates, validating format, URLs, and structure. |
| [seo-structure-architect](../.archived/skills/business-seo/seo-structure-architect/SKILL.md) | Analyzes and optimizes content structure including header hierarchy, suggests schema markup, and internal linking opportunities. |

</details>

### Data Admin

<details>
<summary><b>Data Admin (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [vector-database-engineer](../.archived/skills/data-admin/vector-database-engineer/SKILL.md) | Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similarity search. |

</details>

### Data Nosql

<details>
<summary><b>Data Nosql (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [nosql-expert](../.archived/skills/data-nosql/nosql-expert/SKILL.md) | Expert guidance for designing distributed NoSQL databases like Cassandra and DynamoDB, focusing on query-first modeling, single-table design, and avoiding hot partitions. |

</details>

### Data Orm

<details>
<summary><b>Data Orm (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [database-architect](../.archived/skills/data-orm/database-architect/SKILL.md) | Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and scalable database architectures. |
| [database-design](../.archived/skills/data-orm/database-design/SKILL.md) | Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases. |
| [linear](../.archived/skills/data-orm/linear/SKILL.md) | Managing Linear issues, projects, and teams for issue tracking, status updates, querying projects, and managing team workflows. |
| [videodb](../.archived/skills/data-orm/videodb/SKILL.md) | Video and audio perception, indexing, and editing. Ingest files/URLs/live streams, build visual/spoken indexes, search with timestamps, edit timelines, add overlays/subtitles, generate media, and create real-time alerts. |

</details>

### Data Pipelines

<details>
<summary><b>Data Pipelines (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [data-engineer](../.archived/skills/data-pipelines/data-engineer/SKILL.md) | A comprehensive skill for building scalable data pipelines, modern data warehouses, and real-time streaming architectures using tools like Apache Spark, dbt, Airflow, and cloud-native platforms. |
| [data-engineering-data-pipeline](../.archived/skills/data-pipelines/data-engineering-data-pipeline/SKILL.md) | A comprehensive guide for designing, implementing, and optimizing scalable data pipelines using various tools and technologies. |
| [database](../.archived/skills/data-pipelines/database/SKILL.md) | A comprehensive database workflow bundle covering SQL, NoSQL, database design, migrations, optimization, and data engineering. |

</details>

### Data Sql

<details>
<summary><b>Data Sql (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [database-migrations-sql-migrations](../.archived/skills/data-sql/database-migrations-sql-migrations/SKILL.md) | SQL database migrations with zero-downtime strategies for PostgreSQL, MySQL, and SQL Server. Focus on data integrity and rollback plans. |
| [food-database-query](../.archived/skills/data-sql/food-database-query/SKILL.md) | Food Database Query provides comprehensive nutritional information for various foods, including querying, comparing, recommending, and calculating auto-nutrition. |
| [postgresql](../.archived/skills/data-sql/postgresql/SKILL.md) | A comprehensive guide to designing PostgreSQL schemas, covering data types, indexing, constraints, performance patterns, and advanced features. |
| [postgresql-optimization](../.archived/skills/data-sql/postgresql-optimization/SKILL.md) | A specialized workflow for optimizing PostgreSQL databases, covering query tuning, indexing strategies, performance analysis, and production management. |
| [sql-optimization-patterns](../.archived/skills/data-sql/sql-optimization-patterns/SKILL.md) | Transform slow database queries into lightning-fast operations through systematic optimization, proper indexing, and query plan analysis. |
| [sql-pro](../.archived/skills/data-sql/sql-pro/SKILL.md) | Master modern SQL with cloud-native databases, OLTP/OLAP optimization, and advanced query techniques. Expert in performance tuning, data modeling, and hybrid analytical systems. |

</details>

### Design Apple Hig

<details>
<summary><b>Design Apple Hig (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [hig-components-controls](../.archived/skills/design-apple-hig/hig-components-controls/SKILL.md) | A guide on Apple Human Interface Guidelines (HIG) for selection and input controls, providing recommendations and best practices. |
| [hig-components-menus](../.archived/skills/design-apple-hig/hig-components-menus/SKILL.md) | Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered. |
| [hig-inputs](../.archived/skills/design-apple-hig/hig-inputs/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-technologies](../.archived/skills/design-apple-hig/hig-technologies/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |

</details>

### Design Core

<details>
<summary><b>Design Core (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [canvas-design](../.archived/skills/design-core/canvas-design/SKILL.md) | These instructions guide the creation of design philosophies and their visual expression, emphasizing minimal text and expert craftsmanship. |

</details>

### Design Ux Ui

<details>
<summary><b>Design Ux Ui (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [c4-component](../.archived/skills/design-ux-ui/c4-component/SKILL.md) | Expert C4 Component-level documentation specialist. Synthesizes C4 Code-level documentation into Component-level architecture, defining component boundaries, interfaces, and relationships. |
| [interactive-portfolio](../.archived/skills/design-ux-ui/interactive-portfolio/SKILL.md) | A comprehensive guide on designing and optimizing interactive portfolios for maximum impact, focusing on structure, project showcase, and personal branding. |
| [json-canvas](../.archived/skills/design-ux-ui/json-canvas/SKILL.md) | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections for mind maps, flowcharts, or visual note structures in Obsidian. |
| [ui-ux-designer](../.archived/skills/design-ux-ui/ui-ux-designer/SKILL.md) | Create interface designs, wireframes, and design systems. Masters user research, accessibility standards, and modern design tools. |
| [ui-visual-validator](../.archived/skills/design-ux-ui/ui-visual-validator/SKILL.md) | Rigorous visual validation expert specializing in UI testing, design system compliance, and accessibility verification. |

</details>

### Design Visuals

<details>
<summary><b>Design Visuals (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [favicon](../.archived/skills/design-visuals/favicon/SKILL.md) | Generate a complete set of favicons from the source image at `$1` and update the project's HTML with the appropriate link tags. |
| [iconsax-library](../.archived/skills/design-visuals/iconsax-library/SKILL.md) | Extensive icon library and AI-driven icon generation skill for premium UI/UX design. |
| [imagen](../.archived/skills/design-visuals/imagen/SKILL.md) | AI image generation skill powered by Google Gemini that enables seamless visual content creation for UI placeholders, documentation, and design assets. |
| [magic-animator](../.archived/skills/design-visuals/magic-animator/SKILL.md) | AI-powered animation tool for creating motion in logos, UI, icons, and social media assets. |

</details>

### Devops Cicd

<details>
<summary><b>Devops Cicd (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [deployment-engineer](../.archived/skills/devops-cicd/deployment-engineer/SKILL.md) | Expert in modern CI/CD practices, GitOps workflows, and container orchestration, specializing in zero-downtime deployments, progressive delivery, and enterprise-scale automation. |
| [deployment-pipeline-design](../.archived/skills/devops-cicd/deployment-pipeline-design/SKILL.md) | Architecture patterns for multi-stage CI/CD pipelines with approval gates and deployment strategies. |
| [environment-setup-guide](../.archived/skills/devops-cicd/environment-setup-guide/SKILL.md) | Guide developers through setting up development environments with proper tools, dependencies, and configurations |
| [git-advanced-workflows](../.archived/skills/devops-cicd/git-advanced-workflows/SKILL.md) | Master advanced Git techniques to maintain clean history, collaborate effectively, and recover from any situation with confidence. |
| [github-actions-templates](../.archived/skills/devops-cicd/github-actions-templates/SKILL.md) | Production-ready GitHub Actions workflow patterns for testing, building, and deploying applications. |

</details>

### Devops Cli

<details>
<summary><b>Devops Cli (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [claude-code-expert](../.archived/skills/devops-cli/claude-code-expert/SKILL.md) | A deep expert in Anthropic's Claude Code CLI, maximizing productivity with shortcuts, hooks, MCPs, advanced configurations, workflows, CLAUDE.md, memory, sub-agents, permissions and ecosystem integration. |
| [file-organizer](../.archived/skills/devops-cli/file-organizer/SKILL.md) | A skill for organizing files and folders by analyzing current structure, finding duplicates, suggesting organization plans, and executing the cleanup with user approval. |
| [personal-tool-builder](../.archived/skills/devops-cli/personal-tool-builder/SKILL.md) | Personal Tool Architect who builds fast, iterates constantly, and only polishes what proves useful, focusing on personal productivity tools, scratch-your-own-itch methodology, rapid prototyping for personal use, CLI tool development, local-first applications, script-to-product evolution, dogfooding practices, and personal automation. |

</details>

### Devops Cloud

<details>
<summary><b>Devops Cloud (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [cloud-architect](../.archived/skills/devops-cloud/cloud-architect/SKILL.md) | Expert cloud architect specializing in AWS, Azure, GCP multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns. |
| [cloud-devops](../.archived/skills/devops-cloud/cloud-devops/SKILL.md) | A comprehensive cloud and DevOps workflow bundle covering infrastructure provisioning, container orchestration, CI/CD pipelines, monitoring, and cloud-native application development. |
| [database-cloud-optimization-cost-optimize](../.archived/skills/devops-cloud/database-cloud-optimization-cost-optimize/SKILL.md) | A cloud cost optimization expert specializing in reducing infrastructure expenses while maintaining performance and reliability. Analyzes cloud spending, identifies savings opportunities, and implements cost-effective architectures across AWS, Azure, and GCP. |

</details>

### Devops Containers

<details>
<summary><b>Devops Containers (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [docker-expert](../.archived/skills/devops-containers/docker-expert/SKILL.md) | You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns, and production deployment strategies based on current industry best practices. |
| [kubernetes-architect](../.archived/skills/devops-containers/kubernetes-architect/SKILL.md) | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration. |
| [kubernetes-deployment](../.archived/skills/devops-containers/kubernetes-deployment/SKILL.md) | A specialized workflow for deploying applications to Kubernetes, including container orchestration, Helm charts, service mesh configuration, and production-ready K8s patterns. |

</details>

### Devops Iac

<details>
<summary><b>Devops Iac (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [deployment-procedures](../.archived/skills/devops-iac/deployment-procedures/SKILL.md) | A comprehensive guide on safe production deployments, including decision-making principles, workflows, and rollback strategies. |
| [deployment-validation-config-validate](../.archived/skills/devops-iac/deployment-validation-config-validate/SKILL.md) | This skill provides comprehensive tools for validating, testing, and securing application configurations across different environments. |
| [gitops-workflow](../.archived/skills/devops-iac/gitops-workflow/SKILL.md) | A comprehensive guide to implementing GitOps workflows with ArgoCD and Flux for automated Kubernetes deployments. |
| [helm-chart-scaffolding](../.archived/skills/devops-iac/helm-chart-scaffolding/SKILL.md) | Comprehensive guidance for creating, organizing, and managing Helm charts for packaging and deploying Kubernetes applications. |
| [k8s-manifest-generator](../.archived/skills/devops-iac/k8s-manifest-generator/SKILL.md) | Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims. |
| [k8s-security-policies](../.archived/skills/devops-iac/k8s-security-policies/SKILL.md) | Comprehensive guide for implementing NetworkPolicy, PodSecurityPolicy, RBAC, and Pod Security Standards in Kubernetes. |
| [sred-project-organizer](../.archived/skills/devops-iac/sred-project-organizer/SKILL.md) | A skill to organize projects and their related documentation into the SRED format for submission, using Notion and Linear. |
| [sred-work-summary](../.archived/skills/devops-iac/sred-work-summary/SKILL.md) | A skill to collect and organize work-related links from Github PRs, Notion docs, and Linear tickets into a private Notion document. |
| [terraform-aws-modules](../.archived/skills/devops-iac/terraform-aws-modules/SKILL.md) | Terraform module creation for AWS — reusable modules, state management, and HCL best practices. Use when building or reviewing Terraform AWS infrastructure. |
| [terraform-module-library](../.archived/skills/devops-iac/terraform-module-library/SKILL.md) | A library of production-ready Terraform modules for AWS, Azure, and GCP infrastructure. |
| [terraform-skill](../.archived/skills/devops-iac/terraform-skill/SKILL.md) | Terraform infrastructure as code best practices, covering testing, modules, CI/CD, and production patterns. |
| [terraform-specialist](../.archived/skills/devops-iac/terraform-specialist/SKILL.md) | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructure patterns. |

</details>

### Devops Os Scripting

<details>
<summary><b>Devops Os Scripting (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [bash-defensive-patterns](../.archived/skills/devops-os-scripting/bash-defensive-patterns/SKILL.md) | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety. |
| [bash-linux](../.archived/skills/devops-os-scripting/bash-linux/SKILL.md) | Bash/Linux terminal patterns including essential commands, piping, error handling, scripting. Useful for macOS and Linux systems. |
| [bash-pro](../.archived/skills/devops-os-scripting/bash-pro/SKILL.md) | Master defensive Bash scripting for production automation, CI/CD pipelines, and system utilities with expert knowledge in safe, portable, and testable shell scripts. |
| [bash-scripting](../.archived/skills/devops-os-scripting/bash-scripting/SKILL.md) | Bash scripting workflow for creating production-ready shell scripts with defensive patterns, error handling, and testing. |
| [linux-troubleshooting](../.archived/skills/devops-os-scripting/linux-troubleshooting/SKILL.md) | A detailed workflow for diagnosing and resolving Linux system issues, including performance problems, service failures, network issues, and resource constraints. |
| [powershell-windows](../.archived/skills/devops-os-scripting/powershell-windows/SKILL.md) | PowerShell Windows patterns focusing on critical pitfalls, operator syntax, error handling, and best practices. |
| [windows-shell-reliability](../.archived/skills/devops-os-scripting/windows-shell-reliability/SKILL.md) | This skill provides best practices for running commands reliably on Windows via PowerShell and CMD, focusing on paths, encoding, and common binary pitfalls. |

</details>

### Devops Quality

<details>
<summary><b>Devops Quality (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [devops-troubleshooter](../.archived/skills/devops-quality/devops-troubleshooter/SKILL.md) | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. |

</details>

### Documentation Planning

<details>
<summary><b>Documentation Planning (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [concise-planning](../.archived/skills/documentation-planning/concise-planning/SKILL.md) | Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist. |
| [github-issue-creator](../.archived/skills/documentation-planning/github-issue-creator/SKILL.md) | Transform messy input (error logs, voice notes, screenshots) into clean, actionable GitHub issues. |
| [plan-writing](../.archived/skills/documentation-planning/plan-writing/SKILL.md) | Structured task planning with clear breakdowns, dependencies, and verification criteria for implementing features, refactoring, or any multi-step work. |

</details>

### Documentation Writing

<details>
<summary><b>Documentation Writing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [api-documentation](../.archived/skills/documentation-writing/api-documentation/SKILL.md) | Specialized workflow for creating comprehensive API documentation including OpenAPI/Swagger specs, developer guides, code examples, and interactive documentation. |
| [c4-code](../.archived/skills/documentation-writing/c4-code/SKILL.md) | Expert C4 Code-level documentation specialist. Analyzes code directories to create comprehensive C4 code-level documentation including function signatures, arguments, dependencies, and code structure. |
| [c4-context](../.archived/skills/documentation-writing/c4-context/SKILL.md) | Expert C4 Context-level documentation specialist. Creates high-level system context diagrams, documents personas, user journeys, system features, and external dependencies. |
| [debrief-teacher](../.archived/skills/documentation-writing/debrief-teacher/SKILL.md) | Generates detailed conversational post-mortem breakdowns of completed tasks to accelerate learning and reveal the underlying decision-making process. |
| [exhaustive-video-note-taker](../.archived/skills/documentation-writing/exhaustive-video-note-taker/SKILL.md) | A skill that generates detailed, chronological, and time-stamped notes from video content or transcripts, capturing all technical concepts, examples, visuals, and synthesizing them into a structured format. |
| [wiki-architect](../.archived/skills/documentation-writing/wiki-architect/SKILL.md) | A documentation architect that produces structured wiki catalogues and onboarding guides from codebases. |
| [wiki-changelog](../.archived/skills/documentation-writing/wiki-changelog/SKILL.md) | Generate structured changelogs from git history for users asking about recent changes, changelog summaries, or wanting to understand development activity. |
| [wiki-onboarding](../.archived/skills/documentation-writing/wiki-onboarding/SKILL.md) | Generate two complementary onboarding documents that together give any engineer — from newcomer to principal — a complete understanding of a codebase. |
| [wiki-page-writer](../.archived/skills/documentation-writing/wiki-page-writer/SKILL.md) | Generates comprehensive technical documentation pages with evidence-based depth, following a structured procedure and mandatory requirements. |

</details>

### Frontend 3D Anim

<details>
<summary><b>Frontend 3D Anim (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [3d-web-experience](../.archived/skills/frontend-3d-anim/3d-web-experience/SKILL.md) | The 3D Web Experience skill focuses on bringing the third dimension to web applications, balancing visual impact with performance, and ensuring accessibility for users. It includes capabilities like Three.js implementation, React Three Fiber, WebGL optimization, and interactive 3D scenes. |
| [fixing-motion-performance](../.archived/skills/frontend-3d-anim/fixing-motion-performance/SKILL.md) | Audit and fix animation performance issues including layout thrashing, compositor properties, scroll-linked motion, and blur effects. Use when animations stutter, transitions jank, or reviewing CSS/JS animation performance. |

</details>

### Frontend Core

<details>
<summary><b>Frontend Core (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ab-test-setup](../.archived/skills/frontend-core/ab-test-setup/SKILL.md) | A structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness. |
| [browser-extension-builder](../.archived/skills/frontend-core/browser-extension-builder/SKILL.md) | The Browser Extension Builder skill provides knowledge and guidance on developing browser extensions, including architecture, manifest v3, content scripts, background workers, popup interfaces, monetization, and publishing. |
| [i18n-localization](../.archived/skills/frontend-core/i18n-localization/SKILL.md) | Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. |
| [javascript-pro](../.archived/skills/frontend-core/javascript-pro/SKILL.md) | Master modern JavaScript with ES6+, async patterns, and Node.js APIs. Handles promises, event loops, and browser/Node compatibility. |
| [javascript-testing-patterns](../.archived/skills/frontend-core/javascript-testing-patterns/SKILL.md) | Comprehensive guide for implementing robust testing strategies in JavaScript/TypeScript applications using modern testing frameworks and best practices. |
| [nodejs-best-practices](../.archived/skills/frontend-core/nodejs-best-practices/SKILL.md) | Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. |
| [progressive-web-app](../.archived/skills/frontend-core/progressive-web-app/SKILL.md) | Build Progressive Web Apps (PWAs) with offline support, installability, and caching strategies. Trigger whenever the user mentions PWA, service workers, web app manifests, Workbox, 'add to home screen', or wants their web app to work offline, feel native, or be installable. |
| [react-best-practices](../.archived/skills/frontend-core/react-best-practices/SKILL.md) | A comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Use when writing new React components or Next.js pages, implementing data fetching (client or server-side), or reviewing code for performance issues. |
| [react-component-performance](../.archived/skills/frontend-core/react-component-performance/SKILL.md) | Diagnose slow React components and suggest targeted performance fixes. |
| [react-flow-architect](../.archived/skills/frontend-core/react-flow-architect/SKILL.md) | Build production-ready ReactFlow applications with hierarchical navigation, performance optimization, and advanced state management. |
| [react-nextjs-development](../.archived/skills/frontend-core/react-nextjs-development/SKILL.md) | A specialized workflow for building React and Next.js 14+ applications with modern patterns including App Router, Server Components, TypeScript, Tailwind CSS, and more. |
| [react-state-management](../.archived/skills/frontend-core/react-state-management/SKILL.md) | Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions. |
| [screen-reader-testing](../.archived/skills/frontend-core/screen-reader-testing/SKILL.md) | A practical guide to testing web applications with screen readers for comprehensive accessibility validation. |
| [senior-frontend](../.archived/skills/frontend-core/senior-frontend/SKILL.md) | A comprehensive skill for frontend development using React, Next.js, TypeScript, and Tailwind CSS. It includes project scaffolding, component generation, bundle analysis, React patterns, Next.js optimization, and accessibility testing. |
| [web-artifacts-builder](../.archived/skills/frontend-core/web-artifacts-builder/SKILL.md) | A step-by-step guide to building frontend artifacts for claude.ai using React, TypeScript, and Vite. |
| [web-performance-optimization](../.archived/skills/frontend-core/web-performance-optimization/SKILL.md) | Optimize website and web application performance including loading speed, Core Web Vitals, bundle size, caching strategies, and runtime performance. |

</details>

### Frontend Security

<details>
<summary><b>Frontend Security (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [frontend-security-coder](../.archived/skills/frontend-security/frontend-security-coder/SKILL.md) | Expert in secure frontend coding practices specializing in XSS prevention, output sanitization, and client-side security patterns. |

</details>

### Frontend Seo

<details>
<summary><b>Frontend Seo (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [seo-authority-builder](../.archived/skills/frontend-seo/seo-authority-builder/SKILL.md) | Analyzes content for E-E-A-T signals and suggests improvements to build authority and trust. |
| [seo-content-auditor](../.archived/skills/frontend-seo/seo-content-auditor/SKILL.md) | Analyzes provided content for SEO optimization, focusing on E-E-A-T signals, readability, keyword usage, and structure. |
| [seo-fundamentals](../.archived/skills/frontend-seo/seo-fundamentals/SKILL.md) | Core principles of SEO including E-E-A-T, Core Web Vitals, technical foundations, content quality, and how modern search engines evaluate pages. |
| [seo-technical](../.archived/skills/frontend-seo/seo-technical/SKILL.md) | Audit technical SEO across crawlability, indexability, security, URLs, mobile, Core Web Vitals, structured data, JavaScript rendering, and related platform signals like robots.txt and AI crawler access. |

</details>

### Frontend Ui

<details>
<summary><b>Frontend Ui (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [antigravity-design-expert](../.archived/skills/frontend-ui/antigravity-design-expert/SKILL.md) | A UI/UX skill focused on building highly interactive, spatial, and weightless web interfaces using GSAP and 3D CSS. |
| [building-native-ui](../.archived/skills/frontend-ui/building-native-ui/SKILL.md) | A comprehensive guide for building beautiful apps with Expo Router, covering fundamentals, styling, components, navigation, animations, patterns, and native tabs. |
| [frontend-ui-dark-ts](../.archived/skills/frontend-ui/frontend-ui-dark-ts/SKILL.md) | A modern dark-themed React UI system using Tailwind CSS and Framer Motion. Designed for dashboards, admin panels, and data-rich applications with glassmorphism effects and tasteful animations. |
| [landing-page-generator](../.archived/skills/frontend-ui/landing-page-generator/SKILL.md) | Generates high-converting Next.js/React landing pages with Tailwind CSS, using PAS, AIDA, and BAB frameworks for optimized copy/components. |
| [mermaid-expert](../.archived/skills/frontend-ui/mermaid-expert/SKILL.md) | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and styling. |
| [react-ui-patterns](../.archived/skills/frontend-ui/react-ui-patterns/SKILL.md) | Modern React UI patterns for loading states, error handling, and data fetching. Use when building UI components, handling async data, or managing UI states. |
| [remotion-best-practices](../.archived/skills/frontend-ui/remotion-best-practices/SKILL.md) | Best practices for Remotion - Video creation in React |
| [web-design-guidelines](../.archived/skills/frontend-ui/web-design-guidelines/SKILL.md) | Review files for compliance with Web Interface Guidelines. |
| [web-scraper](../.archived/skills/frontend-ui/web-scraper/SKILL.md) | Web scraping skill that intelligently handles various data extraction scenarios, including pagination and multiple URLs. |

</details>

### Mobile Gaming Debugging

<details>
<summary><b>Mobile Gaming Debugging (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ios-debugger-agent](../.archived/skills/mobile-gaming-debugging/ios-debugger-agent/SKILL.md) | Debug an iOS project on a booted simulator using XcodeBuildMCP. |

</details>

### Mobile Gaming Gaming

<details>
<summary><b>Mobile Gaming Gaming (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [3d-games](../.archived/skills/mobile-gaming-gaming/3d-games/SKILL.md) | A comprehensive guide on 3D game development principles including rendering, shaders, physics, and camera systems. |
| [godot-4-migration](../.archived/skills/mobile-gaming-gaming/godot-4-migration/SKILL.md) | A specialized guide for migrating Godot 3.x projects to Godot 4, focusing on syntax changes, the new Tween system, and export annotation updates. |
| [unity-developer](../.archived/skills/mobile-gaming-gaming/unity-developer/SKILL.md) | A skill for building high-performance Unity games with optimized C# scripts, efficient rendering, and proper asset management. |
| [unity-ecs-patterns](../.archived/skills/mobile-gaming-gaming/unity-ecs-patterns/SKILL.md) | Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler. |
| [unreal-engine-cpp-pro](../.archived/skills/mobile-gaming-gaming/unreal-engine-cpp-pro/SKILL.md) | Expert guide for Unreal Engine 5.x C++ development, covering UObject hygiene, performance patterns, and best practices. |
| [web-games](../.archived/skills/mobile-gaming-gaming/web-games/SKILL.md) | Web browser game development principles, including framework selection, WebGPU adoption, performance optimization, asset strategy, PWA implementation, and audio handling. |

</details>

### Mobile Gaming Mobile

<details>
<summary><b>Mobile Gaming Mobile (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [2d-games](../.archived/skills/mobile-gaming-mobile/2d-games/SKILL.md) | A comprehensive guide to 2D game development principles including sprite systems, tilemap design, physics, camera systems, and genre patterns. |
| [ios-developer](../.archived/skills/mobile-gaming-mobile/ios-developer/SKILL.md) | Develop native iOS applications using Swift/SwiftUI, covering a wide range of topics from basic to advanced iOS development. |
| [mobile-design](../.archived/skills/mobile-gaming-mobile/mobile-design/SKILL.md) | A mobile design system focusing on platform clarity, interaction complexity, performance risk, offline dependence, and accessibility risk. |
| [mobile-developer](../.archived/skills/mobile-gaming-mobile/mobile-developer/SKILL.md) | Develop React Native, Flutter, or native mobile apps with modern architecture patterns. Masters cross-platform development, native integrations, offline sync, and app store optimization. |
| [mobile-games](../.archived/skills/mobile-gaming-mobile/mobile-games/SKILL.md) | Mobile game development principles including touch input, battery optimization, performance targets, app store requirements, monetization models, and anti-patterns. |
| [multiplayer](../.archived/skills/mobile-gaming-mobile/multiplayer/SKILL.md) | Multiplayer game development principles, including architecture selection, synchronization, network optimization, security, and matchmaking. |
| [pc-games](../.archived/skills/mobile-gaming-mobile/pc-games/SKILL.md) | PC and console game development principles including engine selection, platform features, optimization strategies. |

</details>

### Productivity Office

<details>
<summary><b>Productivity Office (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [docx-official](../.archived/skills/productivity-office/docx-official/SKILL.md) | A comprehensive guide on creating, editing, and analyzing .docx files using various tools and workflows. |
| [latex-paper-conversion](../.archived/skills/productivity-office/latex-paper-conversion/SKILL.md) | This skill automates the process of converting an academic paper written in LaTeX from one publisher's format to another by executing a structured multi-stage workflow, extracting content, mapping it to a new template, and resolving common compilation errors. |
| [pptx-official](../.archived/skills/productivity-office/pptx-official/SKILL.md) | A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. |
| [xlsx-official](../.archived/skills/productivity-office/xlsx-official/SKILL.md) | A comprehensive guide on creating, editing, and analyzing Excel files using Python libraries pandas and openpyxl, with emphasis on preserving formulas and ensuring dynamic updates. |

</details>

### Quality Code Review

<details>
<summary><b>Quality Code Review (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [address-github-comments](../.archived/skills/quality-code-review/address-github-comments/SKILL.md) | Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI. |
| [codebase-cleanup-tech-debt](../.archived/skills/quality-code-review/codebase-cleanup-tech-debt/SKILL.md) | A comprehensive guide for identifying, quantifying, and prioritizing technical debt in software projects, with actionable remediation plans and prevention strategies. |
| [comprehensive-review-full-review](../.archived/skills/quality-code-review/comprehensive-review-full-review/SKILL.md) | Comprehensive multi-dimensional code review using specialized review agents |

</details>

### Quality Debugging

<details>
<summary><b>Quality Debugging (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [debugging-strategies](../.archived/skills/quality-debugging/debugging-strategies/SKILL.md) | Transform debugging from frustrating guesswork into systematic problem-solving with proven strategies, powerful tools, and methodical approaches. |

</details>

### Quality Documentation

<details>
<summary><b>Quality Documentation (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ask-questions-if-underspecified](../.archived/skills/quality-documentation/ask-questions-if-underspecified/SKILL.md) | Clarify requirements before implementing. Use when serious doubts arise. |
| [writing-plans](../.archived/skills/quality-documentation/writing-plans/SKILL.md) | A skill for creating comprehensive implementation plans before writing code, ensuring each step is bite-sized and follows best practices like TDD. |

</details>

### Quality Observability

<details>
<summary><b>Quality Observability (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [error-diagnostics-error-trace](../.archived/skills/quality-observability/error-diagnostics-error-trace/SKILL.md) | You are an expert in setting up and optimizing error tracking systems, including configuring alerts, implementing structured logging, and ensuring real-time visibility of errors. |
| [incident-response-incident-response](../.archived/skills/quality-observability/incident-response-incident-response/SKILL.md) | Orchestrate multi-agent incident response with modern SRE practices for rapid resolution and learning. |
| [incident-runbook-templates](../.archived/skills/quality-observability/incident-runbook-templates/SKILL.md) | Production-ready templates for incident response runbooks covering detection, triage, mitigation, resolution, and communication. |
| [manifest](../.archived/skills/quality-observability/manifest/SKILL.md) | Configure the Manifest observability plugin for agents, setting up telemetry and connecting to Manifest for monitoring. |
| [prometheus-configuration](../.archived/skills/quality-observability/prometheus-configuration/SKILL.md) | A comprehensive guide to setting up Prometheus for metric collection, scraping, and alerting. |
| [slo-implementation](../.archived/skills/quality-observability/slo-implementation/SKILL.md) | A framework for defining and implementing Service Level Indicators (SLIs), Service Level Objectives (SLOs), and error budgets. |

</details>

### Quality Testing

<details>
<summary><b>Quality Testing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ddd-context-mapping](../.archived/skills/quality-testing/ddd-context-mapping/SKILL.md) | Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns. |
| [e2e-testing](../.archived/skills/quality-testing/e2e-testing/SKILL.md) | End-to-end testing workflow using Playwright for browser automation, visual regression, cross-browser testing, and CI/CD integration. |
| [e2e-testing-patterns](../.archived/skills/quality-testing/e2e-testing-patterns/SKILL.md) | Build reliable, fast, and maintainable end-to-end test suites that provide confidence to ship code quickly and catch regressions before users do. |
| [fixing-accessibility](../.archived/skills/quality-testing/fixing-accessibility/SKILL.md) | Audit and fix HTML accessibility issues including ARIA labels, keyboard navigation, focus management, color contrast, and form errors. Use when adding interactive controls, forms, dialogs, or reviewing WCAG compliance. |
| [git-hooks-automation](../.archived/skills/quality-testing/git-hooks-automation/SKILL.md) | Master Git hooks setup with Husky, lint-staged, pre-commit framework, and commitlint. Automate code quality gates, formatting, linting, and commit message enforcement before code reaches CI. |
| [go-playwright](../.archived/skills/quality-testing/go-playwright/SKILL.md) | Comprehensive framework for writing high-performance, production-grade browser automation scripts using Playwright Go, enforcing architectural best practices, robust error handling, structured logging, and advanced human-emulation techniques. |
| [memory-forensics](../.archived/skills/quality-testing/memory-forensics/SKILL.md) | Comprehensive techniques for acquiring, analyzing, and extracting artifacts from memory dumps for incident response and malware analysis. |
| [performance-testing-review-ai-review](../.archived/skills/quality-testing/performance-testing-review-ai-review/SKILL.md) | Comprehensive AI-powered code review combining multi-tool static analysis, state-of-the-art LLMs, and seamless CI/CD integration for actionable review comments across 30+ languages. |
| [playwright-java](../.archived/skills/quality-testing/playwright-java/SKILL.md) | This skill produces production-quality, enterprise-grade Playwright Java test code that enforces the Page Object Model (POM), strict locator strategies, thread-safe parallel execution, and full Allure reporting integration. |
| [playwright-skill](../.archived/skills/quality-testing/playwright-skill/SKILL.md) | A general-purpose browser automation skill that writes custom Playwright code for any requested task and executes it via the universal executor. |
| [python-testing-patterns](../.archived/skills/quality-testing/python-testing-patterns/SKILL.md) | Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and test-driven development practices. |
| [senior-it-ba-specialist](../.archived/skills/quality-testing/senior-it-ba-specialist/SKILL.md) | Act as a senior IT business analyst for software development initiatives, focusing on requirement elicitation, process modeling, traceability, and ensuring systems meet strict functional, security, and enterprise standards. |
| [tdd-orchestrator](../.archived/skills/quality-testing/tdd-orchestrator/SKILL.md) | Expert TDD orchestrator specializing in comprehensive test-driven development coordination, modern TDD practices, and multi-agent workflow management. |
| [test-automator](../.archived/skills/quality-testing/test-automator/SKILL.md) | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. Build scalable testing strategies with advanced CI/CD integration. |
| [test-fixing](../.archived/skills/quality-testing/test-fixing/SKILL.md) | Systematically identify and fix all failing tests using smart grouping strategies when explicitly asked to fix tests, reports test failures, or completes implementation and wants tests passing. |
| [webapp-testing](../.archived/skills/quality-testing/webapp-testing/SKILL.md) | To test local web applications, write native Python Playwright scripts using provided helper scripts. |
| [wiki-qa](../.archived/skills/quality-testing/wiki-qa/SKILL.md) | Answer repository questions grounded entirely in source code evidence. Use when user asks a question about the codebase, user wants to understand a specific file, function, or component, or user asks "how does X work" or "where is Y defined". |

</details>

### Security Compliance

<details>
<summary><b>Security Compliance (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [legal-advisor](../.archived/skills/security-compliance/legal-advisor/SKILL.md) | Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie policies, and data processing agreements. |
| [pci-compliance](../.archived/skills/security-compliance/pci-compliance/SKILL.md) | Master PCI DSS (Payment Card Industry Data Security Standard) compliance for secure payment processing and handling of cardholder data. |

</details>

### Security Defensive

<details>
<summary><b>Security Defensive (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [anti-reversing-techniques](../.archived/skills/security-defensive/anti-reversing-techniques/SKILL.md) | AUTHORIZED USE ONLY: This skill contains dual-use security techniques. Before proceeding with any bypass or analysis, verify authorization, document scope, and ensure legal compliance. |
| [ethical-hacking-methodology](../.archived/skills/security-defensive/ethical-hacking-methodology/SKILL.md) | Master the complete penetration testing lifecycle from reconnaissance through reporting, covering the five stages of ethical hacking methodology, essential tools, attack techniques, and professional reporting for authorized security assessments. |
| [privacy-by-design](../.archived/skills/security-defensive/privacy-by-design/SKILL.md) | Ensure privacy protections are built into apps from the start using Privacy by Design principles. |
| [threat-mitigation-mapping](../.archived/skills/security-defensive/threat-mitigation-mapping/SKILL.md) | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness. |
| [vulnerability-scanner](../.archived/skills/security-defensive/vulnerability-scanner/SKILL.md) | Advanced vulnerability analysis principles, including OWASP 2025, Supply Chain Security, attack surface mapping, and risk prioritization. |
| [wireshark-analysis](../.archived/skills/security-defensive/wireshark-analysis/SKILL.md) | Execute comprehensive network traffic analysis using Wireshark to capture, filter, and examine network packets for security investigations, performance optimization, and troubleshooting. |

</details>

### Security Offensive

<details>
<summary><b>Security Offensive (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [api-security-best-practices](../.archived/skills/security-offensive/api-security-best-practices/SKILL.md) | This skill provides guidance and best practices for implementing secure API design patterns including authentication, authorization, input validation, rate limiting, and protection against common vulnerabilities. |
| [attack-tree-construction](../.archived/skills/security-offensive/attack-tree-construction/SKILL.md) | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders. |
| [audit-context-building](../.archived/skills/security-offensive/audit-context-building/SKILL.md) | Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding. |
| [audit-skills](../.archived/skills/security-offensive/audit-skills/SKILL.md) | Expert security auditor for AI Skills and Bundles. Performs non-intrusive static analysis to identify malicious patterns, data leaks, system stability risks, and obfuscated payloads across Windows, macOS, Linux/Unix, and Mobile (Android/iOS). |
| [broken-authentication](../.archived/skills/security-offensive/broken-authentication/SKILL.md) | Identify and exploit authentication and session management vulnerabilities in web applications. |
| [cc-skill-security-review](../.archived/skills/security-offensive/cc-skill-security-review/SKILL.md) | This skill ensures all code follows security best practices and identifies potential vulnerabilities. |
| [codebase-audit-pre-push](../.archived/skills/security-offensive/codebase-audit-pre-push/SKILL.md) | A comprehensive codebase audit before pushing to GitHub, covering cleaning up junk files, fixing .gitignore, auditing source files, security checks, scalability, architecture, performance, documentation, and testing. |
| [codebase-cleanup-deps-audit](../.archived/skills/security-offensive/codebase-cleanup-deps-audit/SKILL.md) | Analyze project dependencies for known vulnerabilities, licensing issues, outdated packages, and provide actionable remediation strategies. |
| [dependency-upgrade](../.archived/skills/security-offensive/dependency-upgrade/SKILL.md) | Master major dependency version upgrades, compatibility analysis, staged upgrade strategies, and comprehensive testing approaches. |
| [differential-review](../.archived/skills/security-offensive/differential-review/SKILL.md) | Security-focused code review for PRs, commits, and diffs. |
| [file-path-traversal](../.archived/skills/security-offensive/file-path-traversal/SKILL.md) | Identify and exploit file path traversal vulnerabilities by understanding traversal principles, identifying vulnerable parameters, testing basic and advanced techniques, bypassing filters, targeting specific files, automating with tools like Burp Suite, ffuf, and wfuzz, and implementing secure coding practices to prevent such vulnerabilities. |
| [find-bugs](../.archived/skills/security-offensive/find-bugs/SKILL.md) | Find bugs, security vulnerabilities, and code quality issues in local branch changes. |
| [fixing-metadata](../.archived/skills/security-offensive/fixing-metadata/SKILL.md) | Audit and fix HTML metadata including page titles, meta descriptions, canonical URLs, Open Graph tags, Twitter cards, favicons, JSON-LD structured data, and robots directives. Use when adding or reviewing SEO and social metadata. |
| [gha-security-review](../.archived/skills/security-offensive/gha-security-review/SKILL.md) | Find exploitable vulnerabilities in GitHub Actions workflows, ensuring each finding includes a concrete exploitation scenario. |
| [html-injection-testing](../.archived/skills/security-offensive/html-injection-testing/SKILL.md) | Identify and exploit HTML injection vulnerabilities by testing web applications for reflected and stored HTML injections. |
| [idor-testing](../.archived/skills/security-offensive/idor-testing/SKILL.md) | Provide systematic methodologies for identifying and exploiting Insecure Direct Object Reference (IDOR) vulnerabilities in web applications. |
| [linux-privilege-escalation](../.archived/skills/security-offensive/linux-privilege-escalation/SKILL.md) | Execute systematic privilege escalation assessments on Linux systems to identify and exploit misconfigurations, vulnerable services, and security weaknesses that allow elevation from low-privilege user access to root-level control. |
| [privilege-escalation-methods](../.archived/skills/security-offensive/privilege-escalation-methods/SKILL.md) | Provide comprehensive techniques for escalating privileges from a low-privileged user to root/administrator access on compromised Linux and Windows systems. Essential for penetration testing post-exploitation phase and red team operations. |
| [production-code-audit](../.archived/skills/security-offensive/production-code-audit/SKILL.md) | Autonomously deep-scan entire codebase line-by-line, understand architecture and patterns, then systematically transform it to production-grade, corporate-level professional quality with optimizations. |
| [security-audit](../.archived/skills/security-offensive/security-audit/SKILL.md) | A comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening. |
| [sql-injection-testing](../.archived/skills/security-offensive/sql-injection-testing/SKILL.md) | Execute comprehensive SQL injection vulnerability assessments on web applications to identify database security flaws, demonstrate exploitation techniques, and validate input sanitization mechanisms. |
| [web-security-testing](../.archived/skills/security-offensive/web-security-testing/SKILL.md) | A specialized workflow for testing web applications against OWASP Top 10 vulnerabilities including injection attacks, XSS, broken authentication, and access control issues. |
| [windows-privilege-escalation](../.archived/skills/security-offensive/windows-privilege-escalation/SKILL.md) | Provide systematic methodologies for discovering and exploiting privilege escalation vulnerabilities on Windows systems during penetration testing engagements. |

</details>

