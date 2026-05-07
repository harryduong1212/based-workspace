"""End-to-end ranking integration test for the Context Bridge.

Exercises connector → chunker → embedder → upsert → search through the
real llama-swap embedding model and a live Postgres + pgvector. Skips
cleanly when either piece is unreachable, so this file is safe to keep
in validate.py's default run.

Asserts that semantic ranking is *qualitatively* correct (top result
matches the obvious answer; off-topic ticket lands below on-topic
ones), not specific distance values — quantization or model swaps
shouldn't break the suite.
"""
import json
import unittest
import urllib.error
import urllib.request
from pathlib import Path

import psycopg

from services.context_bridge.cli import _build_docs
from services.context_bridge.connectors import jira
from services.context_bridge.embedder import Embedder
from services.context_bridge.store import VectorStore, _build_dsn_from_env


def _postgres_reachable() -> bool:
    try:
        with psycopg.connect(_build_dsn_from_env(), connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return True
    except Exception:
        return False


def _llama_swap_reachable() -> bool:
    """Probe the embedder endpoint at /v1/models. Doesn't load a model."""
    try:
        url = Embedder().base_url + "/models"
        with urllib.request.urlopen(url, timeout=2):
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return False


SKIP_REASON = (
    "Round-trip needs both Postgres (pgvector) and llama-swap reachable. "
    "Bring up: `podman compose -f infrastructure/core/docker-compose.yaml up -d based-workspace-postgres` "
    "and `podman compose -f infrastructure/llm/docker-compose.yaml up -d`."
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "jira_sample.json"
FIXTURE_SOURCE_IDS = ("PROJ-412", "PROJ-381", "PROJ-419")


@unittest.skipUnless(_postgres_reachable() and _llama_swap_reachable(), SKIP_REASON)
class IngestSearchRoundTripTest(unittest.TestCase):
    """Real round-trip: ingest the jira fixture with the live embedder, then query."""

    @classmethod
    def setUpClass(cls):
        """Ingest once; the search tests below all read from the same corpus."""
        cls.vs = VectorStore()
        cls.vs.init_schema()
        cls._wipe(cls)

        payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        docs = _build_docs(
            payload,
            "jira",
            target_tokens=512,
            embedder=Embedder(),
            adapter=jira.adapt,
        )
        assert docs, "fixture produced no documents — check jira_sample.json"
        cls.vs.upsert(docs)

    @classmethod
    def tearDownClass(cls):
        cls._wipe(cls)
        cls.vs.close()

    def _wipe(self):
        with self.vs.connect().cursor() as cur:
            cur.execute(
                "DELETE FROM documents WHERE source = 'jira' AND source_id = ANY(%s)",
                (list(FIXTURE_SOURCE_IDS),),
            )
        self.vs.connect().commit()

    def _embed(self, query: str) -> list[float]:
        [v] = Embedder().embed([query])
        return v

    def _search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        results = self.vs.search(self._embed(query), k=k, source="jira")
        return [(d.source_id, dist) for d, dist in results]

    def test_audit_log_query_ranks_proj_419_first(self):
        """PROJ-419 is the only ticket about audit logs — it should win cleanly."""
        results = self._search("audit log compliance session tokens", k=3)
        self.assertEqual(results[0][0], "PROJ-419")

    def test_rate_limiting_query_pushes_off_topic_ticket_last(self):
        """Both PROJ-381 (postmortem) and PROJ-412 (ticket) discuss rate
        limiting; PROJ-419 (audit logs) is off-topic and must rank last."""
        results = self._search("rate limiting per-tenant gateway", k=3)
        self.assertEqual(len(results), 3)
        ranking = [sid for sid, _ in results]
        self.assertEqual(ranking[-1], "PROJ-419")
        self.assertIn(ranking[0], {"PROJ-381", "PROJ-412"})

    def test_distances_strictly_ascending(self):
        """Smoke: pgvector ORDER BY actually orders, and distances are real."""
        results = self._search("rate limiting", k=3)
        distances = [d for _, d in results]
        self.assertEqual(distances, sorted(distances))


if __name__ == "__main__":
    unittest.main()
