"""Unit tests for the Tier-2 (container) feature handler.

A fake `runner` substitutes for podman + a fake `http_prober` for HTTP
health probes, so tests never touch the network or spawn subprocesses.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import textwrap
import unittest
from pathlib import Path

_HAS_YAML = importlib.util.find_spec("yaml") is not None


def _make_runner(routes):
    """routes: dict[tuple[str,...], (stdout, returncode)] — match by prefix."""
    calls = []

    def _runner(argv):
        calls.append(list(argv))
        for prefix, response in routes.items():
            if tuple(argv[: len(prefix)]) == prefix:
                return response
        return ("", 0)

    _runner.calls = calls  # type: ignore[attr-defined]
    return _runner


def _inspect_payload(running: bool, status: str = "running") -> str:
    return json.dumps(
        [{"State": {"Running": running, "Status": status if running else "exited"}}]
    )


@unittest.skipUnless(_HAS_YAML, "PyYAML not installed; skipping features tests")
class ContainerHandlerTest(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(tempfile.mkdtemp())
        compose_dir = self.workspace / "infrastructure" / "core"
        compose_dir.mkdir(parents=True)
        (compose_dir / "docker-compose.yaml").write_text("services: {}\n")

        self.catalog = self.workspace / "catalog.yaml"
        self.catalog.write_text(textwrap.dedent(
            """\
            system: {}
            container:
              postgres:
                name: Postgres
                description: db
                compose_file: infrastructure/core/docker-compose.yaml
                compose_service: based-workspace-postgres
                container_name: based-workspace-postgres
                health:
                  type: exec
                  command: ["pg_isready"]
                requires: [podman]
              n8n:
                name: n8n
                description: workflow
                compose_file: infrastructure/core/docker-compose.yaml
                compose_service: n8n-atom
                container_name: n8n-atom-dev
                profile: n8n-atom
                health:
                  type: http
                  url: "http://localhost:5678/healthz"
                requires: [podman, postgres]
            """
        ))

    def _handler(self, runner, prober=lambda url, t: 200):
        from services.control_panel.features.container import ContainerFeatureHandler

        return ContainerFeatureHandler(
            workspace_root=self.workspace,
            catalog_path=self.catalog,
            runner=runner,
            http_prober=prober,
        )

    def test_absent_container_is_available(self):
        from services.control_panel.features import FeatureStatus

        runner = _make_runner({("podman", "inspect"): ("[]", 1)})
        f = self._handler(runner).get("postgres")
        self.assertEqual(f.status, FeatureStatus.AVAILABLE)

    def test_running_container_with_passing_exec_health_is_installed(self):
        from services.control_panel.features import FeatureStatus

        runner = _make_runner({
            ("podman", "inspect"): (_inspect_payload(True), 0),
            ("podman", "exec"): ("ok", 0),
        })
        f = self._handler(runner).get("postgres")
        self.assertEqual(f.status, FeatureStatus.INSTALLED)

    def test_running_container_with_failing_exec_health_is_partial(self):
        from services.control_panel.features import FeatureStatus

        runner = _make_runner({
            ("podman", "inspect"): (_inspect_payload(True), 0),
            ("podman", "exec"): ("not ready", 1),
        })
        f = self._handler(runner).get("postgres")
        self.assertEqual(f.status, FeatureStatus.PARTIAL)
        self.assertIn("exec returned 1", f.detail["health_error"])

    def test_stopped_container_is_error(self):
        from services.control_panel.features import FeatureStatus

        runner = _make_runner({
            ("podman", "inspect"): (_inspect_payload(False, "exited"), 0),
        })
        f = self._handler(runner).get("postgres")
        self.assertEqual(f.status, FeatureStatus.ERROR)
        self.assertEqual(f.detail["state"], "exited")

    def test_http_health_uses_prober(self):
        from services.control_panel.features import FeatureStatus

        runner = _make_runner({("podman", "inspect"): (_inspect_payload(True), 0)})

        statuses = []

        def prober(url, _t):
            statuses.append(url)
            return 503

        f = self._handler(runner, prober=prober).get("n8n")
        self.assertEqual(f.status, FeatureStatus.PARTIAL)
        self.assertEqual(statuses, ["http://localhost:5678/healthz"])

    def test_http_health_2xx_means_installed(self):
        from services.control_panel.features import FeatureStatus

        runner = _make_runner({("podman", "inspect"): (_inspect_payload(True), 0)})
        f = self._handler(runner, prober=lambda u, t: 204).get("n8n")
        self.assertEqual(f.status, FeatureStatus.INSTALLED)

    def test_install_invokes_compose_up(self):
        runner = _make_runner({
            ("podman", "inspect"): ("[]", 1),  # not running yet
            ("podman", "compose"): ("Started", 0),
        })
        handler = self._handler(runner)
        result = handler.install("n8n")
        self.assertTrue(result["ok"])
        cmd = result["command"]
        self.assertIn("podman compose -f", cmd)
        self.assertIn("--profile n8n-atom", cmd)
        self.assertIn("up -d n8n-atom", cmd)

    def test_install_idempotent_when_already_installed(self):
        runner = _make_runner({
            ("podman", "inspect"): (_inspect_payload(True), 0),
            ("podman", "exec"): ("ok", 0),
        })
        result = self._handler(runner).install("postgres")
        self.assertTrue(result["ok"])
        self.assertTrue(result["noop"])

    def test_install_unavailable_when_compose_file_missing(self):
        from services.control_panel.features import FeatureStatus

        # Rewrite catalog pointing at a missing compose file
        self.catalog.write_text(textwrap.dedent(
            """\
            system: {}
            container:
              postgres:
                name: Postgres
                description: db
                compose_file: nonexistent/docker-compose.yaml
                compose_service: based-workspace-postgres
                container_name: based-workspace-postgres
                requires: [podman]
            """
        ))
        f = self._handler(_make_runner({})).get("postgres")
        self.assertEqual(f.status, FeatureStatus.UNAVAILABLE)
        self.assertIn("compose file not found", f.detail["error"])

    def test_uninstall_stop_then_rm(self):
        runner = _make_runner({
            ("podman", "inspect"): (_inspect_payload(True), 0),
            ("podman", "exec"): ("ok", 0),
            ("podman", "compose"): ("", 0),
        })
        result = self._handler(runner).uninstall("postgres")
        self.assertTrue(result["ok"])
        # Ensure both `stop` and `rm` were invoked.
        compose_calls = [c for c in runner.calls if c[0] == "podman" and c[1] == "compose"]
        verbs = {v for c in compose_calls for v in c if v in ("stop", "rm")}
        self.assertEqual(verbs, {"stop", "rm"})

    def test_uninstall_noop_when_absent(self):
        runner = _make_runner({("podman", "inspect"): ("[]", 1)})
        result = self._handler(runner).uninstall("postgres")
        self.assertTrue(result["ok"])
        self.assertTrue(result["noop"])

    def test_list_returns_all(self):
        runner = _make_runner({("podman", "inspect"): ("[]", 1)})
        features = self._handler(runner).list()
        self.assertEqual({f.id for f in features}, {"postgres", "n8n"})

    def test_unknown_id_errors(self):
        h = self._handler(_make_runner({}))
        self.assertIsNone(h.get("does-not-exist"))
        self.assertFalse(h.install("does-not-exist")["ok"])
        self.assertFalse(h.uninstall("does-not-exist")["ok"])
        self.assertFalse(h.verify("does-not-exist")["ok"])


if __name__ == "__main__":
    unittest.main()
