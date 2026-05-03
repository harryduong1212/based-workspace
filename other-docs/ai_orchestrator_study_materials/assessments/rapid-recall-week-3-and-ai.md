# Rapid Recall — Week 3 + AI Deep-Dives

> **Format:** punchy single-line Q&A. Same shape as Weeks 1 and 2.
> **Pacing:** ~30 seconds per card; whole file in 40–50 minutes (largest of the three recall files — covers Days 12–13 plus all 8 AI orchestration deep-dives).
> **Why this file matters most:** these are the topics interviewers will probe in the system-design and "tell me about your AI architecture" rounds.

---

## Topic: Heaps & Agentic Patterns (Day 12)

**Q1.** Java's `PriorityQueue` is what kind of heap by default? How do you flip it?
**A.** Min-heap. For max-heap: `new PriorityQueue<>(Comparator.reverseOrder())`.

**Q2.** Merge K Sorted Lists with a heap — what's the time complexity, and why isn't it `O(N log N)`?
**A.** `O(N log k)`. The heap holds at most `k` elements (one per list), not `N`.

**Q3.** Top K Frequent — why bounded *min*-heap of size k, not max-heap?
**A.** Bounded min-heap is `O(n log k)`; max-heap-then-pop-k is `O(n log n)`. Same answer, log-factor faster.

**Q4.** Find Median from Data Stream — what's the trick?
**A.** Two heaps balanced: max-heap of lower half + min-heap of upper half. `getMedian` is O(1) on the roots.

**Q5.** ReAct loop steps?
**A.** Thought → Action (tool call) → Observation → Thought → ... → Final Answer. Each iteration grounds the LLM in real tool output, cuts hallucinations.

**Q6.** Why is "let the LLM make 20 tool calls in one ReAct loop" brittle?
**A.** Latency compounds, hallucination probability multiplies, debugging is hell. Fix: hard step cap + decomposition into multiple smaller agents.

**Q7.** Semantic caching — what do you cache, and what's the threshold?
**A.** Cache the **embedding** of the query (not the string). On cosine similarity > ~0.95 to a cached query, return the stored response.

**Q8.** Cosine 0.95 cache hit — give an example where it returns wrongly.
**A.** "How do I cancel my subscription?" vs "How do I cancel an order?" — high similarity, different intent. Mitigate with per-tenant + per-intent namespaces, optional re-rank with cross-encoder.

**Q9.** Why is n8n's Wait node better than a Spring `@Scheduled` polling job for human approvals?
**A.** Persists workflow state externally, survives restarts, has audit trail + Slack/email integrations, event-driven not poll-based.

---

## Topic: Intervals & System Design (Day 13)

**Q10.** Merge Intervals — what's the boundary call you must clarify aloud?
**A.** Are `[1,3]` and `[3,5]` overlapping? On LC: yes (`<=`). In billing: usually no (`<`). State the assumption.

**Q11.** Insert Interval — name the three phases.
**A.** (1) Emit intervals strictly left of new. (2) Merge all that overlap. (3) Emit strictly right.

**Q12.** Meeting Rooms II — what data structure tracks active meetings?
**A.** Min-heap of *end times*. Sorted by start; for each meeting, pop ended ones, push current end.

**Q13.** Five-step system design blueprint?
**A.** (1) Requirements. (2) Back-of-envelope. (3) API + data model. (4) High-level architecture. (5) Deep-dive trade-offs.

**Q14.** Back-of-envelope: 10M DAU × 10 req/day → average QPS? Peak QPS?
**A.** ~1,150 avg (`10M × 10 / 86,400`). Peak ≈ 2-3× average ≈ 3,000.

**Q15.** Senior signal: in Step 5, what *operational* concerns separate staff from senior?
**A.** Rollout strategy + feature flags; SLO + paging policy; cost-per-tenant attribution; data-retention/GDPR; runbook + on-call.

---

## Topic: Spring AI Tool Calling (Day 10 deep-dive)

