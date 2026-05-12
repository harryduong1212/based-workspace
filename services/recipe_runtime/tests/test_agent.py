"""Unit tests for dispatch_agent.

The HTTP transport is replaced with an injected `http_post` that returns
canned Anthropic Messages API responses, so these tests don't hit the network
or require ANTHROPIC_API_KEY.
"""
from __future__ import annotations

import io
import unittest
from unittest.mock import patch

from services.recipe_runtime.dispatcher import dispatch_agent


def _msg_text(text: str, stop="end_turn") -> dict:
    """Build a single-text-block Anthropic response."""
    return {"stop_reason": stop, "content": [{"type": "text", "text": text}]}


def _msg_tool_use(tool_name: str, tool_input: dict, tool_id: str = "toolu_1") -> dict:
    """Build a tool_use response that ends the turn pending tool_result."""
    return {
        "stop_reason": "tool_use",
        "content": [
            {"type": "text", "text": "calling tool..."},
            {
                "type": "tool_use",
                "id": tool_id,
                "name": tool_name,
                "input": tool_input,
            },
        ],
    }


FM_BASIC = {"execution": {"type": "agent", "model": "anthropic/claude-haiku-4-5-20251001"}}


class DispatchAgentTest(unittest.TestCase):
    def test_single_turn_text_response_is_returned_and_streamed(self):
        out = io.StringIO()
        replies = [_msg_text("hello world")]

        def http(payload):
            return replies.pop(0)

        result = dispatch_agent(
            FM_BASIC,
            "Say hi.",
            {},
            out=out,
            http_post=http,
        )

        self.assertEqual(result, "hello world")
        self.assertEqual(out.getvalue(), "hello world")
        self.assertEqual(len(replies), 0)  # exactly one HTTP call

    def test_tool_use_triggers_followup_call_with_tool_result(self):
        out = io.StringIO()
        # Turn 1: model asks for the current time. Turn 2: model answers.
        replies = [
            _msg_tool_use("get_current_time", {}, tool_id="toolu_xyz"),
            _msg_text("ack"),
        ]
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return replies.pop(0)

        result = dispatch_agent(
            FM_BASIC,
            "What time is it?",
            {},
            out=out,
            http_post=http,
        )

        self.assertEqual(len(captured), 2, "expected 2 round trips (tool_use → tool_result)")
        # Second request must include the assistant's tool_use AND a tool_result
        second = captured[1]["messages"]
        roles = [m["role"] for m in second]
        self.assertEqual(roles, ["user", "assistant", "user"])
        tool_result_blocks = [
            b for b in second[2]["content"] if b.get("type") == "tool_result"
        ]
        self.assertEqual(len(tool_result_blocks), 1)
        self.assertEqual(tool_result_blocks[0]["tool_use_id"], "toolu_xyz")
        self.assertIn("T", tool_result_blocks[0]["content"], "expected ISO 8601 'T' separator")
        self.assertEqual(result, "calling tool...ack")

    def test_unknown_tool_returns_error_in_tool_result(self):
        replies = [
            _msg_tool_use("does_not_exist", {"foo": "bar"}),
            _msg_text("got the error, moving on"),
        ]
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return replies.pop(0)

        dispatch_agent(FM_BASIC, "Try a bad tool.", {}, http_post=http)

        tool_result_content = captured[1]["messages"][2]["content"][0]["content"]
        self.assertIn("unknown tool", tool_result_content)

    def test_max_iterations_stops_runaway_loop(self):
        """If the model never says end_turn, we still bail after MAX_AGENT_ITERATIONS."""
        replies = []
        # 20 tool_use responses — more than the iteration cap (10).
        for _ in range(20):
            replies.append(_msg_tool_use("get_current_time", {}))
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return replies.pop(0)

        dispatch_agent(FM_BASIC, "Loop forever.", {}, http_post=http)
        self.assertLessEqual(len(captured), 10)

    def test_non_anthropic_model_raises(self):
        with self.assertRaises(NotImplementedError):
            dispatch_agent(
                {"execution": {"type": "agent", "model": "gemini/gemini-2.0-flash"}},
                "hi",
                {},
                http_post=lambda p: _msg_text("ok"),
            )

    def test_skill_bodies_become_system_message(self):
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return _msg_text("ack")

        dispatch_agent(
            FM_BASIC,
            "Hello.",
            {},
            skill_bodies=["You are concise.", "Never apologize."],
            http_post=http,
        )

        self.assertIn("system", captured[0])
        self.assertIn("You are concise.", captured[0]["system"])
        self.assertIn("Never apologize.", captured[0]["system"])

    def test_input_substitution_in_user_message(self):
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return _msg_text("ack")

        dispatch_agent(
            FM_BASIC,
            "Echo: {input.message}",
            {"message": "hello world"},
            http_post=http,
        )
        user_msg = captured[0]["messages"][0]["content"]
        self.assertEqual(user_msg, "Echo: hello world")


if __name__ == "__main__":
    unittest.main()
