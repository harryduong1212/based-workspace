"""Live-Postgres integration tests for VectorStore.

Skipped automatically when the Postgres container isn't reachable, so this
file is safe to include in the default validate.py run.
"""
import unittest

import psycopg

from services.context_bridge.store import Document, VectorStore, _build_dsn_from_env


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


def _doc(source_id: str, chunk_idx: int, *, content: str = "x", meta: dict | None = None) -> Document:
    """Build a Document with a deterministic 384-dim embedding."""
    embedding = [0.0] * 384
    embedding[0] = float(chunk_idx)
    return Document(
        source="jira",
        source_id=source_id,
        chunk_idx=chunk_idx,
        content=content,
        embedding=embedding,
        metadata=meta or {"summary": content},
    )


@unittest.skipUnless(_postgres_reachable(), SKIP_REASON)
class UpsertIntegrationTest(unittest.TestCase):
    """Live-Postgres tests for upsert: row counts, idempotency, replacement."""

    SOURCE_IDS = ("ITEST-1", "ITEST-2")

    def setUp(self):
        self.vs = VectorStore()
        self.vs.init_schema()
        with self.vs.connect().cursor() as cur:
            cur.execute(
                "DELETE FROM documents WHERE source = 'jira' AND source_id = ANY(%s)",
                (list(self.SOURCE_IDS),),
            )
        self.vs.connect().commit()

    def tearDown(self):
        with self.vs.connect().cursor() as cur:
            cur.execute(
                "DELETE FROM documents WHERE source = 'jira' AND source_id = ANY(%s)",
                (list(self.SOURCE_IDS),),
            )
        self.vs.connect().commit()
        self.vs.close()

    def _count(self, source_id: str) -> int:
        with self.vs.connect().cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM documents WHERE source = 'jira' AND source_id = %s",
                (source_id,),
            )
            return cur.fetchone()[0]

    def test_upsert_inserts_chunks_and_returns_count(self):
        n = self.vs.upsert([_doc("ITEST-1", 0), _doc("ITEST-1", 1), _doc("ITEST-1", 2)])
        self.assertEqual(n, 3)
        self.assertEqual(self._count("ITEST-1"), 3)

    def test_re_upsert_smaller_replaces_old(self):
        """Stale higher-index chunks must be deleted on re-ingest."""
        self.vs.upsert([_doc("ITEST-1", i) for i in range(3)])
        self.assertEqual(self._count("ITEST-1"), 3)
        self.vs.upsert([_doc("ITEST-1", 0, content="new"), _doc("ITEST-1", 1, content="new")])
        self.assertEqual(self._count("ITEST-1"), 2)

    def test_re_upsert_larger_replaces_old(self):
        self.vs.upsert([_doc("ITEST-1", i) for i in range(2)])
        self.vs.upsert([_doc("ITEST-1", i) for i in range(4)])
        self.assertEqual(self._count("ITEST-1"), 4)

    def test_upsert_does_not_touch_other_source_ids(self):
        self.vs.upsert([_doc("ITEST-1", 0), _doc("ITEST-2", 0), _doc("ITEST-2", 1)])
        # Re-upsert ITEST-1 with one chunk; ITEST-2 must remain untouched.
        self.vs.upsert([_doc("ITEST-1", 0, content="updated")])
        self.assertEqual(self._count("ITEST-1"), 1)
        self.assertEqual(self._count("ITEST-2"), 2)

    def test_upsert_persists_metadata_and_embedding(self):
        self.vs.upsert([_doc("ITEST-1", 0, content="hello", meta={"status": "Open"})])
        with self.vs.connect().cursor() as cur:
            cur.execute(
                """
                SELECT content, metadata, embedding::text
                FROM documents WHERE source = 'jira' AND source_id = %s
                """,
                ("ITEST-1",),
            )
            row = cur.fetchone()
        self.assertEqual(row[0], "hello")
        self.assertEqual(row[1], {"status": "Open"})
        self.assertTrue(row[2].startswith("[0,"))


@unittest.skipUnless(_postgres_reachable(), SKIP_REASON)
class SearchIntegrationTest(unittest.TestCase):
    """Live-Postgres tests for search: ranking, k, source filter."""

    SOURCE_IDS = ("STEST-1", "STEST-2", "STEST-3", "STEST-BB-1")

    def _crafted_embedding(self, axis: int) -> list[float]:
        """384-dim one-hot at `axis`. Cosine distance is minimized when
        the query points along the same axis."""
        v = [0.0] * 384
        v[axis] = 1.0
        return v

    def setUp(self):
        self.vs = VectorStore()
        self.vs.init_schema()
        self._cleanup()
        # Seed three jira docs along axes 0/1/2, plus one bitbucket doc on axis 0.
        self.vs.upsert([
            Document("jira", "STEST-1", 0, "axis-0 doc", self._crafted_embedding(0), {"summary": "A"}),
            Document("jira", "STEST-2", 0, "axis-1 doc", self._crafted_embedding(1), {"summary": "B"}),
            Document("jira", "STEST-3", 0, "axis-2 doc", self._crafted_embedding(2), {"summary": "C"}),
            Document("bitbucket", "STEST-BB-1", 0, "bb axis-0", self._crafted_embedding(0), {"summary": "D"}),
        ])

    def tearDown(self):
        self._cleanup()
        self.vs.close()

    def _cleanup(self):
        with self.vs.connect().cursor() as cur:
            cur.execute(
                "DELETE FROM documents WHERE source_id = ANY(%s)",
                (list(self.SOURCE_IDS),),
            )
        self.vs.connect().commit()

    def test_top_result_is_axis_aligned(self):
        results = self.vs.search(self._crafted_embedding(1), k=3)
        self.assertGreater(len(results), 0)
        top_doc, top_dist = results[0]
        self.assertEqual(top_doc.source_id, "STEST-2")
        # axis-1 vs axis-1 is a perfect match — cosine distance ≈ 0.
        self.assertAlmostEqual(top_dist, 0.0, places=4)

    def test_results_ordered_by_ascending_distance(self):
        results = self.vs.search(self._crafted_embedding(0), k=4)
        distances = [d for _, d in results]
        self.assertEqual(distances, sorted(distances))

    def test_k_caps_result_count(self):
        results = self.vs.search(self._crafted_embedding(0), k=2)
        self.assertEqual(len(results), 2)

    def test_source_filter_excludes_other_connectors(self):
        results = self.vs.search(self._crafted_embedding(0), k=10, source="jira")
        self.assertTrue(all(d.source == "jira" for d, _ in results))

    def test_no_source_filter_returns_all_connectors(self):
        results = self.vs.search(self._crafted_embedding(0), k=10)
        sources = {d.source for d, _ in results}
        self.assertIn("jira", sources)
        self.assertIn("bitbucket", sources)


if __name__ == "__main__":
    unittest.main()
