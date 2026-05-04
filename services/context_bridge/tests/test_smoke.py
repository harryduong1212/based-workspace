"""Smoke test placeholder — Phase F.2 wires the real round-trip.

The eventual test will:
    1. init_schema() against a test Postgres
    2. ingest jira_sample.json
    3. search "rate limiting" — assert PROJ-412 ranks first

For now: just verify the package imports cleanly and the fixtures parse.
"""
import json
from pathlib import Path


def test_package_imports():
    from services.context_bridge import cli, embedder, store
    from services.context_bridge.chunkers import sentence
    from services.context_bridge.connectors import jira, bitbucket
    assert cli.main is not None
    assert embedder.Embedder.DIMENSION == 384
    assert store.VectorStore is not None


def test_fixtures_parse():
    fdir = Path(__file__).parent / "fixtures"
    jira = json.loads((fdir / "jira_sample.json").read_text())
    bb = json.loads((fdir / "bitbucket_sample.json").read_text())
    assert len(jira["issues"]) == 3
    assert len(bb["values"]) == 2
