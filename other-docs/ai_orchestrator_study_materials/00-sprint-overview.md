# 21-Day AI Orchestrator Sprint — Overview

> **Goal:** become legible to a senior/staff AI Orchestrator interviewer in 21 days. The sprint won't make you a senior engineer if you aren't already — it will surface what you already know, fill the gaps that matter for this specific role, and drill the muscle memory needed to perform under interview pressure.
>
> **Audience:** Java/Spring engineers targeting roles where the work is "build agentic AI systems on top of LLMs" — Spring AI, RAG, vector DBs, multi-tenant SaaS, observability, system design.

---

## 1. How This Material Is Organized

```
ai_orchestrator_study_materials/
├── 00-sprint-overview.md           ← you are here
├── 21-day-sprint/                  ← per-day study plans (this is what you follow)
│   ├── week-1-core-engineering/     (Days 1–5)
│   ├── week-2-security-and-ai/      (Days 6–11)
│   └── week-3-system-design-crucible/ (Days 12–21)
├── java-21-study-guide/            ← deep-dive reference docs (the syllabus)
│   ├── 01-core/   02-collections/   03-concurrency/   04-jvm/
│   ├── 05-ecosystem/   06-microservices/   07-security-and-identity/
│   ├── 08-infrastructure/   09-ai-orchestration/   10-system-design-leadership/
└── assessments/                    ← rapid-recall + scenario drills
```

**The two halves work together.** Each sprint day points to one or two syllabus deep-dives. You read the deep-dive to understand the concept; you do the day's deliverables to lock it in.

---

## 2. The 21-Day Calendar (At a Glance)

| # | Day | Topic — DSA × Engineering | Syllabus refs |
| - | --- | -------------------------- | ------------- |
| **Week 1 — Core Engineering** |
| 1 | Day 1  | Arrays × JVM Internals | [04-jvm/jvm-architecture](java-21-study-guide/04-jvm/jvm-architecture.md) |
| 2 | Day 2  | Linked Lists × Virtual Threads | [03-concurrency/multithreading](java-21-study-guide/03-concurrency/multithreading.md) |
| 3 | Day 3  | Trees × DB Optimization | [05-ecosystem/jdbc](java-21-study-guide/05-ecosystem/jdbc.md) |
| 4 | Day 4  | Graphs × Spring Internals | [05-ecosystem/spring-framework](java-21-study-guide/05-ecosystem/spring-framework.md) |
| 5 | Day 5  | Sliding Window × Resilience | [06-microservices/resilience-and-patterns](java-21-study-guide/06-microservices/resilience-and-patterns.md), [06-microservices/saga-and-comms](java-21-study-guide/06-microservices/saga-and-comms.md) |
| **Week 2 — Security & AI** |
| 6 | Day 6  | Two Pointers × OAuth/JWT | [07-security-and-identity/oauth2-and-jwt](java-21-study-guide/07-security-and-identity/oauth2-and-jwt.md) |
| 7 | Day 7  | Binary Search × Multi-Tenancy (RLS) | [07-security-and-identity/multi-tenancy](java-21-study-guide/07-security-and-identity/multi-tenancy.md) |
| 8 | Day 8  | Dynamic Programming × Containers (Podman) | [08-infrastructure/containerization](java-21-study-guide/08-infrastructure/containerization.md) |
| 9 | Day 9  | Backtracking × Observability | [08-infrastructure/observability](java-21-study-guide/08-infrastructure/observability.md) |
| 10 | Day 10 | Greedy × Spring AI tool calling | [09-ai-orchestration/spring-ai-tools](java-21-study-guide/09-ai-orchestration/spring-ai-tools.md), [09-ai-orchestration/mcp-protocol](java-21-study-guide/09-ai-orchestration/mcp-protocol.md) |
| 11 | Day 11 | Tries × Advanced RAG | [09-ai-orchestration/advanced-rag](java-21-study-guide/09-ai-orchestration/advanced-rag.md), [09-ai-orchestration/vector-db-tradeoffs](java-21-study-guide/09-ai-orchestration/vector-db-tradeoffs.md), [09-ai-orchestration/llm-evaluation](java-21-study-guide/09-ai-orchestration/llm-evaluation.md) |
| **Week 3 — System Design Crucible** |
| 12 | Day 12 | Heaps × Agentic Patterns | [09-ai-orchestration/agentic-patterns](java-21-study-guide/09-ai-orchestration/agentic-patterns.md), [09-ai-orchestration/multi-agent-patterns](java-21-study-guide/09-ai-orchestration/multi-agent-patterns.md), [09-ai-orchestration/agent-memory](java-21-study-guide/09-ai-orchestration/agent-memory.md), [09-ai-orchestration/cost-and-telemetry](java-21-study-guide/09-ai-orchestration/cost-and-telemetry.md), [09-ai-orchestration/llm-streaming](java-21-study-guide/09-ai-orchestration/llm-streaming.md) |
| 13 | Day 13 | Intervals × System Design Blueprint | [10-system-design-leadership/system-design-blueprint](java-21-study-guide/10-system-design-leadership/system-design-blueprint.md) |
| 14 | Day 14 | Coding Mock #1 + Week 2 Review | (across Week 2) |
| 15 | Day 15 | System Design Mock #1: Multi-Tenant Chatbot | [10-system-design-leadership/system-design-blueprint](java-21-study-guide/10-system-design-leadership/system-design-blueprint.md) |
| 16 | Day 16 | Spaced Review of Week 1 Topics | (across Week 1) |
| 17 | Day 17 | Coding Mock #2 + 4 STAR Stories | [10-system-design-leadership/behavioral-mastery](java-21-study-guide/10-system-design-leadership/behavioral-mastery.md) |
| 18 | Day 18 | System Design Mock #2: Enterprise RAG Search | (across week 2 + 3) |
| 19 | Day 19 | Behavioral Mock + Remaining 4 STARs + Q&A Bank | [10-system-design-leadership/behavioral-mastery](java-21-study-guide/10-system-design-leadership/behavioral-mastery.md) |
| 20 | Day 20 | Capstone Polish + Light Coding + `#weak` Sweep | (your weak-tagged topics) |
| 21 | Day 21 | Final Dry-Run + Post-Sprint Plan | (everything) |

