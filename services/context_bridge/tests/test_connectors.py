"""Unit tests for connector adapters — payload → (source_id, content, metadata).

Tests the two adapters together so they stay structurally aligned. The
real-fixture parsing for both connectors is already covered by
test_cli.BuildDocsWithRealAdapterTest (jira) and the round-trip test;
this file pins the contract: skip records missing IDs, preserve
content order, populate metadata.
"""
from __future__ import annotations

import unittest

from services.context_bridge.connectors import bitbucket, jira


class JiraAdapterTest(unittest.TestCase):
    def test_empty_payload_yields_nothing(self):
        self.assertEqual(list(jira.adapt({})), [])
        self.assertEqual(list(jira.adapt({"issues": []})), [])

    def test_skips_issues_without_key(self):
        payload = {"issues": [{"fields": {"summary": "no key"}}]}
        self.assertEqual(list(jira.adapt(payload)), [])

    def test_minimal_issue_yields_summary_only(self):
        payload = {"issues": [{"key": "X-1", "fields": {"summary": "hi"}}]}
        [(sid, content, meta)] = list(jira.adapt(payload))
        self.assertEqual(sid, "X-1")
        self.assertEqual(content, "hi")
        self.assertEqual(meta["summary"], "hi")
        self.assertIsNone(meta["status"])
        self.assertIsNone(meta["assignee"])

    def test_full_issue_concatenates_summary_description_and_comments(self):
        payload = {"issues": [{
            "key": "X-1",
            "fields": {
                "summary": "S",
                "description": "D",
                "status": {"name": "Open"},
                "assignee": {"displayName": "Alice"},
                "comment": {"comments": [
                    {"author": {"displayName": "Bob"}, "body": "c1"},
                    {"author": {"displayName": "Alice"}, "body": "c2"},
                ]},
            },
        }]}
        [(_, content, meta)] = list(jira.adapt(payload))
        self.assertIn("S", content)
        self.assertIn("D", content)
        self.assertIn("Bob: c1", content)
        self.assertIn("Alice: c2", content)
        self.assertEqual(meta, {"summary": "S", "status": "Open", "assignee": "Alice"})


class BitbucketAdapterTest(unittest.TestCase):
    def test_empty_payload_yields_nothing(self):
        self.assertEqual(list(bitbucket.adapt({})), [])
        self.assertEqual(list(bitbucket.adapt({"values": []})), [])

    def test_skips_prs_without_id(self):
        payload = {"values": [{"title": "no id"}]}
        self.assertEqual(list(bitbucket.adapt(payload)), [])

    def test_int_id_coerced_to_string_for_source_id(self):
        """source_id is TEXT in the schema — Bitbucket's int IDs must be stringified."""
        payload = {"values": [{"id": 287, "title": "t", "description": "d"}]}
        [(sid, _, _)] = list(bitbucket.adapt(payload))
        self.assertEqual(sid, "287")

    def test_minimal_pr_yields_title_only(self):
        payload = {"values": [{"id": 1, "title": "T"}]}
        [(sid, content, meta)] = list(bitbucket.adapt(payload))
        self.assertEqual(sid, "1")
        self.assertEqual(content, "T")
        self.assertEqual(meta["title"], "T")
        self.assertIsNone(meta["state"])
        self.assertIsNone(meta["author"])
        self.assertIsNone(meta["branch"])

    def test_full_pr_populates_metadata(self):
        payload = {"values": [{
            "id": 287,
            "title": "Migrate auth",
            "description": "Body",
            "state": "OPEN",
            "author": {"display_name": "Carol"},
            "source": {"branch": {"name": "feat/auth"}},
        }]}
        [(_, content, meta)] = list(bitbucket.adapt(payload))
        self.assertIn("Migrate auth", content)
        self.assertIn("Body", content)
        self.assertEqual(meta, {
            "title": "Migrate auth",
            "state": "OPEN",
            "author": "Carol",
            "branch": "feat/auth",
        })

    def test_inlined_comments_are_concatenated(self):
        """Bitbucket Cloud comments live on a separate endpoint, but if a
        caller pre-merged them into the PR dict we accept either shape."""
        payload = {"values": [{
            "id": 1,
            "title": "T",
            "comments": [
                {"user": {"display_name": "Bob"}, "content": {"raw": "looks good"}},
                {"user": {"display_name": "Alice"}, "body": "ship it"},  # alt shape
            ],
        }]}
        [(_, content, _)] = list(bitbucket.adapt(payload))
        self.assertIn("Bob: looks good", content)
        self.assertIn("Alice: ship it", content)

    def test_real_fixture_parses(self):
        import json
        from pathlib import Path
        fixture = Path(__file__).parent / "fixtures" / "bitbucket_sample.json"
        payload = json.loads(fixture.read_text())
        results = list(bitbucket.adapt(payload))
        self.assertEqual({sid for sid, _, _ in results}, {"287", "251"})
        # Both fixture PRs have a description — content should be non-trivial.
        for _, content, _ in results:
            self.assertGreater(len(content), 50)


if __name__ == "__main__":
    unittest.main()
