"""Unit tests for VectorStore — DSN resolution and connection lifecycle.

Live-Postgres tests live in test_store_integration.py and skip when the
container is not reachable.
"""
import os
import unittest
from unittest import mock

from services.context_bridge.store import (
    Document,
    VectorStore,
    _build_dsn_from_env,
    _vector_literal,
)


class _PgEnvScope:
    KEYS = ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "POSTGRES_HOST", "POSTGRES_PORT")

    def __enter__(self):
        self.saved = {k: os.environ.get(k) for k in self.KEYS}
        for k in self.KEYS:
            os.environ.pop(k, None)
        return self

    def __exit__(self, *exc):
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


class DsnFromEnvTest(unittest.TestCase):
    def test_uses_env_vars(self):
        with _PgEnvScope():
            os.environ.update({
                "POSTGRES_USER": "alice",
                "POSTGRES_PASSWORD": "s3cret",
                "POSTGRES_DB": "ai_memory",
                "POSTGRES_HOST": "db.local",
                "POSTGRES_PORT": "6543",
            })
            self.assertEqual(
                _build_dsn_from_env(),
                "postgresql://alice:s3cret@db.local:6543/ai_memory",
            )

    def test_defaults_when_unset(self):
        with _PgEnvScope():
            self.assertEqual(
                _build_dsn_from_env(),
                "postgresql://postgres:@localhost:5432/postgres",
            )


class VectorStoreDsnTest(unittest.TestCase):
    def test_explicit_dsn_overrides_env(self):
        with _PgEnvScope():
            os.environ["POSTGRES_USER"] = "from-env"
            vs = VectorStore(dsn="postgresql://override@h/d")
            self.assertEqual(vs.dsn, "postgresql://override@h/d")

    def test_falls_back_to_env(self):
        with _PgEnvScope():
            os.environ["POSTGRES_USER"] = "from-env"
            os.environ["POSTGRES_DB"] = "ai_memory"
            vs = VectorStore()
            self.assertIn("from-env", vs.dsn)
            self.assertIn("/ai_memory", vs.dsn)


