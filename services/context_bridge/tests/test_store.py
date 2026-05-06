"""Unit tests for VectorStore — DSN resolution and connection lifecycle.

Live-Postgres tests live in test_store_integration.py and skip when the
container is not reachable.
"""
import os
import unittest
from unittest import mock

from services.context_bridge.store import VectorStore, _build_dsn_from_env


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


if __name__ == "__main__":
    unittest.main()
