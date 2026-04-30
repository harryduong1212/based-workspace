# Vector Database Trade-Offs

Picking a vector DB is one of the highest-leverage decisions in an AI orchestrator's architecture. The wrong choice surfaces 18 months later as a six-figure migration. The right choice depends on **three axes** the marketing pages don't surface: *hybrid filtering*, *operational burden*, and *blast radius*.

## 1. The Decision Matrix

| Engine | Hybrid filter quality | ACID with relational data | Ops burden (self-host) | Scale ceiling (100M vectors) | Pricing model |
| ------ | -------------------- | ------------------------- | ---------------------- | ----------------------------- | ------------- |
| **pgvector** | Excellent — SQL is the filter language | **Yes** — same Postgres txn | Low (your existing PG) | ~10–50M comfortable; >100M painful | Storage + compute |
| **Pinecone** | Good (metadata filters) | No (separate system) | Zero (managed-only) | Unlimited | Per-pod ($) |
| **Qdrant** | Excellent (rich filter DSL) | No | Medium (yet another stateful system) | Strong; tested to billions | OSS, paid managed available |
| **Weaviate** | Good (GraphQL filter) | No | Medium-high | Strong | OSS, paid managed |
| **Milvus** | Good | No | High (HA setup is involved) | Excellent (largest deployments) | OSS, paid managed |
| **OpenSearch / Elasticsearch + kNN plugin** | Good (Lucene queries) | No | Medium (if already running ES) | Strong | OSS, paid managed |

This table over-simplifies. The honest decision is *which trade-off you're optimizing*.

## 2. The First Decision: pgvector or Specialist?

### Default to pgvector unless you hit a hard limit

For 90% of teams starting an AI orchestrator product, **pgvector is the right call**. Reasons:

1. **Hybrid filtering is a single SQL query.** Filter by tenant, date, status, etc., *then* vector search — all in one query plan. Most "we picked Pinecone and regret it" stories trace back to fanning out a metadata pre-filter, then re-ranking. SQL does this natively.
2. **Transactional consistency.** When a user uploads a doc, you can write the document row + chunk rows + embeddings in a single transaction. If the txn rolls back, no orphaned vectors.
3. **One stateful system to operate.** You already run Postgres. Adding pgvector is `CREATE EXTENSION` and an HNSW index — not a new HA cluster, not new IAM, not new backup strategy.
4. **Your team already speaks SQL.**

### When pgvector breaks down

Move off pgvector when **at least one** of:
- You're past **~100M vectors** and seeing index-build times > hours and query latency P99 > 200ms even after tuning.
- Your workload is **vector-first** (vector queries are 99% of traffic, relational is incidental). At that ratio the specialist's optimizations matter.
- You need **billion-scale** with high write throughput. pgvector's HNSW becomes painful past ~50M; specialists like Milvus or Qdrant scale better.
- You need **multi-region active-active** for sub-100ms latency globally. Postgres is hard for this; managed Pinecone or distributed Qdrant solve it natively.

## 3. Indexing Algorithms — What You Need to Know

Vector DBs let you pick an Approximate Nearest Neighbor (ANN) index. The three relevant ones:

### HNSW (Hierarchical Navigable Small World)
- **Recall:** excellent (99%+ achievable).
- **Build time:** slow (`CREATE INDEX` on 10M rows in pgvector: 30 min – several hours).
- **Update cost:** moderate; tolerates incremental inserts.
- **Memory:** high (the graph layers live in memory for fast traversal).
- **Tune knobs:** `m` (graph connectivity, default 16), `ef_construction` (build-time exploration, default 64), `ef_search` (query-time exploration, often 40–200).
- **Use as default.** It's the right answer for most workloads.

### IVFFlat (Inverted File with Flat lists)
- **Recall:** lower than HNSW unless `lists` and `probes` are tuned.
- **Build time:** fast.
- **Update cost:** low — append-friendly.
- **Memory:** lower than HNSW.
- **Tune knobs:** `lists` (cluster count; rule of thumb `lists = rows / 1000`), `probes` (query-time).
- **Use when:** you have a *write-heavy* workload that re-indexes often, or memory is tight. Otherwise prefer HNSW.

### DiskANN (Microsoft, used by some managed services)
- **Recall:** excellent.
- **Memory:** much lower than HNSW (graph lives on SSD).
- **Use when:** vector count exceeds RAM budget. Managed Pinecone uses a DiskANN-like approach internally.

### The `m` and `ef_search` rule of thumb (HNSW)
| Goal | `m` | `ef_search` |
| ---- | --- | ----------- |
| Latency-first | 16 | 40 |
| Balanced | 16 | 80 |
| Recall-first (RAG quality matters more than 50ms) | 32 | 200 |

Doubling `ef_search` roughly halves the recall miss rate at ~1.5× latency. Tune *with your eval set*, not by reading docs.

## 4. Hybrid Search — The Pattern That Matters Most

Pure vector search is rare in production. **Real queries always combine vector similarity with metadata filters** (tenant ID, date range, document type, ACL). The order matters.

```sql
-- pgvector — hybrid query
SELECT id, content, (embedding <=> $1) AS distance
FROM document_chunks
WHERE tenant_id = $2                  -- relational filter (B-tree)
  AND created_at > NOW() - INTERVAL '90 days'
  AND status = 'PUBLISHED'
ORDER BY embedding <=> $1             -- vector search (HNSW)
LIMIT 10;
```

