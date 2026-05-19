"""Tests for indexer.parse_skill_md + walk_skills + stable_point_id.

Uses a temp directory with a tiny fake `.archived/skills/<cat>/<skill>/SKILL.md`
tree — no fixtures committed to the repo, no network.
"""
from __future__ import annotations

import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from services.skill_discovery_mcp.indexer import (
    SkillDoc,
    index_skills,
    parse_skill_md,
    stable_point_id,
    walk_skills,
)


def _skill_md(name: str, description: str, body: str = "extra body text") -> str:
    return textwrap.dedent(
        f"""\
        ---
        name: {name}
        description: "{description}"
        risk: low
        source: community
        date_added: "2026-05-18"
        ---

        # {name.title()}

        {body}
        """
    )


class ParseSkillMdTests(unittest.TestCase):
    def test_happy_path(self) -> None:
        doc = parse_skill_md(
            _skill_md("vector-database-engineer", "Expert in vector databases."),
            path=".archived/skills/data-vector/vector-database-engineer/SKILL.md",
            category="data-vector",
        )
        self.assertIsNotNone(doc)
        assert doc is not None  # narrow for mypy/pylance
        self.assertEqual(doc.name, "vector-database-engineer")
        self.assertEqual(doc.description, "Expert in vector databases.")
        self.assertEqual(doc.category, "data-vector")
        self.assertEqual(doc.risk, "low")
        self.assertEqual(doc.source, "community")
        self.assertIn("Expert in vector databases.", doc.text_for_embedding)

    def test_missing_frontmatter_returns_none(self) -> None:
        self.assertIsNone(parse_skill_md("just a body, no frontmatter", path="x", category="c"))

    def test_unterminated_frontmatter_returns_none(self) -> None:
        bad = "---\nname: thing\ndescription: x\n"  # missing closing ---
        self.assertIsNone(parse_skill_md(bad, path="x", category="c"))

    def test_invalid_yaml_returns_none(self) -> None:
        bad = "---\n: : :\n---\nbody\n"
        self.assertIsNone(parse_skill_md(bad, path="x", category="c"))

    def test_missing_name_or_description_returns_none(self) -> None:
        no_name = "---\ndescription: only desc\n---\nbody\n"
        no_desc = "---\nname: only-name\n---\nbody\n"
        self.assertIsNone(parse_skill_md(no_name, path="x", category="c"))
        self.assertIsNone(parse_skill_md(no_desc, path="x", category="c"))

    def test_body_excerpt_is_trimmed(self) -> None:
        long_body = "x" * 5000
        doc = parse_skill_md(
            _skill_md("trim", "desc", body=long_body),
            path="x",
            category="c",
        )
        assert doc is not None
        self.assertLessEqual(len(doc.body_excerpt), 800)


class WalkSkillsTests(unittest.TestCase):
    def test_walks_two_categories(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for cat, skill, desc in [
                ("data-vector", "vector-database-engineer", "Vector DB expert."),
                ("frontend-core", "react-best-practices", "React patterns."),
            ]:
                (root / cat / skill).mkdir(parents=True)
                (root / cat / skill / "SKILL.md").write_text(_skill_md(skill, desc))

            docs = list(walk_skills(root))
            names = {d.name for d in docs}
            self.assertEqual(names, {"vector-database-engineer", "react-best-practices"})
            cats = {d.name: d.category for d in docs}
            self.assertEqual(cats["vector-database-engineer"], "data-vector")

    def test_skips_dirs_without_skill_md(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "empty-cat" / "no-skill-here").mkdir(parents=True)  # no SKILL.md
            (root / "good" / "ok").mkdir(parents=True)
            (root / "good" / "ok" / "SKILL.md").write_text(_skill_md("ok", "fine"))

            docs = list(walk_skills(root))
            self.assertEqual([d.name for d in docs], ["ok"])

    def test_skips_unreadable_or_bad_frontmatter(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "cat" / "bad").mkdir(parents=True)
            (root / "cat" / "bad" / "SKILL.md").write_text("no frontmatter here")
            (root / "cat" / "good").mkdir(parents=True)
            (root / "cat" / "good" / "SKILL.md").write_text(_skill_md("good", "y"))

            docs = list(walk_skills(root))
            self.assertEqual([d.name for d in docs], ["good"])

    def test_missing_root_yields_nothing(self) -> None:
        with TemporaryDirectory() as tmp:
            self.assertEqual(list(walk_skills(Path(tmp) / "nope")), [])

    def test_index_skills_returns_list(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "c" / "s").mkdir(parents=True)
            (root / "c" / "s" / "SKILL.md").write_text(_skill_md("s", "d"))
            result = index_skills(root)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)


class StablePointIdTests(unittest.TestCase):
    def test_is_deterministic_and_positive(self) -> None:
        doc = SkillDoc(
            name="x", description="y", category="c", path="p",
            risk="r", source="s", body_excerpt="b",
        )
        a = stable_point_id(doc)
        b = stable_point_id(doc)
        self.assertEqual(a, b)
        self.assertGreaterEqual(a, 0)
        self.assertLess(a, 1 << 63)

    def test_differs_per_skill(self) -> None:
        d1 = SkillDoc(name="a", description="x", category="c", path="p", risk="r", source="s", body_excerpt="")
        d2 = SkillDoc(name="b", description="x", category="c", path="p", risk="r", source="s", body_excerpt="")
        self.assertNotEqual(stable_point_id(d1), stable_point_id(d2))

    def test_differs_per_category(self) -> None:
        d1 = SkillDoc(name="x", description="y", category="cat-a", path="p", risk="r", source="s", body_excerpt="")
        d2 = SkillDoc(name="x", description="y", category="cat-b", path="p", risk="r", source="s", body_excerpt="")
        self.assertNotEqual(stable_point_id(d1), stable_point_id(d2))


if __name__ == "__main__":
    unittest.main()