---

## 3. The Capstone

You are designing and **incrementally building**, across the 21 days, **one anchor system** that you can defend in 60 minutes of system-design probing:

> **A multi-tenant AI chatbot SaaS platform.** 1,000 business customers, each uploading their own document corpus. Their end-customers chat with an AI widget on the business's website. The widget streams answers grounded in the tenant's documents. Strong tenant isolation. Per-tenant cost tracking. Async ingestion pipeline.

This is the "fully worked example" in [system-design-blueprint.md](java-21-study-guide/10-system-design-leadership/system-design-blueprint.md). The sprint is a controlled scaffolding of building blocks for it:

| You learn | On day | The capstone uses it for |
| --------- | ------ | ------------------------ |
| Virtual threads + structured concurrency | Day 2 | Fan-out for embedding + vector search + cache check |
| DB optimization (HikariCP, indexes, N+1) | Day 3 | The relational metadata store |
| Spring `@Transactional` + AOP proxies | Day 4 | Transactional outbox for events |
| Microservice resilience + Saga + Outbox | Day 5 | Reliable event emission for billing/memory |
| OAuth2 / JWT | Day 6 | Tenant auth via JWT claims |
| RLS multi-tenancy | Day 7 | DB-kernel tenant isolation |
| Container hardening + native image | Day 8 | Fast Cloud Run cold starts |
| Distributed tracing | Day 9 | Cross-service request correlation |
| Spring AI tool calling | Day 10 | The agent's action surface |
| Advanced RAG + pgvector + HNSW | Day 11 | The retrieval layer |
| ReAct + semantic caching | Day 12 | Agent loop + cost reduction |
| System design blueprint | Day 13 | The framework you'll use to defend it |

By Day 21 you should have, in Obsidian: (a) a **1,500-word design doc** of the capstone, iterated across Days 15/16/18/20; (b) a small **working code prototype** (pgvector + Spring Boot + a tool-calling agent + tenant isolation) — proof you actually shipped something.

---

## 4. The Daily Template

Every Week-1 and Week-2 day file follows the same shape:

1. **Timebox banner** (2.5h typical; flagged days are 2.75–3h).
2. **Algorithmic Canvas** — 1–2 LeetCode problems with: link, target Big-O, key insight in plain English, working Java skeleton, useful pattern visual, 3 follow-up variants.
3. **Engineering Deep-Dive** — pointer to the syllabus + **5 specific extraction targets** (what to pull from the read, not "read the doc") + **5 senior-style recall questions** ("your teammate said X, what's wrong?").
4. **Day Deliverables** — concrete artifacts: Java files with header comments, two 200–400-word Obsidian notes, hands-on experiments, spaced-repetition tags pointing forward to specific review days.
5. **References** — curated and grouped, no empty sections.