class VectorStoreLifecycleTest(unittest.TestCase):
    """Connection lifecycle with psycopg.connect mocked out."""

    def test_connect_calls_psycopg_connect_with_dsn(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake = mock.MagicMock()
            fake.closed = False
            m.return_value = fake
            conn = vs.connect()
            m.assert_called_once_with("postgresql://x@h/d")
            self.assertIs(conn, fake)

    def test_connect_is_idempotent_when_open(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake = mock.MagicMock()
            fake.closed = False
            m.return_value = fake
            vs.connect()
            vs.connect()
            self.assertEqual(m.call_count, 1)

    def test_connect_reopens_when_closed(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            first = mock.MagicMock(); first.closed = True
            second = mock.MagicMock(); second.closed = False
            m.side_effect = [first, second]
            vs.connect()
            new = vs.connect()
            self.assertEqual(m.call_count, 2)
            self.assertIs(new, second)

    def test_close_closes_open_connection(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake = mock.MagicMock(); fake.closed = False
            m.return_value = fake
            vs.connect()
            vs.close()
            fake.close.assert_called_once()
            self.assertIsNone(vs._conn)

    def test_close_is_safe_when_unconnected(self):
        VectorStore(dsn="postgresql://x@h/d").close()  # should not raise

    def test_context_manager_opens_and_closes(self):
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake = mock.MagicMock(); fake.closed = False
            m.return_value = fake
            with VectorStore(dsn="postgresql://x@h/d") as vs:
                self.assertIs(vs._conn, fake)
            fake.close.assert_called_once()


class InitSchemaUnitTest(unittest.TestCase):
    """init_schema executes the SQL file and commits."""

    def test_executes_schema_file_and_commits(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn = mock.MagicMock(); fake_conn.closed = False
            fake_cur = mock.MagicMock()
            fake_conn.cursor.return_value.__enter__.return_value = fake_cur
            m.return_value = fake_conn

            vs.init_schema()

            args, _ = fake_cur.execute.call_args
            sql = args[0]
            self.assertIn("CREATE EXTENSION IF NOT EXISTS vector", sql)
            self.assertIn("CREATE TABLE IF NOT EXISTS documents", sql)
            self.assertIn("ivfflat", sql)
            fake_conn.commit.assert_called_once()


class VectorLiteralTest(unittest.TestCase):
    def test_formats_floats_into_pgvector_text(self):
        self.assertEqual(_vector_literal([0.1, 0.2, 0.3]), "[0.1,0.2,0.3]")

    def test_coerces_ints_to_float(self):
        self.assertEqual(_vector_literal([1, 2, 3]), "[1.0,2.0,3.0]")

    def test_empty_embedding(self):
        self.assertEqual(_vector_literal([]), "[]")


def _doc(source="jira", source_id="ABC-1", chunk_idx=0, content="c", embedding=None, metadata=None):
    return Document(
        source=source,
        source_id=source_id,
        chunk_idx=chunk_idx,
        content=content,
        embedding=embedding if embedding is not None else [0.0, 0.1, 0.2],
        metadata=metadata or {},
    )


def _mock_conn():
    """psycopg.connect mock that supports cursor() and transaction() context managers."""
    fake_conn = mock.MagicMock()
    fake_conn.closed = False
    fake_cur = mock.MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cur
    return fake_conn, fake_cur


class UpsertUnitTest(unittest.TestCase):
    """upsert: deterministic delete-then-insert per (source, source_id) group."""

    def test_empty_input_is_noop(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            self.assertEqual(vs.upsert([]), 0)
            m.assert_not_called()

    def test_returns_total_doc_count(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, _ = _mock_conn()
            m.return_value = fake_conn
            n = vs.upsert([_doc(chunk_idx=0), _doc(chunk_idx=1), _doc(chunk_idx=2)])
            self.assertEqual(n, 3)

    def test_groups_by_source_and_source_id(self):
        """Two source_ids → two DELETEs and two executemany calls."""
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = _mock_conn()
            m.return_value = fake_conn
            vs.upsert([
                _doc(source_id="A-1", chunk_idx=0),
                _doc(source_id="A-1", chunk_idx=1),
                _doc(source_id="B-2", chunk_idx=0),
            ])
            delete_calls = [c for c in fake_cur.execute.call_args_list if "DELETE" in c.args[0]]
            self.assertEqual(len(delete_calls), 2)
            self.assertEqual(fake_cur.executemany.call_count, 2)

    def test_delete_runs_before_insert_within_group(self):
        """For a given (source, source_id), DELETE must be issued before INSERT."""
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = _mock_conn()
            ordered: list[str] = []
            fake_cur.execute.side_effect = lambda sql, *a, **kw: ordered.append(("execute", sql.strip()[:6]))
            fake_cur.executemany.side_effect = lambda sql, *a, **kw: ordered.append(("executemany", sql.strip()[:6]))
            m.return_value = fake_conn
            vs.upsert([_doc(source_id="A-1", chunk_idx=0), _doc(source_id="A-1", chunk_idx=1)])
            kinds = [k for k, _ in ordered]
            self.assertEqual(kinds[0], "execute")
            self.assertEqual(kinds[1], "executemany")

    def test_runs_inside_one_transaction(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, _ = _mock_conn()
            m.return_value = fake_conn
            vs.upsert([_doc(), _doc(source_id="B-2")])
            fake_conn.transaction.assert_called_once()

    def test_embedding_serialized_as_pgvector_literal(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = _mock_conn()
            m.return_value = fake_conn
            vs.upsert([_doc(embedding=[0.5, -0.25, 0.0])])
            args, _ = fake_cur.executemany.call_args
            rows = args[1]
            self.assertEqual(rows[0][4], "[0.5,-0.25,0.0]")

    def test_metadata_serialized_as_json(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = _mock_conn()
            m.return_value = fake_conn
            vs.upsert([_doc(metadata={"status": "Open", "assignee": "alice"})])
            args, _ = fake_cur.executemany.call_args
            rows = args[1]
            import json as _json
            self.assertEqual(_json.loads(rows[0][5]), {"status": "Open", "assignee": "alice"})

    def test_none_metadata_becomes_empty_object(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = _mock_conn()
            m.return_value = fake_conn
            d = _doc()
            d.metadata = None
            vs.upsert([d])
            args, _ = fake_cur.executemany.call_args
            self.assertEqual(args[1][0][5], "{}")


class SearchUnitTest(unittest.TestCase):
    """search: SQL shape, parameter binding, result mapping."""

    def _setup(self, rows):
        fake_conn, fake_cur = _mock_conn()
        fake_cur.fetchall.return_value = rows
        return fake_conn, fake_cur

    def test_empty_query_short_circuits_to_empty_list(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            self.assertEqual(vs.search([]), [])
            m.assert_not_called()

    def test_executes_with_vector_literal_and_k(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = self._setup([])
            m.return_value = fake_conn
            vs.search([0.1, 0.2, 0.3], k=7)
            args, _ = fake_cur.execute.call_args
            sql, params = args[0], args[1]
            self.assertEqual(params["v"], "[0.1,0.2,0.3]")
            self.assertEqual(params["k"], 7)
            self.assertIn("ORDER BY embedding <=> %(v)s::vector", sql)
            self.assertIn("LIMIT %(k)s", sql)

    def test_default_k_is_5(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = self._setup([])
            m.return_value = fake_conn
            vs.search([0.1, 0.2])
            self.assertEqual(fake_cur.execute.call_args.args[1]["k"], 5)

    def test_no_source_filter_omits_where_clause(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = self._setup([])
            m.return_value = fake_conn
            vs.search([0.1])
            sql, params = fake_cur.execute.call_args.args
            self.assertNotIn("WHERE", sql)
            self.assertNotIn("source", params)

    def test_source_filter_adds_where_and_param(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, fake_cur = self._setup([])
            m.return_value = fake_conn
            vs.search([0.1], source="jira")
            sql, params = fake_cur.execute.call_args.args
            self.assertIn("WHERE source = %(source)s", sql)
            self.assertEqual(params["source"], "jira")

    def test_returns_documents_paired_with_distances(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, _ = self._setup([
                ("jira", "PROJ-1", 0, "first", {"summary": "A"}, 0.12),
                ("jira", "PROJ-2", 1, "second", {"summary": "B"}, 0.34),
            ])
            m.return_value = fake_conn
            results = vs.search([0.1, 0.2], k=2)
            self.assertEqual(len(results), 2)
            d1, dist1 = results[0]
            self.assertEqual(d1.source, "jira")
            self.assertEqual(d1.source_id, "PROJ-1")
            self.assertEqual(d1.chunk_idx, 0)
            self.assertEqual(d1.content, "first")
            self.assertEqual(d1.metadata, {"summary": "A"})
            self.assertEqual(d1.embedding, [])  # not round-tripped
            self.assertAlmostEqual(dist1, 0.12)
            self.assertAlmostEqual(results[1][1], 0.34)

    def test_null_metadata_becomes_empty_dict(self):
        vs = VectorStore(dsn="postgresql://x@h/d")
        with mock.patch("services.context_bridge.store.psycopg.connect") as m:
            fake_conn, _ = self._setup([
                ("jira", "PROJ-1", 0, "x", None, 0.1),
            ])
            m.return_value = fake_conn
            results = vs.search([0.1])
            self.assertEqual(results[0][0].metadata, {})


if __name__ == "__main__":
    unittest.main()
