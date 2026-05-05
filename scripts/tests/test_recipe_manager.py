"""Tests for scripts.recipe_manager helpers — focus on _extract_section
fenced-block handling, the bug surfaced by the audit warnings layer,
and the _audit_text / _audit_warnings audit primitives."""

import unittest

from scripts.recipe_manager import (
    _extract_section,
    _audit_text,
    _audit_warnings,
)


class ExtractSectionBasicsTest(unittest.TestCase):
    def test_simple_section(self):
        body = "## Foo\nbody line\n## Bar\nother\n"
        self.assertEqual(_extract_section(body, "Foo"), "body line")

    def test_match_is_case_insensitive(self):
        body = "## Prompt\nhello\n"
        self.assertEqual(_extract_section(body, "prompt"), "hello")
        self.assertEqual(_extract_section(body, "PROMPT"), "hello")

    def test_section_at_end_of_body(self):
        body = "## Foo\nfirst\n## Bar\nlast line\nstill last"
        self.assertEqual(_extract_section(body, "Bar"), "last line\nstill last")

    def test_section_in_middle(self):
        body = "## A\nalpha\n## B\nbeta\n## C\ngamma\n"
        self.assertEqual(_extract_section(body, "B"), "beta")

    def test_missing_section_returns_none(self):
        body = "## Foo\nx\n## Bar\ny\n"
        self.assertIsNone(_extract_section(body, "Quux"))

    def test_empty_body_returns_none(self):
        self.assertIsNone(_extract_section("", "Foo"))

    def test_none_body_returns_none(self):
        self.assertIsNone(_extract_section(None, "Foo"))

    def test_title_whitespace_tolerated(self):
        body = "## Agent\nbody\n"
        self.assertEqual(_extract_section(body, "  Agent  "), "body")


class ExtractSectionFencedBlocksTest(unittest.TestCase):
    """The bug fixed in scripts/recipe_manager.py: section boundaries must
    not trigger on `##` lines that live inside fenced code blocks."""

    def test_hash_hash_inside_fenced_block_does_not_end_section(self):
        body = (
            "## Agent\n"
            "Phase 1.\n"
            "```\n"
            "## Summary\n"
            "<example template content>\n"
            "## Changes\n"
            "```\n"
            "Phase 2.\n"
            "## Next Section\n"
            "should be excluded\n"
        )
        result = _extract_section(body, "Agent")
        self.assertIn("Phase 1.", result)
        self.assertIn("## Summary", result)
        self.assertIn("## Changes", result)
        self.assertIn("Phase 2.", result)
        self.assertNotIn("should be excluded", result)

    def test_fence_with_language_tag(self):
        body = (
            "## Agent\n"
            "before\n"
            "```python\n"
            "## not a heading\n"
            "code = 1\n"
            "```\n"
            "after\n"
            "## Other\nx\n"
        )
        result = _extract_section(body, "Agent")
        self.assertIn("before", result)
        self.assertIn("## not a heading", result)
        self.assertIn("after", result)
        self.assertNotIn("Other", result)

    def test_unclosed_fence_swallows_rest(self):
        body = (
            "## Agent\n"
            "intro\n"
            "```\n"
            "## Sub\n"
            "## Stays\n"
        )
        result = _extract_section(body, "Agent")
        self.assertIn("## Sub", result)
        self.assertIn("## Stays", result)

    def test_indented_fence_marker_toggles(self):
        body = (
            "## Agent\n"
            "intro\n"
            "  ```\n"
            "  ## inside-indented-fence\n"
            "  ```\n"
            "outro\n"
            "## Next\nskip\n"
        )
        result = _extract_section(body, "Agent")
        self.assertIn("inside-indented-fence", result)
        self.assertIn("outro", result)
        self.assertNotIn("skip", result)

    def test_multiple_fenced_blocks_in_section(self):
        body = (
            "## Agent\n"
            "```\n## one\n```\n"
            "between\n"
            "```\n## two\n```\n"
            "## Done\nelsewhere\n"
        )
        result = _extract_section(body, "Agent")
        self.assertIn("## one", result)
        self.assertIn("between", result)
        self.assertIn("## two", result)
        self.assertNotIn("elsewhere", result)


class ExtractSectionRealRecipeShape(unittest.TestCase):
    """Mirrors the actual git-pr / release-notes shape that exposed the bug."""

    def test_recipe_with_phase_and_template_block(self):
        body = (
            "## What this does\nblurb\n\n"
            "## Agent\n\n"
            "### Phase 1 — Gather\n\n"
            "1. Run `git log {input.target}..HEAD --oneline`.\n\n"
            "### Phase 3 — Draft\n\n"
            "Default body structure:\n\n"
            "```\n"
            "## Summary\n"
            "## Changes\n"
            "## Related\n"
            "use {input.issue_number} if set\n"
            "```\n\n"
            "Title format: `<type>(<scope>): <summary>`.\n\n"
            "### Constraints\n\n"
            "- Do not invent.\n"
        )
        result = _extract_section(body, "Agent")
        self.assertIn("Phase 1", result)
        self.assertIn("{input.target}", result)
        self.assertIn("{input.issue_number}", result)
        self.assertIn("### Constraints", result)
        self.assertIn("Do not invent.", result)


