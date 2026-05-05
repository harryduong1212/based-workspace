"""Unit tests for services.recipe_runtime.prompt_assembler."""
import unittest

from services.recipe_runtime.prompt_assembler import assemble, substitute_inputs


class SubstituteInputsTest(unittest.TestCase):
    def test_single_placeholder(self):
        out, applied = substitute_inputs("Hello {input.name}", {"name": "world"})
        self.assertEqual(out, "Hello world")
        self.assertEqual(applied, {"name": "world"})

    def test_multiple_placeholders(self):
        out, applied = substitute_inputs(
            "{input.greeting}, {input.name}!",
            {"greeting": "Hi", "name": "Linh"},
        )
        self.assertEqual(out, "Hi, Linh!")
        self.assertEqual(applied, {"greeting": "Hi", "name": "Linh"})

    def test_repeated_placeholder(self):
        out, applied = substitute_inputs(
            "{input.x} and {input.x} again",
            {"x": "hello"},
        )
        self.assertEqual(out, "hello and hello again")
        self.assertEqual(applied, {"x": "hello"})

    def test_missing_input_becomes_empty(self):
        out, applied = substitute_inputs("before {input.absent} after", {})
        self.assertEqual(out, "before  after")
        self.assertEqual(applied, {"absent": ""})

    def test_no_placeholders_unchanged(self):
        out, applied = substitute_inputs("plain text", {"unused": "x"})
        self.assertEqual(out, "plain text")
        self.assertEqual(applied, {})

    def test_empty_string(self):
        out, applied = substitute_inputs("", {"x": "y"})
        self.assertEqual(out, "")
        self.assertEqual(applied, {})

    def test_non_string_value_coerced(self):
        out, applied = substitute_inputs("count={input.n}", {"n": 42})
        self.assertEqual(out, "count=42")
        self.assertEqual(applied, {"n": "42"})

    def test_special_chars_in_value_preserved(self):
        out, _ = substitute_inputs("{input.path}", {"path": "src/auth/*.py"})
        self.assertEqual(out, "src/auth/*.py")

    def test_underscore_and_digits_in_name(self):
        out, applied = substitute_inputs(
            "{input.target_branch} {input.pr_id_42}",
            {"target_branch": "main", "pr_id_42": "287"},
        )
        self.assertEqual(out, "main 287")
        self.assertEqual(applied, {"target_branch": "main", "pr_id_42": "287"})

    def test_invalid_placeholder_syntax_left_alone(self):
        # Names must start with a letter or underscore — leading digit is invalid syntax,
        # so the placeholder is treated as literal text (not substituted, not in applied map).
        out, applied = substitute_inputs("{input.1bad}", {"1bad": "x"})
        self.assertEqual(out, "{input.1bad}")
        self.assertEqual(applied, {})


class AssembleTest(unittest.TestCase):
    def test_basic_prompt_recipe(self):
        env = assemble(
            {
                "execution": {"model": "claude-opus-4-7"},
                "requires_skills": ["wiki-changelog"],
            },
            "## Prompt\nDo {input.task}",
            {"task": "X"},
        )
        self.assertEqual(env["model"], "claude-opus-4-7")
        self.assertEqual(env["skill_ids"], ["wiki-changelog"])
        self.assertEqual(env["recipe_prelude"], "")
        self.assertEqual(env["user_message"], "## Prompt\nDo X")
        self.assertEqual(env["substitutions"], {"task": "X"})

    def test_no_execution_model(self):
        env = assemble({"execution": {}, "requires_skills": []}, "body", {})
        self.assertIsNone(env["model"])

    def test_no_requires_skills(self):
        env = assemble({"execution": {"model": "x"}}, "body", {})
        self.assertEqual(env["skill_ids"], [])

    def test_empty_body_section(self):
        env = assemble({}, "", {})
        self.assertEqual(env["user_message"], "")
        self.assertEqual(env["substitutions"], {})

    def test_none_body_section(self):
        env = assemble({}, None, {})
        self.assertEqual(env["user_message"], "")

    def test_execution_missing_entirely(self):
        env = assemble({"requires_skills": ["a"]}, "body", {})
        self.assertIsNone(env["model"])
        self.assertEqual(env["skill_ids"], ["a"])

    def test_skill_ids_order_preserved(self):
        env = assemble(
            {"requires_skills": ["beta", "alpha", "gamma"]},
            "body",
            {},
        )
        self.assertEqual(env["skill_ids"], ["beta", "alpha", "gamma"])

    def test_substitutions_applied_in_body(self):
        env = assemble(
            {"execution": {}},
            "review {input.scope} for {input.focus}",
            {"scope": "auth/", "focus": "security"},
        )
        self.assertEqual(env["user_message"], "review auth/ for security")
        self.assertEqual(env["substitutions"], {"scope": "auth/", "focus": "security"})


if __name__ == "__main__":
    unittest.main()
