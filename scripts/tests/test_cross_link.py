"""Tests for the pure helpers in scripts.cross_link.

The orchestration functions (process_connectors, process_skills,
collect_backrefs, resolve_skill_paths) walk the live tree and would
require fixtures or temp dirs; they're exercised by the validate.py
'Cross-link backrefs sync' check end-to-end.

These tests cover the string-manipulation helpers that decide what
gets written into each connector / skill body."""

import unittest

from scripts.cross_link import (
    render_section_body,
    update_existing_section,
    append_section,
)


class RenderSectionBodyTest(unittest.TestCase):
    def test_empty_list_renders_none_marker(self):
        out = render_section_body([])
        self.assertIn("(none", out)
        self.assertTrue(out.endswith("\n"))

    def test_single_recipe_renders_one_bullet(self):
        out = render_section_body(["git-pr"])
        self.assertEqual(out, "- `git-pr`\n")

    def test_multiple_recipes_render_in_given_order(self):
        out = render_section_body(["zeta", "alpha", "mike"])
        # the helper preserves caller-supplied ordering — sorting happens upstream
        self.assertEqual(out, "- `zeta`\n- `alpha`\n- `mike`\n")


class UpdateExistingSectionTest(unittest.TestCase):
    def test_replaces_body_of_existing_section(self):
        original = (
            "# Title\n\n"
            "## What this is\nA connector.\n\n"
            "## Used by recipes\n"
            "- `old-stale`\n\n"
        )
        new_content, replaced = update_existing_section(original, ["a", "b"])
        self.assertTrue(replaced)
        self.assertIn("- `a`\n- `b`\n", new_content)
        self.assertNotIn("old-stale", new_content)
        self.assertIn("## What this is\nA connector.", new_content)

    def test_replace_preserves_section_order(self):
        original = (
            "## Used by recipes\n- `x`\n\n"
            "## Trailing section\nstays put\n"
        )
        new_content, replaced = update_existing_section(original, ["only"])
        self.assertTrue(replaced)
        self.assertIn("## Used by recipes\n- `only`\n", new_content)
        self.assertIn("## Trailing section\nstays put", new_content)

    def test_no_existing_section_returns_unchanged_with_false(self):
        original = "# Heading\n\n## Other\nbody\n"
        new_content, replaced = update_existing_section(original, ["a"])
        self.assertFalse(replaced)
        self.assertEqual(new_content, original)

    def test_empty_recipe_list_writes_none_marker(self):
        original = "## Used by recipes\n- `x`\n- `y`\n"
        new_content, replaced = update_existing_section(original, [])
        self.assertTrue(replaced)
        self.assertIn("(none", new_content)
        self.assertNotIn("- `x`", new_content)


class AppendSectionTest(unittest.TestCase):
    def test_appends_to_content_with_single_trailing_newline(self):
        original = "# Skill\n\nbody text\n"
        out = append_section(original, ["recipe-a"])
        self.assertTrue(out.startswith(original))
        self.assertIn("\n## Used by recipes\n- `recipe-a`\n", out)

    def test_appends_to_content_without_trailing_newline(self):
        original = "no trailing newline"
        out = append_section(original, ["r"])
        self.assertIn("\n\n## Used by recipes\n- `r`\n", out)

    def test_appends_to_content_with_double_trailing_newline(self):
        original = "body\n\n"
        out = append_section(original, ["r"])
        # already has the blank-line gap; should not insert a third newline
        self.assertEqual(out.count("\n\n## Used by recipes"), 1)
        self.assertNotIn("\n\n\n## Used by recipes", out)

    def test_empty_recipe_list_appends_none_marker(self):
        out = append_section("body\n", [])
        self.assertIn("## Used by recipes\n", out)
        self.assertIn("(none", out)


if __name__ == "__main__":
    unittest.main()
