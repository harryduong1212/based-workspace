# Advanced RAG (Retrieval-Augmented Generation)

Naive RAG (chunking a document every 500 tokens, embedding it, and doing a simple vector search) fails in production. 

## 1. The Problems with Naive RAG

1. **Lost in the Middle**: LLMs pay attention to the beginning and end of their context window. If the exact answer is buried in chunk #7 out of 15, the LLM will likely ignore it or hallucinate.
2. **The Chunking Problem**: If you split a document exactly at 500 tokens, you might cut a crucial sentence in half, destroying its semantic meaning. The vector embedding will be useless.

---

## 2. Advanced Architecture: Parent-Document Retrieval

To solve the chunking problem, we decouple the *embedding chunk* from the *retrieval chunk*.

1. **Small Embeddings**: Chunk the document into very small, semantically dense pieces (e.g., 100 tokens or a single sentence). This creates highly accurate vector representations.
2. **Parent Pointers**: In the database, store a reference from this small chunk to its parent paragraph (e.g., 1000 tokens).
3. **The Flow**: When a user asks a question, run the vector search against the 100-token chunks. Once you find a match, **do not send the 100-token chunk to the LLM**. Instead, retrieve the 1000-token parent paragraph and send *that* as context. 

This gives you the accuracy of micro-chunking with the full context of macro-chunking.

---

## 3. Database Mechanics (pgvector)

PostgreSQL with the `pgvector` extension is the standard for enterprise RAG, as it allows combining relational ACID filtering with semantic vector search.

### Schema Setup
```sql
-- 1. Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create table with vector column 
-- (1536 dimensions is the standard for OpenAI text-embedding-3-small)
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY,
    document_id VARCHAR(255),
    content TEXT,
    metadata JSONB,
    embedding vector(1536)
);
```

### The HNSW Index
A standard exact Nearest Neighbor search must calculate the distance between the query and *every single row* in the database (O(N)). This is incredibly slow.
We use **HNSW** (Hierarchical Navigable Small World) to perform Approximate Nearest Neighbor (ANN) search. It builds a multi-layered graph, allowing sub-millisecond search times over millions of vectors.

```sql
-- Create HNSW index for ultra-fast vector math (cosine similarity)
CREATE INDEX ON document_chunks USING hnsw (embedding vector_cosine_ops);
```

### Hybrid Search
Always filter your data using standard SQL *before* doing vector math.
```sql
SELECT content 
FROM document_chunks 
WHERE metadata->>'tenant_id' = 'tenant-123' -- Relational Filter
ORDER BY embedding <=> '[0.1, 0.2, ...]' -- Vector Search
LIMIT 5;
```
