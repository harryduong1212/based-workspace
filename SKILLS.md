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
| [advanced-evaluation](.archived/skills/ai-llm-agent-development/advanced-evaluation/SKILL.md) | This skill should be used when the user asks to "implement LLM-as-judge", "compare model outputs", "create evaluation rubrics", "mitigate evaluation bias", or mentions direct scoring, pairwise comparison, position bias, evaluation pipelines, or automated quality assessment. |
| [aegisops-ai](.archived/skills/ai-llm-agent-development/aegisops-ai/SKILL.md) | Autonomous DevSecOps & FinOps Guardrails. |
| [agent-evaluation](.archived/skills/ai-llm-agent-development/agent-evaluation/SKILL.md) | Evaluate LLM agents beyond benchmarks |
| [agent-memory-mcp](.archived/skills/ai-llm-agent-development/agent-memory-mcp/SKILL.md) | Hybrid persistent memory management for AI agents |
| [agent-memory-systems](.archived/skills/ai-llm-agent-development/agent-memory-systems/SKILL.md) | Memory architectures for intelligent agents |
| [agent-orchestrator](.archived/skills/ai-llm-agent-development/agent-orchestrator/SKILL.md) | Meta-skill: scan, match, coordinate multi-skill workflows |
| [agent-tool-builder](.archived/skills/ai-llm-agent-development/agent-tool-builder/SKILL.md) | Design tools for LLM-agent interaction |
| [agentfolio](.archived/skills/ai-llm-agent-development/agentfolio/SKILL.md) | Skill for discovering and researching autonomous AI agents, tools, and ecosystems using the AgentFolio directory. |
| [ai-agent-development](.archived/skills/ai-llm-agent-development/ai-agent-development/SKILL.md) | Build autonomous agents, multi-agent systems, orchestration |
| [ai-agents-architect](.archived/skills/ai-llm-agent-development/ai-agents-architect/SKILL.md) | Design autonomous AI systems with graceful degradation |
| [ai-analyzer](.archived/skills/ai-llm-agent-development/ai-analyzer/SKILL.md) | AI驱动的综合健康分析系统，整合多维度健康数据、识别异常模式、预测健康风险、提供个性化建议。支持智能问答和AI健康报告生成。 |
| [ai-engineer](.archived/skills/ai-llm-agent-development/ai-engineer/SKILL.md) | Production-ready LLM apps, RAG, intelligent agents |
| [ai-engineering-toolkit](.archived/skills/ai-llm-agent-development/ai-engineering-toolkit/SKILL.md) | 6 production AI workflows: prompt eval, RAG, agent security |
| [ai-ml](.archived/skills/ai-llm-agent-development/ai-ml/SKILL.md) | AI/ML workflow: LLM apps, RAG, agent architecture |
| [ai-product](.archived/skills/ai-llm-agent-development/ai-product/SKILL.md) | Ship LLM features to production at scale |
| [ai-studio-image](.archived/skills/ai-llm-agent-development/ai-studio-image/SKILL.md) | Geracao de imagens humanizadas via Google AI Studio (Gemini). Fotos realistas estilo influencer ou educacional com iluminacao natural e imperfeicoes sutis. |
| [ai-wrapper-product](.archived/skills/ai-llm-agent-development/ai-wrapper-product/SKILL.md) | Build AI products people pay for and use daily |
| [andrej-karpathy](.archived/skills/ai-llm-agent-development/andrej-karpathy/SKILL.md) | Agente que simula Andrej Karpathy — ex-Director of AI da Tesla, co-fundador da OpenAI, fundador da Eureka Labs, e o maior educador de deep learning do mundo. |
| [autonomous-agent-patterns](.archived/skills/ai-llm-agent-development/autonomous-agent-patterns/SKILL.md) | Design patterns for autonomous coding agents |
| [autonomous-agents](.archived/skills/ai-llm-agent-development/autonomous-agents/SKILL.md) | Autonomous AI patterns with safety and oversight |
| [c4-container](.archived/skills/ai-llm-agent-development/c4-container/SKILL.md) | Expert C4 Container-level documentation specialist. |
| [claude-in-chrome-troubleshooting](.archived/skills/ai-llm-agent-development/claude-in-chrome-troubleshooting/SKILL.md) | Diagnose and fix Claude in Chrome MCP extension connectivity issues. Use when mcp__claude-in-chrome__* tools fail, return "Browser extension is not connected", or behave erratically. |
| [code-documentation-code-explain](.archived/skills/ai-llm-agent-development/code-documentation-code-explain/SKILL.md) | You are a code education expert specializing in explaining complex code through clear narratives, visual diagrams, and step-by-step breakdowns. Transform difficult concepts into understandable explanations for developers at all levels. |
| [code-reviewer](.archived/skills/ai-llm-agent-development/code-reviewer/SKILL.md) | Elite code review expert specializing in modern AI-powered code |
| [computer-use-agents](.archived/skills/ai-llm-agent-development/computer-use-agents/SKILL.md) | Vision-action loop for computer use agents |
| [context-compression](.archived/skills/ai-llm-agent-development/context-compression/SKILL.md) | Compress agent conversation history |
| [context-fundamentals](.archived/skills/ai-llm-agent-development/context-fundamentals/SKILL.md) | Context is the complete state available to a language model at inference time. It includes everything the model can attend to when generating responses: system instructions, tool definitions, retrieved documents, message history, and tool outputs. |
| [context-manager](.archived/skills/ai-llm-agent-development/context-manager/SKILL.md) | Dynamic context management, vector DBs, knowledge graphs |
| [context-optimization](.archived/skills/ai-llm-agent-development/context-optimization/SKILL.md) | Strategic compression, caching, partitioning |
| [context-window-management](.archived/skills/ai-llm-agent-development/context-window-management/SKILL.md) | Optimize LLM context windows at scale |
| [conversation-memory](.archived/skills/ai-llm-agent-development/conversation-memory/SKILL.md) | Persistent memory for LLM conversations |
| [crewai](.archived/skills/ai-llm-agent-development/crewai/SKILL.md) | Design collaborative AI agent teams with CrewAI |
| [customer-support](.archived/skills/ai-llm-agent-development/customer-support/SKILL.md) | Elite AI-powered customer support specialist mastering conversational AI, automated ticketing, sentiment analysis, and omnichannel support experiences. |
| [daily](.archived/skills/ai-llm-agent-development/daily/SKILL.md) | Documentation and capabilities reference for Daily |
| [dispatching-parallel-agents](.archived/skills/ai-llm-agent-development/dispatching-parallel-agents/SKILL.md) | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [evaluation](.archived/skills/ai-llm-agent-development/evaluation/SKILL.md) | Build evaluation frameworks for agent systems |
| [explain-like-socrates](.archived/skills/ai-llm-agent-development/explain-like-socrates/SKILL.md) | > |
| [fal-audio](.archived/skills/ai-llm-agent-development/fal-audio/SKILL.md) | Text-to-speech and speech-to-text using fal.ai audio models |
| [fal-generate](.archived/skills/ai-llm-agent-development/fal-generate/SKILL.md) | Generate images and videos using fal.ai AI models |
| [fal-image-edit](.archived/skills/ai-llm-agent-development/fal-image-edit/SKILL.md) | AI-powered image editing with style transfer and object removal |
| [fal-upscale](.archived/skills/ai-llm-agent-development/fal-upscale/SKILL.md) | Upscale and enhance image and video resolution using AI |
| [fal-workflow](.archived/skills/ai-llm-agent-development/fal-workflow/SKILL.md) | Generate workflow JSON files for chaining AI models |
| [geo-fundamentals](.archived/skills/ai-llm-agent-development/geo-fundamentals/SKILL.md) | Generative Engine Optimization for AI search engines (ChatGPT, Claude, Perplexity). |
| [hierarchical-agent-memory](.archived/skills/ai-llm-agent-development/hierarchical-agent-memory/SKILL.md) | Scoped CLAUDE.md memory system that reduces context token spend. Creates directory-level context files, tracks savings via dashboard, and routes agents to the right sub-context. |
| [hosted-agents](.archived/skills/ai-llm-agent-development/hosted-agents/SKILL.md) | Build background agents in sandboxed environments |
| [image-studio](.archived/skills/ai-llm-agent-development/image-studio/SKILL.md) | Studio de geracao de imagens inteligente — roteamento automatico entre ai-studio-image (fotos humanizadas/influencer) e stability-ai (arte/ ilustracao/edicao). Detecta o tipo de imagem solicitada e escolhe o modelo ideal automaticamente. |
| [langchain-architecture](.archived/skills/ai-llm-agent-development/langchain-architecture/SKILL.md) | LangChain framework for LLM applications |
| [langfuse](.archived/skills/ai-llm-agent-development/langfuse/SKILL.md) | LLM observability and evaluation |
| [langgraph](.archived/skills/ai-llm-agent-development/langgraph/SKILL.md) | Production-grade AI agents with LangGraph |
| [leiloeiro-ia](.archived/skills/ai-llm-agent-development/leiloeiro-ia/SKILL.md) | Especialista em leiloes judiciais e extrajudiciais de imoveis. Analise juridica, pericial e de mercado integrada. Orquestra os 5 modulos especializados. |
| [llm-app-patterns](.archived/skills/ai-llm-agent-development/llm-app-patterns/SKILL.md) | Production patterns for LLM applications |
| [llm-evaluation](.archived/skills/ai-llm-agent-development/llm-evaluation/SKILL.md) | Evaluation strategies: automated, human, A/B testing |
| [llm-ops](.archived/skills/ai-llm-agent-development/llm-ops/SKILL.md) | RAG, embeddings, vector DBs, fine-tuning, evals |
| [llm-prompt-optimizer](.archived/skills/ai-llm-agent-development/llm-prompt-optimizer/SKILL.md) | Improve prompts: quality, hallucination, token usage |
| [llm-structured-output](.archived/skills/ai-llm-agent-development/llm-structured-output/SKILL.md) | Reliable JSON/typed objects from LLMs |
| [local-llm-expert](.archived/skills/ai-llm-agent-development/local-llm-expert/SKILL.md) | Local inference with Ollama, llama.cpp, vLLM |
| [mcp-builder](.archived/skills/ai-llm-agent-development/mcp-builder/SKILL.md) | Create MCP servers for LLM tool integration |
| [mcp-builder-ms](.archived/skills/ai-llm-agent-development/mcp-builder-ms/SKILL.md) | MCP servers with FastMCP or MCP SDK |
| [memory-systems](.archived/skills/ai-llm-agent-development/memory-systems/SKILL.md) | Short/long-term and graph-based memory architectures |
| [multi-advisor](.archived/skills/ai-llm-agent-development/multi-advisor/SKILL.md) | Conselho de especialistas — consulta multiplos agentes do ecossistema em paralelo para analise multi-perspectiva de qualquer topico. Ativa personas, especialistas e agentes tecnicos simultaneamente, cada um pela sua otica unica, e consolida em sintese decisoria final. |
| [multi-agent-patterns](.archived/skills/ai-llm-agent-development/multi-agent-patterns/SKILL.md) | Supervisor, swarm, handoff agent patterns |
| [nanobanana-ppt-skills](.archived/skills/ai-llm-agent-development/nanobanana-ppt-skills/SKILL.md) | AI-powered PPT generation with document analysis and styled images |
| [odoo-qweb-templates](.archived/skills/ai-llm-agent-development/odoo-qweb-templates/SKILL.md) | Expert in Odoo QWeb templating for PDF reports, email templates, and website pages. Covers t-if, t-foreach, t-field, and report actions. |
| [plaid-fintech](.archived/skills/ai-llm-agent-development/plaid-fintech/SKILL.md) | Create a linktoken for Plaid Link, exchange publictoken for accesstoken. Link tokens are short-lived, one-time use. Access tokens don't expire but may need updating when users change passwords. |
| [prompt-engineer](.archived/skills/ai-llm-agent-development/prompt-engineer/SKILL.md) | Optimize prompts with frameworks (RTF, RISEN, CoT) |
| [prompt-engineering](.archived/skills/ai-llm-agent-development/prompt-engineering/SKILL.md) | Prompt patterns, best practices, optimization |
| [prompt-engineering-patterns](.archived/skills/ai-llm-agent-development/prompt-engineering-patterns/SKILL.md) | Advanced prompt techniques for LLM performance |
| [pydantic-ai](.archived/skills/ai-llm-agent-development/pydantic-ai/SKILL.md) | Type-safe AI agents with PydanticAI |
| [rag-engineer](.archived/skills/ai-llm-agent-development/rag-engineer/SKILL.md) | Chunking, embeddings, retrieval optimization |
| [rag-implementation](.archived/skills/ai-llm-agent-development/rag-implementation/SKILL.md) | Embedding selection, vector DB setup, chunking |
| [seek-and-analyze-video](.archived/skills/ai-llm-agent-development/seek-and-analyze-video/SKILL.md) | Seek and analyze video content using Memories.ai Large Visual Memory Model for persistent video intelligence |
| [skill-check](.archived/skills/ai-llm-agent-development/skill-check/SKILL.md) | Validate Claude Code skills against the agentskills specification. Catches structural, semantic, and naming issues before users do. |
| [stability-ai](.archived/skills/ai-llm-agent-development/stability-ai/SKILL.md) | Geracao de imagens via Stability AI (SD3.5, Ultra, Core). Text-to-image, img2img, inpainting, upscale, remove-bg, search-replace. 15 estilos artisticos. |
| [subagent-driven-development](.archived/skills/ai-llm-agent-development/subagent-driven-development/SKILL.md) | Use when executing implementation plans with independent tasks in the current session |
| [tool-use-guardian](.archived/skills/ai-llm-agent-development/tool-use-guardian/SKILL.md) | FREE — Intelligent tool-call reliability wrapper. Monitors, retries, fixes, and learns from tool failures. Auto-recovers from truncated JSON, timeouts, rate limits, and mid-chain failures. |
| [vercel-ai-sdk-expert](.archived/skills/ai-llm-agent-development/vercel-ai-sdk-expert/SKILL.md) | Vercel AI SDK: generateText, useChat, tool calling |
| [voice-agents](.archived/skills/ai-llm-agent-development/voice-agents/SKILL.md) | Production voice agents with latency optimization |
| [voice-ai-development](.archived/skills/ai-llm-agent-development/voice-ai-development/SKILL.md) | Real-time voice applications |
| [voice-ai-engine-development](.archived/skills/ai-llm-agent-development/voice-ai-engine-development/SKILL.md) | Async voice pipelines with TTS and interrupt handling |
| [warren-buffett](.archived/skills/ai-llm-agent-development/warren-buffett/SKILL.md) | Agente que simula Warren Buffett — o maior investidor do seculo XX e XXI, CEO da Berkshire Hathaway, discipulo de Benjamin Graham e socio intelectual de Charlie Munger. |
| [yann-lecun-debate](.archived/skills/ai-llm-agent-development/yann-lecun-debate/SKILL.md) | Sub-skill de debates e posições de Yann LeCun. Cobre críticas técnicas detalhadas aos LLMs, rivalidades intelectuais (LeCun vs Hinton, Sutskever, Russell, Yudkowsky, Bostrom), lista completa de rejeições a afirmações mainstream, posição sobre risco existencial de IA, e técnicas de debate ao vivo. |

</details>

### 🌐 Frontend Development

