"""Tests for scripts.connector_manager — focus on lint_connector since
that's the validation surface the CLI exposes via `connector_manager.py lint`."""

import unittest
from pathlib import Path

from scripts.connector_manager import lint_connector, REQUIRED_FIELDS


def _valid_fm():
    return {
        "id": "jira",
        "name": "Jira",
        "description": "Atlassian Jira issue tracking and project management.",
        "status": "experimental",
        "provides": ["issues", "projects"],
        "auth_type": "api_token",
        "requires_env": ["JIRA_BASE_URL", "JIRA_API_TOKEN"],
    }


class LintConnectorBaselineTest(unittest.TestCase):
    def setUp(self):
        self.path = Path("connectors/jira.md")

    def test_valid_frontmatter_passes(self):
        self.assertEqual(lint_connector(self.path, _valid_fm(), None), [])

    def test_parse_error_propagated_short_circuits(self):
        errs = lint_connector(self.path, {}, "YAML parse failure")
        self.assertEqual(errs, ["YAML parse failure"])


class LintConnectorRequiredFieldsTest(unittest.TestCase):
    def setUp(self):
        self.path = Path("connectors/jira.md")

    def test_each_required_field_missing_produces_one_error(self):
        for field in REQUIRED_FIELDS:
            with self.subTest(field=field):
                fm = _valid_fm()
                fm.pop(field)
                errs = lint_connector(self.path, fm, None)
                self.assertTrue(
                    any(f"missing required field: {field}" in e for e in errs),
                    f"expected missing-field error for {field}; got {errs}",
                )

    def test_empty_string_required_field_treated_as_missing(self):
        fm = _valid_fm()
        fm["name"] = ""
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("missing required field: name" in e for e in errs))

    def test_empty_list_required_field_treated_as_missing(self):
        fm = _valid_fm()
        fm["provides"] = []
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("missing required field: provides" in e for e in errs))


class LintConnectorEnumsTest(unittest.TestCase):
    def setUp(self):
        self.path = Path("connectors/jira.md")

    def test_id_must_match_filename_stem(self):
        fm = _valid_fm()
        fm["id"] = "bitbucket"
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("does not match filename stem" in e for e in errs))

    def test_invalid_status_rejected(self):
        fm = _valid_fm()
        fm["status"] = "released"
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("status must be one of" in e for e in errs))

    def test_invalid_auth_type_rejected(self):
        fm = _valid_fm()
        fm["auth_type"] = "magic"
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("auth_type must be one of" in e for e in errs))

    def test_each_valid_status_passes(self):
        for status in ("experimental", "stable", "deprecated"):
            with self.subTest(status=status):
                fm = _valid_fm()
                fm["status"] = status
                self.assertEqual(lint_connector(self.path, fm, None), [])

    def test_each_valid_auth_type_passes(self):
        for auth in ("api_token", "oauth2", "basic", "bearer", "none"):
            with self.subTest(auth=auth):
                fm = _valid_fm()
                fm["auth_type"] = auth
                self.assertEqual(lint_connector(self.path, fm, None), [])


class LintConnectorTypeShapeTest(unittest.TestCase):
    def setUp(self):
        self.path = Path("connectors/jira.md")

    def test_provides_must_be_list(self):
        fm = _valid_fm()
        fm["provides"] = "issues"
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("provides must be a list" in e for e in errs))

    def test_requires_env_must_be_list(self):
        fm = _valid_fm()
        fm["requires_env"] = "JIRA_API_TOKEN"
        errs = lint_connector(self.path, fm, None)
        self.assertTrue(any("requires_env must be a list" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
