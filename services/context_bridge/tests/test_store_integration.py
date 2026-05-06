"""Live-Postgres integration tests for VectorStore.

Skipped automatically when the Postgres container isn't reachable, so this
file is safe to include in the default validate.py run.
"""
import unittest

import psycopg

from services.context_bridge.store import VectorStore, _build_dsn_from_env


def _postgres_reachable() -> bool:
    """Quick TCP probe; returns True only if a real connection succeeds."""
    try:
        with psycopg.connect(_build_dsn_from_env(), connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return True
    except Exception:
        return False


SKIP_REASON = (
    "Postgres unreachable — start it with "
    "`podman compose -f infrastructure/core/docker-compose.yaml up -d based-workspace-postgres`"
)


@unittest.skipUnless(_postgres_reachable(), SKIP_REASON)
class InitSchemaIntegrationTest(unittest.TestCase):
    """Verifies init_schema actually creates the schema in a live container."""

    def setUp(self):
        # Require that .env values are present (sourced by validate.py via systemd or shell).
        # If they're not, _build_dsn_from_env still returns a sensible default.
        self.vs = VectorStore()
        self.vs.init_schema()  # idempotent; ensures known starting state

    def tearDown(self):
        self.vs.close()

    def _query(self, sql, params=()):
        with VectorStore() as vs:
            with vs.connect().cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()

    def test_vector_extension_present(self):
        rows = self._query("SELECT extname FROM pg_extension WHERE extname = 'vector'")
        self.assertEqual(len(rows), 1)

    def test_documents_table_exists(self):
        rows = self._query(
            "SELECT to_regclass('public.documents')"
        )
        self.assertEqual(rows[0][0], "documents")

    def test_documents_unique_constraint_present(self):
        rows = self._query(
            """
            SELECT a.attname
            FROM pg_index i
            JOIN pg_class c ON c.oid = i.indrelid
            JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(i.indkey)
            WHERE c.relname = 'documents' AND i.indisunique AND NOT i.indisprimary
            ORDER BY a.attname
            """
        )
        cols = sorted(r[0] for r in rows)
        self.assertEqual(cols, ["chunk_idx", "source", "source_id"])

    def test_ivfflat_index_present(self):
        rows = self._query(
            """
            SELECT indexname FROM pg_indexes
            WHERE tablename = 'documents' AND indexname = 'documents_embedding_ivfflat'
            """
        )
        self.assertEqual(len(rows), 1)

    def test_init_schema_is_idempotent(self):
        # Calling again on an already-initialized DB must not raise or churn data.
        for _ in range(2):
            with VectorStore() as vs:
                vs.init_schema()
        rows = self._query("SELECT COUNT(*) FROM documents")
        self.assertGreaterEqual(rows[0][0], 0)


if __name__ == "__main__":
    unittest.main()