<details>
<summary><b>🌐 Frontend Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [00-andruia-consultant](.archived/skills/frontend-development/00-andruia-consultant/SKILL.md) | Arquitecto de Soluciones Principal y Consultor Tecnológico de Andru.ia. Diagnostica y traza la hoja de ruta óptima para proyectos de IA en español. |
| [10-andruia-skill-smith](.archived/skills/frontend-development/10-andruia-skill-smith/SKILL.md) | Ingeniero de Sistemas de Andru.ia. Diseña, redacta y despliega nuevas habilidades (skills) dentro del repositorio siguiendo el Estándar de Diamante. |
| [20-andruia-niche-intelligence](.archived/skills/frontend-development/20-andruia-niche-intelligence/SKILL.md) | Estratega de Inteligencia de Dominio de Andru.ia. Analiza el nicho específico de un proyecto para inyectar conocimientos, regulaciones y estándares únicos del sector. Actívalo tras definir el nicho. |
| [ab-test-setup](.archived/skills/frontend-development/ab-test-setup/SKILL.md) | Structured guide for setting up A/B tests with mandatory gates for hypothesis, metrics, and execution readiness. |
| [accessibility-compliance-accessibility-audit](.archived/skills/frontend-development/accessibility-compliance-accessibility-audit/SKILL.md) | You are an accessibility expert specializing in WCAG compliance, inclusive design, and assistive technology compatibility. Conduct audits, identify barriers, and provide remediation guidance. |
| [ai-native-cli](.archived/skills/frontend-development/ai-native-cli/SKILL.md) | Design spec with 98 rules for building CLI tools that AI agents can safely use. Covers structured JSON output, error handling, input contracts, safety guardrails, exit codes, and agent self-description. |
| [airflow-dag-patterns](.archived/skills/frontend-development/airflow-dag-patterns/SKILL.md) | Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs. |
| [algolia-search](.archived/skills/frontend-development/algolia-search/SKILL.md) | Expert patterns for Algolia search implementation, indexing strategies, React InstantSearch, and relevance tuning Use when: adding search to, algolia, instantsearch, search api, search functionality. |
| [alpha-vantage](.archived/skills/frontend-development/alpha-vantage/SKILL.md) | Access 20+ years of global financial data: equities, options, forex, crypto, commodities, economic indicators, and 50+ technical indicators. |
| [android_ui_verification](.archived/skills/frontend-development/android_ui_verification/SKILL.md) | Automated end-to-end UI testing and verification on an Android Emulator using ADB. |
| [angular](.archived/skills/frontend-development/angular/SKILL.md) | Angular v20+: Signals, Standalone, Zoneless |
| [angular-best-practices](.archived/skills/frontend-development/angular-best-practices/SKILL.md) | Angular performance and bundle optimization |
| [angular-migration](.archived/skills/frontend-development/angular-migration/SKILL.md) | AngularJS to Angular migration |
| [angular-state-management](.archived/skills/frontend-development/angular-state-management/SKILL.md) | Signals, NgRx, RxJS state management |
| [angular-ui-patterns](.archived/skills/frontend-development/angular-ui-patterns/SKILL.md) | Loading states, error handling, data display |
| [antigravity-skill-orchestrator](.archived/skills/frontend-development/antigravity-skill-orchestrator/SKILL.md) | A meta-skill that understands task requirements, dynamically selects appropriate skills, tracks successful skill combinations using agent-memory-mcp, and prevents skill overuse for simple tasks. |
| [antigravity-workflows](.archived/skills/frontend-development/antigravity-workflows/SKILL.md) | Orchestrate multiple Antigravity skills through guided workflows for SaaS MVP delivery, security audits, AI agent builds, and browser QA. |
| [api-endpoint-builder](.archived/skills/frontend-development/api-endpoint-builder/SKILL.md) | Builds production-ready REST API endpoints with validation, error handling, authentication, and documentation. Follows best practices for security and scalability. |
| [app-builder](.archived/skills/frontend-development/app-builder/SKILL.md) | Main application building orchestrator. Creates full-stack applications from natural language requests. Determines project type, selects tech stack, coordinates agents. |
| [application-performance-performance-optimization](.archived/skills/frontend-development/application-performance-performance-optimization/SKILL.md) | Optimize end-to-end application performance with profiling, observability, and backend/frontend tuning. Use when coordinating performance optimization across the stack. |
| [ask-questions-if-underspecified](.archived/skills/frontend-development/ask-questions-if-underspecified/SKILL.md) | Clarify requirements before implementing. Use when serious doubts arise. |
| [astro](.archived/skills/frontend-development/astro/SKILL.md) | Content-focused sites with zero JS by default |
| [async-python-patterns](.archived/skills/frontend-development/async-python-patterns/SKILL.md) | Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems. |
| [attack-tree-construction](.archived/skills/frontend-development/attack-tree-construction/SKILL.md) | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders. |
| [audit-context-building](.archived/skills/frontend-development/audit-context-building/SKILL.md) | Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding. |
| [auth-implementation-patterns](.archived/skills/frontend-development/auth-implementation-patterns/SKILL.md) | Build secure, scalable authentication and authorization systems using industry-standard patterns and modern best practices. |
| [avalonia-layout-zafiro](.archived/skills/frontend-development/avalonia-layout-zafiro/SKILL.md) | Guidelines for modern Avalonia UI layout using Zafiro.Avalonia, emphasizing shared styles, generic components, and avoiding XAML redundancy. |
| [avalonia-viewmodels-zafiro](.archived/skills/frontend-development/avalonia-viewmodels-zafiro/SKILL.md) | Optimal ViewModel and Wizard creation patterns for Avalonia using Zafiro and ReactiveUI. |
| [avalonia-zafiro-development](.archived/skills/frontend-development/avalonia-zafiro-development/SKILL.md) | Mandatory skills, conventions, and behavioral rules for Avalonia UI development using the Zafiro toolkit. |
| [awt-e2e-testing](.archived/skills/frontend-development/awt-e2e-testing/SKILL.md) | AI-powered E2E web testing — eyes and hands for AI coding tools. Declarative YAML scenarios, Playwright execution, visual matching (OpenCV + OCR), platform auto-detection (Flutter/React/Vue), learning DB. Install: npx skills add ksgisang/awt-skill --skill awt -g |
| [backend-development-feature-development](.archived/skills/frontend-development/backend-development-feature-development/SKILL.md) | Orchestrate end-to-end backend feature development from requirements to deployment. Use when coordinating multi-phase feature delivery across teams and services. |
| [backtesting-frameworks](.archived/skills/frontend-development/backtesting-frameworks/SKILL.md) | Build robust, production-grade backtesting systems that avoid common pitfalls and produce reliable strategy performance estimates. |
| [baseline-ui](.archived/skills/frontend-development/baseline-ui/SKILL.md) | Validates animation durations, enforces typography scale, checks component accessibility, and prevents layout anti-patterns in Tailwind CSS projects. Use when building UI components, reviewing CSS utilities, styling React views, or enforcing design consistency. |
| [bash-defensive-patterns](.archived/skills/frontend-development/bash-defensive-patterns/SKILL.md) | Master defensive Bash programming techniques for production-grade scripts. Use when writing robust shell scripts, CI/CD pipelines, or system utilities requiring fault tolerance and safety. |
| [bats-testing-patterns](.archived/skills/frontend-development/bats-testing-patterns/SKILL.md) | Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities. |
| [bazel-build-optimization](.archived/skills/frontend-development/bazel-build-optimization/SKILL.md) | Optimize Bazel builds for large-scale monorepos. Use when configuring Bazel, implementing remote execution, or optimizing build performance for enterprise codebases. |
| [bdi-mental-states](.archived/skills/frontend-development/bdi-mental-states/SKILL.md) | This skill should be used when the user asks to "model agent mental states", "implement BDI architecture", "create belief-desire-intention models", "transform RDF to beliefs", "build cognitive agent", or mentions BDI ontology, mental state modeling, rational agency, or neuro-symbolic AI integration. |
| [bill-gates](.archived/skills/frontend-development/bill-gates/SKILL.md) | Agente que simula Bill Gates — cofundador da Microsoft, arquiteto da industria de software comercial, estrategista tecnologico global, investidor sistemico e filantropo baseado em dados. |
| [brand-guidelines](.archived/skills/frontend-development/brand-guidelines/SKILL.md) | Write copy following Sentry brand guidelines. Use when writing UI text, error messages, empty states, onboarding flows, 404 pages, documentation, marketing copy, or any user-facing content. Covers both Plain Speech (default) and Sentry Voice tones. |
| [brand-guidelines-anthropic](.archived/skills/frontend-development/brand-guidelines-anthropic/SKILL.md) | To access Anthropic's official brand identity and style resources, use this skill. |
| [brand-guidelines-community](.archived/skills/frontend-development/brand-guidelines-community/SKILL.md) | To access Anthropic's official brand identity and style resources, use this skill. |
| [browser-automation](.archived/skills/frontend-development/browser-automation/SKILL.md) | You are a browser automation expert who has debugged thousands of flaky tests and built scrapers that run for years without breaking. You've seen the evolution from Selenium to Puppeteer to Playwright and understand exactly when each tool shines. |
| [browser-extension-builder](.archived/skills/frontend-development/browser-extension-builder/SKILL.md) | You extend the browser to give users superpowers. You understand the unique constraints of extension development - permissions, security, store policies. You build extensions that people install and actually use daily. You know the difference between a toy and a tool. |
| [build](.archived/skills/frontend-development/build/SKILL.md) | build |
| [burp-suite-testing](.archived/skills/frontend-development/burp-suite-testing/SKILL.md) | Execute comprehensive web application security testing using Burp Suite's integrated toolset, including HTTP traffic interception and modification, request analysis and replay, automated vulnerability scanning, and manual testing workflows. |
| [burpsuite-project-parser](.archived/skills/frontend-development/burpsuite-project-parser/SKILL.md) | Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with regex patterns, extracting security audit findings, dumping proxy history or site map data, or analyzing HTTP traffic captured in a Burp project. |
| [busybox-on-windows](.archived/skills/frontend-development/busybox-on-windows/SKILL.md) | How to use a Win32 build of BusyBox to run many of the standard UNIX command line tools on Windows. |
| [cc-skill-coding-standards](.archived/skills/frontend-development/cc-skill-coding-standards/SKILL.md) | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development. |
| [cc-skill-frontend-patterns](.archived/skills/frontend-development/cc-skill-frontend-patterns/SKILL.md) | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| [cc-skill-project-guidelines-example](.archived/skills/frontend-development/cc-skill-project-guidelines-example/SKILL.md) | Project Guidelines Skill (Example) |
| [chat-widget](.archived/skills/frontend-development/chat-widget/SKILL.md) | Build a real-time support chat system with a floating widget for users and an admin dashboard for support staff. Use when the user wants live chat, customer support chat, real-time messaging, or in-app support. |
| [chrome-extension-developer](.archived/skills/frontend-development/chrome-extension-developer/SKILL.md) | Expert in building Chrome Extensions using Manifest V3. Covers background scripts, service workers, content scripts, and cross-context communication. |
| [cirq](.archived/skills/frontend-development/cirq/SKILL.md) | Cirq is Google Quantum AI's open-source framework for designing, simulating, and running quantum circuits on quantum computers and simulators. |
| [claimable-postgres](.archived/skills/frontend-development/claimable-postgres/SKILL.md) | Provision instant temporary Postgres databases via Claimable Postgres by Neon (pg.new). No login or credit card required. Use for quick Postgres environments and throwaway DATABASE_URL for prototyping. |
| [claude-ally-health](.archived/skills/frontend-development/claude-ally-health/SKILL.md) | A health assistant skill for medical information analysis, symptom tracking, and wellness guidance. |
| [claude-api](.archived/skills/frontend-development/claude-api/SKILL.md) | Build apps with the Claude API or Anthropic SDK. TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`, or user asks to use Claude API, Anthropic SDKs, or Agent SDK. DO NOT TRIGGER when: code imports `openai`/other AI SDK, general programming, or ML/data-science tasks. |
| [claude-code-guide](.archived/skills/frontend-development/claude-code-guide/SKILL.md) | To provide a comprehensive reference for configuring and using Claude Code (the agentic coding tool) to its full potential. This skill synthesizes best practices, configuration templates, and advanced usage patterns. |
| [claude-d3js-skill](.archived/skills/frontend-development/claude-d3js-skill/SKILL.md) | This skill provides guidance for creating sophisticated, interactive data visualisations using d3.js. |
| [claude-settings-audit](.archived/skills/frontend-development/claude-settings-audit/SKILL.md) | Analyze a repository to generate recommended Claude Code settings.json permissions. Use when setting up a new project, auditing existing settings, or determining which read-only bash commands to allow. Detects tech stack, build tools, and monorepo structure. |
| [code-documentation-doc-generate](.archived/skills/frontend-development/code-documentation-doc-generate/SKILL.md) | You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams, user guides, and technical references using AI-powered analysis and industry best practices. |
| [comfyui-gateway](.archived/skills/frontend-development/comfyui-gateway/SKILL.md) | REST API gateway for ComfyUI servers. Workflow management, job queuing, webhooks, caching, auth, rate limiting, and image delivery (URL + base64). |
| [competitor-alternatives](.archived/skills/frontend-development/competitor-alternatives/SKILL.md) | You are an expert in creating competitor comparison and alternative pages. Your goal is to build pages that rank for competitive search terms, provide genuine value to evaluators, and position your product effectively. |
| [context-agent](.archived/skills/frontend-development/context-agent/SKILL.md) | Agente de contexto para continuidade entre sessoes. Salva resumos, decisoes, tarefas pendentes e carrega briefing automatico na sessao seguinte. |
| [context-driven-development](.archived/skills/frontend-development/context-driven-development/SKILL.md) | Guide for implementing and maintaining context as a managed artifact alongside code, enabling consistent AI interactions and team alignment through structured project documentation. |
| [context7-auto-research](.archived/skills/frontend-development/context7-auto-research/SKILL.md) | Automatically fetch latest library/framework documentation for Claude Code via Context7 API. Use when you need up-to-date documentation for libraries and frameworks or asking about React, Next.js, Prisma, or any other popular library. |
| [copilot-sdk](.archived/skills/frontend-development/copilot-sdk/SKILL.md) | Build applications that programmatically interact with GitHub Copilot. The SDK wraps the Copilot CLI via JSON-RPC, providing session management, custom tools, hooks, MCP server integration, and streaming across Node.js, Python, Go, and .NET. |
| [core-components](.archived/skills/frontend-development/core-components/SKILL.md) | Core component library and design system patterns. Use when building UI, using design tokens, or working with the component library. |
| [crypto-bd-agent](.archived/skills/frontend-development/crypto-bd-agent/SKILL.md) | Production-tested patterns for building AI agents that autonomously discover, > evaluate, and acquire token listings for cryptocurrency exchanges. |
| [data-engineering-data-driven-feature](.archived/skills/frontend-development/data-engineering-data-driven-feature/SKILL.md) | Build features guided by data insights, A/B testing, and continuous measurement using specialized agents for analysis, implementation, and experimentation. |
| [data-quality-frameworks](.archived/skills/frontend-development/data-quality-frameworks/SKILL.md) | Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts. |
| [dbos-golang](.archived/skills/frontend-development/dbos-golang/SKILL.md) | Guide for building reliable, fault-tolerant Go applications with DBOS durable workflows. Use when adding DBOS to existing Go code, creating workflows and steps, or using queues for concurrency control. |
| [dbos-python](.archived/skills/frontend-development/dbos-python/SKILL.md) | Guide for building reliable, fault-tolerant Python applications with DBOS durable workflows. Use when adding DBOS to existing Python code, creating workflows and steps, or using queues for concurrency control. |
| [dbos-typescript](.archived/skills/frontend-development/dbos-typescript/SKILL.md) | Guide for building reliable, fault-tolerant TypeScript applications with DBOS durable workflows. Use when adding DBOS to existing TypeScript code, creating workflows and steps, or using queues for concurrency control. |
| [defi-protocol-templates](.archived/skills/frontend-development/defi-protocol-templates/SKILL.md) | Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems. Use when building decentralized finance applications or smart contract protocols. |
| [development](.archived/skills/frontend-development/development/SKILL.md) | Comprehensive web, mobile, and backend development workflow bundling frontend, backend, full-stack, and mobile development skills for end-to-end application delivery. |
| [discord-bot-architect](.archived/skills/frontend-development/discord-bot-architect/SKILL.md) | Specialized skill for building production-ready Discord bots. Covers Discord.js (JavaScript) and Pycord (Python), gateway intents, slash commands, interactive components, rate limiting, and sharding. |
| [doc-coauthoring](.archived/skills/frontend-development/doc-coauthoring/SKILL.md) | This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing. |
| [documentation-generation-doc-generate](.archived/skills/frontend-development/documentation-generation-doc-generate/SKILL.md) | You are a documentation expert specializing in creating comprehensive, maintainable documentation from code. Generate API docs, architecture diagrams, user guides, and technical references using AI-powered analysis and industry best practices. |
| [documentation-templates](.archived/skills/frontend-development/documentation-templates/SKILL.md) | Documentation templates and structure guidelines. README, API docs, code comments, and AI-friendly documentation. |
| [dotnet-backend-patterns](.archived/skills/frontend-development/dotnet-backend-patterns/SKILL.md) | Master C#/.NET patterns for building production-grade APIs, MCP servers, and enterprise backends with modern best practices (2024/2025). |
| [earllm-build](.archived/skills/frontend-development/earllm-build/SKILL.md) | Build, maintain, and extend the EarLLM One Android project — a Kotlin/Compose app that connects Bluetooth earbuds to an LLM via voice pipeline. |
| [electron-development](.archived/skills/frontend-development/electron-development/SKILL.md) | Master Electron desktop app development with secure IPC, contextIsolation, preload scripts, multi-process architecture, electron-builder packaging, code signing, and auto-update. |
| [embedding-strategies](.archived/skills/frontend-development/embedding-strategies/SKILL.md) | Guide to selecting and optimizing embedding models for vector search applications. |
| [enhance-prompt](.archived/skills/frontend-development/enhance-prompt/SKILL.md) | Transforms vague UI ideas into polished, Stitch-optimized prompts. Enhances specificity, adds UI/UX keywords, injects design system context, and structures output for better generation results. |
| [environment-setup-guide](.archived/skills/frontend-development/environment-setup-guide/SKILL.md) | Guide developers through setting up development environments with proper tools, dependencies, and configurations |
| [error-debugging-error-trace](.archived/skills/frontend-development/error-debugging-error-trace/SKILL.md) | You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking systems, configure alerts, implement structured logging, and ensure teams can quickly identify and resolve production issues. |
| [error-handling-patterns](.archived/skills/frontend-development/error-handling-patterns/SKILL.md) | Build resilient applications with robust error handling strategies that gracefully handle failures and provide excellent debugging experiences. |
| [event-store-design](.archived/skills/frontend-development/event-store-design/SKILL.md) | Design and implement event stores for event-sourced systems. Use when building event sourcing infrastructure, choosing event store technologies, or implementing event persistence patterns. |
| [expo-cicd-workflows](.archived/skills/frontend-development/expo-cicd-workflows/SKILL.md) | Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS context, mentions .eas/workflows/, or wants help with EAS build pipelines or deployment automation. |
| [expo-dev-client](.archived/skills/frontend-development/expo-dev-client/SKILL.md) | Build and distribute Expo development clients locally or via TestFlight |
| [expo-tailwind-setup](.archived/skills/frontend-development/expo-tailwind-setup/SKILL.md) | Set up Tailwind CSS v4 in Expo with react-native-css and NativeWind v5 for universal styling |
| [expo-ui-jetpack-compose](.archived/skills/frontend-development/expo-ui-jetpack-compose/SKILL.md) | expo-ui-jetpack-compose |
| [expo-ui-swift-ui](.archived/skills/frontend-development/expo-ui-swift-ui/SKILL.md) | expo-ui-swift-ui |
| [fastapi-templates](.archived/skills/frontend-development/fastapi-templates/SKILL.md) | Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects. |
| [ffuf-web-fuzzing](.archived/skills/frontend-development/ffuf-web-fuzzing/SKILL.md) | Expert guidance for ffuf web fuzzing during penetration testing, including authenticated fuzzing with raw requests, auto-calibration, and result analysis |
| [finishing-a-development-branch](.archived/skills/frontend-development/finishing-a-development-branch/SKILL.md) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup |
| [firecrawl-scraper](.archived/skills/frontend-development/firecrawl-scraper/SKILL.md) | Deep web scraping, screenshots, PDF parsing, and website crawling using Firecrawl API. Use when you need deep content extraction from web pages, page interaction is required (clicking, scrolling, etc.), or you want screenshots or PDF parsing. |
| [fixing-motion-performance](.archived/skills/frontend-development/fixing-motion-performance/SKILL.md) | Audit and fix animation performance issues including layout thrashing, compositor properties, scroll-linked motion, and blur effects. Use when animations stutter, transitions jank, or reviewing CSS/JS animation performance. |
| [fp-either-ref](.archived/skills/frontend-development/fp-either-ref/SKILL.md) | Quick reference for Either type. Use when user needs error handling, validation, or operations that can fail with typed errors. |
| [fp-option-ref](.archived/skills/frontend-development/fp-option-ref/SKILL.md) | Quick reference for Option type. Use when user needs to handle nullable values, optional data, or wants to avoid null checks. |
| [fp-pipe-ref](.archived/skills/frontend-development/fp-pipe-ref/SKILL.md) | Quick reference for pipe and flow. Use when user needs to chain functions, compose operations, or build data pipelines in fp-ts. |
| [fp-pragmatic](.archived/skills/frontend-development/fp-pragmatic/SKILL.md) | A practical, jargon-free guide to functional programming - the 80/20 approach that gets results without the academic overhead |
| [fp-react](.archived/skills/frontend-development/fp-react/SKILL.md) | Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Works with React 18/19, Next.js 14/15. |
| [fp-refactor](.archived/skills/frontend-development/fp-refactor/SKILL.md) | Comprehensive guide for refactoring imperative TypeScript code to fp-ts functional patterns |
| [fp-taskeither-ref](.archived/skills/frontend-development/fp-taskeither-ref/SKILL.md) | Quick reference for TaskEither. Use when user needs async error handling, API calls, or Promise-based operations that can fail. |
| [fp-ts-pragmatic](.archived/skills/frontend-development/fp-ts-pragmatic/SKILL.md) | A practical, jargon-free guide to fp-ts functional programming - the 80/20 approach that gets results without the academic overhead. Use when writing TypeScript with fp-ts library. |
| [fp-ts-react](.archived/skills/frontend-development/fp-ts-react/SKILL.md) | Practical patterns for using fp-ts with React - hooks, state, forms, data fetching. Use when building React apps with functional programming patterns. Works with React 18/19, Next.js 14/15. |
| [fp-types-ref](.archived/skills/frontend-development/fp-types-ref/SKILL.md) | Quick reference for fp-ts types. Use when user asks which type to use, needs Option/Either/Task decision help, or wants fp-ts imports. |
| [free-tool-strategy](.archived/skills/frontend-development/free-tool-strategy/SKILL.md) | You are an expert in engineering-as-marketing strategy. Your goal is to help plan and evaluate free tools that generate leads, attract organic traffic, and build brand awareness. |
| [frontend-design](.archived/skills/frontend-development/frontend-design/SKILL.md) | Frontend designer-engineer mindset |
| [frontend-dev-guidelines](.archived/skills/frontend-development/frontend-dev-guidelines/SKILL.md) | You are a senior frontend engineer operating under strict architectural and performance standards. Use when creating components or pages, adding new features, or fetching or mutating data. |
| [frontend-developer](.archived/skills/frontend-development/frontend-developer/SKILL.md) | React 19, Next.js 15, responsive layouts |
| [frontend-mobile-development-component-scaffold](.archived/skills/frontend-development/frontend-mobile-development-component-scaffold/SKILL.md) | You are a React component architecture expert specializing in scaffolding production-ready, accessible, and performant components. Generate complete component implementations with TypeScript, tests, s |
| [frontend-mobile-security-xss-scan](.archived/skills/frontend-development/frontend-mobile-security-xss-scan/SKILL.md) | You are a frontend security specialist focusing on Cross-Site Scripting (XSS) vulnerability detection and prevention. Analyze React, Vue, Angular, and vanilla JavaScript code to identify injection poi |
| [frontend-ui-dark-ts](.archived/skills/frontend-development/frontend-ui-dark-ts/SKILL.md) | A modern dark-themed React UI system using Tailwind CSS and Framer Motion. Designed for dashboards, admin panels, and data-rich applications with glassmorphism effects and tasteful animations. |
| [gdpr-data-handling](.archived/skills/frontend-development/gdpr-data-handling/SKILL.md) | Practical implementation guide for GDPR-compliant data processing, consent management, and privacy controls. |
| [gitlab-ci-patterns](.archived/skills/frontend-development/gitlab-ci-patterns/SKILL.md) | Comprehensive GitLab CI/CD pipeline patterns for automated testing, building, and deployment. |
| [go-concurrency-patterns](.archived/skills/frontend-development/go-concurrency-patterns/SKILL.md) | Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions. |
| [go-rod-master](.archived/skills/frontend-development/go-rod-master/SKILL.md) | Comprehensive guide for browser automation and web scraping with go-rod (Chrome DevTools Protocol) including stealth anti-bot-detection patterns. |
| [godot-4-migration](.archived/skills/frontend-development/godot-4-migration/SKILL.md) | Specialized guide for migrating Godot 3.x projects to Godot 4 (GDScript 2.0), covering syntax changes, Tweens, and exports. |
| [google-docs-automation](.archived/skills/frontend-development/google-docs-automation/SKILL.md) | Lightweight Google Docs integration with standalone OAuth authentication. No MCP server required. |
| [google-slides-automation](.archived/skills/frontend-development/google-slides-automation/SKILL.md) | Lightweight Google Slides integration with standalone OAuth authentication. No MCP server required. Full read/write access. |
| [grpc-golang](.archived/skills/frontend-development/grpc-golang/SKILL.md) | Build production-ready gRPC services in Go with mTLS, streaming, and observability. Use when designing Protobuf contracts with Buf or implementing secure service-to-service transport. |
| [hig-components-content](.archived/skills/frontend-development/hig-components-content/SKILL.md) | Apple Human Interface Guidelines for content display components. |
| [hig-components-dialogs](.archived/skills/frontend-development/hig-components-dialogs/SKILL.md) | Apple HIG guidance for presentation components including alerts, action sheets, popovers, sheets, and digit entry views. |
| [hig-components-layout](.archived/skills/frontend-development/hig-components-layout/SKILL.md) | Apple Human Interface Guidelines for layout and navigation components. |
| [hig-components-search](.archived/skills/frontend-development/hig-components-search/SKILL.md) | Apple HIG guidance for navigation-related components including search fields, page controls, and path controls. |
| [hig-components-status](.archived/skills/frontend-development/hig-components-status/SKILL.md) | Apple HIG guidance for status and progress UI components including progress indicators, status bars, and activity rings. |
| [hig-components-system](.archived/skills/frontend-development/hig-components-system/SKILL.md) | Apple HIG guidance for system experience components: widgets, live activities, notifications, complications, home screen quick actions, top shelf, watch faces, app clips, and app shortcuts. |
| [hig-foundations](.archived/skills/frontend-development/hig-foundations/SKILL.md) | Apple Human Interface Guidelines design foundations. |
| [hig-patterns](.archived/skills/frontend-development/hig-patterns/SKILL.md) | Apple Human Interface Guidelines interaction and UX patterns. |
| [hig-platforms](.archived/skills/frontend-development/hig-platforms/SKILL.md) | Apple Human Interface Guidelines for platform-specific design. |
| [hig-project-context](.archived/skills/frontend-development/hig-project-context/SKILL.md) | Create or update a shared Apple design context document that other HIG skills use to tailor guidance. |
| [hugging-face-tool-builder](.archived/skills/frontend-development/hugging-face-tool-builder/SKILL.md) | Your purpose is now is to create reusable command line scripts and utilities for using the Hugging Face API, allowing chaining, piping and intermediate processing where helpful. You can access the API directly, as well as use the hf command line tool. |
| [hybrid-search-implementation](.archived/skills/frontend-development/hybrid-search-implementation/SKILL.md) | Combine vector and keyword search for improved retrieval. Use when implementing RAG systems, building search engines, or when neither approach alone provides sufficient recall. |
| [imagen](.archived/skills/frontend-development/imagen/SKILL.md) | AI image generation skill powered by Google Gemini, enabling seamless visual content creation for UI placeholders, documentation, and design assets. |
| [ios-debugger-agent](.archived/skills/frontend-development/ios-debugger-agent/SKILL.md) | Debug the current iOS project on a booted simulator with XcodeBuildMCP. |
| [istio-traffic-management](.archived/skills/frontend-development/istio-traffic-management/SKILL.md) | Comprehensive guide to Istio traffic management for production service mesh deployments. |
| [javascript-mastery](.archived/skills/frontend-development/javascript-mastery/SKILL.md) | 33+ essential JS concepts |
| [javascript-pro](.archived/skills/frontend-development/javascript-pro/SKILL.md) | ES6+, async patterns, Node.js APIs |
| [javascript-typescript-typescript-scaffold](.archived/skills/frontend-development/javascript-typescript-typescript-scaffold/SKILL.md) | You are a TypeScript project architecture expert specializing in scaffolding production-ready Node.js and frontend applications. Generate complete project structures with modern tooling (pnpm, Vite, N |
| [jobgpt](.archived/skills/frontend-development/jobgpt/SKILL.md) | Job search automation, auto apply, resume generation, application tracking, salary intelligence, and recruiter outreach using the JobGPT MCP server. |
| [kaizen](.archived/skills/frontend-development/kaizen/SKILL.md) | Guide for continuous improvement, error proofing, and standardization. Use this skill when the user wants to improve code quality, refactor, or discuss process improvements. |
| [landing-page-generator](.archived/skills/frontend-development/landing-page-generator/SKILL.md) | Generates high-converting Next.js/React landing pages with Tailwind CSS. Uses PAS, AIDA, and BAB frameworks for optimized copy/components (Heroes, Features, Pricing). Focuses on Core Web Vitals/SEO. |
| [launch-strategy](.archived/skills/frontend-development/launch-strategy/SKILL.md) | You are an expert in SaaS product launches and feature announcements. Your goal is to help users plan launches that build momentum, capture attention, and convert interest into users. |
| [leiloeiro-avaliacao](.archived/skills/frontend-development/leiloeiro-avaliacao/SKILL.md) | Avaliacao pericial de imoveis em leilao. Valor de mercado, liquidacao forcada, ABNT NBR 14653, metodos comparativo/renda/custo, CUB e margem de seguranca. |
| [leiloeiro-mercado](.archived/skills/frontend-development/leiloeiro-mercado/SKILL.md) | Analise de mercado imobiliario para leiloes. Liquidez, desagio tipico, ROI, estrategias de saida (flip/reforma/renda), Selic 2025 e benchmark CDI/FII. |
| [lightning-architecture-review](.archived/skills/frontend-development/lightning-architecture-review/SKILL.md) | Review Bitcoin Lightning Network protocol designs, compare channel factory approaches, and analyze Layer 2 scaling tradeoffs. Covers trust models, on-chain footprint, consensus requirements, HTLC/PTLC compatibility, liveness, and watchtower support. |
| [lightning-factory-explainer](.archived/skills/frontend-development/lightning-factory-explainer/SKILL.md) | Explain Bitcoin Lightning channel factories and the SuperScalar protocol — scalable Lightning onboarding using shared UTXOs, Decker-Wattenhofer trees, timeout-signature trees, MuSig2, and Taproot. No soft fork required. |
| [linux-shell-scripting](.archived/skills/frontend-development/linux-shell-scripting/SKILL.md) | Provide production-ready shell script templates for common Linux system administration tasks including backups, monitoring, user management, log analysis, and automation. These scripts serve as building blocks for security operations and penetration testing environments. |
| [m365-agents-dotnet](.archived/skills/frontend-development/m365-agents-dotnet/SKILL.md) | Microsoft 365 Agents SDK for .NET. Build multichannel agents for Teams/M365/Copilot Studio with ASP.NET Core hosting, AgentApplication routing, and MSAL-based auth. |
| [m365-agents-py](.archived/skills/frontend-development/m365-agents-py/SKILL.md) | Microsoft 365 Agents SDK for Python. Build multichannel agents for Teams/M365/Copilot Studio with aiohttp hosting, AgentApplication routing, streaming responses, and MSAL-based auth. |
| [macos-menubar-tuist-app](.archived/skills/frontend-development/macos-menubar-tuist-app/SKILL.md) | Build, refactor, or review SwiftUI macOS menubar apps that use Tuist. |
| [macos-spm-app-packaging](.archived/skills/frontend-development/macos-spm-app-packaging/SKILL.md) | Scaffold, build, sign, and package SwiftPM macOS apps without Xcode projects. |
| [magic-animator](.archived/skills/frontend-development/magic-animator/SKILL.md) | AI-powered animation tool for creating motion in logos, UI, icons, and social media assets. |
| [makepad-skills](.archived/skills/frontend-development/makepad-skills/SKILL.md) | Makepad UI development skills for Rust apps: setup, patterns, shaders, packaging, and troubleshooting. |
| [matematico-tao](.archived/skills/frontend-development/matematico-tao/SKILL.md) | Matemático ultra-avançado inspirado em Terence Tao. Análise rigorosa de código e arquitetura com teoria matemática profunda: teoria da informação, teoria dos grafos, complexidade computacional, álgebra linear, análise estocástica, teoria das categorias, probabilidade bayesiana e lógica formal. |
| [memory-forensics](.archived/skills/frontend-development/memory-forensics/SKILL.md) | Comprehensive techniques for acquiring, analyzing, and extracting artifacts from memory dumps for incident response and malware analysis. |
| [modern-javascript-patterns](.archived/skills/frontend-development/modern-javascript-patterns/SKILL.md) | ES6+ features and functional patterns |
| [monorepo-management](.archived/skills/frontend-development/monorepo-management/SKILL.md) | Build efficient, scalable monorepos that enable code sharing, consistent tooling, and atomic changes across multiple packages and applications. |
| [moodle-external-api-development](.archived/skills/frontend-development/moodle-external-api-development/SKILL.md) | This skill guides you through creating custom external web service APIs for Moodle LMS, following Moodle's external API framework and coding standards. |
| [multi-platform-apps-multi-platform](.archived/skills/frontend-development/multi-platform-apps-multi-platform/SKILL.md) | Build and deploy the same feature consistently across web, mobile, and desktop platforms using API-first architecture and parallel implementation strategies. |
| [n8n-mcp-tools-expert](.archived/skills/frontend-development/n8n-mcp-tools-expert/SKILL.md) | Expert guide for using n8n-mcp MCP tools effectively. Use when searching for nodes, validating configurations, accessing templates, managing workflows, or using any n8n-mcp tool. Provides tool selection guidance, parameter formats, and common patterns. |
| [n8n-node-configuration](.archived/skills/frontend-development/n8n-node-configuration/SKILL.md) | Operation-aware node configuration guidance. Use when configuring nodes, understanding property dependencies, determining required fields, choosing between get_node detail levels, or learning common configuration patterns by node type. |
| [n8n-validation-expert](.archived/skills/frontend-development/n8n-validation-expert/SKILL.md) | Expert guide for interpreting and fixing n8n validation errors. |
| [native-data-fetching](.archived/skills/frontend-development/native-data-fetching/SKILL.md) | Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, React Query, SWR, error handling, caching, offline support, and Expo Router data loaders (useLoaderData). |
| [nextjs-app-router-patterns](.archived/skills/frontend-development/nextjs-app-router-patterns/SKILL.md) | Next.js 14+ App Router, Server Components |
| [nextjs-best-practices](.archived/skills/frontend-development/nextjs-best-practices/SKILL.md) | Server Components, data fetching, routing |
| [nextjs-supabase-auth](.archived/skills/frontend-development/nextjs-supabase-auth/SKILL.md) | Expert integration of Supabase Auth with Next.js App Router Use when: supabase auth next, authentication next.js, login supabase, auth middleware, protected route. |
| [notion-template-business](.archived/skills/frontend-development/notion-template-business/SKILL.md) | You know templates are real businesses that can generate serious income. You've seen creators make six figures selling Notion templates. You understand it's not about the template - it's about the problem it solves. You build systems that turn templates into scalable digital products. |
| [nx-workspace-patterns](.archived/skills/frontend-development/nx-workspace-patterns/SKILL.md) | Configure and optimize Nx monorepo workspaces. Use when setting up Nx, configuring project boundaries, optimizing build caching, or implementing affected commands. |
| [obsidian-clipper-template-creator](.archived/skills/frontend-development/obsidian-clipper-template-creator/SKILL.md) | Guide for creating templates for the Obsidian Web Clipper. Use when you want to create a new clipping template, understand available variables, or format clipped content. |
| [odoo-accounting-setup](.archived/skills/frontend-development/odoo-accounting-setup/SKILL.md) | Expert guide for configuring Odoo Accounting: chart of accounts, journals, fiscal positions, taxes, payment terms, and bank reconciliation. |
| [odoo-ecommerce-configurator](.archived/skills/frontend-development/odoo-ecommerce-configurator/SKILL.md) | Expert guide for Odoo eCommerce and Website: product catalog, payment providers, shipping methods, SEO, and order-to-fulfillment workflow. |
| [odoo-edi-connector](.archived/skills/frontend-development/odoo-edi-connector/SKILL.md) | Guide for implementing EDI (Electronic Data Interchange) with Odoo: X12, EDIFACT document mapping, partner onboarding, and automated order processing. |
| [odoo-hr-payroll-setup](.archived/skills/frontend-development/odoo-hr-payroll-setup/SKILL.md) | Expert guide for Odoo HR and Payroll: salary structures, payslip rules, leave policies, employee contracts, and payroll journal entries. |
| [odoo-inventory-optimizer](.archived/skills/frontend-development/odoo-inventory-optimizer/SKILL.md) | Expert guide for Odoo Inventory: stock valuation (FIFO/AVCO), reordering rules, putaway strategies, routes, and multi-warehouse configuration. |
| [odoo-manufacturing-advisor](.archived/skills/frontend-development/odoo-manufacturing-advisor/SKILL.md) | Expert guide for Odoo Manufacturing: Bills of Materials (BoM), Work Centers, routings, MRP planning, and production order workflows. |
| [odoo-migration-helper](.archived/skills/frontend-development/odoo-migration-helper/SKILL.md) | Step-by-step guide for migrating Odoo custom modules between versions (v14→v15→v16→v17). Covers API changes, deprecated methods, and view migration. |
| [odoo-module-developer](.archived/skills/frontend-development/odoo-module-developer/SKILL.md) | Expert guide for creating custom Odoo modules. Covers __manifest__.py, model inheritance, ORM patterns, and module structure best practices. |
| [odoo-performance-tuner](.archived/skills/frontend-development/odoo-performance-tuner/SKILL.md) | Expert guide for diagnosing and fixing Odoo performance issues: slow queries, worker configuration, memory limits, PostgreSQL tuning, and profiling tools. |
| [odoo-project-timesheet](.archived/skills/frontend-development/odoo-project-timesheet/SKILL.md) | Expert guide for Odoo Project and Timesheets: task stages, billable time tracking, timesheet approval, budget alerts, and invoicing from timesheets. |
| [odoo-purchase-workflow](.archived/skills/frontend-development/odoo-purchase-workflow/SKILL.md) | Expert guide for Odoo Purchase: RFQ → PO → Receipt → Vendor Bill workflow, purchase agreements, vendor price lists, and 3-way matching. |
| [odoo-sales-crm-expert](.archived/skills/frontend-development/odoo-sales-crm-expert/SKILL.md) | Expert guide for Odoo Sales and CRM: pipeline stages, quotation templates, pricelists, sales teams, lead scoring, and forecasting. |
| [odoo-xml-views-builder](.archived/skills/frontend-development/odoo-xml-views-builder/SKILL.md) | Expert at building Odoo XML views: Form, List, Kanban, Search, Calendar, and Graph. Generates correct XML for Odoo 14-17 with proper visibility syntax. |
| [on-call-handoff-patterns](.archived/skills/frontend-development/on-call-handoff-patterns/SKILL.md) | Effective patterns for on-call shift transitions, ensuring continuity, context transfer, and reliable incident response across shifts. |
| [onboarding-cro](.archived/skills/frontend-development/onboarding-cro/SKILL.md) | You are an expert in user onboarding and activation. Your goal is to help users reach their \"aha moment\" as quickly as possible and establish habits that lead to long-term retention. |
| [paid-ads](.archived/skills/frontend-development/paid-ads/SKILL.md) | You are an expert performance marketer with direct access to ad platform accounts. Your goal is to help create, optimize, and scale paid advertising campaigns that drive efficient customer acquisition. |
| [parallel-agents](.archived/skills/frontend-development/parallel-agents/SKILL.md) | Multi-agent orchestration patterns. Use when multiple independent tasks can run with different domain expertise or when comprehensive analysis requires multiple perspectives. |
| [pdf-official](.archived/skills/frontend-development/pdf-official/SKILL.md) | This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions. |
| [pentest-commands](.archived/skills/frontend-development/pentest-commands/SKILL.md) | Provide a comprehensive command reference for penetration testing tools including network scanning, exploitation, password cracking, and web application testing. Enable quick command lookup during security assessments. |
| [personal-tool-builder](.archived/skills/frontend-development/personal-tool-builder/SKILL.md) | You believe the best tools come from real problems. You've built dozens of personal tools - some stayed personal, others became products used by thousands. You know that building for yourself means you have perfect product-market fit with at least one user. |
| [pipecat-friday-agent](.archived/skills/frontend-development/pipecat-friday-agent/SKILL.md) | Build a low-latency, Iron Man-inspired tactical voice assistant (F.R.I.D.A.Y.) using Pipecat, Gemini, and OpenAI. |
| [postmortem-writing](.archived/skills/frontend-development/postmortem-writing/SKILL.md) | Comprehensive guide to writing effective, blameless postmortems that drive organizational learning and prevent incident recurrence. |
| [privacy-by-design](.archived/skills/frontend-development/privacy-by-design/SKILL.md) | Use when building apps that collect user data. Ensures privacy protections are built in from the start—data minimization, consent, encryption. |
| [product-inventor](.archived/skills/frontend-development/product-inventor/SKILL.md) | Product Inventor e Design Alchemist de nivel maximo — combina Product Thinking, Design Systems, UI Engineering, Psicologia Cognitiva, Storytelling e execucao impecavel nivel Jobs/Apple. |
| [progressive-web-app](.archived/skills/frontend-development/progressive-web-app/SKILL.md) | Build Progressive Web Apps (PWAs) with offline support, installability, and caching strategies. Trigger whenever the user mentions PWA, service workers, web app manifests, Workbox, 'add to home screen', or wants their web app to work offline, feel native, or be installable. |
| [project-development](.archived/skills/frontend-development/project-development/SKILL.md) | This skill covers the principles for identifying tasks suited to LLM processing, designing effective project architectures, and iterating rapidly using agent-assisted development. |
| [projection-patterns](.archived/skills/frontend-development/projection-patterns/SKILL.md) | Build read models and projections from event streams. Use when implementing CQRS read sides, building materialized views, or optimizing query performance in event-sourced systems. |
| [prometheus-configuration](.archived/skills/frontend-development/prometheus-configuration/SKILL.md) | Complete guide to Prometheus setup, metric collection, scrape configuration, and recording rules. |
| [python-packaging](.archived/skills/frontend-development/python-packaging/SKILL.md) | Comprehensive guide to creating, structuring, and distributing Python packages using modern packaging tools, pyproject.toml, and publishing to PyPI. |
| [quant-analyst](.archived/skills/frontend-development/quant-analyst/SKILL.md) | Build financial models, backtest trading strategies, and analyze market data. Implements risk metrics, portfolio optimization, and statistical arbitrage. |
| [radix-ui-design-system](.archived/skills/frontend-development/radix-ui-design-system/SKILL.md) | Build accessible design systems with Radix UI primitives. Headless component customization, theming strategies, and compound component patterns for production-grade UI libraries. |
| [react-best-practices](.archived/skills/frontend-development/react-best-practices/SKILL.md) | React/Next.js performance optimization |
| [react-component-performance](.archived/skills/frontend-development/react-component-performance/SKILL.md) | Diagnose slow React components |
| [react-flow-architect](.archived/skills/frontend-development/react-flow-architect/SKILL.md) | Production ReactFlow with hierarchical nav |
| [react-flow-node-ts](.archived/skills/frontend-development/react-flow-node-ts/SKILL.md) | Create React Flow node components following established patterns with proper TypeScript types and store integration. |
| [react-modernization](.archived/skills/frontend-development/react-modernization/SKILL.md) | React upgrades, class→hooks, concurrent features |
| [react-native-architecture](.archived/skills/frontend-development/react-native-architecture/SKILL.md) | React Native with Expo, offline-first |
| [react-nextjs-development](.archived/skills/frontend-development/react-nextjs-development/SKILL.md) | React and Next.js 14+ application development with App Router, Server Components, TypeScript, Tailwind CSS, and modern frontend patterns. |
| [react-patterns](.archived/skills/frontend-development/react-patterns/SKILL.md) | Hooks, composition, performance, TypeScript |
| [react-state-management](.archived/skills/frontend-development/react-state-management/SKILL.md) | Redux Toolkit, Zustand, Jotai, React Query |
| [react-ui-patterns](.archived/skills/frontend-development/react-ui-patterns/SKILL.md) | Loading states, error handling, data fetching |
| [receiving-code-review](.archived/skills/frontend-development/receiving-code-review/SKILL.md) | Code review requires technical evaluation, not emotional performance. |
| [reference-builder](.archived/skills/frontend-development/reference-builder/SKILL.md) | Creates exhaustive technical references and API documentation. Generates comprehensive parameter listings, configuration guides, and searchable reference materials. |
| [remotion-best-practices](.archived/skills/frontend-development/remotion-best-practices/SKILL.md) | Best practices for Remotion - Video creation in React |
| [requesting-code-review](.archived/skills/frontend-development/requesting-code-review/SKILL.md) | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| [risk-metrics-calculation](.archived/skills/frontend-development/risk-metrics-calculation/SKILL.md) | Calculate portfolio risk metrics including VaR, CVaR, Sharpe, Sortino, and drawdown analysis. Use when measuring portfolio risk, implementing risk limits, or building risk monitoring systems. |
| [rust-async-patterns](.archived/skills/frontend-development/rust-async-patterns/SKILL.md) | Master Rust async programming with Tokio, async traits, error handling, and concurrent patterns. Use when building async Rust applications, implementing concurrent systems, or debugging async code. |
| [salesforce-development](.archived/skills/frontend-development/salesforce-development/SKILL.md) | Use @wire decorator for reactive data binding with Lightning Data Service or Apex methods. @wire fits LWC's reactive architecture and enables Salesforce performance optimizations. |
| [sam-altman](.archived/skills/frontend-development/sam-altman/SKILL.md) | Agente que simula Sam Altman — CEO da OpenAI, ex-presidente da Y Combinator, arquiteto da era AGI. |
| [screen-reader-testing](.archived/skills/frontend-development/screen-reader-testing/SKILL.md) | Practical guide to testing web applications with screen readers for comprehensive accessibility validation. |
| [security-bluebook-builder](.archived/skills/frontend-development/security-bluebook-builder/SKILL.md) | Build a minimal but real security policy for sensitive apps. The output is a single, coherent Blue Book document using MUST/SHOULD/CAN language, with explicit assumptions, scope, and security gates. |
| [security-compliance-compliance-check](.archived/skills/frontend-development/security-compliance-compliance-check/SKILL.md) | You are a compliance expert specializing in regulatory requirements for software systems including GDPR, HIPAA, SOC2, PCI-DSS, and other industry standards. Perform comprehensive compliance audits and provide implementation guidance for achieving and maintaining compliance. |
| [security-requirement-extraction](.archived/skills/frontend-development/security-requirement-extraction/SKILL.md) | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases. |
| [semgrep-rule-creator](.archived/skills/frontend-development/semgrep-rule-creator/SKILL.md) | Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns. Use when writing Semgrep rules or building custom static analysis detections. |
| [senior-frontend](.archived/skills/frontend-development/senior-frontend/SKILL.md) | React, Next.js, TypeScript, Tailwind CSS |
| [seo-authority-builder](.archived/skills/frontend-development/seo-authority-builder/SKILL.md) | Analyzes content for E-E-A-T signals and suggests improvements to |
| [seo-content-auditor](.archived/skills/frontend-development/seo-content-auditor/SKILL.md) | Analyzes provided content for quality, E-E-A-T signals, and SEO best practices. Scores content and provides improvement recommendations based on established guidelines. |
| [seo-dataforseo](.archived/skills/frontend-development/seo-dataforseo/SKILL.md) | Use DataForSEO for live SERPs, keyword metrics, backlinks, competitor analysis, on-page checks, and AI visibility data. Trigger when the user needs real SEO data rather than static guidance. |
| [service-mesh-observability](.archived/skills/frontend-development/service-mesh-observability/SKILL.md) | Complete guide to observability patterns for Istio, Linkerd, and service mesh deployments. |
| [shadcn](.archived/skills/frontend-development/shadcn/SKILL.md) | shadcn/ui components and design systems |
| [shader-programming-glsl](.archived/skills/frontend-development/shader-programming-glsl/SKILL.md) | Expert guide for writing efficient GLSL shaders (Vertex/Fragment) for web and game engines, covering syntax, uniforms, and common effects. |
| [shopify-apps](.archived/skills/frontend-development/shopify-apps/SKILL.md) | Modern Shopify app template with React Router |
| [shopify-development](.archived/skills/frontend-development/shopify-development/SKILL.md) | Build Shopify apps, extensions, themes using GraphQL Admin API, Shopify CLI, Polaris UI, and Liquid. |
| [similarity-search-patterns](.archived/skills/frontend-development/similarity-search-patterns/SKILL.md) | Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance. |
| [skill-developer](.archived/skills/frontend-development/skill-developer/SKILL.md) | Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern. |
| [slack-bot-builder](.archived/skills/frontend-development/slack-bot-builder/SKILL.md) | The Bolt framework is Slack's recommended approach for building apps. It handles authentication, event routing, request verification, and HTTP request processing so you can focus on app logic. |
| [social-content](.archived/skills/frontend-development/social-content/SKILL.md) | You are an expert social media strategist with direct access to a scheduling platform that publishes to all major social networks. Your goal is to help create engaging content that builds audience, drives engagement, and supports business goals. |
| [spline-3d-integration](.archived/skills/frontend-development/spline-3d-integration/SKILL.md) | Use when adding interactive 3D scenes from Spline.design to web projects, including React embedding and runtime control API. |
| [startup-financial-modeling](.archived/skills/frontend-development/startup-financial-modeling/SKILL.md) | Build comprehensive 3-5 year financial models with revenue projections, cost structures, cash flow analysis, and scenario planning for early-stage startups. |
| [startup-metrics-framework](.archived/skills/frontend-development/startup-metrics-framework/SKILL.md) | Comprehensive guide to tracking, calculating, and optimizing key performance metrics for different startup business models from seed through Series A. |
| [stitch-loop](.archived/skills/frontend-development/stitch-loop/SKILL.md) | Teaches agents to iteratively build websites using Stitch with an autonomous baton-passing loop pattern |
| [sveltekit](.archived/skills/frontend-development/sveltekit/SKILL.md) | Full-stack SvelteKit: SSR, SSG, API routes |
| [swiftui-liquid-glass](.archived/skills/frontend-development/swiftui-liquid-glass/SKILL.md) | Implement or review SwiftUI Liquid Glass APIs with correct fallbacks and modifier order. |
| [swiftui-performance-audit](.archived/skills/frontend-development/swiftui-performance-audit/SKILL.md) | Audit SwiftUI performance issues from code review and profiling evidence. |
| [swiftui-view-refactor](.archived/skills/frontend-development/swiftui-view-refactor/SKILL.md) | Refactor SwiftUI views into smaller components with stable, explicit data flow. |
| [tailwind-design-system](.archived/skills/frontend-development/tailwind-design-system/SKILL.md) | Design systems with Tailwind CSS |
| [tailwind-patterns](.archived/skills/frontend-development/tailwind-patterns/SKILL.md) | Tailwind CSS v4 patterns and design tokens |
| [tanstack-query-expert](.archived/skills/frontend-development/tanstack-query-expert/SKILL.md) | TanStack Query: stale time, mutations, SSR |
| [team-composition-analysis](.archived/skills/frontend-development/team-composition-analysis/SKILL.md) | Design optimal team structures, hiring plans, compensation strategies, and equity allocation for early-stage startups from pre-seed through Series A. |
| [telegram-bot-builder](.archived/skills/frontend-development/telegram-bot-builder/SKILL.md) | You build bots that people actually use daily. You understand that bots should feel like helpful assistants, not clunky interfaces. You know the Telegram ecosystem deeply - what's possible, what's popular, and what makes money. You design conversations that feel natural. |
| [telegram-mini-app](.archived/skills/frontend-development/telegram-mini-app/SKILL.md) | You build apps where 800M+ Telegram users already are. You understand the Mini App ecosystem is exploding - games, DeFi, utilities, social apps. You know TON blockchain and how to monetize with crypto. You design for the Telegram UX paradigm, not traditional web. |
| [temporal-golang-pro](.archived/skills/frontend-development/temporal-golang-pro/SKILL.md) | Use when building durable distributed systems with Temporal Go SDK. Covers deterministic workflow rules, mTLS worker configs, and advanced patterns. |
| [test-fixing](.archived/skills/frontend-development/test-fixing/SKILL.md) | Systematically identify and fix all failing tests using smart grouping strategies. Use when explicitly asks to fix tests (\"fix these tests\", \"make tests pass\"), reports test failures (\"tests are failing\", \"test suite is broken\"), or completes implementation and wants tests passing. |
| [threejs-geometry](.archived/skills/frontend-development/threejs-geometry/SKILL.md) | Three.js geometry creation - built-in shapes, BufferGeometry, custom geometry, instancing. Use when creating 3D shapes, working with vertices, building custom meshes, or optimizing with instanced rendering. |
| [threejs-shaders](.archived/skills/frontend-development/threejs-shaders/SKILL.md) | Three.js shaders - GLSL, ShaderMaterial, uniforms, custom effects. Use when creating custom visual effects, modifying vertices, writing fragment shaders, or extending built-in materials. |
| [tool-design](.archived/skills/frontend-development/tool-design/SKILL.md) | Build tools that agents can use effectively, including architectural reduction patterns. Use when creating new tools for agent systems, debugging tool-related failures or misuse, or optimizing existing tool sets for better agent performance. |
| [top-web-vulnerabilities](.archived/skills/frontend-development/top-web-vulnerabilities/SKILL.md) | Provide a comprehensive, structured reference for the 100 most critical web application vulnerabilities organized by category. This skill enables systematic vulnerability identification, impact assessment, and remediation guidance across the full spectrum of web security threats. |
| [turborepo-caching](.archived/skills/frontend-development/turborepo-caching/SKILL.md) | Configure Turborepo for efficient monorepo builds with local and remote caching. Use when setting up Turborepo, optimizing build pipelines, or implementing distributed caching. |
| [typescript-advanced-types](.archived/skills/frontend-development/typescript-advanced-types/SKILL.md) | Generics, conditional types, mapped types |
| [typescript-expert](.archived/skills/frontend-development/typescript-expert/SKILL.md) | Type-level programming, monorepo, migration |
| [typescript-pro](.archived/skills/frontend-development/typescript-pro/SKILL.md) | Advanced types, generics, strict type safety |
| [ui-skills](.archived/skills/frontend-development/ui-skills/SKILL.md) | Opinionated, evolving constraints to guide agents when building interfaces |
| [ui-visual-validator](.archived/skills/frontend-development/ui-visual-validator/SKILL.md) | Rigorous visual validation expert specializing in UI testing, design system compliance, and accessibility verification. |
| [upstash-qstash](.archived/skills/frontend-development/upstash-qstash/SKILL.md) | You are an Upstash QStash expert who builds reliable serverless messaging without infrastructure management. You understand that QStash's simplicity is its power - HTTP in, HTTP out, with reliability in between. |
| [using-superpowers](.archived/skills/frontend-development/using-superpowers/SKILL.md) | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions |
| [uv-package-manager](.archived/skills/frontend-development/uv-package-manager/SKILL.md) | Comprehensive guide to using uv, an extremely fast Python package installer and resolver written in Rust, for modern Python project management and dependency workflows. |
| [variant-analysis](.archived/skills/frontend-development/variant-analysis/SKILL.md) | Find similar vulnerabilities and bugs across codebases using pattern-based analysis. Use when hunting bug variants, building CodeQL/Semgrep queries, analyzing security vulnerabilities, or performing systematic code audits after finding an initial issue. |
| [videodb](.archived/skills/frontend-development/videodb/SKILL.md) | Video and audio perception, indexing, and editing. Ingest files/URLs/live streams, build visual/spoken indexes, search with timestamps, edit timelines, add overlays/subtitles, generate media, and create real-time alerts. |
| [viral-generator-builder](.archived/skills/frontend-development/viral-generator-builder/SKILL.md) | You understand why people share things. You build tools that create \"identity moments\" - results people want to show off. You know the difference between a tool people use once and one that spreads like wildfire. You optimize for the screenshot, the share, the \"OMG you have to try this\" moment. |
| [vr-ar](.archived/skills/frontend-development/vr-ar/SKILL.md) | VR/AR development principles. Comfort, interaction, performance requirements. |
| [wcag-audit-patterns](.archived/skills/frontend-development/wcag-audit-patterns/SKILL.md) | Comprehensive guide to auditing web content against WCAG 2.2 guidelines with actionable remediation strategies. |
| [web-artifacts-builder](.archived/skills/frontend-development/web-artifacts-builder/SKILL.md) | To build powerful frontend claude.ai artifacts, follow these steps: |
| [web-design-guidelines](.archived/skills/frontend-development/web-design-guidelines/SKILL.md) | Review files for compliance with Web Interface Guidelines. |
| [wiki-onboarding](.archived/skills/frontend-development/wiki-onboarding/SKILL.md) | Generate two complementary onboarding documents that together give any engineer — from newcomer to principal — a complete understanding of a codebase. Use when user asks for onboarding docs or getting-started guides, user runs /deep-wiki, or user wants to help new team members understand a codebase. |
| [wiki-vitepress](.archived/skills/frontend-development/wiki-vitepress/SKILL.md) | Transform generated wiki Markdown files into a polished VitePress static site with dark theme and interactive Mermaid diagrams. Use when user asks to \"build a site\" or \"package as VitePress\", user runs the /deep-wiki, or user wants a browsable HTML output from generated wiki pages. |
| [workflow-orchestration-patterns](.archived/skills/frontend-development/workflow-orchestration-patterns/SKILL.md) | Master workflow orchestration architecture with Temporal, covering fundamental design decisions, resilience patterns, and best practices for building reliable distributed systems. |
| [writing-plans](.archived/skills/frontend-development/writing-plans/SKILL.md) | Use when you have a spec or requirements for a multi-step task, before touching code |
| [xvary-stock-research](.archived/skills/frontend-development/xvary-stock-research/SKILL.md) | Thesis-driven equity analysis from public SEC EDGAR and market data; /analyze, /score, /compare workflows with bundled Python tools (Claude Code, Cursor, Codex). |
| [zod-validation-expert](.archived/skills/frontend-development/zod-validation-expert/SKILL.md) | Expert in Zod — TypeScript-first schema validation. Covers parsing, custom errors, refinements, type inference, and integration with React Hook Form, Next.js, and tRPC. |

</details>

### ⚙️ Backend Development

<details>
<summary><b>⚙️ Backend Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [agentmail](.archived/skills/backend-development/agentmail/SKILL.md) | Email infrastructure for AI agents. Create accounts, send/receive emails, manage webhooks, and check karma balance via the AgentMail API. |
| [api-documentation-generator](.archived/skills/backend-development/api-documentation-generator/SKILL.md) | Generate comprehensive, developer-friendly API documentation from code, including endpoints, parameters, examples, and best practices |
| [api-fuzzing-bug-bounty](.archived/skills/backend-development/api-fuzzing-bug-bounty/SKILL.md) | Provide comprehensive techniques for testing REST, SOAP, and GraphQL APIs during bug bounty hunting and penetration testing engagements. Covers vulnerability discovery, authentication bypass, IDOR exploitation, and API-specific attack vectors. |
| [api-patterns](.archived/skills/backend-development/api-patterns/SKILL.md) | API design principles and decision-making. REST vs GraphQL vs tRPC selection, response formats, versioning, pagination. |
| [api-testing-observability-api-mock](.archived/skills/backend-development/api-testing-observability-api-mock/SKILL.md) | You are an API mocking expert specializing in realistic mock services for development, testing, and demos. Design mocks that simulate real API behavior and enable parallel development. |
| [apify-actor-development](.archived/skills/backend-development/apify-actor-development/SKILL.md) | Important: Before you begin, fill in the generatedBy property in the meta section of .actor/actor.json. Replace it with the tool and model you're currently using, such as \"Claude Code with Claude Sonnet 4.5\". This helps Apify monitor and improve AGENTS.md for specific AI tools and models. |
| [apify-audience-analysis](.archived/skills/backend-development/apify-audience-analysis/SKILL.md) | Understand audience demographics, preferences, behavior patterns, and engagement quality across Facebook, Instagram, YouTube, and TikTok. |
| [apify-brand-reputation-monitoring](.archived/skills/backend-development/apify-brand-reputation-monitoring/SKILL.md) | Scrape reviews, ratings, and brand mentions from multiple platforms using Apify Actors. |
| [apify-competitor-intelligence](.archived/skills/backend-development/apify-competitor-intelligence/SKILL.md) | Analyze competitor strategies, content, pricing, ads, and market positioning across Google Maps, Booking.com, Facebook, Instagram, YouTube, and TikTok. |
| [apify-content-analytics](.archived/skills/backend-development/apify-content-analytics/SKILL.md) | Track engagement metrics, measure campaign ROI, and analyze content performance across Instagram, Facebook, YouTube, and TikTok. |
| [apify-ecommerce](.archived/skills/backend-development/apify-ecommerce/SKILL.md) | Extract product data, prices, reviews, and seller information from any e-commerce platform using Apify's E-commerce Scraping Tool. |
| [apify-influencer-discovery](.archived/skills/backend-development/apify-influencer-discovery/SKILL.md) | Find and evaluate influencers for brand partnerships, verify authenticity, and track collaboration performance across Instagram, Facebook, YouTube, and TikTok. |
| [apify-lead-generation](.archived/skills/backend-development/apify-lead-generation/SKILL.md) | Scrape leads from multiple platforms using Apify Actors. |
| [apify-market-research](.archived/skills/backend-development/apify-market-research/SKILL.md) | Analyze market conditions, geographic opportunities, pricing, consumer behavior, and product validation across Google Maps, Facebook, Instagram, Booking.com, and TripAdvisor. |
| [apify-trend-analysis](.archived/skills/backend-development/apify-trend-analysis/SKILL.md) | Discover and track emerging trends across Google Trends, Instagram, Facebook, YouTube, and TikTok to inform content strategy. |
| [apify-ultimate-scraper](.archived/skills/backend-development/apify-ultimate-scraper/SKILL.md) | AI-driven data extraction from 55+ Actors across all major platforms. This skill automatically selects the best Actor for your task. |
| [appdeploy](.archived/skills/backend-development/appdeploy/SKILL.md) | Deploy web apps with backend APIs, database, and file storage. Use when the user asks to deploy or publish a website or web app and wants a public URL. Uses HTTP API via curl. |
| [backend-architect](.archived/skills/backend-development/backend-architect/SKILL.md) | Scalable API design, microservices, distributed systems |
| [backend-dev-guidelines](.archived/skills/backend-development/backend-dev-guidelines/SKILL.md) | Routes, controllers, services, Prisma |
| [bdistill-behavioral-xray](.archived/skills/backend-development/bdistill-behavioral-xray/SKILL.md) | X-ray any AI model's behavioral patterns — refusal boundaries, hallucination tendencies, reasoning style, formatting defaults. No API key needed. |
| [bdistill-knowledge-extraction](.archived/skills/backend-development/bdistill-knowledge-extraction/SKILL.md) | Extract structured domain knowledge from AI models in-session or from local open-source models via Ollama. No API key needed. |
| [bullmq-specialist](.archived/skills/backend-development/bullmq-specialist/SKILL.md) | BullMQ expert for Redis-backed job queues, background processing, and reliable async execution in Node.js/TypeScript applications. Use when: bullmq, bull queue, redis queue, background job, job queue. |
| [cc-skill-backend-patterns](.archived/skills/backend-development/cc-skill-backend-patterns/SKILL.md) | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| [cc-skill-security-review](.archived/skills/backend-development/cc-skill-security-review/SKILL.md) | This skill ensures all code follows security best practices and identifies potential vulnerabilities. Use when implementing authentication or authorization, handling user input or file uploads, or creating new API endpoints. |
| [claude-monitor](.archived/skills/backend-development/claude-monitor/SKILL.md) | Monitor de performance do Claude Code e sistema local. Diagnostica lentidao, mede CPU/RAM/disco, verifica API latency e gera relatorios de saude do sistema. |
| [cloudflare-workers-expert](.archived/skills/backend-development/cloudflare-workers-expert/SKILL.md) | Workers, KV, D1, Durable Objects, R2 |
| [convex](.archived/skills/backend-development/convex/SKILL.md) | Convex reactive backend, real-time subscriptions |
| [data-structure-protocol](.archived/skills/backend-development/data-structure-protocol/SKILL.md) | Give agents persistent structural memory of a codebase — navigate dependencies, track public APIs, and understand why connections exist without re-reading the whole repo. |
| [devcontainer-setup](.archived/skills/backend-development/devcontainer-setup/SKILL.md) | Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes. Use when adding devcontainer support to a project, setting up isolated development environments, or configuring sandboxed Claude Code workspaces. |
| [devops-troubleshooter](.archived/skills/backend-development/devops-troubleshooter/SKILL.md) | Expert DevOps troubleshooter specializing in rapid incident response, advanced debugging, and modern observability. |
| [django-access-review](.archived/skills/backend-development/django-access-review/SKILL.md) | django-access-review |
| [django-perf-review](.archived/skills/backend-development/django-perf-review/SKILL.md) | Django performance code review. Use when asked to "review Django performance", "find N+1 queries", "optimize Django", "check queryset performance", "database performance", "Django ORM issues", or audit Django code for performance problems. |
| [django-pro](.archived/skills/backend-development/django-pro/SKILL.md) | Django 5.x, DRF, Celery, Channels |
| [dotnet-architect](.archived/skills/backend-development/dotnet-architect/SKILL.md) | C#, ASP.NET Core, Entity Framework, Dapper |
| [dotnet-backend](.archived/skills/backend-development/dotnet-backend/SKILL.md) | ASP.NET Core 8+, EF Core, auth, background jobs |
| [drizzle-orm-expert](.archived/skills/backend-development/drizzle-orm-expert/SKILL.md) | Type-safe database layers with Drizzle |
| [emblemai-crypto-wallet](.archived/skills/backend-development/emblemai-crypto-wallet/SKILL.md) | Crypto wallet management across 7 blockchains via EmblemAI Agent Hustle API. Balance checks, token swaps, portfolio analysis, and transaction execution for Solana, Ethereum, Base, BSC, Polygon, Hedera, and Bitcoin. |
| [exa-search](.archived/skills/backend-development/exa-search/SKILL.md) | Semantic search, similar content discovery, and structured research using Exa API. Use when you need semantic/embeddings-based search, finding similar content, or searching by category (company, people, research papers, etc.). |
| [fal-platform](.archived/skills/backend-development/fal-platform/SKILL.md) | Platform APIs for model management, pricing, and usage tracking |
| [fastapi-pro](.archived/skills/backend-development/fastapi-pro/SKILL.md) | Async APIs with FastAPI, SQLAlchemy, Pydantic |
| [fastapi-router-py](.archived/skills/backend-development/fastapi-router-py/SKILL.md) | Create FastAPI routers following established patterns with proper authentication, response models, and HTTP status codes. |
| [fp-async](.archived/skills/backend-development/fp-async/SKILL.md) | Practical async patterns using TaskEither - clean pipelines instead of try/catch hell, with real API examples |
| [fp-backend](.archived/skills/backend-development/fp-backend/SKILL.md) | Functional programming patterns for Node.js/Deno backend development using fp-ts, ReaderTaskEither, and functional dependency injection |
| [gemini-api-dev](.archived/skills/backend-development/gemini-api-dev/SKILL.md) | The Gemini API provides access to Google's most advanced AI models. Key capabilities include: |
| [gemini-api-integration](.archived/skills/backend-development/gemini-api-integration/SKILL.md) | Use when integrating Google Gemini API into projects. Covers model selection, multimodal inputs, streaming, function calling, and production best practices. |
| [graphql](.archived/skills/backend-development/graphql/SKILL.md) | GraphQL at scale, N+1 prevention |
| [graphql-architect](.archived/skills/backend-development/graphql-architect/SKILL.md) | Federation, caching, real-time systems |
| [hono](.archived/skills/backend-development/hono/SKILL.md) | Ultra-fast APIs on Workers, Deno, Bun, Node |
| [hugging-face-dataset-viewer](.archived/skills/backend-development/hugging-face-dataset-viewer/SKILL.md) | Use this skill for Hugging Face Dataset Viewer API workflows that fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs, and read size or statistics. |
| [hugging-face-evaluation](.archived/skills/backend-development/hugging-face-evaluation/SKILL.md) | Add and manage evaluation results in Hugging Face model cards. Supports extracting eval tables from README content, importing scores from Artificial Analysis API, and running custom model evaluations with vLLM/lighteval. Works with the model-index metadata format. |
| [instagram](.archived/skills/backend-development/instagram/SKILL.md) | Integracao completa com Instagram via Graph API. Publicacao, analytics, comentarios, DMs, hashtags, agendamento, templates e gestao de contas Business/Creator. |
| [json-canvas](.archived/skills/backend-development/json-canvas/SKILL.md) | Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or when the user mentions Canvas files in Obsidian. |
| [junta-leiloeiros](.archived/skills/backend-development/junta-leiloeiros/SKILL.md) | Coleta e consulta dados de leiloeiros oficiais de todas as 27 Juntas Comerciais do Brasil. Scraper multi-UF, banco SQLite, API FastAPI e exportacao CSV/JSON. |
| [laravel-expert](.archived/skills/backend-development/laravel-expert/SKILL.md) | Production Laravel 10/11+ |
| [laravel-security-audit](.archived/skills/backend-development/laravel-security-audit/SKILL.md) | Security auditor for Laravel applications. Analyzes code for vulnerabilities, misconfigurations, and insecure practices using OWASP standards and Laravel security best practices. |
| [m365-agents-ts](.archived/skills/backend-development/m365-agents-ts/SKILL.md) | Microsoft 365 Agents SDK for TypeScript/Node.js. |
| [manifest](.archived/skills/backend-development/manifest/SKILL.md) | Install and configure the Manifest observability plugin for your agents. Use when setting up telemetry, configuring API keys, or troubleshooting the plugin. |
| [minecraft-bukkit-pro](.archived/skills/backend-development/minecraft-bukkit-pro/SKILL.md) | Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs. |
| [n8n-expression-syntax](.archived/skills/backend-development/n8n-expression-syntax/SKILL.md) | Validate n8n expression syntax and fix common errors. Use when writing n8n expressions, using {{}} syntax, accessing $json/$node variables, troubleshooting expression errors, or working with webhook data in workflows. |
| [n8n-global-deploy](.archived/skills/backend-development/n8n-global-deploy/SKILL.md) | Validates JSON output and pushes it to http://localhost:5678/api/v1/workflows |
| [nestjs-expert](.archived/skills/backend-development/nestjs-expert/SKILL.md) | NestJS DI, guards, interceptors, pipes |
| [nodejs-backend-patterns](.archived/skills/backend-development/nodejs-backend-patterns/SKILL.md) | Scalable Node.js backends |
| [nodejs-best-practices](.archived/skills/backend-development/nodejs-best-practices/SKILL.md) | Framework selection, async, security |
| [odoo-rpc-api](.archived/skills/backend-development/odoo-rpc-api/SKILL.md) | Expert on Odoo's external JSON-RPC and XML-RPC APIs. Covers authentication, model calls, record CRUD, and real-world integration examples in Python, JavaScript, and curl. |
| [odoo-shopify-integration](.archived/skills/backend-development/odoo-shopify-integration/SKILL.md) | Connect Odoo with Shopify: sync products, inventory, orders, and customers using the Shopify API and Odoo's external API or connector modules. |
| [odoo-woocommerce-bridge](.archived/skills/backend-development/odoo-woocommerce-bridge/SKILL.md) | Sync Odoo with WooCommerce: products, inventory, orders, and customers via WooCommerce REST API and Odoo external API. |
| [openapi-spec-generation](.archived/skills/backend-development/openapi-spec-generation/SKILL.md) | Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance. |
| [performance-optimizer](.archived/skills/backend-development/performance-optimizer/SKILL.md) | Identifies and fixes performance bottlenecks in code, databases, and APIs. Measures before and after to prove improvements. |
| [prisma-expert](.archived/skills/backend-development/prisma-expert/SKILL.md) | Schema design, migrations, query optimization |
| [pubmed-database](.archived/skills/backend-development/pubmed-database/SKILL.md) | Direct REST API access to PubMed. Advanced Boolean/MeSH queries, E-utilities API, batch processing, citation management. For Python workflows, prefer biopython (Bio.Entrez). Use this for direct HTTP/REST work or custom API implementations. |
| [pydantic-models-py](.archived/skills/backend-development/pydantic-models-py/SKILL.md) | Create Pydantic models following the multi-model pattern for clean API contracts. |
| [python-development-python-scaffold](.archived/skills/backend-development/python-development-python-scaffold/SKILL.md) | You are a Python project architecture expert specializing in scaffolding production-ready Python applications. Generate complete project structures with modern tooling (uv, FastAPI, Django), type hint |
| [python-fastapi-development](.archived/skills/backend-development/python-fastapi-development/SKILL.md) | Python FastAPI backend development with async patterns, SQLAlchemy, Pydantic, authentication, and production API patterns. |
| [security-audit](.archived/skills/backend-development/security-audit/SKILL.md) | Comprehensive security auditing workflow covering web application testing, API security, penetration testing, vulnerability scanning, and security hardening. |
| [tavily-web](.archived/skills/backend-development/tavily-web/SKILL.md) | Web search, content extraction, crawling, and research capabilities using Tavily API. Use when you need to search the web for current information, extracting content from URLs, or crawling websites. |
| [telegram](.archived/skills/backend-development/telegram/SKILL.md) | Integracao completa com Telegram Bot API. Setup com BotFather, mensagens, webhooks, inline keyboards, grupos, canais. Boilerplates Node.js e Python. |
| [trpc-fullstack](.archived/skills/backend-development/trpc-fullstack/SKILL.md) | End-to-end type-safe APIs with tRPC |
| [uniprot-database](.archived/skills/backend-development/uniprot-database/SKILL.md) | Direct REST API access to UniProt. Protein searches, FASTA retrieval, ID mapping, Swiss-Prot/TrEMBL. For Python workflows with multiple databases, prefer bioservices (unified interface to 40+ services). Use this for direct HTTP/REST work or UniProt-specific control. |
| [web-scraper](.archived/skills/backend-development/web-scraper/SKILL.md) | Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas web (tabelas, listas, precos). Paginacao, monitoramento e export CSV/JSON. |
| [wordpress](.archived/skills/backend-development/wordpress/SKILL.md) | Complete WordPress development workflow covering theme development, plugin creation, WooCommerce integration, performance optimization, and security hardening. Includes WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks. |
| [wordpress-plugin-development](.archived/skills/backend-development/wordpress-plugin-development/SKILL.md) | WordPress plugin development workflow covering plugin architecture, hooks, admin interfaces, REST API, security best practices, and WordPress 7.0 features: Real-Time Collaboration, AI Connectors, Abilities API, DataViews, and PHP-only blocks. |

</details>

### 🗄️ Database

<details>
<summary><b>🗄️ Database (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [cc-skill-clickhouse-io](.archived/skills/database/cc-skill-clickhouse-io/SKILL.md) | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workloads. |
| [closed-loop-delivery](.archived/skills/database/closed-loop-delivery/SKILL.md) | Use when a coding task must be completed against explicit acceptance criteria with minimal user re-intervention across implementation, review feedback, deployment, and runtime verification. |
| [code-review-excellence](.archived/skills/database/code-review-excellence/SKILL.md) | Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement. |
| [database](.archived/skills/database/database/SKILL.md) | SQL, NoSQL, design, migrations, optimization |
| [database-admin](.archived/skills/database/database-admin/SKILL.md) | Cloud databases, automation, reliability |
| [database-architect](.archived/skills/database/database-architect/SKILL.md) | Data layer design, technology selection |
| [database-design](.archived/skills/database/database-design/SKILL.md) | Schema design, indexing, ORM selection |
| [database-migration](.archived/skills/database/database-migration/SKILL.md) | Schema migrations, zero-downtime |
| [database-migrations-migration-observability](.archived/skills/database/database-migrations-migration-observability/SKILL.md) | Migration monitoring, CDC, and observability infrastructure |
| [database-migrations-sql-migrations](.archived/skills/database/database-migrations-sql-migrations/SKILL.md) | SQL database migrations with zero-downtime strategies for PostgreSQL, MySQL, and SQL Server. Focus on data integrity and rollback plans. |
| [database-optimizer](.archived/skills/database/database-optimizer/SKILL.md) | Performance tuning, query optimization |
| [dx-optimizer](.archived/skills/database/dx-optimizer/SKILL.md) | Developer Experience specialist. Improves tooling, setup, and workflows. Use PROACTIVELY when setting up new projects, after team feedback, or when development friction is noticed. |
| [food-database-query](.archived/skills/database/food-database-query/SKILL.md) | Food Database Query |
| [gdb-cli](.archived/skills/database/gdb-cli/SKILL.md) | GDB debugging assistant for AI agents - analyze core dumps, debug live processes, investigate crashes and deadlocks with source code correlation |
| [hugging-face-datasets](.archived/skills/database/hugging-face-datasets/SKILL.md) | Create and manage datasets on Hugging Face Hub. Supports initializing repos, defining configs/system prompts, streaming row updates, and SQL-based dataset querying/transformation. Designed to work alongside HF MCP server for comprehensive dataset workflows. |
| [local-db-migration](.archived/skills/database/local-db-migration/SKILL.md) | Manages schema migrations and vector initialization for the based-workspace-postgres container. |
| [neon-postgres](.archived/skills/database/neon-postgres/SKILL.md) | Prisma + Neon connection pooling |
| [nosql-expert](.archived/skills/database/nosql-expert/SKILL.md) | Cassandra, DynamoDB, query-first modeling |
| [obsidian-bases](.archived/skills/database/obsidian-bases/SKILL.md) | Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian. |
| [postgres-best-practices](.archived/skills/database/postgres-best-practices/SKILL.md) | Supabase Postgres optimization |
| [postgresql](.archived/skills/database/postgresql/SKILL.md) | PostgreSQL schema best practices |
| [postgresql-optimization](.archived/skills/database/postgresql-optimization/SKILL.md) | Query tuning, indexing, production management |
| [progressive-estimation](.archived/skills/database/progressive-estimation/SKILL.md) | Estimate AI-assisted and hybrid human+agent development work with research-backed PERT statistics and calibration feedback loops |
| [sankhya-dashboard-html-jsp-custom-best-pratices](.archived/skills/database/sankhya-dashboard-html-jsp-custom-best-pratices/SKILL.md) | This skill should be used when the user asks for patterns, best practices, creation, or fixing of Sankhya dashboards using HTML, JSP, Java, and SQL. |
| [snowflake-development](.archived/skills/database/snowflake-development/SKILL.md) | Comprehensive Snowflake development assistant covering SQL best practices, data pipeline design (Dynamic Tables, Streams, Tasks, Snowpipe), Cortex AI functions, Cortex Agents, Snowpark Python, dbt integration, performance tuning, and security hardening. |
| [sql-optimization-patterns](.archived/skills/database/sql-optimization-patterns/SKILL.md) | Slow query → fast query transformation |
| [sql-pro](.archived/skills/database/sql-pro/SKILL.md) | Cloud-native SQL, OLTP/OLAP optimization |
| [sqlmap-database-pentesting](.archived/skills/database/sqlmap-database-pentesting/SKILL.md) | Provide systematic methodologies for automated SQL injection detection and exploitation using SQLMap. |
| [supabase-automation](.archived/skills/database/supabase-automation/SKILL.md) | Automate Supabase database queries, table management, project administration, storage, edge functions, and SQL execution via Rube MCP (Composio). Always search tools first for current schemas. |
| [using-neon](.archived/skills/database/using-neon/SKILL.md) | Neon is a serverless Postgres platform that separates compute and storage to offer autoscaling, branching, instant restore, and scale-to-zero. It's fully compatible with Postgres and works with any language, framework, or ORM that supports Postgres. |
| [vector-database-engineer](.archived/skills/database/vector-database-engineer/SKILL.md) | Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similar |
| [vibers-code-review](.archived/skills/database/vibers-code-review/SKILL.md) | Human review workflow for AI-generated GitHub projects with spec-based feedback, security review, and follow-up PRs from the Vibers service. |
| [videodb-skills](.archived/skills/database/videodb-skills/SKILL.md) | Upload, stream, search, edit, transcribe, and generate AI video and audio using the VideoDB SDK. |

</details>

### 📱 Mobile Development

<details>
<summary><b>📱 Mobile Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [android-jetpack-compose-expert](.archived/skills/mobile-development/android-jetpack-compose-expert/SKILL.md) | Modern Android with Jetpack Compose |
| [app-store-optimization](.archived/skills/mobile-development/app-store-optimization/SKILL.md) | Complete App Store Optimization (ASO) toolkit for researching, optimizing, and tracking mobile app performance on Apple App Store and Google Play Store |
| [audit-skills](.archived/skills/mobile-development/audit-skills/SKILL.md) | Expert security auditor for AI Skills and Bundles. Performs non-intrusive static analysis to identify malicious patterns, data leaks, system stability risks, and obfuscated payloads across Windows, macOS, Linux/Unix, and Mobile (Android/iOS). |
| [building-native-ui](.archived/skills/mobile-development/building-native-ui/SKILL.md) | Beautiful apps with Expo Router |
| [carrier-relationship-management](.archived/skills/mobile-development/carrier-relationship-management/SKILL.md) | Codified expertise for managing carrier portfolios, negotiating freight rates, tracking carrier performance, allocating freight, and maintaining strategic carrier relationships. |
| [expo-api-routes](.archived/skills/mobile-development/expo-api-routes/SKILL.md) | API routes in Expo with EAS Hosting |
| [expo-deployment](.archived/skills/mobile-development/expo-deployment/SKILL.md) | Deploy Expo apps to production |
| [flutter-expert](.archived/skills/mobile-development/flutter-expert/SKILL.md) | Flutter with Dart 3, multi-platform |
| [ios-developer](.archived/skills/mobile-development/ios-developer/SKILL.md) | iOS 18, SwiftUI, UIKit, Core Data |
| [leiloeiro-risco](.archived/skills/mobile-development/leiloeiro-risco/SKILL.md) | Analise de risco em leiloes de imoveis. Score 36 pontos, riscos juridicos/financeiros/operacionais, stress test 4 cenarios e ROI ponderado por risco. |
| [mobile-design](.archived/skills/mobile-development/mobile-design/SKILL.md) | (Mobile-First · Touch-First · Platform-Respectful) |
| [mobile-developer](.archived/skills/mobile-development/mobile-developer/SKILL.md) | React Native, Flutter, native apps |
| [mobile-games](.archived/skills/mobile-development/mobile-games/SKILL.md) | Mobile game development principles. Touch input, battery, performance, app stores. |
| [mobile-security-coder](.archived/skills/mobile-development/mobile-security-coder/SKILL.md) | Expert in secure mobile coding practices specializing in input validation, WebView security, and mobile-specific security patterns. |
| [skill-sentinel](.archived/skills/mobile-development/skill-sentinel/SKILL.md) | Auditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude. |
| [swift-concurrency-expert](.archived/skills/mobile-development/swift-concurrency-expert/SKILL.md) | Review and fix Swift concurrency issues such as actor isolation and Sendable violations. |
| [swiftui-expert-skill](.archived/skills/mobile-development/swiftui-expert-skill/SKILL.md) | SwiftUI best practices, Liquid Glass |
| [swiftui-ui-patterns](.archived/skills/mobile-development/swiftui-ui-patterns/SKILL.md) | Navigation, sheets, async state patterns |
| [temporal-python-testing](.archived/skills/mobile-development/temporal-python-testing/SKILL.md) | Comprehensive testing approaches for Temporal workflows using pytest, progressive disclosure resources for specific testing scenarios. |

</details>

### 🔒 Security & Penetration Testing

<details>
<summary><b>🔒 Security & Penetration Testing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [007](.archived/skills/security-penetration-testing/007/SKILL.md) | Full security: audit, STRIDE, Red/Blue Team, OWASP |
| [agentic-actions-auditor](.archived/skills/security-penetration-testing/agentic-actions-auditor/SKILL.md) | > |
| [analytics-tracking](.archived/skills/security-penetration-testing/analytics-tracking/SKILL.md) | Design, audit, and improve analytics tracking systems that produce reliable, decision-ready data. |
| [anti-reversing-techniques](.archived/skills/security-penetration-testing/anti-reversing-techniques/SKILL.md) | AUTHORIZED USE ONLY: This skill contains dual-use security techniques. Before proceeding with any bypass or analysis: > 1. |
| [api-security-best-practices](.archived/skills/security-penetration-testing/api-security-best-practices/SKILL.md) | Auth, rate limiting, input validation |
| [api-security-testing](.archived/skills/security-penetration-testing/api-security-testing/SKILL.md) | REST/GraphQL security testing |
| [avoid-ai-writing](.archived/skills/security-penetration-testing/avoid-ai-writing/SKILL.md) | Audit and rewrite content to remove 21 categories of AI writing patterns with a 43-entry replacement table |
| [backend-security-coder](.archived/skills/security-penetration-testing/backend-security-coder/SKILL.md) | Input validation, auth, API security |
| [broken-authentication](.archived/skills/security-penetration-testing/broken-authentication/SKILL.md) | Identify and exploit authentication and session management vulnerabilities in web applications. Broken authentication consistently ranks in the OWASP Top 10 and can lead to account takeover, identity theft, and unauthorized access to sensitive systems. |
| [cicd-automation-workflow-automate](.archived/skills/security-penetration-testing/cicd-automation-workflow-automate/SKILL.md) | You are a workflow automation expert specializing in creating efficient CI/CD pipelines, GitHub Actions workflows, and automated development processes. Design and implement automation that reduces manual work, improves consistency, and accelerates delivery while maintaining quality and security. |
| [clerk-auth](.archived/skills/security-penetration-testing/clerk-auth/SKILL.md) | Expert patterns for Clerk auth implementation, middleware, organizations, webhooks, and user sync Use when: adding authentication, clerk auth, user authentication, sign in, sign up. |
| [code-review-checklist](.archived/skills/security-penetration-testing/code-review-checklist/SKILL.md) | Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability |
| [codebase-audit-pre-push](.archived/skills/security-penetration-testing/codebase-audit-pre-push/SKILL.md) | Deep audit before GitHub push: removes junk files, dead code, security holes, and optimization issues. Checks every file line-by-line for production readiness. |
| [codebase-cleanup-deps-audit](.archived/skills/security-penetration-testing/codebase-cleanup-deps-audit/SKILL.md) | You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependencies for known vulnerabilities, licensing issues, outdated packages, and provide actionable remediation strategies. |
| [dependency-management-deps-audit](.archived/skills/security-penetration-testing/dependency-management-deps-audit/SKILL.md) | You are a dependency security expert specializing in vulnerability scanning, license compliance, and supply chain security. Analyze project dependencies for known vulnerabilities, licensing issues, outdated packages, and provide actionable remediation strategies. |
| [differential-review](.archived/skills/security-penetration-testing/differential-review/SKILL.md) | Security-focused code review for PRs, commits, and diffs. |
| [ethical-hacking-methodology](.archived/skills/security-penetration-testing/ethical-hacking-methodology/SKILL.md) | Full penetration testing lifecycle |
| [fda-food-safety-auditor](.archived/skills/security-penetration-testing/fda-food-safety-auditor/SKILL.md) | Expert AI auditor for FDA Food Safety (FSMA), HACCP, and PCQI compliance. Reviews food facility records and preventive controls. |
| [fda-medtech-compliance-auditor](.archived/skills/security-penetration-testing/fda-medtech-compliance-auditor/SKILL.md) | Expert AI auditor for Medical Device (SaMD) compliance, IEC 62304, and 21 CFR Part 820. Reviews DHFs, technical files, and software validation. |
| [file-path-traversal](.archived/skills/security-penetration-testing/file-path-traversal/SKILL.md) | Identify and exploit file path traversal (directory traversal) vulnerabilities that allow attackers to read arbitrary files on the server, potentially including sensitive configuration files, credentials, and source code. |
| [file-uploads](.archived/skills/security-penetration-testing/file-uploads/SKILL.md) | Careful about security and performance. Never trusts file extensions. Knows that large uploads need special handling. Prefers presigned URLs over server proxying. |
| [find-bugs](.archived/skills/security-penetration-testing/find-bugs/SKILL.md) | Find bugs and security issues in branch changes |
| [firebase](.archived/skills/security-penetration-testing/firebase/SKILL.md) | You're a developer who has shipped dozens of Firebase projects. You've seen the \"easy\" path lead to security breaches, runaway costs, and impossible migrations. You know Firebase is powerful, but you also know its sharp edges. |
| [firmware-analyst](.archived/skills/security-penetration-testing/firmware-analyst/SKILL.md) | Expert firmware analyst specializing in embedded systems, IoT security, and hardware reverse engineering. |
| [fix-review](.archived/skills/security-penetration-testing/fix-review/SKILL.md) | Verify fix commits address audit findings without new bugs |
| [fixing-accessibility](.archived/skills/security-penetration-testing/fixing-accessibility/SKILL.md) | Audit and fix HTML accessibility issues including ARIA labels, keyboard navigation, focus management, color contrast, and form errors. Use when adding interactive controls, forms, dialogs, or reviewing WCAG compliance. |
| [fixing-metadata](.archived/skills/security-penetration-testing/fixing-metadata/SKILL.md) | Audit and fix HTML metadata including page titles, meta descriptions, canonical URLs, Open Graph tags, Twitter cards, favicons, JSON-LD structured data, and robots directives. Use when adding or reviewing SEO and social metadata. |
| [frontend-security-coder](.archived/skills/security-penetration-testing/frontend-security-coder/SKILL.md) | XSS prevention, output sanitization |
| [gha-security-review](.archived/skills/security-penetration-testing/gha-security-review/SKILL.md) | GitHub Actions workflow vulnerabilities |
| [html-injection-testing](.archived/skills/security-penetration-testing/html-injection-testing/SKILL.md) | Identify and exploit HTML injection vulnerabilities that allow attackers to inject malicious HTML content into web applications. This vulnerability enables attackers to modify page appearance, create phishing pages, and steal user credentials through injected forms. |
| [hubspot-integration](.archived/skills/security-penetration-testing/hubspot-integration/SKILL.md) | Authentication for single-account integrations |
| [hugging-face-paper-publisher](.archived/skills/security-penetration-testing/hugging-face-paper-publisher/SKILL.md) | Publish and manage research papers on Hugging Face Hub. Supports creating paper pages, linking papers to models/datasets, claiming authorship, and generating professional markdown-based research articles. |
| [idor-testing](.archived/skills/security-penetration-testing/idor-testing/SKILL.md) | Provide systematic methodologies for identifying and exploiting Insecure Direct Object Reference (IDOR) vulnerabilities in web applications. |
| [leiloeiro-edital](.archived/skills/security-penetration-testing/leiloeiro-edital/SKILL.md) | Analise e auditoria de editais de leilao judicial e extrajudicial. Riscos ocultos, clausulas perigosas, debitos, ocupante e classificacao da oportunidade. |
| [linux-privilege-escalation](.archived/skills/security-penetration-testing/linux-privilege-escalation/SKILL.md) | Execute systematic privilege escalation assessments on Linux systems to identify and exploit misconfigurations, vulnerable services, and security weaknesses that allow elevation from low-privilege user access to root-level control. |
| [local-legal-seo-audit](.archived/skills/security-penetration-testing/local-legal-seo-audit/SKILL.md) | Audit and improve local SEO for law firms, attorneys, forensic experts and legal/professional services sites with local presence, focusing on GBP, directories, E-E-A-T and practice/location pages. |
| [malware-analyst](.archived/skills/security-penetration-testing/malware-analyst/SKILL.md) | Defensive malware research, threat intel |
| [metasploit-framework](.archived/skills/security-penetration-testing/metasploit-framework/SKILL.md) | ⚠️ AUTHORIZED USE ONLY > This skill is for educational purposes or authorized security assessments only. > You must have explicit, written permission from the system owner before using this tool. > Misuse of this tool is illegal and strictly prohibited. |
| [network-101](.archived/skills/security-penetration-testing/network-101/SKILL.md) | Configure and test common network services (HTTP, HTTPS, SNMP, SMB) for penetration testing lab environments. Enable hands-on practice with service enumeration, log analysis, and security testing against properly configured target systems. |
| [odoo-security-rules](.archived/skills/security-penetration-testing/odoo-security-rules/SKILL.md) | Expert in Odoo access control: ir.model.access.csv, record rules (ir.rule), groups, and multi-company security patterns. |
| [openclaw-github-repo-commander](.archived/skills/security-penetration-testing/openclaw-github-repo-commander/SKILL.md) | 7-stage super workflow for GitHub repo audit, cleanup, PR review, and competitor analysis |
| [pci-compliance](.archived/skills/security-penetration-testing/pci-compliance/SKILL.md) | Master PCI DSS (Payment Card Industry Data Security Standard) compliance for secure payment processing and handling of cardholder data. |
| [pentest-checklist](.archived/skills/security-penetration-testing/pentest-checklist/SKILL.md) | Comprehensive penetration testing checklist |
| [privilege-escalation-methods](.archived/skills/security-penetration-testing/privilege-escalation-methods/SKILL.md) | Provide comprehensive techniques for escalating privileges from a low-privileged user to root/administrator access on compromised Linux and Windows systems. Essential for penetration testing post-exploitation phase and red team operations. |
| [production-code-audit](.archived/skills/security-penetration-testing/production-code-audit/SKILL.md) | Autonomously deep-scan entire codebase line-by-line, understand architecture and patterns, then systematically transform it to production-grade, corporate-level professional quality with optimizations |
| [project-skill-audit](.archived/skills/security-penetration-testing/project-skill-audit/SKILL.md) | Audit a project and recommend the highest-value skills to add or update. |
| [protocol-reverse-engineering](.archived/skills/security-penetration-testing/protocol-reverse-engineering/SKILL.md) | Comprehensive techniques for capturing, analyzing, and documenting network protocols for security research, interoperability, and debugging. |
| [red-team-tools](.archived/skills/security-penetration-testing/red-team-tools/SKILL.md) | Implement proven methodologies and tool workflows from top security researchers for effective reconnaissance, vulnerability discovery, and bug bounty hunting. Automate common tasks while maintaining thorough coverage of attack surfaces. |
| [returns-reverse-logistics](.archived/skills/security-penetration-testing/returns-reverse-logistics/SKILL.md) | Codified expertise for returns authorisation, receipt and inspection, disposition decisions, refund processing, fraud detection, and warranty claims management. |
| [reverse-engineer](.archived/skills/security-penetration-testing/reverse-engineer/SKILL.md) | Binary analysis with IDA Pro, Ghidra |
| [sast-configuration](.archived/skills/security-penetration-testing/sast-configuration/SKILL.md) | Static Application Security Testing (SAST) tool setup, configuration, and custom rule creation for comprehensive security scanning across multiple programming languages. |
| [scanning-tools](.archived/skills/security-penetration-testing/scanning-tools/SKILL.md) | Master essential security scanning tools for network discovery, vulnerability assessment, web application testing, wireless security, and compliance validation. This skill covers tool selection, configuration, and practical usage across different scanning categories. |
| [security-auditor](.archived/skills/security-penetration-testing/security-auditor/SKILL.md) | DevSecOps, cybersecurity, compliance |
| [security-scanning-security-dependencies](.archived/skills/security-penetration-testing/security-scanning-security-dependencies/SKILL.md) | You are a security expert specializing in dependency vulnerability analysis, SBOM generation, and supply chain security. Scan project dependencies across multiple ecosystems to identify vulnerabilities, assess risks, and provide automated remediation strategies. |
| [security-scanning-security-hardening](.archived/skills/security-penetration-testing/security-scanning-security-hardening/SKILL.md) | Coordinate multi-layer security scanning and hardening across application, infrastructure, and compliance controls. |
| [security-scanning-security-sast](.archived/skills/security-penetration-testing/security-scanning-security-sast/SKILL.md) | Static Application Security Testing (SAST) for code vulnerability |
| [seo-programmatic](.archived/skills/security-penetration-testing/seo-programmatic/SKILL.md) | Plan and audit programmatic SEO pages generated at scale from structured data. Use when designing templates, URL systems, internal linking, quality gates, and index-bloat safeguards for pages at scale. |
| [site-architecture](.archived/skills/security-penetration-testing/site-architecture/SKILL.md) | Plan or restructure website hierarchy, navigation, URL patterns, breadcrumbs, and internal linking. Use when mapping pages, sections, and site structure, but not for XML sitemap auditing or schema markup. |
| [skill-scanner](.archived/skills/security-penetration-testing/skill-scanner/SKILL.md) | Scan agent skills for security issues before adoption. Detects prompt injection, malicious code, excessive permissions, secret exposure, and supply chain risks. |
| [smtp-penetration-testing](.archived/skills/security-penetration-testing/smtp-penetration-testing/SKILL.md) | Conduct comprehensive security assessments of SMTP (Simple Mail Transfer Protocol) servers to identify vulnerabilities including open relays, user enumeration, weak authentication, and misconfiguration. |
| [spec-to-code-compliance](.archived/skills/security-penetration-testing/spec-to-code-compliance/SKILL.md) | Verifies code implements exactly what documentation specifies for blockchain audits. Use when comparing code against whitepapers, finding gaps between specs and implementation, or performing compliance checks for protocol implementations. |
| [sql-injection-testing](.archived/skills/security-penetration-testing/sql-injection-testing/SKILL.md) | SQL injection vulnerability assessment |
| [ssh-penetration-testing](.archived/skills/security-penetration-testing/ssh-penetration-testing/SKILL.md) | Conduct comprehensive SSH security assessments including enumeration, credential attacks, vulnerability exploitation, tunneling techniques, and post-exploitation activities. This skill covers the complete methodology for testing SSH service security. |
| [stride-analysis-patterns](.archived/skills/security-penetration-testing/stride-analysis-patterns/SKILL.md) | Apply STRIDE methodology to systematically identify threats. Use when analyzing system security, conducting threat modeling sessions, or creating security documentation. |
| [supply-chain-risk-auditor](.archived/skills/security-penetration-testing/supply-chain-risk-auditor/SKILL.md) | Identifies dependencies at heightened risk of exploitation or takeover. Use when assessing supply chain attack surface, evaluating dependency health, or scoping security engagements. |
| [threat-mitigation-mapping](.archived/skills/security-penetration-testing/threat-mitigation-mapping/SKILL.md) | Map identified threats to appropriate security controls and mitigations. Use when prioritizing security investments, creating remediation plans, or validating control effectiveness. |
| [threat-modeling-expert](.archived/skills/security-penetration-testing/threat-modeling-expert/SKILL.md) | STRIDE, PASTA, attack trees |
| [vulnerability-scanner](.archived/skills/security-penetration-testing/vulnerability-scanner/SKILL.md) | OWASP 2025, supply chain, risk mapping |
| [windows-privilege-escalation](.archived/skills/security-penetration-testing/windows-privilege-escalation/SKILL.md) | Provide systematic methodologies for discovering and exploiting privilege escalation vulnerabilities on Windows systems during penetration testing engagements. |
| [wireshark-analysis](.archived/skills/security-penetration-testing/wireshark-analysis/SKILL.md) | Execute comprehensive network traffic analysis using Wireshark to capture, filter, and examine network packets for security investigations, performance optimization, and troubleshooting. |
| [xss-html-injection](.archived/skills/security-penetration-testing/xss-html-injection/SKILL.md) | Client-side injection testing |
| [zeroize-audit](.archived/skills/security-penetration-testing/zeroize-audit/SKILL.md) | Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with assembly-level analysis, and control-flow verification. Use for auditing C/C++/Rust code handling secrets, keys, passwords, or other sensitive data. |

</details>

### ☁️ Cloud, DevOps & Infrastructure

<details>
<summary><b>☁️ Cloud, DevOps & Infrastructure (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [amazon-alexa](.archived/skills/cloud-devops-infrastructure/amazon-alexa/SKILL.md) | Integracao completa com Amazon Alexa para criar skills de voz inteligentes, transformar Alexa em assistente com Claude como cerebro (projeto Auri) e integrar com AWS ecosystem (Lambda, DynamoDB, Polly, Transcribe, Lex, Smart Home). |
| [apify-actorization](.archived/skills/cloud-devops-infrastructure/apify-actorization/SKILL.md) | Actorization converts existing software into reusable serverless applications compatible with the Apify platform. Actors are programs packaged as Docker images that accept well-defined JSON input, perform an action, and optionally produce structured JSON output. |
| [auri-core](.archived/skills/cloud-devops-infrastructure/auri-core/SKILL.md) | Auri: assistente de voz inteligente (Alexa + Claude claude-opus-4-20250805). Visao do produto, persona Vitoria Neural, stack AWS, modelo Free/Pro/Business/Enterprise, roadmap 4 fases, GTM, north star WAC e analise competitiva. |
| [aws-cost-cleanup](.archived/skills/cloud-devops-infrastructure/aws-cost-cleanup/SKILL.md) | Automated cleanup of unused AWS resources to reduce costs |
| [aws-cost-optimizer](.archived/skills/cloud-devops-infrastructure/aws-cost-optimizer/SKILL.md) | Comprehensive AWS cost analysis and optimization recommendations using AWS CLI and Cost Explorer |
| [aws-penetration-testing](.archived/skills/cloud-devops-infrastructure/aws-penetration-testing/SKILL.md) | Provide comprehensive techniques for penetration testing AWS cloud environments. Covers IAM enumeration, privilege escalation, SSRF to metadata endpoint, S3 bucket exploitation, Lambda code extraction, and persistence techniques for red team operations. |
| [aws-serverless](.archived/skills/cloud-devops-infrastructure/aws-serverless/SKILL.md) | Lambda functions with error handling |
| [aws-skills](.archived/skills/cloud-devops-infrastructure/aws-skills/SKILL.md) | AWS dev with infrastructure automation |
| [cdk-patterns](.archived/skills/cloud-devops-infrastructure/cdk-patterns/SKILL.md) | Common AWS CDK patterns and constructs for building cloud infrastructure with TypeScript, Python, or Java. Use when designing reusable CDK stacks and L3 constructs. |
| [cloud-architect](.archived/skills/cloud-devops-infrastructure/cloud-architect/SKILL.md) | Multi-cloud, IaC, FinOps |
| [cloud-devops](.archived/skills/cloud-devops-infrastructure/cloud-devops/SKILL.md) | AWS/Azure/GCP, K8s, Terraform, CI/CD |
| [cloudformation-best-practices](.archived/skills/cloud-devops-infrastructure/cloudformation-best-practices/SKILL.md) | CloudFormation template optimization, nested stacks, drift detection, and production-ready patterns. Use when writing or reviewing CF templates. |
| [deployment-engineer](.archived/skills/cloud-devops-infrastructure/deployment-engineer/SKILL.md) | CI/CD pipelines, GitOps, automation |
| [devops-deploy](.archived/skills/cloud-devops-infrastructure/devops-deploy/SKILL.md) | DevOps e deploy de aplicacoes — Docker, CI/CD com GitHub Actions, AWS Lambda, SAM, Terraform, infraestrutura como codigo e monitoramento. |
| [docker-expert](.archived/skills/cloud-devops-infrastructure/docker-expert/SKILL.md) | Container optimization, security, orchestration |
| [gcp-cloud-run](.archived/skills/cloud-devops-infrastructure/gcp-cloud-run/SKILL.md) | When to use: ['Web applications and APIs', 'Need any runtime or library', 'Complex services with multiple endpoints', 'Stateless containerized workloads'] |
| [github-actions-templates](.archived/skills/cloud-devops-infrastructure/github-actions-templates/SKILL.md) | Production GitHub Actions workflows |
| [gitops-workflow](.archived/skills/cloud-devops-infrastructure/gitops-workflow/SKILL.md) | ArgoCD and Flux for K8s |
| [grafana-dashboards](.archived/skills/cloud-devops-infrastructure/grafana-dashboards/SKILL.md) | Production Grafana dashboards |
| [helm-chart-scaffolding](.archived/skills/cloud-devops-infrastructure/helm-chart-scaffolding/SKILL.md) | Comprehensive guidance for creating, organizing, and managing Helm charts for packaging and deploying Kubernetes applications. |
| [hugging-face-jobs](.archived/skills/cloud-devops-infrastructure/hugging-face-jobs/SKILL.md) | Run any workload on fully managed Hugging Face infrastructure. No local setup required—jobs run on cloud CPUs, GPUs, or TPUs and can persist results to the Hugging Face Hub. |
| [hugging-face-model-trainer](.archived/skills/cloud-devops-infrastructure/hugging-face-model-trainer/SKILL.md) | Train language models using TRL (Transformer Reinforcement Learning) on fully managed Hugging Face infrastructure. No local GPU setup required—models train on cloud GPUs and results are automatically saved to the Hugging Face Hub. |
| [hybrid-cloud-networking](.archived/skills/cloud-devops-infrastructure/hybrid-cloud-networking/SKILL.md) | Configure secure, high-performance connectivity between on-premises and cloud environments using VPN, Direct Connect, and ExpressRoute. |
| [ilya-sutskever](.archived/skills/cloud-devops-infrastructure/ilya-sutskever/SKILL.md) | Agente que simula Ilya Sutskever — co-fundador da OpenAI, ex-Chief Scientist, fundador da SSI. Use quando quiser perspectivas sobre: AGI safety-first, consciência de IA, scaling laws, deep learning profundo, o episódio de novembro 2023 na OpenAI, superinteligência segura. |
| [incident-responder](.archived/skills/cloud-devops-infrastructure/incident-responder/SKILL.md) | Rapid problem resolution, observability |
| [k8s-manifest-generator](.archived/skills/cloud-devops-infrastructure/k8s-manifest-generator/SKILL.md) | Step-by-step guidance for creating production-ready Kubernetes manifests including Deployments, Services, ConfigMaps, Secrets, and PersistentVolumeClaims. |
| [k8s-security-policies](.archived/skills/cloud-devops-infrastructure/k8s-security-policies/SKILL.md) | Comprehensive guide for implementing NetworkPolicy, PodSecurityPolicy, RBAC, and Pod Security Standards in Kubernetes. |
| [kubernetes-architect](.archived/skills/cloud-devops-infrastructure/kubernetes-architect/SKILL.md) | Cloud-native K8s, ArgoCD/Flux |
| [kubernetes-deployment](.archived/skills/cloud-devops-infrastructure/kubernetes-deployment/SKILL.md) | Helm charts, service mesh, production K8s |
| [linkerd-patterns](.archived/skills/cloud-devops-infrastructure/linkerd-patterns/SKILL.md) | Production patterns for Linkerd service mesh - the lightweight, security-first service mesh for Kubernetes. |
| [loki-mode](.archived/skills/cloud-devops-infrastructure/loki-mode/SKILL.md) | Version 2.35.0 | PRD to Production | Zero Human Intervention > Research-enhanced: OpenAI SDK, DeepMind, Anthropic, AWS Bedrock, Agent SDK, HN Production (2025) |
| [network-engineer](.archived/skills/cloud-devops-infrastructure/network-engineer/SKILL.md) | Expert network engineer specializing in modern cloud networking, security architectures, and performance optimization. |
| [observability-engineer](.archived/skills/cloud-devops-infrastructure/observability-engineer/SKILL.md) | Monitoring, logging, tracing, SLI/SLO |
| [odoo-backup-strategy](.archived/skills/cloud-devops-infrastructure/odoo-backup-strategy/SKILL.md) | Complete Odoo backup and restore strategy: database dumps, filestore backup, automated scheduling, cloud storage upload, and tested restore procedures. |
| [odoo-docker-deployment](.archived/skills/cloud-devops-infrastructure/odoo-docker-deployment/SKILL.md) | Production-ready Docker and docker-compose setup for Odoo with PostgreSQL, persistent volumes, environment-based configuration, and Nginx reverse proxy. |
| [secrets-management](.archived/skills/cloud-devops-infrastructure/secrets-management/SKILL.md) | Secure secrets management practices for CI/CD pipelines using Vault, AWS Secrets Manager, and other tools. |
| [service-mesh-expert](.archived/skills/cloud-devops-infrastructure/service-mesh-expert/SKILL.md) | Expert service mesh architect specializing in Istio, Linkerd, and cloud-native networking patterns. Masters traffic management, security policies, observability integration, and multi-cluster mesh con |
| [terraform-aws-modules](.archived/skills/cloud-devops-infrastructure/terraform-aws-modules/SKILL.md) | Terraform module creation for AWS — reusable modules, state management, and HCL best practices. Use when building or reviewing Terraform AWS infrastructure. |
| [terraform-infrastructure](.archived/skills/cloud-devops-infrastructure/terraform-infrastructure/SKILL.md) | Terraform for cloud resources |
| [terraform-specialist](.archived/skills/cloud-devops-infrastructure/terraform-specialist/SKILL.md) | Advanced IaC, state management |
| [vibe-code-auditor](.archived/skills/cloud-devops-infrastructure/vibe-code-auditor/SKILL.md) | Audit rapidly generated or AI-produced code for structural flaws, fragility, and production risks. |
| [web-security-testing](.archived/skills/cloud-devops-infrastructure/web-security-testing/SKILL.md) | Web application security testing workflow for OWASP Top 10 vulnerabilities including injection, XSS, authentication flaws, and access control issues. |
| [whatsapp-cloud-api](.archived/skills/cloud-devops-infrastructure/whatsapp-cloud-api/SKILL.md) | Integracao com WhatsApp Business Cloud API (Meta). Mensagens, templates, webhooks HMAC-SHA256, automacao de atendimento. Boilerplates Node.js e Python. |
| [x-twitter-scraper](.archived/skills/cloud-devops-infrastructure/x-twitter-scraper/SKILL.md) | X (Twitter) data platform skill — tweet search, user lookup, follower extraction, engagement metrics, giveaway draws, monitoring, webhooks, 19 extraction tools, MCP server. |

</details>

### 🧪 Testing & Quality

<details>
<summary><b>🧪 Testing & Quality (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [active-directory-attacks](.archived/skills/testing-quality/active-directory-attacks/SKILL.md) | Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement, privilege escalation, and domain dominance for red team operations and penetration testing. |
| [ad-creative](.archived/skills/testing-quality/ad-creative/SKILL.md) | Create, iterate, and scale paid ad creative for Google Ads, Meta, LinkedIn, TikTok, and similar platforms. Use when generating headlines, descriptions, primary text, or large sets of ad variations for testing and performance optimization. |
| [ai-md](.archived/skills/testing-quality/ai-md/SKILL.md) | Convert human-written CLAUDE.md into AI-native structured-label format. Battle-tested across 4 models. Same rules, fewer tokens, higher compliance. |
| [bash-scripting](.archived/skills/testing-quality/bash-scripting/SKILL.md) | Bash scripting workflow for creating production-ready shell scripts with defensive patterns, error handling, and testing. |
| [behavioral-modes](.archived/skills/testing-quality/behavioral-modes/SKILL.md) | AI operational modes (brainstorm, implement, debug, review, teach, ship, orchestrate). Use to adapt behavior based on task type. |
| [bug-hunter](.archived/skills/testing-quality/bug-hunter/SKILL.md) | Systematic debugging: symptoms → root cause |
| [circleci-automation](.archived/skills/testing-quality/circleci-automation/SKILL.md) | Automate CircleCI tasks via Rube MCP (Composio): trigger pipelines, monitor workflows/jobs, retrieve artifacts and test metadata. Always search tools first for current schemas. |
| [debug-buttercup](.archived/skills/testing-quality/debug-buttercup/SKILL.md) | All pods run in namespace crs. Use when pods in the crs namespace are in CrashLoopBackOff, OOMKilled, or restarting, multiple services restart simultaneously (cascade failure), or redis is unresponsive or showing AOF warnings. |
| [debugger](.archived/skills/testing-quality/debugger/SKILL.md) | Errors, test failures, unexpected behavior |
| [debugging-strategies](.archived/skills/testing-quality/debugging-strategies/SKILL.md) | Transform debugging from frustrating guesswork into systematic problem-solving with proven strategies, powerful tools, and methodical approaches. |
| [debugging-toolkit-smart-debug](.archived/skills/testing-quality/debugging-toolkit-smart-debug/SKILL.md) | Use when working with debugging toolkit smart debug |
| [dependency-upgrade](.archived/skills/testing-quality/dependency-upgrade/SKILL.md) | Master major dependency version upgrades, compatibility analysis, staged upgrade strategies, and comprehensive testing approaches. |
| [deployment-validation-config-validate](.archived/skills/testing-quality/deployment-validation-config-validate/SKILL.md) | You are a configuration management expert specializing in validating, testing, and ensuring the correctness of application configurations. Create comprehensive validation schemas, implement configurat |
| [distributed-debugging-debug-trace](.archived/skills/testing-quality/distributed-debugging-debug-trace/SKILL.md) | You are a debugging expert specializing in setting up comprehensive debugging environments, distributed tracing, and diagnostic tools. Configure debugging workflows, implement tracing solutions, and establish troubleshooting practices for development and production environments. |
| [dwarf-expert](.archived/skills/testing-quality/dwarf-expert/SKILL.md) | Provides expertise for analyzing DWARF debug files and understanding the DWARF debug format/standard (v3-v5). Triggers when understanding DWARF information, interacting with DWARF files, answering DWARF-related questions, or working with code that parses DWARF data. |
| [e2e-testing](.archived/skills/testing-quality/e2e-testing/SKILL.md) | Playwright E2E testing workflow |
| [e2e-testing-patterns](.archived/skills/testing-quality/e2e-testing-patterns/SKILL.md) | Reliable, fast E2E test suites |
| [email-systems](.archived/skills/testing-quality/email-systems/SKILL.md) | You are an email systems engineer who has maintained 99.9% deliverability across millions of emails. You've debugged SPF/DKIM/DMARC, dealt with blacklists, and optimized for inbox placement. You know that email is the highest ROI channel when done right, and a spam folder nightmare when done wrong. |
| [error-debugging-error-analysis](.archived/skills/testing-quality/error-debugging-error-analysis/SKILL.md) | You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing comprehensive observability solutions. |
| [error-debugging-multi-agent-review](.archived/skills/testing-quality/error-debugging-multi-agent-review/SKILL.md) | Use when working with error debugging multi agent review |
| [error-diagnostics-error-analysis](.archived/skills/testing-quality/error-diagnostics-error-analysis/SKILL.md) | You are an expert error analysis specialist with deep expertise in debugging distributed systems, analyzing production incidents, and implementing comprehensive observability solutions. |
| [error-diagnostics-smart-debug](.archived/skills/testing-quality/error-diagnostics-smart-debug/SKILL.md) | Use when working with error diagnostics smart debug |
| [framework-migration-deps-upgrade](.archived/skills/testing-quality/framework-migration-deps-upgrade/SKILL.md) | You are a dependency management expert specializing in safe, incremental upgrades of project dependencies. Plan and execute dependency updates with minimal risk, proper testing, and clear migration pa |
| [git-pr-workflows-git-workflow](.archived/skills/testing-quality/git-pr-workflows-git-workflow/SKILL.md) | Orchestrate a comprehensive git workflow from code review through PR creation, leveraging specialized agents for quality assurance, testing, and deployment readiness. This workflow implements modern g |
| [go-playwright](.archived/skills/testing-quality/go-playwright/SKILL.md) | Expert capability for robust, stealthy, and efficient browser automation using Playwright Go. |
| [incident-response-smart-fix](.archived/skills/testing-quality/incident-response-smart-fix/SKILL.md) | [Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observability platforms to systematically diagnose and res |
| [infinite-gratitude](.archived/skills/testing-quality/infinite-gratitude/SKILL.md) | Multi-agent research skill for parallel research execution (10 agents, battle-tested with real case studies). |
| [javascript-testing-patterns](.archived/skills/testing-quality/javascript-testing-patterns/SKILL.md) | JS/TS testing with modern frameworks |
| [k6-load-testing](.archived/skills/testing-quality/k6-load-testing/SKILL.md) | k6 load testing for APIs and browsers |
| [makepad-reference](.archived/skills/testing-quality/makepad-reference/SKILL.md) | This category provides reference materials for debugging, code quality, and advanced layout patterns. |
| [obsidian-cli](.archived/skills/testing-quality/obsidian-cli/SKILL.md) | Use the Obsidian CLI to read, create, search, and manage vault content, or to develop and debug Obsidian plugins and themes from the command line. |
| [odoo-automated-tests](.archived/skills/testing-quality/odoo-automated-tests/SKILL.md) | Write and run Odoo automated tests using TransactionCase, HttpCase, and browser tour tests. Covers test data setup, mocking, and CI integration. |
| [os-scripting](.archived/skills/testing-quality/os-scripting/SKILL.md) | Operating system and shell scripting troubleshooting workflow for Linux, macOS, and Windows. Covers bash scripting, system administration, debugging, and automation. |
| [performance-testing-review-ai-review](.archived/skills/testing-quality/performance-testing-review-ai-review/SKILL.md) | You are an expert AI-powered code review specialist combining automated static analysis, intelligent pattern recognition, and modern DevOps practices. Leverage AI tools (GitHub Copilot, Qodo, GPT-5, C |
| [performance-testing-review-multi-agent-review](.archived/skills/testing-quality/performance-testing-review-multi-agent-review/SKILL.md) | Use when working with performance testing review multi agent review |
| [playwright-java](.archived/skills/testing-quality/playwright-java/SKILL.md) | Scaffold, write, debug, and enhance enterprise-grade Playwright E2E tests in Java using Page Object Model, JUnit 5, Allure reporting, and parallel execution. |
| [playwright-skill](.archived/skills/testing-quality/playwright-skill/SKILL.md) | Playwright automation skill |
| [prompt-library](.archived/skills/testing-quality/prompt-library/SKILL.md) | A comprehensive collection of battle-tested prompts inspired by [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) and community best practices. |
| [pypict-skill](.archived/skills/testing-quality/pypict-skill/SKILL.md) | Pairwise test generation |
| [python-performance-optimization](.archived/skills/testing-quality/python-performance-optimization/SKILL.md) | Profile and optimize Python code using cProfile, memory profilers, and performance best practices. Use when debugging slow Python code, optimizing bottlenecks, or improving application performance. |
| [python-testing-patterns](.archived/skills/testing-quality/python-testing-patterns/SKILL.md) | pytest, fixtures, mocking, TDD |
| [screenshots](.archived/skills/testing-quality/screenshots/SKILL.md) | Generate marketing screenshots of your app using Playwright. Use when the user wants to create screenshots for Product Hunt, social media, landing pages, or documentation. |
| [semgrep-rule-variant-creator](.archived/skills/testing-quality/semgrep-rule-variant-creator/SKILL.md) | Creates language variants of existing Semgrep rules. Use when porting a Semgrep rule to specified target languages. Takes an existing rule and target languages as input, produces independent rule+test directories for each language. |
| [shodan-reconnaissance](.archived/skills/testing-quality/shodan-reconnaissance/SKILL.md) | Provide systematic methodologies for leveraging Shodan as a reconnaissance tool during penetration testing engagements. |
| [systematic-debugging](.archived/skills/testing-quality/systematic-debugging/SKILL.md) | Debug any bug before proposing fixes |
| [systems-programming-rust-project](.archived/skills/testing-quality/systems-programming-rust-project/SKILL.md) | You are a Rust project architecture expert specializing in scaffolding production-ready Rust applications. Generate complete project structures with cargo tooling, proper module organization, testing |
| [tdd-orchestrator](.archived/skills/testing-quality/tdd-orchestrator/SKILL.md) | Red-green-refactor TDD discipline |
| [tdd-workflow](.archived/skills/testing-quality/tdd-workflow/SKILL.md) | Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle. |
| [tdd-workflows-tdd-green](.archived/skills/testing-quality/tdd-workflows-tdd-green/SKILL.md) | Implement the minimal code needed to make failing tests pass in the TDD green phase. |
| [tdd-workflows-tdd-red](.archived/skills/testing-quality/tdd-workflows-tdd-red/SKILL.md) | Generate failing tests for the TDD red phase to define expected behavior and edge cases. |
| [test-automator](.archived/skills/testing-quality/test-automator/SKILL.md) | AI-powered test automation |
| [test-driven-development](.archived/skills/testing-quality/test-driven-development/SKILL.md) | Use when implementing any feature or bugfix, before writing implementation code |
| [testing-patterns](.archived/skills/testing-quality/testing-patterns/SKILL.md) | Jest patterns, factories, mocking, TDD |
| [testing-qa](.archived/skills/testing-quality/testing-qa/SKILL.md) | Comprehensive testing and QA workflow covering unit testing, integration testing, E2E testing, browser automation, and quality assurance. |
| [unit-testing-test-generate](.archived/skills/testing-quality/unit-testing-test-generate/SKILL.md) | Generate comprehensive, maintainable unit tests across languages with strong coverage and edge case focus. |
| [webapp-testing](.archived/skills/testing-quality/webapp-testing/SKILL.md) | To test local web applications, write native Python Playwright scripts. |
| [wiki-qa](.archived/skills/testing-quality/wiki-qa/SKILL.md) | Answer repository questions grounded entirely in source code evidence. Use when user asks a question about the codebase, user wants to understand a specific file, function, or component, or user asks \"how does X work\" or \"where is Y defined\". |
| [wordpress-penetration-testing](.archived/skills/testing-quality/wordpress-penetration-testing/SKILL.md) | Assess WordPress installations for common vulnerabilities and WordPress 7.0 attack surfaces. |
| [yes-md](.archived/skills/testing-quality/yes-md/SKILL.md) | 6-layer AI governance: safety gates, evidence-based debugging, anti-slack detection, and machine-enforced hooks. Makes AI safe, thorough, and honest. |

</details>

### 🔧 Programming Languages

<details>
<summary><b>🔧 Programming Languages (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [animejs-animation](.archived/skills/programming-languages/animejs-animation/SKILL.md) | Advanced JavaScript animation library skill for creating complex, high-performance web animations. |
| [bun-development](.archived/skills/programming-languages/bun-development/SKILL.md) | Fast, modern JavaScript/TypeScript development with the Bun runtime, inspired by [oven-sh/bun](https://github.com/oven-sh/bun). |
| [c-pro](.archived/skills/programming-languages/c-pro/SKILL.md) | C with proper memory management |
| [cpp-pro](.archived/skills/programming-languages/cpp-pro/SKILL.md) | Modern C++, RAII, smart pointers, STL |
| [csharp-pro](.archived/skills/programming-languages/csharp-pro/SKILL.md) | Modern C# with records, pattern matching |
| [elixir-pro](.archived/skills/programming-languages/elixir-pro/SKILL.md) | Elixir OTP, supervision trees, Phoenix |
| [golang-pro](.archived/skills/programming-languages/golang-pro/SKILL.md) | Go 1.21+ with modern concurrency |
| [haskell-pro](.archived/skills/programming-languages/haskell-pro/SKILL.md) | Advanced Haskell type systems |
| [java-pro](.archived/skills/programming-languages/java-pro/SKILL.md) | Java 21+, virtual threads, Spring Boot 3 |
| [julia-pro](.archived/skills/programming-languages/julia-pro/SKILL.md) | Julia 1.10+ with multiple dispatch |
| [kotlin-coroutines-expert](.archived/skills/programming-languages/kotlin-coroutines-expert/SKILL.md) | Kotlin Coroutines and Flow |
| [mtls-configuration](.archived/skills/programming-languages/mtls-configuration/SKILL.md) | Configure mutual TLS (mTLS) for zero-trust service-to-service communication. Use when implementing zero-trust networking, certificate management, or securing internal service communication. |
| [php-pro](.archived/skills/programming-languages/php-pro/SKILL.md) | Modern PHP with generators, iterators |
| [popup-cro](.archived/skills/programming-languages/popup-cro/SKILL.md) | Create and optimize popups, modals, overlays, slide-ins, and banners to increase conversions without harming user experience or brand trust. |
| [python-patterns](.archived/skills/programming-languages/python-patterns/SKILL.md) | Python development principles and decision-making. Framework selection, async patterns, type hints, project structure. Teaches thinking, not copying. |
| [python-pro](.archived/skills/programming-languages/python-pro/SKILL.md) | Python 3.12+, uv, ruff, pydantic, FastAPI |
| [ruby-pro](.archived/skills/programming-languages/ruby-pro/SKILL.md) | Ruby metaprogramming, Rails, gems |
| [rust-pro](.archived/skills/programming-languages/rust-pro/SKILL.md) | Rust 1.75+, async, advanced type system |
| [scala-pro](.archived/skills/programming-languages/scala-pro/SKILL.md) | Scala FP, Pekko, Spark, ZIO |
| [seaborn](.archived/skills/programming-languages/seaborn/SKILL.md) | Seaborn is a Python visualization library for creating publication-quality statistical graphics. Use this skill for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures with minimal code. |
| [sql-pro](.archived/skills/programming-languages/sql-pro/SKILL.md) | Cloud-native SQL, OLTP/OLAP |
| [statsmodels](.archived/skills/programming-languages/statsmodels/SKILL.md) | Statsmodels is Python's premier library for statistical modeling, providing tools for estimation, inference, and diagnostics across a wide range of statistical methods. |

</details>

### 🎨 Design, UI/UX & Creative

<details>
<summary><b>🎨 Design, UI/UX & Creative (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [3d-web-experience](.archived/skills/design-ui-ux-creative/3d-web-experience/SKILL.md) | 3D on the web: impact vs. performance |
| [agent-manager-skill](.archived/skills/design-ui-ux-creative/agent-manager-skill/SKILL.md) | Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling. |
| [antigravity-design-expert](.archived/skills/design-ui-ux-creative/antigravity-design-expert/SKILL.md) | Glassmorphism, GSAP, 3D CSS interfaces |
| [bash-linux](.archived/skills/design-ui-ux-creative/bash-linux/SKILL.md) | Bash/Linux terminal patterns. Critical commands, piping, error handling, scripting. Use when working on macOS or Linux systems. |
| [brainstorming](.archived/skills/design-ui-ux-creative/brainstorming/SKILL.md) | Use before creative or constructive work (features, architecture, behavior). Transforms vague ideas into validated designs through disciplined reasoning and collaboration. |
| [canva-automation](.archived/skills/design-ui-ux-creative/canva-automation/SKILL.md) | Automate Canva tasks via Rube MCP (Composio): designs, exports, folders, brand templates, autofill. Always search tools first for current schemas. |
| [canvas-design](.archived/skills/design-ui-ux-creative/canvas-design/SKILL.md) | These are instructions for creating design philosophies - aesthetic movements that are then EXPRESSED VISUALLY. Output only .md files, .pdf files, and .png files. |
| [code-refactoring-refactor-clean](.archived/skills/design-ui-ux-creative/code-refactoring-refactor-clean/SKILL.md) | You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance. |
| [codebase-cleanup-refactor-clean](.archived/skills/design-ui-ux-creative/codebase-cleanup-refactor-clean/SKILL.md) | You are a code refactoring expert specializing in clean code principles, SOLID design patterns, and modern software engineering best practices. Analyze and refactor the provided code to improve its quality, maintainability, and performance. |
| [context-degradation](.archived/skills/design-ui-ux-creative/context-degradation/SKILL.md) | Language models exhibit predictable degradation patterns as context length increases. Understanding these patterns is essential for diagnosing failures and designing resilient systems. |
| [deployment-pipeline-design](.archived/skills/design-ui-ux-creative/deployment-pipeline-design/SKILL.md) | Architecture patterns for multi-stage CI/CD pipelines with approval gates and deployment strategies. |
| [design-md](.archived/skills/design-ui-ux-creative/design-md/SKILL.md) | Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files |
| [design-orchestration](.archived/skills/design-ui-ux-creative/design-orchestration/SKILL.md) | Orchestrates design workflows by routing work through brainstorming, multi-agent review, and execution readiness in the correct order. |
| [design-spells](.archived/skills/design-ui-ux-creative/design-spells/SKILL.md) | Micro-interactions and design "magic" |
| [domain-driven-design](.archived/skills/design-ui-ux-creative/domain-driven-design/SKILL.md) | Plan and route Domain-Driven Design work from strategic modeling to tactical implementation and evented architecture patterns. |
| [figma-automation](.archived/skills/design-ui-ux-creative/figma-automation/SKILL.md) | Automate Figma tasks via Rube MCP (Composio): files, components, design tokens, comments, exports. Always search tools first for current schemas. |
| [frontend-slides](.archived/skills/design-ui-ux-creative/frontend-slides/SKILL.md) | Animation-rich HTML presentations |
| [game-audio](.archived/skills/design-ui-ux-creative/game-audio/SKILL.md) | Game audio principles. Sound design, music integration, adaptive audio systems. |
| [game-design](.archived/skills/design-ui-ux-creative/game-design/SKILL.md) | Game design principles. GDD structure, balancing, player psychology, progression. |
| [hig-components-controls](.archived/skills/design-ui-ux-creative/hig-components-controls/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-components-menus](.archived/skills/design-ui-ux-creative/hig-components-menus/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-inputs](.archived/skills/design-ui-ux-creative/hig-inputs/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [hig-technologies](.archived/skills/design-ui-ux-creative/hig-technologies/SKILL.md) | Check for .claude/apple-design-context.md before asking questions. Use existing context and only ask for information not already covered. |
| [iconsax-library](.archived/skills/design-ui-ux-creative/iconsax-library/SKILL.md) | Icon library with AI-driven generation |
| [interactive-portfolio](.archived/skills/design-ui-ux-creative/interactive-portfolio/SKILL.md) | Portfolio sites that convert |
| [kpi-dashboard-design](.archived/skills/design-ui-ux-creative/kpi-dashboard-design/SKILL.md) | Comprehensive patterns for designing effective Key Performance Indicator (KPI) dashboards that drive business decisions. |
| [lead-magnets](.archived/skills/design-ui-ux-creative/lead-magnets/SKILL.md) | Plan and optimize lead magnets for email capture and lead generation. Use when designing gated content, checklists, templates, downloadable resources, or other offers that convert visitors into subscribers. |
| [linux-troubleshooting](.archived/skills/design-ui-ux-creative/linux-troubleshooting/SKILL.md) | Linux system troubleshooting workflow for diagnosing and resolving system issues, performance problems, and service failures. |
| [llm-application-dev-ai-assistant](.archived/skills/design-ui-ux-creative/llm-application-dev-ai-assistant/SKILL.md) | You are an AI assistant development expert specializing in creating intelligent conversational interfaces, chatbots, and AI-powered applications. Design comprehensive AI assistant solutions with natur |
| [machine-learning-ops-ml-pipeline](.archived/skills/design-ui-ux-creative/machine-learning-ops-ml-pipeline/SKILL.md) | Design and implement a complete ML pipeline for: $ARGUMENTS |
| [magic-ui-generator](.archived/skills/design-ui-ux-creative/magic-ui-generator/SKILL.md) | Multiple UI component variations |
| [multi-agent-brainstorming](.archived/skills/design-ui-ux-creative/multi-agent-brainstorming/SKILL.md) | Simulate a structured peer-review process using multiple specialized agents to validate designs, surface hidden assumptions, and identify failure modes before implementation. |
| [nerdzao-elite](.archived/skills/design-ui-ux-creative/nerdzao-elite/SKILL.md) | Senior Elite Software Engineer (15+) and Senior Product Designer. Full workflow with planning, architecture, TDD, clean code, and pixel-perfect UX validation. |
| [nerdzao-elite-gemini-high](.archived/skills/design-ui-ux-creative/nerdzao-elite-gemini-high/SKILL.md) | Modo Elite Coder + UX Pixel-Perfect otimizado especificamente para Gemini 3.1 Pro High. Workflow completo com foco em qualidade máxima e eficiência de tokens. |
| [observability-monitoring-slo-implement](.archived/skills/design-ui-ux-creative/observability-monitoring-slo-implement/SKILL.md) | You are an SLO (Service Level Objective) expert specializing in implementing reliability standards and error budget-based engineering practices. Design comprehensive SLO frameworks, establish meaningful SLIs, and create monitoring systems that balance reliability with feature velocity. |
| [pakistan-payments-stack](.archived/skills/design-ui-ux-creative/pakistan-payments-stack/SKILL.md) | Design and implement production-grade Pakistani payment integrations (JazzCash, Easypaisa, bank/PSP rails, optional Raast) for SaaS with PKR billing, webhook reliability, and reconciliation. |
| [product-design](.archived/skills/design-ui-ux-creative/product-design/SKILL.md) | Apple-level product design |
| [programmatic-seo](.archived/skills/design-ui-ux-creative/programmatic-seo/SKILL.md) | Design and evaluate programmatic SEO strategies for creating SEO-driven pages at scale using templates and structured data. |
| [referral-program](.archived/skills/design-ui-ux-creative/referral-program/SKILL.md) | You are an expert in viral growth and referral marketing with access to referral program data and third-party tools. Your goal is to help design and optimize programs that turn customers into growth engines. |
| [revops](.archived/skills/design-ui-ux-creative/revops/SKILL.md) | Design and improve revenue operations, lead lifecycle rules, scoring, routing, handoffs, and CRM process automation. Use when marketing, sales, and customer success workflows need clearer operational structure. |
| [schema-markup](.archived/skills/design-ui-ux-creative/schema-markup/SKILL.md) | Design, validate, and optimize schema.org structured data for eligibility, correctness, and measurable SEO impact. |
| [scroll-experience](.archived/skills/design-ui-ux-creative/scroll-experience/SKILL.md) | Scroll-driven narrative design |
| [social-orchestrator](.archived/skills/design-ui-ux-creative/social-orchestrator/SKILL.md) | Orquestrador unificado de canais sociais — coordena Instagram, Telegram e WhatsApp em um unico fluxo de trabalho. Publicacao cross-channel, metricas unificadas, reutilizacao de conteudo por formato, agendamento sincronizado e gestao centralizada de campanhas em todos os canais simultaneamente. |
| [steve-jobs](.archived/skills/design-ui-ux-creative/steve-jobs/SKILL.md) | Agente que simula Steve Jobs — cofundador da Apple, CEO da Pixar, fundador da NeXT, o maior designer de produtos tecnologicos da historia e o mais influente apresentador de produtos do mundo. |
| [stitch-ui-design](.archived/skills/design-ui-ux-creative/stitch-ui-design/SKILL.md) | AI-powered UI design with Google Stitch |
| [theme-factory](.archived/skills/design-ui-ux-creative/theme-factory/SKILL.md) | Professional font and color themes |
| [threejs-skills](.archived/skills/design-ui-ux-creative/threejs-skills/SKILL.md) | 3D scenes with Three.js |
| [ui-ux-designer](.archived/skills/design-ui-ux-creative/ui-ux-designer/SKILL.md) | Interface design, wireframes, design systems |
| [ui-ux-pro-max](.archived/skills/design-ui-ux-creative/ui-ux-pro-max/SKILL.md) | Comprehensive web/mobile design guide |
| [vizcom](.archived/skills/design-ui-ux-creative/vizcom/SKILL.md) | AI-powered product design tool for transforming sketches into full-fidelity 3D renders. |
| [wordpress-theme-development](.archived/skills/design-ui-ux-creative/wordpress-theme-development/SKILL.md) | WordPress theme development workflow covering theme architecture, template hierarchy, custom post types, block editor support, responsive design, and WordPress 7.0 features: DataViews, Pattern Editing, Navigation Overlays, and admin refresh. |

</details>

### 📚 Documentation & Writing

<details>
<summary><b>📚 Documentation & Writing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [agents-md](.archived/skills/documentation-writing/agents-md/SKILL.md) | This skill should be used when the user asks to "create AGENTS.md", "update AGENTS.md", "maintain agent docs", "set up CLAUDE.md", or needs to keep agent instructions concise. Enforces research-backed best practices for minimal, high-signal agent documentation. |
| [api-documentation](.archived/skills/documentation-writing/api-documentation/SKILL.md) | OpenAPI specs, developer guides |
| [api-documenter](.archived/skills/documentation-writing/api-documenter/SKILL.md) | OpenAPI 3.1, interactive docs, SDKs |
| [architecture-decision-records](.archived/skills/documentation-writing/architecture-decision-records/SKILL.md) | ADRs for technical decisions |
| [audio-transcriber](.archived/skills/documentation-writing/audio-transcriber/SKILL.md) | Transform audio recordings into professional Markdown documentation with intelligent summaries using LLM integration |
| [beautiful-prose](.archived/skills/documentation-writing/beautiful-prose/SKILL.md) | Forceful prose without AI tics |
| [blog-writing-guide](.archived/skills/documentation-writing/blog-writing-guide/SKILL.md) | Sentry blog writing standards |
| [coda-automation](.archived/skills/documentation-writing/coda-automation/SKILL.md) | Automate Coda tasks via Rube MCP (Composio): manage docs, pages, tables, rows, formulas, permissions, and publishing. Always search tools first for current schemas. |
| [cold-email](.archived/skills/documentation-writing/cold-email/SKILL.md) | Write B2B cold emails and follow-up sequences that earn replies. Use when creating outbound prospecting emails, SDR outreach, personalized opening lines, subject lines, CTAs, and multi-touch follow-up sequences. |
| [content-creator](.archived/skills/documentation-writing/content-creator/SKILL.md) | Brand voice analysis, SEO, content frameworks |
| [daily-news-report](.archived/skills/documentation-writing/daily-news-report/SKILL.md) | Scrapes content based on a preset URL list, filters high-quality technical information, and generates daily Markdown reports. |
| [defuddle](.archived/skills/documentation-writing/defuddle/SKILL.md) | Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page. |
| [docs-architect](.archived/skills/documentation-writing/docs-architect/SKILL.md) | Technical documentation from codebases |
| [documentation](.archived/skills/documentation-writing/documentation/SKILL.md) | API docs, architecture docs, README |
| [googlesheets-automation](.archived/skills/documentation-writing/googlesheets-automation/SKILL.md) | Automate Google Sheets operations (read, write, format, filter, manage spreadsheets) via Rube MCP (Composio). Read/write data, manage tabs, apply formatting, and search rows programmatically. |
| [internal-comms](.archived/skills/documentation-writing/internal-comms/SKILL.md) | Write internal communications such as status reports, leadership updates, 3P updates, newsletters, FAQs, incident reports, and project updates using repeatable internal formats. |
| [internal-comms-anthropic](.archived/skills/documentation-writing/internal-comms-anthropic/SKILL.md) | To write internal communications, use this skill for: |
| [internal-comms-community](.archived/skills/documentation-writing/internal-comms-community/SKILL.md) | To write internal communications, use this skill for: |
| [last30days](.archived/skills/documentation-writing/last30days/SKILL.md) | Research a topic from the last 30 days on Reddit + X + Web, become an expert, and write copy-paste-ready prompts for the user's target tool. |
| [meta-skills-guide](.archived/skills/documentation-writing/meta-skills-guide/SKILL.md) | Meta Skills Guide |
| [obsidian-markdown](.archived/skills/documentation-writing/obsidian-markdown/SKILL.md) | Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes. |
| [odoo-orm-expert](.archived/skills/documentation-writing/odoo-orm-expert/SKILL.md) | Master Odoo ORM patterns: search, browse, create, write, domain filters, computed fields, and performance-safe query techniques. |
| [planning-with-files](.archived/skills/documentation-writing/planning-with-files/SKILL.md) | Work like Manus: Use persistent markdown files as your \"working memory on disk.\ |
| [pr-writer](.archived/skills/documentation-writing/pr-writer/SKILL.md) | Create pull requests following Sentry's engineering practices. |
| [readme](.archived/skills/documentation-writing/readme/SKILL.md) | Absurdly thorough README files |
| [sales-enablement](.archived/skills/documentation-writing/sales-enablement/SKILL.md) | Create sales collateral such as decks, one-pagers, objection docs, demo scripts, playbooks, and proposal templates. Use when a sales team needs assets that help reps move deals forward and close. |
| [scientific-writing](.archived/skills/documentation-writing/scientific-writing/SKILL.md) | Deep research with verified citations |
| [seo-content-writer](.archived/skills/documentation-writing/seo-content-writer/SKILL.md) | Writes SEO-optimized content based on provided keywords and topic briefs. Creates engaging, comprehensive content following best practices. Use PROACTIVELY for content creation tasks. |
| [skill-writer](.archived/skills/documentation-writing/skill-writer/SKILL.md) | Create and improve agent skills following the Agent Skills specification. Use when asked to create, write, or update skills. |
| [wiki-architect](.archived/skills/documentation-writing/wiki-architect/SKILL.md) | Wiki catalogues from codebases |
| [wiki-changelog](.archived/skills/documentation-writing/wiki-changelog/SKILL.md) | Generate structured changelogs from git history. Use when user asks \"what changed recently\", \"generate a changelog\", \"summarize commits\" or user wants to understand recent development activity. |
| [wiki-page-writer](.archived/skills/documentation-writing/wiki-page-writer/SKILL.md) | You are a senior documentation engineer that generates comprehensive technical documentation pages with evidence-based depth. |
| [wiki-researcher](.archived/skills/documentation-writing/wiki-researcher/SKILL.md) | You are an expert software engineer and systems analyst. Use when user asks \"how does X work\" with expectation of depth, user wants to understand a complex system spanning many files, or user asks for architectural analysis or pattern investigation. |

</details>

### 🔀 Git & Version Control

<details>
<summary><b>🔀 Git & Version Control (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [2d-games](.archived/skills/git-version-control/2d-games/SKILL.md) | 2D game development principles. Sprites, tilemaps, physics, camera. |
| [3d-games](.archived/skills/git-version-control/3d-games/SKILL.md) | 3D game development principles. Rendering, shaders, physics, cameras. |
| [address-github-comments](.archived/skills/git-version-control/address-github-comments/SKILL.md) | Use when you need to address review or issue comments on an open GitHub Pull Request using the gh CLI. |
| [advogado-criminal](.archived/skills/git-version-control/advogado-criminal/SKILL.md) | Advogado criminalista especializado em Maria da Penha, violencia domestica, feminicidio, direito penal brasileiro, medidas protetivas, inquerito policial e acao penal. |
| [advogado-especialista](.archived/skills/git-version-control/advogado-especialista/SKILL.md) | Advogado especialista em todas as areas do Direito brasileiro: familia, criminal, trabalhista, tributario, consumidor, imobiliario, empresarial, civil e constitucional. |
| [agent-orchestration-improve-agent](.archived/skills/git-version-control/agent-orchestration-improve-agent/SKILL.md) | Systematic improvement of existing agents through performance analysis, prompt engineering, and continuous iteration. |
| [agent-orchestration-multi-agent-optimize](.archived/skills/git-version-control/agent-orchestration-multi-agent-optimize/SKILL.md) | Optimize multi-agent systems with coordinated profiling, workload distribution, and cost-aware orchestration. Use when improving agent performance, throughput, or reliability. |
| [ai-seo](.archived/skills/git-version-control/ai-seo/SKILL.md) | Optimize content for AI search and LLM citations across AI Overviews, ChatGPT, Perplexity, Claude, Gemini, and similar systems. Use when improving AI visibility, answer engine optimization, or citation readiness. |
| [algorithmic-art](.archived/skills/git-version-control/algorithmic-art/SKILL.md) | Algorithmic philosophies are computational aesthetic movements that are then expressed through code. Output .md files (philosophy), .html files (interactive viewer), and .js files (generative algorithms). |
| [analytics-product](.archived/skills/git-version-control/analytics-product/SKILL.md) | Analytics de produto — PostHog, Mixpanel, eventos, funnels, cohorts, retencao, north star metric, OKRs e dashboards de produto. |
| [analyze-project](.archived/skills/git-version-control/analyze-project/SKILL.md) | Forensic root cause analyzer for Antigravity sessions. Classifies scope deltas, rework patterns, root causes, hotspots, and auto-improves prompts/health. |
| [app-store-changelog](.archived/skills/git-version-control/app-store-changelog/SKILL.md) | Generate user-facing App Store release notes from git history since the last tag. |
| [basecamp-automation](.archived/skills/git-version-control/basecamp-automation/SKILL.md) | Automate Basecamp project management, to-dos, messages, people, and to-do list organization via Rube MCP (Composio). Always search tools first for current schemas. |
| [bash-pro](.archived/skills/git-version-control/bash-pro/SKILL.md) | Master of defensive Bash scripting for production automation, CI/CD |
| [binary-analysis-patterns](.archived/skills/git-version-control/binary-analysis-patterns/SKILL.md) | Comprehensive patterns and techniques for analyzing compiled binaries, understanding assembly code, and reconstructing program logic. |
| [blueprint](.archived/skills/git-version-control/blueprint/SKILL.md) | Turn a one-line objective into a step-by-step construction plan any coding agent can execute cold. Each step has a self-contained context brief — a fresh agent in a new session can pick up any step without reading prior steps. |
| [c4-architecture-c4-architecture](.archived/skills/git-version-control/c4-architecture-c4-architecture/SKILL.md) | Generate comprehensive C4 architecture documentation for an existing repository/codebase using a bottom-up analysis approach. |
| [c4-code](.archived/skills/git-version-control/c4-code/SKILL.md) | Expert C4 Code-level documentation specialist. Analyzes code directories to create comprehensive C4 code-level documentation including function signatures, arguments, dependencies, and code structure. |
| [changelog-automation](.archived/skills/git-version-control/changelog-automation/SKILL.md) | Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions. |
| [churn-prevention](.archived/skills/git-version-control/churn-prevention/SKILL.md) | Reduce voluntary and involuntary churn with cancel flows, save offers, dunning, win-back tactics, and retention strategy. Use when users are cancelling, failed payments are rising, or subscription retention needs improvement. |
| [citation-management](.archived/skills/git-version-control/citation-management/SKILL.md) | Manage citations systematically throughout the research and writing process. |
| [claude-code-expert](.archived/skills/git-version-control/claude-code-expert/SKILL.md) | Especialista profundo em Claude Code - CLI da Anthropic. Maximiza produtividade com atalhos, hooks, MCPs, configuracoes avancadas, workflows, CLAUDE.md, memoria, sub-agentes, permissoes e integracao com ecossistemas. |
| [claude-speed-reader](.archived/skills/git-version-control/claude-speed-reader/SKILL.md) | -Speed read Claude's responses at 600+ WPM using RSVP with Spritz-style ORP highlighting |
| [code-refactoring-tech-debt](.archived/skills/git-version-control/code-refactoring-tech-debt/SKILL.md) | You are a technical debt expert specializing in identifying, quantifying, and prioritizing technical debt in software projects. Analyze the codebase to uncover debt, assess its impact, and create acti |
| [code-review-ai-ai-review](.archived/skills/git-version-control/code-review-ai-ai-review/SKILL.md) | You are an expert AI-powered code review specialist combining automated static analysis, intelligent pattern recognition, and modern DevOps practices. Leverage AI tools (GitHub Copilot, Qodo, GPT-5, C |
| [code-simplifier](.archived/skills/git-version-control/code-simplifier/SKILL.md) | Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when asked to "simplify code", "clean up code", "refactor for clarity", "improve readability", or review recently modified code for elegance. Focuses on project-specific best practices. |
| [codebase-cleanup-tech-debt](.archived/skills/git-version-control/codebase-cleanup-tech-debt/SKILL.md) | You are a technical debt expert specializing in identifying, quantifying, and prioritizing technical debt in software projects. Analyze the codebase to uncover debt, assess its impact, and create acti |
| [codex-review](.archived/skills/git-version-control/codex-review/SKILL.md) | Professional code review with auto CHANGELOG generation, integrated with Codex AI. Use when you want professional code review before commits, you need automatic CHANGELOG generation, or reviewing large-scale refactoring. |
| [commit](.archived/skills/git-version-control/commit/SKILL.md) | Conventional commits with issue refs |
| [competitive-landscape](.archived/skills/git-version-control/competitive-landscape/SKILL.md) | Comprehensive frameworks for analyzing competition, identifying differentiation opportunities, and developing winning market positioning strategies. |
| [comprehensive-review-full-review](.archived/skills/git-version-control/comprehensive-review-full-review/SKILL.md) | Use when working with comprehensive review full review |
| [comprehensive-review-pr-enhance](.archived/skills/git-version-control/comprehensive-review-pr-enhance/SKILL.md) | > |
| [conductor-revert](.archived/skills/git-version-control/conductor-revert/SKILL.md) | Git-aware undo by logical work unit (track, phase, or task) |
| [conductor-setup](.archived/skills/git-version-control/conductor-setup/SKILL.md) | Configure a Rails project to work with Conductor (parallel coding agents) |
| [conductor-status](.archived/skills/git-version-control/conductor-status/SKILL.md) | Display project status, active tracks, and next actions |
| [conductor-validator](.archived/skills/git-version-control/conductor-validator/SKILL.md) | Validates Conductor project artifacts for completeness, |
| [context-guardian](.archived/skills/git-version-control/context-guardian/SKILL.md) | Guardiao de contexto que preserva dados criticos antes da compactacao automatica. Snapshots, verificacao de integridade e zero perda de informacao. |
| [copy-editing](.archived/skills/git-version-control/copy-editing/SKILL.md) | You are an expert copy editor specializing in marketing and conversion copy. Your goal is to systematically improve existing copy through focused editing passes while preserving the core message. |
| [create-branch](.archived/skills/git-version-control/create-branch/SKILL.md) | Branch naming conventions |
| [create-pr](.archived/skills/git-version-control/create-pr/SKILL.md) | Pull request writing |
| [cred-omega](.archived/skills/git-version-control/cred-omega/SKILL.md) | CISO operacional enterprise para gestao total de credenciais e segredos. |
| [data-engineering-data-pipeline](.archived/skills/git-version-control/data-engineering-data-pipeline/SKILL.md) | You are a data pipeline architecture expert specializing in scalable, reliable, and cost-effective data pipelines for batch and streaming data processing. |
| [deep-research](.archived/skills/git-version-control/deep-research/SKILL.md) | Run autonomous research tasks that plan, search, read, and synthesize information into comprehensive reports. |
| [deployment-procedures](.archived/skills/git-version-control/deployment-procedures/SKILL.md) | Production deployment principles and decision-making. Safe deployment workflows, rollback strategies, and verification. Teaches thinking, not scripts. |
| [diary](.archived/skills/git-version-control/diary/SKILL.md) | Unified Diary System: A context-preserving automated logger for multi-project development. |
| [elon-musk](.archived/skills/git-version-control/elon-musk/SKILL.md) | Agente que simula Elon Musk com profundidade psicologica e comunicacional de alta fidelidade. Ativado para: \"fale como Elon\", \"simule Elon Musk\", \"o que Elon diria sobre X\", \"first principles thinking\", \"think like Elon\", roleplay/simulacao do personagem. |
| [energy-procurement](.archived/skills/git-version-control/energy-procurement/SKILL.md) | Codified expertise for electricity and gas procurement, tariff optimisation, demand charge management, renewable PPA evaluation, and multi-facility energy cost management. |
| [error-diagnostics-error-trace](.archived/skills/git-version-control/error-diagnostics-error-trace/SKILL.md) | You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking systems, configure alerts, implement structured logging, |
| [evolution](.archived/skills/git-version-control/evolution/SKILL.md) | This skill enables makepad-skills to self-improve continuously during development. |
| [file-organizer](.archived/skills/git-version-control/file-organizer/SKILL.md) | 6. Reduces Clutter: Identifies old files you probably don't need anymore |
| [find-bugs](.archived/skills/git-version-control/find-bugs/SKILL.md) | Bug finding in branch changes |
| [fp-errors](.archived/skills/git-version-control/fp-errors/SKILL.md) | Stop throwing everywhere - handle errors as values using Either and TaskEither for cleaner, more predictable code |
| [fp-ts-errors](.archived/skills/git-version-control/fp-ts-errors/SKILL.md) | Handle errors as values using fp-ts Either and TaskEither for cleaner, more predictable TypeScript code. Use when implementing error handling patterns with fp-ts. |
| [framework-migration-code-migrate](.archived/skills/git-version-control/framework-migration-code-migrate/SKILL.md) | You are a code migration expert specializing in transitioning codebases between frameworks, languages, versions, and platforms. Generate comprehensive migration plans, automated migration scripts, and |
| [framework-migration-legacy-modernize](.archived/skills/git-version-control/framework-migration-legacy-modernize/SKILL.md) | Orchestrate a comprehensive legacy system modernization using the strangler fig pattern, enabling gradual replacement of outdated components while maintaining continuous business operations through ex |
| [game-art](.archived/skills/git-version-control/game-art/SKILL.md) | Game art principles. Visual style selection, asset pipeline, animation workflow. |
| [geoffrey-hinton](.archived/skills/git-version-control/geoffrey-hinton/SKILL.md) | Agente que simula Geoffrey Hinton — Godfather of Deep Learning, Prêmio Turing 2018, criador do backpropagation e das Deep Belief Networks. |
| [gh-review-requests](.archived/skills/git-version-control/gh-review-requests/SKILL.md) | Fetch unread GitHub notifications for open PRs where review is requested from a specified team or opened by a team member. Use when asked to "find PRs I need to review", "show my review requests", "what needs my review", "fetch GitHub review requests", or "check team review queue". |
| [git-advanced-workflows](.archived/skills/git-version-control/git-advanced-workflows/SKILL.md) | Clean history, collaboration, recovery |
| [git-hooks-automation](.archived/skills/git-version-control/git-hooks-automation/SKILL.md) | Husky, lint-staged, commitlint |
| [git-pr-workflows-onboard](.archived/skills/git-version-control/git-pr-workflows-onboard/SKILL.md) | You are an **expert onboarding specialist and knowledge transfer architect** with deep experience in remote-first organizations, technical team integration, and accelerated learning methodologies. You |
| [git-pr-workflows-pr-enhance](.archived/skills/git-version-control/git-pr-workflows-pr-enhance/SKILL.md) | You are a PR optimization expert specializing in creating high-quality pull requests that facilitate efficient code reviews. Generate comprehensive PR descriptions, automate review processes, and ensu |
| [git-pushing](.archived/skills/git-version-control/git-pushing/SKILL.md) | Stage, commit, push workflow |
| [github](.archived/skills/git-version-control/github/SKILL.md) | gh CLI for issues, PRs, Actions |
| [github-issue-creator](.archived/skills/git-version-control/github-issue-creator/SKILL.md) | Transform messy input (error logs, voice notes, screenshots) into clean, actionable GitHub issues. |
| [github-workflow-automation](.archived/skills/git-version-control/github-workflow-automation/SKILL.md) | Patterns for automating GitHub workflows with AI assistance, inspired by [Gemini CLI](https://github.com/google-gemini/gemini-cli) and modern DevOps practices. |
| [gitlab-automation](.archived/skills/git-version-control/gitlab-automation/SKILL.md) | Automate GitLab project management, issues, merge requests, pipelines, branches, and user operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [google-analytics-automation](.archived/skills/git-version-control/google-analytics-automation/SKILL.md) | Automate Google Analytics tasks via Rube MCP (Composio): run reports, list accounts/properties, funnels, pivots, key events. Always search tools first for current schemas. |
| [hr-pro](.archived/skills/git-version-control/hr-pro/SKILL.md) | Professional, ethical HR partner for hiring, onboarding/offboarding, PTO and leave, performance, compliant policies, and employee relations. |
| [hugging-face-cli](.archived/skills/git-version-control/hugging-face-cli/SKILL.md) | The hf CLI provides direct terminal access to the Hugging Face Hub for downloading, uploading, and managing repositories, cache, and compute resources. |
| [incident-runbook-templates](.archived/skills/git-version-control/incident-runbook-templates/SKILL.md) | Production-ready templates for incident response runbooks covering detection, triage, mitigation, resolution, and communication. |
| [inventory-demand-planning](.archived/skills/git-version-control/inventory-demand-planning/SKILL.md) | Codified expertise for demand forecasting, safety stock optimisation, replenishment planning, and promotional lift estimation at multi-location retailers. |
| [issues](.archived/skills/git-version-control/issues/SKILL.md) | Interact with GitHub issues - create, list, and view issues. |
| [iterate-pr](.archived/skills/git-version-control/iterate-pr/SKILL.md) | Fix CI failures until green |
| [latex-paper-conversion](.archived/skills/git-version-control/latex-paper-conversion/SKILL.md) | This skill should be used when the user asks to convert an academic paper in LaTeX from one format (e.g., Springer, IPOL) to another format (e.g., MDPI, IEEE, Nature). It automates extraction, injection, fixing formatting, and compiling. |
| [legal-advisor](.archived/skills/git-version-control/legal-advisor/SKILL.md) | Draft privacy policies, terms of service, disclaimers, and legal notices. Creates GDPR-compliant texts, cookie policies, and data processing agreements. |
| [leiloeiro-juridico](.archived/skills/git-version-control/leiloeiro-juridico/SKILL.md) | Analise juridica de leiloes: nulidades, bem de familia, alienacao fiduciaria, CPC arts 829-903, Lei 9514/97, onus reais, embargos e jurisprudencia. |
| [linear-claude-skill](.archived/skills/git-version-control/linear-claude-skill/SKILL.md) | Manage Linear issues, projects, and teams |
| [linkedin-automation](.archived/skills/git-version-control/linkedin-automation/SKILL.md) | Automate LinkedIn tasks via Rube MCP (Composio): create posts, manage profile, company info, comments, and image uploads. Always search tools first for current schemas. |
| [linkedin-cli](.archived/skills/git-version-control/linkedin-cli/SKILL.md) | Use when automating LinkedIn via CLI: fetch profiles, search people/companies, send messages, manage connections, create posts, and Sales Navigator. |
| [lint-and-validate](.archived/skills/git-version-control/lint-and-validate/SKILL.md) | MANDATORY: Run appropriate validation tools after EVERY code change. Do not finish a task until the code is error-free. |
| [llm-application-dev-langchain-agent](.archived/skills/git-version-control/llm-application-dev-langchain-agent/SKILL.md) | You are an expert LangChain agent developer specializing in production-grade AI systems using LangChain 0.1+ and LangGraph. |
| [llm-application-dev-prompt-optimize](.archived/skills/git-version-control/llm-application-dev-prompt-optimize/SKILL.md) | You are an expert prompt engineer specializing in crafting effective prompts for LLMs through advanced techniques including constitutional AI, chain-of-thought reasoning, and model-specific optimizati |
| [logistics-exception-management](.archived/skills/git-version-control/logistics-exception-management/SKILL.md) | Codified expertise for handling freight exceptions, shipment delays, damages, losses, and carrier disputes. Informed by logistics professionals with 15+ years operational experience. |
| [market-sizing-analysis](.archived/skills/git-version-control/market-sizing-analysis/SKILL.md) | Comprehensive market sizing methodologies for calculating Total Addressable Market (TAM), Serviceable Available Market (SAM), and Serviceable Obtainable Market (SOM) for startup opportunities. |
| [marketing-psychology](.archived/skills/git-version-control/marketing-psychology/SKILL.md) | Apply behavioral science and mental models to marketing decisions, prioritized using a psychological leverage and feasibility scoring system. |
| [maxia](.archived/skills/git-version-control/maxia/SKILL.md) | Connect to MAXIA AI-to-AI marketplace on Solana. Discover, buy, sell AI services. Earn USDC. 13 MCP tools, A2A protocol, DeFi yields, sentiment analysis, rug detection. |
| [memory-safety-patterns](.archived/skills/git-version-control/memory-safety-patterns/SKILL.md) | Cross-language patterns for memory-safe programming including RAII, ownership, smart pointers, and resource management. |
| [mixpanel-automation](.archived/skills/git-version-control/mixpanel-automation/SKILL.md) | Automate Mixpanel tasks via Rube MCP (Composio): events, segmentation, funnels, cohorts, user profiles, JQL queries. Always search tools first for current schemas. |
| [ml-pipeline-workflow](.archived/skills/git-version-control/ml-pipeline-workflow/SKILL.md) | Complete end-to-end MLOps pipeline orchestration from data preparation through model deployment. |
| [monetization](.archived/skills/git-version-control/monetization/SKILL.md) | Estrategia e implementacao de monetizacao para produtos digitais - Stripe, subscriptions, pricing experiments, freemium, upgrade flows, churn prevention, revenue optimization e modelos de negocio SaaS. |
| [multiplayer](.archived/skills/git-version-control/multiplayer/SKILL.md) | Multiplayer game development principles. Architecture, networking, synchronization. |
| [new-rails-project](.archived/skills/git-version-control/new-rails-project/SKILL.md) | Create a new Rails project |
| [observability-monitoring-monitor-setup](.archived/skills/git-version-control/observability-monitoring-monitor-setup/SKILL.md) | You are a monitoring and observability expert specializing in implementing comprehensive monitoring solutions. Set up metrics collection, distributed tracing, log aggregation, and create insightful da |
| [odoo-upgrade-advisor](.archived/skills/git-version-control/odoo-upgrade-advisor/SKILL.md) | Step-by-step Odoo version upgrade advisor: pre-upgrade checklist, community vs enterprise upgrade path, OCA module compatibility, and post-upgrade validation. |
| [office-productivity](.archived/skills/git-version-control/office-productivity/SKILL.md) | Office productivity workflow covering document creation, spreadsheet automation, presentation generation, and integration with LibreOffice and Microsoft Office formats. |
| [paywall-upgrade-cro](.archived/skills/git-version-control/paywall-upgrade-cro/SKILL.md) | You are an expert in in-app paywalls and upgrade flows. Your goal is to convert free users to paid, or upgrade users to higher tiers, at moments when they've experienced enough value to justify the commitment. |
| [pc-games](.archived/skills/git-version-control/pc-games/SKILL.md) | PC and console game development principles. Engine selection, platform features, optimization strategies. |
| [performance-profiling](.archived/skills/git-version-control/performance-profiling/SKILL.md) | Performance profiling principles. Measurement, analysis, and optimization techniques. |
| [posix-shell-pro](.archived/skills/git-version-control/posix-shell-pro/SKILL.md) | Expert in strict POSIX sh scripting for maximum portability across Unix-like systems. Specializes in shell scripts that run on any POSIX-compliant shell (dash, ash, sh, bash --posix). |
| [posthog-automation](.archived/skills/git-version-control/posthog-automation/SKILL.md) | Automate PostHog tasks via Rube MCP (Composio): events, feature flags, projects, user profiles, annotations. Always search tools first for current schemas. |
| [product-manager-toolkit](.archived/skills/git-version-control/product-manager-toolkit/SKILL.md) | Essential tools and frameworks for modern product management, from discovery to delivery. |
| [product-marketing-context](.archived/skills/git-version-control/product-marketing-context/SKILL.md) | Create or update a reusable product marketing context document with positioning, audience, ICP, use cases, and messaging. Use at the start of a project to avoid repeating core marketing context across tasks. |
| [production-scheduling](.archived/skills/git-version-control/production-scheduling/SKILL.md) | Codified expertise for production scheduling, job sequencing, line balancing, changeover optimisation, and bottleneck resolution in discrete and batch manufacturing. |
| [professional-proofreader](.archived/skills/git-version-control/professional-proofreader/SKILL.md) | > |
| [prompt-caching](.archived/skills/git-version-control/prompt-caching/SKILL.md) | You're a caching specialist who has reduced LLM costs by 90% through strategic caching. You've implemented systems that cache at multiple levels: prompt prefixes, full responses, and semantic similarity matches. |
| [recallmax](.archived/skills/git-version-control/recallmax/SKILL.md) | FREE — God-tier long-context memory for AI agents. Injects 500K-1M clean tokens, auto-summarizes with tone/intent preservation, compresses 14-turn history into 800 tokens. |
| [red-team-tactics](.archived/skills/git-version-control/red-team-tactics/SKILL.md) | Red team tactics principles based on MITRE ATT&CK. Attack phases, detection evasion, reporting. |
| [remotion](.archived/skills/git-version-control/remotion/SKILL.md) | Generate walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays |
| [render-automation](.archived/skills/git-version-control/render-automation/SKILL.md) | Automate Render tasks via Rube MCP (Composio): services, deployments, projects. Always search tools first for current schemas. |
| [senior-fullstack](.archived/skills/git-version-control/senior-fullstack/SKILL.md) | Complete toolkit for senior fullstack with modern tools and best practices. |
| [sentry-automation](.archived/skills/git-version-control/sentry-automation/SKILL.md) | Automate Sentry tasks via Rube MCP (Composio): manage issues/events, configure alerts, track releases, monitor projects and teams. Always search tools first for current schemas. |
| [seo-cannibalization-detector](.archived/skills/git-version-control/seo-cannibalization-detector/SKILL.md) | Analyzes multiple provided pages to identify keyword overlap and potential cannibalization issues. Suggests differentiation strategies. Use PROACTIVELY when reviewing similar content. |
| [seo-content-planner](.archived/skills/git-version-control/seo-content-planner/SKILL.md) | Creates comprehensive content outlines and topic clusters for SEO. |
| [seo-content-refresher](.archived/skills/git-version-control/seo-content-refresher/SKILL.md) | Identifies outdated elements in provided content and suggests updates to maintain freshness. Finds statistics, dates, and examples that need updating. Use PROACTIVELY for older content. |
| [seo-fundamentals](.archived/skills/git-version-control/seo-fundamentals/SKILL.md) | Core principles of SEO including E-E-A-T, Core Web Vitals, technical foundations, content quality, and how modern search engines evaluate pages. |
| [seo-image-gen](.archived/skills/git-version-control/seo-image-gen/SKILL.md) | Generate SEO-focused images such as OG cards, hero images, schema assets, product visuals, and infographics. Use when image generation is part of an SEO workflow or content publishing task. |
| [seo-keyword-strategist](.archived/skills/git-version-control/seo-keyword-strategist/SKILL.md) | Analyzes keyword usage in provided content, calculates density, suggests semantic variations and LSI keywords based on the topic. Prevents over-optimization. Use PROACTIVELY for content optimization. |
| [seo-meta-optimizer](.archived/skills/git-version-control/seo-meta-optimizer/SKILL.md) | Creates optimized meta titles, descriptions, and URL suggestions based on character limits and best practices. Generates compelling, keyword-rich metadata. Use PROACTIVELY for new content. |
| [seo-snippet-hunter](.archived/skills/git-version-control/seo-snippet-hunter/SKILL.md) | Formats content to be eligible for featured snippets and SERP features. Creates snippet-optimized content blocks based on best practices. Use PROACTIVELY for question-based content. |
| [server-management](.archived/skills/git-version-control/server-management/SKILL.md) | Server management principles and decision-making. Process management, monitoring strategy, and scaling decisions. Teaches thinking, not commands. |
| [skill-creator](.archived/skills/git-version-control/skill-creator/SKILL.md) | To create new CLI skills following Anthropic's official best practices with zero manual configuration. This skill automates brainstorming, template application, validation, and installation processes while maintaining progressive disclosure patterns and writing style standards. |
| [skill-improver](.archived/skills/git-version-control/skill-improver/SKILL.md) | Iteratively improve a Claude Code skill using the skill-reviewer agent until it meets quality standards. Use when improving a skill with multiple quality issues, iterating on a new skill until it meets standards, or automated fix-review cycles instead of manual editing. |
| [skill-rails-upgrade](.archived/skills/git-version-control/skill-rails-upgrade/SKILL.md) | Analyze Rails apps and provide upgrade assessments |
| [skill-seekers](.archived/skills/git-version-control/skill-seekers/SKILL.md) | -Automatically convert documentation websites, GitHub repositories, and PDFs into Claude AI skills in minutes. |
| [skin-health-analyzer](.archived/skills/git-version-control/skin-health-analyzer/SKILL.md) | Analyze skin health data, identify skin problem patterns, assess skin health status. Supports correlation analysis with nutrition, chronic diseases, and medication data. |
| [slack-gif-creator](.archived/skills/git-version-control/slack-gif-creator/SKILL.md) | A toolkit providing utilities and knowledge for creating animated GIFs optimized for Slack. |
| [sred-project-organizer](.archived/skills/git-version-control/sred-project-organizer/SKILL.md) | Take a list of projects and their related documentation, and organize them into the SRED format for submission. |
| [sred-work-summary](.archived/skills/git-version-control/sred-work-summary/SKILL.md) | Go back through the previous year of work and create a Notion doc that groups relevant links into projects that can then be documented as SRED projects. |
| [startup-business-analyst-business-case](.archived/skills/git-version-control/startup-business-analyst-business-case/SKILL.md) | Generate comprehensive investor-ready business case document with |
| [startup-business-analyst-financial-projections](.archived/skills/git-version-control/startup-business-analyst-financial-projections/SKILL.md) | Create detailed 3-5 year financial model with revenue, costs, cash |
| [startup-business-analyst-market-opportunity](.archived/skills/git-version-control/startup-business-analyst-market-opportunity/SKILL.md) | Generate comprehensive market opportunity analysis with TAM/SAM/SOM |
| [task-intelligence](.archived/skills/git-version-control/task-intelligence/SKILL.md) | Protocolo de Inteligência Pré-Tarefa — ativa TODOS os agentes relevantes do ecossistema ANTES de executar qualquer tarefa solicitada pelo usuário. |
| [team-collaboration-issue](.archived/skills/git-version-control/team-collaboration-issue/SKILL.md) | You are a GitHub issue resolution expert specializing in systematic bug investigation, feature implementation, and collaborative development workflows. Your expertise spans issue triage, root cause an |
| [team-collaboration-standup-notes](.archived/skills/git-version-control/team-collaboration-standup-notes/SKILL.md) | You are an expert team communication specialist focused on async-first standup practices, AI-assisted note generation from commit history, and effective remote team coordination patterns. |
| [terraform-skill](.archived/skills/git-version-control/terraform-skill/SKILL.md) | Terraform infrastructure as code best practices |
| [threejs-animation](.archived/skills/git-version-control/threejs-animation/SKILL.md) | Three.js animation - keyframe animation, skeletal animation, morph targets, animation mixing. Use when animating objects, playing GLTF animations, creating procedural motion, or blending animations. |
| [threejs-loaders](.archived/skills/git-version-control/threejs-loaders/SKILL.md) | Three.js asset loading - GLTF, textures, images, models, async patterns. Use when loading 3D models, textures, HDR environments, or managing loading progress. |
| [threejs-materials](.archived/skills/git-version-control/threejs-materials/SKILL.md) | Three.js materials - PBR, basic, phong, shader materials, material properties. Use when styling meshes, working with textures, creating custom shaders, or optimizing material performance. |
| [threejs-postprocessing](.archived/skills/git-version-control/threejs-postprocessing/SKILL.md) | Three.js post-processing - EffectComposer, bloom, DOF, screen effects. Use when adding visual effects, color grading, blur, glow, or creating custom screen-space shaders. |
| [tiktok-automation](.archived/skills/git-version-control/tiktok-automation/SKILL.md) | Automate TikTok tasks via Rube MCP (Composio): upload/publish videos, post photos, manage content, and view user profiles/stats. Always search tools first for current schemas. |
| [todoist-automation](.archived/skills/git-version-control/todoist-automation/SKILL.md) | Automate Todoist task management, projects, sections, filtering, and bulk operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [tutorial-engineer](.archived/skills/git-version-control/tutorial-engineer/SKILL.md) | Creates step-by-step tutorials and educational content from code. Transforms complex concepts into progressive learning experiences with hands-on examples. |
| [uncle-bob-craft](.archived/skills/git-version-control/uncle-bob-craft/SKILL.md) | Use when performing code review, writing or refactoring code, or discussing architecture; complements clean-code and does not replace project linter/formatter. |
| [unity-ecs-patterns](.archived/skills/git-version-control/unity-ecs-patterns/SKILL.md) | Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler. |
| [unsplash-integration](.archived/skills/git-version-control/unsplash-integration/SKILL.md) | Integration skill for searching and fetching high-quality, free-to-use professional photography from Unsplash. |
| [using-git-worktrees](.archived/skills/git-version-control/using-git-worktrees/SKILL.md) | Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching. |
| [varlock-claude-skill](.archived/skills/git-version-control/varlock-claude-skill/SKILL.md) | Secure environment variable management ensuring secrets are never exposed in Claude sessions, terminals, logs, or git commits |
| [vercel-automation](.archived/skills/git-version-control/vercel-automation/SKILL.md) | Automate Vercel tasks via Rube MCP (Composio): manage deployments, domains, DNS, env vars, projects, and teams. Always search tools first for current schemas. |
| [vercel-deployment](.archived/skills/git-version-control/vercel-deployment/SKILL.md) | Expert knowledge for deploying to Vercel with Next.js Use when: vercel, deploy, deployment, hosting, production. |
| [verification-before-completion](.archived/skills/git-version-control/verification-before-completion/SKILL.md) | Claiming work is complete without verification is dishonesty, not efficiency. Use when ANY variation of success/completion claims, ANY expression of satisfaction, or ANY positive statement about work state. |
| [vexor-cli](.archived/skills/git-version-control/vexor-cli/SKILL.md) | Semantic file discovery via `vexor`. Use whenever locating where something is implemented/loaded/defined in a medium or large repo, or when the file location is unclear. Prefer this over manual browsing. |
| [web-games](.archived/skills/git-version-control/web-games/SKILL.md) | Web browser game development principles. Framework selection, WebGPU, optimization, PWA. |
| [wellally-tech](.archived/skills/git-version-control/wellally-tech/SKILL.md) | Integrate multiple digital health data sources, connect to [WellAlly.tech](https://www.wellally.tech/) knowledge base, providing data import and knowledge reference for personal health management systems. |
| [wordpress-woocommerce-development](.archived/skills/git-version-control/wordpress-woocommerce-development/SKILL.md) | WooCommerce store development workflow covering store setup, payment integration, shipping configuration, customization, and WordPress 7.0 features: AI connectors, DataViews, and collaboration tools. |
| [workflow-patterns](.archived/skills/git-version-control/workflow-patterns/SKILL.md) | Use this skill when implementing tasks according to Conductor's TDD workflow, handling phase checkpoints, managing git commits for tasks, or understanding the verification protocol. |
| [wrike-automation](.archived/skills/git-version-control/wrike-automation/SKILL.md) | Automate Wrike project management via Rube MCP (Composio): create tasks/folders, manage projects, assign work, and track progress. Always search tools first for current schemas. |
| [writing-skills](.archived/skills/git-version-control/writing-skills/SKILL.md) | Use when creating, updating, or improving agent skills. |
| [yann-lecun](.archived/skills/git-version-control/yann-lecun/SKILL.md) | Agente que simula Yann LeCun — inventor das Convolutional Neural Networks, Chief AI Scientist da Meta, Prêmio Turing 2018. |
| [yann-lecun-tecnico](.archived/skills/git-version-control/yann-lecun-tecnico/SKILL.md) | Sub-skill técnica de Yann LeCun. Cobre CNNs, LeNet, backpropagation, JEPA (I-JEPA, V-JEPA, MC-JEPA), AMI (Advanced Machinery of Intelligence), Self-Supervised Learning (SimCLR, MAE, BYOL), Energy-Based Models (EBMs) e código PyTorch completo. |
| [youtube-summarizer](.archived/skills/git-version-control/youtube-summarizer/SKILL.md) | Extract transcripts from YouTube videos and generate comprehensive, detailed summaries using intelligent analysis frameworks |
| [zustand-store-ts](.archived/skills/git-version-control/zustand-store-ts/SKILL.md) | Create Zustand stores following established patterns with proper TypeScript types and middleware. |

</details>

### 🏗️ Architecture & Patterns

<details>
<summary><b>🏗️ Architecture & Patterns (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [api-design-principles](.archived/skills/architecture-patterns/api-design-principles/SKILL.md) | REST vs GraphQL vs tRPC |
| [architect-review](.archived/skills/architecture-patterns/architect-review/SKILL.md) | Master software architect specializing in modern architecture |
| [architecture](.archived/skills/architecture-patterns/architecture/SKILL.md) | Requirements, trade-offs, ADRs |
| [architecture-patterns](.archived/skills/architecture-patterns/architecture-patterns/SKILL.md) | Clean, Hexagonal, DDD |
| [c4-component](.archived/skills/architecture-patterns/c4-component/SKILL.md) | Expert C4 Component-level documentation specialist. Synthesizes C4 Code-level documentation into Component-level architecture, defining component boundaries, interfaces, and relationships. |
| [clean-code](.archived/skills/architecture-patterns/clean-code/SKILL.md) | Uncle Bob's Clean Code principles |
| [cqrs-implementation](.archived/skills/architecture-patterns/cqrs-implementation/SKILL.md) | Command Query Responsibility Segregation |
| [ddd-context-mapping](.archived/skills/architecture-patterns/ddd-context-mapping/SKILL.md) | Map relationships between bounded contexts and define integration contracts using DDD context mapping patterns. |
| [ddd-strategic-design](.archived/skills/architecture-patterns/ddd-strategic-design/SKILL.md) | Bounded contexts, ubiquitous language |
| [ddd-tactical-patterns](.archived/skills/architecture-patterns/ddd-tactical-patterns/SKILL.md) | Entities, value objects, aggregates |
| [employment-contract-templates](.archived/skills/architecture-patterns/employment-contract-templates/SKILL.md) | Templates and patterns for creating legally sound employment documentation including contracts, offer letters, and HR policies. |
| [error-detective](.archived/skills/architecture-patterns/error-detective/SKILL.md) | Search logs and codebases for error patterns, stack traces, and anomalies. Correlates errors across systems and identifies root causes. |
| [event-sourcing-architect](.archived/skills/architecture-patterns/event-sourcing-architect/SKILL.md) | Event sourcing, CQRS, event-driven |
| [fp-data-transforms](.archived/skills/architecture-patterns/fp-data-transforms/SKILL.md) | Everyday data transformations using functional patterns - arrays, objects, grouping, aggregation, and null-safe access |
| [i18n-localization](.archived/skills/architecture-patterns/i18n-localization/SKILL.md) | Internationalization and localization patterns. Detecting hardcoded strings, managing translations, locale files, RTL support. |
| [lightning-channel-factories](.archived/skills/architecture-patterns/lightning-channel-factories/SKILL.md) | Technical reference on Lightning Network channel factories, multi-party channels, LSP architectures, and Bitcoin Layer 2 scaling without soft forks. Covers Decker-Wattenhofer, timeout trees, MuSig2 key aggregation, HTLC/PTLC forwarding, and watchtower breach detection. |
| [mermaid-expert](.archived/skills/architecture-patterns/mermaid-expert/SKILL.md) | Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures. Masters syntax for all diagram types and styling. |
| [microservices-patterns](.archived/skills/architecture-patterns/microservices-patterns/SKILL.md) | Service boundaries, communication, resilience |
| [monorepo-architect](.archived/skills/architecture-patterns/monorepo-architect/SKILL.md) | Nx, Turborepo, Bazel, Lerna |
| [powershell-windows](.archived/skills/architecture-patterns/powershell-windows/SKILL.md) | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. |
| [robius-app-architecture](.archived/skills/architecture-patterns/robius-app-architecture/SKILL.md) | | |
| [robius-widget-patterns](.archived/skills/architecture-patterns/robius-widget-patterns/SKILL.md) | | |
| [saga-orchestration](.archived/skills/architecture-patterns/saga-orchestration/SKILL.md) | Distributed transactions, long-running processes |
| [software-architecture](.archived/skills/architecture-patterns/software-architecture/SKILL.md) | Quality-focused architecture guide |

</details>

### 📊 Data & ML Engineering

<details>
<summary><b>📊 Data & ML Engineering (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [box-automation](.archived/skills/data-ml-engineering/box-automation/SKILL.md) | Automate Box operations including file upload/download, content search, folder management, collaboration, metadata queries, and sign requests through Composio's Box toolkit. |
| [constant-time-analysis](.archived/skills/data-ml-engineering/constant-time-analysis/SKILL.md) | Analyze cryptographic code to detect operations that leak secret data through execution timing variations. |
| [content-marketer](.archived/skills/data-ml-engineering/content-marketer/SKILL.md) | Elite content marketing strategist specializing in AI-powered content creation, omnichannel distribution, SEO optimization, and data-driven performance marketing. |
| [data-engineer](.archived/skills/data-ml-engineering/data-engineer/SKILL.md) | Data pipelines, Spark, dbt, Airflow |
| [data-scientist](.archived/skills/data-ml-engineering/data-scientist/SKILL.md) | Advanced analytics, predictive modeling |
| [data-storytelling](.archived/skills/data-ml-engineering/data-storytelling/SKILL.md) | Transform raw data into compelling narratives that drive decisions and inspire action. |
| [datadog-automation](.archived/skills/data-ml-engineering/datadog-automation/SKILL.md) | Automate Datadog tasks via Rube MCP (Composio): query metrics, search logs, manage monitors/dashboards, create events and downtimes. Always search tools first for current schemas. |
| [dbt-transformation-patterns](.archived/skills/data-ml-engineering/dbt-transformation-patterns/SKILL.md) | dbt model organization, testing |
| [docx-official](.archived/skills/data-ml-engineering/docx-official/SKILL.md) | A user may ask you to create, edit, or analyze the contents of a .docx file. A .docx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks. |
| [health-trend-analyzer](.archived/skills/data-ml-engineering/health-trend-analyzer/SKILL.md) | 分析一段时间内健康数据的趋势和模式。关联药物、症状、生命体征、化验结果和其他健康指标的变化。识别令人担忧的趋势、改善情况，并提供数据驱动的洞察。当用户询问健康趋势、模式、随时间的变化或"我的健康状况有什么变化？"时使用。支持多维度分析（体重/BMI、症状、药物依从性、化验结果、情绪睡眠），相关性分析，变化检测，以及交互式HTML可视化报告（ECharts图表）。 |
| [mailchimp-automation](.archived/skills/data-ml-engineering/mailchimp-automation/SKILL.md) | Automate Mailchimp email marketing including campaigns, audiences, subscribers, segments, and analytics via Rube MCP (Composio). Always search tools first for current schemas. |
| [ml-engineer](.archived/skills/data-ml-engineering/ml-engineer/SKILL.md) | PyTorch 2.x, TensorFlow, model serving |
| [mlops-engineer](.archived/skills/data-ml-engineering/mlops-engineer/SKILL.md) | ML pipelines, MLflow, Kubeflow |
| [polars](.archived/skills/data-ml-engineering/polars/SKILL.md) | Fast DataFrames for 1-100GB datasets |
| [pptx-official](.archived/skills/data-ml-engineering/pptx-official/SKILL.md) | A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks. |
| [scikit-learn](.archived/skills/data-ml-engineering/scikit-learn/SKILL.md) | Classification, regression, ML pipelines |
| [segment-cdp](.archived/skills/data-ml-engineering/segment-cdp/SKILL.md) | Client-side tracking with Analytics.js. Include track, identify, page, and group calls. Anonymous ID persists until identify merges with user. |
| [sendgrid-automation](.archived/skills/data-ml-engineering/sendgrid-automation/SKILL.md) | Automate SendGrid email delivery workflows including marketing campaigns (Single Sends), contact and list management, sender identity setup, and email analytics through Composio's SendGrid toolkit. |
| [spark-optimization](.archived/skills/data-ml-engineering/spark-optimization/SKILL.md) | Spark performance tuning |
| [youtube-automation](.archived/skills/data-ml-engineering/youtube-automation/SKILL.md) | Automate YouTube tasks via Rube MCP (Composio): upload videos, manage playlists, search content, get analytics, and handle comments. Always search tools first for current schemas. |

</details>

### 🔎 SEO & Growth

<details>
<summary><b>🔎 SEO & Growth (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [brevo-automation](.archived/skills/seo-growth/brevo-automation/SKILL.md) | Automate Brevo (formerly Sendinblue) email marketing operations through Composio's Brevo toolkit via Rube MCP. |
| [content-strategy](.archived/skills/seo-growth/content-strategy/SKILL.md) | Topic clusters, editorial roadmap |
| [email-sequence](.archived/skills/seo-growth/email-sequence/SKILL.md) | You are an expert in email marketing and automation. Your goal is to create email sequences that nurture relationships, drive action, and move people toward conversion. |
| [growth-engine](.archived/skills/seo-growth/growth-engine/SKILL.md) | Growth hacking, SEO, ASO, viral loops |
| [marketing-ideas](.archived/skills/seo-growth/marketing-ideas/SKILL.md) | SaaS marketing strategies |
| [seo](.archived/skills/seo-growth/seo/SKILL.md) | Full SEO audit: technical, on-page, schema |
| [seo-audit](.archived/skills/seo-growth/seo-audit/SKILL.md) | Crawlability, indexation, rankings |
| [seo-competitor-pages](.archived/skills/seo-growth/seo-competitor-pages/SKILL.md) | > |
| [seo-content](.archived/skills/seo-growth/seo-content/SKILL.md) | Content quality and E-E-A-T analysis |
| [seo-forensic-incident-response](.archived/skills/seo-growth/seo-forensic-incident-response/SKILL.md) | Investigate sudden drops in organic traffic or rankings and run a structured forensic SEO incident response with triage, root-cause analysis and recovery plan. |
| [seo-geo](.archived/skills/seo-growth/seo-geo/SKILL.md) | AI Overviews, ChatGPT, Perplexity optimization |
| [seo-hreflang](.archived/skills/seo-growth/seo-hreflang/SKILL.md) | > |
| [seo-images](.archived/skills/seo-growth/seo-images/SKILL.md) | > |
| [seo-page](.archived/skills/seo-growth/seo-page/SKILL.md) | > |
| [seo-plan](.archived/skills/seo-growth/seo-plan/SKILL.md) | > |
| [seo-schema](.archived/skills/seo-growth/seo-schema/SKILL.md) | Schema.org structured data |
| [seo-sitemap](.archived/skills/seo-growth/seo-sitemap/SKILL.md) | > |
| [seo-structure-architect](.archived/skills/seo-growth/seo-structure-architect/SKILL.md) | Analyzes and optimizes content structure including header hierarchy, suggests schema markup, and internal linking opportunities. Creates search-friendly content organization. |
| [seo-technical](.archived/skills/seo-growth/seo-technical/SKILL.md) | Crawlability, Core Web Vitals, robots.txt |

</details>

### 💰 Business, Product & Marketing

<details>
<summary><b>💰 Business, Product & Marketing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [business-analyst](.archived/skills/business-product-marketing/business-analyst/SKILL.md) | KPI frameworks, predictive models |
| [copywriting](.archived/skills/business-product-marketing/copywriting/SKILL.md) | Conversion-focused marketing copy |
| [micro-saas-launcher](.archived/skills/business-product-marketing/micro-saas-launcher/SKILL.md) | Idea → paying customers in weeks |
| [pricing-strategy](.archived/skills/business-product-marketing/pricing-strategy/SKILL.md) | Pricing, packaging, monetization |
| [saas-mvp-launcher](.archived/skills/business-product-marketing/saas-mvp-launcher/SKILL.md) | SaaS MVP roadmap |
| [sales-automator](.archived/skills/business-product-marketing/sales-automator/SKILL.md) | Cold emails, proposals, pricing pages |
| [senior-product-manager](.archived/skills/business-product-marketing/senior-product-manager/SKILL.md) | PM agent with 30+ frameworks |
| [startup-analyst](.archived/skills/business-product-marketing/startup-analyst/SKILL.md) | Market sizing, financial modeling |
| [whatsapp-automation](.archived/skills/business-product-marketing/whatsapp-automation/SKILL.md) | Automate WhatsApp Business tasks via Rube MCP (Composio): send messages, manage templates, upload media, and handle contacts. Always search tools first for current schemas. |

</details>

### 🔌 SaaS Integrations & Automations

<details>
<summary><b>🔌 SaaS Integrations & Automations (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [airtable-automation](.archived/skills/saas-integrations-automations/airtable-automation/SKILL.md) | Airtable via Composio |
| [asana-automation](.archived/skills/saas-integrations-automations/asana-automation/SKILL.md) | Asana via Composio |
| [clickup-automation](.archived/skills/saas-integrations-automations/clickup-automation/SKILL.md) | ClickUp via Composio |
| [discord-automation](.archived/skills/saas-integrations-automations/discord-automation/SKILL.md) | Discord via Composio |
| [github-automation](.archived/skills/saas-integrations-automations/github-automation/SKILL.md) | GitHub via Composio |
| [gmail-automation](.archived/skills/saas-integrations-automations/gmail-automation/SKILL.md) | Gmail with standalone OAuth |
| [google-calendar-automation](.archived/skills/saas-integrations-automations/google-calendar-automation/SKILL.md) | Google Calendar with OAuth |
| [google-drive-automation](.archived/skills/saas-integrations-automations/google-drive-automation/SKILL.md) | Google Drive with OAuth |
| [google-sheets-automation](.archived/skills/saas-integrations-automations/google-sheets-automation/SKILL.md) | Google Sheets with OAuth |
| [hubspot-automation](.archived/skills/saas-integrations-automations/hubspot-automation/SKILL.md) | HubSpot CRM via Composio |
| [jira-automation](.archived/skills/saas-integrations-automations/jira-automation/SKILL.md) | Jira via Composio |
| [linear-automation](.archived/skills/saas-integrations-automations/linear-automation/SKILL.md) | Linear via Composio |
| [notion-automation](.archived/skills/saas-integrations-automations/notion-automation/SKILL.md) | Notion via Composio |
| [salesforce-automation](.archived/skills/saas-integrations-automations/salesforce-automation/SKILL.md) | Salesforce via Composio |
| [shopify-automation](.archived/skills/saas-integrations-automations/shopify-automation/SKILL.md) | Shopify via Composio |
| [slack-automation](.archived/skills/saas-integrations-automations/slack-automation/SKILL.md) | Slack via Composio |
| [stripe-automation](.archived/skills/saas-integrations-automations/stripe-automation/SKILL.md) | Stripe via Composio |
| [trello-automation](.archived/skills/saas-integrations-automations/trello-automation/SKILL.md) | Trello via Composio |
| [zendesk-automation](.archived/skills/saas-integrations-automations/zendesk-automation/SKILL.md) | Zendesk via Composio |
| [zoom-automation](.archived/skills/saas-integrations-automations/zoom-automation/SKILL.md) | Zoom via Composio |

</details>

### ☁️ Azure SDKs

<details>
<summary><b>☁️ Azure SDKs (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [agent-framework-azure-ai-py](.archived/skills/azure-sdks/agent-framework-azure-ai-py/SKILL.md) | Build persistent agents on Azure AI Foundry using the Microsoft Agent Framework Python SDK. |
| [agents-v2-py](.archived/skills/azure-sdks/agents-v2-py/SKILL.md) | Build container-based Foundry Agents with Azure AI Projects SDK (ImageBasedHostedAgentDefinition). Use when creating hosted agents with custom container images in Azure AI Foundry. |
| [azd-deployment](.archived/skills/azure-sdks/azd-deployment/SKILL.md) | Deploy containerized frontend + backend applications to Azure Container Apps with remote builds, managed identity, and idempotent infrastructure. |
| [azure-ai-agents-persistent-dotnet](.archived/skills/azure-sdks/azure-ai-agents-persistent-dotnet/SKILL.md) | Azure AI Agents Persistent SDK for .NET. Low-level SDK for creating and managing AI agents with threads, messages, runs, and tools. |
| [azure-ai-agents-persistent-java](.archived/skills/azure-sdks/azure-ai-agents-persistent-java/SKILL.md) | Azure AI Agents Persistent SDK for Java. Low-level SDK for creating and managing AI agents with threads, messages, runs, and tools. |
| [azure-ai-anomalydetector-java](.archived/skills/azure-sdks/azure-ai-anomalydetector-java/SKILL.md) | Build anomaly detection applications with Azure AI Anomaly Detector SDK for Java. Use when implementing univariate/multivariate anomaly detection, time-series analysis, or AI-powered monitoring. |
| [azure-ai-contentsafety-java](.archived/skills/azure-sdks/azure-ai-contentsafety-java/SKILL.md) | Build content moderation applications using the Azure AI Content Safety SDK for Java. |
| [azure-ai-contentsafety-py](.archived/skills/azure-sdks/azure-ai-contentsafety-py/SKILL.md) | Azure AI Content Safety SDK for Python. Use for detecting harmful content in text and images with multi-severity classification. |
| [azure-ai-contentsafety-ts](.archived/skills/azure-sdks/azure-ai-contentsafety-ts/SKILL.md) | Analyze text and images for harmful content with customizable blocklists. |
| [azure-ai-contentunderstanding-py](.archived/skills/azure-sdks/azure-ai-contentunderstanding-py/SKILL.md) | Azure AI Content Understanding SDK for Python. Use for multimodal content extraction from documents, images, audio, and video. |
| [azure-ai-document-intelligence-dotnet](.archived/skills/azure-sdks/azure-ai-document-intelligence-dotnet/SKILL.md) | Azure AI Document Intelligence SDK for .NET. Extract text, tables, and structured data from documents using prebuilt and custom models. |
| [azure-ai-document-intelligence-ts](.archived/skills/azure-sdks/azure-ai-document-intelligence-ts/SKILL.md) | Extract text, tables, and structured data from documents using prebuilt and custom models. |
| [azure-ai-formrecognizer-java](.archived/skills/azure-sdks/azure-ai-formrecognizer-java/SKILL.md) | Build document analysis applications using the Azure AI Document Intelligence SDK for Java. |
| [azure-ai-ml-py](.archived/skills/azure-sdks/azure-ai-ml-py/SKILL.md) | Azure Machine Learning SDK v2 for Python. Use for ML workspaces, jobs, models, datasets, compute, and pipelines. |
| [azure-ai-openai-dotnet](.archived/skills/azure-sdks/azure-ai-openai-dotnet/SKILL.md) | Azure OpenAI SDK for .NET |
| [azure-ai-projects-dotnet](.archived/skills/azure-sdks/azure-ai-projects-dotnet/SKILL.md) | Azure AI Projects SDK for .NET. High-level client for Azure AI Foundry projects including agents, connections, datasets, deployments, evaluations, and indexes. |
| [azure-ai-projects-java](.archived/skills/azure-sdks/azure-ai-projects-java/SKILL.md) | Azure AI Projects SDK for Java. High-level SDK for Azure AI Foundry project management including connections, datasets, indexes, and evaluations. |
| [azure-ai-projects-py](.archived/skills/azure-sdks/azure-ai-projects-py/SKILL.md) | Azure AI Foundry SDK for Python |
| [azure-ai-projects-ts](.archived/skills/azure-sdks/azure-ai-projects-ts/SKILL.md) | High-level SDK for Azure AI Foundry projects with agents, connections, deployments, and evaluations. |
| [azure-ai-textanalytics-py](.archived/skills/azure-sdks/azure-ai-textanalytics-py/SKILL.md) | Azure AI Text Analytics SDK for sentiment analysis, entity recognition, key phrases, language detection, PII, and healthcare NLP. Use for natural language processing on text. |
| [azure-ai-transcription-py](.archived/skills/azure-sdks/azure-ai-transcription-py/SKILL.md) | Azure AI Transcription SDK for Python. Use for real-time and batch speech-to-text transcription with timestamps and diarization. |
| [azure-ai-translation-document-py](.archived/skills/azure-sdks/azure-ai-translation-document-py/SKILL.md) | Azure AI Document Translation SDK for batch translation of documents with format preservation. Use for translating Word, PDF, Excel, PowerPoint, and other document formats at scale. |
| [azure-ai-translation-text-py](.archived/skills/azure-sdks/azure-ai-translation-text-py/SKILL.md) | Azure AI Text Translation SDK for real-time text translation, transliteration, language detection, and dictionary lookup. Use for translating text content in applications. |
| [azure-ai-translation-ts](.archived/skills/azure-sdks/azure-ai-translation-ts/SKILL.md) | Text and document translation with REST-style clients. |
| [azure-ai-vision-imageanalysis-java](.archived/skills/azure-sdks/azure-ai-vision-imageanalysis-java/SKILL.md) | Build image analysis applications with Azure AI Vision SDK for Java. Use when implementing image captioning, OCR text extraction, object detection, tagging, or smart cropping. |
| [azure-ai-vision-imageanalysis-py](.archived/skills/azure-sdks/azure-ai-vision-imageanalysis-py/SKILL.md) | Azure AI Vision Image Analysis SDK for captions, tags, objects, OCR, people detection, and smart cropping. Use for computer vision and image understanding tasks. |
| [azure-ai-voicelive-dotnet](.archived/skills/azure-sdks/azure-ai-voicelive-dotnet/SKILL.md) | Azure AI Voice Live SDK for .NET. Build real-time voice AI applications with bidirectional WebSocket communication. |
| [azure-ai-voicelive-java](.archived/skills/azure-sdks/azure-ai-voicelive-java/SKILL.md) | Azure AI VoiceLive SDK for Java. Real-time bidirectional voice conversations with AI assistants using WebSocket. |
| [azure-ai-voicelive-py](.archived/skills/azure-sdks/azure-ai-voicelive-py/SKILL.md) | Build real-time voice AI applications with bidirectional WebSocket communication. |
| [azure-ai-voicelive-ts](.archived/skills/azure-sdks/azure-ai-voicelive-ts/SKILL.md) | Azure AI Voice Live SDK for JavaScript/TypeScript. Build real-time voice AI applications with bidirectional WebSocket communication. |
| [azure-appconfiguration-java](.archived/skills/azure-sdks/azure-appconfiguration-java/SKILL.md) | Azure App Configuration SDK for Java. Centralized application configuration management with key-value settings, feature flags, and snapshots. |
| [azure-appconfiguration-py](.archived/skills/azure-sdks/azure-appconfiguration-py/SKILL.md) | Azure App Configuration SDK for Python. Use for centralized configuration management, feature flags, and dynamic settings. |
| [azure-appconfiguration-ts](.archived/skills/azure-sdks/azure-appconfiguration-ts/SKILL.md) | Centralized configuration management with feature flags and dynamic refresh. |
| [azure-communication-callautomation-java](.archived/skills/azure-sdks/azure-communication-callautomation-java/SKILL.md) | Build server-side call automation workflows including IVR systems, call routing, recording, and AI-powered interactions. |
| [azure-communication-callingserver-java](.archived/skills/azure-sdks/azure-communication-callingserver-java/SKILL.md) | ⚠️ DEPRECATED: This SDK has been renamed to Call Automation. For new projects, use azure-communication-callautomation instead. This skill is for maintaining legacy code only. |
| [azure-communication-chat-java](.archived/skills/azure-sdks/azure-communication-chat-java/SKILL.md) | Build real-time chat applications with thread management, messaging, participants, and read receipts. |
| [azure-communication-common-java](.archived/skills/azure-sdks/azure-communication-common-java/SKILL.md) | Azure Communication Services common utilities for Java. Use when working with CommunicationTokenCredential, user identifiers, token refresh, or shared authentication across ACS services. |
| [azure-communication-sms-java](.archived/skills/azure-sdks/azure-communication-sms-java/SKILL.md) | Send SMS messages with Azure Communication Services SMS Java SDK. Use when implementing SMS notifications, alerts, OTP delivery, bulk messaging, or delivery reports. |
| [azure-compute-batch-java](.archived/skills/azure-sdks/azure-compute-batch-java/SKILL.md) | Azure Batch SDK for Java. Run large-scale parallel and HPC batch jobs with pools, jobs, tasks, and compute nodes. |
| [azure-containerregistry-py](.archived/skills/azure-sdks/azure-containerregistry-py/SKILL.md) | Azure Container Registry SDK for Python. Use for managing container images, artifacts, and repositories. |
| [azure-cosmos-db-py](.archived/skills/azure-sdks/azure-cosmos-db-py/SKILL.md) | Build production-grade Azure Cosmos DB NoSQL services following clean code, security best practices, and TDD principles. |
| [azure-cosmos-java](.archived/skills/azure-sdks/azure-cosmos-java/SKILL.md) | Azure Cosmos DB SDK for Java. NoSQL database operations with global distribution, multi-model support, and reactive patterns. |
| [azure-cosmos-py](.archived/skills/azure-sdks/azure-cosmos-py/SKILL.md) | Cosmos DB NoSQL for Python |
| [azure-cosmos-rust](.archived/skills/azure-sdks/azure-cosmos-rust/SKILL.md) | Azure Cosmos DB SDK for Rust (NoSQL API). Use for document CRUD, queries, containers, and globally distributed data. |
| [azure-cosmos-ts](.archived/skills/azure-sdks/azure-cosmos-ts/SKILL.md) | Azure Cosmos DB JavaScript/TypeScript SDK (@azure/cosmos) for data plane operations. Use for CRUD operations on documents, queries, bulk operations, and container management. |
| [azure-data-tables-java](.archived/skills/azure-sdks/azure-data-tables-java/SKILL.md) | Build table storage applications using the Azure Tables SDK for Java. Works with both Azure Table Storage and Cosmos DB Table API. |
| [azure-data-tables-py](.archived/skills/azure-sdks/azure-data-tables-py/SKILL.md) | Azure Tables SDK for Python (Storage and Cosmos DB). Use for NoSQL key-value storage, entity CRUD, and batch operations. |
| [azure-eventgrid-dotnet](.archived/skills/azure-sdks/azure-eventgrid-dotnet/SKILL.md) | Azure Event Grid SDK for .NET. Client library for publishing and consuming events with Azure Event Grid. Use for event-driven architectures, pub/sub messaging, CloudEvents, and EventGridEvents. |
| [azure-eventgrid-java](.archived/skills/azure-sdks/azure-eventgrid-java/SKILL.md) | Build event-driven applications with Azure Event Grid SDK for Java. Use when publishing events, implementing pub/sub patterns, or integrating with Azure services via events. |
| [azure-eventgrid-py](.archived/skills/azure-sdks/azure-eventgrid-py/SKILL.md) | Azure Event Grid SDK for Python. Use for publishing events, handling CloudEvents, and event-driven architectures. |
| [azure-eventhub-dotnet](.archived/skills/azure-sdks/azure-eventhub-dotnet/SKILL.md) | Azure Event Hubs SDK for .NET. |
| [azure-eventhub-java](.archived/skills/azure-sdks/azure-eventhub-java/SKILL.md) | Build real-time streaming applications with Azure Event Hubs SDK for Java. Use when implementing event streaming, high-throughput data ingestion, or building event-driven architectures. |
| [azure-eventhub-py](.archived/skills/azure-sdks/azure-eventhub-py/SKILL.md) | Azure Event Hubs streaming |
| [azure-eventhub-rust](.archived/skills/azure-sdks/azure-eventhub-rust/SKILL.md) | Azure Event Hubs SDK for Rust. Use for sending and receiving events, streaming data ingestion. |
| [azure-eventhub-ts](.archived/skills/azure-sdks/azure-eventhub-ts/SKILL.md) | High-throughput event streaming and real-time data ingestion. |
| [azure-functions](.archived/skills/azure-sdks/azure-functions/SKILL.md) | Modern .NET execution model with process isolation |
| [azure-identity-dotnet](.archived/skills/azure-sdks/azure-identity-dotnet/SKILL.md) | Azure Identity SDK for .NET. Authentication library for Azure SDK clients using Microsoft Entra ID. Use for DefaultAzureCredential, managed identity, service principals, and developer credentials. |
| [azure-identity-java](.archived/skills/azure-sdks/azure-identity-java/SKILL.md) | Authenticate Java applications with Azure services using Microsoft Entra ID (Azure AD). |
| [azure-identity-py](.archived/skills/azure-sdks/azure-identity-py/SKILL.md) | Azure Identity authentication |
| [azure-identity-rust](.archived/skills/azure-sdks/azure-identity-rust/SKILL.md) | Azure Identity SDK for Rust authentication. Use for DeveloperToolsCredential, ManagedIdentityCredential, ClientSecretCredential, and token-based authentication. |
| [azure-identity-ts](.archived/skills/azure-sdks/azure-identity-ts/SKILL.md) | Authenticate to Azure services with various credential types. |
| [azure-keyvault-certificates-rust](.archived/skills/azure-sdks/azure-keyvault-certificates-rust/SKILL.md) | Azure Key Vault Certificates SDK for Rust. Use for creating, importing, and managing certificates. |
| [azure-keyvault-keys-rust](.archived/skills/azure-sdks/azure-keyvault-keys-rust/SKILL.md) | Azure Key Vault Keys SDK for Rust. Use for creating, managing, and using cryptographic keys. Triggers: "keyvault keys rust", "KeyClient rust", "create key rust", "encrypt rust", "sign rust". |
| [azure-keyvault-keys-ts](.archived/skills/azure-sdks/azure-keyvault-keys-ts/SKILL.md) | Manage cryptographic keys using Azure Key Vault Keys SDK for JavaScript (@azure/keyvault-keys). Use when creating, encrypting/decrypting, signing, or rotating keys. |
| [azure-keyvault-py](.archived/skills/azure-sdks/azure-keyvault-py/SKILL.md) | Azure Key Vault secrets/keys |
| [azure-keyvault-secrets-rust](.archived/skills/azure-sdks/azure-keyvault-secrets-rust/SKILL.md) | Azure Key Vault Secrets SDK for Rust. Use for storing and retrieving secrets, passwords, and API keys. Triggers: "keyvault secrets rust", "SecretClient rust", "get secret rust", "set secret rust". |
| [azure-keyvault-secrets-ts](.archived/skills/azure-sdks/azure-keyvault-secrets-ts/SKILL.md) | Manage secrets using Azure Key Vault Secrets SDK for JavaScript (@azure/keyvault-secrets). Use when storing and retrieving application secrets or configuration values. |
| [azure-maps-search-dotnet](.archived/skills/azure-sdks/azure-maps-search-dotnet/SKILL.md) | Azure Maps SDK for .NET. Location-based services including geocoding, routing, rendering, geolocation, and weather. Use for address search, directions, map tiles, IP geolocation, and weather data. |
| [azure-messaging-webpubsub-java](.archived/skills/azure-sdks/azure-messaging-webpubsub-java/SKILL.md) | Build real-time web applications with Azure Web PubSub SDK for Java. Use when implementing WebSocket-based messaging, live updates, chat applications, or server-to-client push notifications. |
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
| [azure-postgres-ts](.archived/skills/azure-sdks/azure-postgres-ts/SKILL.md) | Connect to Azure Database for PostgreSQL Flexible Server from Node.js/TypeScript using the pg (node-postgres) package. |
| [azure-resource-manager-cosmosdb-dotnet](.archived/skills/azure-sdks/azure-resource-manager-cosmosdb-dotnet/SKILL.md) | Azure Resource Manager SDK for Cosmos DB in .NET. |
| [azure-resource-manager-durabletask-dotnet](.archived/skills/azure-sdks/azure-resource-manager-durabletask-dotnet/SKILL.md) | Azure Resource Manager SDK for Durable Task Scheduler in .NET. |
| [azure-resource-manager-mysql-dotnet](.archived/skills/azure-sdks/azure-resource-manager-mysql-dotnet/SKILL.md) | Azure MySQL Flexible Server SDK for .NET. Database management for MySQL Flexible Server deployments. |
| [azure-resource-manager-playwright-dotnet](.archived/skills/azure-sdks/azure-resource-manager-playwright-dotnet/SKILL.md) | Azure Resource Manager SDK for Microsoft Playwright Testing in .NET. |
| [azure-resource-manager-postgresql-dotnet](.archived/skills/azure-sdks/azure-resource-manager-postgresql-dotnet/SKILL.md) | Azure PostgreSQL Flexible Server SDK for .NET. Database management for PostgreSQL Flexible Server deployments. |
| [azure-resource-manager-redis-dotnet](.archived/skills/azure-sdks/azure-resource-manager-redis-dotnet/SKILL.md) | Azure Resource Manager SDK for Redis in .NET. |
| [azure-resource-manager-sql-dotnet](.archived/skills/azure-sdks/azure-resource-manager-sql-dotnet/SKILL.md) | Azure Resource Manager SDK for Azure SQL in .NET. |
| [azure-search-documents-dotnet](.archived/skills/azure-sdks/azure-search-documents-dotnet/SKILL.md) | Azure AI Search SDK for .NET (Azure.Search.Documents). Use for building search applications with full-text, vector, semantic, and hybrid search. |
| [azure-search-documents-py](.archived/skills/azure-sdks/azure-search-documents-py/SKILL.md) | Azure AI Search (vector, hybrid, semantic) |
| [azure-search-documents-ts](.archived/skills/azure-sdks/azure-search-documents-ts/SKILL.md) | Build search applications with vector, hybrid, and semantic search capabilities. |
| [azure-security-keyvault-keys-dotnet](.archived/skills/azure-sdks/azure-security-keyvault-keys-dotnet/SKILL.md) | Azure Key Vault Keys SDK for .NET. Client library for managing cryptographic keys in Azure Key Vault and Managed HSM. Use for key creation, rotation, encryption, decryption, signing, and verification. |
| [azure-security-keyvault-keys-java](.archived/skills/azure-sdks/azure-security-keyvault-keys-java/SKILL.md) | Azure Key Vault Keys Java SDK for cryptographic key management. Use when creating, managing, or using RSA/EC keys, performing encrypt/decrypt/sign/verify operations, or working with HSM-backed keys. |
| [azure-security-keyvault-secrets-java](.archived/skills/azure-sdks/azure-security-keyvault-secrets-java/SKILL.md) | Azure Key Vault Secrets Java SDK for secret management. Use when storing, retrieving, or managing passwords, API keys, connection strings, or other sensitive configuration data. |
| [azure-servicebus-dotnet](.archived/skills/azure-sdks/azure-servicebus-dotnet/SKILL.md) | Azure Service Bus SDK for .NET. Enterprise messaging with queues, topics, subscriptions, and sessions. |
| [azure-servicebus-py](.archived/skills/azure-sdks/azure-servicebus-py/SKILL.md) | Azure Service Bus messaging |
| [azure-servicebus-ts](.archived/skills/azure-sdks/azure-servicebus-ts/SKILL.md) | Enterprise messaging with queues, topics, and subscriptions. |
| [azure-speech-to-text-rest-py](.archived/skills/azure-sdks/azure-speech-to-text-rest-py/SKILL.md) | Azure Speech to Text REST API for short audio (Python). Use for simple speech recognition of audio files up to 60 seconds without the Speech SDK. |
| [azure-storage-blob-java](.archived/skills/azure-sdks/azure-storage-blob-java/SKILL.md) | Build blob storage applications using the Azure Storage Blob SDK for Java. |
| [azure-storage-blob-py](.archived/skills/azure-sdks/azure-storage-blob-py/SKILL.md) | Azure Blob Storage for Python |
| [azure-storage-blob-rust](.archived/skills/azure-sdks/azure-storage-blob-rust/SKILL.md) | Azure Blob Storage SDK for Rust. Use for uploading, downloading, and managing blobs and containers. |
| [azure-storage-blob-ts](.archived/skills/azure-sdks/azure-storage-blob-ts/SKILL.md) | Azure Blob Storage JavaScript/TypeScript SDK (@azure/storage-blob) for blob operations. Use for uploading, downloading, listing, and managing blobs and containers. |
| [azure-storage-file-datalake-py](.archived/skills/azure-sdks/azure-storage-file-datalake-py/SKILL.md) | Azure Data Lake Storage Gen2 SDK for Python. Use for hierarchical file systems, big data analytics, and file/directory operations. |
| [azure-storage-file-share-py](.archived/skills/azure-sdks/azure-storage-file-share-py/SKILL.md) | Azure Storage File Share SDK for Python. Use for SMB file shares, directories, and file operations in the cloud. |
| [azure-storage-file-share-ts](.archived/skills/azure-sdks/azure-storage-file-share-ts/SKILL.md) | Azure File Share JavaScript/TypeScript SDK (@azure/storage-file-share) for SMB file share operations. |
| [azure-storage-queue-py](.archived/skills/azure-sdks/azure-storage-queue-py/SKILL.md) | Azure Queue Storage SDK for Python. Use for reliable message queuing, task distribution, and asynchronous processing. |
| [azure-storage-queue-ts](.archived/skills/azure-sdks/azure-storage-queue-ts/SKILL.md) | Azure Queue Storage JavaScript/TypeScript SDK (@azure/storage-queue) for message queue operations. Use for sending, receiving, peeking, and deleting messages in queues. |
| [azure-web-pubsub-ts](.archived/skills/azure-sdks/azure-web-pubsub-ts/SKILL.md) | Real-time messaging with WebSocket connections and pub/sub patterns. |
| [cloud-penetration-testing](.archived/skills/azure-sdks/cloud-penetration-testing/SKILL.md) | Conduct comprehensive security assessments of cloud infrastructure across Microsoft Azure, Amazon Web Services (AWS), and Google Cloud Platform (GCP). |
| [cost-optimization](.archived/skills/azure-sdks/cost-optimization/SKILL.md) | Strategies and patterns for optimizing cloud costs across AWS, Azure, and GCP. |
| [database-cloud-optimization-cost-optimize](.archived/skills/azure-sdks/database-cloud-optimization-cost-optimize/SKILL.md) | You are a cloud cost optimization expert specializing in reducing infrastructure expenses while maintaining performance and reliability. Analyze cloud spending, identify savings opportunities, and implement cost-effective architectures across AWS, Azure, and GCP. |
| [hosted-agents-v2-py](.archived/skills/azure-sdks/hosted-agents-v2-py/SKILL.md) | Build hosted agents using Azure AI Projects SDK with ImageBasedHostedAgentDefinition. Use when creating container-based agents in Azure AI Foundry. |
| [hybrid-cloud-architect](.archived/skills/azure-sdks/hybrid-cloud-architect/SKILL.md) | Expert hybrid cloud architect specializing in complex multi-cloud solutions across AWS/Azure/GCP and private clouds (OpenStack/VMware). |
| [microsoft-azure-webjobs-extensions-authentication-events-dotnet](.archived/skills/azure-sdks/microsoft-azure-webjobs-extensions-authentication-events-dotnet/SKILL.md) | Microsoft Entra Authentication Events SDK for .NET. Azure Functions triggers for custom authentication extensions. |
| [multi-cloud-architecture](.archived/skills/azure-sdks/multi-cloud-architecture/SKILL.md) | Decision framework and patterns for architecting applications across AWS, Azure, and GCP. |
| [podcast-generation](.archived/skills/azure-sdks/podcast-generation/SKILL.md) | Generate real audio narratives from text content using Azure OpenAI's Realtime API. |
| [skill-creator-ms](.archived/skills/azure-sdks/skill-creator-ms/SKILL.md) | Guide for creating effective skills for AI coding agents working with Azure SDKs and Microsoft Foundry services. Use when creating new skills or updating existing skills. |
| [terraform-module-library](.archived/skills/azure-sdks/terraform-module-library/SKILL.md) | Production-ready Terraform module patterns for AWS, Azure, and GCP infrastructure. |

</details>

### 🎮 Game Development

<details>
<summary><b>🎮 Game Development (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [bevy-ecs-expert](.archived/skills/game-development/bevy-ecs-expert/SKILL.md) | Bevy ECS in Rust |
| [game-development](.archived/skills/game-development/game-development/SKILL.md) | Game dev orchestrator |
| [godot-gdscript-patterns](.archived/skills/game-development/godot-gdscript-patterns/SKILL.md) | Godot 4 GDScript patterns |
| [unity-developer](.archived/skills/game-development/unity-developer/SKILL.md) | Unity 6 LTS, URP/HDRP |
| [unreal-engine-cpp-pro](.archived/skills/game-development/unreal-engine-cpp-pro/SKILL.md) | Unreal Engine 5 C++ |

</details>

### 🛠️ Workflow & Automation Platforms

<details>
<summary><b>🛠️ Workflow & Automation Platforms (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [activecampaign-automation](.archived/skills/workflow-automation-platforms/activecampaign-automation/SKILL.md) | Automate ActiveCampaign tasks via Rube MCP (Composio): manage contacts, tags, list subscriptions, automation enrollment, and tasks. Always search tools first for current schemas. |
| [amplitude-automation](.archived/skills/workflow-automation-platforms/amplitude-automation/SKILL.md) | Automate Amplitude tasks via Rube MCP (Composio): events, user activity, cohorts, user identification. Always search tools first for current schemas. |
| [bamboohr-automation](.archived/skills/workflow-automation-platforms/bamboohr-automation/SKILL.md) | Automate BambooHR tasks via Rube MCP (Composio): employees, time-off, benefits, dependents, employee updates. Always search tools first for current schemas. |
| [bitbucket-automation](.archived/skills/workflow-automation-platforms/bitbucket-automation/SKILL.md) | Automate Bitbucket repositories, pull requests, branches, issues, and workspace management via Rube MCP (Composio). Always search tools first for current schemas. |
| [cal-com-automation](.archived/skills/workflow-automation-platforms/cal-com-automation/SKILL.md) | Automate Cal.com tasks via Rube MCP (Composio): manage bookings, check availability, configure webhooks, and handle teams. Always search tools first for current schemas. |
| [calendly-automation](.archived/skills/workflow-automation-platforms/calendly-automation/SKILL.md) | Automate Calendly scheduling, event management, invitee tracking, availability checks, and organization administration via Rube MCP (Composio). Always search tools first for current schemas. |
| [close-automation](.archived/skills/workflow-automation-platforms/close-automation/SKILL.md) | Automate Close CRM tasks via Rube MCP (Composio): create leads, manage calls/SMS, handle tasks, and track notes. Always search tools first for current schemas. |
| [confluence-automation](.archived/skills/workflow-automation-platforms/confluence-automation/SKILL.md) | Automate Confluence page creation, content search, space management, labels, and hierarchy navigation via Rube MCP (Composio). Always search tools first for current schemas. |
| [convertkit-automation](.archived/skills/workflow-automation-platforms/convertkit-automation/SKILL.md) | Automate ConvertKit (Kit) tasks via Rube MCP (Composio): manage subscribers, tags, broadcasts, and broadcast stats. Always search tools first for current schemas. |
| [docusign-automation](.archived/skills/workflow-automation-platforms/docusign-automation/SKILL.md) | Automate DocuSign tasks via Rube MCP (Composio): templates, envelopes, signatures, document management. Always search tools first for current schemas. |
| [dropbox-automation](.archived/skills/workflow-automation-platforms/dropbox-automation/SKILL.md) | Automate Dropbox file management, sharing, search, uploads, downloads, and folder operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [freshdesk-automation](.archived/skills/workflow-automation-platforms/freshdesk-automation/SKILL.md) | Automate Freshdesk helpdesk operations including tickets, contacts, companies, notes, and replies via Rube MCP (Composio). Always search tools first for current schemas. |
| [freshservice-automation](.archived/skills/workflow-automation-platforms/freshservice-automation/SKILL.md) | Automate Freshservice ITSM tasks via Rube MCP (Composio): create/update tickets, bulk operations, service requests, and outbound emails. Always search tools first for current schemas. |
| [helpdesk-automation](.archived/skills/workflow-automation-platforms/helpdesk-automation/SKILL.md) | Automate HelpDesk tasks via Rube MCP (Composio): list tickets, manage views, use canned responses, and configure custom fields. Always search tools first for current schemas. |
| [inngest](.archived/skills/workflow-automation-platforms/inngest/SKILL.md) | Durable background processing |
| [instagram-automation](.archived/skills/workflow-automation-platforms/instagram-automation/SKILL.md) | Automate Instagram tasks via Rube MCP (Composio): create posts, carousels, manage media, get insights, and publishing limits. Always search tools first for current schemas. |
| [intercom-automation](.archived/skills/workflow-automation-platforms/intercom-automation/SKILL.md) | Automate Intercom tasks via Rube MCP (Composio): conversations, contacts, companies, segments, admins. Always search tools first for current schemas. |
| [klaviyo-automation](.archived/skills/workflow-automation-platforms/klaviyo-automation/SKILL.md) | Automate Klaviyo tasks via Rube MCP (Composio): manage email/SMS campaigns, inspect campaign messages, track tags, and monitor send jobs. Always search tools first for current schemas. |
| [make-automation](.archived/skills/workflow-automation-platforms/make-automation/SKILL.md) | Automate Make (Integromat) tasks via Rube MCP (Composio): operations, enums, language and timezone lookups. Always search tools first for current schemas. |
| [makepad-animation](.archived/skills/workflow-automation-platforms/makepad-animation/SKILL.md) | | |
| [makepad-basics](.archived/skills/workflow-automation-platforms/makepad-basics/SKILL.md) | | |
| [makepad-deployment](.archived/skills/workflow-automation-platforms/makepad-deployment/SKILL.md) | | |
| [makepad-dsl](.archived/skills/workflow-automation-platforms/makepad-dsl/SKILL.md) | | |
| [makepad-event-action](.archived/skills/workflow-automation-platforms/makepad-event-action/SKILL.md) | | |
| [makepad-font](.archived/skills/workflow-automation-platforms/makepad-font/SKILL.md) | | |
| [makepad-layout](.archived/skills/workflow-automation-platforms/makepad-layout/SKILL.md) | | |
| [makepad-platform](.archived/skills/workflow-automation-platforms/makepad-platform/SKILL.md) | | |
| [makepad-shaders](.archived/skills/workflow-automation-platforms/makepad-shaders/SKILL.md) | | |
| [makepad-splash](.archived/skills/workflow-automation-platforms/makepad-splash/SKILL.md) | | |
| [makepad-widgets](.archived/skills/workflow-automation-platforms/makepad-widgets/SKILL.md) | Version: makepad-widgets (dev branch) | Last Updated: 2026-01-19 > > Check for updates: https://crates.io/crates/makepad-widgets |
| [microsoft-teams-automation](.archived/skills/workflow-automation-platforms/microsoft-teams-automation/SKILL.md) | Automate Microsoft Teams tasks via Rube MCP (Composio): send messages, manage channels, create meetings, handle chats, and search messages. Always search tools first for current schemas. |
| [miro-automation](.archived/skills/workflow-automation-platforms/miro-automation/SKILL.md) | Automate Miro tasks via Rube MCP (Composio): boards, items, sticky notes, frames, sharing, connectors. Always search tools first for current schemas. |
| [monday-automation](.archived/skills/workflow-automation-platforms/monday-automation/SKILL.md) | Automate Monday.com work management including boards, items, columns, groups, subitems, and updates via Rube MCP (Composio). Always search tools first for current schemas. |
| [n8n-code-javascript](.archived/skills/workflow-automation-platforms/n8n-code-javascript/SKILL.md) | JavaScript in n8n Code nodes |
| [n8n-code-python](.archived/skills/workflow-automation-platforms/n8n-code-python/SKILL.md) | Python in n8n Code nodes |
| [n8n-workflow-patterns](.archived/skills/workflow-automation-platforms/n8n-workflow-patterns/SKILL.md) | n8n workflow architecture patterns |
| [one-drive-automation](.archived/skills/workflow-automation-platforms/one-drive-automation/SKILL.md) | Automate OneDrive file management, search, uploads, downloads, sharing, permissions, and folder operations via Rube MCP (Composio). Always search tools first for current schemas. |
| [outlook-automation](.archived/skills/workflow-automation-platforms/outlook-automation/SKILL.md) | Automate Outlook tasks via Rube MCP (Composio): emails, calendar, contacts, folders, attachments. Always search tools first for current schemas. |
| [outlook-calendar-automation](.archived/skills/workflow-automation-platforms/outlook-calendar-automation/SKILL.md) | Automate Outlook Calendar tasks via Rube MCP (Composio): create events, manage attendees, find meeting times, and handle invitations. Always search tools first for current schemas. |
| [pagerduty-automation](.archived/skills/workflow-automation-platforms/pagerduty-automation/SKILL.md) | Automate PagerDuty tasks via Rube MCP (Composio): manage incidents, services, schedules, escalation policies, and on-call rotations. Always search tools first for current schemas. |
| [pipedrive-automation](.archived/skills/workflow-automation-platforms/pipedrive-automation/SKILL.md) | Automate Pipedrive CRM operations including deals, contacts, organizations, activities, notes, and pipeline management via Rube MCP (Composio). Always search tools first for current schemas. |
| [postmark-automation](.archived/skills/workflow-automation-platforms/postmark-automation/SKILL.md) | Automate Postmark email delivery tasks via Rube MCP (Composio): send templated emails, manage templates, monitor delivery stats and bounces. Always search tools first for current schemas. |
| [reddit-automation](.archived/skills/workflow-automation-platforms/reddit-automation/SKILL.md) | Automate Reddit tasks via Rube MCP (Composio): search subreddits, create posts, manage comments, and browse top content. Always search tools first for current schemas. |
| [segment-automation](.archived/skills/workflow-automation-platforms/segment-automation/SKILL.md) | Automate Segment tasks via Rube MCP (Composio): track events, identify users, manage groups, page views, aliases, batch operations. Always search tools first for current schemas. |
| [square-automation](.archived/skills/workflow-automation-platforms/square-automation/SKILL.md) | Automate Square tasks via Rube MCP (Composio): payments, orders, invoices, locations. Always search tools first for current schemas. |
| [telegram-automation](.archived/skills/workflow-automation-platforms/telegram-automation/SKILL.md) | Automate Telegram tasks via Rube MCP (Composio): send messages, manage chats, share photos/documents, and handle bot commands. Always search tools first for current schemas. |
| [temporal-python-pro](.archived/skills/workflow-automation-platforms/temporal-python-pro/SKILL.md) | Temporal workflow orchestration |
| [trigger-dev](.archived/skills/workflow-automation-platforms/trigger-dev/SKILL.md) | Background jobs with Trigger.dev |
| [twitter-automation](.archived/skills/workflow-automation-platforms/twitter-automation/SKILL.md) | Automate Twitter/X tasks via Rube MCP (Composio): posts, search, users, bookmarks, lists, media. Always search tools first for current schemas. |
| [webflow-automation](.archived/skills/workflow-automation-platforms/webflow-automation/SKILL.md) | Automate Webflow CMS collections, site publishing, page management, asset uploads, and ecommerce orders via Rube MCP (Composio). Always search tools first for current schemas. |
| [workflow-automation](.archived/skills/workflow-automation-platforms/workflow-automation/SKILL.md) | Workflow automation architecture |
| [zapier-make-patterns](.archived/skills/workflow-automation-platforms/zapier-make-patterns/SKILL.md) | No-code Zapier/Make automations |
| [zoho-crm-automation](.archived/skills/workflow-automation-platforms/zoho-crm-automation/SKILL.md) | Automate Zoho CRM tasks via Rube MCP (Composio): create/update records, search contacts, manage leads, and convert leads. Always search tools first for current schemas. |

</details>

### 💳 Payments & Billing

<details>
<summary><b>💳 Payments & Billing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [billing-automation](.archived/skills/payments-billing/billing-automation/SKILL.md) | Recurring billing, invoicing, dunning |
| [payment-integration](.archived/skills/payments-billing/payment-integration/SKILL.md) | Stripe, PayPal, PCI compliance |
| [paypal-integration](.archived/skills/payments-billing/paypal-integration/SKILL.md) | PayPal checkout, IPN, recurring billing |
| [stripe-integration](.archived/skills/payments-billing/stripe-integration/SKILL.md) | Stripe checkout, subscriptions, webhooks |

</details>

### 🌍 Blockchain & Web3

<details>
<summary><b>🌍 Blockchain & Web3 (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [blockchain-developer](.archived/skills/blockchain-web3/blockchain-developer/SKILL.md) | Smart contracts, DeFi, NFTs, DAOs |
| [nft-standards](.archived/skills/blockchain-web3/nft-standards/SKILL.md) | ERC-721, ERC-1155 best practices |
| [solidity-security](.archived/skills/blockchain-web3/solidity-security/SKILL.md) | Smart contract security patterns |
| [web3-testing](.archived/skills/blockchain-web3/web3-testing/SKILL.md) | Hardhat, Foundry testing strategies |

</details>

### 🧬 Scientific Computing

<details>
<summary><b>🧬 Scientific Computing (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [astropy](.archived/skills/scientific-computing/astropy/SKILL.md) | Astronomy research with Python |
| [biopython](.archived/skills/scientific-computing/biopython/SKILL.md) | Biological computation tools |
| [matplotlib](.archived/skills/scientific-computing/matplotlib/SKILL.md) | Python visualization |
| [networkx](.archived/skills/scientific-computing/networkx/SKILL.md) | Complex network analysis |
| [plotly](.archived/skills/scientific-computing/plotly/SKILL.md) | Interactive visualizations |
| [qiskit](.archived/skills/scientific-computing/qiskit/SKILL.md) | Quantum computing framework |
| [scanpy](.archived/skills/scientific-computing/scanpy/SKILL.md) | Single-cell RNA-seq analysis |
| [sympy](.archived/skills/scientific-computing/sympy/SKILL.md) | Symbolic mathematics |

</details>

### 📦 Miscellaneous / Other

<details>
<summary><b>📦 Miscellaneous / Other (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [SPDD](.archived/skills/miscellaneous-other/SPDD/SKILL.md) | Spdd |
| [acceptance-orchestrator](.archived/skills/miscellaneous-other/acceptance-orchestrator/SKILL.md) | Use when a coding task should be driven end-to-end from issue intake through implementation, review, deployment, and acceptance verification with minimal human re-intervention. |
| [arm-cortex-expert](.archived/skills/miscellaneous-other/arm-cortex-expert/SKILL.md) | Senior embedded software engineer specializing in firmware and driver development for ARM Cortex-M microcontrollers (Teensy, STM32, nRF52, SAMD). |
| [aws-compliance-checker](.archived/skills/miscellaneous-other/aws-compliance-checker/SKILL.md) | Automated compliance checking against CIS, PCI-DSS, HIPAA, and SOC 2 benchmarks |
| [aws-iam-best-practices](.archived/skills/miscellaneous-other/aws-iam-best-practices/SKILL.md) | IAM policy review, hardening, and least privilege implementation |
| [aws-secrets-rotation](.archived/skills/miscellaneous-other/aws-secrets-rotation/SKILL.md) | Automate AWS secrets rotation for RDS, API keys, and credentials |
| [aws-security-audit](.archived/skills/miscellaneous-other/aws-security-audit/SKILL.md) | Comprehensive AWS security posture assessment using AWS CLI and security best practices |
| [blockrun](.archived/skills/miscellaneous-other/blockrun/SKILL.md) | BlockRun works with Claude Code and Google Antigravity. |
| [c4-context](.archived/skills/miscellaneous-other/c4-context/SKILL.md) | Expert C4 Context-level documentation specialist. Creates high-level system context diagrams, documents personas, user journeys, system features, and external dependencies. |
| [cc-skill-continuous-learning](.archived/skills/miscellaneous-other/cc-skill-continuous-learning/SKILL.md) | Development skill from everything-claude-code |
| [cc-skill-strategic-compact](.archived/skills/miscellaneous-other/cc-skill-strategic-compact/SKILL.md) | Development skill from everything-claude-code |
| [clarity-gate](.archived/skills/miscellaneous-other/clarity-gate/SKILL.md) | > |
| [claude-scientific-skills](.archived/skills/miscellaneous-other/claude-scientific-skills/SKILL.md) | Scientific research and analysis skills |
| [claude-win11-speckit-update-skill](.archived/skills/miscellaneous-other/claude-win11-speckit-update-skill/SKILL.md) | Windows 11 system management |
| [code-refactoring-context-restore](.archived/skills/miscellaneous-other/code-refactoring-context-restore/SKILL.md) | Use when working with code refactoring context restore |
| [computer-vision-expert](.archived/skills/miscellaneous-other/computer-vision-expert/SKILL.md) | SOTA Computer Vision Expert (2026). Specialized in YOLO26, Segment Anything 3 (SAM 3), Vision Language Models, and real-time spatial analysis. |
| [concise-planning](.archived/skills/miscellaneous-other/concise-planning/SKILL.md) | Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist. |
| [conductor-implement](.archived/skills/miscellaneous-other/conductor-implement/SKILL.md) | Execute tasks from a track's implementation plan following TDD workflow |
| [conductor-manage](.archived/skills/miscellaneous-other/conductor-manage/SKILL.md) | Manage track lifecycle: archive, restore, delete, rename, and cleanup |
| [conductor-new-track](.archived/skills/miscellaneous-other/conductor-new-track/SKILL.md) | Create a new track with specification and phased implementation plan |
| [context-management-context-restore](.archived/skills/miscellaneous-other/context-management-context-restore/SKILL.md) | Use when working with context management context restore |
| [context-management-context-save](.archived/skills/miscellaneous-other/context-management-context-save/SKILL.md) | Use when working with context management context save |
| [create-issue-gate](.archived/skills/miscellaneous-other/create-issue-gate/SKILL.md) | Use when starting a new implementation task and an issue must be created with strict acceptance criteria gating before execution. |
| [customs-trade-compliance](.archived/skills/miscellaneous-other/customs-trade-compliance/SKILL.md) | Codified expertise for customs documentation, tariff classification, duty optimisation, restricted party screening, and regulatory compliance across multiple jurisdictions. |
| [distributed-tracing](.archived/skills/miscellaneous-other/distributed-tracing/SKILL.md) | Implement distributed tracing with Jaeger and Tempo for request flow visibility across microservices. |
| [emergency-card](.archived/skills/miscellaneous-other/emergency-card/SKILL.md) | 生成紧急情况下快速访问的医疗信息摘要卡片。当用户需要旅行、就诊准备、紧急情况或询问"紧急信息"、"医疗卡片"、"急救信息"时使用此技能。提取关键信息（过敏、用药、急症、植入物），支持多格式输出（JSON、文本、二维码），用于急救或快速就医。 |
| [executing-plans](.archived/skills/miscellaneous-other/executing-plans/SKILL.md) | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| [family-health-analyzer](.archived/skills/miscellaneous-other/family-health-analyzer/SKILL.md) | 分析家族病史、评估遗传风险、识别家庭健康模式、提供个性化预防建议 |
| [favicon](.archived/skills/miscellaneous-other/favicon/SKILL.md) | Generate favicons from a source image |
| [ffuf-claude-skill](.archived/skills/miscellaneous-other/ffuf-claude-skill/SKILL.md) | Web fuzzing with ffuf |
| [filesystem-context](.archived/skills/miscellaneous-other/filesystem-context/SKILL.md) | Use for file-based context management, dynamic context discovery, and reducing context window bloat. Offload context to files for just-in-time loading. |
| [fitness-analyzer](.archived/skills/miscellaneous-other/fitness-analyzer/SKILL.md) | 分析运动数据、识别运动模式、评估健身进展，并提供个性化训练建议。支持与慢性病数据的关联分析。 |
| [form-cro](.archived/skills/miscellaneous-other/form-cro/SKILL.md) | Optimize any form that is NOT signup or account registration — including lead capture, contact, demo request, application, survey, quote, and checkout forms. |
| [full-stack-orchestration-full-stack-feature](.archived/skills/miscellaneous-other/full-stack-orchestration-full-stack-feature/SKILL.md) | Use when working with full stack orchestration full stack feature |
| [goal-analyzer](.archived/skills/miscellaneous-other/goal-analyzer/SKILL.md) | 分析健康目标数据、识别目标模式、评估目标进度,并提供个性化目标管理建议。支持与营养、运动、睡眠等健康数据的关联分析。 |
| [incident-response-incident-response](.archived/skills/miscellaneous-other/incident-response-incident-response/SKILL.md) | Use when working with incident response incident response |
| [interview-coach](.archived/skills/miscellaneous-other/interview-coach/SKILL.md) | Full job search coaching system — JD decoding, resume, storybank, mock interviews, transcript analysis, comp negotiation. 23 commands, persistent state. |
| [keyword-extractor](.archived/skills/miscellaneous-other/keyword-extractor/SKILL.md) | > |
| [legacy-modernizer](.archived/skills/miscellaneous-other/legacy-modernizer/SKILL.md) | Refactor legacy codebases, migrate outdated frameworks, and implement gradual modernization. Handles technical debt, dependency updates, and backward compatibility. |
| [lex](.archived/skills/miscellaneous-other/lex/SKILL.md) | Centralized 'Truth Engine' for cross-jurisdictional legal context (US, EU, CA) and contract scaffolding. |
| [libreoffice-base](.archived/skills/miscellaneous-other/libreoffice-base/SKILL.md) | Database management, forms, reports, and data operations with LibreOffice Base. |
| [libreoffice-calc](.archived/skills/miscellaneous-other/libreoffice-calc/SKILL.md) | Spreadsheet creation, format conversion (ODS/XLSX/CSV), formulas, data automation with LibreOffice Calc. |
| [libreoffice-draw](.archived/skills/miscellaneous-other/libreoffice-draw/SKILL.md) | Vector graphics and diagram creation, format conversion (ODG/SVG/PDF) with LibreOffice Draw. |
| [libreoffice-impress](.archived/skills/miscellaneous-other/libreoffice-impress/SKILL.md) | Presentation creation, format conversion (ODP/PPTX/PDF), slide automation with LibreOffice Impress. |
| [libreoffice-writer](.archived/skills/miscellaneous-other/libreoffice-writer/SKILL.md) | Document creation, format conversion (ODT/DOCX/PDF), mail merge, and automation with LibreOffice Writer. |
| [linear](.archived/skills/miscellaneous-other/linear/SKILL.md) | Linear |
| [mental-health-analyzer](.archived/skills/miscellaneous-other/mental-health-analyzer/SKILL.md) | 分析心理健康数据、识别心理模式、评估心理健康状况、提供个性化心理健康建议。支持与睡眠、运动、营养等其他健康数据的关联分析。 |
| [molykit](.archived/skills/miscellaneous-other/molykit/SKILL.md) | | |
| [moyu](.archived/skills/miscellaneous-other/moyu/SKILL.md) | > |
| [notebooklm](.archived/skills/miscellaneous-other/notebooklm/SKILL.md) | Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes. |
| [nutrition-analyzer](.archived/skills/miscellaneous-other/nutrition-analyzer/SKILL.md) | 分析营养数据、识别营养模式、评估营养状况，并提供个性化营养建议。支持与运动、睡眠、慢性病数据的关联分析。 |
| [occupational-health-analyzer](.archived/skills/miscellaneous-other/occupational-health-analyzer/SKILL.md) | 分析职业健康数据、识别工作相关健康风险、评估职业健康状况、提供个性化职业健康建议。支持与睡眠、运动、心理健康等其他健康数据的关联分析。 |
| [odoo-l10n-compliance](.archived/skills/miscellaneous-other/odoo-l10n-compliance/SKILL.md) | Country-specific Odoo localization: tax configuration, e-invoicing (CFDI, FatturaPA, SAF-T), fiscal reporting, and country chart of accounts setup. |
| [oral-health-analyzer](.archived/skills/miscellaneous-other/oral-health-analyzer/SKILL.md) | 分析口腔健康数据、识别口腔问题模式、评估口腔健康状况、提供个性化口腔健康建议。支持与营养、慢性病、用药等其他健康数据的关联分析。 |
| [orchestrate-batch-refactor](.archived/skills/miscellaneous-other/orchestrate-batch-refactor/SKILL.md) | Plan and execute large refactors with dependency-aware work packets and parallel analysis. |
| [oss-hunter](.archived/skills/miscellaneous-other/oss-hunter/SKILL.md) | Automatically hunt for high-impact OSS contribution opportunities in trending repositories. |
| [page-cro](.archived/skills/miscellaneous-other/page-cro/SKILL.md) | Analyze and optimize individual pages for conversion performance. |
| [performance-engineer](.archived/skills/miscellaneous-other/performance-engineer/SKILL.md) | Expert performance engineer specializing in modern observability, |
| [plan-writing](.archived/skills/miscellaneous-other/plan-writing/SKILL.md) | Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work. |
| [quality-nonconformance](.archived/skills/miscellaneous-other/quality-nonconformance/SKILL.md) | Codified expertise for quality control, non-conformance investigation, root cause analysis, corrective action, and supplier quality management in regulated manufacturing. |
| [rehabilitation-analyzer](.archived/skills/miscellaneous-other/rehabilitation-analyzer/SKILL.md) | 分析康复训练数据、识别康复模式、评估康复进展，并提供个性化康复建议 |
| [risk-manager](.archived/skills/miscellaneous-other/risk-manager/SKILL.md) | Monitor portfolio risk, R-multiples, and position limits. Creates hedging strategies, calculates expectancy, and implements stop-losses. |
| [robius-event-action](.archived/skills/miscellaneous-other/robius-event-action/SKILL.md) | | |
| [robius-matrix-integration](.archived/skills/miscellaneous-other/robius-matrix-integration/SKILL.md) | | |
| [robius-state-management](.archived/skills/miscellaneous-other/robius-state-management/SKILL.md) | | |
| [search-specialist](.archived/skills/miscellaneous-other/search-specialist/SKILL.md) | Expert web researcher using advanced search techniques and |
| [sexual-health-analyzer](.archived/skills/miscellaneous-other/sexual-health-analyzer/SKILL.md) | Sexual Health Analyzer |
| [sharp-edges](.archived/skills/miscellaneous-other/sharp-edges/SKILL.md) | sharp-edges |
| [shellcheck-configuration](.archived/skills/miscellaneous-other/shellcheck-configuration/SKILL.md) | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script portability. |
| [signup-flow-cro](.archived/skills/miscellaneous-other/signup-flow-cro/SKILL.md) | You are an expert in optimizing signup and registration flows. Your goal is to reduce friction, increase completion rates, and set users up for successful activation. |
| [simplify-code](.archived/skills/miscellaneous-other/simplify-code/SKILL.md) | Review a diff for clarity and safe simplifications, then optionally apply low-risk fixes. |
| [skill-installer](.archived/skills/miscellaneous-other/skill-installer/SKILL.md) | Instala, valida, registra e verifica novas skills no ecossistema. 10 checks de seguranca, copia, registro no orchestrator e verificacao pos-instalacao. |
| [skill-router](.archived/skills/miscellaneous-other/skill-router/SKILL.md) | Use when the user is unsure which skill to use or where to start. Interviews the user with targeted questions and recommends the best skill(s) from the installed library for their goal. |
| [sleep-analyzer](.archived/skills/miscellaneous-other/sleep-analyzer/SKILL.md) | 分析睡眠数据、识别睡眠模式、评估睡眠质量，并提供个性化睡眠改善建议。支持与其他健康数据的关联分析。 |
| [slo-implementation](.archived/skills/miscellaneous-other/slo-implementation/SKILL.md) | Framework for defining and implementing Service Level Indicators (SLIs), Service Level Objectives (SLOs), and error budgets. |
| [speckit-updater](.archived/skills/miscellaneous-other/speckit-updater/SKILL.md) | SpecKit Safe Update |
| [speed](.archived/skills/miscellaneous-other/speed/SKILL.md) | Launch RSVP speed reader for text |
| [superpowers-lab](.archived/skills/miscellaneous-other/superpowers-lab/SKILL.md) | Lab environment for Claude superpowers |
| [tcm-constitution-analyzer](.archived/skills/miscellaneous-other/tcm-constitution-analyzer/SKILL.md) | 分析中医体质数据、识别体质类型、评估体质特征,并提供个性化养生建议。支持与营养、运动、睡眠等健康数据的关联分析。 |
| [tdd-workflows-tdd-cycle](.archived/skills/miscellaneous-other/tdd-workflows-tdd-cycle/SKILL.md) | Use when working with tdd workflows tdd cycle |
| [tdd-workflows-tdd-refactor](.archived/skills/miscellaneous-other/tdd-workflows-tdd-refactor/SKILL.md) | Use when working with tdd workflows tdd refactor |
| [threejs-fundamentals](.archived/skills/miscellaneous-other/threejs-fundamentals/SKILL.md) | Three.js scene setup, cameras, renderer, Object3D hierarchy, coordinate systems. Use when setting up 3D scenes, creating cameras, configuring renderers, managing object hierarchies, or working with transforms. |
| [threejs-interaction](.archived/skills/miscellaneous-other/threejs-interaction/SKILL.md) | Three.js interaction - raycasting, controls, mouse/touch input, object selection. Use when handling user input, implementing click detection, adding camera controls, or creating interactive 3D experiences. |
| [threejs-lighting](.archived/skills/miscellaneous-other/threejs-lighting/SKILL.md) | Three.js lighting - light types, shadows, environment lighting. Use when adding lights, configuring shadows, setting up IBL, or optimizing lighting performance. |
| [threejs-textures](.archived/skills/miscellaneous-other/threejs-textures/SKILL.md) | Three.js textures - texture types, UV mapping, environment maps, texture settings. Use when working with images, UV coordinates, cubemaps, HDR environments, or texture optimization. |
| [track-management](.archived/skills/miscellaneous-other/track-management/SKILL.md) | Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Applies to spec.md, plan.md, and track lifecycle operations. |
| [travel-health-analyzer](.archived/skills/miscellaneous-other/travel-health-analyzer/SKILL.md) | 分析旅行健康数据、评估目的地健康风险、提供疫苗接种建议、生成多语言紧急医疗信息卡片。支持WHO/CDC数据集成的专业级旅行健康风险评估。 |
| [twilio-communications](.archived/skills/miscellaneous-other/twilio-communications/SKILL.md) | Basic pattern for sending SMS messages with Twilio. Handles the fundamentals: phone number formatting, message delivery, and delivery status callbacks. |
| [upgrading-expo](.archived/skills/miscellaneous-other/upgrading-expo/SKILL.md) | Upgrade Expo SDK versions |
| [varlock](.archived/skills/miscellaneous-other/varlock/SKILL.md) | Secure-by-default environment variable management for Claude Code sessions. |
| [vector-index-tuning](.archived/skills/miscellaneous-other/vector-index-tuning/SKILL.md) | Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure. |
| [vexor](.archived/skills/miscellaneous-other/vexor/SKILL.md) | Vector-powered CLI for semantic file search with a Claude/Codex skill |
| [web-performance-optimization](.archived/skills/miscellaneous-other/web-performance-optimization/SKILL.md) | Optimize website and web application performance including loading speed, Core Web Vitals, bundle size, caching strategies, and runtime performance |
| [weightloss-analyzer](.archived/skills/miscellaneous-other/weightloss-analyzer/SKILL.md) | 分析减肥数据、计算代谢率、追踪能量缺口、管理减肥阶段 |
| [windows-shell-reliability](.archived/skills/miscellaneous-other/windows-shell-reliability/SKILL.md) | Reliable command execution on Windows: paths, encoding, and common binary pitfalls. |
| [x-article-publisher-skill](.archived/skills/miscellaneous-other/x-article-publisher-skill/SKILL.md) | Publish articles to X/Twitter |
| [xlsx-official](.archived/skills/miscellaneous-other/xlsx-official/SKILL.md) | Unless otherwise stated by the user or existing template |
| [yann-lecun-filosofia](.archived/skills/miscellaneous-other/yann-lecun-filosofia/SKILL.md) | Sub-skill filosófica e pedagógica de Yann LeCun. |

</details>

### 🎯 Custom Skills

<details>
<summary><b>🎯 Custom Skills (Click to expand)</b></summary>

| Skill | Description |
|---|---|
| [custom-debrief](.archived/skills/custom-skills/custom-debrief/SKILL.md) | **(Custom)** Post-mortem task breakdowns and mentor insights. |
| [custom-senior-architect](.archived/skills/custom-skills/custom-senior-architect/SKILL.md) | **(Custom)** Specialist for end-to-end technical flow mapping and sequence diagrams. |
| [custom-senior-it-ba-specialist](.archived/skills/custom-skills/custom-senior-it-ba-specialist/SKILL.md) | **(Custom)** Senior IT business analyst for technical requirements and workflow mapping. |
| [custom-video-analyst](.archived/skills/custom-skills/custom-video-analyst/SKILL.md) | **(Custom)** Expert note-taker for video/transcripts with zero technical loss. |
| [senior-architect](.archived/skills/custom-skills/senior-architect/SKILL.md) | **(Custom)** Senior architect toolkit for modern system designs. |

</details>

## Finding Skills

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
