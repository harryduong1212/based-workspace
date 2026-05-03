# Scenario Drills — Cross-Topic Integration

> **Purpose:** rapid-recall tests *single-topic* memory. These drills test **integration** — your ability to compose multiple deep-dives into a coherent answer under pressure. This is the actual senior-interview signal.
> **Format:** each drill is one mock-interview prompt + an answer-checklist + the syllabus refs you'd reach for. Read the prompt, **answer aloud for 2-3 minutes**, then compare to the checklist.
> **Pacing:** ~5 minutes per drill (2-3 talking, 2-3 reviewing). Whole file in ~50 minutes.

---

## Drill 1 — The Hot Tenant

**Setup:** "Your multi-tenant chatbot SaaS has 1,000 customers. Tenant X has 100M documents indexed; Tenant Y has 10. Tenant X is degrading Tenant Y's query latency. Walk me through how you'd diagnose and fix this without giving X a worse experience."

**Probe yourself for:**
- [ ] Diagnosis steps: per-tenant query latency dashboards, P50/P95/P99 breakdown by tenant.
- [ ] Hypothesis: shared HNSW index dominated by X's vectors → all queries pay X's index size.
- [ ] Fix tier 1: per-tenant index parameters or partitioned indexes (sharding pgvector by `tenant_id` once a tenant exceeds a threshold).
- [ ] Fix tier 2: Postgres connection-pool partitioning — separate pool for X so its slow queries don't starve Y's pool.
- [ ] Fix tier 3: tier-based pricing — X pays for dedicated infra (separate pgvector instance/cluster), unblocking Y at no extra cost to other tenants.
- [ ] Operational: alerts when any tenant crosses *N* % of total query share so you don't get caught off-guard.

**Refs:** [vector-db-tradeoffs](../java-21-study-guide/09-ai-orchestration/vector-db-tradeoffs.md), [multi-tenancy](../java-21-study-guide/07-security-and-identity/multi-tenancy.md), [resilience-and-patterns](../java-21-study-guide/06-microservices/resilience-and-patterns.md) (bulkhead).

---

## Drill 2 — The Streaming Cost Spike

**Setup:** "Your dashboard shows LLM cost spiked 3× last week with no traffic increase. P95 conversation length is unchanged. Cache hit rate is normal. Find the bug in 90 seconds."

**Probe yourself for:**
- [ ] Suspect 1: a prompt change increased system prompt size (long system prompts dominate cost when output is short). Check version-tagged prompts.
- [ ] Suspect 2: streaming clients aren't propagating cancellation — users close the tab, the LLM keeps generating, you keep paying. Check correlation between disconnect events and post-disconnect token consumption.
- [ ] Suspect 3: a new feature added agentic tool-calling but without a step budget → some conversations are now 30-step ReAct loops.
- [ ] Suspect 4: prompt cache invalidation — someone reordered the prompt, dropping the cache hit rate from 60% to 5%. *(Cache hit rate said normal in setup, so this is ruled out.)*
- [ ] Diagnosis tools: per-feature cost breakdown, per-prompt-version cost, distribution of tokens-per-conversation.

**Refs:** [cost-and-telemetry](../java-21-study-guide/09-ai-orchestration/cost-and-telemetry.md), [llm-streaming](../java-21-study-guide/09-ai-orchestration/llm-streaming.md), [multi-agent-patterns](../java-21-study-guide/09-ai-orchestration/multi-agent-patterns.md).

---

## Drill 3 — The Hallucination Regression

**Setup:** "After last Tuesday's prompt change, customer thumbs-down rate doubled. The team is rolling back. Senior leadership wants to know: how do we prevent this in the future? You have 5 minutes."

**Probe yourself for:**
- [ ] Root cause: shipping prompts without offline eval gating.
- [ ] Build: a golden dataset of 50-500 (input, expected) cases sampled from real production logs.
- [ ] Heuristic + embedding-similarity + LLM-as-judge eval pipeline.
- [ ] CI gate: any metric regression > 2% blocks merge.
- [ ] RAG-specific: faithfulness, answer relevancy, context precision/recall (Ragas).
- [ ] Production telemetry feedback loop: thumbs-down events flow back into the eval set; quarterly re-sampling.
- [ ] Adversarial set, run on every prompt change.
- [ ] Prompt versioning: every LLM call logs the prompt version; debugging old reports is then trivial.

