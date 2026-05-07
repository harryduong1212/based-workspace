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

-- No vector index for now: ivfflat needs `lists ≈ rows / 1000` and
-- centroids trained on representative data. With a tiny MVP corpus and
-- `lists = 100`, default `probes = 1` only scans 1/100th of the index
-- and silently returns 0 rows. Seq-scan over a few thousand 384-dim
-- rows is microseconds. Switch to HNSW (or rebuild ivfflat with
-- calibrated `lists` after data exists) when the corpus grows past
-- ~10k rows. Drops the prior bad index if it exists.
DROP INDEX IF EXISTS documents_embedding_ivfflat;

CREATE INDEX IF NOT EXISTS documents_source_idx ON documents (source);
CREATE INDEX IF NOT EXISTS documents_metadata_gin ON documents USING gin (metadata);
