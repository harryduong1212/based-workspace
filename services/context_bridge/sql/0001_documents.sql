-- Context Bridge schema — Phase F
-- One shared documents table; source distinguishes connector origin.
-- Upsert key: (source, source_id, chunk_idx).

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id          BIGSERIAL PRIMARY KEY,
    source      TEXT      NOT NULL,         -- e.g. 'jira', 'bitbucket'
    source_id   TEXT      NOT NULL,         -- ticket key, PR id
    chunk_idx   INTEGER   NOT NULL,
    content     TEXT      NOT NULL,
    embedding   VECTOR(384),                -- bge-small-en-v1.5 dimension
    metadata    JSONB     NOT NULL DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source, source_id, chunk_idx)
);

-- IVF flat index for cosine distance — adequate up to ~100k rows.
-- Switch to HNSW once corpus grows past ~1M.
CREATE INDEX IF NOT EXISTS documents_embedding_ivfflat
    ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE INDEX IF NOT EXISTS documents_source_idx ON documents (source);
CREATE INDEX IF NOT EXISTS documents_metadata_gin ON documents USING gin (metadata);
