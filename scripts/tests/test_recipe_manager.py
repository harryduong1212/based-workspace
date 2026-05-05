"""Tests for scripts.recipe_manager helpers — focus on _extract_section
fenced-block handling, the bug surfaced by the audit warnings layer."""

import unittest

from scripts.recipe_manager import _extract_section


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


if __name__ == "__main__":
    unittest.main()
