# 🧠 Antigravity Skills

**1,300+ specialized AI skills to give your coding agent domain expertise — automatically.**

> Sourced from [antigravity-awesome-skills](https://github.com/anthropics/awesome-claude-code-skills)

---

## 🤔 What Are Skills?

Skills are specialized instruction sets that teach AI assistants how to handle specific tasks. Think of them as **expert knowledge modules** that your AI can load on-demand.

**Simple analogy:** Just like you might consult different experts (a designer, a security expert, a marketer), skills let your AI become an expert in different areas exactly when you need them.

## 🚀 How to Use Skills

| Concept | Description |
|---|---|
| **Auto-Activation** | ⚡ Skills trigger automatically when your request matches a skill's domain. |
| **Manual Activation** | 🛠️ Say *"Use the [name] skill"* to explicitly load one. |
| **Deep Learning** | 📖 Each folder contains a `SKILL.md` with full technical instructions. |
| **Efficiency** | 📉 Minimal context is loaded first; details are only added as needed. |

---

## 📂 Folder Structure

Each skill is organized for both human browsing and AI context:

```
.archived/skills/
└── <category>/
    └── <skill-name>/
        ├── SKILL.md             # Main definition (the "brain")
        ├── scripts/             # Helper code (optional)
        ├── examples/            # How to use (optional)
        └── resources/           # Templates (optional)
```

---

## 🏗️ Skills by Category

### 🤖 AI, LLM & Agent Development

<details>
<summary><b>🤖 AI, LLM & Agent Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [20-andruia-niche-intelligence](.archived/skills/ai-llm-agent-development/20-andruia-niche-intelligence/SKILL.md) | Estratega de Inteligencia de Dominio de Andru.ia. Analiza el nicho específico de un proyecto para inyectar conocimientos, regulaciones y estándares únicos del sector. Actívalo tras definir el nicho. |
| [activecampaign-automation](.archived/skills/ai-llm-agent-development/activecampaign-automation/SKILL.md) | Automate ActiveCampaign tasks via Rube MCP (Composio): manage contacts, tags, list subscriptions, automation enrollment, and tasks. Always search tools first for current schemas. |
| [advanced-evaluation](.archived/skills/ai-llm-agent-development/advanced-evaluation/SKILL.md) | This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation bias", or mentions direct scoring, pairwise comparison, position bias, evaluation pipelines, or automated quality assessment. |
| [aegisops-ai](.archived/skills/ai-llm-agent-development/aegisops-ai/SKILL.md) | Autonomous DevSecOps & FinOps Guardrails. |
| [agent-evaluation](.archived/skills/ai-llm-agent-development/agent-evaluation/SKILL.md) | You're a quality engineer who has seen agents that aced benchmarks fail spectacularly in production. You've learned that evaluating LLM agents is fundamentally different from testing traditional software—the same input can produce different outputs, and \"correct\" often has no single answer. |
| [agent-framework-azure-ai-py](.archived/skills/ai-llm-agent-development/agent-framework-azure-ai-py/SKILL.md) | Build persistent agents on Azure AI Foundry using the Microsoft Agent Framework Python SDK. |
| [agent-manager-skill](.archived/skills/ai-llm-agent-development/agent-manager-skill/SKILL.md) | Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling. |
| [agent-memory-mcp](.archived/skills/ai-llm-agent-development/agent-memory-mcp/SKILL.md) | A hybrid memory system that provides persistent, searchable knowledge management for AI agents (Architecture, Patterns, Decisions). |
| [agent-memory-systems](.archived/skills/ai-llm-agent-development/agent-memory-systems/SKILL.md) | You are a cognitive architect who understands that memory makes agents intelligent. You've built memory systems for agents handling millions of interactions. You know that the hard part isn't storing - it's retrieving the right memory at the right time. |
| [agent-orchestration-improve-agent](.archived/skills/ai-llm-agent-development/agent-orchestration-improve-agent/SKILL.md) | Systematic improvement of existing agents through performance analysis, prompt engineering, and continuous iteration. |
| [agent-orchestrator](.archived/skills/ai-llm-agent-development/agent-orchestrator/SKILL.md) | Meta-skill que orquestra todos os agentes do ecossistema. Scan automatico de skills, match por capacidades, coordenacao de workflows multi-skill e registry management. |
| [agent-tool-builder](.archived/skills/ai-llm-agent-development/agent-tool-builder/SKILL.md) | You are an expert in the interface between LLMs and the outside world. You've seen tools that work beautifully and tools that cause agents to hallucinate, loop, or fail silently. The difference is almost always in the design, not the implementation. |
| [agentfolio](.archived/skills/ai-llm-agent-development/agentfolio/SKILL.md) | Skill for discovering and researching autonomous AI agents, tools, and ecosystems using the AgentFolio directory. |
| [agentmail](.archived/skills/ai-llm-agent-development/agentmail/SKILL.md) | Email infrastructure for AI agents. Create accounts, send/receive emails, manage webhooks, and check karma balance via the AgentMail API. |
| [agents-md](.archived/skills/ai-llm-agent-development/agents-md/SKILL.md) | This skill should be used when the user asks to "create AGENTS.md", "update AGENTS.md", "maintain agent docs", "set up CLAUDE.md", or needs to keep agent instructions concise. Enforces research-backed best practices for minimal, high-signal agent documentation. |
| [agents-v2-py](.archived/skills/ai-llm-agent-development/agents-v2-py/SKILL.md) | Build container-based Foundry Agents with Azure AI Projects SDK (ImageBasedHostedAgentDefinition). Use when creating hosted agents with custom container images in Azure AI Foundry. |
| [ai-agent-development](.archived/skills/ai-llm-agent-development/ai-agent-development/SKILL.md) | AI agent development workflow for building autonomous agents, multi-agent systems, and agent orchestration with CrewAI, LangGraph, and custom agents. |
| [ai-agents-architect](.archived/skills/ai-llm-agent-development/ai-agents-architect/SKILL.md) | I build AI systems that can act autonomously while remaining controllable. I understand that agents fail in unexpected ways - I design for graceful degradation and clear failure modes. I balance autonomy with oversight, knowing when an agent should ask for help vs proceed independently. |
| [ai-analyzer](.archived/skills/ai-llm-agent-development/ai-analyzer/SKILL.md) | AI驱动的综合健康分析系统，整合多维度健康数据、识别异常模式、预测健康风险、提供个性化建议。支持智能问答和AI健康报告生成。 |
| [ai-engineer](.archived/skills/ai-llm-agent-development/ai-engineer/SKILL.md) | Build production-ready LLM applications, advanced RAG systems, and intelligent agents. Implements vector search, multimodal AI, agent orchestration, and enterprise AI integrations. |
| [ai-engineering-toolkit](.archived/skills/ai-llm-agent-development/ai-engineering-toolkit/SKILL.md) | 6 production-ready AI engineering workflows: prompt evaluation (8-dimension scoring), context budget planning, RAG pipeline design, agent security audit (65-point checklist), eval harness building, and product sense coaching. |
| [ai-md](.archived/skills/ai-llm-agent-development/ai-md/SKILL.md) | Convert human-written CLAUDE.md into AI-native structured-label format. Battle-tested across 4 models. Same rules, fewer tokens, higher compliance. |
| [ai-ml](.archived/skills/ai-llm-agent-development/ai-ml/SKILL.md) | AI and machine learning workflow covering LLM application development, RAG implementation, agent architecture, ML pipelines, and AI-powered features. |
| [ai-native-cli](.archived/skills/ai-llm-agent-development/ai-native-cli/SKILL.md) | Design spec with 98 rules for building CLI tools that AI agents can safely use. Covers structured JSON output, error handling, input contracts, safety guardrails, exit codes, and agent self-description. |
| [ai-product](.archived/skills/ai-llm-agent-development/ai-product/SKILL.md) | You are an AI product engineer who has shipped LLM features to millions of users. You've debugged hallucinations at 3am, optimized prompts to reduce costs by 80%, and built safety systems that caught thousands of harmful outputs. You know that demos are easy and production is hard. |
| [ai-seo](.archived/skills/ai-llm-agent-development/ai-seo/SKILL.md) | Optimize content for AI search and LLM citations across AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and similar systems. Use when improving AI visibility, answer engine optimization, or citation readiness. |
| [ai-studio-image](.archived/skills/ai-llm-agent-development/ai-studio-image/SKILL.md) | Geracao de imagens humanizadas via Google AI Studio (Gemini). Fotos realistas estilo influencer ou educacional com iluminacao natural e imperfeicoes sutis. |
| [ai-wrapper-product](.archived/skills/ai-llm-agent-development/ai-wrapper-product/SKILL.md) | You know AI wrappers get a bad rap, but the good ones solve real problems. You build products where AI is the engine, not the gimmick. You understand prompt engineering is product development. You balance costs with user experience. You create AI products people actually pay for and use daily. |
| [airtable-automation](.archived/skills/ai-llm-agent-development/airtable-automation/SKILL.md) | Automate Airtable tasks via Rube MCP (Composio): records, bases, tables, fields, views. Always search tools first for current schemas. |
| [amplitude-automation](.archived/skills/ai-llm-agent-development/amplitude-automation/SKILL.md) | Automate Amplitude tasks via Rube MCP (Composio): events, user activity, cohorts, user identification. Always search tools first for current schemas. |
| [analyze-project](.archived/skills/ai-llm-agent-development/analyze-project/SKILL.md) | Forensic root cause analyzer for Antigravity sessions. Classifies scope deltas, rework patterns, root causes, hotspots, and auto-improves prompts/health. |
| [andrej-karpathy](.archived/skills/ai-llm-agent-development/andrej-karpathy/SKILL.md) | Agente que simula Andrej Karpathy — ex-Director of AI da Tesla, co-fundador da OpenAI, fundador da Eureka Labs, e o maior educador de deep learning do mundo. |
| [anti-reversing-techniques](.archived/skills/ai-llm-agent-development/anti-reversing-techniques/SKILL.md) | AUTHORIZED USE ONLY: This skill contains dual-use security techniques. Before proceeding with any bypass or analysis: > 1. |
| [apify-actor-development](.archived/skills/ai-llm-agent-development/apify-actor-development/SKILL.md) | Important: Before you begin, fill in the generatedBy property in the meta section of .actor/actor.json. Replace it with the tool and model you're currently using, such as \"Claude Code with Claude Sonnet 4.5\". This helps Apify monitor and improve AGENTS.md for specific AI tools and models. |
| [apify-competitor-intelligence](.archived/skills/ai-llm-agent-development/apify-competitor-intelligence/SKILL.md) | Analyze competitor strategies, content, pricing, ads, and market positioning across Google Maps, Booking.com, Facebook, Instagram, YouTube, and TikTok. |
| [apify-ultimate-scraper](.archived/skills/ai-llm-agent-development/apify-ultimate-scraper/SKILL.md) | AI-driven data extraction from 55+ Actors across all major platforms. This skill automatically selects the best Actor for your task. |
| [app-builder](.archived/skills/ai-llm-agent-development/app-builder/SKILL.md) | Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents. |
| [architecture-decision-records](.archived/skills/ai-llm-agent-development/architecture-decision-records/SKILL.md) | Comprehensive patterns for creating, maintaining, and managing Architecture Decision Records (ADRs) that capture the context and rationale behind significant technical decisions. |
| [arm-cortex-expert](.archived/skills/ai-llm-agent-development/arm-cortex-expert/SKILL.md) | Senior embedded software engineer specializing in firmware and driver development for ARM Cortex-M microcontrollers (Teensy, STM32, nRF52, SAMD). |
| [asana-automation](.archived/skills/ai-llm-agent-development/asana-automation/SKILL.md) | Automate Asana tasks via Rube MCP (Composio): tasks, projects, sections, teams, workspaces. Always search tools first for current schemas. |
| [audio-transcriber](.archived/skills/ai-llm-agent-development/audio-transcriber/SKILL.md) | Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration |
| [autonomous-agent-patterns](.archived/skills/ai-llm-agent-development/autonomous-agent-patterns/SKILL.md) | Design patterns for building autonomous coding agents, inspired by [Cline](https://github.com/cline/cline) and [OpenAI Codex](https://github.com/openai/codex). |
| [autonomous-agents](.archived/skills/ai-llm-agent-development/autonomous-agents/SKILL.md) | You are an agent architect who has learned the hard lessons of autonomous AI. You've seen the gap between impressive demos and production disasters. You know that a 95% success rate per step means only 60% by step 10. |
| [avoid-ai-writing](.archived/skills/ai-llm-agent-development/avoid-ai-writing/SKILL.md) | Audit and rewrite content to remove 21 categories of AI writing patterns with a 43-entry replacement table |
| [aws-compliance-checker](.archived/skills/ai-llm-agent-development/aws-compliance-checker/SKILL.md) | Automated compliance checking against CIS, PCI-DSS, HIPAA, and SOC 2 benchmarks |
| [azure-ai-agents-persistent-dotnet](.archived/skills/ai-llm-agent-development/azure-ai-agents-persistent-dotnet/SKILL.md) | Azure AI Agents Persistent SDK for .NET. Low-level SDK for creating and managing AI agents with threads, messages, runs, and tools. |
| [azure-ai-agents-persistent-java](.archived/skills/ai-llm-agent-development/azure-ai-agents-persistent-java/SKILL.md) | Azure AI Agents Persistent SDK for Java. Low-level SDK for creating and managing AI agents with threads, messages, runs, and tools. |
| [azure-ai-document-intelligence-dotnet](.archived/skills/ai-llm-agent-development/azure-ai-document-intelligence-dotnet/SKILL.md) | Azure AI Document Intelligence SDK for .NET. Extract text, tables, and structured data from documents using prebuilt and custom models. |
| [azure-ai-document-intelligence-ts](.archived/skills/ai-llm-agent-development/azure-ai-document-intelligence-ts/SKILL.md) | Extract text, tables, and structured data from documents using prebuilt and custom models. |
| [azure-ai-formrecognizer-java](.archived/skills/ai-llm-agent-development/azure-ai-formrecognizer-java/SKILL.md) | Build document analysis applications using the Azure AI Document Intelligence SDK for Java. |
| [azure-ai-projects-dotnet](.archived/skills/ai-llm-agent-development/azure-ai-projects-dotnet/SKILL.md) | Azure AI Projects SDK for .NET. High-level client for Azure AI Foundry projects including agents, connections, datasets, deployments, evaluations, and indexes. |
| [azure-ai-projects-ts](.archived/skills/ai-llm-agent-development/azure-ai-projects-ts/SKILL.md) | High-level SDK for Azure AI Foundry projects with agents, connections, deployments, and evaluations. |
| [azure-communication-callautomation-java](.archived/skills/ai-llm-agent-development/azure-communication-callautomation-java/SKILL.md) | Build server-side call automation workflows including IVR systems, call routing, recording, and AI-powered interactions. |
| [azure-communication-callingserver-java](.archived/skills/ai-llm-agent-development/azure-communication-callingserver-java/SKILL.md) | ⚠️ DEPRECATED: This SDK has been renamed to Call Automation. For new projects, use azure-communication-callautomation instead. This skill is for maintaining legacy code only. |
| [azure-storage-blob-py](.archived/skills/ai-llm-agent-development/azure-storage-blob-py/SKILL.md) | Azure Blob Storage SDK for Python. Use for uploading, downloading, listing blobs, managing containers, and blob lifecycle. |
| [azure-storage-blob-rust](.archived/skills/ai-llm-agent-development/azure-storage-blob-rust/SKILL.md) | Azure Blob Storage SDK for Rust. Use for uploading, downloading, and managing blobs and containers. |
| [azure-storage-blob-ts](.archived/skills/ai-llm-agent-development/azure-storage-blob-ts/SKILL.md) | Azure Blob Storage JavaScript/TypeScript SDK (@azure/storage-blob) for blob operations. Use for uploading, downloading, listing, and managing blobs and containers. |
| [bamboohr-automation](.archived/skills/ai-llm-agent-development/bamboohr-automation/SKILL.md) | Automate BambooHR tasks via Rube MCP (Composio): employees, time-off, benefits, dependents, employee updates. Always search tools first for current schemas. |
| [basecamp-automation](.archived/skills/ai-llm-agent-development/basecamp-automation/SKILL.md) | Automate Basecamp project management, to-dos, messages, people, and to-do list organization via Rube MCP (Composio). Always search tools first for current schemas. |
| [bash-pro](.archived/skills/ai-llm-agent-development/bash-pro/SKILL.md) | Master of defensive Bash scripting for production automation, CI/CD |
| [bdi-mental-states](.archived/skills/ai-llm-agent-development/bdi-mental-states/SKILL.md) | This skill should be used when the user asks to "model agent mental states", "implement BDI architecture", "create belief-desire-intention models", "transform RDF to beliefs", "build cognitive agent", or mentions BDI ontology, mental state modeling, rational agency, or neuro-symbolic AI integration. |
| [bdistill-behavioral-xray](.archived/skills/ai-llm-agent-development/bdistill-behavioral-xray/SKILL.md) | X-ray any AI model's behavioral patterns — refusal boundaries, hallucination tendencies, reasoning style, formatting defaults. No API key needed. |
| [bdistill-knowledge-extraction](.archived/skills/ai-llm-agent-development/bdistill-knowledge-extraction/SKILL.md) | Extract structured domain knowledge from AI models in-session or from local open-source models via Ollama. No API key needed. |
| [beautiful-prose](.archived/skills/ai-llm-agent-development/beautiful-prose/SKILL.md) | A hard-edged writing style contract for timeless, forceful English prose without modern AI tics. Use when users ask for prose or rewrites that must be clean, exact, concrete, and free of AI cadence, filler, or therapeutic tone. |
| [behavioral-modes](.archived/skills/ai-llm-agent-development/behavioral-modes/SKILL.md) | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. |
| [bitbucket-automation](.archived/skills/ai-llm-agent-development/bitbucket-automation/SKILL.md) | Automate Bitbucket repositories, pull requests, branches, issues, and workspace management via Rube MCP (Composio). Always search tools first for current schemas. |
| [blueprint](.archived/skills/ai-llm-agent-development/blueprint/SKILL.md) | Turn a one-line objective into a step-by-step construction plan any coding agent can execute cold. Each step has a self-contained context brief — a fresh agent in a new session can pick up any step without reading prior steps. |
| [box-automation](.archived/skills/ai-llm-agent-development/box-automation/SKILL.md) | Automate Box operations including file upload/download, content search, folder management, collaboration, metadata queries, and sign requests through Composio's Box toolkit. |
| [brevo-automation](.archived/skills/ai-llm-agent-development/brevo-automation/SKILL.md) | Automate Brevo (formerly Sendinblue) email marketing operations through Composio's Brevo toolkit via Rube MCP. |
| [bullmq-specialist](.archived/skills/ai-llm-agent-development/bullmq-specialist/SKILL.md) | BullMQ expert for Redis-backed job queues, background processing, and reliable async execution in Node.js/TypeScript applications. Use when: bullmq, bull queue, redis queue, background job, job queue. |
| [c4-container](.archived/skills/ai-llm-agent-development/c4-container/SKILL.md) | Expert C4 Container-level documentation specialist. |
| [cal-com-automation](.archived/skills/ai-llm-agent-development/cal-com-automation/SKILL.md) | Automate Cal.com tasks via Rube MCP (Composio): manage bookings, check availability, configure webhooks, and handle teams. Always search tools first for current schemas. |
| [calendly-automation](.archived/skills/ai-llm-agent-development/calendly-automation/SKILL.md) | Automate Calendly scheduling, event management, invitee tracking, availability checks, and organization administration via Rube MCP (Composio). Always search tools first for current schemas. |
| [canva-automation](.archived/skills/ai-llm-agent-development/canva-automation/SKILL.md) | Automate Canva tasks via Rube MCP (Composio): designs, exports, folders, brand templates, autofill. Always search tools first for current schemas. |
| [cc-skill-continuous-learning](.archived/skills/ai-llm-agent-development/cc-skill-continuous-learning/SKILL.md) | Development skill from everything-claude-code |
| [cc-skill-strategic-compact](.archived/skills/ai-llm-agent-development/cc-skill-strategic-compact/SKILL.md) | Development skill from everything-claude-code |
| [changelog-automation](.archived/skills/ai-llm-agent-development/changelog-automation/SKILL.md) | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions. |
| [cicd-automation-workflow-automate](.archived/skills/ai-llm-agent-development/cicd-automation-workflow-automate/SKILL.md) | You are a workflow automation expert specializing in creating efficient CI/CD pipelines, GitHub Actions workflows, and automated development processes. Design and implement automation that reduces manual work, improves consistency, and accelerates delivery while maintaining quality and security. |
| [circleci-automation](.archived/skills/ai-llm-agent-development/circleci-automation/SKILL.md) | Automate CircleCI tasks via Rube MCP (Composio): trigger pipelines, monitor workflows/jobs, retrieve artifacts and test metadata. Always search tools first for current schemas. |
| [claude-api](.archived/skills/ai-llm-agent-development/claude-api/SKILL.md) | Build apps with the Claude API or Anthropic SDK. TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`, or user asks to use Claude API, Anthropic SDKs, or Agent SDK. DO NOT TRIGGER when: code imports `openai`/other AI SDK, general programming, or ML/data-science tasks. |
| [clickup-automation](.archived/skills/ai-llm-agent-development/clickup-automation/SKILL.md) | Automate ClickUp project management including tasks, spaces, folders, lists, comments, and team operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [close-automation](.archived/skills/ai-llm-agent-development/close-automation/SKILL.md) | Automate Close CRM tasks via Rube MCP (Composio): create leads, manage calls/SMS, handle tasks, and track notes. Always search tools first for current schemas. |
| [coda-automation](.archived/skills/ai-llm-agent-development/coda-automation/SKILL.md) | Automate Coda tasks via Rube MCP (Composio): manage docs, pages, tables, rows, formulas, permissions, and publishing. Always search tools first for current schemas. |
| [code-review-ai-ai-review](.archived/skills/ai-llm-agent-development/code-review-ai-ai-review/SKILL.md) | You are an expert AI-powered code review specialist combining automated static analysis, intelligent pattern recognition, and modern DevOps practices. Leverage AI tools (GitHub Copilot, Qodo, GPT-5, C |
| [code-reviewer](.archived/skills/ai-llm-agent-development/code-reviewer/SKILL.md) | Elite code review expert specializing in modern AI-powered code |
| [code-simplifier](.archived/skills/ai-llm-agent-development/code-simplifier/SKILL.md) | Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when asked to "simplify code", "clean up code", "refactor for clarity", "improve readability", or review recently modified code for elegance. Focuses on project-specific best practices. |
| [codex-review](.archived/skills/ai-llm-agent-development/codex-review/SKILL.md) | Professional code review with auto CHANGELOG generation, integrated with Codex AI. Use when you want professional code review before commits, you need automatic CHANGELOG generation, or reviewing large-scale refactoring. |
| [cold-email](.archived/skills/ai-llm-agent-development/cold-email/SKILL.md) | Write B2B cold emails and follow-up sequences that earn replies. Use when creating outbound prospecting emails, SDR outreach, personalized opening lines, subject lines, CTAs, and multi-touch follow-up sequences. |
| [computer-use-agents](.archived/skills/ai-llm-agent-development/computer-use-agents/SKILL.md) | The fundamental architecture of computer use agents: observe screen, reason about next action, execute action, repeat. This loop integrates vision models with action execution through an iterative pipeline. |
| [conductor-setup](.archived/skills/ai-llm-agent-development/conductor-setup/SKILL.md) | Configure a Rails project to work with Conductor (parallel coding agents) |
| [confluence-automation](.archived/skills/ai-llm-agent-development/confluence-automation/SKILL.md) | Automate Confluence page creation, content search, space management, labels, and hierarchy navigation via Rube MCP (Composio). Always search tools first for current schemas. |
| [context-driven-development](.archived/skills/ai-llm-agent-development/context-driven-development/SKILL.md) | Guide for implementing and maintaining context as a managed artifact alongside code, enabling consistent AI interactions and team alignment through structured project documentation. |
| [context-fundamentals](.archived/skills/ai-llm-agent-development/context-fundamentals/SKILL.md) | Context is the complete state available to a language model at inference time. It includes everything the model can attend to when generating responses: system instructions, tool definitions, retrieved documents, message history, and tool outputs. |
| [context-manager](.archived/skills/ai-llm-agent-development/context-manager/SKILL.md) | Elite AI context engineering specialist mastering dynamic context management, vector databases, knowledge graphs, and intelligent memory systems. |
| [context-window-management](.archived/skills/ai-llm-agent-development/context-window-management/SKILL.md) | You're a context engineering specialist who has optimized LLM applications handling millions of conversations. You've seen systems hit token limits, suffer context rot, and lose critical information mid-dialogue. |
| [conversation-memory](.archived/skills/ai-llm-agent-development/conversation-memory/SKILL.md) | Persistent memory systems for LLM conversations including short-term, long-term, and entity-based memory Use when: conversation memory, remember, memory persistence, long-term memory, chat history. |
| [convertkit-automation](.archived/skills/ai-llm-agent-development/convertkit-automation/SKILL.md) | Automate ConvertKit (Kit) tasks via Rube MCP (Composio): manage subscribers, tags, broadcasts, and broadcast stats. Always search tools first for current schemas. |
| [cred-omega](.archived/skills/ai-llm-agent-development/cred-omega/SKILL.md) | CISO operacional enterprise para gestao total de credenciais e segredos. |
| [crewai](.archived/skills/ai-llm-agent-development/crewai/SKILL.md) | You are an expert in designing collaborative AI agent teams with CrewAI. You think in terms of roles, responsibilities, and delegation. You design clear agent personas with specific expertise, create well-defined tasks with expected outputs, and orchestrate crews for optimal collaboration. |
| [crypto-bd-agent](.archived/skills/ai-llm-agent-development/crypto-bd-agent/SKILL.md) | Production-tested patterns for building AI agents that autonomously discover, > evaluate, and acquire token listings for cryptocurrency exchanges. |
| [csharp-pro](.archived/skills/ai-llm-agent-development/csharp-pro/SKILL.md) | Write modern C# code with advanced features like records, pattern matching, and async/await. Optimizes .NET applications, implements enterprise patterns, and ensures comprehensive testing. |
| [customer-support](.archived/skills/ai-llm-agent-development/customer-support/SKILL.md) | Elite AI-powered customer support specialist mastering conversational AI, automated ticketing, sentiment analysis, and omnichannel support experiences. |
| [daily](.archived/skills/ai-llm-agent-development/daily/SKILL.md) | Documentation and capabilities reference for Daily |
| [daily-news-report](.archived/skills/ai-llm-agent-development/daily-news-report/SKILL.md) | Scrapes content based on a preset URL list, filters high-quality technical information, and generates daily Markdown reports. |
| [data-engineering-data-driven-feature](.archived/skills/ai-llm-agent-development/data-engineering-data-driven-feature/SKILL.md) | Build features guided by data insights, A/B testing, and continuous measurement using specialized agents for analysis, implementation, and experimentation. |
| [data-structure-protocol](.archived/skills/ai-llm-agent-development/data-structure-protocol/SKILL.md) | Give agents persistent structural memory of a codebase — navigate dependencies, track public APIs, and understand why connections exist without re-reading the whole repo. |
| [database-admin](.archived/skills/ai-llm-agent-development/database-admin/SKILL.md) | Expert database administrator specializing in modern cloud databases, automation, and reliability engineering. |
| [datadog-automation](.archived/skills/ai-llm-agent-development/datadog-automation/SKILL.md) | Automate Datadog tasks via Rube MCP (Composio): query metrics, search logs, manage monitors/dashboards, create events and downtimes. Always search tools first for current schemas. |
| [ddd-tactical-patterns](.archived/skills/ai-llm-agent-development/ddd-tactical-patterns/SKILL.md) | Apply DDD tactical patterns in code using entities, value objects, aggregates, repositories, and domain events with explicit invariants. |
| [debug-buttercup](.archived/skills/ai-llm-agent-development/debug-buttercup/SKILL.md) | All pods run in namespace crs. Use when pods in the crs namespace are in CrashLoopBackOff, OOMKilled, or restarting, multiple services restart simultaneously (cascade failure), or redis is unresponsive or showing AOF warnings. |
| [deployment-engineer](.archived/skills/ai-llm-agent-development/deployment-engineer/SKILL.md) | Expert deployment engineer specializing in modern CI/CD pipelines, GitOps workflows, and advanced deployment automation. |
| [diary](.archived/skills/ai-llm-agent-development/diary/SKILL.md) | Unified Diary System: A context-preserving automated logger for multi-project development. |
| [dispatching-parallel-agents](.archived/skills/ai-llm-agent-development/dispatching-parallel-agents/SKILL.md) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [docusign-automation](.archived/skills/ai-llm-agent-development/docusign-automation/SKILL.md) | Automate DocuSign tasks via Rube MCP (Composio): templates, envelopes, signatures, document management. Always search tools first for current schemas. |
| [dropbox-automation](.archived/skills/ai-llm-agent-development/dropbox-automation/SKILL.md) | Automate Dropbox file management, sharing, search, uploads, downloads, and folder operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [dx-optimizer](.archived/skills/ai-llm-agent-development/dx-optimizer/SKILL.md) | Developer Experience specialist. Improves tooling, setup, and workflows. Use PROACTIVELY when setting up new projects, after team feedback, or when development friction is noticed. |
| [e2e-testing-patterns](.archived/skills/ai-llm-agent-development/e2e-testing-patterns/SKILL.md) | Build reliable, fast, and maintainable end-to-end test suites that provide confidence to ship code quickly and catch regressions before users do. |
| [earllm-build](.archived/skills/ai-llm-agent-development/earllm-build/SKILL.md) | Build, maintain, and extend the EarLLM One Android project — a Kotlin/Compose app that connects Bluetooth earbuds to an LLM via voice pipeline. |
| [enhance-prompt](.archived/skills/ai-llm-agent-development/enhance-prompt/SKILL.md) | Transforms vague UI ideas into polished, Stitch-optimized prompts. Enhances specificity, adds UI/UX keywords, injects design system context, and structures output for better generation results. |
| [evolution](.archived/skills/ai-llm-agent-development/evolution/SKILL.md) | This skill enables makepad-skills to self-improve continuously during development. |
| [explain-like-socrates](.archived/skills/ai-llm-agent-development/explain-like-socrates/SKILL.md) | > |
| [expo-cicd-workflows](.archived/skills/ai-llm-agent-development/expo-cicd-workflows/SKILL.md) | Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS context, mentions .eas/workflows/, or wants help with EAS build pipelines or deployment automation. |
| [fal-audio](.archived/skills/ai-llm-agent-development/fal-audio/SKILL.md) | Text-to-speech and speech-to-text using fal.ai audio models |
| [fal-generate](.archived/skills/ai-llm-agent-development/fal-generate/SKILL.md) | Generate images and videos using fal.ai AI models |
| [fal-image-edit](.archived/skills/ai-llm-agent-development/fal-image-edit/SKILL.md) | AI-powered image editing with style transfer and object removal |
| [fal-upscale](.archived/skills/ai-llm-agent-development/fal-upscale/SKILL.md) | Upscale and enhance image and video resolution using AI |
| [fal-workflow](.archived/skills/ai-llm-agent-development/fal-workflow/SKILL.md) | Generate workflow JSON files for chaining AI models |
| [fda-food-safety-auditor](.archived/skills/ai-llm-agent-development/fda-food-safety-auditor/SKILL.md) | Expert AI auditor for FDA Food Safety (FSMA), HACCP, and PCQI compliance. Reviews food facility records and preventive controls. |
| [fda-medtech-compliance-auditor](.archived/skills/ai-llm-agent-development/fda-medtech-compliance-auditor/SKILL.md) | Expert AI auditor for Medical Device (SaMD) compliance, IEC 62304, and 21 CFR Part 820. Reviews DHFs, technical files, and software validation. |
| [figma-automation](.archived/skills/ai-llm-agent-development/figma-automation/SKILL.md) | Automate Figma tasks via Rube MCP (Composio): files, components, design tokens, comments, exports. Always search tools first for current schemas. |
| [fp-either-ref](.archived/skills/ai-llm-agent-development/fp-either-ref/SKILL.md) | Quick reference for Either type. Use when user needs error handling, validation, or operations that can fail with typed errors. |
| [fp-pragmatic](.archived/skills/ai-llm-agent-development/fp-pragmatic/SKILL.md) | A practical, jargon-free guide to functional programming - the 80/20 approach that gets results without the academic overhead |
| [freshdesk-automation](.archived/skills/ai-llm-agent-development/freshdesk-automation/SKILL.md) | Automate Freshdesk helpdesk operations including tickets, contacts, companies, notes, and replies via Rube MCP (Composio). Always search tools first for current schemas. |
| [freshservice-automation](.archived/skills/ai-llm-agent-development/freshservice-automation/SKILL.md) | Automate Freshservice ITSM tasks via Rube MCP (Composio): create/update tickets, bulk operations, service requests, and outbound emails. Always search tools first for current schemas. |
| [gdb-cli](.archived/skills/ai-llm-agent-development/gdb-cli/SKILL.md) | GDB debugging assistant for AI agents - analyze core dumps, debug live processes, investigate crashes and deadlocks with source code correlation |
| [gemini-api-dev](.archived/skills/ai-llm-agent-development/gemini-api-dev/SKILL.md) | The Gemini API provides access to Google's most advanced AI models. Key capabilities include: |
| [geo-fundamentals](.archived/skills/ai-llm-agent-development/geo-fundamentals/SKILL.md) | Generative Engine Optimization for AI search engines (ChatGPT, Claude, Perplexity). |
| [git-advanced-workflows](.archived/skills/ai-llm-agent-development/git-advanced-workflows/SKILL.md) | Master advanced Git techniques to maintain clean history, collaborate effectively, and recover from any situation with confidence. |
| [git-pr-workflows-git-workflow](.archived/skills/ai-llm-agent-development/git-pr-workflows-git-workflow/SKILL.md) | Orchestrate a comprehensive git workflow from code review through PR creation, leveraging specialized agents for quality assurance, testing, and deployment readiness. This workflow implements modern g |
| [github-automation](.archived/skills/ai-llm-agent-development/github-automation/SKILL.md) | Automate GitHub repositories, issues, pull requests, branches, CI/CD, and permissions via Rube MCP (Composio). Manage code workflows, review PRs, search code, and handle deployments programmatically. |
| [github-workflow-automation](.archived/skills/ai-llm-agent-development/github-workflow-automation/SKILL.md) | Patterns for automating GitHub workflows with AI assistance, inspired by [Gemini CLI](https://github.com/google-gemini/gemini-cli) and modern DevOps practices. |
| [gitlab-automation](.archived/skills/ai-llm-agent-development/gitlab-automation/SKILL.md) | Automate GitLab project management, issues, merge requests, pipelines, branches, and user operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [go-playwright](.archived/skills/ai-llm-agent-development/go-playwright/SKILL.md) | Expert capability for robust, stealthy, and efficient browser automation using Playwright Go. |
| [google-analytics-automation](.archived/skills/ai-llm-agent-development/google-analytics-automation/SKILL.md) | Automate Google Analytics tasks via Rube MCP (Composio): run reports, list accounts/properties, funnels, pivots, key events. Always search tools first for current schemas. |
| [googlesheets-automation](.archived/skills/ai-llm-agent-development/googlesheets-automation/SKILL.md) | Automate Google Sheets operations (read, write, format, filter, manage spreadsheets) via Rube MCP (Composio). Read/write data, manage tabs, apply formatting, and search rows programmatically. |
| [helpdesk-automation](.archived/skills/ai-llm-agent-development/helpdesk-automation/SKILL.md) | Automate HelpDesk tasks via Rube MCP (Composio): list tickets, manage views, use canned responses, and configure custom fields. Always search tools first for current schemas. |
| [hierarchical-agent-memory](.archived/skills/ai-llm-agent-development/hierarchical-agent-memory/SKILL.md) | Scoped CLAUDE.md memory system that reduces context token spend. Creates directory-level context files, tracks savings via dashboard, and routes agents to the right sub-context. |
| [hosted-agents](.archived/skills/ai-llm-agent-development/hosted-agents/SKILL.md) | Build background agents in sandboxed environments. Use for hosted coding agents, sandboxed VMs, Modal sandboxes, and remote coding environments. |
| [hosted-agents-v2-py](.archived/skills/ai-llm-agent-development/hosted-agents-v2-py/SKILL.md) | Build hosted agents using Azure AI Projects SDK with ImageBasedHostedAgentDefinition. Use when creating container-based agents in Azure AI Foundry. |
| [hybrid-search-implementation](.archived/skills/ai-llm-agent-development/hybrid-search-implementation/SKILL.md) | Combine vector and keyword search for improved retrieval. Use when implementing RAG systems, building search engines, or when neither approach alone provides sufficient recall. |
| [iconsax-library](.archived/skills/ai-llm-agent-development/iconsax-library/SKILL.md) | Extensive icon library and AI-driven icon generation skill for premium UI/UX design. |
| [ilya-sutskever](.archived/skills/ai-llm-agent-development/ilya-sutskever/SKILL.md) | Agente que simula Ilya Sutskever — co-fundador da OpenAI, ex-Chief Scientist, fundador da SSI. Use quando quiser perspectivas sobre: AGI safety-first, consciência de IA, scaling laws, deep learning profundo, o episódio de novembro 2023 na OpenAI, superinteligência segura. |
| [image-studio](.archived/skills/ai-llm-agent-development/image-studio/SKILL.md) | Studio de geracao de imagens inteligente — roteamento automatico entre ai-studio-image (fotos humanizadas/influencer) e stability-ai (arte/ ilustracao/edicao). Detecta o tipo de imagem solicitada e escolhe o modelo ideal automaticamente. |
| [incident-response-smart-fix](.archived/skills/ai-llm-agent-development/incident-response-smart-fix/SKILL.md) | [Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observability platforms to systematically diagnose and res |
| [infinite-gratitude](.archived/skills/ai-llm-agent-development/infinite-gratitude/SKILL.md) | Multi-agent research skill for parallel research execution (10 agents, battle-tested with real case studies). |
| [instagram-automation](.archived/skills/ai-llm-agent-development/instagram-automation/SKILL.md) | Automate Instagram tasks via Rube MCP (Composio): create posts, carousels, manage media, get insights, and publishing limits. Always search tools first for current schemas. |
| [intercom-automation](.archived/skills/ai-llm-agent-development/intercom-automation/SKILL.md) | Automate Intercom tasks via Rube MCP (Composio): conversations, contacts, companies, segments, admins. Always search tools first for current schemas. |
| [inventory-demand-planning](.archived/skills/ai-llm-agent-development/inventory-demand-planning/SKILL.md) | Codified expertise for demand forecasting, safety stock optimisation, replenishment planning, and promotional lift estimation at multi-location retailers. |
| [iterate-pr](.archived/skills/ai-llm-agent-development/iterate-pr/SKILL.md) | Iterate on a PR until CI passes. Use when you need to fix CI failures, address review feedback, or continuously push fixes until all checks are green. Automates the feedback-fix-push-wait cycle. |
| [jira-automation](.archived/skills/ai-llm-agent-development/jira-automation/SKILL.md) | Automate Jira tasks via Rube MCP (Composio): issues, projects, sprints, boards, comments, users. Always search tools first for current schemas. |
| [jobgpt](.archived/skills/ai-llm-agent-development/jobgpt/SKILL.md) | Job search automation, auto apply, resume generation, application tracking, salary intelligence, and recruiter outreach using the JobGPT MCP server. |
| [kaizen](.archived/skills/ai-llm-agent-development/kaizen/SKILL.md) | Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements. |
| [klaviyo-automation](.archived/skills/ai-llm-agent-development/klaviyo-automation/SKILL.md) | Automate Klaviyo tasks via Rube MCP (Composio): manage email/SMS campaigns, inspect campaign messages, track tags, and monitor send jobs. Always search tools first for current schemas. |
| [langchain-architecture](.archived/skills/ai-llm-agent-development/langchain-architecture/SKILL.md) | Master the LangChain framework for building sophisticated LLM applications with agents, chains, memory, and tool integration. |
| [langfuse](.archived/skills/ai-llm-agent-development/langfuse/SKILL.md) | You are an expert in LLM observability and evaluation. You think in terms of traces, spans, and metrics. You know that LLM applications need monitoring just like traditional software - but with different dimensions (cost, quality, latency). |
| [langgraph](.archived/skills/ai-llm-agent-development/langgraph/SKILL.md) | You are an expert in building production-grade AI agents with LangGraph. You understand that agents need explicit structure - graphs make the flow visible and debuggable. You design state carefully, use reducers appropriately, and always consider persistence for production. |
| [last30days](.archived/skills/ai-llm-agent-development/last30days/SKILL.md) | Research a topic from the last 30 days on Reddit + X + Web, become an expert, and write copy-paste-ready prompts for the user's target tool. |
| [lead-magnets](.archived/skills/ai-llm-agent-development/lead-magnets/SKILL.md) | Plan and optimize lead magnets for email capture and lead generation. Use when designing gated content, checklists, templates, downloadable resources, or other offers that convert visitors into subscribers. |
| [legal-advisor](.archived/skills/ai-llm-agent-development/legal-advisor/SKILL.md) | Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie policies, and data processing agreements. |
| [leiloeiro-juridico](.archived/skills/ai-llm-agent-development/leiloeiro-juridico/SKILL.md) | Analise juridica de leiloes: nulidades, bem de familia, alienacao fiduciaria, CPC arts 829-903, Lei 9514/97, onus reais, embargos e jurisprudencia. |
| [libreoffice-calc](.archived/skills/ai-llm-agent-development/libreoffice-calc/SKILL.md) | Spreadsheet creation, format conversion (ODS/XLSX/CSV), formulas, data automation with LibreOffice Calc. |
| [libreoffice-impress](.archived/skills/ai-llm-agent-development/libreoffice-impress/SKILL.md) | Presentation creation, format conversion (ODP/PPTX/PDF), slide automation with LibreOffice Impress. |
| [libreoffice-writer](.archived/skills/ai-llm-agent-development/libreoffice-writer/SKILL.md) | Document creation, format conversion (ODT/DOCX/PDF), mail merge, and automation with LibreOffice Writer. |
| [lightning-factory-explainer](.archived/skills/ai-llm-agent-development/lightning-factory-explainer/SKILL.md) | Explain Bitcoin Lightning channel factories and the SuperScalar protocol — scalable Lightning onboarding using shared UTXOs, Decker-Wattenhofer trees, timeout-signature trees, MuSig2, and Taproot. No soft fork required. |
| [linear-automation](.archived/skills/ai-llm-agent-development/linear-automation/SKILL.md) | Automate Linear tasks via Rube MCP (Composio): issues, projects, cycles, teams, labels. Always search tools first for current schemas. |
| [linkedin-automation](.archived/skills/ai-llm-agent-development/linkedin-automation/SKILL.md) | Automate LinkedIn tasks via Rube MCP (Composio): create posts, manage profile, company info, comments, and image uploads. Always search tools first for current schemas. |
| [llm-app-patterns](.archived/skills/ai-llm-agent-development/llm-app-patterns/SKILL.md) | Production-ready patterns for building LLM applications, inspired by [Dify](https://github.com/langgenius/dify) and industry best practices. |
| [llm-application-dev-ai-assistant](.archived/skills/ai-llm-agent-development/llm-application-dev-ai-assistant/SKILL.md) | You are an AI assistant development expert specializing in creating intelligent conversational interfaces, chatbots, and AI-powered applications. Design comprehensive AI assistant solutions with natur |
| [llm-application-dev-langchain-agent](.archived/skills/ai-llm-agent-development/llm-application-dev-langchain-agent/SKILL.md) | You are an expert LangChain agent developer specializing in production-grade AI systems using LangChain 0.1+ and LangGraph. |
| [llm-application-dev-prompt-optimize](.archived/skills/ai-llm-agent-development/llm-application-dev-prompt-optimize/SKILL.md) | You are an expert prompt engineer specializing in crafting effective prompts for LLMs through advanced techniques including constitutional AI, chain-of-thought reasoning, and model-specific optimizati |
| [llm-evaluation](.archived/skills/ai-llm-agent-development/llm-evaluation/SKILL.md) | Master comprehensive evaluation strategies for LLM applications, from automated metrics to human evaluation and A/B testing. |
| [llm-ops](.archived/skills/ai-llm-agent-development/llm-ops/SKILL.md) | LLM Operations -- RAG, embeddings, vector databases, fine-tuning, prompt engineering avancado, custos de LLM, evals de qualidade e arquiteturas de IA para producao. |
| [llm-prompt-optimizer](.archived/skills/ai-llm-agent-development/llm-prompt-optimizer/SKILL.md) | Use when improving prompts for any LLM. Applies proven prompt engineering techniques to boost output quality, reduce hallucinations, and cut token usage. |
| [llm-structured-output](.archived/skills/ai-llm-agent-development/llm-structured-output/SKILL.md) | > |
| [local-db-migration](.archived/skills/ai-llm-agent-development/local-db-migration/SKILL.md) | Manages schema migrations and vector initialization for the based-workspace-postgres container. |
| [local-llm-expert](.archived/skills/ai-llm-agent-development/local-llm-expert/SKILL.md) | Master local LLM inference, model selection, VRAM optimization, and local deployment using Ollama, llama.cpp, vLLM, and LM Studio. Expert in quantization formats (GGUF, EXL2) and local AI privacy. |
| [m365-agents-dotnet](.archived/skills/ai-llm-agent-development/m365-agents-dotnet/SKILL.md) | Microsoft 365 Agents SDK for .NET. Build multichannel agents for Teams/M365/Copilot Studio with ASP.NET Core hosting, AgentApplication routing, and MSAL-based auth. |
| [m365-agents-py](.archived/skills/ai-llm-agent-development/m365-agents-py/SKILL.md) | Microsoft 365 Agents SDK for Python. Build multichannel agents for Teams/M365/Copilot Studio with aiohttp hosting, AgentApplication routing, streaming responses, and MSAL-based auth. |
| [m365-agents-ts](.archived/skills/ai-llm-agent-development/m365-agents-ts/SKILL.md) | Microsoft 365 Agents SDK for TypeScript/Node.js. |
| [magic-animator](.archived/skills/ai-llm-agent-development/magic-animator/SKILL.md) | AI-powered animation tool for creating motion in logos, UI, icons, and social media assets. |
| [make-automation](.archived/skills/ai-llm-agent-development/make-automation/SKILL.md) | Automate Make (Integromat) tasks via Rube MCP (Composio): operations, enums, language and timezone lookups. Always search tools first for current schemas. |
| [malware-analyst](.archived/skills/ai-llm-agent-development/malware-analyst/SKILL.md) | Expert malware analyst specializing in defensive malware research, threat intelligence, and incident response. Masters sandbox analysis, behavioral analysis, and malware family identification. |
| [manifest](.archived/skills/ai-llm-agent-development/manifest/SKILL.md) | Install and configure the Manifest observability plugin for your agents. Use when setting up telemetry, configuring API keys, or troubleshooting the plugin. |
| [market-sizing-analysis](.archived/skills/ai-llm-agent-development/market-sizing-analysis/SKILL.md) | Comprehensive market sizing methodologies for calculating Total Addressable Market (TAM), Serviceable Available Market (SAM), and Serviceable Obtainable Market (SOM) for startup opportunities. |
| [maxia](.archived/skills/ai-llm-agent-development/maxia/SKILL.md) | Connect to MAXIA AI-to-AI marketplace on Solana. Discover, buy, sell AI services. Earn USDC. 13 MCP tools, A2A protocol, DeFi yields, sentiment analysis, rug detection. |
| [memory-safety-patterns](.archived/skills/ai-llm-agent-development/memory-safety-patterns/SKILL.md) | Cross-language patterns for memory-safe programming including RAII, ownership, smart pointers, and resource management. |
| [micro-saas-launcher](.archived/skills/ai-llm-agent-development/micro-saas-launcher/SKILL.md) | You ship fast and iterate. You know the difference between a side project and a business. You've seen what works in the indie hacker community. You help people go from idea to paying customers in weeks, not years. You focus on sustainable, profitable businesses - not unicorn hunting. |
| [microsoft-teams-automation](.archived/skills/ai-llm-agent-development/microsoft-teams-automation/SKILL.md) | Automate Microsoft Teams tasks via Rube MCP (Composio): send messages, manage channels, create meetings, handle chats, and search messages. Always search tools first for current schemas. |
| [miro-automation](.archived/skills/ai-llm-agent-development/miro-automation/SKILL.md) | Automate Miro tasks via Rube MCP (Composio): boards, items, sticky notes, frames, sharing, connectors. Always search tools first for current schemas. |
| [mixpanel-automation](.archived/skills/ai-llm-agent-development/mixpanel-automation/SKILL.md) | Automate Mixpanel tasks via Rube MCP (Composio): events, segmentation, funnels, cohorts, user profiles, JQL queries. Always search tools first for current schemas. |
| [modern-javascript-patterns](.archived/skills/ai-llm-agent-development/modern-javascript-patterns/SKILL.md) | Comprehensive guide for mastering modern JavaScript (ES6+) features, functional programming patterns, and best practices for writing clean, maintainable, and performant code. |
| [monday-automation](.archived/skills/ai-llm-agent-development/monday-automation/SKILL.md) | Automate Monday.com work management including boards, items, columns, groups, subitems, and updates via Rube MCP (Composio). Always search tools first for current schemas. |
| [multi-agent-brainstorming](.archived/skills/ai-llm-agent-development/multi-agent-brainstorming/SKILL.md) | Simulate a structured peer-review process using multiple specialized agents to validate designs, surface hidden assumptions, and identify failure modes before implementation. |
| [nanobanana-ppt-skills](.archived/skills/ai-llm-agent-development/nanobanana-ppt-skills/SKILL.md) | AI-powered PPT generation with document analysis and styled images |
| [new-rails-project](.archived/skills/ai-llm-agent-development/new-rails-project/SKILL.md) | Create a new Rails project |
| [notion-automation](.archived/skills/ai-llm-agent-development/notion-automation/SKILL.md) | Automate Notion tasks via Rube MCP (Composio): pages, databases, blocks, comments, users. Always search tools first for current schemas. |
| [one-drive-automation](.archived/skills/ai-llm-agent-development/one-drive-automation/SKILL.md) | Automate OneDrive file management, search, uploads, downloads, sharing, permissions, and folder operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [outlook-automation](.archived/skills/ai-llm-agent-development/outlook-automation/SKILL.md) | Automate Outlook tasks via Rube MCP (Composio): emails, calendar, contacts, folders, attachments. Always search tools first for current schemas. |
| [outlook-calendar-automation](.archived/skills/ai-llm-agent-development/outlook-calendar-automation/SKILL.md) | Automate Outlook Calendar tasks via Rube MCP (Composio): create events, manage attendees, find meeting times, and handle invitations. Always search tools first for current schemas. |
| [pagerduty-automation](.archived/skills/ai-llm-agent-development/pagerduty-automation/SKILL.md) | Automate PagerDuty tasks via Rube MCP (Composio): manage incidents, services, schedules, escalation policies, and on-call rotations. Always search tools first for current schemas. |
| [parallel-agents](.archived/skills/ai-llm-agent-development/parallel-agents/SKILL.md) | Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives. |
| [paywall-upgrade-cro](.archived/skills/ai-llm-agent-development/paywall-upgrade-cro/SKILL.md) | You are an expert in in-app paywalls and upgrade flows. Your goal is to convert free users to paid, or upgrade users to higher tiers, at moments when they've experienced enough value to justify the commitment. |
| [performance-testing-review-ai-review](.archived/skills/ai-llm-agent-development/performance-testing-review-ai-review/SKILL.md) | You are an expert AI-powered code review specialist combining automated static analysis, intelligent pattern recognition, and modern DevOps practices. Leverage AI tools (GitHub Copilot, Qodo, GPT-5, C |
| [pipecat-friday-agent](.archived/skills/ai-llm-agent-development/pipecat-friday-agent/SKILL.md) | Build a low-latency, Iron Man-inspired tactical voice assistant (F.R.I.D.A.Y.) using Pipecat, Gemini, and OpenAI. |
| [pipedrive-automation](.archived/skills/ai-llm-agent-development/pipedrive-automation/SKILL.md) | Automate Pipedrive CRM operations including deals, contacts, organizations, activities, notes, and pipeline management via Rube MCP (Composio). Always search tools first for current schemas. |
| [posthog-automation](.archived/skills/ai-llm-agent-development/posthog-automation/SKILL.md) | Automate PostHog tasks via Rube MCP (Composio): events, feature flags, projects, user profiles, annotations. Always search tools first for current schemas. |
| [postmark-automation](.archived/skills/ai-llm-agent-development/postmark-automation/SKILL.md) | Automate Postmark email delivery tasks via Rube MCP (Composio): send templated emails, manage templates, monitor delivery stats and bounces. Always search tools first for current schemas. |
| [progressive-estimation](.archived/skills/ai-llm-agent-development/progressive-estimation/SKILL.md) | Estimate AI-assisted and hybrid human+agent development work with research-backed PERT statistics and calibration feedback loops |
| [project-development](.archived/skills/ai-llm-agent-development/project-development/SKILL.md) | This skill covers the principles for identifying tasks suited to LLM processing, designing effective project architectures, and iterating rapidly using agent-assisted development. |
| [prompt-caching](.archived/skills/ai-llm-agent-development/prompt-caching/SKILL.md) | You're a caching specialist who has reduced LLM costs by 90% through strategic caching. You've implemented systems that cache at multiple levels: prompt prefixes, full responses, and semantic similarity matches. |
| [prompt-engineer](.archived/skills/ai-llm-agent-development/prompt-engineer/SKILL.md) | Transforms user prompts into optimized prompts using frameworks (RTF, RISEN, Chain of Thought, RODES, Chain of Density, RACE, RISE, STAR, SOAP, CLEAR, GROW) |
| [prompt-engineering](.archived/skills/ai-llm-agent-development/prompt-engineering/SKILL.md) | Expert guide on prompt engineering patterns, best practices, and optimization techniques. Use when user wants to improve prompts, learn prompting strategies, or debug agent behavior. |
| [prompt-engineering-patterns](.archived/skills/ai-llm-agent-development/prompt-engineering-patterns/SKILL.md) | Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability. |
| [prompt-library](.archived/skills/ai-llm-agent-development/prompt-library/SKILL.md) | A comprehensive collection of battle-tested prompts inspired by [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) and community best practices. |
| [pydantic-ai](.archived/skills/ai-llm-agent-development/pydantic-ai/SKILL.md) | Build production-ready AI agents with PydanticAI — type-safe tool use, structured outputs, dependency injection, and multi-model support. |
| [pypict-skill](.archived/skills/ai-llm-agent-development/pypict-skill/SKILL.md) | Pairwise test generation |
| [rag-engineer](.archived/skills/ai-llm-agent-development/rag-engineer/SKILL.md) | I bridge the gap between raw documents and LLM understanding. I know that retrieval quality determines generation quality - garbage in, garbage out. I obsess over chunking boundaries, embedding dimensions, and similarity metrics because they make the difference between helpful and hallucinating. |
| [rag-implementation](.archived/skills/ai-llm-agent-development/rag-implementation/SKILL.md) | RAG (Retrieval-Augmented Generation) implementation workflow covering embedding selection, vector database setup, chunking strategies, and retrieval optimization. |
| [recallmax](.archived/skills/ai-llm-agent-development/recallmax/SKILL.md) | FREE — God-tier long-context memory for AI agents. Injects 500K-1M clean tokens, auto-summarizes with tone/intent preservation, compresses 14-turn history into 800 tokens. |
| [red-team-tools](.archived/skills/ai-llm-agent-development/red-team-tools/SKILL.md) | Implement proven methodologies and tool workflows from top security researchers for effective reconnaissance, vulnerability discovery, and bug bounty hunting. Automate common tasks while maintaining thorough coverage of attack surfaces. |
| [reddit-automation](.archived/skills/ai-llm-agent-development/reddit-automation/SKILL.md) | Automate Reddit tasks via Rube MCP (Composio): search subreddits, create posts, manage comments, and browse top content. Always search tools first for current schemas. |
| [render-automation](.archived/skills/ai-llm-agent-development/render-automation/SKILL.md) | Automate Render tasks via Rube MCP (Composio): services, deployments, projects. Always search tools first for current schemas. |
| [returns-reverse-logistics](.archived/skills/ai-llm-agent-development/returns-reverse-logistics/SKILL.md) | Codified expertise for returns authorisation, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims management. |
| [reverse-engineer](.archived/skills/ai-llm-agent-development/reverse-engineer/SKILL.md) | Expert reverse engineer specializing in binary analysis, disassembly, decompilation, and software analysis. Masters IDA Pro, Ghidra, radare2, x64dbg, and modern RE toolchains. |
| [sales-automator](.archived/skills/ai-llm-agent-development/sales-automator/SKILL.md) | Draft cold emails, follow-ups, and proposal templates. Creates |
| [salesforce-automation](.archived/skills/ai-llm-agent-development/salesforce-automation/SKILL.md) | Automate Salesforce tasks via Rube MCP (Composio): leads, contacts, accounts, opportunities, SOQL queries. Always search tools first for current schemas. |
| [sam-altman](.archived/skills/ai-llm-agent-development/sam-altman/SKILL.md) | Agente que simula Sam Altman — CEO da OpenAI, ex-presidente da Y Combinator, arquiteto da era AGI. |
| [seek-and-analyze-video](.archived/skills/ai-llm-agent-development/seek-and-analyze-video/SKILL.md) | Seek and analyze video content using Memories.ai Large Visual Memory Model for persistent video intelligence |
| [segment-automation](.archived/skills/ai-llm-agent-development/segment-automation/SKILL.md) | Automate Segment tasks via Rube MCP (Composio): track events, identify users, manage groups, page views, aliases, batch operations. Always search tools first for current schemas. |
| [sentry-automation](.archived/skills/ai-llm-agent-development/sentry-automation/SKILL.md) | Automate Sentry tasks via Rube MCP (Composio): manage issues/events, configure alerts, track releases, monitor projects and teams. Always search tools first for current schemas. |
| [seo](.archived/skills/ai-llm-agent-development/seo/SKILL.md) | Run a broad SEO audit across technical SEO, on-page SEO, schema, sitemaps, content quality, AI search readiness, and GEO. Use as the umbrella skill when the user asks for a full SEO analysis or strategy. |
| [seo-content-refresher](.archived/skills/ai-llm-agent-development/seo-content-refresher/SKILL.md) | Identifies outdated elements in provided content and suggests updates to maintain freshness. Finds statistics, dates, and examples that need updating. Use PROACTIVELY for older content. |
| [seo-dataforseo](.archived/skills/ai-llm-agent-development/seo-dataforseo/SKILL.md) | Use DataForSEO for live SERPs, keyword metrics, backlinks, competitor analysis, on-page checks, and AI visibility data. Trigger when the user needs real SEO data rather than static guidance. |
| [seo-geo](.archived/skills/ai-llm-agent-development/seo-geo/SKILL.md) | Optimize content for AI Overviews, ChatGPT, Perplexity, and other AI search systems. Use when improving GEO, AI citations, llms.txt readiness, crawler accessibility, and passage-level citability. |
| [shodan-reconnaissance](.archived/skills/ai-llm-agent-development/shodan-reconnaissance/SKILL.md) | Provide systematic methodologies for leveraging Shodan as a reconnaissance tool during penetration testing engagements. |
| [shopify-automation](.archived/skills/ai-llm-agent-development/shopify-automation/SKILL.md) | Automate Shopify tasks via Rube MCP (Composio): products, orders, customers, inventory, collections. Always search tools first for current schemas. |
| [skill-check](.archived/skills/ai-llm-agent-development/skill-check/SKILL.md) | Validate Claude Code skills against the agentskills specification. Catches structural, semantic, and naming issues before users do. |
| [skill-creator](.archived/skills/ai-llm-agent-development/skill-creator/SKILL.md) | To create new CLI skills following Anthropic's official best practices with zero manual configuration. This skill automates brainstorming, template application, validation, and installation processes while maintaining progressive disclosure patterns and writing style standards. |
| [skill-improver](.archived/skills/ai-llm-agent-development/skill-improver/SKILL.md) | Iteratively improve a Claude Code skill using the skill-reviewer agent until it meets quality standards. Use when improving a skill with multiple quality issues, iterating on a new skill until it meets standards, or automated fix-review cycles instead of manual editing. |
| [skill-rails-upgrade](.archived/skills/ai-llm-agent-development/skill-rails-upgrade/SKILL.md) | Analyze Rails apps and provide upgrade assessments |
| [skill-scanner](.archived/skills/ai-llm-agent-development/skill-scanner/SKILL.md) | Scan agent skills for security issues before adoption. Detects prompt injection, malicious code, excessive permissions, secret exposure, and supply chain risks. |
| [skill-seekers](.archived/skills/ai-llm-agent-development/skill-seekers/SKILL.md) | -Automatically convert documentation websites, GitHub repositories, and PDFs into Claude AI skills in minutes. |
| [skill-writer](.archived/skills/ai-llm-agent-development/skill-writer/SKILL.md) | Create and improve agent skills following the Agent Skills specification. Use when asked to create, write, or update skills. |
| [slack-automation](.archived/skills/ai-llm-agent-development/slack-automation/SKILL.md) | Automate Slack workspace operations including messaging, search, channel management, and reaction workflows through Composio's Slack toolkit. |
| [snowflake-development](.archived/skills/ai-llm-agent-development/snowflake-development/SKILL.md) | Comprehensive Snowflake development assistant covering SQL best practices, data pipeline design (Dynamic Tables, Streams, Tasks, Snowpipe), Cortex AI functions, Cortex Agents, Snowpark Python, dbt integration, performance tuning, and security hardening. |
| [social-orchestrator](.archived/skills/ai-llm-agent-development/social-orchestrator/SKILL.md) | Orquestrador unificado de canais sociais — coordena Instagram, Telegram e WhatsApp em um unico fluxo de trabalho. Publicacao cross-channel, metricas unificadas, reutilizacao de conteudo por formato, agendamento sincronizado e gestao centralizada de campanhas em todos os canais simultaneamente. |
| [solidity-security](.archived/skills/ai-llm-agent-development/solidity-security/SKILL.md) | Master smart contract security best practices, vulnerability prevention, and secure Solidity development patterns. |
| [spec-to-code-compliance](.archived/skills/ai-llm-agent-development/spec-to-code-compliance/SKILL.md) | Verifies code implements exactly what documentation specifies for blockchain audits. Use when comparing code against whitepapers, finding gaps between specs and implementation, or performing compliance checks for protocol implementations. |
| [square-automation](.archived/skills/ai-llm-agent-development/square-automation/SKILL.md) | Automate Square tasks via Rube MCP (Composio): payments, orders, invoices, locations. Always search tools first for current schemas. |
| [stability-ai](.archived/skills/ai-llm-agent-development/stability-ai/SKILL.md) | Geracao de imagens via Stability AI (SD3.5, Ultra, Core). Text-to-image, img2img, inpainting, upscale, remove-bg, search-replace. 15 estilos artisticos. |
| [startup-business-analyst-financial-projections](.archived/skills/ai-llm-agent-development/startup-business-analyst-financial-projections/SKILL.md) | Create detailed 3-5 year financial model with revenue, costs, cash |
| [steve-jobs](.archived/skills/ai-llm-agent-development/steve-jobs/SKILL.md) | Agente que simula Steve Jobs — cofundador da Apple, CEO da Pixar, fundador da NeXT, o maior designer de produtos tecnologicos da historia e o mais influente apresentador de produtos do mundo. |
| [stitch-ui-design](.archived/skills/ai-llm-agent-development/stitch-ui-design/SKILL.md) | Expert guidance for crafting effective prompts in Google Stitch, the AI-powered UI design tool by Google Labs. This skill helps create precise, actionable prompts that generate high-quality UI designs for web and mobile applications. |
| [subagent-driven-development](.archived/skills/ai-llm-agent-development/subagent-driven-development/SKILL.md) | Use when executing implementation plans with independent tasks in the current session |
| [task-intelligence](.archived/skills/ai-llm-agent-development/task-intelligence/SKILL.md) | Protocolo de Inteligência Pré-Tarefa — ativa TODOS os agentes relevantes do ecossistema ANTES de executar qualquer tarefa solicitada pelo usuário. |
| [tdd-orchestrator](.archived/skills/ai-llm-agent-development/tdd-orchestrator/SKILL.md) | Master TDD orchestrator specializing in red-green-refactor discipline, multi-agent workflow coordination, and comprehensive test-driven development practices. |
| [tdd-workflow](.archived/skills/ai-llm-agent-development/tdd-workflow/SKILL.md) | Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle. |
| [tdd-workflows-tdd-green](.archived/skills/ai-llm-agent-development/tdd-workflows-tdd-green/SKILL.md) | Implement the minimal code needed to make failing tests pass in the TDD green phase. |
| [tdd-workflows-tdd-red](.archived/skills/ai-llm-agent-development/tdd-workflows-tdd-red/SKILL.md) | Generate failing tests for the TDD red phase to define expected behavior and edge cases. |
| [team-collaboration-issue](.archived/skills/ai-llm-agent-development/team-collaboration-issue/SKILL.md) | You are a GitHub issue resolution expert specializing in systematic bug investigation, feature implementation, and collaborative development workflows. Your expertise spans issue triage, root cause an |
| [team-collaboration-standup-notes](.archived/skills/ai-llm-agent-development/team-collaboration-standup-notes/SKILL.md) | You are an expert team communication specialist focused on async-first standup practices, AI-assisted note generation from commit history, and effective remote team coordination patterns. |
| [telegram-automation](.archived/skills/ai-llm-agent-development/telegram-automation/SKILL.md) | Automate Telegram tasks via Rube MCP (Composio): send messages, manage chats, share photos/documents, and handle bot commands. Always search tools first for current schemas. |
| [test-driven-development](.archived/skills/ai-llm-agent-development/test-driven-development/SKILL.md) | Use when implementing any feature or bugfix, before writing implementation code |
| [test-fixing](.archived/skills/ai-llm-agent-development/test-fixing/SKILL.md) | Systematically identify and fix all failing tests using smart grouping strategies. Use when explicitly asks to fix tests (\"fix these tests\", \"make tests pass\"), reports test failures (\"tests are failing\", \"test suite is broken\"), or completes implementation and wants tests passing. |
| [theme-factory](.archived/skills/ai-llm-agent-development/theme-factory/SKILL.md) | This skill provides a curated collection of professional font and color themes themes, each with carefully selected color palettes and font pairings. Once a theme is chosen, it can be applied to any artifact. |
| [tiktok-automation](.archived/skills/ai-llm-agent-development/tiktok-automation/SKILL.md) | Automate TikTok tasks via Rube MCP (Composio): upload/publish videos, post photos, manage content, and view user profiles/stats. Always search tools first for current schemas. |
| [todoist-automation](.archived/skills/ai-llm-agent-development/todoist-automation/SKILL.md) | Automate Todoist task management, projects, sections, filtering, and bulk operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [tool-use-guardian](.archived/skills/ai-llm-agent-development/tool-use-guardian/SKILL.md) | FREE — Intelligent tool-call reliability wrapper. Monitors, retries, fixes, and learns from tool failures. Auto-recovers from truncated JSON, timeouts, rate limits, and mid-chain failures. |
| [trello-automation](.archived/skills/ai-llm-agent-development/trello-automation/SKILL.md) | Automate Trello boards, cards, and workflows via Rube MCP (Composio). Create cards, manage lists, assign members, and search across boards programmatically. |
| [twitter-automation](.archived/skills/ai-llm-agent-development/twitter-automation/SKILL.md) | Automate Twitter/X tasks via Rube MCP (Composio): posts, search, users, bookmarks, lists, media. Always search tools first for current schemas. |
| [ui-skills](.archived/skills/ai-llm-agent-development/ui-skills/SKILL.md) | Opinionated, evolving constraints to guide agents when building interfaces |
| [unit-testing-test-generate](.archived/skills/ai-llm-agent-development/unit-testing-test-generate/SKILL.md) | Generate comprehensive, maintainable unit tests across languages with strong coverage and edge case focus. |
| [vector-database-engineer](.archived/skills/ai-llm-agent-development/vector-database-engineer/SKILL.md) | Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similar |
| [vercel-automation](.archived/skills/ai-llm-agent-development/vercel-automation/SKILL.md) | Automate Vercel tasks via Rube MCP (Composio): manage deployments, domains, DNS, env vars, projects, and teams. Always search tools first for current schemas. |
| [verification-before-completion](.archived/skills/ai-llm-agent-development/verification-before-completion/SKILL.md) | Claiming work is complete without verification is dishonesty, not efficiency. Use when ANY variation of success/completion claims, ANY expression of satisfaction, or ANY positive statement about work state. |
| [vibe-code-auditor](.archived/skills/ai-llm-agent-development/vibe-code-auditor/SKILL.md) | Audit rapidly generated or AI-produced code for structural flaws, fragility, and production risks. |
| [vibers-code-review](.archived/skills/ai-llm-agent-development/vibers-code-review/SKILL.md) | Human review workflow for AI-generated GitHub projects with spec-based feedback, security review, and follow-up PRs from the Vibers service. |
| [videodb-skills](.archived/skills/ai-llm-agent-development/videodb-skills/SKILL.md) | Upload, stream, search, edit, transcribe, and generate AI video and audio using the VideoDB SDK. |
| [voice-agents](.archived/skills/ai-llm-agent-development/voice-agents/SKILL.md) | You are a voice AI architect who has shipped production voice agents handling millions of calls. You understand the physics of latency - every component adds milliseconds, and the sum determines whether conversations feel natural or awkward. |
| [voice-ai-development](.archived/skills/ai-llm-agent-development/voice-ai-development/SKILL.md) | You are an expert in building real-time voice applications. You think in terms of latency budgets, audio quality, and user experience. You know that voice apps feel magical when fast and broken when slow. |
| [voice-ai-engine-development](.archived/skills/ai-llm-agent-development/voice-ai-engine-development/SKILL.md) | Build real-time conversational AI voice engines using async worker pipelines, streaming transcription, LLM agents, and TTS synthesis with interrupt handling and multi-provider support |
| [vulnerability-scanner](.archived/skills/ai-llm-agent-development/vulnerability-scanner/SKILL.md) | Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization. |
| [warren-buffett](.archived/skills/ai-llm-agent-development/warren-buffett/SKILL.md) | Agente que simula Warren Buffett — o maior investidor do seculo XX e XXI, CEO da Berkshire Hathaway, discipulo de Benjamin Graham e socio intelectual de Charlie Munger. |
| [webflow-automation](.archived/skills/ai-llm-agent-development/webflow-automation/SKILL.md) | Automate Webflow CMS collections, site publishing, page management, asset uploads, and ecommerce orders via Rube MCP (Composio). Always search tools first for current schemas. |
| [whatsapp-automation](.archived/skills/ai-llm-agent-development/whatsapp-automation/SKILL.md) | Automate WhatsApp Business tasks via Rube MCP (Composio): send messages, manage templates, upload media, and handle contacts. Always search tools first for current schemas. |
| [wiki-changelog](.archived/skills/ai-llm-agent-development/wiki-changelog/SKILL.md) | Generate structured changelogs from git history. Use when user asks \"what changed recently\", \"generate a changelog\", \"summarize commits\" or user wants to understand recent development activity. |
| [wordpress-plugin-development](.archived/skills/ai-llm-agent-development/wordpress-plugin-development/SKILL.md) | WordPress plugin development workflow covering plugin architecture, hooks, admin interfaces, REST API, security best practices, and WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks. |
| [wordpress-woocommerce-development](.archived/skills/ai-llm-agent-development/wordpress-woocommerce-development/SKILL.md) | WooCommerce store development workflow covering store setup, payment integration, shipping configuration, customization, and WordPress 7.0 features: AI connectors, DataViews, and collaboration tools. |
| [workflow-automation](.archived/skills/ai-llm-agent-development/workflow-automation/SKILL.md) | You are a workflow automation architect who has seen both the promise and the pain of these platforms. You've migrated teams from brittle cron jobs to durable execution and watched their on-call burden drop by 80%. |
| [wrike-automation](.archived/skills/ai-llm-agent-development/wrike-automation/SKILL.md) | Automate Wrike project management via Rube MCP (Composio): create tasks/folders, manage projects, assign work, and track progress. Always search tools first for current schemas. |
| [writing-skills](.archived/skills/ai-llm-agent-development/writing-skills/SKILL.md) | Use when creating, updating, or improving agent skills. |
| [yann-lecun](.archived/skills/ai-llm-agent-development/yann-lecun/SKILL.md) | Agente que simula Yann LeCun — inventor das Convolutional Neural Networks, Chief AI Scientist da Meta, Prêmio Turing 2018. |
| [yann-lecun-debate](.archived/skills/ai-llm-agent-development/yann-lecun-debate/SKILL.md) | Sub-skill de debates e posições de Yann LeCun. Cobre críticas técnicas detalhadas aos LLMs, rivalidades intelectuais (LeCun vs Hinton, Sutskever, Russell, Yudkowsky, Bostrom), lista completa de rejeições a afirmações mainstream, posição sobre risco existencial de IA, e técnicas de debate ao vivo. |
| [yann-lecun-tecnico](.archived/skills/ai-llm-agent-development/yann-lecun-tecnico/SKILL.md) | Sub-skill técnica de Yann LeCun. Cobre CNNs, LeNet, backpropagation, JEPA (I-JEPA, V-JEPA, MC-JEPA), AMI (Advanced Machinery of Intelligence), Self-Supervised Learning (SimCLR, MAE, BYOL), Energy-Based Models (EBMs) e código PyTorch completo. |
| [yes-md](.archived/skills/ai-llm-agent-development/yes-md/SKILL.md) | 6-layer AI governance: safety gates, evidence-based debugging, anti-slack detection, and machine-enforced hooks. Makes AI safe, thorough, and honest. |
| [youtube-automation](.archived/skills/ai-llm-agent-development/youtube-automation/SKILL.md) | Automate YouTube tasks via Rube MCP (Composio): upload videos, manage playlists, search content, get analytics, and handle comments. Always search tools first for current schemas. |
| [youtube-summarizer](.archived/skills/ai-llm-agent-development/youtube-summarizer/SKILL.md) | Extract transcripts from YouTube videos and generate comprehensive, detailed summaries using intelligent analysis frameworks |
| [zendesk-automation](.archived/skills/ai-llm-agent-development/zendesk-automation/SKILL.md) | Automate Zendesk tasks via Rube MCP (Composio): tickets, users, organizations, replies. Always search tools first for current schemas. |
| [zoho-crm-automation](.archived/skills/ai-llm-agent-development/zoho-crm-automation/SKILL.md) | Automate Zoho CRM tasks via Rube MCP (Composio): create/update records, search contacts, manage leads, and convert leads. Always search tools first for current schemas. |
| [zoom-automation](.archived/skills/ai-llm-agent-development/zoom-automation/SKILL.md) | Automate Zoom meeting creation, management, recordings, webinars, and participant tracking via Rube MCP (Composio). Always search tools first for current schemas. |

</details>

### 🌐 Frontend Development

<details>
<summary><b>🌐 Frontend Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [00-andruia-consultant](.archived/skills/frontend-development/00-andruia-consultant/SKILL.md) | Arquitecto de Soluciones Principal y Consultor Tecnológico de Andru.ia. Diagnostica y traza la hoja de ruta óptima para proyectos de IA en español. |
| [10-andruia-skill-smith](.archived/skills/frontend-development/10-andruia-skill-smith/SKILL.md) | Ingeniero de Sistemas de Andru.ia. Diseña, redacta y despliega nuevas habilidades (skills) dentro del repositorio siguiendo el Estándar de Diamante. |
| [3d-web-experience](.archived/skills/frontend-development/3d-web-experience/SKILL.md) | You bring the third dimension to the web. You know when 3D enhances and when it's just showing off. You balance visual impact with performance. You make 3D accessible to users who've never touched a 3D app. You create moments of wonder without sacrificing usability. |
| [ab-test-setup](.archived/skills/frontend-development/ab-test-setup/SKILL.md) | Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness. |
| [algolia-search](.archived/skills/frontend-development/algolia-search/SKILL.md) | Expert patterns for Algolia search implementation, indexing strategies, React InstantSearch, and relevance tuning Use when: adding search to, algolia, instantsearch, search api, search functionality. |
| [android_ui_verification](.archived/skills/frontend-development/android_ui_verification/SKILL.md) | Automated end-to-end UI testing and verification on an Android Emulator using ADB. |
| [angular](.archived/skills/frontend-development/angular/SKILL.md) | Modern Angular (v20+) expert with deep knowledge of Signals, Standalone Components, Zoneless applications, SSR/Hydration, and reactive patterns. |
| [angular-ui-patterns](.archived/skills/frontend-development/angular-ui-patterns/SKILL.md) | Modern Angular UI patterns for loading states, error handling, and data display. Use when building UI components, handling async data, or managing component states. |
| [animejs-animation](.archived/skills/frontend-development/animejs-animation/SKILL.md) | Advanced JavaScript animation library skill for creating complex, high-performance web animations. |
| [antigravity-design-expert](.archived/skills/frontend-development/antigravity-design-expert/SKILL.md) | Core UI/UX engineering skill for building highly interactive, spatial, weightless, and glassmorphism-based web interfaces using GSAP and 3D CSS. |
| [antigravity-skill-orchestrator](.archived/skills/frontend-development/antigravity-skill-orchestrator/SKILL.md) | A meta-skill that understands task requirements, dynamically selects appropriate skills, tracks successful skill combinations using agent-memory-mcp, and prevents skill overuse for simple tasks. |
| [antigravity-workflows](.archived/skills/frontend-development/antigravity-workflows/SKILL.md) | Orchestrate multiple Antigravity skills through guided workflows for SaaS MVP delivery, security audits, AI agent builds, and browser QA. |
| [architecture](.archived/skills/frontend-development/architecture/SKILL.md) | Architectural decision-making framework. Requirements analysis, trade-off evaluation, ADR documentation. Use when making architecture decisions or analyzing system design. |
| [ask-questions-if-underspecified](.archived/skills/frontend-development/ask-questions-if-underspecified/SKILL.md) | Clarify requirements before implementing. Use when serious doubts arise. |
| [astro](.archived/skills/frontend-development/astro/SKILL.md) | Build content-focused websites with Astro — zero JS by default, islands architecture, multi-framework components, and Markdown/MDX support. |
| [attack-tree-construction](.archived/skills/frontend-development/attack-tree-construction/SKILL.md) | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders. |
| [avalonia-layout-zafiro](.archived/skills/frontend-development/avalonia-layout-zafiro/SKILL.md) | Guidelines for modern Avalonia UI layout using Zafiro.Avalonia, emphasizing shared styles, generic components, and avoiding XAML redundancy. |
| [avalonia-viewmodels-zafiro](.archived/skills/frontend-development/avalonia-viewmodels-zafiro/SKILL.md) | Optimal ViewModel and Wizard creation patterns for Avalonia using Zafiro and ReactiveUI. |
| [avalonia-zafiro-development](.archived/skills/frontend-development/avalonia-zafiro-development/SKILL.md) | Mandatory skills, conventions, and behavioral rules for Avalonia UI development using the Zafiro toolkit. |
| [awt-e2e-testing](.archived/skills/frontend-development/awt-e2e-testing/SKILL.md) | AI-powered E2E web testing — eyes and hands for AI coding tools. Declarative YAML scenarios, Playwright execution, visual matching (OpenCV + OCR), platform auto-detection (Flutter/React/Vue), learning DB. Install: npx skills add ksgisang/awt-skill --skill awt -g |
| [azure-ai-voicelive-dotnet](.archived/skills/frontend-development/azure-ai-voicelive-dotnet/SKILL.md) | Azure AI Voice Live SDK for .NET. Build real-time voice AI applications with bidirectional WebSocket communication. |
| [azure-ai-voicelive-py](.archived/skills/frontend-development/azure-ai-voicelive-py/SKILL.md) | Build real-time voice AI applications with bidirectional WebSocket communication. |
| [azure-ai-voicelive-ts](.archived/skills/frontend-development/azure-ai-voicelive-ts/SKILL.md) | Azure AI Voice Live SDK for JavaScript/TypeScript. Build real-time voice AI applications with bidirectional WebSocket communication. |
| [azure-messaging-webpubsub-java](.archived/skills/frontend-development/azure-messaging-webpubsub-java/SKILL.md) | Build real-time web applications with Azure Web PubSub SDK for Java. Use when implementing WebSocket-based messaging, live updates, chat applications, or server-to-client push notifications. |
| [baseline-ui](.archived/skills/frontend-development/baseline-ui/SKILL.md) | Validates animation durations, enforces typography scale, checks component accessibility, and prevents layout anti-patterns in Tailwind CSS projects. Use when building UI components, reviewing CSS utilities, styling React views, or enforcing design consistency. |
| [brand-guidelines-anthropic](.archived/skills/frontend-development/brand-guidelines-anthropic/SKILL.md) | To access Anthropic's official brand identity and style resources, use this skill. |
| [brand-guidelines-community](.archived/skills/frontend-development/brand-guidelines-community/SKILL.md) | To access Anthropic's official brand identity and style resources, use this skill. |
| [broken-authentication](.archived/skills/frontend-development/broken-authentication/SKILL.md) | Identify and exploit authentication and session management vulnerabilities in web applications. Broken authentication consistently ranks in the OWASP Top 10 and can lead to account takeover, identity theft, and unauthorized access to sensitive systems. |
| [browser-automation](.archived/skills/frontend-development/browser-automation/SKILL.md) | You are a browser automation expert who has debugged thousands of flaky tests and built scrapers that run for years without breaking. You've seen the evolution from Selenium to Puppeteer to Playwright and understand exactly when each tool shines. |
| [browser-extension-builder](.archived/skills/frontend-development/browser-extension-builder/SKILL.md) | You extend the browser to give users superpowers. You understand the unique constraints of extension development - permissions, security, store policies. You build extensions that people install and actually use daily. You know the difference between a toy and a tool. |
| [build](.archived/skills/frontend-development/build/SKILL.md) | build |
| [building-native-ui](.archived/skills/frontend-development/building-native-ui/SKILL.md) | Complete guide for building beautiful apps with Expo Router. Covers fundamentals, styling, components, navigation, animations, patterns, and native tabs. |
| [burp-suite-testing](.archived/skills/frontend-development/burp-suite-testing/SKILL.md) | Execute comprehensive web application security testing using Burp Suite's integrated toolset, including HTTP traffic interception and modification, request analysis and replay, automated vulnerability scanning, and manual testing workflows. |
| [business-analyst](.archived/skills/frontend-development/business-analyst/SKILL.md) | Master modern business analysis with AI-powered analytics, real-time dashboards, and data-driven insights. Build comprehensive KPI frameworks, predictive models, and strategic recommendations. |
| [cc-skill-coding-standards](.archived/skills/frontend-development/cc-skill-coding-standards/SKILL.md) | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development. |
| [cc-skill-frontend-patterns](.archived/skills/frontend-development/cc-skill-frontend-patterns/SKILL.md) | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| [cc-skill-project-guidelines-example](.archived/skills/frontend-development/cc-skill-project-guidelines-example/SKILL.md) | Project Guidelines Skill (Example) |
| [chat-widget](.archived/skills/frontend-development/chat-widget/SKILL.md) | Build a real-time support chat system with a floating widget for users and an admin dashboard for support staff. Use when the user wants live chat, customer support chat, real-time messaging, or in-app support. |
| [cirq](.archived/skills/frontend-development/cirq/SKILL.md) | Cirq is Google Quantum AI's open-source framework for designing, simulating, and running quantum circuits on quantum computers and simulators. |
| [claude-ally-health](.archived/skills/frontend-development/claude-ally-health/SKILL.md) | A health assistant skill for medical information analysis, symptom tracking, and wellness guidance. |
| [claude-code-guide](.archived/skills/frontend-development/claude-code-guide/SKILL.md) | To provide a comprehensive reference for configuring and using Claude Code (the agentic coding tool) to its full potential. This skill synthesizes best practices, configuration templates, and advanced usage patterns. |
| [claude-in-chrome-troubleshooting](.archived/skills/frontend-development/claude-in-chrome-troubleshooting/SKILL.md) | Diagnose and fix Claude in Chrome MCP extension connectivity issues. Use when mcp__claude-in-chrome__* tools fail, return "Browser extension is not connected", or behave erratically. |
| [competitive-landscape](.archived/skills/frontend-development/competitive-landscape/SKILL.md) | Comprehensive frameworks for analyzing competition, identifying differentiation opportunities, and developing winning market positioning strategies. |
| [context-agent](.archived/skills/frontend-development/context-agent/SKILL.md) | Agente de contexto para continuidade entre sessoes. Salva resumos, decisoes, tarefas pendentes e carrega briefing automatico na sessao seguinte. |
| [context7-auto-research](.archived/skills/frontend-development/context7-auto-research/SKILL.md) | Automatically fetch latest library/framework documentation for Claude Code via Context7 API. Use when you need up-to-date documentation for libraries and frameworks or asking about React, Next.js, Prisma, or any other popular library. |
| [data-quality-frameworks](.archived/skills/frontend-development/data-quality-frameworks/SKILL.md) | Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts. |
| [dbos-golang](.archived/skills/frontend-development/dbos-golang/SKILL.md) | Guide for building reliable, fault-tolerant Go applications with DBOS durable workflows. Use when adding DBOS to existing Go code, creating workflows and steps, or using queues for concurrency control. |
| [dbos-typescript](.archived/skills/frontend-development/dbos-typescript/SKILL.md) | Guide for building reliable, fault-tolerant TypeScript applications with DBOS durable workflows. Use when adding DBOS to existing TypeScript code, creating workflows and steps, or using queues for concurrency control. |
| [dbt-transformation-patterns](.archived/skills/frontend-development/dbt-transformation-patterns/SKILL.md) | Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing. |
| [defuddle](.archived/skills/frontend-development/defuddle/SKILL.md) | Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page. |
| [discord-automation](.archived/skills/frontend-development/discord-automation/SKILL.md) | Automate Discord tasks via Rube MCP (Composio): messages, channels, roles, webhooks, reactions. Always search tools first for current schemas. |
| [django-pro](.archived/skills/frontend-development/django-pro/SKILL.md) | Master Django 5.x with async views, DRF, Celery, and Django Channels. Build scalable web applications with proper architecture, testing, and deployment. |
| [doc-coauthoring](.archived/skills/frontend-development/doc-coauthoring/SKILL.md) | This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing. |
| [electron-development](.archived/skills/frontend-development/electron-development/SKILL.md) | Master Electron desktop app development with secure IPC, contextIsolation, preload scripts, multi-process architecture, electron-builder packaging, code signing, and auto-update. |
| [embedding-strategies](.archived/skills/frontend-development/embedding-strategies/SKILL.md) | Guide to selecting and optimizing embedding models for vector search applications. |
| [evaluation](.archived/skills/frontend-development/evaluation/SKILL.md) | Build evaluation frameworks for agent systems. Use when testing agent performance systematically, validating context engineering choices, or measuring improvements over time. |
| [expo-dev-client](.archived/skills/frontend-development/expo-dev-client/SKILL.md) | Build and distribute Expo development clients locally or via TestFlight |
| [expo-tailwind-setup](.archived/skills/frontend-development/expo-tailwind-setup/SKILL.md) | Set up Tailwind CSS v4 in Expo with react-native-css and NativeWind v5 for universal styling |
| [expo-ui-jetpack-compose](.archived/skills/frontend-development/expo-ui-jetpack-compose/SKILL.md) | expo-ui-jetpack-compose |
| [expo-ui-swift-ui](.archived/skills/frontend-development/expo-ui-swift-ui/SKILL.md) | expo-ui-swift-ui |
| [ffuf-claude-skill](.archived/skills/frontend-development/ffuf-claude-skill/SKILL.md) | Web fuzzing with ffuf |
| [ffuf-web-fuzzing](.archived/skills/frontend-development/ffuf-web-fuzzing/SKILL.md) | Expert guidance for ffuf web fuzzing during penetration testing, including authenticated fuzzing with raw requests, auto-calibration, and result analysis |
| [firecrawl-scraper](.archived/skills/frontend-development/firecrawl-scraper/SKILL.md) | Deep web scraping, screenshots, PDF parsing, and website crawling using Firecrawl API. Use when you need deep content extraction from web pages, page interaction is required (clicking, scrolling, etc.), or you want screenshots or PDF parsing. |
| [fixing-motion-performance](.archived/skills/frontend-development/fixing-motion-performance/SKILL.md) | Audit and fix animation performance issues including layout thrashing, compositor properties, scroll-linked motion, and blur effects. Use when animations stutter, transitions jank, or reviewing CSS/JS animation performance. |
| [fp-option-ref](.archived/skills/frontend-development/fp-option-ref/SKILL.md) | Quick reference for Option type. Use when user needs to handle nullable values, optional data, or wants to avoid null checks. |
| [fp-react](.archived/skills/frontend-development/fp-react/SKILL.md) | Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Works with React 18/19, Next.js 14/15. |
| [fp-refactor](.archived/skills/frontend-development/fp-refactor/SKILL.md) | Comprehensive guide for refactoring imperative TypeScript code to fp-ts functional patterns |
| [fp-ts-react](.archived/skills/frontend-development/fp-ts-react/SKILL.md) | Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Use when building React apps with functional programming patterns. Works with React 18/19, Next.js 14/15. |
| [framework-migration-code-migrate](.archived/skills/frontend-development/framework-migration-code-migrate/SKILL.md) | You are a code migration expert specializing in transitioning codebases between frameworks, languages, versions, and platforms. Generate comprehensive migration plans, automated migration scripts, and |
| [framework-migration-deps-upgrade](.archived/skills/frontend-development/framework-migration-deps-upgrade/SKILL.md) | You are a dependency management expert specializing in safe, incremental upgrades of project dependencies. Plan and execute dependency updates with minimal risk, proper testing, and clear migration pa |
| [framework-migration-legacy-modernize](.archived/skills/frontend-development/framework-migration-legacy-modernize/SKILL.md) | Orchestrate a comprehensive legacy system modernization using the strangler fig pattern, enabling gradual replacement of outdated components while maintaining continuous business operations through ex |
| [frontend-developer](.archived/skills/frontend-development/frontend-developer/SKILL.md) | Build React components, implement responsive layouts, and handle client-side state management. Masters React 19, Next.js 15, and modern frontend architecture. |
| [frontend-mobile-development-component-scaffold](.archived/skills/frontend-development/frontend-mobile-development-component-scaffold/SKILL.md) | You are a React component architecture expert specializing in scaffolding production-ready, accessible, and performant components. Generate complete component implementations with TypeScript, tests, s |
| [frontend-mobile-security-xss-scan](.archived/skills/frontend-development/frontend-mobile-security-xss-scan/SKILL.md) | You are a frontend security specialist focusing on Cross-Site Scripting (XSS) vulnerability detection and prevention. Analyze React, Vue, Angular, and vanilla JavaScript code to identify injection poi |
| [frontend-security-coder](.archived/skills/frontend-development/frontend-security-coder/SKILL.md) | Expert in secure frontend coding practices specializing in XSS prevention, output sanitization, and client-side security patterns. |
| [frontend-slides](.archived/skills/frontend-development/frontend-slides/SKILL.md) | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. |
| [frontend-ui-dark-ts](.archived/skills/frontend-development/frontend-ui-dark-ts/SKILL.md) | A modern dark-themed React UI system using Tailwind CSS and Framer Motion. Designed for dashboards, admin panels, and data-rich applications with glassmorphism effects and tasteful animations. |
| [gdpr-data-handling](.archived/skills/frontend-development/gdpr-data-handling/SKILL.md) | Practical implementation guide for GDPR-compliant data processing, consent management, and privacy controls. |
| [go-rod-master](.archived/skills/frontend-development/go-rod-master/SKILL.md) | Comprehensive guide for browser automation and web scraping with go-rod (Chrome DevTools Protocol) including stealth anti-bot-detection patterns. |
| [grpc-golang](.archived/skills/frontend-development/grpc-golang/SKILL.md) | Build production-ready gRPC services in Go with mTLS, streaming, and observability. Use when designing Protobuf contracts with Buf or implementing secure service-to-service transport. |
| [hig-components-dialogs](.archived/skills/frontend-development/hig-components-dialogs/SKILL.md) | Apple HIG guidance for presentation components including alerts, action sheets, popovers, sheets, and digit entry views. |
| [hig-components-search](.archived/skills/frontend-development/hig-components-search/SKILL.md) | Apple HIG guidance for navigation-related components including search fields, page controls, and path controls. |
| [hig-components-status](.archived/skills/frontend-development/hig-components-status/SKILL.md) | Apple HIG guidance for status and progress UI components including progress indicators, status bars, and activity rings. |
| [hono](.archived/skills/frontend-development/hono/SKILL.md) | Build ultra-fast web APIs and full-stack apps with Hono — runs on Cloudflare Workers, Deno, Bun, Node.js, and any WinterCG-compatible runtime. |
| [javascript-pro](.archived/skills/frontend-development/javascript-pro/SKILL.md) | Master modern JavaScript with ES6+, async patterns, and Node.js APIs. Handles promises, event loops, and browser/Node compatibility. |
| [javascript-testing-patterns](.archived/skills/frontend-development/javascript-testing-patterns/SKILL.md) | Comprehensive guide for implementing robust testing strategies in JavaScript/TypeScript applications using modern testing frameworks and best practices. |
| [k6-load-testing](.archived/skills/frontend-development/k6-load-testing/SKILL.md) | Comprehensive k6 load testing skill for API, browser, and scalability testing. Write realistic load scenarios, analyze results, and integrate with CI/CD. |
| [landing-page-generator](.archived/skills/frontend-development/landing-page-generator/SKILL.md) | Generates high-converting Next.js/React landing pages with Tailwind CSS. Uses PAS, AIDA, and BAB frameworks for optimized copy/components (Heroes, Features, Pricing). Focuses on Core Web Vitals/SEO. |
| [legacy-modernizer](.archived/skills/frontend-development/legacy-modernizer/SKILL.md) | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, dependency updates, and backward compatibility. |
| [macos-menubar-tuist-app](.archived/skills/frontend-development/macos-menubar-tuist-app/SKILL.md) | Build, refactor, or review SwiftUI macOS menubar apps that use Tuist. |
| [macos-spm-app-packaging](.archived/skills/frontend-development/macos-spm-app-packaging/SKILL.md) | Scaffold, build, sign, and package SwiftPM macOS apps without Xcode projects. |
| [magic-ui-generator](.archived/skills/frontend-development/magic-ui-generator/SKILL.md) | Utilizes Magic by 21st.dev to generate, compare, and integrate multiple production-ready UI component variations. |
| [makepad-skills](.archived/skills/frontend-development/makepad-skills/SKILL.md) | Makepad UI development skills for Rust apps: setup, patterns, shaders, packaging, and troubleshooting. |
| [matematico-tao](.archived/skills/frontend-development/matematico-tao/SKILL.md) | Matemático ultra-avançado inspirado em Terence Tao. Análise rigorosa de código e arquitetura com teoria matemática profunda: teoria da informação, teoria dos grafos, complexidade computacional, álgebra linear, análise estocástica, teoria das categorias, probabilidade bayesiana e lógica formal. |
| [memory-forensics](.archived/skills/frontend-development/memory-forensics/SKILL.md) | Comprehensive techniques for acquiring, analyzing, and extracting artifacts from memory dumps for incident response and malware analysis. |
| [meta-skills-guide](.archived/skills/frontend-development/meta-skills-guide/SKILL.md) | Meta Skills Guide |
| [metasploit-framework](.archived/skills/frontend-development/metasploit-framework/SKILL.md) | ⚠️ AUTHORIZED USE ONLY > This skill is for educational purposes or authorized security assessments only. > You must have explicit, written permission from the system owner before using this tool. > Misuse of this tool is illegal and strictly prohibited. |
| [ml-engineer](.archived/skills/frontend-development/ml-engineer/SKILL.md) | Build production ML systems with PyTorch 2.x, TensorFlow, and modern ML frameworks. Implements model serving, feature engineering, A/B testing, and monitoring. |
| [mobile-security-coder](.archived/skills/frontend-development/mobile-security-coder/SKILL.md) | Expert in secure mobile coding practices specializing in input validation, WebView security, and mobile-specific security patterns. |
| [monorepo-management](.archived/skills/frontend-development/monorepo-management/SKILL.md) | Build efficient, scalable monorepos that enable code sharing, consistent tooling, and atomic changes across multiple packages and applications. |
| [moodle-external-api-development](.archived/skills/frontend-development/moodle-external-api-development/SKILL.md) | This skill guides you through creating custom external web service APIs for Moodle LMS, following Moodle's external API framework and coding standards. |
| [multi-platform-apps-multi-platform](.archived/skills/frontend-development/multi-platform-apps-multi-platform/SKILL.md) | Build and deploy the same feature consistently across web, mobile, and desktop platforms using API-first architecture and parallel implementation strategies. |
| [native-data-fetching](.archived/skills/frontend-development/native-data-fetching/SKILL.md) | Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, React Query, SWR, error handling, caching, offline support, and Expo Router data loaders (useLoaderData). |
| [nextjs-app-router-patterns](.archived/skills/frontend-development/nextjs-app-router-patterns/SKILL.md) | Comprehensive patterns for Next.js 14+ App Router architecture, Server Components, and modern full-stack React development. |
| [nodejs-backend-patterns](.archived/skills/frontend-development/nodejs-backend-patterns/SKILL.md) | Comprehensive guidance for building scalable, maintainable, and production-ready Node.js backend applications with modern frameworks, architectural patterns, and best practices. |
| [nodejs-best-practices](.archived/skills/frontend-development/nodejs-best-practices/SKILL.md) | Node.js development principles and decision-making. Framework selection, async patterns, security, and architecture. Teaches thinking, not copying. |
| [notebooklm](.archived/skills/frontend-development/notebooklm/SKILL.md) | Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes. |
| [nx-workspace-patterns](.archived/skills/frontend-development/nx-workspace-patterns/SKILL.md) | Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affected commands. |
| [obsidian-clipper-template-creator](.archived/skills/frontend-development/obsidian-clipper-template-creator/SKILL.md) | Guide for creating templates for the Obsidian Web Clipper. Use when you want to create a new clipping template, understand available variables, or format clipped content. |
| [odoo-accounting-setup](.archived/skills/frontend-development/odoo-accounting-setup/SKILL.md) | Expert guide for configuring Odoo Accounting: chart of accounts, journals, fiscal positions, taxes, payment terms, and bank reconciliation. |
| [odoo-automated-tests](.archived/skills/frontend-development/odoo-automated-tests/SKILL.md) | Write and run Odoo automated tests using TransactionCase, HttpCase, and browser tour tests. Covers test data setup, mocking, and CI integration. |
| [odoo-ecommerce-configurator](.archived/skills/frontend-development/odoo-ecommerce-configurator/SKILL.md) | Expert guide for Odoo eCommerce and Website: product catalog, payment providers, shipping methods, SEO, and order-to-fulfillment workflow. |
| [odoo-edi-connector](.archived/skills/frontend-development/odoo-edi-connector/SKILL.md) | Guide for implementing EDI (Electronic Data Interchange) with Odoo: X12, EDIFACT document mapping, partner onboarding, and automated order processing. |
| [odoo-hr-payroll-setup](.archived/skills/frontend-development/odoo-hr-payroll-setup/SKILL.md) | Expert guide for Odoo HR and Payroll: salary structures, payslip rules, leave policies, employee contracts, and payroll journal entries. |
| [odoo-inventory-optimizer](.archived/skills/frontend-development/odoo-inventory-optimizer/SKILL.md) | Expert guide for Odoo Inventory: stock valuation (FIFO/AVCO), reordering rules, putaway strategies, routes, and multi-warehouse configuration. |
| [odoo-manufacturing-advisor](.archived/skills/frontend-development/odoo-manufacturing-advisor/SKILL.md) | Expert guide for Odoo Manufacturing: Bills of Materials (BoM), Work Centers, routings, MRP planning, and production order workflows. |
| [odoo-module-developer](.archived/skills/frontend-development/odoo-module-developer/SKILL.md) | Expert guide for creating custom Odoo modules. Covers __manifest__.py, model inheritance, ORM patterns, and module structure best practices. |
| [odoo-project-timesheet](.archived/skills/frontend-development/odoo-project-timesheet/SKILL.md) | Expert guide for Odoo Project and Timesheets: task stages, billable time tracking, timesheet approval, budget alerts, and invoicing from timesheets. |
| [odoo-purchase-workflow](.archived/skills/frontend-development/odoo-purchase-workflow/SKILL.md) | Expert guide for Odoo Purchase: RFQ → PO → Receipt → Vendor Bill workflow, purchase agreements, vendor price lists, and 3-way matching. |
| [odoo-sales-crm-expert](.archived/skills/frontend-development/odoo-sales-crm-expert/SKILL.md) | Expert guide for Odoo Sales and CRM: pipeline stages, quotation templates, pricelists, sales teams, lead scoring, and forecasting. |
| [on-call-handoff-patterns](.archived/skills/frontend-development/on-call-handoff-patterns/SKILL.md) | Effective patterns for on-call shift transitions, ensuring continuity, context transfer, and reliable incident response across shifts. |
| [onboarding-cro](.archived/skills/frontend-development/onboarding-cro/SKILL.md) | You are an expert in user onboarding and activation. Your goal is to help users reach their \"aha moment\" as quickly as possible and establish habits that lead to long-term retention. |
| [pentest-commands](.archived/skills/frontend-development/pentest-commands/SKILL.md) | Provide a comprehensive command reference for penetration testing tools including network scanning, exploitation, password cracking, and web application testing. Enable quick command lookup during security assessments. |
| [postmortem-writing](.archived/skills/frontend-development/postmortem-writing/SKILL.md) | Comprehensive guide to writing effective, blameless postmortems that drive organizational learning and prevent incident recurrence. |
| [progressive-web-app](.archived/skills/frontend-development/progressive-web-app/SKILL.md) | Build Progressive Web Apps (PWAs) with offline support, installability, and caching strategies. Trigger whenever the user mentions PWA, service workers, web app manifests, Workbox, 'add to home screen', or wants their web app to work offline, feel native, or be installable. |
| [prometheus-configuration](.archived/skills/frontend-development/prometheus-configuration/SKILL.md) | Complete guide to Prometheus setup, metric collection, scrape configuration, and recording rules. |
| [python-patterns](.archived/skills/frontend-development/python-patterns/SKILL.md) | Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying. |
| [qiskit](.archived/skills/frontend-development/qiskit/SKILL.md) | Qiskit is the world's most popular open-source quantum computing framework with 13M+ downloads. Build quantum circuits, optimize for hardware, execute on simulators or real quantum computers, and analyze results. Supports IBM Quantum (100+ qubit systems), IonQ, Amazon Braket, and other providers. |
| [react-best-practices](.archived/skills/frontend-development/react-best-practices/SKILL.md) | Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel. Use when writing new React components or Next.js pages, implementing data fetching (client or server-side), or reviewing code for performance issues. |
| [react-component-performance](.archived/skills/frontend-development/react-component-performance/SKILL.md) | Diagnose slow React components and suggest targeted performance fixes. |
| [react-flow-architect](.archived/skills/frontend-development/react-flow-architect/SKILL.md) | Build production-ready ReactFlow applications with hierarchical navigation, performance optimization, and advanced state management. |
| [react-flow-node-ts](.archived/skills/frontend-development/react-flow-node-ts/SKILL.md) | Create React Flow node components following established patterns with proper TypeScript types and store integration. |
| [react-modernization](.archived/skills/frontend-development/react-modernization/SKILL.md) | Master React version upgrades, class to hooks migration, concurrent features adoption, and codemods for automated transformation. |
| [react-native-architecture](.archived/skills/frontend-development/react-native-architecture/SKILL.md) | Production-ready patterns for React Native development with Expo, including navigation, state management, native modules, and offline-first architecture. |
| [react-nextjs-development](.archived/skills/frontend-development/react-nextjs-development/SKILL.md) | React and Next.js 14+ application development with App Router, Server Components, TypeScript, Tailwind CSS, and modern frontend patterns. |
| [react-patterns](.archived/skills/frontend-development/react-patterns/SKILL.md) | Modern React patterns and principles. Hooks, composition, performance, TypeScript best practices. |
| [react-state-management](.archived/skills/frontend-development/react-state-management/SKILL.md) | Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions. |
| [react-ui-patterns](.archived/skills/frontend-development/react-ui-patterns/SKILL.md) | Modern React UI patterns for loading states, error handling, and data fetching. Use when building UI components, handling async data, or managing UI states. |
| [remotion-best-practices](.archived/skills/frontend-development/remotion-best-practices/SKILL.md) | Best practices for Remotion - Video creation in React |
| [requesting-code-review](.archived/skills/frontend-development/requesting-code-review/SKILL.md) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| [saas-mvp-launcher](.archived/skills/frontend-development/saas-mvp-launcher/SKILL.md) | Use when planning or building a SaaS MVP from scratch. Provides a structured roadmap covering tech stack, architecture, auth, payments, and launch checklist. |
| [scanning-tools](.archived/skills/frontend-development/scanning-tools/SKILL.md) | Master essential security scanning tools for network discovery, vulnerability assessment, web application testing, wireless security, and compliance validation. This skill covers tool selection, configuration, and practical usage across different scanning categories. |
| [screen-reader-testing](.archived/skills/frontend-development/screen-reader-testing/SKILL.md) | Practical guide to testing web applications with screen readers for comprehensive accessibility validation. |
| [search-specialist](.archived/skills/frontend-development/search-specialist/SKILL.md) | Expert web researcher using advanced search techniques and |
| [security-bluebook-builder](.archived/skills/frontend-development/security-bluebook-builder/SKILL.md) | Build a minimal but real security policy for sensitive apps. The output is a single, coherent Blue Book document using MUST/SHOULD/CAN language, with explicit assumptions, scope, and security gates. |
| [security-requirement-extraction](.archived/skills/frontend-development/security-requirement-extraction/SKILL.md) | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases. |
| [senior-frontend](.archived/skills/frontend-development/senior-frontend/SKILL.md) | Frontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. Use when building React components, optimizing Next.js performance, analyzing bundle sizes, scaffolding frontend projects, implementing accessibility, or reviewing frontend code quality. |
| [seo-authority-builder](.archived/skills/frontend-development/seo-authority-builder/SKILL.md) | Analyzes content for E-E-A-T signals and suggests improvements to |
| [seo-content-auditor](.archived/skills/frontend-development/seo-content-auditor/SKILL.md) | Analyzes provided content for quality, E-E-A-T signals, and SEO best practices. Scores content and provides improvement recommendations based on established guidelines. |
| [seo-fundamentals](.archived/skills/frontend-development/seo-fundamentals/SKILL.md) | Core principles of SEO including E-E-A-T, Core Web Vitals, technical foundations, content quality, and how modern search engines evaluate pages. |
| [service-mesh-observability](.archived/skills/frontend-development/service-mesh-observability/SKILL.md) | Complete guide to observability patterns for Istio, Linkerd, and service mesh deployments. |
| [shader-programming-glsl](.archived/skills/frontend-development/shader-programming-glsl/SKILL.md) | Expert guide for writing efficient GLSL shaders (Vertex/Fragment) for web and game engines, covering syntax, uniforms, and common effects. |
| [shopify-apps](.archived/skills/frontend-development/shopify-apps/SKILL.md) | Modern Shopify app template with React Router |
| [shopify-development](.archived/skills/frontend-development/shopify-development/SKILL.md) | Build Shopify apps, extensions, themes using GraphQL Admin API, Shopify CLI, Polaris UI, and Liquid. |
| [skill-developer](.archived/skills/frontend-development/skill-developer/SKILL.md) | Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern. |
| [slack-bot-builder](.archived/skills/frontend-development/slack-bot-builder/SKILL.md) | The Bolt framework is Slack's recommended approach for building apps. It handles authentication, event routing, request verification, and HTTP request processing so you can focus on app logic. |
| [slo-implementation](.archived/skills/frontend-development/slo-implementation/SKILL.md) | Framework for defining and implementing Service Level Indicators (SLIs), Service Level Objectives (SLOs), and error budgets. |
| [social-content](.archived/skills/frontend-development/social-content/SKILL.md) | You are an expert social media strategist with direct access to a scheduling platform that publishes to all major social networks. Your goal is to help create engaging content that builds audience, drives engagement, and supports business goals. |
| [spline-3d-integration](.archived/skills/frontend-development/spline-3d-integration/SKILL.md) | Use when adding interactive 3D scenes from Spline.design to web projects, including React embedding and runtime control API. |
| [startup-metrics-framework](.archived/skills/frontend-development/startup-metrics-framework/SKILL.md) | Comprehensive guide to tracking, calculating, and optimizing key performance metrics for different startup business models from seed through Series A. |
| [stitch-loop](.archived/skills/frontend-development/stitch-loop/SKILL.md) | Teaches agents to iteratively build websites using Stitch with an autonomous baton-passing loop pattern |
| [sveltekit](.archived/skills/frontend-development/sveltekit/SKILL.md) | Build full-stack web applications with SvelteKit — file-based routing, SSR, SSG, API routes, and form actions in one framework. |
| [swiftui-liquid-glass](.archived/skills/frontend-development/swiftui-liquid-glass/SKILL.md) | Implement or review SwiftUI Liquid Glass APIs with correct fallbacks and modifier order. |
| [swiftui-ui-patterns](.archived/skills/frontend-development/swiftui-ui-patterns/SKILL.md) | Apply proven SwiftUI UI patterns for navigation, sheets, async state, and reusable screens. |
| [swiftui-view-refactor](.archived/skills/frontend-development/swiftui-view-refactor/SKILL.md) | Refactor SwiftUI views into smaller components with stable, explicit data flow. |
| [tanstack-query-expert](.archived/skills/frontend-development/tanstack-query-expert/SKILL.md) | Expert in TanStack Query (React Query) — asynchronous state management. Covers data fetching, stale time configuration, mutations, optimistic updates, and Next.js App Router (SSR) integration. |
| [tavily-web](.archived/skills/frontend-development/tavily-web/SKILL.md) | Web search, content extraction, crawling, and research capabilities using Tavily API. Use when you need to search the web for current information, extracting content from URLs, or crawling websites. |
| [telegram-mini-app](.archived/skills/frontend-development/telegram-mini-app/SKILL.md) | You build apps where 800M+ Telegram users already are. You understand the Mini App ecosystem is exploding - games, DeFi, utilities, social apps. You know TON blockchain and how to monetize with crypto. You design for the Telegram UX paradigm, not traditional web. |
| [threejs-geometry](.archived/skills/frontend-development/threejs-geometry/SKILL.md) | Three.js geometry creation - built-in shapes, BufferGeometry, custom geometry, instancing. Use when creating 3D shapes, working with vertices, building custom meshes, or optimizing with instanced rendering. |
| [top-web-vulnerabilities](.archived/skills/frontend-development/top-web-vulnerabilities/SKILL.md) | Provide a comprehensive, structured reference for the 100 most critical web application vulnerabilities organized by category. This skill enables systematic vulnerability identification, impact assessment, and remediation guidance across the full spectrum of web security threats. |
| [trpc-fullstack](.archived/skills/frontend-development/trpc-fullstack/SKILL.md) | Build end-to-end type-safe APIs with tRPC — routers, procedures, middleware, subscriptions, and Next.js/React integration patterns. |
| [ui-ux-pro-max](.archived/skills/frontend-development/ui-ux-pro-max/SKILL.md) | Comprehensive design guide for web and mobile applications. Use when designing new UI components or pages, choosing color palettes and typography, or reviewing code for UX issues. |
| [using-neon](.archived/skills/frontend-development/using-neon/SKILL.md) | Neon is a serverless Postgres platform that separates compute and storage to offer autoscaling, branching, instant restore, and scale-to-zero. It's fully compatible with Postgres and works with any language, framework, or ORM that supports Postgres. |
| [using-superpowers](.archived/skills/frontend-development/using-superpowers/SKILL.md) | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions |
| [vercel-ai-sdk-expert](.archived/skills/frontend-development/vercel-ai-sdk-expert/SKILL.md) | Expert in the Vercel AI SDK. Covers Core API (generateText, streamText), UI hooks (useChat, useCompletion), tool calling, and streaming UI components with React and Next.js. |
| [wcag-audit-patterns](.archived/skills/frontend-development/wcag-audit-patterns/SKILL.md) | Comprehensive guide to auditing web content against WCAG 2.2 guidelines with actionable remediation strategies. |
| [web-artifacts-builder](.archived/skills/frontend-development/web-artifacts-builder/SKILL.md) | To build powerful frontend claude.ai artifacts, follow these steps: |
| [web-design-guidelines](.archived/skills/frontend-development/web-design-guidelines/SKILL.md) | Review files for compliance with Web Interface Guidelines. |
| [web-performance-optimization](.archived/skills/frontend-development/web-performance-optimization/SKILL.md) | Optimize website and web application performance including loading speed, Core Web Vitals, bundle size, caching strategies, and runtime performance |
| [web-scraper](.archived/skills/frontend-development/web-scraper/SKILL.md) | Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas web (tabelas, listas, precos). Paginacao, monitoramento e export CSV/JSON. |
| [webapp-testing](.archived/skills/frontend-development/webapp-testing/SKILL.md) | To test local web applications, write native Python Playwright scripts. |
| [writing-plans](.archived/skills/frontend-development/writing-plans/SKILL.md) | Use when you have a spec or requirements for a multi-step task, before touching code |
| [xss-html-injection](.archived/skills/frontend-development/xss-html-injection/SKILL.md) | Execute comprehensive client-side injection vulnerability assessments on web applications to identify XSS and HTML injection flaws, demonstrate exploitation techniques for session hijacking and credential theft, and validate input sanitization and output encoding mechanisms. |
| [zod-validation-expert](.archived/skills/frontend-development/zod-validation-expert/SKILL.md) | Expert in Zod — TypeScript-first schema validation. Covers parsing, custom errors, refinements, type inference, and integration with React Hook Form, Next.js, and tRPC. |

</details>

### ⚙️ Backend Development

<details>
<summary><b>⚙️ Backend Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [ad-creative](.archived/skills/backend-development/ad-creative/SKILL.md) | Create, iterate, and scale paid ad creative for Google Ads, Meta, LinkedIn, TikTok, and similar platforms. Use when generating headlines, descriptions, primary text, or large sets of ad variations for testing and performance optimization. |
| [agent-orchestration-multi-agent-optimize](.archived/skills/backend-development/agent-orchestration-multi-agent-optimize/SKILL.md) | Optimize multi-agent systems with coordinated profiling, workload distribution, and cost-aware orchestration. Use when improving agent performance, throughput, or reliability. |
| [android-jetpack-compose-expert](.archived/skills/backend-development/android-jetpack-compose-expert/SKILL.md) | Expert guidance for building modern Android UIs with Jetpack Compose, covering state management, navigation, performance, and Material Design 3. |
| [angular-best-practices](.archived/skills/backend-development/angular-best-practices/SKILL.md) | Angular performance optimization and best practices guide. Use when writing, reviewing, or refactoring Angular code for optimal performance, bundle size, and rendering efficiency. |
| [api-design-principles](.archived/skills/backend-development/api-design-principles/SKILL.md) | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers and stand the test of time. |
| [api-documentation-generator](.archived/skills/backend-development/api-documentation-generator/SKILL.md) | Generate comprehensive, developer-friendly API documentation from code, including endpoints, parameters, examples, and best practices |
| [api-endpoint-builder](.archived/skills/backend-development/api-endpoint-builder/SKILL.md) | Builds production-ready REST API endpoints with validation, error handling, authentication, and documentation. Follows best practices for security and scalability. |
| [api-fuzzing-bug-bounty](.archived/skills/backend-development/api-fuzzing-bug-bounty/SKILL.md) | Provide comprehensive techniques for testing REST, SOAP, and GraphQL APIs during bug bounty hunting and penetration testing engagements. Covers vulnerability discovery, authentication bypass, IDOR exploitation, and API-specific attack vectors. |
| [api-security-testing](.archived/skills/backend-development/api-security-testing/SKILL.md) | API security testing workflow for REST and GraphQL APIs covering authentication, authorization, rate limiting, input validation, and security best practices. |
| [api-testing-observability-api-mock](.archived/skills/backend-development/api-testing-observability-api-mock/SKILL.md) | You are an API mocking expert specializing in realistic mock services for development, testing, and demos. Design mocks that simulate real API behavior and enable parallel development. |
| [apify-audience-analysis](.archived/skills/backend-development/apify-audience-analysis/SKILL.md) | Understand audience demographics, preferences, behavior patterns, and engagement quality across Facebook, Instagram, YouTube, and TikTok. |
| [apify-brand-reputation-monitoring](.archived/skills/backend-development/apify-brand-reputation-monitoring/SKILL.md) | Scrape reviews, ratings, and brand mentions from multiple platforms using Apify Actors. |
| [apify-content-analytics](.archived/skills/backend-development/apify-content-analytics/SKILL.md) | Track engagement metrics, measure campaign ROI, and analyze content performance across Instagram, Facebook, YouTube, and TikTok. |
| [apify-influencer-discovery](.archived/skills/backend-development/apify-influencer-discovery/SKILL.md) | Find and evaluate influencers for brand partnerships, verify authenticity, and track collaboration performance across Instagram, Facebook, YouTube, and TikTok. |
| [apify-lead-generation](.archived/skills/backend-development/apify-lead-generation/SKILL.md) | Scrape leads from multiple platforms using Apify Actors. |
| [app-store-optimization](.archived/skills/backend-development/app-store-optimization/SKILL.md) | Complete App Store Optimization (ASO) toolkit for researching, optimizing, and tracking mobile app performance on Apple App Store and Google Play Store |
| [appdeploy](.archived/skills/backend-development/appdeploy/SKILL.md) | Deploy web apps with backend APIs, database, and file storage. Use when the user asks to deploy or publish a website or web app and wants a public URL. Uses HTTP API via curl. |
| [application-performance-performance-optimization](.archived/skills/backend-development/application-performance-performance-optimization/SKILL.md) | Optimize end-to-end application performance with profiling, observability, and backend/frontend tuning. Use when coordinating performance optimization across the stack. |
| [aws-secrets-rotation](.archived/skills/backend-development/aws-secrets-rotation/SKILL.md) | Automate AWS secrets rotation for RDS, API keys, and credentials |
| [backend-architect](.archived/skills/backend-development/backend-architect/SKILL.md) | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. |
| [backend-dev-guidelines](.archived/skills/backend-development/backend-dev-guidelines/SKILL.md) | You are a senior backend engineer operating production-grade services under strict architectural and reliability constraints. Use when routes, controllers, services, repositories, express middleware, or prisma database access. |
| [backend-development-feature-development](.archived/skills/backend-development/backend-development-feature-development/SKILL.md) | Orchestrate end-to-end backend feature development from requirements to deployment. Use when coordinating multi-phase feature delivery across teams and services. |
| [backend-security-coder](.archived/skills/backend-development/backend-security-coder/SKILL.md) | Expert in secure backend coding practices specializing in input validation, authentication, and API security. Use PROACTIVELY for backend security implementations or security code reviews. |
| [bazel-build-optimization](.archived/skills/backend-development/bazel-build-optimization/SKILL.md) | Optimize Bazel builds for large-scale monorepos. Use when configuring Bazel, implementing remote execution, or optimizing build performance for enterprise codebases. |
| [binary-analysis-patterns](.archived/skills/backend-development/binary-analysis-patterns/SKILL.md) | Comprehensive patterns and techniques for analyzing compiled binaries, understanding assembly code, and reconstructing program logic. |
| [biopython](.archived/skills/backend-development/biopython/SKILL.md) | Biopython is a comprehensive set of freely available Python tools for biological computation. It provides functionality for sequence manipulation, file I/O, database access, structural bioinformatics, phylogenetics, and many other bioinformatics tasks. |
| [cc-skill-backend-patterns](.archived/skills/backend-development/cc-skill-backend-patterns/SKILL.md) | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| [cc-skill-clickhouse-io](.archived/skills/backend-development/cc-skill-clickhouse-io/SKILL.md) | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. |
| [claude-monitor](.archived/skills/backend-development/claude-monitor/SKILL.md) | Monitor de performance do Claude Code e sistema local. Diagnostica lentidao, mede CPU/RAM/disco, verifica API latency e gera relatorios de saude do sistema. |
| [code-review-checklist](.archived/skills/backend-development/code-review-checklist/SKILL.md) | Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability |
| [comfyui-gateway](.archived/skills/backend-development/comfyui-gateway/SKILL.md) | REST API gateway for ComfyUI servers. Workflow management, job queuing, webhooks, caching, auth, rate limiting, and image delivery (URL + base64). |
| [conductor-revert](.archived/skills/backend-development/conductor-revert/SKILL.md) | Git-aware undo by logical work unit (track, phase, or task) |
| [convex](.archived/skills/backend-development/convex/SKILL.md) | Convex reactive backend expert: schema design, TypeScript functions, real-time subscriptions, auth, file storage, scheduling, and deployment. |
| [cqrs-implementation](.archived/skills/backend-development/cqrs-implementation/SKILL.md) | Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems. |
| [database-migration](.archived/skills/backend-development/database-migration/SKILL.md) | Master database schema and data migrations across ORMs (Sequelize, TypeORM, Prisma), including rollback strategies and zero-downtime deployments. |
| [database-optimizer](.archived/skills/backend-development/database-optimizer/SKILL.md) | Expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures. |
| [development](.archived/skills/backend-development/development/SKILL.md) | Comprehensive web, mobile, and backend development workflow bundling frontend, backend, full-stack, and mobile development skills for end-to-end application delivery. |
| [django-perf-review](.archived/skills/backend-development/django-perf-review/SKILL.md) | Django performance code review. Use when asked to "review Django performance", "find N+1 queries", "optimize Django", "check queryset performance", "database performance", "Django ORM issues", or audit Django code for performance problems. |
| [dotnet-architect](.archived/skills/backend-development/dotnet-architect/SKILL.md) | Expert .NET backend architect specializing in C#, ASP.NET Core, Entity Framework, Dapper, and enterprise application patterns. |
| [dotnet-backend](.archived/skills/backend-development/dotnet-backend/SKILL.md) | Build ASP.NET Core 8+ backend services with EF Core, auth, background jobs, and production API patterns. |
| [dotnet-backend-patterns](.archived/skills/backend-development/dotnet-backend-patterns/SKILL.md) | Master C#/.NET patterns for building production-grade APIs, MCP servers, and enterprise backends with modern best practices (2024/2025). |
| [drizzle-orm-expert](.archived/skills/backend-development/drizzle-orm-expert/SKILL.md) | Expert in Drizzle ORM for TypeScript — schema design, relational queries, migrations, and serverless database integration. Use when building type-safe database layers with Drizzle. |
| [elon-musk](.archived/skills/backend-development/elon-musk/SKILL.md) | Agente que simula Elon Musk com profundidade psicologica e comunicacional de alta fidelidade. Ativado para: \"fale como Elon\", \"simule Elon Musk\", \"o que Elon diria sobre X\", \"first principles thinking\", \"think like Elon\", roleplay/simulacao do personagem. |
| [exa-search](.archived/skills/backend-development/exa-search/SKILL.md) | Semantic search, similar content discovery, and structured research using Exa API. Use when you need semantic/embeddings-based search, finding similar content, or searching by category (company, people, research papers, etc.). |
| [expo-api-routes](.archived/skills/backend-development/expo-api-routes/SKILL.md) | Guidelines for creating API routes in Expo Router with EAS Hosting |
| [fal-platform](.archived/skills/backend-development/fal-platform/SKILL.md) | Platform APIs for model management, pricing, and usage tracking |
| [fastapi-pro](.archived/skills/backend-development/fastapi-pro/SKILL.md) | Build high-performance async APIs with FastAPI, SQLAlchemy 2.0, and Pydantic V2. Master microservices, WebSockets, and modern Python async patterns. |
| [fastapi-router-py](.archived/skills/backend-development/fastapi-router-py/SKILL.md) | Create FastAPI routers following established patterns with proper authentication, response models, and HTTP status codes. |
| [fastapi-templates](.archived/skills/backend-development/fastapi-templates/SKILL.md) | Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects. |
| [file-uploads](.archived/skills/backend-development/file-uploads/SKILL.md) | Careful about security and performance. Never trusts file extensions. Knows that large uploads need special handling. Prefers presigned URLs over server proxying. |
| [fp-async](.archived/skills/backend-development/fp-async/SKILL.md) | Practical async patterns using TaskEither - clean pipelines instead of try/catch hell, with real API examples |
| [fp-backend](.archived/skills/backend-development/fp-backend/SKILL.md) | Functional programming patterns for Node.js/Deno backend development using fp-ts, ReaderTaskEither, and functional dependency injection |
| [fp-taskeither-ref](.archived/skills/backend-development/fp-taskeither-ref/SKILL.md) | Quick reference for TaskEither. Use when user needs async error handling, API calls, or Promise-based operations that can fail. |
| [frontend-dev-guidelines](.archived/skills/backend-development/frontend-dev-guidelines/SKILL.md) | You are a senior frontend engineer operating under strict architectural and performance standards. Use when creating components or pages, adding new features, or fetching or mutating data. |
| [gemini-api-integration](.archived/skills/backend-development/gemini-api-integration/SKILL.md) | Use when integrating Google Gemini API into projects. Covers model selection, multimodal inputs, streaming, function calling, and production best practices. |
| [github](.archived/skills/backend-development/github/SKILL.md) | Use the `gh` CLI for issues, pull requests, Actions runs, and GitHub API queries. |
| [golang-pro](.archived/skills/backend-development/golang-pro/SKILL.md) | Master Go 1.21+ with modern patterns, advanced concurrency, performance optimization, and production-ready microservices. |
| [graphql](.archived/skills/backend-development/graphql/SKILL.md) | You're a developer who has built GraphQL APIs at scale. You've seen the N+1 query problem bring down production servers. You've watched clients craft deeply nested queries that took minutes to resolve. You know that GraphQL's power is also its danger. |
| [hr-pro](.archived/skills/backend-development/hr-pro/SKILL.md) | Professional, ethical HR partner for hiring, onboarding/offboarding, PTO and leave, performance, compliant policies, and employee relations. |
| [hugging-face-dataset-viewer](.archived/skills/backend-development/hugging-face-dataset-viewer/SKILL.md) | Use this skill for Hugging Face Dataset Viewer API workflows that fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs, and read size or statistics. |
| [hugging-face-evaluation](.archived/skills/backend-development/hugging-face-evaluation/SKILL.md) | Add and manage evaluation results in Hugging Face model cards. Supports extracting eval tables from README content, importing scores from Artificial Analysis API, and running custom model evaluations with vLLM/lighteval. Works with the model-index metadata format. |
| [hugging-face-tool-builder](.archived/skills/backend-development/hugging-face-tool-builder/SKILL.md) | Your purpose is now is to create reusable command line scripts and utilities for using the Hugging Face API, allowing chaining, piping and intermediate processing where helpful. You can access the API directly, as well as use the hf command line tool. |
| [hybrid-cloud-networking](.archived/skills/backend-development/hybrid-cloud-networking/SKILL.md) | Configure secure, high-performance connectivity between on-premises and cloud environments using VPN, Direct Connect, and ExpressRoute. |
| [julia-pro](.archived/skills/backend-development/julia-pro/SKILL.md) | Master Julia 1.10+ with modern features, performance optimization, multiple dispatch, and production-ready practices. |
| [laravel-expert](.archived/skills/backend-development/laravel-expert/SKILL.md) | Senior Laravel Engineer role for production-grade, maintainable, and idiomatic Laravel solutions. Focuses on clean architecture, security, performance, and modern standards (Laravel 10/11+). |
| [libreoffice-base](.archived/skills/backend-development/libreoffice-base/SKILL.md) | Database management, forms, reports, and data operations with LibreOffice Base. |
| [linux-troubleshooting](.archived/skills/backend-development/linux-troubleshooting/SKILL.md) | Linux system troubleshooting workflow for diagnosing and resolving system issues, performance problems, and service failures. |
| [mcp-builder](.archived/skills/backend-development/mcp-builder/SKILL.md) | Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks. |
| [mcp-builder-ms](.archived/skills/backend-development/mcp-builder-ms/SKILL.md) | Use this skill when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| [minecraft-bukkit-pro](.archived/skills/backend-development/minecraft-bukkit-pro/SKILL.md) | Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs. |
| [n8n-global-deploy](.archived/skills/backend-development/n8n-global-deploy/SKILL.md) | Validates JSON output and pushes it to http://localhost:5678/api/v1/workflows |
| [network-engineer](.archived/skills/backend-development/network-engineer/SKILL.md) | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization. |
| [obsidian-bases](.archived/skills/backend-development/obsidian-bases/SKILL.md) | Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian. |
| [odoo-migration-helper](.archived/skills/backend-development/odoo-migration-helper/SKILL.md) | Step-by-step guide for migrating Odoo custom modules between versions (v14→v15→v16→v17). Covers API changes, deprecated methods, and view migration. |
| [odoo-orm-expert](.archived/skills/backend-development/odoo-orm-expert/SKILL.md) | Master Odoo ORM patterns: search, browse, create, write, domain filters, computed fields, and performance-safe query techniques. |
| [odoo-performance-tuner](.archived/skills/backend-development/odoo-performance-tuner/SKILL.md) | Expert guide for diagnosing and fixing Odoo performance issues: slow queries, worker configuration, memory limits, PostgreSQL tuning, and profiling tools. |
| [odoo-rpc-api](.archived/skills/backend-development/odoo-rpc-api/SKILL.md) | Expert on Odoo's external JSON-RPC and XML-RPC APIs. Covers authentication, model calls, record CRUD, and real-world integration examples in Python, JavaScript, and curl. |
| [odoo-shopify-integration](.archived/skills/backend-development/odoo-shopify-integration/SKILL.md) | Connect Odoo with Shopify: sync products, inventory, orders, and customers using the Shopify API and Odoo's external API or connector modules. |
| [odoo-woocommerce-bridge](.archived/skills/backend-development/odoo-woocommerce-bridge/SKILL.md) | Sync Odoo with WooCommerce: products, inventory, orders, and customers via WooCommerce REST API and Odoo external API. |
| [page-cro](.archived/skills/backend-development/page-cro/SKILL.md) | Analyze and optimize individual pages for conversion performance. |
| [paid-ads](.archived/skills/backend-development/paid-ads/SKILL.md) | You are an expert performance marketer with direct access to ad platform accounts. Your goal is to help create, optimize, and scale paid advertising campaigns that drive efficient customer acquisition. |
| [performance-engineer](.archived/skills/backend-development/performance-engineer/SKILL.md) | Expert performance engineer specializing in modern observability, |
| [performance-optimizer](.archived/skills/backend-development/performance-optimizer/SKILL.md) | Identifies and fixes performance bottlenecks in code, databases, and APIs. Measures before and after to prove improvements. |
| [performance-profiling](.archived/skills/backend-development/performance-profiling/SKILL.md) | Performance profiling principles. Measurement, analysis, and optimization techniques. |
| [performance-testing-review-multi-agent-review](.archived/skills/backend-development/performance-testing-review-multi-agent-review/SKILL.md) | Use when working with performance testing review multi agent review |
| [postgres-best-practices](.archived/skills/backend-development/postgres-best-practices/SKILL.md) | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations. |
| [pubmed-database](.archived/skills/backend-development/pubmed-database/SKILL.md) | Direct REST API access to PubMed. Advanced Boolean/MeSH queries, E-utilities API, batch processing, citation management. For Python workflows, prefer biopython (Bio.Entrez). Use this for direct HTTP/REST work or custom API implementations. |
| [pydantic-models-py](.archived/skills/backend-development/pydantic-models-py/SKILL.md) | Create Pydantic models following the multi-model pattern for clean API contracts. |
| [python-fastapi-development](.archived/skills/backend-development/python-fastapi-development/SKILL.md) | Python FastAPI backend development with async patterns, SQLAlchemy, Pydantic, authentication, and production API patterns. |
| [python-performance-optimization](.archived/skills/backend-development/python-performance-optimization/SKILL.md) | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance. |
| [python-pro](.archived/skills/backend-development/python-pro/SKILL.md) | Master Python 3.12+ with modern features, async programming, performance optimization, and production-ready practices. Expert in the latest Python ecosystem including uv, ruff, pydantic, and FastAPI. |
| [receiving-code-review](.archived/skills/backend-development/receiving-code-review/SKILL.md) | Code review requires technical evaluation, not emotional performance. |
| [ruby-pro](.archived/skills/backend-development/ruby-pro/SKILL.md) | Write idiomatic Ruby code with metaprogramming, Rails patterns, and performance optimization. Specializes in Ruby on Rails, gem development, and testing frameworks. |
| [salesforce-development](.archived/skills/backend-development/salesforce-development/SKILL.md) | Use @wire decorator for reactive data binding with Lightning Data Service or Apex methods. @wire fits LWC's reactive architecture and enables Salesforce performance optimizations. |
| [scroll-experience](.archived/skills/backend-development/scroll-experience/SKILL.md) | You see scrolling as a narrative device, not just navigation. You create moments of delight as users scroll. You know when to use subtle animations and when to go cinematic. You balance performance with visual impact. You make websites feel like movies you control with your thumb. |
| [seo-audit](.archived/skills/backend-development/seo-audit/SKILL.md) | Diagnose and audit SEO issues affecting crawlability, indexation, rankings, and organic performance. |
| [similarity-search-patterns](.archived/skills/backend-development/similarity-search-patterns/SKILL.md) | Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance. |
| [swiftui-expert-skill](.archived/skills/backend-development/swiftui-expert-skill/SKILL.md) | Write, review, or improve SwiftUI code following best practices for state management, view composition, performance, and iOS 26+ Liquid Glass adoption. Use when building new SwiftUI features, refactoring existing views, reviewing code quality, or adopting modern SwiftUI patterns. |
| [swiftui-performance-audit](.archived/skills/backend-development/swiftui-performance-audit/SKILL.md) | Audit SwiftUI performance issues from code review and profiling evidence. |
| [telegram](.archived/skills/backend-development/telegram/SKILL.md) | Integracao completa com Telegram Bot API. Setup com BotFather, mensagens, webhooks, inline keyboards, grupos, canais. Boilerplates Node.js e Python. |
| [threejs-lighting](.archived/skills/backend-development/threejs-lighting/SKILL.md) | Three.js lighting - light types, shadows, environment lighting. Use when adding lights, configuring shadows, setting up IBL, or optimizing lighting performance. |
| [threejs-materials](.archived/skills/backend-development/threejs-materials/SKILL.md) | Three.js materials - PBR, basic, phong, shader materials, material properties. Use when styling meshes, working with textures, creating custom shaders, or optimizing material performance. |
| [typescript-expert](.archived/skills/backend-development/typescript-expert/SKILL.md) | TypeScript and JavaScript expert with deep knowledge of type-level programming, performance optimization, monorepo management, migration strategies, and modern tooling. |
| [uniprot-database](.archived/skills/backend-development/uniprot-database/SKILL.md) | Direct REST API access to UniProt. Protein searches, FASTA retrieval, ID mapping, Swiss-Prot/TrEMBL. For Python workflows with multiple databases, prefer bioservices (unified interface to 40+ services). Use this for direct HTTP/REST work or UniProt-specific control. |
| [unreal-engine-cpp-pro](.archived/skills/backend-development/unreal-engine-cpp-pro/SKILL.md) | Expert guide for Unreal Engine 5.x C++ development, covering UObject hygiene, performance patterns, and best practices. |
| [vr-ar](.archived/skills/backend-development/vr-ar/SKILL.md) | VR/AR development principles. Comfort, interaction, performance requirements. |
| [wordpress](.archived/skills/backend-development/wordpress/SKILL.md) | Complete WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security hardening. Includes WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks. |

</details>

### 🗄️ Database

<details>
<summary><b>🗄️ Database (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [aws-penetration-testing](.archived/skills/database/aws-penetration-testing/SKILL.md) | Provide comprehensive techniques for penetration testing AWS cloud environments. Covers IAM enumeration, privilege escalation, SSRF to metadata endpoint, S3 bucket exploitation, Lambda code extraction, and persistence techniques for red team operations. |
| [azure-cosmos-db-py](.archived/skills/database/azure-cosmos-db-py/SKILL.md) | Build production-grade Azure Cosmos DB NoSQL services following clean code, security best practices, and TDD principles. |
| [azure-cosmos-java](.archived/skills/database/azure-cosmos-java/SKILL.md) | Azure Cosmos DB SDK for Java. NoSQL database operations with global distribution, multi-model support, and reactive patterns. |
| [azure-data-tables-py](.archived/skills/database/azure-data-tables-py/SKILL.md) | Azure Tables SDK for Python (Storage and Cosmos DB). Use for NoSQL key-value storage, entity CRUD, and batch operations. |
| [azure-postgres-ts](.archived/skills/database/azure-postgres-ts/SKILL.md) | Connect to Azure Database for PostgreSQL Flexible Server from Node.js/TypeScript using the pg (node-postgres) package. |
| [azure-resource-manager-mysql-dotnet](.archived/skills/database/azure-resource-manager-mysql-dotnet/SKILL.md) | Azure MySQL Flexible Server SDK for .NET. Database management for MySQL Flexible Server deployments. |
| [azure-resource-manager-postgresql-dotnet](.archived/skills/database/azure-resource-manager-postgresql-dotnet/SKILL.md) | Azure PostgreSQL Flexible Server SDK for .NET. Database management for PostgreSQL Flexible Server deployments. |
| [cloudflare-workers-expert](.archived/skills/database/cloudflare-workers-expert/SKILL.md) | Expert in Cloudflare Workers and the Edge Computing ecosystem. Covers Wrangler, KV, D1, Durable Objects, and R2 storage. |
| [database](.archived/skills/database/database/SKILL.md) | Database development and operations workflow covering SQL, NoSQL, database design, migrations, optimization, and data engineering. |
| [database-design](.archived/skills/database/database-design/SKILL.md) | Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases. |
| [database-migrations-sql-migrations](.archived/skills/database/database-migrations-sql-migrations/SKILL.md) | SQL database migrations with zero-downtime strategies for PostgreSQL, MySQL, and SQL Server. Focus on data integrity and rollback plans. |
| [food-database-query](.archived/skills/database/food-database-query/SKILL.md) | Food Database Query |
| [hugging-face-datasets](.archived/skills/database/hugging-face-datasets/SKILL.md) | Create and manage datasets on Hugging Face Hub. Supports initializing repos, defining configs/system prompts, streaming row updates, and SQL-based dataset querying/transformation. Designed to work alongside HF MCP server for comprehensive dataset workflows. |
| [linear](.archived/skills/database/linear/SKILL.md) | Managing Linear issues, projects, and teams for issue tracking, status updates, querying projects, and managing team workflows. |
| [nosql-expert](.archived/skills/database/nosql-expert/SKILL.md) | Expert guidance for distributed NoSQL databases (Cassandra, DynamoDB). Focuses on mental models, query-first modeling, single-table design, and avoiding hot partitions in high-scale systems. |
| [odoo-backup-strategy](.archived/skills/database/odoo-backup-strategy/SKILL.md) | Complete Odoo backup and restore strategy: database dumps, filestore backup, automated scheduling, cloud storage upload, and tested restore procedures. |
| [postgresql](.archived/skills/database/postgresql/SKILL.md) | Design a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features |
| [postgresql-optimization](.archived/skills/database/postgresql-optimization/SKILL.md) | PostgreSQL database optimization workflow for query tuning, indexing strategies, performance analysis, and production database management. |
| [prisma-expert](.archived/skills/database/prisma-expert/SKILL.md) | You are an expert in Prisma ORM with deep knowledge of schema design, migrations, query optimization, relations modeling, and database operations across PostgreSQL, MySQL, and SQLite. |
| [sankhya-dashboard-html-jsp-custom-best-pratices](.archived/skills/database/sankhya-dashboard-html-jsp-custom-best-pratices/SKILL.md) | This skill should be used when the user asks for patterns, best practices, creation, or fixing of Sankhya dashboards using HTML, JSP, Java, and SQL. |
| [sql-injection-testing](.archived/skills/database/sql-injection-testing/SKILL.md) | Execute comprehensive SQL injection vulnerability assessments on web applications to identify database security flaws, demonstrate exploitation techniques, and validate input sanitization mechanisms. |
| [sql-optimization-patterns](.archived/skills/database/sql-optimization-patterns/SKILL.md) | Transform slow database queries into lightning-fast operations through systematic optimization, proper indexing, and query plan analysis. |
| [sql-pro](.archived/skills/database/sql-pro/SKILL.md) | Master modern SQL with cloud-native databases, OLTP/OLAP optimization, and advanced query techniques. Expert in performance tuning, data modeling, and hybrid analytical systems. |
| [sqlmap-database-pentesting](.archived/skills/database/sqlmap-database-pentesting/SKILL.md) | Provide systematic methodologies for automated SQL injection detection and exploitation using SQLMap. |
| [supabase-automation](.archived/skills/database/supabase-automation/SKILL.md) | Automate Supabase database queries, table management, project administration, storage, edge functions, and SQL execution via Rube MCP (Composio). Always search tools first for current schemas. |
| [videodb](.archived/skills/database/videodb/SKILL.md) | Video and audio perception, indexing, and editing. Ingest files/URLs/live streams, build visual/spoken indexes, search with timestamps, edit timelines, add overlays/subtitles, generate media, and create real-time alerts. |

</details>

### 📱 Mobile Development

<details>
<summary><b>📱 Mobile Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [audit-skills](.archived/skills/mobile-development/audit-skills/SKILL.md) | Expert security auditor for AI Skills and Bundles. Performs non-intrusive static analysis to identify malicious patterns, data leaks, system stability risks, and obfuscated payloads across Windows, macOS, Linux/Unix, and Mobile (Android/iOS). |
| [flutter-expert](.archived/skills/mobile-development/flutter-expert/SKILL.md) | Master Flutter development with Dart 3, advanced widgets, and multi-platform deployment. |
| [ios-debugger-agent](.archived/skills/mobile-development/ios-debugger-agent/SKILL.md) | Debug the current iOS project on a booted simulator with XcodeBuildMCP. |
| [ios-developer](.archived/skills/mobile-development/ios-developer/SKILL.md) | Develop native iOS applications with Swift/SwiftUI. Masters iOS 18, SwiftUI, UIKit integration, Core Data, networking, and App Store optimization. |
| [mobile-developer](.archived/skills/mobile-development/mobile-developer/SKILL.md) | Develop React Native, Flutter, or native mobile apps with modern architecture patterns. Masters cross-platform development, native integrations, offline sync, and app store optimization. |
| [skill-sentinel](.archived/skills/mobile-development/skill-sentinel/SKILL.md) | Auditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude. |

</details>

### 🔒 Security & Penetration Testing

<details>
<summary><b>🔒 Security & Penetration Testing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [007](.archived/skills/security-penetration-testing/007/SKILL.md) | Security audit, hardening, threat modeling (STRIDE/PASTA), Red/Blue Team, OWASP checks, code review, incident response, and infrastructure security for any project. |
| [accessibility-compliance-accessibility-audit](.archived/skills/security-penetration-testing/accessibility-compliance-accessibility-audit/SKILL.md) | You are an accessibility expert specializing in WCAG compliance, inclusive design, and assistive technology compatibility. Conduct audits, identify barriers, and provide remediation guidance. |
| [api-security-best-practices](.archived/skills/security-penetration-testing/api-security-best-practices/SKILL.md) | Implement secure API design patterns including authentication, authorization, input validation, rate limiting, and protection against common API vulnerabilities |
| [audit-context-building](.archived/skills/security-penetration-testing/audit-context-building/SKILL.md) | Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding. |
| [aws-iam-best-practices](.archived/skills/security-penetration-testing/aws-iam-best-practices/SKILL.md) | IAM policy review, hardening, and least privilege implementation |
| [aws-security-audit](.archived/skills/security-penetration-testing/aws-security-audit/SKILL.md) | Comprehensive AWS security posture assessment using AWS CLI and security best practices |
| [azure-security-keyvault-keys-dotnet](.archived/skills/security-penetration-testing/azure-security-keyvault-keys-dotnet/SKILL.md) | Azure Key Vault Keys SDK for .NET. Client library for managing cryptographic keys in Azure Key Vault and Managed HSM. Use for key creation, rotation, encryption, decryption, signing, and verification. |
| [burpsuite-project-parser](.archived/skills/security-penetration-testing/burpsuite-project-parser/SKILL.md) | Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with regex patterns, extracting security audit findings, dumping proxy history or site map data, or analyzing HTTP traffic captured in a Burp project. |
| [cc-skill-security-review](.archived/skills/security-penetration-testing/cc-skill-security-review/SKILL.md) | This skill ensures all code follows security best practices and identifies potential vulnerabilities. Use when implementing authentication or authorization, handling user input or file uploads, or creating new API endpoints. |
| [claude-settings-audit](.archived/skills/security-penetration-testing/claude-settings-audit/SKILL.md) | Analyze a repository to generate recommended Claude Code settings.json permissions. Use when setting up a new project, auditing existing settings, or determining which read-only bash commands to allow. Detects tech stack, build tools, and monorepo structure. |
| [codebase-audit-pre-push](.archived/skills/security-penetration-testing/codebase-audit-pre-push/SKILL.md) | Deep audit before GitHub push: removes junk files, dead code, security holes, and optimization issues. Checks every file line-by-line for production readiness. |
| [codebase-cleanup-deps-audit](.archived/skills/security-penetration-testing/codebase-cleanup-deps-audit/SKILL.md) | You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependencies for known vulnerabilities, licensing issues, outdated packages, and provide actionable remediation strategies. |
| [dependency-management-deps-audit](.archived/skills/security-penetration-testing/dependency-management-deps-audit/SKILL.md) | You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependencies for known vulnerabilities, licensing issues, outdated packages, and provide actionable remediation strategies. |
| [dependency-upgrade](.archived/skills/security-penetration-testing/dependency-upgrade/SKILL.md) | Master major dependency version upgrades, compatibility analysis, staged upgrade strategies, and comprehensive testing approaches. |
| [differential-review](.archived/skills/security-penetration-testing/differential-review/SKILL.md) | Security-focused code review for PRs, commits, and diffs. |
| [file-path-traversal](.archived/skills/security-penetration-testing/file-path-traversal/SKILL.md) | Identify and exploit file path traversal (directory traversal) vulnerabilities that allow attackers to read arbitrary files on the server, potentially including sensitive configuration files, credentials, and source code. |
| [find-bugs](.archived/skills/security-penetration-testing/find-bugs/SKILL.md) | Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or audit code on the current branch. |
| [firebase](.archived/skills/security-penetration-testing/firebase/SKILL.md) | You're a developer who has shipped dozens of Firebase projects. You've seen the \"easy\" path lead to security breaches, runaway costs, and impossible migrations. You know Firebase is powerful, but you also know its sharp edges. |
| [fix-review](.archived/skills/security-penetration-testing/fix-review/SKILL.md) | Verify fix commits address audit findings without new bugs |
| [fixing-accessibility](.archived/skills/security-penetration-testing/fixing-accessibility/SKILL.md) | Audit and fix HTML accessibility issues including ARIA labels, keyboard navigation, focus management, color contrast, and form errors. Use when adding interactive controls, forms, dialogs, or reviewing WCAG compliance. |
| [fixing-metadata](.archived/skills/security-penetration-testing/fixing-metadata/SKILL.md) | Audit and fix HTML metadata including page titles, meta descriptions, canonical URLs, Open Graph tags, Twitter cards, favicons, JSON-LD structured data, and robots directives. Use when adding or reviewing SEO and social metadata. |
| [gha-security-review](.archived/skills/security-penetration-testing/gha-security-review/SKILL.md) | Find exploitable vulnerabilities in GitHub Actions workflows. Every finding MUST include a concrete exploitation scenario — if you can't build the attack, don't report it. |
| [html-injection-testing](.archived/skills/security-penetration-testing/html-injection-testing/SKILL.md) | Identify and exploit HTML injection vulnerabilities that allow attackers to inject malicious HTML content into web applications. This vulnerability enables attackers to modify page appearance, create phishing pages, and steal user credentials through injected forms. |
| [idor-testing](.archived/skills/security-penetration-testing/idor-testing/SKILL.md) | Provide systematic methodologies for identifying and exploiting Insecure Direct Object Reference (IDOR) vulnerabilities in web applications. |
| [kotlin-coroutines-expert](.archived/skills/security-penetration-testing/kotlin-coroutines-expert/SKILL.md) | Expert patterns for Kotlin Coroutines and Flow, covering structured concurrency, error handling, and testing. |
| [laravel-security-audit](.archived/skills/security-penetration-testing/laravel-security-audit/SKILL.md) | Security auditor for Laravel applications. Analyzes code for vulnerabilities, misconfigurations, and insecure practices using OWASP standards and Laravel security best practices. |
| [local-legal-seo-audit](.archived/skills/security-penetration-testing/local-legal-seo-audit/SKILL.md) | Audit and improve local SEO for law firms, attorneys, forensic experts and legal/professional services sites with local presence, focusing on GBP, directories, E-E-A-T and practice/location pages. |
| [odoo-security-rules](.archived/skills/security-penetration-testing/odoo-security-rules/SKILL.md) | Expert in Odoo access control: ir.model.access.csv, record rules (ir.rule), groups, and multi-company security patterns. |
| [openclaw-github-repo-commander](.archived/skills/security-penetration-testing/openclaw-github-repo-commander/SKILL.md) | 7-stage super workflow for GitHub repo audit, cleanup, PR review, and competitor analysis |
| [pci-compliance](.archived/skills/security-penetration-testing/pci-compliance/SKILL.md) | Master PCI DSS (Payment Card Industry Data Security Standard) compliance for secure payment processing and handling of cardholder data. |
| [pentest-checklist](.archived/skills/security-penetration-testing/pentest-checklist/SKILL.md) | Provide a comprehensive checklist for planning, executing, and following up on penetration tests. Ensure thorough preparation, proper scoping, and effective remediation of discovered vulnerabilities. |
| [privacy-by-design](.archived/skills/security-penetration-testing/privacy-by-design/SKILL.md) | Use when building apps that collect user data. Ensures privacy protections are built in from the start—data minimization, consent, encryption. |
| [production-code-audit](.archived/skills/security-penetration-testing/production-code-audit/SKILL.md) | Autonomously deep-scan entire codebase line-by-line, understand architecture and patterns, then systematically transform it to production-grade, corporate-level professional quality with optimizations |
| [project-skill-audit](.archived/skills/security-penetration-testing/project-skill-audit/SKILL.md) | Audit a project and recommend the highest-value skills to add or update. |
| [security-audit](.archived/skills/security-penetration-testing/security-audit/SKILL.md) | Comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening. |
| [security-auditor](.archived/skills/security-penetration-testing/security-auditor/SKILL.md) | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. |
| [security-scanning-security-dependencies](.archived/skills/security-penetration-testing/security-scanning-security-dependencies/SKILL.md) | You are a security expert specializing in dependency vulnerability analysis, SBOM generation, and supply chain security. Scan project dependencies across multiple ecosystems to identify vulnerabilities, assess risks, and provide automated remediation strategies. |
| [security-scanning-security-hardening](.archived/skills/security-penetration-testing/security-scanning-security-hardening/SKILL.md) | Coordinate multi-layer security scanning and hardening across application, infrastructure, and compliance controls. |
| [security-scanning-security-sast](.archived/skills/security-penetration-testing/security-scanning-security-sast/SKILL.md) | Static Application Security Testing (SAST) for code vulnerability |
| [semgrep-rule-creator](.archived/skills/security-penetration-testing/semgrep-rule-creator/SKILL.md) | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rules or building custom static analysis detections. |
| [seo-technical](.archived/skills/security-penetration-testing/seo-technical/SKILL.md) | Audit technical SEO across crawlability, indexability, security, URLs, mobile, Core Web Vitals, structured data, JavaScript rendering, and related platform signals like robots.txt and AI crawler access. |
| [smtp-penetration-testing](.archived/skills/security-penetration-testing/smtp-penetration-testing/SKILL.md) | Conduct comprehensive security assessments of SMTP (Simple Mail Transfer Protocol) servers to identify vulnerabilities including open relays, user enumeration, weak authentication, and misconfiguration. |
| [ssh-penetration-testing](.archived/skills/security-penetration-testing/ssh-penetration-testing/SKILL.md) | Conduct comprehensive SSH security assessments including enumeration, credential attacks, vulnerability exploitation, tunneling techniques, and post-exploitation activities. This skill covers the complete methodology for testing SSH service security. |
| [supply-chain-risk-auditor](.archived/skills/security-penetration-testing/supply-chain-risk-auditor/SKILL.md) | Identifies dependencies at heightened risk of exploitation or takeover. Use when assessing supply chain attack surface, evaluating dependency health, or scoping security engagements. |
| [testing-patterns](.archived/skills/security-penetration-testing/testing-patterns/SKILL.md) | Jest testing patterns, factory functions, mocking strategies, and TDD workflow. Use when writing unit tests, creating test factories, or following TDD red-green-refactor cycle. |
| [threat-mitigation-mapping](.archived/skills/security-penetration-testing/threat-mitigation-mapping/SKILL.md) | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness. |
| [variant-analysis](.archived/skills/security-penetration-testing/variant-analysis/SKILL.md) | Find similar vulnerabilities and bugs across codebases using pattern-based analysis. Use when hunting bug variants, building CodeQL/Semgrep queries, analyzing security vulnerabilities, or performing systematic code audits after finding an initial issue. |
| [web-security-testing](.archived/skills/security-penetration-testing/web-security-testing/SKILL.md) | Web application security testing workflow for OWASP Top 10 vulnerabilities including injection, XSS, authentication flaws, and access control issues. |
| [windows-privilege-escalation](.archived/skills/security-penetration-testing/windows-privilege-escalation/SKILL.md) | Provide systematic methodologies for discovering and exploiting privilege escalation vulnerabilities on Windows systems during penetration testing engagements. |
| [wordpress-penetration-testing](.archived/skills/security-penetration-testing/wordpress-penetration-testing/SKILL.md) | Assess WordPress installations for common vulnerabilities and WordPress 7.0 attack surfaces. |

</details>

### ☁️ Cloud, DevOps & Infrastructure

<details>
<summary><b>☁️ Cloud, DevOps & Infrastructure (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [acceptance-orchestrator](.archived/skills/cloud-devops-infrastructure/acceptance-orchestrator/SKILL.md) | Use when a coding task should be driven end-to-end from issue intake through implementation, review, deployment, and acceptance verification with minimal human re-intervention. |
| [aws-skills](.archived/skills/cloud-devops-infrastructure/aws-skills/SKILL.md) | AWS development with infrastructure automation and cloud architecture patterns |
| [azd-deployment](.archived/skills/cloud-devops-infrastructure/azd-deployment/SKILL.md) | Deploy containerized frontend + backend applications to Azure Container Apps with remote builds, managed identity, and idempotent infrastructure. |
| [cdk-patterns](.archived/skills/cloud-devops-infrastructure/cdk-patterns/SKILL.md) | Common AWS CDK patterns and constructs for building cloud infrastructure with TypeScript, Python, or Java. Use when designing reusable CDK stacks and L3 constructs. |
| [closed-loop-delivery](.archived/skills/cloud-devops-infrastructure/closed-loop-delivery/SKILL.md) | Use when a coding task must be completed against explicit acceptance criteria with minimal user re-intervention across implementation, review feedback, deployment, and runtime verification. |
| [cloud-devops](.archived/skills/cloud-devops-infrastructure/cloud-devops/SKILL.md) | Cloud infrastructure and DevOps workflow covering AWS, Azure, GCP, Kubernetes, Terraform, CI/CD, monitoring, and cloud-native development. |
| [database-migrations-migration-observability](.archived/skills/cloud-devops-infrastructure/database-migrations-migration-observability/SKILL.md) | Migration monitoring, CDC, and observability infrastructure |
| [deployment-procedures](.archived/skills/cloud-devops-infrastructure/deployment-procedures/SKILL.md) | Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts. |
| [deployment-validation-config-validate](.archived/skills/cloud-devops-infrastructure/deployment-validation-config-validate/SKILL.md) | You are a configuration management expert specializing in validating, testing, and ensuring the correctness of application configurations. Create comprehensive validation schemas, implement configurat |
| [devops-deploy](.archived/skills/cloud-devops-infrastructure/devops-deploy/SKILL.md) | DevOps e deploy de aplicacoes — Docker, CI/CD com GitHub Actions, AWS Lambda, SAM, Terraform, infraestrutura como codigo e monitoramento. |
| [docker-expert](.archived/skills/cloud-devops-infrastructure/docker-expert/SKILL.md) | You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns, and production deployment strategies based on current industry best practices. |
| [expo-deployment](.archived/skills/cloud-devops-infrastructure/expo-deployment/SKILL.md) | Deploy Expo apps to production |
| [gitlab-ci-patterns](.archived/skills/cloud-devops-infrastructure/gitlab-ci-patterns/SKILL.md) | Comprehensive GitLab CI/CD pipeline patterns for automated testing, building, and deployment. |
| [gitops-workflow](.archived/skills/cloud-devops-infrastructure/gitops-workflow/SKILL.md) | Complete guide to implementing GitOps workflows with ArgoCD and Flux for automated Kubernetes deployments. |
| [helm-chart-scaffolding](.archived/skills/cloud-devops-infrastructure/helm-chart-scaffolding/SKILL.md) | Comprehensive guidance for creating, organizing, and managing Helm charts for packaging and deploying Kubernetes applications. |
| [hugging-face-jobs](.archived/skills/cloud-devops-infrastructure/hugging-face-jobs/SKILL.md) | Run any workload on fully managed Hugging Face infrastructure. No local setup required—jobs run on cloud CPUs, GPUs, or TPUs and can persist results to the Hugging Face Hub. |
| [hugging-face-model-trainer](.archived/skills/cloud-devops-infrastructure/hugging-face-model-trainer/SKILL.md) | Train language models using TRL (Transformer Reinforcement Learning) on fully managed Hugging Face infrastructure. No local GPU setup required—models train on cloud GPUs and results are automatically saved to the Hugging Face Hub. |
| [incident-responder](.archived/skills/cloud-devops-infrastructure/incident-responder/SKILL.md) | Expert SRE incident responder specializing in rapid problem resolution, modern observability, and comprehensive incident management. |
| [inngest](.archived/skills/cloud-devops-infrastructure/inngest/SKILL.md) | You are an Inngest expert who builds reliable background processing without managing infrastructure. You understand that serverless doesn't mean you can't have durable, long-running workflows - it means you don't manage the workers. |
| [k8s-manifest-generator](.archived/skills/cloud-devops-infrastructure/k8s-manifest-generator/SKILL.md) | Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims. |
| [k8s-security-policies](.archived/skills/cloud-devops-infrastructure/k8s-security-policies/SKILL.md) | Comprehensive guide for implementing NetworkPolicy, PodSecurityPolicy, RBAC, and Pod Security Standards in Kubernetes. |
| [kubernetes-architect](.archived/skills/cloud-devops-infrastructure/kubernetes-architect/SKILL.md) | Expert Kubernetes architect specializing in cloud-native infrastructure, advanced GitOps workflows (ArgoCD/Flux), and enterprise container orchestration. |
| [kubernetes-deployment](.archived/skills/cloud-devops-infrastructure/kubernetes-deployment/SKILL.md) | Kubernetes deployment workflow for container orchestration, Helm charts, service mesh, and production-ready K8s configurations. |
| [linkerd-patterns](.archived/skills/cloud-devops-infrastructure/linkerd-patterns/SKILL.md) | Production patterns for Linkerd service mesh - the lightweight, security-first service mesh for Kubernetes. |
| [makepad-deployment](.archived/skills/cloud-devops-infrastructure/makepad-deployment/SKILL.md) | | |
| [odoo-docker-deployment](.archived/skills/cloud-devops-infrastructure/odoo-docker-deployment/SKILL.md) | Production-ready Docker and docker-compose setup for Odoo with PostgreSQL, persistent volumes, environment-based configuration, and Nginx reverse proxy. |
| [shellcheck-configuration](.archived/skills/cloud-devops-infrastructure/shellcheck-configuration/SKILL.md) | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability. |
| [sred-project-organizer](.archived/skills/cloud-devops-infrastructure/sred-project-organizer/SKILL.md) | Take a list of projects and their related documentation, and organize them into the SRED format for submission. |
| [sred-work-summary](.archived/skills/cloud-devops-infrastructure/sred-work-summary/SKILL.md) | Go back through the previous year of work and create a Notion doc that groups relevant links into projects that can then be documented as SRED projects. |
| [terraform-aws-modules](.archived/skills/cloud-devops-infrastructure/terraform-aws-modules/SKILL.md) | Terraform module creation for AWS — reusable modules, state management, and HCL best practices. Use when building or reviewing Terraform AWS infrastructure. |
| [terraform-infrastructure](.archived/skills/cloud-devops-infrastructure/terraform-infrastructure/SKILL.md) | Terraform infrastructure as code workflow for provisioning cloud resources, creating reusable modules, and managing infrastructure at scale. |
| [terraform-module-library](.archived/skills/cloud-devops-infrastructure/terraform-module-library/SKILL.md) | Production-ready Terraform module patterns for AWS, Azure, and GCP infrastructure. |
| [terraform-skill](.archived/skills/cloud-devops-infrastructure/terraform-skill/SKILL.md) | Terraform infrastructure as code best practices |
| [terraform-specialist](.archived/skills/cloud-devops-infrastructure/terraform-specialist/SKILL.md) | Expert Terraform/OpenTofu specialist mastering advanced IaC automation, state management, and enterprise infrastructure patterns. |
| [unity-developer](.archived/skills/cloud-devops-infrastructure/unity-developer/SKILL.md) | Build Unity games with optimized C# scripts, efficient rendering, and proper asset management. Masters Unity 6 LTS, URP/HDRP pipelines, and cross-platform deployment. |
| [upstash-qstash](.archived/skills/cloud-devops-infrastructure/upstash-qstash/SKILL.md) | You are an Upstash QStash expert who builds reliable serverless messaging without infrastructure management. You understand that QStash's simplicity is its power - HTTP in, HTTP out, with reliability in between. |
| [vector-index-tuning](.archived/skills/cloud-devops-infrastructure/vector-index-tuning/SKILL.md) | Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure. |
| [vercel-deployment](.archived/skills/cloud-devops-infrastructure/vercel-deployment/SKILL.md) | Expert knowledge for deploying to Vercel with Next.js Use when: vercel, deploy, deployment, hosting, production. |

</details>

### 🧪 Testing & Quality

<details>
<summary><b>🧪 Testing & Quality (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [bug-hunter](.archived/skills/testing-quality/bug-hunter/SKILL.md) | Systematically finds and fixes bugs using proven debugging techniques. Traces from symptoms to root cause, implements fixes, and prevents regression. |
| [copilot-sdk](.archived/skills/testing-quality/copilot-sdk/SKILL.md) | Build applications that programmatically interact with GitHub Copilot. The SDK wraps the Copilot CLI via JSON-RPC, providing session management, custom tools, hooks, MCP server integration, and streaming across Node.js, Python, Go, and .NET. |
| [custom-senior-it-ba-specialist](.archived/skills/testing-quality/custom-senior-it-ba-specialist/SKILL.md) | Act as a senior IT business analyst for software development initiatives. Use when the user needs business objectives translated into technical requirements, complex workflow analysis, system integration mapping, or rigorous requirements traceability. |
| [ddd-context-mapping](.archived/skills/testing-quality/ddd-context-mapping/SKILL.md) | Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns. |
| [debugger](.archived/skills/testing-quality/debugger/SKILL.md) | Debugging specialist for errors, test failures, and unexpected |
| [debugging-strategies](.archived/skills/testing-quality/debugging-strategies/SKILL.md) | Transform debugging from frustrating guesswork into systematic problem-solving with proven strategies, powerful tools, and methodical approaches. |
| [debugging-toolkit-smart-debug](.archived/skills/testing-quality/debugging-toolkit-smart-debug/SKILL.md) | Use when working with debugging toolkit smart debug |
| [devops-troubleshooter](.archived/skills/testing-quality/devops-troubleshooter/SKILL.md) | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. |
| [distributed-debugging-debug-trace](.archived/skills/testing-quality/distributed-debugging-debug-trace/SKILL.md) | You are a debugging expert specializing in setting up comprehensive debugging environments, distributed tracing, and diagnostic tools. Configure debugging workflows, implement tracing solutions, and establish troubleshooting practices for development and production environments. |
| [e2e-testing](.archived/skills/testing-quality/e2e-testing/SKILL.md) | End-to-end testing workflow with Playwright for browser automation, visual regression, cross-browser testing, and CI/CD integration. |
| [error-debugging-error-analysis](.archived/skills/testing-quality/error-debugging-error-analysis/SKILL.md) | You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing comprehensive observability solutions. |
| [error-debugging-error-trace](.archived/skills/testing-quality/error-debugging-error-trace/SKILL.md) | You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking systems, configure alerts, implement structured logging, and ensure teams can quickly identify and resolve production issues. |
| [error-debugging-multi-agent-review](.archived/skills/testing-quality/error-debugging-multi-agent-review/SKILL.md) | Use when working with error debugging multi agent review |
| [error-diagnostics-error-analysis](.archived/skills/testing-quality/error-diagnostics-error-analysis/SKILL.md) | You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing comprehensive observability solutions. |
| [error-handling-patterns](.archived/skills/testing-quality/error-handling-patterns/SKILL.md) | Build resilient applications with robust error handling strategies that gracefully handle failures and provide excellent debugging experiences. |
| [git-hooks-automation](.archived/skills/testing-quality/git-hooks-automation/SKILL.md) | Master Git hooks setup with Husky, lint-staged, pre-commit framework, and commitlint. Automate code quality gates, formatting, linting, and commit message enforcement before code reaches CI. |
| [git-pr-workflows-onboard](.archived/skills/testing-quality/git-pr-workflows-onboard/SKILL.md) | You are an **expert onboarding specialist and knowledge transfer architect** with deep experience in remote-first organizations, technical team integration, and accelerated learning methodologies. You |
| [gmail-automation](.archived/skills/testing-quality/gmail-automation/SKILL.md) | Lightweight Gmail integration with standalone OAuth authentication. No MCP server required. |
| [go-concurrency-patterns](.archived/skills/testing-quality/go-concurrency-patterns/SKILL.md) | Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions. |
| [google-calendar-automation](.archived/skills/testing-quality/google-calendar-automation/SKILL.md) | Lightweight Google Calendar integration with standalone OAuth authentication. No MCP server required. |
| [google-docs-automation](.archived/skills/testing-quality/google-docs-automation/SKILL.md) | Lightweight Google Docs integration with standalone OAuth authentication. No MCP server required. |
| [google-drive-automation](.archived/skills/testing-quality/google-drive-automation/SKILL.md) | Lightweight Google Drive integration with standalone OAuth authentication. No MCP server required. Full read/write access. |
| [google-sheets-automation](.archived/skills/testing-quality/google-sheets-automation/SKILL.md) | Lightweight Google Sheets integration with standalone OAuth authentication. No MCP server required. Full read/write access. |
| [google-slides-automation](.archived/skills/testing-quality/google-slides-automation/SKILL.md) | Lightweight Google Slides integration with standalone OAuth authentication. No MCP server required. Full read/write access. |
| [hubspot-automation](.archived/skills/testing-quality/hubspot-automation/SKILL.md) | Automate HubSpot CRM operations (contacts, companies, deals, tickets, properties) via Rube MCP using Composio integration. |
| [hubspot-integration](.archived/skills/testing-quality/hubspot-integration/SKILL.md) | Authentication for single-account integrations |
| [linux-shell-scripting](.archived/skills/testing-quality/linux-shell-scripting/SKILL.md) | Provide production-ready shell script templates for common Linux system administration tasks including backups, monitoring, user management, log analysis, and automation. These scripts serve as building blocks for security operations and penetration testing environments. |
| [makepad-reference](.archived/skills/testing-quality/makepad-reference/SKILL.md) | This category provides reference materials for debugging, code quality, and advanced layout patterns. |
| [nextjs-supabase-auth](.archived/skills/testing-quality/nextjs-supabase-auth/SKILL.md) | Expert integration of Supabase Auth with Next.js App Router Use when: supabase auth next, authentication next.js, login supabase, auth middleware, protected route. |
| [office-productivity](.archived/skills/testing-quality/office-productivity/SKILL.md) | Office productivity workflow covering document creation, spreadsheet automation, presentation generation, and integration with LibreOffice and Microsoft Office formats. |
| [os-scripting](.archived/skills/testing-quality/os-scripting/SKILL.md) | Operating system and shell scripting troubleshooting workflow for Linux, macOS, and Windows. Covers bash scripting, system administration, debugging, and automation. |
| [protocol-reverse-engineering](.archived/skills/testing-quality/protocol-reverse-engineering/SKILL.md) | Comprehensive techniques for capturing, analyzing, and documenting network protocols for security research, interoperability, and debugging. |
| [quality-nonconformance](.archived/skills/testing-quality/quality-nonconformance/SKILL.md) | Codified expertise for quality control, non-conformance investigation, root cause analysis, corrective action, and supplier quality management in regulated manufacturing. |
| [robius-matrix-integration](.archived/skills/testing-quality/robius-matrix-integration/SKILL.md) | | |
| [service-mesh-expert](.archived/skills/testing-quality/service-mesh-expert/SKILL.md) | Expert service mesh architect specializing in Istio, Linkerd, and cloud-native networking patterns. Masters traffic management, security policies, observability integration, and multi-cluster mesh con |
| [systematic-debugging](.archived/skills/testing-quality/systematic-debugging/SKILL.md) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| [test-automator](.archived/skills/testing-quality/test-automator/SKILL.md) | Master AI-powered test automation with modern frameworks, self-healing tests, and comprehensive quality engineering. Build scalable testing strategies with advanced CI/CD integration. |
| [testing-qa](.archived/skills/testing-quality/testing-qa/SKILL.md) | Comprehensive testing and QA workflow covering unit testing, integration testing, E2E testing, browser automation, and quality assurance. |
| [track-management](.archived/skills/testing-quality/track-management/SKILL.md) | Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Applies to spec.md, plan.md, and track lifecycle operations. |
| [unsplash-integration](.archived/skills/testing-quality/unsplash-integration/SKILL.md) | Integration skill for searching and fetching high-quality, free-to-use professional photography from Unsplash. |
| [wiki-qa](.archived/skills/testing-quality/wiki-qa/SKILL.md) | Answer repository questions grounded entirely in source code evidence. Use when user asks a question about the codebase, user wants to understand a specific file, function, or component, or user asks \"how does X work\" or \"where is Y defined\". |

</details>

### 🔧 Programming Languages

<details>
<summary><b>🔧 Programming Languages (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [bash-scripting](.archived/skills/programming-languages/bash-scripting/SKILL.md) | Bash scripting workflow for creating production-ready shell scripts with defensive patterns, error handling, and testing. |
| [bun-development](.archived/skills/programming-languages/bun-development/SKILL.md) | Fast, modern JavaScript/TypeScript development with the Bun runtime, inspired by [oven-sh/bun](https://github.com/oven-sh/bun). |
| [fp-ts-errors](.archived/skills/programming-languages/fp-ts-errors/SKILL.md) | Handle errors as values using fp-ts Either and TaskEither for cleaner, more predictable TypeScript code. Use when implementing error handling patterns with fp-ts. |
| [fp-ts-pragmatic](.archived/skills/programming-languages/fp-ts-pragmatic/SKILL.md) | A practical, jargon-free guide to fp-ts functional programming - the 80/20 approach that gets results without the academic overhead. Use when writing TypeScript with fp-ts library. |
| [fp-types-ref](.archived/skills/programming-languages/fp-types-ref/SKILL.md) | Quick reference for fp-ts types. Use when user asks which type to use, needs Option/Either/Task decision help, or wants fp-ts imports. |
| [godot-4-migration](.archived/skills/programming-languages/godot-4-migration/SKILL.md) | Specialized guide for migrating Godot 3.x projects to Godot 4 (GDScript 2.0), covering syntax changes, Tweens, and exports. |
| [javascript-typescript-typescript-scaffold](.archived/skills/programming-languages/javascript-typescript-typescript-scaffold/SKILL.md) | You are a TypeScript project architecture expert specializing in scaffolding production-ready Node.js and frontend applications. Generate complete project structures with modern tooling (pnpm, Vite, N |
| [mermaid-expert](.archived/skills/programming-languages/mermaid-expert/SKILL.md) | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and styling. |
| [n8n-code-javascript](.archived/skills/programming-languages/n8n-code-javascript/SKILL.md) | Write JavaScript code in n8n Code nodes. Use when writing JavaScript in n8n, using $input/$json/$node syntax, making HTTP requests with $helpers, working with dates using DateTime, troubleshooting Code node errors, or choosing between Code node modes. |
| [n8n-code-python](.archived/skills/programming-languages/n8n-code-python/SKILL.md) | Write Python code in n8n Code nodes. Use when writing Python in n8n, using _input/_json/_node syntax, working with standard library, or need to understand Python limitations in n8n Code nodes. |
| [n8n-expression-syntax](.archived/skills/programming-languages/n8n-expression-syntax/SKILL.md) | Validate n8n expression syntax and fix common errors. Use when writing n8n expressions, using {{}} syntax, accessing $json/$node variables, troubleshooting expression errors, or working with webhook data in workflows. |
| [obsidian-markdown](.archived/skills/programming-languages/obsidian-markdown/SKILL.md) | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes. |
| [odoo-xml-views-builder](.archived/skills/programming-languages/odoo-xml-views-builder/SKILL.md) | Expert at building Odoo XML views: Form, List, Kanban, Search, Calendar, and Graph. Generates correct XML for Odoo 14-17 with proper visibility syntax. |
| [posix-shell-pro](.archived/skills/programming-languages/posix-shell-pro/SKILL.md) | Expert in strict POSIX sh scripting for maximum portability across Unix-like systems. Specializes in shell scripts that run on any POSIX-compliant shell (dash, ash, sh, bash --posix). |
| [powershell-windows](.archived/skills/programming-languages/powershell-windows/SKILL.md) | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. |
| [sast-configuration](.archived/skills/programming-languages/sast-configuration/SKILL.md) | Static Application Security Testing (SAST) tool setup, configuration, and custom rule creation for comprehensive security scanning across multiple programming languages. |
| [threejs-textures](.archived/skills/programming-languages/threejs-textures/SKILL.md) | Three.js textures - texture types, UV mapping, environment maps, texture settings. Use when working with images, UV coordinates, cubemaps, HDR environments, or texture optimization. |
| [typescript-advanced-types](.archived/skills/programming-languages/typescript-advanced-types/SKILL.md) | Comprehensive guidance for mastering TypeScript's advanced type system including generics, conditional types, mapped types, template literal types, and utility types for building robust, type-safe applications. |
| [zustand-store-ts](.archived/skills/programming-languages/zustand-store-ts/SKILL.md) | Create Zustand stores following established patterns with proper TypeScript types and middleware. |

</details>

### 🎨 Design, UI/UX & Creative

<details>
<summary><b>🎨 Design, UI/UX & Creative (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [c4-component](.archived/skills/design-ui-ux-creative/c4-component/SKILL.md) | Expert C4 Component-level documentation specialist. Synthesizes C4 Code-level documentation into Component-level architecture, defining component boundaries, interfaces, and relationships. |
| [claimable-postgres](.archived/skills/design-ui-ux-creative/claimable-postgres/SKILL.md) | Provision instant temporary Postgres databases via Claimable Postgres by Neon (pg.new). No login or credit card required. Use for quick Postgres environments and throwaway DATABASE_URL for prototyping. |
| [code-documentation-code-explain](.archived/skills/design-ui-ux-creative/code-documentation-code-explain/SKILL.md) | You are a code education expert specializing in explaining complex code through clear narratives, visual diagrams, and step-by-step breakdowns. Transform difficult concepts into understandable explanations for developers at all levels. |
| [game-art](.archived/skills/design-ui-ux-creative/game-art/SKILL.md) | Game art principles. Visual style selection, asset pipeline, animation workflow. |
| [hig-components-content](.archived/skills/design-ui-ux-creative/hig-components-content/SKILL.md) | Apple Human Interface Guidelines for content display components. |
| [hig-components-layout](.archived/skills/design-ui-ux-creative/hig-components-layout/SKILL.md) | Apple Human Interface Guidelines for layout and navigation components. |
| [hig-foundations](.archived/skills/design-ui-ux-creative/hig-foundations/SKILL.md) | Apple Human Interface Guidelines design foundations. |
| [hig-patterns](.archived/skills/design-ui-ux-creative/hig-patterns/SKILL.md) | Apple Human Interface Guidelines interaction and UX patterns. |
| [hig-platforms](.archived/skills/design-ui-ux-creative/hig-platforms/SKILL.md) | Apple Human Interface Guidelines for platform-specific design. |
| [imagen](.archived/skills/design-ui-ux-creative/imagen/SKILL.md) | AI image generation skill powered by Google Gemini, enabling seamless visual content creation for UI placeholders, documentation, and design assets. |
| [json-canvas](.archived/skills/design-ui-ux-creative/json-canvas/SKILL.md) | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian. |
| [threejs-postprocessing](.archived/skills/design-ui-ux-creative/threejs-postprocessing/SKILL.md) | Three.js post-processing - EffectComposer, bloom, DOF, screen effects. Use when adding visual effects, color grading, blur, glow, or creating custom screen-space shaders. |
| [threejs-shaders](.archived/skills/design-ui-ux-creative/threejs-shaders/SKILL.md) | Three.js shaders - GLSL, ShaderMaterial, uniforms, custom effects. Use when creating custom visual effects, modifying vertices, writing fragment shaders, or extending built-in materials. |
| [threejs-skills](.archived/skills/design-ui-ux-creative/threejs-skills/SKILL.md) | Create 3D scenes, interactive experiences, and visual effects using Three.js. Use when user requests 3D graphics, WebGL experiences, 3D visualizations, animations, or interactive 3D elements. |
| [ui-visual-validator](.archived/skills/design-ui-ux-creative/ui-visual-validator/SKILL.md) | Rigorous visual validation expert specializing in UI testing, design system compliance, and accessibility verification. |

</details>

### 📚 Documentation & Writing

<details>
<summary><b>📚 Documentation & Writing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [api-documentation](.archived/skills/documentation-writing/api-documentation/SKILL.md) | API documentation workflow for generating OpenAPI specs, creating developer guides, and maintaining comprehensive API documentation. |
| [c4-code](.archived/skills/documentation-writing/c4-code/SKILL.md) | Expert C4 Code-level documentation specialist. Analyzes code directories to create comprehensive C4 code-level documentation including function signatures, arguments, dependencies, and code structure. |
| [c4-context](.archived/skills/documentation-writing/c4-context/SKILL.md) | Expert C4 Context-level documentation specialist. Creates high-level system context diagrams, documents personas, user journeys, system features, and external dependencies. |
| [code-documentation-doc-generate](.archived/skills/documentation-writing/code-documentation-doc-generate/SKILL.md) | You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams, user guides, and technical references using AI-powered analysis and industry best practices. |
| [create-pr](.archived/skills/documentation-writing/create-pr/SKILL.md) | Alias for sentry-skills:pr-writer. Use when users explicitly ask for "create-pr" or reference the legacy skill name. Redirects to the canonical PR writing workflow. |
| [custom-debrief](.archived/skills/documentation-writing/custom-debrief/SKILL.md) | Custom Debrief |
| [customs-trade-compliance](.archived/skills/documentation-writing/customs-trade-compliance/SKILL.md) | Codified expertise for customs documentation, tariff classification, duty optimisation, restricted party screening, and regulatory compliance across multiple jurisdictions. |
| [documentation](.archived/skills/documentation-writing/documentation/SKILL.md) | Documentation generation workflow covering API docs, architecture docs, README files, code comments, and technical writing. |
| [documentation-generation-doc-generate](.archived/skills/documentation-writing/documentation-generation-doc-generate/SKILL.md) | You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams, user guides, and technical references using AI-powered analysis and industry best practices. |
| [documentation-templates](.archived/skills/documentation-writing/documentation-templates/SKILL.md) | Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation. |
| [employment-contract-templates](.archived/skills/documentation-writing/employment-contract-templates/SKILL.md) | Templates and patterns for creating legally sound employment documentation including contracts, offer letters, and HR policies. |
| [finishing-a-development-branch](.archived/skills/documentation-writing/finishing-a-development-branch/SKILL.md) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup |
| [plan-writing](.archived/skills/documentation-writing/plan-writing/SKILL.md) | Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work. |
| [readme](.archived/skills/documentation-writing/readme/SKILL.md) | You are an expert technical writer creating comprehensive project documentation. Your goal is to write a README.md that is absurdly thorough—the kind of documentation you wish every project had. |
| [reference-builder](.archived/skills/documentation-writing/reference-builder/SKILL.md) | Creates exhaustive technical references and API documentation. Generates comprehensive parameter listings, configuration guides, and searchable reference materials. |
| [wiki-architect](.archived/skills/documentation-writing/wiki-architect/SKILL.md) | You are a documentation architect that produces structured wiki catalogues and onboarding guides from codebases. |
| [wiki-onboarding](.archived/skills/documentation-writing/wiki-onboarding/SKILL.md) | Generate two complementary onboarding documents that together give any engineer — from newcomer to principal — a complete understanding of a codebase. Use when user asks for onboarding docs or getting-started guides, user runs /deep-wiki, or user wants to help new team members understand a codebase. |
| [wiki-page-writer](.archived/skills/documentation-writing/wiki-page-writer/SKILL.md) | You are a senior documentation engineer that generates comprehensive technical documentation pages with evidence-based depth. |

</details>

### 🔀 Git & Version Control

<details>
<summary><b>🔀 Git & Version Control (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [c4-architecture-c4-architecture](.archived/skills/git-version-control/c4-architecture-c4-architecture/SKILL.md) | Generate comprehensive C4 architecture documentation for an existing repository/codebase using a bottom-up analysis approach. |
| [makepad-widgets](.archived/skills/git-version-control/makepad-widgets/SKILL.md) | Version: makepad-widgets (dev branch) | Last Updated: 2026-01-19 > > Check for updates: https://crates.io/crates/makepad-widgets |
| [segment-cdp](.archived/skills/git-version-control/segment-cdp/SKILL.md) | Client-side tracking with Analytics.js. Include track, identify, page, and group calls. Anonymous ID persists until identify merges with user. |
| [using-git-worktrees](.archived/skills/git-version-control/using-git-worktrees/SKILL.md) | Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching. |

</details>

### 🏗️ Architecture & Patterns

<details>
<summary><b>🏗️ Architecture & Patterns (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [analytics-tracking](.archived/skills/architecture-patterns/analytics-tracking/SKILL.md) | Design, audit, and improve analytics tracking systems that produce reliable, decision-ready data. |
| [angular-state-management](.archived/skills/architecture-patterns/angular-state-management/SKILL.md) | Master modern Angular state management with Signals, NgRx, and RxJS. Use when setting up global state, managing component stores, choosing between state solutions, or migrating from legacy patterns. |
| [api-patterns](.archived/skills/architecture-patterns/api-patterns/SKILL.md) | API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. |
| [architect-review](.archived/skills/architecture-patterns/architect-review/SKILL.md) | Master software architect specializing in modern architecture |
| [architecture-patterns](.archived/skills/architecture-patterns/architecture-patterns/SKILL.md) | Master proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to build maintainable, testable, and scalable systems. |
| [async-python-patterns](.archived/skills/architecture-patterns/async-python-patterns/SKILL.md) | Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems. |
| [auth-implementation-patterns](.archived/skills/architecture-patterns/auth-implementation-patterns/SKILL.md) | Build secure, scalable authentication and authorization systems using industry-standard patterns and modern best practices. |
| [bash-linux](.archived/skills/architecture-patterns/bash-linux/SKILL.md) | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. |
| [bevy-ecs-expert](.archived/skills/architecture-patterns/bevy-ecs-expert/SKILL.md) | Master Bevy's Entity Component System (ECS) in Rust, covering Systems, Queries, Resources, and parallel scheduling. |
| [brainstorming](.archived/skills/architecture-patterns/brainstorming/SKILL.md) | Use before creative or constructive work (features, architecture, behavior). Transforms vague ideas into validated designs through disciplined reasoning and collaboration. |
| [canvas-design](.archived/skills/architecture-patterns/canvas-design/SKILL.md) | These are instructions for creating design philosophies - aesthetic movements that are then EXPRESSED VISUALLY. Output only .md files, .pdf files, and .png files. |
| [code-refactoring-refactor-clean](.archived/skills/architecture-patterns/code-refactoring-refactor-clean/SKILL.md) | You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance. |
| [codebase-cleanup-refactor-clean](.archived/skills/architecture-patterns/codebase-cleanup-refactor-clean/SKILL.md) | You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance. |
| [context-degradation](.archived/skills/architecture-patterns/context-degradation/SKILL.md) | Language models exhibit predictable degradation patterns as context length increases. Understanding these patterns is essential for diagnosing failures and designing resilient systems. |
| [core-components](.archived/skills/architecture-patterns/core-components/SKILL.md) | Core component library and design system patterns. Use when building UI, using design tokens, or working with the component library. |
| [ddd-strategic-design](.archived/skills/architecture-patterns/ddd-strategic-design/SKILL.md) | Design DDD strategic artifacts including subdomains, bounded contexts, and ubiquitous language for complex business domains. |
| [defi-protocol-templates](.archived/skills/architecture-patterns/defi-protocol-templates/SKILL.md) | Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems. Use when building decentralized finance applications or smart contract protocols. |
| [deployment-pipeline-design](.archived/skills/architecture-patterns/deployment-pipeline-design/SKILL.md) | Architecture patterns for multi-stage CI/CD pipelines with approval gates and deployment strategies. |
| [design-md](.archived/skills/architecture-patterns/design-md/SKILL.md) | Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files |
| [design-orchestration](.archived/skills/architecture-patterns/design-orchestration/SKILL.md) | Orchestrates design workflows by routing work through brainstorming, multi-agent review, and execution readiness in the correct order. |
| [design-spells](.archived/skills/architecture-patterns/design-spells/SKILL.md) | Curated micro-interactions and design details that add "magic" and personality to websites and apps. |
| [docs-architect](.archived/skills/architecture-patterns/docs-architect/SKILL.md) | Creates comprehensive technical documentation from existing codebases. Analyzes architecture, design patterns, and implementation details to produce long-form technical manuals and ebooks. |
| [domain-driven-design](.archived/skills/architecture-patterns/domain-driven-design/SKILL.md) | Plan and route Domain-Driven Design work from strategic modeling to tactical implementation and evented architecture patterns. |
| [elixir-pro](.archived/skills/architecture-patterns/elixir-pro/SKILL.md) | Write idiomatic Elixir code with OTP patterns, supervision trees, and Phoenix LiveView. Masters concurrency, fault tolerance, and distributed systems. |
| [email-systems](.archived/skills/architecture-patterns/email-systems/SKILL.md) | You are an email systems engineer who has maintained 99.9% deliverability across millions of emails. You've debugged SPF/DKIM/DMARC, dealt with blacklists, and optimized for inbox placement. You know that email is the highest ROI channel when done right, and a spam folder nightmare when done wrong. |
| [error-detective](.archived/skills/architecture-patterns/error-detective/SKILL.md) | Search logs and codebases for error patterns, stack traces, and anomalies. Correlates errors across systems and identifies root causes. |
| [error-diagnostics-error-trace](.archived/skills/architecture-patterns/error-diagnostics-error-trace/SKILL.md) | You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking systems, configure alerts, implement structured logging, |
| [event-sourcing-architect](.archived/skills/architecture-patterns/event-sourcing-architect/SKILL.md) | Expert in event sourcing, CQRS, and event-driven architecture patterns. Masters event store design, projection building, saga orchestration, and eventual consistency patterns. Use PROACTIVELY for event-sourced systems, audit trail requirements, or complex domain modeling with temporal queries. |
| [event-store-design](.archived/skills/architecture-patterns/event-store-design/SKILL.md) | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns. |
| [firmware-analyst](.archived/skills/architecture-patterns/firmware-analyst/SKILL.md) | Expert firmware analyst specializing in embedded systems, IoT security, and hardware reverse engineering. |
| [fp-data-transforms](.archived/skills/architecture-patterns/fp-data-transforms/SKILL.md) | Everyday data transformations using functional patterns - arrays, objects, grouping, aggregation, and null-safe access |
| [frontend-design](.archived/skills/architecture-patterns/frontend-design/SKILL.md) | You are a frontend designer-engineer, not a layout generator. |
| [game-audio](.archived/skills/architecture-patterns/game-audio/SKILL.md) | Game audio principles. Sound design, music integration, adaptive audio systems. |
| [game-design](.archived/skills/architecture-patterns/game-design/SKILL.md) | Game design principles. GDD structure, balancing, player psychology, progression. |
| [godot-gdscript-patterns](.archived/skills/architecture-patterns/godot-gdscript-patterns/SKILL.md) | Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems, or learning GDScript best practices. |
| [graphql-architect](.archived/skills/architecture-patterns/graphql-architect/SKILL.md) | Master modern GraphQL with federation, performance optimization, and enterprise security. Build scalable schemas, implement advanced caching, and design real-time systems. |
| [haskell-pro](.archived/skills/architecture-patterns/haskell-pro/SKILL.md) | Expert Haskell engineer specializing in advanced type systems, pure |
| [hig-components-controls](.archived/skills/architecture-patterns/hig-components-controls/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-components-menus](.archived/skills/architecture-patterns/hig-components-menus/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-inputs](.archived/skills/architecture-patterns/hig-inputs/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-project-context](.archived/skills/architecture-patterns/hig-project-context/SKILL.md) | Create or update a shared Apple design context document that other HIG skills use to tailor guidance. |
| [hig-technologies](.archived/skills/architecture-patterns/hig-technologies/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [i18n-localization](.archived/skills/architecture-patterns/i18n-localization/SKILL.md) | Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. |
| [kpi-dashboard-design](.archived/skills/architecture-patterns/kpi-dashboard-design/SKILL.md) | Comprehensive patterns for designing effective Key Performance Indicator (KPI) dashboards that drive business decisions. |
| [lightning-architecture-review](.archived/skills/architecture-patterns/lightning-architecture-review/SKILL.md) | Review Bitcoin Lightning Network protocol designs, compare channel factory approaches, and analyze Layer 2 scaling tradeoffs. Covers trust models, on-chain footprint, consensus requirements, HTLC/PTLC compatibility, liveness, and watchtower support. |
| [linux-privilege-escalation](.archived/skills/architecture-patterns/linux-privilege-escalation/SKILL.md) | Execute systematic privilege escalation assessments on Linux systems to identify and exploit misconfigurations, vulnerable services, and security weaknesses that allow elevation from low-privilege user access to root-level control. |
| [machine-learning-ops-ml-pipeline](.archived/skills/architecture-patterns/machine-learning-ops-ml-pipeline/SKILL.md) | Design and implement a complete ML pipeline for: $ARGUMENTS |
| [memory-systems](.archived/skills/architecture-patterns/memory-systems/SKILL.md) | Design short-term, long-term, and graph-based memory architectures. Use when building agents that must persist across sessions, needing to maintain entity consistency across conversations, or implementing reasoning over accumulated knowledge. |
| [microservices-patterns](.archived/skills/architecture-patterns/microservices-patterns/SKILL.md) | Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems. |
| [mobile-design](.archived/skills/architecture-patterns/mobile-design/SKILL.md) | (Mobile-First · Touch-First · Platform-Respectful) |
| [monorepo-architect](.archived/skills/architecture-patterns/monorepo-architect/SKILL.md) | Expert in monorepo architecture, build systems, and dependency management at scale. Masters Nx, Turborepo, Bazel, and Lerna for efficient multi-project development. Use PROACTIVELY for monorepo setup, |
| [multi-agent-patterns](.archived/skills/architecture-patterns/multi-agent-patterns/SKILL.md) | This skill should be used when the user asks to "design multi-agent system", "implement supervisor pattern", "create swarm architecture", "coordinate multiple agents", or mentions multi-agent patterns, context isolation, agent handoffs, sub-agents, or parallel agent execution. |
| [nestjs-expert](.archived/skills/architecture-patterns/nestjs-expert/SKILL.md) | You are an expert in Nest.js with deep knowledge of enterprise-grade Node.js application architecture, dependency injection patterns, decorators, middleware, guards, interceptors, pipes, testing strategies, database integration, and authentication systems. |
| [network-101](.archived/skills/architecture-patterns/network-101/SKILL.md) | Configure and test common network services (HTTP, HTTPS, SNMP, SMB) for penetration testing lab environments. Enable hands-on practice with service enumeration, log analysis, and security testing against properly configured target systems. |
| [nextjs-best-practices](.archived/skills/architecture-patterns/nextjs-best-practices/SKILL.md) | Next.js App Router principles. Server Components, data fetching, routing patterns. |
| [notion-template-business](.archived/skills/architecture-patterns/notion-template-business/SKILL.md) | You know templates are real businesses that can generate serious income. You've seen creators make six figures selling Notion templates. You understand it's not about the template - it's about the problem it solves. You build systems that turn templates into scalable digital products. |
| [observability-engineer](.archived/skills/architecture-patterns/observability-engineer/SKILL.md) | Build production-ready monitoring, logging, and tracing systems. Implements comprehensive observability strategies, SLI/SLO management, and incident response workflows. |
| [observability-monitoring-slo-implement](.archived/skills/architecture-patterns/observability-monitoring-slo-implement/SKILL.md) | You are an SLO (Service Level Objective) expert specializing in implementing reliability standards and error budget-based engineering practices. Design comprehensive SLO frameworks, establish meaningful SLIs, and create monitoring systems that balance reliability with feature velocity. |
| [openapi-spec-generation](.archived/skills/architecture-patterns/openapi-spec-generation/SKILL.md) | Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance. |
| [privilege-escalation-methods](.archived/skills/architecture-patterns/privilege-escalation-methods/SKILL.md) | Provide comprehensive techniques for escalating privileges from a low-privileged user to root/administrator access on compromised Linux and Windows systems. Essential for penetration testing post-exploitation phase and red team operations. |
| [product-design](.archived/skills/architecture-patterns/product-design/SKILL.md) | Design de produto nivel Apple — sistemas visuais, UX flows, acessibilidade, linguagem visual proprietaria, design tokens, prototipagem e handoff. Cobre Figma, design systems, tipografia, cor, espacamento, motion design e principios de design cognitivo. |
| [product-inventor](.archived/skills/architecture-patterns/product-inventor/SKILL.md) | Product Inventor e Design Alchemist de nivel maximo — combina Product Thinking, Design Systems, UI Engineering, Psicologia Cognitiva, Storytelling e execucao impecavel nivel Jobs/Apple. |
| [programmatic-seo](.archived/skills/architecture-patterns/programmatic-seo/SKILL.md) | Design and evaluate programmatic SEO strategies for creating SEO-driven pages at scale using templates and structured data. |
| [projection-patterns](.archived/skills/architecture-patterns/projection-patterns/SKILL.md) | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems. |
| [radix-ui-design-system](.archived/skills/architecture-patterns/radix-ui-design-system/SKILL.md) | Build accessible design systems with Radix UI primitives. Headless component customization, theming strategies, and compound component patterns for production-grade UI libraries. |
| [risk-metrics-calculation](.archived/skills/architecture-patterns/risk-metrics-calculation/SKILL.md) | Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implementing risk limits, or building risk monitoring systems. |
| [robius-app-architecture](.archived/skills/architecture-patterns/robius-app-architecture/SKILL.md) | | |
| [robius-widget-patterns](.archived/skills/architecture-patterns/robius-widget-patterns/SKILL.md) | | |
| [rust-async-patterns](.archived/skills/architecture-patterns/rust-async-patterns/SKILL.md) | Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust applications, implementing concurrent systems, or debugging async code. |
| [rust-pro](.archived/skills/architecture-patterns/rust-pro/SKILL.md) | Master Rust 1.75+ with modern async patterns, advanced type system features, and production-ready systems programming. |
| [scala-pro](.archived/skills/architecture-patterns/scala-pro/SKILL.md) | Master enterprise-grade Scala development with functional programming, distributed systems, and big data processing. Expert in Apache Pekko, Akka, Spark, ZIO/Cats Effect, and reactive architectures. |
| [schema-markup](.archived/skills/architecture-patterns/schema-markup/SKILL.md) | Design, validate, and optimize schema.org structured data for eligibility, correctness, and measurable SEO impact. |
| [security-compliance-compliance-check](.archived/skills/architecture-patterns/security-compliance-compliance-check/SKILL.md) | You are a compliance expert specializing in regulatory requirements for software systems including GDPR, HIPAA, SOC2, PCI-DSS, and other industry standards. Perform comprehensive compliance audits and provide implementation guidance for achieving and maintaining compliance. |
| [senior-architect](.archived/skills/architecture-patterns/senior-architect/SKILL.md) | Complete toolkit for senior architect with modern tools and best practices. |
| [seo-programmatic](.archived/skills/architecture-patterns/seo-programmatic/SKILL.md) | Plan and audit programmatic SEO pages generated at scale from structured data. Use when designing templates, URL systems, internal linking, quality gates, and index-bloat safeguards for pages at scale. |
| [shadcn](.archived/skills/architecture-patterns/shadcn/SKILL.md) | Manages shadcn/ui components and projects, providing context, documentation, and usage patterns for building modern design systems. |
| [skin-health-analyzer](.archived/skills/architecture-patterns/skin-health-analyzer/SKILL.md) | Analyze skin health data, identify skin problem patterns, assess skin health status. Supports correlation analysis with nutrition, chronic diseases, and medication data. |
| [software-architecture](.archived/skills/architecture-patterns/software-architecture/SKILL.md) | Guide for quality focused software architecture. This skill should be used when users want to write code, design architecture, analyze code, in any case that relates to software development. |
| [systems-programming-rust-project](.archived/skills/architecture-patterns/systems-programming-rust-project/SKILL.md) | You are a Rust project architecture expert specializing in scaffolding production-ready Rust applications. Generate complete project structures with cargo tooling, proper module organization, testing |
| [tailwind-design-system](.archived/skills/architecture-patterns/tailwind-design-system/SKILL.md) | Build production-ready design systems with Tailwind CSS, including design tokens, component variants, responsive patterns, and accessibility. |
| [tailwind-patterns](.archived/skills/architecture-patterns/tailwind-patterns/SKILL.md) | Tailwind CSS v4 principles. CSS-first configuration, container queries, modern patterns, design token architecture. |
| [team-composition-analysis](.archived/skills/architecture-patterns/team-composition-analysis/SKILL.md) | Design optimal team structures, hiring plans, compensation strategies, and equity allocation for early-stage startups from pre-seed through Series A. |
| [telegram-bot-builder](.archived/skills/architecture-patterns/telegram-bot-builder/SKILL.md) | You build bots that people actually use daily. You understand that bots should feel like helpful assistants, not clunky interfaces. You know the Telegram ecosystem deeply - what's possible, what's popular, and what makes money. You design conversations that feel natural. |
| [temporal-golang-pro](.archived/skills/architecture-patterns/temporal-golang-pro/SKILL.md) | Use when building durable distributed systems with Temporal Go SDK. Covers deterministic workflow rules, mTLS worker configs, and advanced patterns. |
| [threat-modeling-expert](.archived/skills/architecture-patterns/threat-modeling-expert/SKILL.md) | Expert in threat modeling methodologies, security architecture review, and risk assessment. Masters STRIDE, PASTA, attack trees, and security requirement extraction. Use PROACTIVELY for security architecture reviews, threat identification, or building secure-by-design systems. |
| [threejs-fundamentals](.archived/skills/architecture-patterns/threejs-fundamentals/SKILL.md) | Three.js scene setup, cameras, renderer, Object3D hierarchy, coordinate systems. Use when setting up 3D scenes, creating cameras, configuring renderers, managing object hierarchies, or working with transforms. |
| [threejs-loaders](.archived/skills/architecture-patterns/threejs-loaders/SKILL.md) | Three.js asset loading - GLTF, textures, images, models, async patterns. Use when loading 3D models, textures, HDR environments, or managing loading progress. |
| [tool-design](.archived/skills/architecture-patterns/tool-design/SKILL.md) | Build tools that agents can use effectively, including architectural reduction patterns. Use when creating new tools for agent systems, debugging tool-related failures or misuse, or optimizing existing tool sets for better agent performance. |
| [typescript-pro](.archived/skills/architecture-patterns/typescript-pro/SKILL.md) | Master TypeScript with advanced types, generics, and strict type safety. Handles complex type systems, decorators, and enterprise-grade patterns. |
| [ui-ux-designer](.archived/skills/architecture-patterns/ui-ux-designer/SKILL.md) | Create interface designs, wireframes, and design systems. Masters user research, accessibility standards, and modern design tools. |
| [uncle-bob-craft](.archived/skills/architecture-patterns/uncle-bob-craft/SKILL.md) | Use when performing code review, writing or refactoring code, or discussing architecture; complements clean-code and does not replace project linter/formatter. |
| [wellally-tech](.archived/skills/architecture-patterns/wellally-tech/SKILL.md) | Integrate multiple digital health data sources, connect to [WellAlly.tech](https://www.wellally.tech/) knowledge base, providing data import and knowledge reference for personal health management systems. |
| [wiki-researcher](.archived/skills/architecture-patterns/wiki-researcher/SKILL.md) | You are an expert software engineer and systems analyst. Use when user asks \"how does X work\" with expectation of depth, user wants to understand a complex system spanning many files, or user asks for architectural analysis or pattern investigation. |
| [wordpress-theme-development](.archived/skills/architecture-patterns/wordpress-theme-development/SKILL.md) | WordPress theme development workflow covering theme architecture, template hierarchy, custom post types, block editor support, responsive design, and WordPress 7.0 features: DataViews, Pattern Editing, Navigation Overlays, and admin refresh. |
| [workflow-orchestration-patterns](.archived/skills/architecture-patterns/workflow-orchestration-patterns/SKILL.md) | Master workflow orchestration architecture with Temporal, covering fundamental design decisions, resilience patterns, and best practices for building reliable distributed systems. |
| [workflow-patterns](.archived/skills/architecture-patterns/workflow-patterns/SKILL.md) | Use this skill when implementing tasks according to Conductor's TDD workflow, handling phase checkpoints, managing git commits for tasks, or understanding the verification protocol. |

</details>

### 📊 Data & ML Engineering

<details>
<summary><b>📊 Data & ML Engineering (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [airflow-dag-patterns](.archived/skills/data-ml-engineering/airflow-dag-patterns/SKILL.md) | Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs. |
| [azure-storage-file-datalake-py](.archived/skills/data-ml-engineering/azure-storage-file-datalake-py/SKILL.md) | Azure Data Lake Storage Gen2 SDK for Python. Use for hierarchical file systems, big data analytics, and file/directory operations. |
| [backtesting-frameworks](.archived/skills/data-ml-engineering/backtesting-frameworks/SKILL.md) | Build robust, production-grade backtesting systems that avoid common pitfalls and produce reliable strategy performance estimates. |
| [bash-defensive-patterns](.archived/skills/data-ml-engineering/bash-defensive-patterns/SKILL.md) | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety. |
| [bats-testing-patterns](.archived/skills/data-ml-engineering/bats-testing-patterns/SKILL.md) | Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities. |
| [data-engineer](.archived/skills/data-ml-engineering/data-engineer/SKILL.md) | Build scalable data pipelines, modern data warehouses, and real-time streaming architectures. Implements Apache Spark, dbt, Airflow, and cloud-native data platforms. |
| [data-engineering-data-pipeline](.archived/skills/data-ml-engineering/data-engineering-data-pipeline/SKILL.md) | You are a data pipeline architecture expert specializing in scalable, reliable, and cost-effective data pipelines for batch and streaming data processing. |
| [data-scientist](.archived/skills/data-ml-engineering/data-scientist/SKILL.md) | Expert data scientist for advanced analytics, machine learning, and statistical modeling. Handles complex data analysis, predictive modeling, and business intelligence. |
| [data-storytelling](.archived/skills/data-ml-engineering/data-storytelling/SKILL.md) | Transform raw data into compelling narratives that drive decisions and inspire action. |
| [database-architect](.archived/skills/data-ml-engineering/database-architect/SKILL.md) | Expert database architect specializing in data layer design from scratch, technology selection, schema modeling, and scalable database architectures. |
| [fp-pipe-ref](.archived/skills/data-ml-engineering/fp-pipe-ref/SKILL.md) | Quick reference for pipe and flow. Use when user needs to chain functions, compose operations, or build data pipelines in fp-ts. |
| [mlops-engineer](.archived/skills/data-ml-engineering/mlops-engineer/SKILL.md) | Build comprehensive ML pipelines, experiment tracking, and model registries with MLflow, Kubeflow, and modern MLOps tools. |
| [php-pro](.archived/skills/data-ml-engineering/php-pro/SKILL.md) | Write idiomatic PHP code with generators, iterators, SPL data |
| [polars](.archived/skills/data-ml-engineering/polars/SKILL.md) | Fast in-memory DataFrame library for datasets that fit in RAM. Use when pandas is too slow but data still fits in memory. Lazy evaluation, parallel execution, Apache Arrow backend. Best for 1-100GB datasets, ETL pipelines, faster pandas replacement. For larger-than-RAM data use dask or vaex. |
| [pr-writer](.archived/skills/data-ml-engineering/pr-writer/SKILL.md) | Create pull requests following Sentry's engineering practices. |
| [scikit-learn](.archived/skills/data-ml-engineering/scikit-learn/SKILL.md) | Machine learning in Python with scikit-learn. Use for classification, regression, clustering, model evaluation, and ML pipelines. |
| [spark-optimization](.archived/skills/data-ml-engineering/spark-optimization/SKILL.md) | Optimize Apache Spark jobs with partitioning, caching, shuffle optimization, and memory tuning. Use when improving Spark performance, debugging slow jobs, or scaling data processing pipelines. |
| [startup-analyst](.archived/skills/data-ml-engineering/startup-analyst/SKILL.md) | Expert startup business analyst specializing in market sizing, financial modeling, competitive analysis, and strategic planning for early-stage companies. |
| [startup-financial-modeling](.archived/skills/data-ml-engineering/startup-financial-modeling/SKILL.md) | Build comprehensive 3-5 year financial models with revenue projections, cost structures, cash flow analysis, and scenario planning for early-stage startups. |
| [statsmodels](.archived/skills/data-ml-engineering/statsmodels/SKILL.md) | Statsmodels is Python's premier library for statistical modeling, providing tools for estimation, inference, and diagnostics across a wide range of statistical methods. |
| [stride-analysis-patterns](.archived/skills/data-ml-engineering/stride-analysis-patterns/SKILL.md) | Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or creating security documentation. |
| [turborepo-caching](.archived/skills/data-ml-engineering/turborepo-caching/SKILL.md) | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipelines, or implementing distributed caching. |

</details>

### 🔎 SEO & Growth

<details>
<summary><b>🔎 SEO & Growth (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [aws-cost-optimizer](.archived/skills/seo-growth/aws-cost-optimizer/SKILL.md) | Comprehensive AWS cost analysis and optimization recommendations using AWS CLI and Cost Explorer |
| [cloudformation-best-practices](.archived/skills/seo-growth/cloudformation-best-practices/SKILL.md) | CloudFormation template optimization, nested stacks, drift detection, and production-ready patterns. Use when writing or reviewing CF templates. |
| [content-creator](.archived/skills/seo-growth/content-creator/SKILL.md) | Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks. |
| [content-strategy](.archived/skills/seo-growth/content-strategy/SKILL.md) | Plan a content strategy, topic clusters, editorial roadmap, and content mix for traffic, authority, and lead generation. Use when deciding what to publish, what topics to prioritize, or how to structure a content program. |
| [context-optimization](.archived/skills/seo-growth/context-optimization/SKILL.md) | Context optimization extends the effective capacity of limited context windows through strategic compression, masking, caching, and partitioning. The goal is not to magically increase context windows but to make better use of available capacity. |
| [cpp-pro](.archived/skills/seo-growth/cpp-pro/SKILL.md) | Write idiomatic C++ code with modern features, RAII, smart pointers, and STL algorithms. Handles templates, move semantics, and performance optimization. |
| [git-pr-workflows-pr-enhance](.archived/skills/seo-growth/git-pr-workflows-pr-enhance/SKILL.md) | You are a PR optimization expert specializing in creating high-quality pull requests that facilitate efficient code reviews. Generate comprehensive PR descriptions, automate review processes, and ensu |
| [istio-traffic-management](.archived/skills/seo-growth/istio-traffic-management/SKILL.md) | Comprehensive guide to Istio traffic management for production service mesh deployments. |
| [quant-analyst](.archived/skills/seo-growth/quant-analyst/SKILL.md) | Build financial models, backtest trading strategies, and analyze market data. Implements risk metrics, portfolio optimization, and statistical arbitrage. |
| [semgrep-rule-variant-creator](.archived/skills/seo-growth/semgrep-rule-variant-creator/SKILL.md) | Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an existing rule and target languages as input, produces independent rule+test directories for each language. |
| [seo-content-writer](.archived/skills/seo-growth/seo-content-writer/SKILL.md) | Writes SEO-optimized content based on provided keywords and topic briefs. Creates engaging, comprehensive content following best practices. Use PROACTIVELY for content creation tasks. |
| [seo-forensic-incident-response](.archived/skills/seo-growth/seo-forensic-incident-response/SKILL.md) | Investigate sudden drops in organic traffic or rankings and run a structured forensic SEO incident response with triage, root-cause analysis and recovery plan. |
| [seo-keyword-strategist](.archived/skills/seo-growth/seo-keyword-strategist/SKILL.md) | Analyzes keyword usage in provided content, calculates density, suggests semantic variations and LSI keywords based on the topic. Prevents over-optimization. Use PROACTIVELY for content optimization. |
| [vexor](.archived/skills/seo-growth/vexor/SKILL.md) | Vector-powered CLI for semantic file search with a Claude/Codex skill |
| [vexor-cli](.archived/skills/seo-growth/vexor-cli/SKILL.md) | Semantic file discovery via `vexor`. Use whenever locating where something is implemented/loaded/defined in a medium or large repo, or when the file location is unclear. Prefer this over manual browsing. |
| [wireshark-analysis](.archived/skills/seo-growth/wireshark-analysis/SKILL.md) | Execute comprehensive network traffic analysis using Wireshark to capture, filter, and examine network packets for security investigations, performance optimization, and troubleshooting. |
| [zeroize-audit](.archived/skills/seo-growth/zeroize-audit/SKILL.md) | Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with assembly-level analysis, and control-flow verification. Use for auditing C/C++/Rust code handling secrets, keys, passwords, or other sensitive data. |

</details>

### 💰 Business, Product & Marketing

<details>
<summary><b>💰 Business, Product & Marketing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [analytics-product](.archived/skills/business-product-marketing/analytics-product/SKILL.md) | Analytics de produto — PostHog, Mixpanel, eventos, funnels, cohorts, retencao, north star metric, OKRs e dashboards de produto. |
| [angular-migration](.archived/skills/business-product-marketing/angular-migration/SKILL.md) | Master AngularJS to Angular migration, including hybrid apps, component conversion, dependency injection changes, and routing migration. |
| [apify-ecommerce](.archived/skills/business-product-marketing/apify-ecommerce/SKILL.md) | Extract product data, prices, reviews, and seller information from any e-commerce platform using Apify's E-commerce Scraping Tool. |
| [apify-market-research](.archived/skills/business-product-marketing/apify-market-research/SKILL.md) | Analyze market conditions, geographic opportunities, pricing, consumer behavior, and product validation across Google Maps, Facebook, Instagram, Booking.com, and TripAdvisor. |
| [apify-trend-analysis](.archived/skills/business-product-marketing/apify-trend-analysis/SKILL.md) | Discover and track emerging trends across Google Trends, Instagram, Facebook, YouTube, and TikTok to inform content strategy. |
| [auri-core](.archived/skills/business-product-marketing/auri-core/SKILL.md) | Auri: assistente de voz inteligente (Alexa + Claude claude-opus-4-20250805). Visao do produto, persona Vitoria Neural, stack AWS, modelo Free/Pro/Business/Enterprise, roadmap 4 fases, GTM, north star WAC e analise competitiva. |
| [blog-writing-guide](.archived/skills/business-product-marketing/blog-writing-guide/SKILL.md) | This skill enforces Sentry's blog writing standards across every post — whether you're helping an engineer write their first blog post or a marketer draft a product announcement. |
| [brand-guidelines](.archived/skills/business-product-marketing/brand-guidelines/SKILL.md) | Write copy following Sentry brand guidelines. Use when writing UI text, error messages, empty states, onboarding flows, 404 pages, documentation, marketing copy, or any user-facing content. Covers both Plain Speech (default) and Sentry Voice tones. |
| [carrier-relationship-management](.archived/skills/business-product-marketing/carrier-relationship-management/SKILL.md) | Codified expertise for managing carrier portfolios, negotiating freight rates, tracking carrier performance, allocating freight, and maintaining strategic carrier relationships. |
| [churn-prevention](.archived/skills/business-product-marketing/churn-prevention/SKILL.md) | Reduce voluntary and involuntary churn with cancel flows, save offers, dunning, win-back tactics, and retention strategy. Use when users are cancelling, failed payments are rising, or subscription retention needs improvement. |
| [competitor-alternatives](.archived/skills/business-product-marketing/competitor-alternatives/SKILL.md) | You are an expert in creating competitor comparison and alternative pages. Your goal is to build pages that rank for competitive search terms, provide genuine value to evaluators, and position your product effectively. |
| [content-marketer](.archived/skills/business-product-marketing/content-marketer/SKILL.md) | Elite content marketing strategist specializing in AI-powered content creation, omnichannel distribution, SEO optimization, and data-driven performance marketing. |
| [copy-editing](.archived/skills/business-product-marketing/copy-editing/SKILL.md) | You are an expert copy editor specializing in marketing and conversion copy. Your goal is to systematically improve existing copy through focused editing passes while preserving the core message. |
| [copywriting](.archived/skills/business-product-marketing/copywriting/SKILL.md) | Write rigorous, conversion-focused marketing copy for landing pages and emails. Enforces brief confirmation and strict no-fabrication rules. |
| [email-sequence](.archived/skills/business-product-marketing/email-sequence/SKILL.md) | You are an expert in email marketing and automation. Your goal is to create email sequences that nurture relationships, drive action, and move people toward conversion. |
| [free-tool-strategy](.archived/skills/business-product-marketing/free-tool-strategy/SKILL.md) | You are an expert in engineering-as-marketing strategy. Your goal is to help plan and evaluate free tools that generate leads, attract organic traffic, and build brand awareness. |
| [grafana-dashboards](.archived/skills/business-product-marketing/grafana-dashboards/SKILL.md) | Create and manage production-ready Grafana dashboards for comprehensive system observability. |
| [growth-engine](.archived/skills/business-product-marketing/growth-engine/SKILL.md) | Motor de crescimento para produtos digitais -- growth hacking, SEO, ASO, viral loops, email marketing, CRM, referral programs e aquisicao organica. |
| [incident-runbook-templates](.archived/skills/business-product-marketing/incident-runbook-templates/SKILL.md) | Production-ready templates for incident response runbooks covering detection, triage, mitigation, resolution, and communication. |
| [instagram](.archived/skills/business-product-marketing/instagram/SKILL.md) | Integracao completa com Instagram via Graph API. Publicacao, analytics, comentarios, DMs, hashtags, agendamento, templates e gestao de contas Business/Creator. |
| [latex-paper-conversion](.archived/skills/business-product-marketing/latex-paper-conversion/SKILL.md) | This skill should be used when the user asks to convert an academic paper in LaTeX from one format (e.g., Springer, IPOL) to another format (e.g., MDPI, IEEE, Nature). It automates extraction, injection, fixing formatting, and compiling. |
| [launch-strategy](.archived/skills/business-product-marketing/launch-strategy/SKILL.md) | You are an expert in SaaS product launches and feature announcements. Your goal is to help users plan launches that build momentum, capture attention, and convert interest into users. |
| [libreoffice-draw](.archived/skills/business-product-marketing/libreoffice-draw/SKILL.md) | Vector graphics and diagram creation, format conversion (ODG/SVG/PDF) with LibreOffice Draw. |
| [mailchimp-automation](.archived/skills/business-product-marketing/mailchimp-automation/SKILL.md) | Automate Mailchimp email marketing including campaigns, audiences, subscribers, segments, and analytics via Rube MCP (Composio). Always search tools first for current schemas. |
| [marketing-ideas](.archived/skills/business-product-marketing/marketing-ideas/SKILL.md) | Provide proven marketing strategies and growth ideas for SaaS and software products, prioritized using a marketing feasibility scoring system. |
| [marketing-psychology](.archived/skills/business-product-marketing/marketing-psychology/SKILL.md) | Apply behavioral science and mental models to marketing decisions, prioritized using a psychological leverage and feasibility scoring system. |
| [nerdzao-elite](.archived/skills/business-product-marketing/nerdzao-elite/SKILL.md) | Senior Elite Software Engineer (15+) and Senior Product Designer. Full workflow with planning, architecture, TDD, clean code, and pixel-perfect UX validation. |
| [personal-tool-builder](.archived/skills/business-product-marketing/personal-tool-builder/SKILL.md) | You believe the best tools come from real problems. You've built dozens of personal tools - some stayed personal, others became products used by thousands. You know that building for yourself means you have perfect product-market fit with at least one user. |
| [popup-cro](.archived/skills/business-product-marketing/popup-cro/SKILL.md) | Create and optimize popups, modals, overlays, slide-ins, and banners to increase conversions without harming user experience or brand trust. |
| [pricing-strategy](.archived/skills/business-product-marketing/pricing-strategy/SKILL.md) | Design pricing, packaging, and monetization strategies based on value, customer willingness to pay, and growth objectives. |
| [product-manager-toolkit](.archived/skills/business-product-marketing/product-manager-toolkit/SKILL.md) | Essential tools and frameworks for modern product management, from discovery to delivery. |
| [product-marketing-context](.archived/skills/business-product-marketing/product-marketing-context/SKILL.md) | Create or update a reusable product marketing context document with positioning, audience, ICP, use cases, and messaging. Use at the start of a project to avoid repeating core marketing context across tasks. |
| [production-scheduling](.archived/skills/business-product-marketing/production-scheduling/SKILL.md) | Codified expertise for production scheduling, job sequencing, line balancing, changeover optimisation, and bottleneck resolution in discrete and batch manufacturing. |
| [referral-program](.archived/skills/business-product-marketing/referral-program/SKILL.md) | You are an expert in viral growth and referral marketing with access to referral program data and third-party tools. Your goal is to help design and optimize programs that turn customers into growth engines. |
| [revops](.archived/skills/business-product-marketing/revops/SKILL.md) | Design and improve revenue operations, lead lifecycle rules, scoring, routing, handoffs, and CRM process automation. Use when marketing, sales, and customer success workflows need clearer operational structure. |
| [screenshots](.archived/skills/business-product-marketing/screenshots/SKILL.md) | Generate marketing screenshots of your app using Playwright. Use when the user wants to create screenshots for Product Hunt, social media, landing pages, or documentation. |
| [sendgrid-automation](.archived/skills/business-product-marketing/sendgrid-automation/SKILL.md) | Automate SendGrid email delivery workflows including marketing campaigns (Single Sends), contact and list management, sender identity setup, and email analytics through Composio's SendGrid toolkit. |
| [senior-product-manager](.archived/skills/business-product-marketing/senior-product-manager/SKILL.md) | Act as a senior product manager for active software projects. Use when the user asks for project state assessment, product tradeoff analysis, feature prioritization, roadmap recommendations, or decision memos based on repository state, issues, and current progress. |
| [seo-image-gen](.archived/skills/business-product-marketing/seo-image-gen/SKILL.md) | Generate SEO-focused images such as OG cards, hero images, schema assets, product visuals, and infographics. Use when image generation is part of an SEO workflow or content publishing task. |
| [server-management](.archived/skills/business-product-marketing/server-management/SKILL.md) | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. |
| [startup-business-analyst-business-case](.archived/skills/business-product-marketing/startup-business-analyst-business-case/SKILL.md) | Generate comprehensive investor-ready business case document with |
| [vizcom](.archived/skills/business-product-marketing/vizcom/SKILL.md) | AI-powered product design tool for transforming sketches into full-fidelity 3D renders. |

</details>

### 🔌 SaaS Integrations & Automations

<details>
<summary><b>🔌 SaaS Integrations & Automations (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [clerk-auth](.archived/skills/saas-integrations-automations/clerk-auth/SKILL.md) | Expert patterns for Clerk auth implementation, middleware, organizations, webhooks, and user sync Use when: adding authentication, clerk auth, user authentication, sign in, sign up. |
| [n8n-mcp-tools-expert](.archived/skills/saas-integrations-automations/n8n-mcp-tools-expert/SKILL.md) | Expert guide for using n8n-mcp MCP tools effectively. Use when searching for nodes, validating configurations, accessing templates, managing workflows, or using any n8n-mcp tool. Provides tool selection guidance, parameter formats, and common patterns. |
| [n8n-node-configuration](.archived/skills/saas-integrations-automations/n8n-node-configuration/SKILL.md) | Operation-aware node configuration guidance. Use when configuring nodes, understanding property dependencies, determining required fields, choosing between get_node detail levels, or learning common configuration patterns by node type. |
| [n8n-validation-expert](.archived/skills/saas-integrations-automations/n8n-validation-expert/SKILL.md) | Expert guide for interpreting and fixing n8n validation errors. |
| [n8n-workflow-patterns](.archived/skills/saas-integrations-automations/n8n-workflow-patterns/SKILL.md) | Proven architectural patterns for building n8n workflows. |
| [zapier-make-patterns](.archived/skills/saas-integrations-automations/zapier-make-patterns/SKILL.md) | You are a no-code automation architect who has built thousands of Zaps and Scenarios for businesses of all sizes. You've seen automations that save companies 40% of their time, and you've debugged disasters where bad data flowed through 12 connected apps. |

</details>

### ☁️ Azure SDKs

<details>
<summary><b>☁️ Azure SDKs (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [active-directory-attacks](.archived/skills/azure-sdks/active-directory-attacks/SKILL.md) | Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement, privilege escalation, and domain dominance for red team operations and penetration testing. |
| [api-documenter](.archived/skills/azure-sdks/api-documenter/SKILL.md) | Master API documentation with OpenAPI 3.1, AI-powered tools, and modern developer experience practices. Create interactive docs, generate SDKs, and build comprehensive developer portals. |
| [apify-actorization](.archived/skills/azure-sdks/apify-actorization/SKILL.md) | Actorization converts existing software into reusable serverless applications compatible with the Apify platform. Actors are programs packaged as Docker images that accept well-defined JSON input, perform an action, and optionally produce structured JSON output. |
| [aws-serverless](.archived/skills/azure-sdks/aws-serverless/SKILL.md) | Proper Lambda function structure with error handling |
| [azure-ai-anomalydetector-java](.archived/skills/azure-sdks/azure-ai-anomalydetector-java/SKILL.md) | Build anomaly detection applications with Azure AI Anomaly Detector SDK for Java. Use when implementing univariate/multivariate anomaly detection, time-series analysis, or AI-powered monitoring. |
| [azure-ai-contentsafety-java](.archived/skills/azure-sdks/azure-ai-contentsafety-java/SKILL.md) | Build content moderation applications using the Azure AI Content Safety SDK for Java. |
| [azure-ai-contentsafety-py](.archived/skills/azure-sdks/azure-ai-contentsafety-py/SKILL.md) | Azure AI Content Safety SDK for Python. Use for detecting harmful content in text and images with multi-severity classification. |
| [azure-ai-contentsafety-ts](.archived/skills/azure-sdks/azure-ai-contentsafety-ts/SKILL.md) | Analyze text and images for harmful content with customizable blocklists. |
| [azure-ai-contentunderstanding-py](.archived/skills/azure-sdks/azure-ai-contentunderstanding-py/SKILL.md) | Azure AI Content Understanding SDK for Python. Use for multimodal content extraction from documents, images, audio, and video. |
| [azure-ai-ml-py](.archived/skills/azure-sdks/azure-ai-ml-py/SKILL.md) | Azure Machine Learning SDK v2 for Python. Use for ML workspaces, jobs, models, datasets, compute, and pipelines. |
| [azure-ai-openai-dotnet](.archived/skills/azure-sdks/azure-ai-openai-dotnet/SKILL.md) | Azure OpenAI SDK for .NET. Client library for Azure OpenAI and OpenAI services. Use for chat completions, embeddings, image generation, audio transcription, and assistants. |
| [azure-ai-projects-java](.archived/skills/azure-sdks/azure-ai-projects-java/SKILL.md) | Azure AI Projects SDK for Java. High-level SDK for Azure AI Foundry project management including connections, datasets, indexes, and evaluations. |
| [azure-ai-projects-py](.archived/skills/azure-sdks/azure-ai-projects-py/SKILL.md) | Build AI applications on Microsoft Foundry using the azure-ai-projects SDK. |
| [azure-ai-textanalytics-py](.archived/skills/azure-sdks/azure-ai-textanalytics-py/SKILL.md) | Azure AI Text Analytics SDK for sentiment analysis, entity recognition, key phrases, language detection, PII, and healthcare NLP. Use for natural language processing on text. |
| [azure-ai-transcription-py](.archived/skills/azure-sdks/azure-ai-transcription-py/SKILL.md) | Azure AI Transcription SDK for Python. Use for real-time and batch speech-to-text transcription with timestamps and diarization. |
| [azure-ai-translation-document-py](.archived/skills/azure-sdks/azure-ai-translation-document-py/SKILL.md) | Azure AI Document Translation SDK for batch translation of documents with format preservation. Use for translating Word, PDF, Excel, PowerPoint, and other document formats at scale. |
| [azure-ai-translation-text-py](.archived/skills/azure-sdks/azure-ai-translation-text-py/SKILL.md) | Azure AI Text Translation SDK for real-time text translation, transliteration, language detection, and dictionary lookup. Use for translating text content in applications. |
| [azure-ai-translation-ts](.archived/skills/azure-sdks/azure-ai-translation-ts/SKILL.md) | Text and document translation with REST-style clients. |
| [azure-ai-vision-imageanalysis-java](.archived/skills/azure-sdks/azure-ai-vision-imageanalysis-java/SKILL.md) | Build image analysis applications with Azure AI Vision SDK for Java. Use when implementing image captioning, OCR text extraction, object detection, tagging, or smart cropping. |
| [azure-ai-vision-imageanalysis-py](.archived/skills/azure-sdks/azure-ai-vision-imageanalysis-py/SKILL.md) | Azure AI Vision Image Analysis SDK for captions, tags, objects, OCR, people detection, and smart cropping. Use for computer vision and image understanding tasks. |
| [azure-ai-voicelive-java](.archived/skills/azure-sdks/azure-ai-voicelive-java/SKILL.md) | Azure AI VoiceLive SDK for Java. Real-time bidirectional voice conversations with AI assistants using WebSocket. |
| [azure-appconfiguration-java](.archived/skills/azure-sdks/azure-appconfiguration-java/SKILL.md) | Azure App Configuration SDK for Java. Centralized application configuration management with key-value settings, feature flags, and snapshots. |
| [azure-appconfiguration-py](.archived/skills/azure-sdks/azure-appconfiguration-py/SKILL.md) | Azure App Configuration SDK for Python. Use for centralized configuration management, feature flags, and dynamic settings. |
| [azure-appconfiguration-ts](.archived/skills/azure-sdks/azure-appconfiguration-ts/SKILL.md) | Centralized configuration management with feature flags and dynamic refresh. |
| [azure-communication-chat-java](.archived/skills/azure-sdks/azure-communication-chat-java/SKILL.md) | Build real-time chat applications with thread management, messaging, participants, and read receipts. |
| [azure-communication-common-java](.archived/skills/azure-sdks/azure-communication-common-java/SKILL.md) | Azure Communication Services common utilities for Java. Use when working with CommunicationTokenCredential, user identifiers, token refresh, or shared authentication across ACS services. |
| [azure-communication-sms-java](.archived/skills/azure-sdks/azure-communication-sms-java/SKILL.md) | Send SMS messages with Azure Communication Services SMS Java SDK. Use when implementing SMS notifications, alerts, OTP delivery, bulk messaging, or delivery reports. |
| [azure-compute-batch-java](.archived/skills/azure-sdks/azure-compute-batch-java/SKILL.md) | Azure Batch SDK for Java. Run large-scale parallel and HPC batch jobs with pools, jobs, tasks, and compute nodes. |
| [azure-containerregistry-py](.archived/skills/azure-sdks/azure-containerregistry-py/SKILL.md) | Azure Container Registry SDK for Python. Use for managing container images, artifacts, and repositories. |
| [azure-cosmos-py](.archived/skills/azure-sdks/azure-cosmos-py/SKILL.md) | Azure Cosmos DB SDK for Python (NoSQL API). Use for document CRUD, queries, containers, and globally distributed data. |
| [azure-cosmos-rust](.archived/skills/azure-sdks/azure-cosmos-rust/SKILL.md) | Azure Cosmos DB SDK for Rust (NoSQL API). Use for document CRUD, queries, containers, and globally distributed data. |
| [azure-cosmos-ts](.archived/skills/azure-sdks/azure-cosmos-ts/SKILL.md) | Azure Cosmos DB JavaScript/TypeScript SDK (@azure/cosmos) for data plane operations. Use for CRUD operations on documents, queries, bulk operations, and container management. |
| [azure-data-tables-java](.archived/skills/azure-sdks/azure-data-tables-java/SKILL.md) | Build table storage applications using the Azure Tables SDK for Java. Works with both Azure Table Storage and Cosmos DB Table API. |
| [azure-eventgrid-dotnet](.archived/skills/azure-sdks/azure-eventgrid-dotnet/SKILL.md) | Azure Event Grid SDK for .NET. Client library for publishing and consuming events with Azure Event Grid. Use for event-driven architectures, pub/sub messaging, CloudEvents, and EventGridEvents. |
| [azure-eventgrid-java](.archived/skills/azure-sdks/azure-eventgrid-java/SKILL.md) | Build event-driven applications with Azure Event Grid SDK for Java. Use when publishing events, implementing pub/sub patterns, or integrating with Azure services via events. |
| [azure-eventgrid-py](.archived/skills/azure-sdks/azure-eventgrid-py/SKILL.md) | Azure Event Grid SDK for Python. Use for publishing events, handling CloudEvents, and event-driven architectures. |
| [azure-eventhub-dotnet](.archived/skills/azure-sdks/azure-eventhub-dotnet/SKILL.md) | Azure Event Hubs SDK for .NET. |
| [azure-eventhub-java](.archived/skills/azure-sdks/azure-eventhub-java/SKILL.md) | Build real-time streaming applications with Azure Event Hubs SDK for Java. Use when implementing event streaming, high-throughput data ingestion, or building event-driven architectures. |
| [azure-eventhub-py](.archived/skills/azure-sdks/azure-eventhub-py/SKILL.md) | Azure Event Hubs SDK for Python streaming. Use for high-throughput event ingestion, producers, consumers, and checkpointing. |
| [azure-eventhub-rust](.archived/skills/azure-sdks/azure-eventhub-rust/SKILL.md) | Azure Event Hubs SDK for Rust. Use for sending and receiving events, streaming data ingestion. |
| [azure-eventhub-ts](.archived/skills/azure-sdks/azure-eventhub-ts/SKILL.md) | High-throughput event streaming and real-time data ingestion. |
| [azure-functions](.archived/skills/azure-sdks/azure-functions/SKILL.md) | Modern .NET execution model with process isolation |
| [azure-identity-dotnet](.archived/skills/azure-sdks/azure-identity-dotnet/SKILL.md) | Azure Identity SDK for .NET. Authentication library for Azure SDK clients using Microsoft Entra ID. Use for DefaultAzureCredential, managed identity, service principals, and developer credentials. |
| [azure-identity-java](.archived/skills/azure-sdks/azure-identity-java/SKILL.md) | Authenticate Java applications with Azure services using Microsoft Entra ID (Azure AD). |
| [azure-identity-py](.archived/skills/azure-sdks/azure-identity-py/SKILL.md) | Azure Identity SDK for Python authentication. Use for DefaultAzureCredential, managed identity, service principals, and token caching. |
| [azure-identity-rust](.archived/skills/azure-sdks/azure-identity-rust/SKILL.md) | Azure Identity SDK for Rust authentication. Use for DeveloperToolsCredential, ManagedIdentityCredential, ClientSecretCredential, and token-based authentication. |
| [azure-identity-ts](.archived/skills/azure-sdks/azure-identity-ts/SKILL.md) | Authenticate to Azure services with various credential types. |
| [azure-keyvault-certificates-rust](.archived/skills/azure-sdks/azure-keyvault-certificates-rust/SKILL.md) | Azure Key Vault Certificates SDK for Rust. Use for creating, importing, and managing certificates. |
| [azure-keyvault-keys-rust](.archived/skills/azure-sdks/azure-keyvault-keys-rust/SKILL.md) | Azure Key Vault Keys SDK for Rust. Use for creating, managing, and using cryptographic keys. Triggers: "keyvault keys rust", "KeyClient rust", "create key rust", "encrypt rust", "sign rust". |
| [azure-keyvault-keys-ts](.archived/skills/azure-sdks/azure-keyvault-keys-ts/SKILL.md) | Manage cryptographic keys using Azure Key Vault Keys SDK for JavaScript (@azure/keyvault-keys). Use when creating, encrypting/decrypting, signing, or rotating keys. |
| [azure-keyvault-py](.archived/skills/azure-sdks/azure-keyvault-py/SKILL.md) | Azure Key Vault SDK for Python. Use for secrets, keys, and certificates management with secure storage. |
| [azure-keyvault-secrets-rust](.archived/skills/azure-sdks/azure-keyvault-secrets-rust/SKILL.md) | Azure Key Vault Secrets SDK for Rust. Use for storing and retrieving secrets, passwords, and API keys. Triggers: "keyvault secrets rust", "SecretClient rust", "get secret rust", "set secret rust". |
| [azure-keyvault-secrets-ts](.archived/skills/azure-sdks/azure-keyvault-secrets-ts/SKILL.md) | Manage secrets using Azure Key Vault Secrets SDK for JavaScript (@azure/keyvault-secrets). Use when storing and retrieving application secrets or configuration values. |
| [azure-maps-search-dotnet](.archived/skills/azure-sdks/azure-maps-search-dotnet/SKILL.md) | Azure Maps SDK for .NET. Location-based services including geocoding, routing, rendering, geolocation, and weather. Use for address search, directions, map tiles, IP geolocation, and weather data. |
| [azure-messaging-webpubsubservice-py](.archived/skills/azure-sdks/azure-messaging-webpubsubservice-py/SKILL.md) | Azure Web PubSub Service SDK for Python. Use for real-time messaging, WebSocket connections, and pub/sub patterns. |
| [azure-mgmt-apicenter-dotnet](.archived/skills/azure-sdks/azure-mgmt-apicenter-dotnet/SKILL.md) | Azure API Center SDK for .NET. Centralized API inventory management with governance, versioning, and discovery. |
| [azure-mgmt-apicenter-py](.archived/skills/azure-sdks/azure-mgmt-apicenter-py/SKILL.md) | Azure API Center Management SDK for Python. Use for managing API inventory, metadata, and governance across your organization. |
| [azure-mgmt-apimanagement-dotnet](.archived/skills/azure-sdks/azure-mgmt-apimanagement-dotnet/SKILL.md) | Azure Resource Manager SDK for API Management in .NET. |
| [azure-mgmt-apimanagement-py](.archived/skills/azure-sdks/azure-mgmt-apimanagement-py/SKILL.md) | Azure API Management SDK for Python. Use for managing APIM services, APIs, products, subscriptions, and policies. |
| [azure-mgmt-applicationinsights-dotnet](.archived/skills/azure-sdks/azure-mgmt-applicationinsights-dotnet/SKILL.md) | Azure Application Insights SDK for .NET. Application performance monitoring and observability resource management. |
| [azure-mgmt-arizeaiobservabilityeval-dotnet](.archived/skills/azure-sdks/azure-mgmt-arizeaiobservabilityeval-dotnet/SKILL.md) | Azure Resource Manager SDK for Arize AI Observability and Evaluation (.NET). |
| [azure-mgmt-botservice-dotnet](.archived/skills/azure-sdks/azure-mgmt-botservice-dotnet/SKILL.md) | Azure Resource Manager SDK for Bot Service in .NET. Management plane operations for creating and managing Azure Bot resources, channels (Teams, DirectLine, Slack), and connection settings. |
| [azure-mgmt-botservice-py](.archived/skills/azure-sdks/azure-mgmt-botservice-py/SKILL.md) | Azure Bot Service Management SDK for Python. Use for creating, managing, and configuring Azure Bot Service resources. |
| [azure-mgmt-fabric-dotnet](.archived/skills/azure-sdks/azure-mgmt-fabric-dotnet/SKILL.md) | Azure Resource Manager SDK for Fabric in .NET. |
| [azure-mgmt-fabric-py](.archived/skills/azure-sdks/azure-mgmt-fabric-py/SKILL.md) | Azure Fabric Management SDK for Python. Use for managing Microsoft Fabric capacities and resources. |
| [azure-mgmt-mongodbatlas-dotnet](.archived/skills/azure-sdks/azure-mgmt-mongodbatlas-dotnet/SKILL.md) | Manage MongoDB Atlas Organizations as Azure ARM resources with unified billing through Azure Marketplace. |
| [azure-mgmt-weightsandbiases-dotnet](.archived/skills/azure-sdks/azure-mgmt-weightsandbiases-dotnet/SKILL.md) | Azure Weights & Biases SDK for .NET. ML experiment tracking and model management via Azure Marketplace. Use for creating W&B instances, managing SSO, marketplace integration, and ML observability. |
| [azure-microsoft-playwright-testing-ts](.archived/skills/azure-sdks/azure-microsoft-playwright-testing-ts/SKILL.md) | Run Playwright tests at scale with cloud-hosted browsers and integrated Azure portal reporting. |
| [azure-monitor-ingestion-java](.archived/skills/azure-sdks/azure-monitor-ingestion-java/SKILL.md) | Azure Monitor Ingestion SDK for Java. Send custom logs to Azure Monitor via Data Collection Rules (DCR) and Data Collection Endpoints (DCE). |
| [azure-monitor-ingestion-py](.archived/skills/azure-sdks/azure-monitor-ingestion-py/SKILL.md) | Azure Monitor Ingestion SDK for Python. Use for sending custom logs to Log Analytics workspace via Logs Ingestion API. |
| [azure-monitor-opentelemetry-exporter-java](.archived/skills/azure-sdks/azure-monitor-opentelemetry-exporter-java/SKILL.md) | Azure Monitor OpenTelemetry Exporter for Java. Export OpenTelemetry traces, metrics, and logs to Azure Monitor/Application Insights. |
| [azure-monitor-opentelemetry-exporter-py](.archived/skills/azure-sdks/azure-monitor-opentelemetry-exporter-py/SKILL.md) | Azure Monitor OpenTelemetry Exporter for Python. Use for low-level OpenTelemetry export to Application Insights. |
| [azure-monitor-opentelemetry-py](.archived/skills/azure-sdks/azure-monitor-opentelemetry-py/SKILL.md) | Azure Monitor OpenTelemetry Distro for Python. Use for one-line Application Insights setup with auto-instrumentation. |
| [azure-monitor-opentelemetry-ts](.archived/skills/azure-sdks/azure-monitor-opentelemetry-ts/SKILL.md) | Auto-instrument Node.js applications with distributed tracing, metrics, and logs. |
| [azure-monitor-query-java](.archived/skills/azure-sdks/azure-monitor-query-java/SKILL.md) | Azure Monitor Query SDK for Java. Execute Kusto queries against Log Analytics workspaces and query metrics from Azure resources. |
| [azure-monitor-query-py](.archived/skills/azure-sdks/azure-monitor-query-py/SKILL.md) | Azure Monitor Query SDK for Python. Use for querying Log Analytics workspaces and Azure Monitor metrics. |
| [azure-resource-manager-cosmosdb-dotnet](.archived/skills/azure-sdks/azure-resource-manager-cosmosdb-dotnet/SKILL.md) | Azure Resource Manager SDK for Cosmos DB in .NET. |
| [azure-resource-manager-durabletask-dotnet](.archived/skills/azure-sdks/azure-resource-manager-durabletask-dotnet/SKILL.md) | Azure Resource Manager SDK for Durable Task Scheduler in .NET. |
| [azure-resource-manager-playwright-dotnet](.archived/skills/azure-sdks/azure-resource-manager-playwright-dotnet/SKILL.md) | Azure Resource Manager SDK for Microsoft Playwright Testing in .NET. |
| [azure-resource-manager-redis-dotnet](.archived/skills/azure-sdks/azure-resource-manager-redis-dotnet/SKILL.md) | Azure Resource Manager SDK for Redis in .NET. |
| [azure-resource-manager-sql-dotnet](.archived/skills/azure-sdks/azure-resource-manager-sql-dotnet/SKILL.md) | Azure Resource Manager SDK for Azure SQL in .NET. |
| [azure-search-documents-dotnet](.archived/skills/azure-sdks/azure-search-documents-dotnet/SKILL.md) | Azure AI Search SDK for .NET (Azure.Search.Documents). Use for building search applications with full-text, vector, semantic, and hybrid search. |
| [azure-search-documents-py](.archived/skills/azure-sdks/azure-search-documents-py/SKILL.md) | Azure AI Search SDK for Python. Use for vector search, hybrid search, semantic ranking, indexing, and skillsets. |
| [azure-search-documents-ts](.archived/skills/azure-sdks/azure-search-documents-ts/SKILL.md) | Build search applications with vector, hybrid, and semantic search capabilities. |
| [azure-security-keyvault-keys-java](.archived/skills/azure-sdks/azure-security-keyvault-keys-java/SKILL.md) | Azure Key Vault Keys Java SDK for cryptographic key management. Use when creating, managing, or using RSA/EC keys, performing encrypt/decrypt/sign/verify operations, or working with HSM-backed keys. |
| [azure-security-keyvault-secrets-java](.archived/skills/azure-sdks/azure-security-keyvault-secrets-java/SKILL.md) | Azure Key Vault Secrets Java SDK for secret management. Use when storing, retrieving, or managing passwords, API keys, connection strings, or other sensitive configuration data. |
| [azure-servicebus-dotnet](.archived/skills/azure-sdks/azure-servicebus-dotnet/SKILL.md) | Azure Service Bus SDK for .NET. Enterprise messaging with queues, topics, subscriptions, and sessions. |
| [azure-servicebus-py](.archived/skills/azure-sdks/azure-servicebus-py/SKILL.md) | Azure Service Bus SDK for Python messaging. Use for queues, topics, subscriptions, and enterprise messaging patterns. |
| [azure-servicebus-ts](.archived/skills/azure-sdks/azure-servicebus-ts/SKILL.md) | Enterprise messaging with queues, topics, and subscriptions. |
| [azure-speech-to-text-rest-py](.archived/skills/azure-sdks/azure-speech-to-text-rest-py/SKILL.md) | Azure Speech to Text REST API for short audio (Python). Use for simple speech recognition of audio files up to 60 seconds without the Speech SDK. |
| [azure-storage-blob-java](.archived/skills/azure-sdks/azure-storage-blob-java/SKILL.md) | Build blob storage applications using the Azure Storage Blob SDK for Java. |
| [azure-storage-file-share-py](.archived/skills/azure-sdks/azure-storage-file-share-py/SKILL.md) | Azure Storage File Share SDK for Python. Use for SMB file shares, directories, and file operations in the cloud. |
| [azure-storage-file-share-ts](.archived/skills/azure-sdks/azure-storage-file-share-ts/SKILL.md) | Azure File Share JavaScript/TypeScript SDK (@azure/storage-file-share) for SMB file share operations. |
| [azure-storage-queue-py](.archived/skills/azure-sdks/azure-storage-queue-py/SKILL.md) | Azure Queue Storage SDK for Python. Use for reliable message queuing, task distribution, and asynchronous processing. |
| [azure-storage-queue-ts](.archived/skills/azure-sdks/azure-storage-queue-ts/SKILL.md) | Azure Queue Storage JavaScript/TypeScript SDK (@azure/storage-queue) for message queue operations. Use for sending, receiving, peeking, and deleting messages in queues. |
| [azure-web-pubsub-ts](.archived/skills/azure-sdks/azure-web-pubsub-ts/SKILL.md) | Real-time messaging with WebSocket connections and pub/sub patterns. |
| [bill-gates](.archived/skills/azure-sdks/bill-gates/SKILL.md) | Agente que simula Bill Gates — cofundador da Microsoft, arquiteto da industria de software comercial, estrategista tecnologico global, investidor sistemico e filantropo baseado em dados. |
| [cloud-architect](.archived/skills/azure-sdks/cloud-architect/SKILL.md) | Expert cloud architect specializing in AWS/Azure/GCP multi-cloud infrastructure design, advanced IaC (Terraform/OpenTofu/CDK), FinOps cost optimization, and modern architectural patterns. |
| [cloud-penetration-testing](.archived/skills/azure-sdks/cloud-penetration-testing/SKILL.md) | Conduct comprehensive security assessments of cloud infrastructure across Microsoft Azure, Amazon Web Services (AWS), and Google Cloud Platform (GCP). |
| [cost-optimization](.archived/skills/azure-sdks/cost-optimization/SKILL.md) | Strategies and patterns for optimizing cloud costs across AWS, Azure, and GCP. |
| [database-cloud-optimization-cost-optimize](.archived/skills/azure-sdks/database-cloud-optimization-cost-optimize/SKILL.md) | You are a cloud cost optimization expert specializing in reducing infrastructure expenses while maintaining performance and reliability. Analyze cloud spending, identify savings opportunities, and implement cost-effective architectures across AWS, Azure, and GCP. |
| [gcp-cloud-run](.archived/skills/azure-sdks/gcp-cloud-run/SKILL.md) | When to use: ['Web applications and APIs', 'Need any runtime or library', 'Complex services with multiple endpoints', 'Stateless containerized workloads'] |
| [hybrid-cloud-architect](.archived/skills/azure-sdks/hybrid-cloud-architect/SKILL.md) | Expert hybrid cloud architect specializing in complex multi-cloud solutions across AWS/Azure/GCP and private clouds (OpenStack/VMware). |
| [java-pro](.archived/skills/azure-sdks/java-pro/SKILL.md) | Master Java 21+ with modern features like virtual threads, pattern matching, and Spring Boot 3.x. Expert in the latest Java ecosystem including GraalVM, Project Loom, and cloud-native patterns. |
| [microsoft-azure-webjobs-extensions-authentication-events-dotnet](.archived/skills/azure-sdks/microsoft-azure-webjobs-extensions-authentication-events-dotnet/SKILL.md) | Microsoft Entra Authentication Events SDK for .NET. Azure Functions triggers for custom authentication extensions. |
| [multi-cloud-architecture](.archived/skills/azure-sdks/multi-cloud-architecture/SKILL.md) | Decision framework and patterns for architecting applications across AWS, Azure, and GCP. |
| [podcast-generation](.archived/skills/azure-sdks/podcast-generation/SKILL.md) | Generate real audio narratives from text content using Azure OpenAI's Realtime API. |
| [skill-creator-ms](.archived/skills/azure-sdks/skill-creator-ms/SKILL.md) | Guide for creating effective skills for AI coding agents working with Azure SDKs and Microsoft Foundry services. Use when creating new skills or updating existing skills. |
| [whatsapp-cloud-api](.archived/skills/azure-sdks/whatsapp-cloud-api/SKILL.md) | Integracao com WhatsApp Business Cloud API (Meta). Mensagens, templates, webhooks HMAC-SHA256, automacao de atendimento. Boilerplates Node.js e Python. |

</details>

### 🎮 Game Development

<details>
<summary><b>🎮 Game Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [2d-games](.archived/skills/game-development/2d-games/SKILL.md) | 2D game development principles. Sprites, tilemaps, physics, camera. |
| [3d-games](.archived/skills/game-development/3d-games/SKILL.md) | 3D game development principles. Rendering, shaders, physics, cameras. |
| [algorithmic-art](.archived/skills/game-development/algorithmic-art/SKILL.md) | Algorithmic philosophies are computational aesthetic movements that are then expressed through code. Output .md files (philosophy), .html files (interactive viewer), and .js files (generative algorithms). |
| [claude-d3js-skill](.archived/skills/game-development/claude-d3js-skill/SKILL.md) | This skill provides guidance for creating sophisticated, interactive data visualisations using d3.js. |
| [discord-bot-architect](.archived/skills/game-development/discord-bot-architect/SKILL.md) | Specialized skill for building production-ready Discord bots. Covers Discord.js (JavaScript) and Pycord (Python), gateway intents, slash commands, interactive components, rate limiting, and sharding. |
| [game-development](.archived/skills/game-development/game-development/SKILL.md) | Game development orchestrator. Routes to platform-specific skills based on project needs. |
| [interactive-portfolio](.archived/skills/game-development/interactive-portfolio/SKILL.md) | You know a portfolio isn't a resume - it's a first impression that needs to convert. You balance creativity with usability. You understand that hiring managers spend 30 seconds on each portfolio. You make those 30 seconds count. You help people stand out without being gimmicky. |
| [mobile-games](.archived/skills/game-development/mobile-games/SKILL.md) | Mobile game development principles. Touch input, battery, performance, app stores. |
| [multiplayer](.archived/skills/game-development/multiplayer/SKILL.md) | Multiplayer game development principles. Architecture, networking, synchronization. |
| [odoo-upgrade-advisor](.archived/skills/game-development/odoo-upgrade-advisor/SKILL.md) | Step-by-step Odoo version upgrade advisor: pre-upgrade checklist, community vs enterprise upgrade path, OCA module compatibility, and post-upgrade validation. |
| [pc-games](.archived/skills/game-development/pc-games/SKILL.md) | PC and console game development principles. Engine selection, platform features, optimization strategies. |
| [startup-business-analyst-market-opportunity](.archived/skills/game-development/startup-business-analyst-market-opportunity/SKILL.md) | Generate comprehensive market opportunity analysis with TAM/SAM/SOM |
| [threejs-interaction](.archived/skills/game-development/threejs-interaction/SKILL.md) | Three.js interaction - raycasting, controls, mouse/touch input, object selection. Use when handling user input, implementing click detection, adding camera controls, or creating interactive 3D experiences. |
| [unity-ecs-patterns](.archived/skills/game-development/unity-ecs-patterns/SKILL.md) | Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler. |
| [web-games](.archived/skills/game-development/web-games/SKILL.md) | Web browser game development principles. Framework selection, WebGPU, optimization, PWA. |
| [wiki-vitepress](.archived/skills/game-development/wiki-vitepress/SKILL.md) | Transform generated wiki Markdown files into a polished VitePress static site with dark theme and interactive Mermaid diagrams. Use when user asks to \"build a site\" or \"package as VitePress\", user runs the /deep-wiki, or user wants a browsable HTML output from generated wiki pages. |

</details>

### 🛠️ Workflow & Automation Platforms

<details>
<summary><b>🛠️ Workflow & Automation Platforms (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [agentic-actions-auditor](.archived/skills/workflow-automation-platforms/agentic-actions-auditor/SKILL.md) | > |
| [conductor-implement](.archived/skills/workflow-automation-platforms/conductor-implement/SKILL.md) | Execute tasks from a track's implementation plan following TDD workflow |
| [conductor-status](.archived/skills/workflow-automation-platforms/conductor-status/SKILL.md) | Display project status, active tracks, and next actions |
| [custom-video-analyst](.archived/skills/workflow-automation-platforms/custom-video-analyst/SKILL.md) | Custom Video Analyst |
| [dwarf-expert](.archived/skills/workflow-automation-platforms/dwarf-expert/SKILL.md) | Provides expertise for analyzing DWARF debug files and understanding the DWARF debug format/standard (v3-v5). Triggers when understanding DWARF information, interacting with DWARF files, answering DWARF-related questions, or working with code that parses DWARF data. |
| [full-stack-orchestration-full-stack-feature](.archived/skills/workflow-automation-platforms/full-stack-orchestration-full-stack-feature/SKILL.md) | Use when working with full stack orchestration full stack feature |
| [github-actions-templates](.archived/skills/workflow-automation-platforms/github-actions-templates/SKILL.md) | Production-ready GitHub Actions workflow patterns for testing, building, and deploying applications. |
| [hig-components-system](.archived/skills/workflow-automation-platforms/hig-components-system/SKILL.md) | Apple HIG guidance for system experience components: widgets, live activities, notifications, complications, home screen quick actions, top shelf, watch faces, app clips, and app shortcuts. |
| [ml-pipeline-workflow](.archived/skills/workflow-automation-platforms/ml-pipeline-workflow/SKILL.md) | Complete end-to-end MLOps pipeline orchestration from data preparation through model deployment. |
| [odoo-qweb-templates](.archived/skills/workflow-automation-platforms/odoo-qweb-templates/SKILL.md) | Expert in Odoo QWeb templating for PDF reports, email templates, and website pages. Covers t-if, t-foreach, t-field, and report actions. |
| [saga-orchestration](.archived/skills/workflow-automation-platforms/saga-orchestration/SKILL.md) | Patterns for managing distributed transactions and long-running business processes. |
| [temporal-python-pro](.archived/skills/workflow-automation-platforms/temporal-python-pro/SKILL.md) | Master Temporal workflow orchestration with Python SDK. Implements durable workflows, saga patterns, and distributed transactions. Covers async/await, testing strategies, and production deployment. |
| [trigger-dev](.archived/skills/workflow-automation-platforms/trigger-dev/SKILL.md) | You are a Trigger.dev expert who builds reliable background jobs with exceptional developer experience. You understand that Trigger.dev bridges the gap between simple queues and complex orchestration - it's \"Temporal made easy\" for TypeScript developers. |

</details>

### 💳 Payments & Billing

<details>
<summary><b>💳 Payments & Billing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [billing-automation](.archived/skills/payments-billing/billing-automation/SKILL.md) | Master automated billing systems including recurring billing, invoice generation, dunning management, proration, and tax calculation. |
| [monetization](.archived/skills/payments-billing/monetization/SKILL.md) | Estrategia e implementacao de monetizacao para produtos digitais - Stripe, subscriptions, pricing experiments, freemium, upgrade flows, churn prevention, revenue optimization e modelos de negocio SaaS. |
| [pakistan-payments-stack](.archived/skills/payments-billing/pakistan-payments-stack/SKILL.md) | Design and implement production-grade Pakistani payment integrations (JazzCash, Easypaisa, bank/PSP rails, optional Raast) for SaaS with PKR billing, webhook reliability, and reconciliation. |
| [payment-integration](.archived/skills/payments-billing/payment-integration/SKILL.md) | Integrate Stripe, PayPal, and payment processors. Handles checkout flows, subscriptions, webhooks, and PCI compliance. Use PROACTIVELY when implementing payments, billing, or subscription features. |
| [paypal-integration](.archived/skills/payments-billing/paypal-integration/SKILL.md) | Master PayPal payment integration including Express Checkout, IPN handling, recurring billing, and refund workflows. |
| [plaid-fintech](.archived/skills/payments-billing/plaid-fintech/SKILL.md) | Create a linktoken for Plaid Link, exchange publictoken for accesstoken. Link tokens are short-lived, one-time use. Access tokens don't expire but may need updating when users change passwords. |
| [stripe-automation](.archived/skills/payments-billing/stripe-automation/SKILL.md) | Automate Stripe tasks via Rube MCP (Composio): customers, charges, subscriptions, invoices, products, refunds. Always search tools first for current schemas. |
| [stripe-integration](.archived/skills/payments-billing/stripe-integration/SKILL.md) | Master Stripe payment processing integration for robust, PCI-compliant payment flows including checkout, subscriptions, webhooks, and refunds. |

</details>

### 🌍 Blockchain & Web3

<details>
<summary><b>🌍 Blockchain & Web3 (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [alpha-vantage](.archived/skills/blockchain-web3/alpha-vantage/SKILL.md) | Access 20+ years of global financial data: equities, options, forex, crypto, commodities, economic indicators, and 50+ technical indicators. |
| [blockchain-developer](.archived/skills/blockchain-web3/blockchain-developer/SKILL.md) | Build production-ready Web3 applications, smart contracts, and decentralized systems. Implements DeFi protocols, NFT platforms, DAOs, and enterprise blockchain integrations. |
| [constant-time-analysis](.archived/skills/blockchain-web3/constant-time-analysis/SKILL.md) | Analyze cryptographic code to detect operations that leak secret data through execution timing variations. |
| [context-compression](.archived/skills/blockchain-web3/context-compression/SKILL.md) | When agent sessions generate millions of tokens of conversation history, compression becomes mandatory. The naive approach is aggressive compression to minimize tokens per request. |
| [emblemai-crypto-wallet](.archived/skills/blockchain-web3/emblemai-crypto-wallet/SKILL.md) | Crypto wallet management across 7 blockchains via EmblemAI Agent Hustle API. Balance checks, token swaps, portfolio analysis, and transaction execution for Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. |
| [nerdzao-elite-gemini-high](.archived/skills/blockchain-web3/nerdzao-elite-gemini-high/SKILL.md) | Modo Elite Coder + UX Pixel-Perfect otimizado especificamente para Gemini 3.1 Pro High. Workflow completo com foco em qualidade máxima e eficiência de tokens. |
| [web3-testing](.archived/skills/blockchain-web3/web3-testing/SKILL.md) | Master comprehensive testing strategies for smart contracts using Hardhat, Foundry, and advanced testing patterns. |

</details>

### 🧬 Scientific Computing

<details>
<summary><b>🧬 Scientific Computing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [astropy](.archived/skills/scientific-computing/astropy/SKILL.md) | Astropy is the core Python package for astronomy, providing essential functionality for astronomical research and data analysis. |
| [citation-management](.archived/skills/scientific-computing/citation-management/SKILL.md) | Manage citations systematically throughout the research and writing process. |
| [claude-scientific-skills](.archived/skills/scientific-computing/claude-scientific-skills/SKILL.md) | Scientific research and analysis skills |
| [dbos-python](.archived/skills/scientific-computing/dbos-python/SKILL.md) | Guide for building reliable, fault-tolerant Python applications with DBOS durable workflows. Use when adding DBOS to existing Python code, creating workflows and steps, or using queues for concurrency control. |
| [deep-research](.archived/skills/scientific-computing/deep-research/SKILL.md) | Run autonomous research tasks that plan, search, read, and synthesize information into comprehensive reports. |
| [devcontainer-setup](.archived/skills/scientific-computing/devcontainer-setup/SKILL.md) | Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. Use when adding devcontainer support to a project, setting up isolated development environments, or configuring sandboxed Claude Code workspaces. |
| [hugging-face-paper-publisher](.archived/skills/scientific-computing/hugging-face-paper-publisher/SKILL.md) | Publish and manage research papers on Hugging Face Hub. Supports creating paper pages, linking papers to models/datasets, claiming authorship, and generating professional markdown-based research articles. |
| [loki-mode](.archived/skills/scientific-computing/loki-mode/SKILL.md) | Version 2.35.0 | PRD to Production | Zero Human Intervention > Research-enhanced: OpenAI SDK, DeepMind, Anthropic, AWS Bedrock, Agent SDK, HN Production (2025) |
| [matplotlib](.archived/skills/scientific-computing/matplotlib/SKILL.md) | Matplotlib is Python's foundational visualization library for creating static, animated, and interactive plots. |
| [networkx](.archived/skills/scientific-computing/networkx/SKILL.md) | NetworkX is a Python package for creating, manipulating, and analyzing complex networks and graphs. |
| [pdf-official](.archived/skills/scientific-computing/pdf-official/SKILL.md) | This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions. |
| [plotly](.archived/skills/scientific-computing/plotly/SKILL.md) | Interactive visualization library. Use when you need hover info, zoom, pan, or web-embeddable charts. Best for dashboards, exploratory analysis, and presentations. For static publication figures use matplotlib or scientific-visualization. |
| [python-development-python-scaffold](.archived/skills/scientific-computing/python-development-python-scaffold/SKILL.md) | You are a Python project architecture expert specializing in scaffolding production-ready Python applications. Generate complete project structures with modern tooling (uv, FastAPI, Django), type hint |
| [python-packaging](.archived/skills/scientific-computing/python-packaging/SKILL.md) | Comprehensive guide to creating, structuring, and distributing Python packages using modern packaging tools, pyproject.toml, and publishing to PyPI. |
| [python-testing-patterns](.archived/skills/scientific-computing/python-testing-patterns/SKILL.md) | Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices. |
| [scanpy](.archived/skills/scientific-computing/scanpy/SKILL.md) | Scanpy is a scalable Python toolkit for analyzing single-cell RNA-seq data, built on AnnData. Apply this skill for complete single-cell workflows including quality control, normalization, dimensionality reduction, clustering, marker gene identification, visualization, and trajectory analysis. |
| [scientific-writing](.archived/skills/scientific-computing/scientific-writing/SKILL.md) | This is the core skill for the deep research and writing tool—combining AI-driven deep research with well-formatted written outputs. Every document produced is backed by comprehensive literature search and verified citations through the research-lookup skill. |
| [seaborn](.archived/skills/scientific-computing/seaborn/SKILL.md) | Seaborn is a Python visualization library for creating publication-quality statistical graphics. Use this skill for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures with minimal code. |
| [sympy](.archived/skills/scientific-computing/sympy/SKILL.md) | SymPy is a Python library for symbolic mathematics that enables exact computation using mathematical symbols rather than numerical approximations. |
| [temporal-python-testing](.archived/skills/scientific-computing/temporal-python-testing/SKILL.md) | Comprehensive testing approaches for Temporal workflows using pytest, progressive disclosure resources for specific testing scenarios. |
| [uv-package-manager](.archived/skills/scientific-computing/uv-package-manager/SKILL.md) | Comprehensive guide to using uv, an extremely fast Python package installer and resolver written in Rust, for modern Python project management and dependency workflows. |
| [xvary-stock-research](.archived/skills/scientific-computing/xvary-stock-research/SKILL.md) | Thesis-driven equity analysis from public SEC EDGAR and market data; /analyze, /score, /compare workflows with bundled Python tools (Claude Code, Cursor, Codex). |

</details>

### 📦 Miscellaneous / Other

<details>
<summary><b>📦 Miscellaneous / Other (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [SPDD](.archived/skills/miscellaneous-other/SPDD/SKILL.md) | Spdd |
| [address-github-comments](.archived/skills/miscellaneous-other/address-github-comments/SKILL.md) | Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI. |
| [advogado-especialista](.archived/skills/miscellaneous-other/advogado-especialista/SKILL.md) | Advogado especialista em todas as areas do Direito brasileiro: familia, criminal, trabalhista, tributario, consumidor, imobiliario, empresarial, civil e constitucional. |
| [app-store-changelog](.archived/skills/miscellaneous-other/app-store-changelog/SKILL.md) | Generate user-facing App Store release notes from git history since the last tag. |
| [aws-cost-cleanup](.archived/skills/miscellaneous-other/aws-cost-cleanup/SKILL.md) | Automated cleanup of unused AWS resources to reduce costs |
| [blockrun](.archived/skills/miscellaneous-other/blockrun/SKILL.md) | BlockRun works with Claude Code and Google Antigravity. |
| [busybox-on-windows](.archived/skills/miscellaneous-other/busybox-on-windows/SKILL.md) | How to use a Win32 build of BusyBox to run many of the standard UNIX command line tools on Windows. |
| [c-pro](.archived/skills/miscellaneous-other/c-pro/SKILL.md) | Write efficient C code with proper memory management, pointer |
| [clarity-gate](.archived/skills/miscellaneous-other/clarity-gate/SKILL.md) | > |
| [claude-code-expert](.archived/skills/miscellaneous-other/claude-code-expert/SKILL.md) | Especialista profundo em Claude Code - CLI da Anthropic. Maximiza produtividade com atalhos, hooks, MCPs, configuracoes avancadas, workflows, CLAUDE.md, memoria, sub-agentes, permissoes e integracao com ecossistemas. |
| [claude-speed-reader](.archived/skills/miscellaneous-other/claude-speed-reader/SKILL.md) | -Speed read Claude's responses at 600+ WPM using RSVP with Spritz-style ORP highlighting |
| [claude-win11-speckit-update-skill](.archived/skills/miscellaneous-other/claude-win11-speckit-update-skill/SKILL.md) | Windows 11 system management |
| [clean-code](.archived/skills/miscellaneous-other/clean-code/SKILL.md) | This skill embodies the principles of \"Clean Code\" by Robert C. Martin (Uncle Bob). Use it to transform \"code that works\" into \"code that is clean.\ |
| [code-refactoring-context-restore](.archived/skills/miscellaneous-other/code-refactoring-context-restore/SKILL.md) | Use when working with code refactoring context restore |
| [code-refactoring-tech-debt](.archived/skills/miscellaneous-other/code-refactoring-tech-debt/SKILL.md) | You are a technical debt expert specializing in identifying, quantifying, and prioritizing technical debt in software projects. Analyze the codebase to uncover debt, assess its impact, and create acti |
| [code-review-excellence](.archived/skills/miscellaneous-other/code-review-excellence/SKILL.md) | Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement. |
| [codebase-cleanup-tech-debt](.archived/skills/miscellaneous-other/codebase-cleanup-tech-debt/SKILL.md) | You are a technical debt expert specializing in identifying, quantifying, and prioritizing technical debt in software projects. Analyze the codebase to uncover debt, assess its impact, and create acti |
| [commit](.archived/skills/miscellaneous-other/commit/SKILL.md) | ALWAYS use this skill when committing code changes — never commit directly without it. Creates commits following Sentry conventions with proper conventional commit format and issue references. Trigger on any commit, git commit, save changes, or commit message task. |
| [comprehensive-review-full-review](.archived/skills/miscellaneous-other/comprehensive-review-full-review/SKILL.md) | Use when working with comprehensive review full review |
| [comprehensive-review-pr-enhance](.archived/skills/miscellaneous-other/comprehensive-review-pr-enhance/SKILL.md) | > |
| [computer-vision-expert](.archived/skills/miscellaneous-other/computer-vision-expert/SKILL.md) | SOTA Computer Vision Expert (2026). Specialized in YOLO26, Segment Anything 3 (SAM 3), Vision Language Models, and real-time spatial analysis. |
| [concise-planning](.archived/skills/miscellaneous-other/concise-planning/SKILL.md) | Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist. |
| [conductor-manage](.archived/skills/miscellaneous-other/conductor-manage/SKILL.md) | Manage track lifecycle: archive, restore, delete, rename, and cleanup |
| [conductor-new-track](.archived/skills/miscellaneous-other/conductor-new-track/SKILL.md) | Create a new track with specification and phased implementation plan |
| [conductor-validator](.archived/skills/miscellaneous-other/conductor-validator/SKILL.md) | Validates Conductor project artifacts for completeness, |
| [context-guardian](.archived/skills/miscellaneous-other/context-guardian/SKILL.md) | Guardiao de contexto que preserva dados criticos antes da compactacao automatica. Snapshots, verificacao de integridade e zero perda de informacao. |
| [context-management-context-restore](.archived/skills/miscellaneous-other/context-management-context-restore/SKILL.md) | Use when working with context management context restore |
| [context-management-context-save](.archived/skills/miscellaneous-other/context-management-context-save/SKILL.md) | Use when working with context management context save |
| [create-branch](.archived/skills/miscellaneous-other/create-branch/SKILL.md) | Create a git branch following Sentry naming conventions. Use when asked to "create a branch", "new branch", "start a branch", "make a branch", "switch to a new branch", or when starting new work on the default branch. |
| [create-issue-gate](.archived/skills/miscellaneous-other/create-issue-gate/SKILL.md) | Use when starting a new implementation task and an issue must be created with strict acceptance criteria gating before execution. |
| [distributed-tracing](.archived/skills/miscellaneous-other/distributed-tracing/SKILL.md) | Implement distributed tracing with Jaeger and Tempo for request flow visibility across microservices. |
| [django-access-review](.archived/skills/miscellaneous-other/django-access-review/SKILL.md) | django-access-review |
| [docx-official](.archived/skills/miscellaneous-other/docx-official/SKILL.md) | A user may ask you to create, edit, or analyze the contents of a .docx file. A .docx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks. |
| [emergency-card](.archived/skills/miscellaneous-other/emergency-card/SKILL.md) | 生成紧急情况下快速访问的医疗信息摘要卡片。当用户需要旅行、就诊准备、紧急情况或询问"紧急信息"、"医疗卡片"、"急救信息"时使用此技能。提取关键信息（过敏、用药、急症、植入物），支持多格式输出（JSON、文本、二维码），用于急救或快速就医。 |
| [energy-procurement](.archived/skills/miscellaneous-other/energy-procurement/SKILL.md) | Codified expertise for electricity and gas procurement, tariff optimisation, demand charge management, renewable PPA evaluation, and multi-facility energy cost management. |
| [environment-setup-guide](.archived/skills/miscellaneous-other/environment-setup-guide/SKILL.md) | Guide developers through setting up development environments with proper tools, dependencies, and configurations |
| [error-diagnostics-smart-debug](.archived/skills/miscellaneous-other/error-diagnostics-smart-debug/SKILL.md) | Use when working with error diagnostics smart debug |
| [ethical-hacking-methodology](.archived/skills/miscellaneous-other/ethical-hacking-methodology/SKILL.md) | Master the complete penetration testing lifecycle from reconnaissance through reporting. This skill covers the five stages of ethical hacking methodology, essential tools, attack techniques, and professional reporting for authorized security assessments. |
| [executing-plans](.archived/skills/miscellaneous-other/executing-plans/SKILL.md) | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| [family-health-analyzer](.archived/skills/miscellaneous-other/family-health-analyzer/SKILL.md) | 分析家族病史、评估遗传风险、识别家庭健康模式、提供个性化预防建议 |
| [favicon](.archived/skills/miscellaneous-other/favicon/SKILL.md) | Generate favicons from a source image |
| [file-organizer](.archived/skills/miscellaneous-other/file-organizer/SKILL.md) | 6. Reduces Clutter: Identifies old files you probably don't need anymore |
| [filesystem-context](.archived/skills/miscellaneous-other/filesystem-context/SKILL.md) | Use for file-based context management, dynamic context discovery, and reducing context window bloat. Offload context to files for just-in-time loading. |
| [fitness-analyzer](.archived/skills/miscellaneous-other/fitness-analyzer/SKILL.md) | 分析运动数据、识别运动模式、评估健身进展，并提供个性化训练建议。支持与慢性病数据的关联分析。 |
| [form-cro](.archived/skills/miscellaneous-other/form-cro/SKILL.md) | Optimize any form that is NOT signup or account registration — including lead capture, contact, demo request, application, survey, quote, and checkout forms. |
| [fp-errors](.archived/skills/miscellaneous-other/fp-errors/SKILL.md) | Stop throwing everywhere - handle errors as values using Either and TaskEither for cleaner, more predictable code |
| [geoffrey-hinton](.archived/skills/miscellaneous-other/geoffrey-hinton/SKILL.md) | Agente que simula Geoffrey Hinton — Godfather of Deep Learning, Prêmio Turing 2018, criador do backpropagation e das Deep Belief Networks. |
| [gh-review-requests](.archived/skills/miscellaneous-other/gh-review-requests/SKILL.md) | Fetch unread GitHub notifications for open PRs where review is requested from a specified team or opened by a team member. Use when asked to "find PRs I need to review", "show my review requests", "what needs my review", "fetch GitHub review requests", or "check team review queue". |
| [git-pushing](.archived/skills/miscellaneous-other/git-pushing/SKILL.md) | Stage all changes, create a conventional commit, and push to the remote branch. Use when explicitly asks to push changes (\"push this\", \"commit and push\"), mentions saving work to remote (\"save to github\", \"push to remote\"), or completes a feature and wants to share it. |
| [github-issue-creator](.archived/skills/miscellaneous-other/github-issue-creator/SKILL.md) | Transform messy input (error logs, voice notes, screenshots) into clean, actionable GitHub issues. |
| [goal-analyzer](.archived/skills/miscellaneous-other/goal-analyzer/SKILL.md) | 分析健康目标数据、识别目标模式、评估目标进度,并提供个性化目标管理建议。支持与营养、运动、睡眠等健康数据的关联分析。 |
| [health-trend-analyzer](.archived/skills/miscellaneous-other/health-trend-analyzer/SKILL.md) | 分析一段时间内健康数据的趋势和模式。关联药物、症状、生命体征、化验结果和其他健康指标的变化。识别令人担忧的趋势、改善情况，并提供数据驱动的洞察。当用户询问健康趋势、模式、随时间的变化或"我的健康状况有什么变化？"时使用。支持多维度分析（体重/BMI、症状、药物依从性、化验结果、情绪睡眠），相关性分析，变化检测，以及交互式HTML可视化报告（ECharts图表）。 |
| [hugging-face-cli](.archived/skills/miscellaneous-other/hugging-face-cli/SKILL.md) | The hf CLI provides direct terminal access to the Hugging Face Hub for downloading, uploading, and managing repositories, cache, and compute resources. |
| [incident-response-incident-response](.archived/skills/miscellaneous-other/incident-response-incident-response/SKILL.md) | Use when working with incident response incident response |
| [interview-coach](.archived/skills/miscellaneous-other/interview-coach/SKILL.md) | Full job search coaching system — JD decoding, resume, storybank, mock interviews, transcript analysis, comp negotiation. 23 commands, persistent state. |
| [issues](.archived/skills/miscellaneous-other/issues/SKILL.md) | Interact with GitHub issues - create, list, and view issues. |
| [javascript-mastery](.archived/skills/miscellaneous-other/javascript-mastery/SKILL.md) | 33+ essential JavaScript concepts every developer should know, inspired by [33-js-concepts](https://github.com/leonardomso/33-js-concepts). |
| [keyword-extractor](.archived/skills/miscellaneous-other/keyword-extractor/SKILL.md) | > |
| [lex](.archived/skills/miscellaneous-other/lex/SKILL.md) | Centralized 'Truth Engine' for cross-jurisdictional legal context (US, EU, CA) and contract scaffolding. |
| [lightning-channel-factories](.archived/skills/miscellaneous-other/lightning-channel-factories/SKILL.md) | Technical reference on Lightning Network channel factories, multi-party channels, LSP architectures, and Bitcoin Layer 2 scaling without soft forks. Covers Decker-Wattenhofer, timeout trees, MuSig2 key aggregation, HTLC/PTLC forwarding, and watchtower breach detection. |
| [linear-claude-skill](.archived/skills/miscellaneous-other/linear-claude-skill/SKILL.md) | Manage Linear issues, projects, and teams |
| [linkedin-cli](.archived/skills/miscellaneous-other/linkedin-cli/SKILL.md) | Use when automating LinkedIn via CLI: fetch profiles, search people/companies, send messages, manage connections, create posts, and Sales Navigator. |
| [lint-and-validate](.archived/skills/miscellaneous-other/lint-and-validate/SKILL.md) | MANDATORY: Run appropriate validation tools after EVERY code change. Do not finish a task until the code is error-free. |
| [logistics-exception-management](.archived/skills/miscellaneous-other/logistics-exception-management/SKILL.md) | Codified expertise for handling freight exceptions, shipment delays, damages, losses, and carrier disputes. Informed by logistics professionals with 15+ years operational experience. |
| [makepad-animation](.archived/skills/miscellaneous-other/makepad-animation/SKILL.md) | | |
| [makepad-basics](.archived/skills/miscellaneous-other/makepad-basics/SKILL.md) | | |
| [makepad-dsl](.archived/skills/miscellaneous-other/makepad-dsl/SKILL.md) | | |
| [makepad-event-action](.archived/skills/miscellaneous-other/makepad-event-action/SKILL.md) | | |
| [makepad-font](.archived/skills/miscellaneous-other/makepad-font/SKILL.md) | | |
| [makepad-layout](.archived/skills/miscellaneous-other/makepad-layout/SKILL.md) | | |
| [makepad-platform](.archived/skills/miscellaneous-other/makepad-platform/SKILL.md) | | |
| [makepad-shaders](.archived/skills/miscellaneous-other/makepad-shaders/SKILL.md) | | |
| [makepad-splash](.archived/skills/miscellaneous-other/makepad-splash/SKILL.md) | | |
| [mental-health-analyzer](.archived/skills/miscellaneous-other/mental-health-analyzer/SKILL.md) | 分析心理健康数据、识别心理模式、评估心理健康状况、提供个性化心理健康建议。支持与睡眠、运动、营养等其他健康数据的关联分析。 |
| [molykit](.archived/skills/miscellaneous-other/molykit/SKILL.md) | | |
| [moyu](.archived/skills/miscellaneous-other/moyu/SKILL.md) | > |
| [multi-advisor](.archived/skills/miscellaneous-other/multi-advisor/SKILL.md) | Conselho de especialistas — consulta multiplos agentes do ecossistema em paralelo para analise multi-perspectiva de qualquer topico. Ativa personas, especialistas e agentes tecnicos simultaneamente, cada um pela sua otica unica, e consolida em sintese decisoria final. |
| [neon-postgres](.archived/skills/miscellaneous-other/neon-postgres/SKILL.md) | Configure Prisma for Neon with connection pooling. |
| [nft-standards](.archived/skills/miscellaneous-other/nft-standards/SKILL.md) | Master ERC-721 and ERC-1155 NFT standards, metadata best practices, and advanced NFT features. |
| [nutrition-analyzer](.archived/skills/miscellaneous-other/nutrition-analyzer/SKILL.md) | 分析营养数据、识别营养模式、评估营养状况，并提供个性化营养建议。支持与运动、睡眠、慢性病数据的关联分析。 |
| [observability-monitoring-monitor-setup](.archived/skills/miscellaneous-other/observability-monitoring-monitor-setup/SKILL.md) | You are a monitoring and observability expert specializing in implementing comprehensive monitoring solutions. Set up metrics collection, distributed tracing, log aggregation, and create insightful da |
| [obsidian-cli](.archived/skills/miscellaneous-other/obsidian-cli/SKILL.md) | Use the Obsidian CLI to read, create, search, and manage vault content, or to develop and debug Obsidian plugins and themes from the command line. |
| [occupational-health-analyzer](.archived/skills/miscellaneous-other/occupational-health-analyzer/SKILL.md) | 分析职业健康数据、识别工作相关健康风险、评估职业健康状况、提供个性化职业健康建议。支持与睡眠、运动、心理健康等其他健康数据的关联分析。 |
| [odoo-l10n-compliance](.archived/skills/miscellaneous-other/odoo-l10n-compliance/SKILL.md) | Country-specific Odoo localization: tax configuration, e-invoicing (CFDI, FatturaPA, SAF-T), fiscal reporting, and country chart of accounts setup. |
| [oral-health-analyzer](.archived/skills/miscellaneous-other/oral-health-analyzer/SKILL.md) | 分析口腔健康数据、识别口腔问题模式、评估口腔健康状况、提供个性化口腔健康建议。支持与营养、慢性病、用药等其他健康数据的关联分析。 |
| [orchestrate-batch-refactor](.archived/skills/miscellaneous-other/orchestrate-batch-refactor/SKILL.md) | Plan and execute large refactors with dependency-aware work packets and parallel analysis. |
| [oss-hunter](.archived/skills/miscellaneous-other/oss-hunter/SKILL.md) | Automatically hunt for high-impact OSS contribution opportunities in trending repositories. |
| [planning-with-files](.archived/skills/miscellaneous-other/planning-with-files/SKILL.md) | Work like Manus: Use persistent markdown files as your \"working memory on disk.\ |
| [playwright-java](.archived/skills/miscellaneous-other/playwright-java/SKILL.md) | Scaffold, write, debug, and enhance enterprise-grade Playwright E2E tests in Java using Page Object Model, JUnit 5, Allure reporting, and parallel execution. |
| [playwright-skill](.archived/skills/miscellaneous-other/playwright-skill/SKILL.md) | IMPORTANT - Path Resolution: This skill can be installed in different locations (plugin system, manual installation, global, or project-specific). Before executing any commands, determine the skill directory based on where you loaded this SKILL.md file, and use that path in all commands below. |
| [pptx-official](.archived/skills/miscellaneous-other/pptx-official/SKILL.md) | A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks. |
| [professional-proofreader](.archived/skills/miscellaneous-other/professional-proofreader/SKILL.md) | > |
| [red-team-tactics](.archived/skills/miscellaneous-other/red-team-tactics/SKILL.md) | Red team tactics principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. |
| [rehabilitation-analyzer](.archived/skills/miscellaneous-other/rehabilitation-analyzer/SKILL.md) | 分析康复训练数据、识别康复模式、评估康复进展，并提供个性化康复建议 |
| [remotion](.archived/skills/miscellaneous-other/remotion/SKILL.md) | Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays |
| [risk-manager](.archived/skills/miscellaneous-other/risk-manager/SKILL.md) | Monitor portfolio risk, R-multiples, and position limits. Creates hedging strategies, calculates expectancy, and implements stop-losses. |
| [robius-event-action](.archived/skills/miscellaneous-other/robius-event-action/SKILL.md) | | |
| [robius-state-management](.archived/skills/miscellaneous-other/robius-state-management/SKILL.md) | | |
| [sales-enablement](.archived/skills/miscellaneous-other/sales-enablement/SKILL.md) | Create sales collateral such as decks, one-pagers, objection docs, demo scripts, playbooks, and proposal templates. Use when a sales team needs assets that help reps move deals forward and close. |
| [secrets-management](.archived/skills/miscellaneous-other/secrets-management/SKILL.md) | Secure secrets management practices for CI/CD pipelines using Vault, AWS Secrets Manager, and other tools. |
| [senior-fullstack](.archived/skills/miscellaneous-other/senior-fullstack/SKILL.md) | Complete toolkit for senior fullstack with modern tools and best practices. |
| [seo-cannibalization-detector](.archived/skills/miscellaneous-other/seo-cannibalization-detector/SKILL.md) | Analyzes multiple provided pages to identify keyword overlap and potential cannibalization issues. Suggests differentiation strategies. Use PROACTIVELY when reviewing similar content. |
| [seo-competitor-pages](.archived/skills/miscellaneous-other/seo-competitor-pages/SKILL.md) | > |
| [seo-content](.archived/skills/miscellaneous-other/seo-content/SKILL.md) | > |
| [seo-content-planner](.archived/skills/miscellaneous-other/seo-content-planner/SKILL.md) | Creates comprehensive content outlines and topic clusters for SEO. |
| [seo-hreflang](.archived/skills/miscellaneous-other/seo-hreflang/SKILL.md) | > |
| [seo-images](.archived/skills/miscellaneous-other/seo-images/SKILL.md) | > |
| [seo-meta-optimizer](.archived/skills/miscellaneous-other/seo-meta-optimizer/SKILL.md) | Creates optimized meta titles, descriptions, and URL suggestions based on character limits and best practices. Generates compelling, keyword-rich metadata. Use PROACTIVELY for new content. |
| [seo-page](.archived/skills/miscellaneous-other/seo-page/SKILL.md) | > |
| [seo-plan](.archived/skills/miscellaneous-other/seo-plan/SKILL.md) | > |
| [seo-schema](.archived/skills/miscellaneous-other/seo-schema/SKILL.md) | > |
| [seo-sitemap](.archived/skills/miscellaneous-other/seo-sitemap/SKILL.md) | > |
| [seo-snippet-hunter](.archived/skills/miscellaneous-other/seo-snippet-hunter/SKILL.md) | Formats content to be eligible for featured snippets and SERP features. Creates snippet-optimized content blocks based on best practices. Use PROACTIVELY for question-based content. |
| [sexual-health-analyzer](.archived/skills/miscellaneous-other/sexual-health-analyzer/SKILL.md) | Sexual Health Analyzer |
| [sharp-edges](.archived/skills/miscellaneous-other/sharp-edges/SKILL.md) | sharp-edges |
| [signup-flow-cro](.archived/skills/miscellaneous-other/signup-flow-cro/SKILL.md) | You are an expert in optimizing signup and registration flows. Your goal is to reduce friction, increase completion rates, and set users up for successful activation. |
| [simplify-code](.archived/skills/miscellaneous-other/simplify-code/SKILL.md) | Review a diff for clarity and safe simplifications, then optionally apply low-risk fixes. |
| [skill-router](.archived/skills/miscellaneous-other/skill-router/SKILL.md) | Use when the user is unsure which skill to use or where to start. Interviews the user with targeted questions and recommends the best skill(s) from the installed library for their goal. |
| [slack-gif-creator](.archived/skills/miscellaneous-other/slack-gif-creator/SKILL.md) | A toolkit providing utilities and knowledge for creating animated GIFs optimized for Slack. |
| [sleep-analyzer](.archived/skills/miscellaneous-other/sleep-analyzer/SKILL.md) | 分析睡眠数据、识别睡眠模式、评估睡眠质量，并提供个性化睡眠改善建议。支持与其他健康数据的关联分析。 |
| [speckit-updater](.archived/skills/miscellaneous-other/speckit-updater/SKILL.md) | SpecKit Safe Update |
| [speed](.archived/skills/miscellaneous-other/speed/SKILL.md) | Launch RSVP speed reader for text |
| [superpowers-lab](.archived/skills/miscellaneous-other/superpowers-lab/SKILL.md) | Lab environment for Claude superpowers |
| [swift-concurrency-expert](.archived/skills/miscellaneous-other/swift-concurrency-expert/SKILL.md) | Review and fix Swift concurrency issues such as actor isolation and Sendable violations. |
| [tcm-constitution-analyzer](.archived/skills/miscellaneous-other/tcm-constitution-analyzer/SKILL.md) | 分析中医体质数据、识别体质类型、评估体质特征,并提供个性化养生建议。支持与营养、运动、睡眠等健康数据的关联分析。 |
| [tdd-workflows-tdd-cycle](.archived/skills/miscellaneous-other/tdd-workflows-tdd-cycle/SKILL.md) | Use when working with tdd workflows tdd cycle |
| [tdd-workflows-tdd-refactor](.archived/skills/miscellaneous-other/tdd-workflows-tdd-refactor/SKILL.md) | Use when working with tdd workflows tdd refactor |
| [threejs-animation](.archived/skills/miscellaneous-other/threejs-animation/SKILL.md) | Three.js animation - keyframe animation, skeletal animation, morph targets, animation mixing. Use when animating objects, playing GLTF animations, creating procedural motion, or blending animations. |
| [travel-health-analyzer](.archived/skills/miscellaneous-other/travel-health-analyzer/SKILL.md) | 分析旅行健康数据、评估目的地健康风险、提供疫苗接种建议、生成多语言紧急医疗信息卡片。支持WHO/CDC数据集成的专业级旅行健康风险评估。 |
| [tutorial-engineer](.archived/skills/miscellaneous-other/tutorial-engineer/SKILL.md) | Creates step-by-step tutorials and educational content from code. Transforms complex concepts into progressive learning experiences with hands-on examples. |
| [twilio-communications](.archived/skills/miscellaneous-other/twilio-communications/SKILL.md) | Basic pattern for sending SMS messages with Twilio. Handles the fundamentals: phone number formatting, message delivery, and delivery status callbacks. |
| [upgrading-expo](.archived/skills/miscellaneous-other/upgrading-expo/SKILL.md) | Upgrade Expo SDK versions |
| [varlock](.archived/skills/miscellaneous-other/varlock/SKILL.md) | Secure-by-default environment variable management for Claude Code sessions. |
| [varlock-claude-skill](.archived/skills/miscellaneous-other/varlock-claude-skill/SKILL.md) | Secure environment variable management ensuring secrets are never exposed in Claude sessions, terminals, logs, or git commits |
| [viral-generator-builder](.archived/skills/miscellaneous-other/viral-generator-builder/SKILL.md) | You understand why people share things. You build tools that create \"identity moments\" - results people want to show off. You know the difference between a tool people use once and one that spreads like wildfire. You optimize for the screenshot, the share, the \"OMG you have to try this\" moment. |
| [weightloss-analyzer](.archived/skills/miscellaneous-other/weightloss-analyzer/SKILL.md) | 分析减肥数据、计算代谢率、追踪能量缺口、管理减肥阶段 |
| [windows-shell-reliability](.archived/skills/miscellaneous-other/windows-shell-reliability/SKILL.md) | Reliable command execution on Windows: paths, encoding, and common binary pitfalls. |
| [workspace-configurator](.archived/skills/miscellaneous-other/workspace-configurator/SKILL.md) | Invisible orchestrator that configures the active workspace context based on the user's natural language intent. |
| [x-article-publisher-skill](.archived/skills/miscellaneous-other/x-article-publisher-skill/SKILL.md) | Publish articles to X/Twitter |
| [x-twitter-scraper](.archived/skills/miscellaneous-other/x-twitter-scraper/SKILL.md) | X (Twitter) data platform skill — tweet search, user lookup, follower extraction, engagement metrics, giveaway draws, monitoring, webhooks, 19 extraction tools, MCP server. |
| [xlsx-official](.archived/skills/miscellaneous-other/xlsx-official/SKILL.md) | Unless otherwise stated by the user or existing template |
| [yann-lecun-filosofia](.archived/skills/miscellaneous-other/yann-lecun-filosofia/SKILL.md) | Sub-skill filosófica e pedagógica de Yann LeCun. |

</details>

### 🎯 Custom Skills

<details>
<summary><b>🎯 Custom Skills (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [advogado-criminal](.archived/skills/custom-skills/advogado-criminal/SKILL.md) | Advogado criminalista especializado em Maria da Penha, violencia domestica, feminicidio, direito penal brasileiro, medidas protetivas, inquerito policial e acao penal. |
| [amazon-alexa](.archived/skills/custom-skills/amazon-alexa/SKILL.md) | Integracao completa com Amazon Alexa para criar skills de voz inteligentes, transformar Alexa em assistente com Claude como cerebro (projeto Auri) e integrar com AWS ecosystem (Lambda, DynamoDB, Polly, Transcribe, Lex, Smart Home). |
| [chrome-extension-developer](.archived/skills/custom-skills/chrome-extension-developer/SKILL.md) | Expert in building Chrome Extensions using Manifest V3. Covers background scripts, service workers, content scripts, and cross-context communication. |
| [custom-senior-architect](.archived/skills/custom-skills/custom-senior-architect/SKILL.md) | Expert system architect specializing in end-to-end technical flow mapping, component identification, and sequence diagram generation. |
| [internal-comms](.archived/skills/custom-skills/internal-comms/SKILL.md) | Write internal communications such as status reports, leadership updates, 3P updates, newsletters, FAQs, incident reports, and project updates using repeatable internal formats. |
| [internal-comms-anthropic](.archived/skills/custom-skills/internal-comms-anthropic/SKILL.md) | To write internal communications, use this skill for: |
| [internal-comms-community](.archived/skills/custom-skills/internal-comms-community/SKILL.md) | To write internal communications, use this skill for: |
| [junta-leiloeiros](.archived/skills/custom-skills/junta-leiloeiros/SKILL.md) | Coleta e consulta dados de leiloeiros oficiais de todas as 27 Juntas Comerciais do Brasil. Scraper multi-UF, banco SQLite, API FastAPI e exportacao CSV/JSON. |
| [leiloeiro-avaliacao](.archived/skills/custom-skills/leiloeiro-avaliacao/SKILL.md) | Avaliacao pericial de imoveis em leilao. Valor de mercado, liquidacao forcada, ABNT NBR 14653, metodos comparativo/renda/custo, CUB e margem de seguranca. |
| [leiloeiro-edital](.archived/skills/custom-skills/leiloeiro-edital/SKILL.md) | Analise e auditoria de editais de leilao judicial e extrajudicial. Riscos ocultos, clausulas perigosas, debitos, ocupante e classificacao da oportunidade. |
| [leiloeiro-ia](.archived/skills/custom-skills/leiloeiro-ia/SKILL.md) | Especialista em leiloes judiciais e extrajudiciais de imoveis. Analise juridica, pericial e de mercado integrada. Orquestra os 5 modulos especializados. |
| [leiloeiro-mercado](.archived/skills/custom-skills/leiloeiro-mercado/SKILL.md) | Analise de mercado imobiliario para leiloes. Liquidez, desagio tipico, ROI, estrategias de saida (flip/reforma/renda), Selic 2025 e benchmark CDI/FII. |
| [leiloeiro-risco](.archived/skills/custom-skills/leiloeiro-risco/SKILL.md) | Analise de risco em leiloes de imoveis. Score 36 pontos, riscos juridicos/financeiros/operacionais, stress test 4 cenarios e ROI ponderado por risco. |
| [mtls-configuration](.archived/skills/custom-skills/mtls-configuration/SKILL.md) | Configure mutual TLS (mTLS) for zero-trust service-to-service communication. Use when implementing zero-trust networking, certificate management, or securing internal service communication. |
| [seo-structure-architect](.archived/skills/custom-skills/seo-structure-architect/SKILL.md) | Analyzes and optimizes content structure including header hierarchy, suggests schema markup, and internal linking opportunities. Creates search-friendly content organization. |
| [site-architecture](.archived/skills/custom-skills/site-architecture/SKILL.md) | Plan or restructure website hierarchy, navigation, URL patterns, breadcrumbs, and internal linking. Use when mapping pages, sections, and site structure, but not for XML sitemap auditing or schema markup. |
| [skill-installer](.archived/skills/custom-skills/skill-installer/SKILL.md) | Instala, valida, registra e verifica novas skills no ecossistema. 10 checks de seguranca, copia, registro no orchestrator e verificacao pos-instalacao. |
| [workspace-analyzer](.archived/skills/custom-skills/workspace-analyzer/SKILL.md) | Architectural investigator that scans a repository to map the high-level architecture, identify the critical path, surface integrations, and flag redundant code. |

</details>

## Finding Skills

All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1336
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1335
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1336
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1336
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1335
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1337
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**macOS / Linux:**
```bash
find .archived/skills -maxdepth 2 -not -path '*/.*' -type d | wc -l
```

**Windows (PowerShell 7):**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1336
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**PowerShell:**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1336
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**PowerShell:**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1336
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**PowerShell:**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object
```

---

> **Total Installed Skills:** 1329
All skills live in `.archived/skills/<category>/<skill-name>/SKILL.md`. To browse:

**PowerShell:**
```powershell
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory -Exclude ".*" | Measure-Object                                  # Count
Get-ChildItem -Path ".archived\skills" -Recurse -Depth 1 -Directory | Where-Object { $_.Name -like "*react*" }        # Search
```

**Bash / Zsh:**
```bash
ls -d .archived/skills/*/*/ | wc -l                  # Count
ls -d .archived/skills/*/*react*/                    # Search
```

**Cross-platform (Node.js):**
```bash
npx -y glob ".archived/skills/*/*/SKILL.md" | wc -l  # Count
npx -y glob ".archived/skills/*/*react*/SKILL.md"     # Search
```

Or just ask: *"Is there a skill for X?"*

---

> **Total Installed Skills:** 1331
>
> **Source:** [antigravity-awesome-skills](https://github.com/anthropics/awesome-claude-code-skills)
