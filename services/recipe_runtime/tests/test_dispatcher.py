"""Unit tests for services.recipe_runtime.dispatcher.

The HTTP transport is replaced with an injected `http_post` capture so these
tests don't open sockets.
"""
import io
import os
import unittest

from services.recipe_runtime.dispatcher import dispatch_prompt


class _Capture:
    """Test double that records arguments and returns a canned reply."""

    def __init__(self, reply: str = "OK"):
        self.reply = reply
        self.calls: list[dict] = []

    def __call__(self, base_url, api_key, payload, *, out, stream):
        self.calls.append({
            "base_url": base_url,
            "api_key": api_key,
            "payload": payload,
            "stream": stream,
        })
        out.write(self.reply)
        return self.reply


def _envelope(**kwargs):
    base = {
        "model": None,
        "skill_ids": [],
        "recipe_prelude": "",
        "user_message": "hello",
        "substitutions": {},
    }
    base.update(kwargs)
    return base


class _EnvScope:
    """Snapshot/restore env vars touched by dispatcher tests."""

    KEYS = ("OPENAI_API_BASE", "OPENAI_API_KEY", "RECIPE_DEFAULT_MODEL")

    def __enter__(self):
        self.saved = {k: os.environ.get(k) for k in self.KEYS}
        for k in self.KEYS:
            os.environ.pop(k, None)
        return self

    def __exit__(self, *exc):
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


class ModelResolutionTest(unittest.TestCase):
    def test_envelope_model_wins(self):
        with _EnvScope():
            os.environ["RECIPE_DEFAULT_MODEL"] = "from-env"
            cap = _Capture()
            dispatch_prompt(
                _envelope(model="from-envelope"),
                default_model="from-arg",
                http_post=cap,
                out=io.StringIO(),
            )
            self.assertEqual(cap.calls[0]["payload"]["model"], "from-envelope")

    def test_default_model_arg_used_when_envelope_blank(self):
        with _EnvScope():
            os.environ["RECIPE_DEFAULT_MODEL"] = "from-env"
            cap = _Capture()
            dispatch_prompt(
                _envelope(model=None),
                default_model="from-arg",
                http_post=cap,
                out=io.StringIO(),
            )
            self.assertEqual(cap.calls[0]["payload"]["model"], "from-arg")

    def test_env_var_used_as_last_resort(self):
        with _EnvScope():
            os.environ["RECIPE_DEFAULT_MODEL"] = "from-env"
            cap = _Capture()
            dispatch_prompt(_envelope(), http_post=cap, out=io.StringIO())
            self.assertEqual(cap.calls[0]["payload"]["model"], "from-env")

    def test_raises_when_no_model_anywhere(self):
        with _EnvScope():
            with self.assertRaises(ValueError):
                dispatch_prompt(_envelope(), http_post=_Capture(), out=io.StringIO())


class MessageAssemblyTest(unittest.TestCase):
    def test_system_message_concatenates_skills_and_prelude(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m", recipe_prelude="P"),
            skill_bodies=["A", "B"],
            http_post=cap,
            out=io.StringIO(),
        )
        msgs = cap.calls[0]["payload"]["messages"]
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[0]["content"], "A\n\nB\n\nP")
        self.assertEqual(msgs[1]["role"], "user")
        self.assertEqual(msgs[1]["content"], "hello")

    def test_skill_bodies_are_stripped_and_blanks_dropped(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m"),
            skill_bodies=["  A  ", "", "   ", "B"],
            http_post=cap,
            out=io.StringIO(),
        )
        self.assertEqual(cap.calls[0]["payload"]["messages"][0]["content"], "A\n\nB")

    def test_no_system_message_when_no_skills_and_no_prelude(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m", recipe_prelude=""),
            skill_bodies=[],
            http_post=cap,
            out=io.StringIO(),
        )
        msgs = cap.calls[0]["payload"]["messages"]
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["role"], "user")

    def test_prelude_alone_creates_system_message(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m", recipe_prelude="rules"),
            http_post=cap,
            out=io.StringIO(),
        )
        msgs = cap.calls[0]["payload"]["messages"]
        self.assertEqual(msgs[0]["content"], "rules")

    def test_user_message_passes_through(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m", user_message="do X"),
            http_post=cap,
            out=io.StringIO(),
        )
        msgs = cap.calls[0]["payload"]["messages"]
        self.assertEqual(msgs[-1]["content"], "do X")

    def test_missing_user_message_becomes_empty_string(self):
        cap = _Capture()
        env = _envelope(model="m")
        env["user_message"] = None
        dispatch_prompt(env, http_post=cap, out=io.StringIO())
        msgs = cap.calls[0]["payload"]["messages"]
        self.assertEqual(msgs[-1]["content"], "")


class EndpointResolutionTest(unittest.TestCase):
    def test_arg_base_url_overrides_env(self):
        with _EnvScope():
            os.environ["OPENAI_API_BASE"] = "http://from-env/v1"
            cap = _Capture()
            dispatch_prompt(
                _envelope(model="m"),
                base_url="http://from-arg/v1",
                http_post=cap,
                out=io.StringIO(),
            )
            self.assertEqual(cap.calls[0]["base_url"], "http://from-arg/v1")

    def test_trailing_slash_stripped_from_base_url(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m"),
            base_url="http://x/v1/",
            http_post=cap,
            out=io.StringIO(),
        )
        self.assertEqual(cap.calls[0]["base_url"], "http://x/v1")

    def test_env_var_used_when_arg_absent(self):
        with _EnvScope():
            os.environ["OPENAI_API_BASE"] = "http://envbase/v1"
            cap = _Capture()
            dispatch_prompt(_envelope(model="m"), http_post=cap, out=io.StringIO())
            self.assertEqual(cap.calls[0]["base_url"], "http://envbase/v1")

    def test_default_base_url_when_unset(self):
        with _EnvScope():
            cap = _Capture()
            dispatch_prompt(_envelope(model="m"), http_post=cap, out=io.StringIO())
            self.assertEqual(cap.calls[0]["base_url"], "http://localhost:11434/v1")

    def test_api_key_arg_overrides_env(self):
        with _EnvScope():
            os.environ["OPENAI_API_KEY"] = "env-key"
            cap = _Capture()
            dispatch_prompt(
                _envelope(model="m"),
                api_key="arg-key",
                http_post=cap,
                out=io.StringIO(),
            )
            self.assertEqual(cap.calls[0]["api_key"], "arg-key")


class PayloadFlagsTest(unittest.TestCase):
    def test_stream_flag_passes_through(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m"),
            stream=False,
            http_post=cap,
            out=io.StringIO(),
        )
        self.assertFalse(cap.calls[0]["payload"]["stream"])
        self.assertFalse(cap.calls[0]["stream"])

    def test_max_tokens_and_temperature_in_payload(self):
        cap = _Capture()
        dispatch_prompt(
            _envelope(model="m"),
            max_tokens=128,
            temperature=0.7,
            http_post=cap,
            out=io.StringIO(),
        )
        payload = cap.calls[0]["payload"]
        self.assertEqual(payload["max_tokens"], 128)
        self.assertEqual(payload["temperature"], 0.7)

    def test_returns_string_from_transport(self):
        cap = _Capture(reply="result-text")
        out = io.StringIO()
        result = dispatch_prompt(_envelope(model="m"), http_post=cap, out=out)
        self.assertEqual(result, "result-text")
        self.assertEqual(out.getvalue(), "result-text")


if __name__ == "__main__":
    unittest.main()