Week-3 day files differ — they're **practice and rehearsal**, not new material. Mock interviews, design write-ups, behavioral story drilling.

---

## 5. The Spaced-Repetition Schedule

Every topic gets revisited **at least twice** after first study. Tags in your Obsidian point forward:

| First studied | First review | Second review |
| ------------- | ------------ | ------------- |
| Day 1  | Day 8  | Day 16 |
| Day 2  | Day 9  | Day 16 |
| Day 3  | Day 11 | Day 17 |
| Day 4  | Day 11 | Day 18 |
| Day 5  | Day 12 | Day 19 |
| Day 6  | Day 13 | Day 19 |
| Day 7  | Day 14 | Day 20 |
| Day 8  | Day 15 | Day 20 |
| Day 9  | Day 16 | Day 20 |
| Day 10 | Day 17 | Day 21 |
| Day 11 | Day 18 | Day 21 |
| Day 12 | Day 19 | Day 21 |
| Day 13 | Days 14, 15, 18, 21 (the most-revisited topic by design) |

The reviews aren't passive re-reads — they're **active recall**: close the doc, answer the day's questions cold, *then* compare. Anything <80% confident gets re-tagged `#weak` and scheduled for another pass.

---

## 6. Topic → Sprint-Day Map (Reverse Index)

Use this when you want to find *where* a concept is studied.

### Java & JVM
- **JVM architecture, GC, JIT, TLABs, Safepoints** → Day 1 ([04-jvm/jvm-architecture](java-21-study-guide/04-jvm/jvm-architecture.md))
- **Garbage collection algorithms** → Day 1 ([04-jvm/garbage-collection](java-21-study-guide/04-jvm/garbage-collection.md))
- **Virtual threads, structured concurrency, pinning** → Day 2 ([03-concurrency/multithreading](java-21-study-guide/03-concurrency/multithreading.md))
- **Synchronization primitives** → Day 2 ([03-concurrency/synchronization](java-21-study-guide/03-concurrency/synchronization.md))
- **OOP fundamentals, SOLID, equals/hashCode, composition** → bonus / pre-Day 1 brush-up ([01-core/oop-fundamentals](java-21-study-guide/01-core/oop-fundamentals.md))
- **Sealed classes + Records + Pattern Matching for switch (the Java 21 trio)** → bonus ([01-core/sealed-classes](java-21-study-guide/01-core/sealed-classes.md), [01-core/records-and-pattern-matching](java-21-study-guide/01-core/records-and-pattern-matching.md))
- **Streams API + Optional** → bonus / pre-Day 3 brush-up ([02-collections/streams-api](java-21-study-guide/02-collections/streams-api.md))

### Data layer
- **JDBC, HikariCP, transactions, isolation** → Day 3 ([05-ecosystem/jdbc](java-21-study-guide/05-ecosystem/jdbc.md))
- **N+1, indexes, EXPLAIN ANALYZE** → Day 3
- **Zero-downtime migrations (Expand-and-Contract)** → Day 3