**Refs:** [llm-evaluation](../java-21-study-guide/09-ai-orchestration/llm-evaluation.md), [observability](../java-21-study-guide/08-infrastructure/observability.md).

---

## Drill 4 — The Compliant Migration

**Setup:** "Legal needs you to migrate from logging full chat transcripts to logging redacted versions. The system has 2 years of data, ~500GB of logs, currently in Postgres. Customers will be SOC2-audited next month. Walk me through the migration plan."

**Probe yourself for:**
- [ ] Scope: backfill (existing logs) + forward (new logs).
- [ ] Forward path: redaction service in front of every log write — PII detection (regex + ML) → mask → write.
- [ ] Backfill path: paginated worker reads → redacts → writes new redacted column → switch reads to new column → drop old column. **Expand-and-contract** pattern.
- [ ] Why batch in pages: a `UPDATE chat_logs SET redacted_content = redact(content)` over 500GB locks the table. Use `LIMIT 10000` with cursors; or `CREATE TABLE LIKE` + dual-write + cutover.
- [ ] Audit: every redaction emitted as a row to an immutable audit table (which user accessed which records, what was redacted).
- [ ] Right-to-erasure: opportunistically purge fully on customer request.
- [ ] Operational: feature flag for the redacted-read path, gradual rollout, runbook for rolling back if redaction service breaks.

**Refs:** [jdbc](../java-21-study-guide/05-ecosystem/jdbc.md) (Expand-and-Contract), [agent-memory](../java-21-study-guide/09-ai-orchestration/agent-memory.md) (right-to-erasure).

---

## Drill 5 — The Embedding Re-Indexing

**Setup:** "We're upgrading from `text-embedding-3-small` (1536 dims) to a domain-fine-tuned model with 1024 dims. We have 200M existing embeddings. Live customer traffic is 3K QPS. Plan the cutover."

