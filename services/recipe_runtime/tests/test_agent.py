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

    def test_unknown_provider_raises(self):
        with self.assertRaises(NotImplementedError):
            dispatch_agent(
                {"execution": {"type": "agent", "model": "imaginaryprov/x"}},
                "hi",
                {},
                http_post=lambda p: {},
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


def _openai_text(text: str, finish: str = "stop") -> dict:
    """Build an OpenAI-shape single-message response."""
    return {
        "choices": [
            {"finish_reason": finish, "message": {"role": "assistant", "content": text}}
        ]
    }


def _openai_tool_call(name: str, args: dict, call_id: str = "call_1") -> dict:
    """Build an OpenAI-shape response with a tool_call and no content."""
    import json as _json
    return {
        "choices": [
            {
                "finish_reason": "tool_calls",
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {"name": name, "arguments": _json.dumps(args)},
                        }
                    ],
                },
            }
        ]
    }


FM_LOCAL = {"execution": {"type": "agent", "model": "local/gemma-3-12b"}}
FM_GEMINI = {"execution": {"type": "agent", "model": "gemini/gemini-2.0-flash"}}


class DispatchAgentOpenAIPathTest(unittest.TestCase):
    """The OpenAI-compatible wire covers local (llama-swap) + gemini."""

    def test_local_single_turn_text(self):
        out = io.StringIO()
        replies = [_openai_text("hello local")]

        def http(payload):
            return replies.pop(0)

        result = dispatch_agent(FM_LOCAL, "Say hi.", {}, out=out, http_post=http)
        self.assertEqual(result, "hello local")
        self.assertEqual(out.getvalue(), "hello local")
        self.assertEqual(len(replies), 0)

    def test_local_tool_call_round_trip(self):
        replies = [
            _openai_tool_call("get_current_time", {}, call_id="call_xyz"),
            _openai_text("done"),
        ]
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return replies.pop(0)

        result = dispatch_agent(FM_LOCAL, "Time?", {}, http_post=http)

        self.assertEqual(len(captured), 2, "expected one round-trip for tool_call → tool result")
        # First request advertises tools in OpenAI shape.
        self.assertIn("tools", captured[0])
        self.assertEqual(captured[0]["tools"][0]["type"], "function")
        # Second request includes assistant tool_calls and a {role:"tool"} result.
        second = captured[1]["messages"]
        roles = [m["role"] for m in second]
        self.assertEqual(roles[-2:], ["assistant", "tool"])
        self.assertEqual(second[-1]["tool_call_id"], "call_xyz")
        self.assertIn("T", second[-1]["content"])  # ISO 8601 separator
        self.assertEqual(result, "done")

    def test_local_unknown_tool_returns_error_to_model(self):
        replies = [
            _openai_tool_call("does_not_exist", {"foo": "bar"}),
            _openai_text("ok"),
        ]
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return replies.pop(0)

        dispatch_agent(FM_LOCAL, "Try bad tool.", {}, http_post=http)
        tool_msg = captured[1]["messages"][-1]
        self.assertEqual(tool_msg["role"], "tool")
        self.assertIn("unknown tool", tool_msg["content"])

    def test_max_iterations_caps_openai_loop(self):
        replies = [_openai_tool_call("get_current_time", {}) for _ in range(20)]
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return replies.pop(0)

        dispatch_agent(FM_LOCAL, "Loop.", {}, http_post=http)
        self.assertLessEqual(len(captured), 10)

    def test_local_skill_bodies_become_system_message(self):
        captured: list[dict] = []

        def http(payload):
            captured.append(payload)
            return _openai_text("ack")

        dispatch_agent(
            FM_LOCAL,
            "Hi.",
            {},
            skill_bodies=["You are concise.", "Never apologize."],
            http_post=http,
        )

        # OpenAI wire: system is the first message, not a top-level field.
        msgs = captured[0]["messages"]
        self.assertEqual(msgs[0]["role"], "system")
        self.assertIn("You are concise.", msgs[0]["content"])
        self.assertIn("Never apologize.", msgs[0]["content"])

    def test_gemini_uses_openai_wire(self):
        # Gemini's OpenAI-compat shim → identical payload shape as local.
        replies = [_openai_text("hello gemini")]

        def http(payload):
            return replies.pop(0)

        result = dispatch_agent(FM_GEMINI, "Hi.", {}, http_post=http)
        self.assertEqual(result, "hello gemini")

    def test_gemini_without_key_or_http_post_raises(self):
        # Real network attempt must require GEMINI_API_KEY.
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError) as ctx:
                dispatch_agent(FM_GEMINI, "Hi.", {})
            self.assertIn("GEMINI_API_KEY", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
