# Day 15 — System Design Mock #1: Multi-Tenant AI Chatbot

> **Timebox: ~3 hours.** Whiteboard mock (50m, hard stop) → Self-review (30m) → Deep-dive on weakest area (60m) → Written write-up (40m).
> This is the **flagship system design** of the sprint. It will be probed in some form by every interviewer for an AI orchestrator role.

---

## 1. The Prompt (don't read past this line until the timer starts)

> *"Design a multi-tenant AI chatbot SaaS platform. 1,000 business customers, each uploads their own document corpus. Their end-customers chat with an AI widget on the business's website. Strong tenant isolation is required. Walk me through the design."*

**Set a 50-minute timer. Use a whiteboard, large paper, or [Excalidraw](https://excalidraw.com). Talk aloud the whole time. Record yourself if possible.**

---

## 2. The 5-Step Blueprint (your scaffolding)

You memorized this on Day 13. Apply it now without referring back.

1. **Requirements clarification (5 min)** — functional + non-functional. Lock in: tenant count, peak QPS, document size limits, latency SLO, consistency model.
2. **Back-of-envelope (5 min)** — write the numbers on the board.
3. **API + data model (10 min)** — draw 4-6 endpoints + table-by-table storage choices.
4. **High-level architecture (10 min)** — boxes and arrows. Identify the hot path.
5. **Deep dive + trade-offs (15 min)** — tenant isolation, ingestion async, query streaming, cost tracking, failure modes.

The remaining 5 min is buffer for questions you didn't expect.

---

## 3. The Areas Interviewers Will Probe (be ready)

These are the questions that separate senior from staff. Have one-sentence answers ready:

1. **Isolation:** "How do you guarantee Tenant A's RAG cannot retrieve Tenant B's documents?" *(→ pgvector with RLS on `tenant_id`; enforced at the DB kernel, not Java layer; verified by an integration test that crosses tenants and asserts zero leak.)*
2. **Hot tenant:** "Tenant X has 100M docs; Tenant Y has 10. How do you keep Y's queries fast?" *(→ shard pgvector by `tenant_id` once a tenant exceeds threshold; per-tenant connection pools; per-tenant index parameters.)*
3. **LLM latency spike:** "GPT-4o latency goes from 800ms to 8s. What does your user see?" *(→ Token streaming masks raw latency; first-token-latency budget; circuit breaker → fallback to a cheaper/faster model; degraded answer warning.)*
4. **Cost runaway:** "A tenant's customer pastes a 50-page PDF into chat. How do you not bankrupt yourself?" *(→ Token budget per turn, per session, per tenant per day; automatic truncation with user-visible warning; pricing tier enforcement at gateway.)*
5. **Document update propagation:** "A tenant edits their refund policy doc. The chatbot should reflect the change in 60s." *(→ document update → re-embed only changed chunks → publish `document_updated` event → invalidate semantic cache entries tagged with that doc_id.)*
6. **Compliance:** "We're selling to healthcare. What changes?" *(→ JWE not JWS for tokens; PHI-safe LLM provider with BAA; audit log of every document accessed per query; DLP on outgoing LLM payloads.)*

---

## 4. Self-Review (30 min)

Compare your design to the worked example in [system-design-blueprint.md](../../java-21-study-guide/10-system-design-leadership/system-design-blueprint.md).

**Score yourself** out of 5 in each dimension:
| Dimension                          | Score | Notes |
| ---------------------------------- | ----- | ----- |
| Requirements clarification         |       |       |
| Back-of-envelope numbers           |       |       |
| Tenant isolation depth             |       |       |
| Async ingestion pipeline           |       |       |
| Query path & streaming             |       |       |
| Cost telemetry / billing           |       |       |
| Failure modes & resilience         |       |       |
| Operational concerns (rollout, SLO)|       |       |

Anything ≤ 3 → mark `#weak` and schedule a 30m reread before Day 21.

---

## 5. Deep Dive on Weakest Area (60 min)

Pick the lowest-scoring dimension. For each, here are the right resources:

- **Tenant isolation** → re-read [multi-tenancy.md](../../java-21-study-guide/07-security-and-identity/multi-tenancy.md), implement an RLS-protected query in Postgres, prove cross-tenant access fails.
- **Async ingestion** → re-read [resilience-and-patterns.md](../../java-21-study-guide/06-microservices/resilience-and-patterns.md) (Outbox + CDC); sketch the embedding-job pipeline including DLQ + retry semantics.
- **Vector search at scale** → re-read [advanced-rag.md](../../java-21-study-guide/09-ai-orchestration/advanced-rag.md); read [pgvector HNSW tuning](https://github.com/pgvector/pgvector#hnsw); be able to defend `m=16, ef_construction=64, ef_search=40` ranges.
- **Cost / billing** → no canonical doc; design from scratch: every LLM response includes token counts → publish to Kafka → Flink/Beam aggregation → per-tenant daily roll-up → Stripe metering.
- **Streaming** → research Server-Sent Events vs WebSocket back-pressure; understand why naïve `Flux.fromIterable` loses chunks under high load.

---

## 6. Written Write-Up (40 min)

In Obsidian, produce a **publishable-quality 1,500-word design doc** of the multi-tenant chatbot. Sections:
1. Problem & requirements (300 words)
2. Capacity estimates (150 words)
3. Architecture diagram (Mermaid, embedded)
4. Data model (table-by-table)
5. Hot-path query flow (numbered steps)
6. Cross-cutting concerns: isolation, cost, observability (300 words)
7. Trade-offs & alternatives considered (300 words)

This document is your **capstone artifact** — keep iterating on it through Days 16–21. By Day 21 it should be something you'd ship as a real architecture proposal.

---

## 7. Day 15 Deliverables

- [ ] 50-minute whiteboard mock completed (recorded if possible).
- [ ] Self-review scorecard filled in.
- [ ] 60-minute deep-dive on weakest area, with concrete artifact (code, query, doc reread).
- [ ] First-pass capstone write-up (1,500 words).
- [ ] Postmortem of which interviewer probes you couldn't answer in <30s.

## 8. References

- [System Design Primer — chat system case study](https://github.com/donnemartin/system-design-primer#design-a-chat-system)
- [ByteByteGo — Designing a chat system (free article)](https://blog.bytebytego.com/p/system-design-interview-design-a)
- [pgvector — HNSW tuning](https://github.com/pgvector/pgvector#hnsw)
- [Anthropic — Streaming responses with the Claude API](https://docs.anthropic.com/en/api/messages-streaming)
