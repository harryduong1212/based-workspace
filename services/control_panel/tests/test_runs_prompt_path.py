"""Regression test for the prompt-path closure bug in runs._worker.

The agent branch used to do `fm = {**fm, ...}`, which made `fm` a local
of `_worker`; the prompt branch's earlier read of the closed-over `fm`
then raised UnboundLocalError — so *every* prompt-type recipe run through
the Control Panel errored with zero output. This drives a prompt run with
the dispatcher faked and asserts it reaches status 'done'.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class PromptPathDoesNotShadowFmTest(unittest.TestCase):
    def setUp(self):
        from services.recipe_runtime import dispatcher

        self.tmp = Path(tempfile.mkdtemp())
        self._real_dp = dispatcher.dispatch_prompt

        def _fake_dispatch_prompt(envelope, *, skill_bodies=None, out=None, **kw):
            text = f"echo:{envelope['user_message']}"
            if out is not None:
                out.write(text)
            return text

        dispatcher.dispatch_prompt = _fake_dispatch_prompt  # type: ignore[assignment]
        self.addCleanup(setattr, dispatcher, "dispatch_prompt", self._real_dp)

    def _cfg(self):
        from services.control_panel.config import Config

        # workspace_root = tmp so the SQLite DB is isolated; `from scripts
        # import recipe_manager` still resolves via the repo root already on
        # the test runner's sys.path.
        return Config(
            workspace_root=self.tmp,
            recipes_dir=self.tmp / "recipes",
            connectors_dir=self.tmp / "connectors",
            services_dir=self.tmp / "services",
            host="127.0.0.1", port=0, reload=False, llama_swap_url="",
        )

    def test_prompt_run_completes(self):
        from services.control_panel import db, runs

        cfg = self._cfg()
        db.init(cfg.workspace_root)
        self.addCleanup(db.close)

        fm = {"id": "t", "execution": {"type": "prompt", "model": "gemma-3-4b"}}
        body = "## Prompt\nSay <{input.phrase}>\n"

        run = runs.start_run(cfg, "t", fm, body, {"phrase": "hi"}, "gemma-3-4b")
        self.assertTrue(run._done.wait(timeout=20), "run never completed")

        self.assertEqual(run.status, "done", f"error was: {run.error!r}")
        self.assertIsNone(run.error)
        self.assertIn("echo:", run.output)

        row = db.get_run_row(run.id)
        self.assertEqual(row.status, "done")
        self.assertIn("echo:", row.output)


if __name__ == "__main__":
    unittest.main()