class AuditTextTest(unittest.TestCase):
    """_audit_text scans a body chunk for hard errors: bare-{name} placeholder
    bugs, Claude-Code-specific phrases, and the auto-generated boilerplate
    stub footer."""

    def test_clean_text_returns_no_findings(self):
        text = "Procedure: do {input.thing}, then return."
        self.assertEqual(_audit_text(text, "body Agent", {"thing"}), [])

    def test_bare_placeholder_for_declared_input_flagged(self):
        text = "Write at .docs/{ticket_key}.md"
        out = _audit_text(text, "body Agent", {"ticket_key"})
        self.assertEqual(len(out), 1)
        self.assertIn("should be {input.ticket_key}", out[0])

    def test_bare_placeholder_for_undeclared_name_flagged_as_stray(self):
        text = "see {feature_slug}"
        out = _audit_text(text, "body Agent", {"feature"})
        self.assertEqual(len(out), 1)
        self.assertIn("stray placeholder-shaped token {feature_slug}", out[0])

    def test_at_brace_git_ref_syntax_not_flagged(self):
        # @{u} is git's "upstream branch" syntax — must not false-positive
        text = "git rev-parse @{u} 2>/dev/null"
        self.assertEqual(_audit_text(text, "body Agent", set()), [])

    def test_fenced_blocks_skipped_for_placeholder_scan(self):
        text = (
            "use {ticket_key} here\n"
            "```\n"
            "{remaining, reset_at}\n"
            "{another}\n"
            "```\n"
        )
        out = _audit_text(text, "body Agent", set())
        # bare {ticket_key} outside the fence fires; tokens inside the
        # fence (object-literal syntax + {another}) do not
        self.assertEqual(len(out), 1)
        self.assertIn("{ticket_key}", out[0])

    def test_task_tool_phrase_flagged_as_cc_specific(self):
        text = "Use Task tool with subagent_type=\"reviewer\""
        out = _audit_text(text, "skill foo", set())
        # both "Task tool" and "subagent_type=" trigger
        self.assertEqual(len(out), 2)
        self.assertTrue(any("Task tool" in e for e in out))
        self.assertTrue(any("subagent_type=" in e for e in out))

    def test_boilerplate_stub_phrase_flagged(self):
        text = "## When to Use\nThis skill is applicable to execute the workflow or actions described in the overview"
        out = _audit_text(text, "skill foo", set())
        self.assertEqual(len(out), 1)
        self.assertIn("boilerplate", out[0])

    def test_input_dotted_name_not_misread_as_bare_placeholder(self):
        text = "use {input.ticket_key} when set"
        self.assertEqual(_audit_text(text, "body Agent", {"ticket_key"}), [])


class AuditWarningsTest(unittest.TestCase):
    """_audit_warnings produces non-fatal hints: unreferenced inputs,
    oversized body sections."""

    def test_no_warnings_when_all_inputs_referenced(self):
        fm = {"inputs": [{"name": "target_branch"}, {"name": "focus"}]}
        body = "use {input.target_branch} and {input.focus}"
        self.assertEqual(_audit_warnings(fm, body, "body Agent"), [])

    def test_unreferenced_input_warns(self):
        fm = {"inputs": [{"name": "pr_id"}]}
        body = "the connector adapter injects PR data"
        out = _audit_warnings(fm, body, "body Prompt")
        self.assertEqual(len(out), 1)
        self.assertIn("'pr_id' declared but never substituted", out[0])

    def test_partial_reference_only_warns_for_missing(self):
        fm = {"inputs": [{"name": "a"}, {"name": "b"}, {"name": "c"}]}
        body = "use {input.a} and {input.c}"
        out = _audit_warnings(fm, body, "body Agent")
        self.assertEqual(len(out), 1)
        self.assertIn("'b'", out[0])

    def test_no_inputs_declared_no_warnings(self):
        fm = {"inputs": []}
        self.assertEqual(_audit_warnings(fm, "any body", "body Agent"), [])

    def test_inputs_field_missing_no_warnings(self):
        self.assertEqual(_audit_warnings({}, "any body", "body Agent"), [])

    def test_oversized_section_warns(self):
        fm = {"inputs": []}
        body = "\n".join("line " + str(i) for i in range(350))
        out = _audit_warnings(fm, body, "body Agent")
        self.assertEqual(len(out), 1)
        self.assertIn("dominate the dispatcher cache window", out[0])

    def test_section_at_threshold_does_not_warn(self):
        fm = {"inputs": []}
        body = "\n".join(["x"] * 300)  # exactly 300 lines
        self.assertEqual(_audit_warnings(fm, body, "body Agent"), [])

    def test_input_with_blank_name_ignored(self):
        fm = {"inputs": [{"name": ""}, {"name": "real"}]}
        body = "use {input.real}"
        self.assertEqual(_audit_warnings(fm, body, "body Agent"), [])


if __name__ == "__main__":
    unittest.main()
