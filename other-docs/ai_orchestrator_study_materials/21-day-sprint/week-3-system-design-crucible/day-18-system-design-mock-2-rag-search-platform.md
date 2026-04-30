# Day 18 — System Design Mock #2: Real-Time RAG Search Platform

> **Timebox: ~3 hours.** Whiteboard mock (50m, hard stop) → Self-review (30m) → Deep-dive on weakest area (60m) → Capstone iteration (40m).
> A *different* design from Day 15 — same blueprint, different domain. The point is to prove your method generalizes, not to memorize one answer.

---

## 1. The Prompt (don't read past this line until the timer starts)

> *"Design a real-time enterprise search & Q&A system. A 50,000-employee company has internal documents (Confluence, SharePoint, Google Drive, Slack messages, GitHub README files). Employees ask questions in natural language; the system returns answers grounded in their permitted documents. Permissions vary per document. Walk me through the design."*

**Set a 50-minute timer. Whiteboard or Excalidraw. Talk aloud.**

The key complications vs. Day 15:
- **Permissions are per-document, not per-tenant.** ABAC, not just RLS.
- **Source heterogeneity.** Connectors for 5+ source types, each with its own auth and incremental sync semantics.
- **Freshness matters.** When Alice updates a Confluence page, Bob's next query must reflect it within minutes.
- **Scale is bigger.** Hundreds of millions of documents, billions of chunks.

---

## 2. Areas Interviewers Will Probe

1. **Permission propagation:** "Alice has access to a Confluence space; she leaves the company. Her embeddings still exist. What happens?" *(→ ACL is *part of the metadata*, not a separate join. Every chunk row has the source's ACL list. Filter at query time. Re-sync when permissions change is a separate event stream.)*
2. **Freshness latency:** "Edit a doc → searchable in N seconds. What's your N, and what limits it?" *(→ Webhook from source → ingestion queue → re-embed changed chunks → upsert to vector DB → invalidate cache. Realistic: 60-300s. Limit: embedding throughput + queue depth.)*
3. **Source connector reliability:** "GitHub Enterprise rate-limits you. Confluence webhooks drop. How do you guarantee no doc is silently stale?" *(→ Reconciliation job: nightly full-corpus walk per source, compare last-modified timestamps, surface diffs. Combined with webhook stream for low-latency happy path.)*
4. **Query routing:** "User asks 'what's our refund policy?'. Should it search code, Slack, *and* Confluence?" *(→ Classifier picks source(s); per-source weight; user can constrain via UI ("search Confluence only"). Or fan-out and re-rank.)*
5. **Re-ranking:** "Vector search returns 100 results. Top 5 sent to LLM. How do you pick the 5?" *(→ Re-ranker (Cohere Rerank, BGE) on the 100 → sort → take top 5. Adds 50-200ms but boosts answer quality dramatically.)*
6. **Hallucination defense:** "User asks something that's not in the corpus. The LLM helpfully invents an answer. What's your defense?" *(→ Confidence score from retriever; if no chunk above threshold, the system says "I couldn't find this". Plus: prompt instructs LLM to cite sources; UI surfaces citations; if no citations, suppress the answer.)*

---

## 3. Self-Review (30 min)

Compare your design to the worked example you already mastered (multi-tenant chatbot from Day 15). Where does this problem *deviate*, and did you handle the deviations?

| Dimension                                | Score | Notes |
| ---------------------------------------- | ----- | ----- |
| Permissions (ACL per doc, not just tenant) |     |       |
| Source heterogeneity (5+ connectors)      |       |       |
| Incremental sync + reconciliation        |       |       |
| Vector scale (billions of chunks)        |       |       |
| Re-ranking pipeline                      |       |       |
| Hallucination defense / source citation  |       |       |
| Cost telemetry                           |       |       |
| Operational concerns (rollout, SLO, on-call) |   |       |

Anything ≤3 → tag `#weak`, schedule a 30m before Day 21.

---

## 4. Deep-Dive on Weakest Area (60 min)

Likely candidates:

- **ACL / ABAC at scale** → re-read [multi-tenancy.md](../../java-21-study-guide/07-security-and-identity/multi-tenancy.md). Search "OPA Open Policy Agent" — the modern external-decision-point approach. Sketch how OPA evaluates "can user U see doc D" at query time.
- **Source connectors** → research the **incremental sync** pattern: each connector tracks per-source `last_synced_cursor` (e.g. Confluence's `lastUpdated` timestamp, GitHub's `since` parameter, Slack's `oldest` cursor). Reconciliation job catches drift.
- **Re-ranking** → read [Cohere's reranking docs](https://docs.cohere.com/docs/reranking). Understand the cost (rerank-on-100 ≈ 50-200ms) and the recall lift (often +20-30% Recall@5).
- **Hallucination defense** → read [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval). Combine that with LLM-as-judge eval and citation enforcement.

---

## 5. Capstone Iteration (40 min)

Take your Day 15 capstone and **add one section**: *"How this design adapts for the enterprise-search variant."* Don't rewrite the whole thing; show that your design is a *framework* you can flex.

This is the artifact you'll bring to a hiring manager conversation if asked "tell me about a system you've designed". The breadth (two domains, one method) is the senior signal.

---

## 6. Day 18 Deliverables

- [ ] 50-minute whiteboard mock completed (recorded if possible).
- [ ] Self-review scorecard.
- [ ] 60-min deep-dive on weakest area, with concrete artifact.
- [ ] Capstone now has both Multi-Tenant-Chatbot and Enterprise-Search variants.
- [ ] Postmortem of which probes you couldn't answer in <30s.

## 7. References

- [Glean (commercial product) — engineering blog](https://www.glean.com/blog) (real-world enterprise-search architecture writing).
- [OPA — Open Policy Agent docs](https://www.openpolicyagent.org/docs/latest/) — the canonical externalized-authorization pattern.
- [Cohere — Re-ranking](https://docs.cohere.com/docs/reranking).
- [Pinecone — Designing the perfect retrieval system](https://www.pinecone.io/learn/series/rag/) (free articles).
- [LangChain — RAG ingestion patterns](https://python.langchain.com/docs/concepts/document_loaders/).