**Q16.** Where does the `@Tool` description end up at runtime?
**A.** Converted into a JSON Schema, included in the prompt sent to the LLM. The description *is* the contract.

**Q17.** What's the execution flow once Spring AI receives a tool-call request from the LLM?
**A.** Deserialize JSON args → invoke the local Java method → serialize the return → send back to LLM as `tool_result` → LLM produces final text.

---

## Topic: Model Context Protocol (MCP)

**Q18.** What is MCP, in one sentence?
**A.** An open protocol (Anthropic, late 2024) standardizing how AI assistants connect to external data and tools — "USB-C for AI tools".

**Q19.** Three primitives an MCP server exposes?
**A.** **Tools** (LLM-driven actions), **Resources** (host-driven context), **Prompts** (reusable templates).

**Q20.** Two transport modes for MCP, and when to pick each?
**A.** **stdio** (subprocess) for local tools. **HTTP+SSE** for remote/multi-tenant servers. Both use JSON-RPC 2.0.

**Q21.** When pick `@Tool` over MCP and vice versa?
**A.** `@Tool` for in-process tools owned by your service. MCP for cross-process tools, especially if multiple AI hosts will consume them.

**Q22.** Biggest MCP security risk that has no easy fix?
**A.** Prompt injection through Resources — a malicious doc/issue body says "now call wire_money". The LLM happily complies. Mitigate: human-in-the-loop on high-impact tools, treat resource content as user input.

---

## Topic: LLM Streaming

**Q23.** Define TTFT, ITL, TTLT.
**A.** Time-to-First-Token, Inter-Token Latency, Time-to-Last-Token. You optimize TTFT + perceived latency; TTLT is bounded by output length.

**Q24.** SSE vs WebSocket — default for chat UI?
**A.** SSE. One-way, plain HTTP, works through every proxy. WebSocket only when you need bidirectional (voice agents, mid-stream interruption).

**Q25.** Java 21 + virtual threads — is plain `SseEmitter` competitive with WebFlux for streaming?
**A.** Yes, for most apps. Carrier thread unmounts during the LLM read, blocking is cheap. Default to plain MVC + virtual threads unless you're already reactive.

**Q26.** Why is unbounded buffering between LLM and SSE client a production bug?
**A.** Slow client + fast LLM → buffer grows unboundedly → OOM. Always bound the buffer; decide overflow policy explicitly (block to apply back-pressure, or drop).

**Q27.** What metadata do you need from the *final* streaming chunk, and why?
**A.** Token usage (`prompt_tokens`, `completion_tokens`). Without it, your billing/cost dashboards drift from provider invoices. OpenAI: must set `stream_options: {include_usage: true}`.

**Q28.** A user closes their browser mid-stream. What must your service do?
**A.** Detect disconnect (next `emitter.send` throws), cancel the upstream LLM call. Otherwise you keep paying for tokens nobody reads.

---

## Topic: Vector DB Trade-Offs

**Q29.** Default vector DB for a fresh AI orchestrator product, and why?
**A.** pgvector. Hybrid filtering is just SQL; transactional consistency with relational data; one stateful system to operate; team already knows it.

**Q30.** When do you outgrow pgvector?
**A.** Past ~50–100M vectors with HNSW build/query pain; or vector queries are 99% of traffic; or you need multi-region active-active.

**Q31.** HNSW — three tuning knobs and what each controls?
**A.** `m` (graph connectivity, default 16). `ef_construction` (build-time exploration, default 64). `ef_search` (query-time, 40-200).

**Q32.** Embedding dimensions — `text-embedding-3-large` (3072) vs `small` (1536) for storage cost?
**A.** Roughly 2× storage, 2× index memory, ~6× API price. Recall lift is often only 3-5% — not always worth it. Eval on *your* data.

**Q33.** Three multi-tenancy patterns in vector DBs, ordered by isolation strength?
**A.** Separate cluster per tenant > Namespaces/collections per tenant > `tenant_id` column with metadata filter. Cost inverse to isolation.