**Probe yourself for:**
- [ ] Constraint: HNSW indexes don't tolerate dimension changes — you must rebuild.
- [ ] Cannot mix old and new vectors in the same index — different vector spaces.
- [ ] Plan: dual-write phase (write both 1536-dim *and* 1024-dim embeddings for new docs), backfill 200M existing docs in the background, switch reads, decommission old.
- [ ] Backfill timing: at 1000 embeds/sec, 200M / 1000 = ~55 hours — but rate-limited by the embedding API, more like 5-10 days.
- [ ] Cost: re-embedding 200M docs = real money (~$4K at OpenAI's small-model price; more for fine-tuned). Budget approval before kickoff.
- [ ] Eval: golden dataset Recall@5 *before* cutover. If new model regresses on critical scenarios, abort.
- [ ] Operational: per-tenant rollout (canary on Tenant Z first), feature flag for switch.
- [ ] Cleanup: drop old `embedding_v1` column + index after cutover stable for 30 days.

**Refs:** [vector-db-tradeoffs](../java-21-study-guide/09-ai-orchestration/vector-db-tradeoffs.md), [advanced-rag](../java-21-study-guide/09-ai-orchestration/advanced-rag.md), [llm-evaluation](../java-21-study-guide/09-ai-orchestration/llm-evaluation.md).

---

## Drill 6 — The Agent That Won't Stop

**Setup:** "An agentic feature in beta is in an infinite ReAct loop on certain inputs — burning $500/hour per stuck conversation. The on-call engineer woke you at 3 AM. Triage in 5 minutes."

**Probe yourself for:**
- [ ] Immediate stop-the-bleed: server-side step budget enforcement (refuse to execute step N+1 if N > limit). Should already be there; if missing, hot-fix it.
- [ ] Per-conversation token budget enforced at the gateway — refuse new LLM calls when budget exceeded.
- [ ] Per-tenant per-day cost circuit breaker.
- [ ] Identify the specific stuck conversations from telemetry; cancel running streams.
- [ ] Root cause: LLM picking the same tool repeatedly because tool descriptions overlap, or the tool returns ambiguous output that doesn't progress state, or no convergence condition.
- [ ] Postmortem: structured handoffs, hard step caps, observability tagging every LLM call with `(trace, agent, step, parent_step)` so we can reproduce.
- [ ] Process: this should never have shipped without step budgets — that's the systemic CI/CD change to prevent recurrence.

**Refs:** [multi-agent-patterns](../java-21-study-guide/09-ai-orchestration/multi-agent-patterns.md) (step budgets), [cost-and-telemetry](../java-21-study-guide/09-ai-orchestration/cost-and-telemetry.md), [agentic-patterns](../java-21-study-guide/09-ai-orchestration/agentic-patterns.md).

---

## Drill 7 — The Multi-Region Decision

**Setup:** "We're at $20M ARR, US-only. Largest prospect (EU) demands EU-resident data and < 200ms p95. Architecture is currently single-region us-east-1, pgvector + Spring Boot + Cloud Run. What's the design?"

**Probe yourself for:**
- [ ] Cannot replicate Postgres async to EU — would violate data-residency.
- [ ] Active-active per region: separate Postgres + pgvector cluster in eu-west-1.
- [ ] Tenant routing: each tenant pinned to a *home region* (encoded in JWT claim or tenant config). Gateway routes accordingly.
- [ ] Cross-region: shared identity provider only (Auth0/Cognito multi-region). No customer data crosses borders.
- [ ] LLM provider: pick one with EU endpoints (Anthropic via AWS Bedrock in eu-west, or Azure OpenAI EU regions).
- [ ] Embedding model: same constraint.
- [ ] Cost telemetry: per-region cost rollup; ensure billing aggregator survives a region outage.
- [ ] Failure mode: if eu-west-1 is down, EU tenants are down. State this explicitly — multi-region active-passive within EU (eu-west-1 + eu-central-1) is the next step if SLA demands it.
- [ ] Rollout: stand up infra → migrate first EU customer → soak for 30 days → marketing.

**Refs:** [multi-tenancy](../java-21-study-guide/07-security-and-identity/multi-tenancy.md), [vector-db-tradeoffs](../java-21-study-guide/09-ai-orchestration/vector-db-tradeoffs.md), [containerization](../java-21-study-guide/08-infrastructure/containerization.md).

---

## Drill 8 — The Performance Investigation

**Setup:** "Chat p99 latency went from 2.3s to 5.8s last week. Nothing changed in our code. Find the bug in 5 minutes — talk through your investigation steps."

**Probe yourself for:**
- [ ] Step 1: confirm the regression. Time-series chart by service hop (gateway → chat → embed → vector search → LLM → response).
- [ ] Step 2: which hop spiked? Likely candidates: LLM provider latency, vector DB scan, embedding API.
- [ ] If LLM hop: provider degradation → check provider's status page. Mitigation: failover to secondary provider (Anthropic ↔ OpenAI) if you architected for it.
- [ ] If vector hop: corpus growth pushed past HNSW's `ef_search` recall plateau → tune `ef_search` down (faster, lower recall) or partition.
- [ ] If embedding hop: rate-limited; queueing latency dominates.
- [ ] If DB hop: sequential scan introduced because the query planner started picking a different plan after a stats refresh — `ANALYZE` and check `pg_stat_statements`.
- [ ] Step 3: traceparent through one slow request end-to-end. Locate the actual culprit, not the symptom.
- [ ] Step 4: rollback / mitigate / root-cause in that order — never the reverse.
- [ ] Postmortem signal: do we have alerts on per-hop latency, not just end-to-end? If not, that's the systemic fix.

**Refs:** [observability](../java-21-study-guide/08-infrastructure/observability.md), [vector-db-tradeoffs](../java-21-study-guide/09-ai-orchestration/vector-db-tradeoffs.md), [jdbc](../java-21-study-guide/05-ecosystem/jdbc.md), [resilience-and-patterns](../java-21-study-guide/06-microservices/resilience-and-patterns.md).

---

## Drill 9 — The Cross-Tenant Leak

**Setup:** "You're paged: customer reports they saw a *different* tenant's document content in their chatbot's response. This is potentially a SOC2 breach. Walk me through the next 4 hours."

**Probe yourself for:**
- [ ] Triage (first 30 min): isolate. Disable the suspicious feature for *all* tenants. Snapshot logs. Notify legal/security.
- [ ] Diagnosis: was the leak in retrieval (vector DB returned wrong rows) or generation (LLM hallucinated content from system-prompt cross-contamination)?
- [ ] Reproduce in staging with the customer's exact query.
- [ ] Likely culprits: missing `tenant_id` filter in a query path; semantic cache without per-tenant namespace; system prompt accidentally leaking content from another conversation.
- [ ] Fix: add the filter; add a cross-tenant integration test that fails until the fix is in; deploy via expedited release path.
- [ ] Communication: customer-facing post, regulator-facing report, internal post-mortem.
- [ ] Systemic prevention: kernel-enforced isolation (RLS) so a missed `WHERE` clause cannot leak. Cross-tenant integration test in CI. Anomaly detection on cache key collisions.
- [ ] The senior tell: explicitly *separate* the immediate fix from the systemic fix. Both must happen.

**Refs:** [multi-tenancy](../java-21-study-guide/07-security-and-identity/multi-tenancy.md), [agent-memory](../java-21-study-guide/09-ai-orchestration/agent-memory.md), [agentic-patterns](../java-21-study-guide/09-ai-orchestration/agentic-patterns.md) (semantic cache).

---

## Drill 10 — The "What Would You Build First?" Question

**Setup:** "You're hired to lead a new AI orchestrator team. Day 1, you have: 2 backend engineers, no users, $50K/mo budget. The product is 'an AI assistant for customer support tickets'. Walk me through your first 90 days."

**Probe yourself for:**
- [ ] Days 1-7: requirements clarification with product/sales. Pick 1 design partner. Define golden dataset of 50 real tickets + expert resolutions.
- [ ] Days 8-21: minimal end-to-end pipeline. Postgres + pgvector + Spring Boot + Spring AI + a single tool (`searchKnowledgeBase`). Single tenant. Slack hook for human review.
- [ ] Days 22-35: ship to design partner under flag. Build observability (correlation IDs, per-call cost telemetry) before scaling.
- [ ] Days 36-60: evals as CI gate. Adversarial test set. Per-tenant config. Multi-tenancy via RLS once you have tenant #2.
- [ ] Days 61-90: incident response runbook. On-call rotation. Cost dashboards per tenant. Plan tier-2 features (memory, multi-agent if warranted).
- [ ] What you'd *defer*: streaming UI polish, native iOS app, multi-region. Defer = explicit list with rationale, not silent.
- [ ] Hiring: a 3rd engineer with strong ML eng / ops experience around month 2.
- [ ] The signal: showing you can sequence work, defer non-essentials, and ship a learning loop in 90 days, not a polished product in 6 months.

**Refs:** [system-design-blueprint](../java-21-study-guide/10-system-design-leadership/system-design-blueprint.md), [llm-evaluation](../java-21-study-guide/09-ai-orchestration/llm-evaluation.md), [behavioral-mastery](../java-21-study-guide/10-system-design-leadership/behavioral-mastery.md).

---

## How to use this file

- **Pre-interview week:** do 2 drills/day; record yourself; compare answer to checklist.
- **Day before an onsite:** read all 10 prompts (no answer attempts). Skim checklists. The goal isn't to memorize answers — it's to remind your brain of the cross-topic patterns.
- **After each drill:** anything you missed in the checklist → tag the relevant deep-dive `#weak`, schedule a 20m re-read.

These drills lean toward "incident" and "decision" framings on purpose. Senior interviews aren't *"design X from scratch"* — they're *"X is broken / changing / scaling, what do you do?"*.

The pattern under all 10 drills:
1. **Triage** — stop bleeding before debugging.
2. **Diagnose** — by hop / by metric / by hypothesis.
3. **Fix** — immediate.
4. **Systemic prevention** — the senior signal.
5. **Communicate** — internally + externally.

Memorize that 5-step shape. It's the spine of every senior incident answer.