The Postgres planner is smart enough to use a B-tree on `tenant_id` first, then HNSW on the surviving rows — *if* you have the right indexes:
```sql
CREATE INDEX ON document_chunks (tenant_id, created_at);                     -- B-tree
CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);   -- HNSW
```

Specialist vector DBs handle this differently. Pinecone has metadata filters but the hybrid execution is opaque; tune by experimentation. Qdrant exposes a payload filter DSL with explicit ordering.

## 5. Embedding Dimensions: The Cost-Performance Knob

| Model | Dims | Per 1M tokens | Notes |
| ----- | ---- | ------------- | ----- |
| OpenAI `text-embedding-3-small` | 1536 (or 512 truncated) | ~$0.02 | Default sweet spot |
| OpenAI `text-embedding-3-large` | 3072 | ~$0.13 | 6.5× cost; ~3-5% recall lift |
| Voyage `voyage-3-large` | 1024 | ~$0.18 | Best public retrieval benchmarks (late 2025) |
| Cohere `embed-v4.0` | 1536 | ~$0.12 | Strong multilingual |
| Local (BGE, E5, GTE via sentence-transformers) | 384–1024 | $0 (CPU/GPU cost) | Re-runs your hardware |

Storage scales linearly with dimensions: a 100M-vector corpus at 1536 dims = ~600GB; at 3072 dims = ~1.2TB. **Index memory roughly doubles too.**

The **right dimension count** is whatever your eval-set says — *not* whatever's biggest. Often `text-embedding-3-large` truncated to 1024 dims is the right answer (configurable on OpenAI's side via `dimensions` param). Always benchmark on *your* data.

## 6. Multi-Tenancy in Vector DBs

Three patterns; pick by isolation requirement:

1. **`tenant_id` column + relational filter** (pgvector + RLS, or Pinecone metadata filter). Cheapest, best query planner support. **Default for SaaS.**
2. **Namespaces / collections per tenant** (Pinecone namespaces, Qdrant collections, Weaviate classes). Better isolation; you can delete a tenant atomically. Watch the **collection-count ceiling** — managed engines often cap at low thousands of collections.
3. **Separate database / cluster per tenant.** Highest isolation, highest cost. Reserve for healthcare, finance, or contractual mandates.

Whichever you pick, **write a cross-tenant integration test** that asserts Tenant A's queries cannot return Tenant B's vectors. This bug is too easy to ship.

## 7. Re-Ranking: The Tier Above Vector Search

Vector search gives you 100 candidates with reasonable recall. A **cross-encoder re-ranker** (Cohere Rerank, BGE-reranker, Jina) re-scores them with a slower but more accurate model, returning the top 5. Latency cost: ~50–200ms. Recall@5 lift: often **+20–30%** on real-world retrieval tasks.

```
Query → Vector search (k=100) → Re-ranker → Top-5 → LLM context
```

If your RAG quality plateaus despite tuning HNSW and chunking strategy, **add a re-ranker before adding more retrieval engineering**. It's the single highest-leverage RAG fix.

## 8. Operational Concerns Marketing Pages Hide

- **Index rebuild on schema change.** HNSW doesn't tolerate dimension changes. If you upgrade embedding models (1536 → 3072 dims), you re-embed and rebuild the index. Plan a 24-72h backfill window.
- **Hot reads on cold data.** New tenants have small corpora; the HNSW graph is over-tuned for the fat tenant. Per-tenant index parameters (or separate indexes) start to matter past ~50 active tenants.
- **Backups.** Postgres `pg_dump` is fine. Pinecone has snapshot APIs. Qdrant snapshots are per-collection. Test restore time, not just backup time.
- **Cost dashboards.** Storage and queries scale separately. Pinecone in particular charges per-pod-hour, not per-query. Surprise bills happen when you forget to scale down dev pods.

## 9. The Decision Tree (Memorize This)

```
Are you starting fresh, < 50 tenants, < 50M vectors expected in 18 months?
  → pgvector. Stop reading.

Are you fully managed-stack (no devops), no Postgres in your future, want zero-ops?
  → Pinecone.

Are you running Elasticsearch/OpenSearch already and search is your core competency?
  → ES/OS kNN plugin. Reuse the cluster.

Are you self-hosting, billion-scale, vector-first?
  → Qdrant or Milvus. Read both benchmarks for *your* workload before picking.

Do you need multi-region active-active, < 100ms global latency, no Postgres lock-in?
  → Pinecone or distributed Qdrant.
```

---

## References
- [pgvector — README & HNSW tuning](https://github.com/pgvector/pgvector)
- [Pinecone — *Vector index types & trade-offs*](https://www.pinecone.io/learn/series/faiss/vector-indexes/)
- [Qdrant — Filtering and indexing](https://qdrant.tech/documentation/concepts/filtering/)
- [HNSW paper — Malkov & Yashunin (2016)](https://arxiv.org/abs/1603.09320)
- [DiskANN paper — Microsoft (2019)](https://suhasjs.github.io/files/diskann_neurips19.pdf)
- [Cohere — Re-ranking guide](https://docs.cohere.com/docs/reranking)
- [MTEB leaderboard — embedding model benchmarks](https://huggingface.co/spaces/mteb/leaderboard) (read with skepticism — benchmarks ≠ your data)