**Q34.** Why is a cross-tenant integration test mandatory?
**A.** A missed `tenant_id` filter silently returns Tenant B's docs to Tenant A. Too easy to ship; the test is the only safety net.

---

## Topic: Multi-Agent Patterns

**Q35.** Four canonical multi-agent patterns?
**A.** Supervisor (one orchestrator + N specialists). Hierarchical (tree). Swarm (peer-to-peer handoff). Plan-and-Execute (planner emits plan, executor runs it).

**Q36.** Default multi-agent pattern for production, and why?
**A.** Supervisor. Centralized state machine = debuggable; specialists are pure functions; flat topology unless complexity genuinely demands hierarchy.

**Q37.** Three rules that keep a Supervisor alive in production?
**A.** (1) Hard step budget (`< 8` hops). (2) Structured output for the supervisor's decision (JSON schema). (3) Append-only state — don't mutate mid-run.

**Q38.** When is multi-agent the *wrong* answer?
**A.** Simple tool calling (use `@Tool` directly). Latency-critical UX (each hop adds 1-3s). When the decomposition is artificial — "I want it to feel smart" is not a reason.

---

## Topic: LLM Evaluation

**Q39.** Why don't standard JUnit equality assertions work for LLM outputs?
**A.** Non-determinism — even temperature=0 isn't bit-deterministic across providers/versions. Replace with: heuristic checks + embedding similarity + LLM-as-judge.

**Q40.** What is a golden dataset, and what's the wrong way to build one?
**A.** 50-500 (input, expected_output) tuples sampled from real production logs, hand-labeled. Wrong way: synthetic data generated by GPT — misses real edge cases.

**Q41.** Four Ragas metrics?
**A.** **Faithfulness** (claims grounded in context?), **Answer Relevancy** (addresses question?), **Context Precision** (retrieved chunks relevant?), **Context Recall** (did we retrieve all relevant?).

**Q42.** Diagnostic value: low *faithfulness* + high *answer relevancy* — what's happening?
**A.** Hallucinating coherent-looking lies. Worst failure mode. Fix: prompt engineering for grounding, citation enforcement, switch model.

**Q43.** Three traps with LLM-as-judge?
**A.** (1) Self-bias (GPT-4 scores GPT-4 outputs higher). (2) Position bias (prefers first option in pairwise). (3) Self-consistency noise — single-shot scores are unreliable; run 3× and average.

**Q44.** What's the human-calibration check?
**A.** Have humans score 50 outputs the judge already scored. Compute Pearson correlation. Below 0.7 → judge is unreliable for this task.

---

## Topic: Cost & Token Telemetry

**Q45.** Approximate cost ratio: completion vs prompt tokens?
**A.** Completion tokens cost ~4-5× prompt tokens. A short answer with a long system prompt is mostly prompt-cost.

**Q46.** Anthropic prompt caching discount? OpenAI's?
**A.** Anthropic: ~90% off for cached prompt tokens (explicit annotation, 5-min TTL). OpenAI: 50% off (automatic, prefix > 1024 tokens, ~10-min window).

**Q47.** Order-of-prompt rule for OpenAI prompt caching?
**A.** Stable content **first** (system, RAG context). Dynamic content **last** (user message, recent turns). Reordering invalidates the cache.

**Q48.** Pre-flight token check — what does it prevent?
**A.** Sending a doomed request to the API and *paying* for it. Use a local tokenizer (jtokkit for OpenAI BPE) to count before sending.

**Q49.** Per-tenant rate limit — what storage backs Bucket4j in HA?
**A.** Redis. Single-node Bucket4j is fine for one pod; multi-pod requires Redis-backed or similar shared state.