### Spring
- **IoC, AOP, bean lifecycle, `@Transactional` proxy trap** → Day 4 ([05-ecosystem/spring-framework](java-21-study-guide/05-ecosystem/spring-framework.md))
- **Caching & messaging** → cross-week ([05-ecosystem/caching-and-messaging](java-21-study-guide/05-ecosystem/caching-and-messaging.md))
- **Project Reactor & Spring WebFlux (when virtual threads aren't enough)** → bonus ([05-ecosystem/reactor-and-webflux](java-21-study-guide/05-ecosystem/reactor-and-webflux.md))

### Microservices
- **Circuit breaker, bulkhead, choreography vs orchestration Saga, Outbox+CDC** → Day 5 ([06-microservices/resilience-and-patterns](java-21-study-guide/06-microservices/resilience-and-patterns.md))
- **Sync vs async comms, Saga orchestrator at scale, AI inference Saga** → Day 5 ([06-microservices/saga-and-comms](java-21-study-guide/06-microservices/saga-and-comms.md))

### Security & identity
- **OAuth2 flows (PKCE, Client Credentials, Token Exchange)** → Day 6 ([07-security-and-identity/oauth2-and-jwt](java-21-study-guide/07-security-and-identity/oauth2-and-jwt.md))
- **JWS vs JWE vs Nested JWT** → Day 6
- **Multi-tenancy isolation (DB-per, schema-per, shared+RLS), RBAC vs ABAC** → Day 7 ([07-security-and-identity/multi-tenancy](java-21-study-guide/07-security-and-identity/multi-tenancy.md))
- **Spring Security configuration** → cross-week ([07-security-and-identity/spring-security](java-21-study-guide/07-security-and-identity/spring-security.md))

### Infrastructure
- **Multi-stage Dockerfile, jlink, container-aware JVM flags, GraalVM native image, rootless Podman** → Day 8 ([08-infrastructure/containerization](java-21-study-guide/08-infrastructure/containerization.md))
- **Distributed tracing, MDC, correlation IDs, Cloud SQL Proxy** → Day 9 ([08-infrastructure/observability](java-21-study-guide/08-infrastructure/observability.md))

### AI Orchestration (the role's surface)
- **Spring AI `@Tool`, prompt injection defense, idempotency** → Day 10 ([09-ai-orchestration/spring-ai-tools](java-21-study-guide/09-ai-orchestration/spring-ai-tools.md))
- **Model Context Protocol (MCP), JSON-RPC, MCP servers vs `@Tool`** → Day 10 ([09-ai-orchestration/mcp-protocol](java-21-study-guide/09-ai-orchestration/mcp-protocol.md))
- **Naïve RAG failures, parent-document retrieval, HNSW, hybrid search** → Day 11 ([09-ai-orchestration/advanced-rag](java-21-study-guide/09-ai-orchestration/advanced-rag.md))
- **Vector DB selection (pgvector vs Pinecone vs Qdrant), embedding dims, re-ranking** → Day 11 ([09-ai-orchestration/vector-db-tradeoffs](java-21-study-guide/09-ai-orchestration/vector-db-tradeoffs.md))
- **Eval-driven development, Ragas metrics, LLM-as-judge** → Day 11 ([09-ai-orchestration/llm-evaluation](java-21-study-guide/09-ai-orchestration/llm-evaluation.md))
- **ReAct loop, n8n orchestration, semantic caching** → Day 12 ([09-ai-orchestration/agentic-patterns](java-21-study-guide/09-ai-orchestration/agentic-patterns.md))
- **Supervisor / Hierarchical / Swarm / Plan-and-Execute** → Day 12 ([09-ai-orchestration/multi-agent-patterns](java-21-study-guide/09-ai-orchestration/multi-agent-patterns.md))
- **Short-term/long-term/episodic/procedural memory** → Day 12 ([09-ai-orchestration/agent-memory](java-21-study-guide/09-ai-orchestration/agent-memory.md))
- **Token telemetry, prompt caching, model routing, per-tenant budgets** → Day 12 ([09-ai-orchestration/cost-and-telemetry](java-21-study-guide/09-ai-orchestration/cost-and-telemetry.md))
- **SSE vs WebSocket, back-pressure, end-of-stream usage capture** → Day 12 ([09-ai-orchestration/llm-streaming](java-21-study-guide/09-ai-orchestration/llm-streaming.md))

### System design & leadership
- **5-step blueprint, BoE estimation, deep-dive trade-offs** → Day 13 ([10-system-design-leadership/system-design-blueprint](java-21-study-guide/10-system-design-leadership/system-design-blueprint.md))
- **STAR framework, 8 must-have stories** → Day 17 + Day 19 ([10-system-design-leadership/behavioral-mastery](java-21-study-guide/10-system-design-leadership/behavioral-mastery.md))

### Bonus deep-dives (not tied to a specific day)

These docs cover material the 21 days don't have time to teach in depth. Read them when you need them; treat them as reference, not assignments.

- [01-core/oop-fundamentals](java-21-study-guide/01-core/oop-fundamentals.md) — SOLID, equals/hashCode contract, composition over inheritance. Pre-Day 1 brush-up if you're rusty.
- [01-core/sealed-classes](java-21-study-guide/01-core/sealed-classes.md) — Sealed types + exhaustive switch. Read alongside `records-and-pattern-matching` below.
- [01-core/records-and-pattern-matching](java-21-study-guide/01-core/records-and-pattern-matching.md) — Records, pattern matching for `instanceof` and `switch`, text blocks. **High value for AI orchestrator code:** structured LLM output schemas (records + sealed), tool dispatch (pattern matching), prompt templates (text blocks).
- [02-collections/streams-api](java-21-study-guide/02-collections/streams-api.md) — Streams, Collectors, Optional, parallel streams (and when virtual threads supersede them).
- [05-ecosystem/reactor-and-webflux](java-21-study-guide/05-ecosystem/reactor-and-webflux.md) — Project Reactor + Spring WebFlux, with the honest 2025 take on when to pick reactive vs. virtual-thread + MVC. Read if you're going to defend a reactive choice in a system design round.

---

## 7. How To Use This Material

### If you're following the sprint linearly
Just open `21-day-sprint/week-1-core-engineering/day-01-...md` and start. Every day file is self-contained.

### If you're cherry-picking
Use the **Topic → Sprint-Day Map** in §6 to find the day file or syllabus doc covering what you need. The day file's recall questions are usually the fastest way to *self-test* a topic.

### If you have less than 21 days
Compress by skipping the spaced-review days (16, 20) and merging Day 17/19 (behavioral) into a single afternoon. You lose ~30% of the spaced-repetition benefit but keep all unique content. Don't skip Days 14, 15, 18, 21 — those are mocks where most of the interview improvement happens.

### If you have more than 21 days
Don't extend the sprint — *use the buffer for production work*. Build the capstone for real (deploy it; have a friend use it). Real shipping is worth more than another mock.

### If you're already strong on the Java side
Skip the Java/JVM/Spring deep-dives, keep the day-file *recall questions* as the litmus test, and over-invest in the AI deep-dives (Days 10–12, plus the entire `09-ai-orchestration/` syllabus including the Tier-2 docs).

### If you're already strong on the AI side but new to Java
Inverse: skim the AI deep-dives, focus on Days 1–9, and keep your AI knowledge implicit by referring to it in the system design mocks.

---

## 8. Post-Sprint Maintenance

The sprint is a peak; without maintenance you'll regress in 4–8 weeks. Pick **one** sustainable habit:

- **A — Coding (≈1h/week):** 2 LeetCode Mediums per week, one from a `#weak`-tagged category.
- **B — System design (≈1.5h/week):** one 60-min mock + 30-min write-up per week. Source prompts from [system-design-primer](https://github.com/donnemartin/system-design-primer).
- **C — Reading (≈30m/week):** one paper/post per week. Recommended sources: [Anthropic engineering blog](https://www.anthropic.com/engineering), [Pragmatic Engineer newsletter](https://blog.pragmaticengineer.com/), [arxiv.org/list/cs.CL/recent](https://arxiv.org/list/cs.CL/recent).
- **D — Anki (≈35m/week):** convert the per-day recall questions into a 200-card deck; 5 minutes daily review.

**Combination recommendation: A + C.** Keeps coding sharp without burnout; keeps you current on a fast-moving field. ~1.5h/week total.

Set the recurring calendar block on Day 21. Treat it as a meeting with yourself.

---

## 9. Assessments

In `assessments/`:

- **`rapid-recall-week-1.md`** — ~30 punchy Q&A across Days 1–5 topics. Use the night before any phone screen for last-minute drilling.
- **`rapid-recall-week-2.md`** — ~30 Q&A across Days 6–11 topics.
- **`rapid-recall-week-3-and-ai.md`** — ~40 Q&A across Days 12–13 topics + all AI orchestration deep-dives (including Tier-2 docs).
- **`scenario-drills.md`** — 10 cross-topic interview-style scenarios that integrate multiple deep-dives, with answer-checklists. Use these to test *integration*, not single-topic recall.

---

## 10. What "Done" Looks Like on Day 21

By the final dry-run, you should have:

- A **tight Obsidian per topic** (your own words, not the syllabus's).
- A **1,500-word capstone design doc** plus a small working prototype.
- **8 STAR stories** drilled to 2-minute speaking time.
- A **10-question interviewer Q&A bank**.
- A **debriefed map of your interview fingerprint** — the patterns of mistakes you make under pressure, plus your in-interview compensations.

The 21 days don't make you a senior AI orchestrator. They make you **legible** as one to an interviewer. The work is real either way.