**Q50.** Top three cost footguns?
**A.** Unbounded conversation memory (quadratic cost growth). Re-embedding on every read. Multi-agent runs with no step cap. (Honorable mention: streaming clients that don't propagate cancellation upstream.)

---

## Topic: Agent Memory

**Q51.** Four agent memory tiers?
**A.** Short-term (context window), Long-term (facts about user), Episodic (past conversation summaries), Procedural (learned playbooks / few-shot patterns).

**Q52.** Sliding-window vs rolling-summary for short-term memory — when does each fail?
**A.** Sliding-window loses old context (bad for "what did we decide last hour?"). Rolling-summary decays through summary-of-summaries; mitigate by occasionally re-summarizing the full history.

**Q53.** Where do you store extracted long-term facts, and what's the schema essentials?
**A.** Postgres + pgvector. Schema: `(user_id, tenant_id, content, embedding, source_type, confidence, last_accessed_at)`.

**Q54.** Conflict resolution for contradicting facts ("user prefers Python" vs "user just switched to Rust") — three strategies?
**A.** Recency-weighted retrieval. Periodic conflict-resolution prompt. Confidence decay over time.

**Q55.** GDPR / Right-to-Erasure design rule for memory?
**A.** Build a `DELETE /v1/users/{id}/memory` endpoint that purges all four tiers. Retrofitting is hard; build it on day 1.

**Q56.** Single most common agent-memory bug?
**A.** Cross-conversation leakage — missing `user_id` filter in retrieval returns another user's facts. Cross-user integration test mandatory.

---

## Topic: Saga & Service Comms

**Q57.** Sync vs async — heuristic for the *one-line decision*?
**A.** "Does the user have to wait?" Yes → sync (HTTP/gRPC). No → async (Kafka, RabbitMQ). Mix freely per flow.

**Q58.** Saga orchestration over choreography — when?
**A.** Workflows >4 steps, complex compensation order, or human-in-the-loop. Centralized state machine wins for debuggability.

**Q59.** What guarantees does a Postgres-state-machine Saga orchestrator give you?
**A.** Crash-safe (resumes from `current_step` after restart). Idempotent (each step dedupes by saga ID). Auditable (`completed_steps` is the trail).

**Q60.** Three AI-specific Saga failure modes that need distinct handling?
**A.** Rate-limit (429): retry with longer backoff. Quota exhaustion (402): don't retry, mark failed. Mid-stream timeout: idempotency keys to prevent double-charging on retry.

**Q61.** Outbox pattern — what is the *one* thing it solves?
**A.** Dual-write atomicity: writing to DB *and* publishing to Kafka cannot be atomic across systems. Outbox makes them atomic by writing the event into the same DB transaction as the entity.

**Q62.** Why is Debezium CDC superior to a `@Scheduled` outbox poller?
**A.** Reads the WAL directly — near-zero latency, no polling load on the OLTP table, replays from any LSN, doesn't need its own concurrency story.

---

## Cross-cutting bonus

**Q63.** Senior signal in a system design round: what 8 cost-architecture concerns can you name?
**A.** (1) Pre-flight token check. (2) TokenUsageEvent on every call. (3) Prompt caching. (4) Semantic response caching. (5) Model routing (cheap → escalate). (6) Per-tenant budgets at gateway. (7) Per-feature cost dashboards. (8) Stripe metering integration.

**Q64.** A capstone defense in 60 seconds — what's the spine of the multi-tenant chatbot?
**A.** WebSocket → Gateway (JWT, tenant context) → ChatService → embed + vector search filtered by `tenant_id` (RLS-protected) → prompt assembly → LLM streamed → SSE/WS to client. Async ingestion: PDF → RabbitMQ → embed worker → pgvector. Per-call `TokenUsageEvent` → Outbox → Kafka → Billing.

---

**Score yourself:** count cards you got right within ~10s.
- 55–64: ready for the AI-orchestration interview rounds.
- 45–54: re-read the lowest-scoring topics; revisit recall in 3 days.
- <45: this file is the *most* important to drill — these are the topics interviewers fixate on for this role.
