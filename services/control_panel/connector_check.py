"""Connector health check — validates that declared env vars are present.

A live API probe needs the connector adapter + real credentials and is
deferred (see feedback-defer-external-connectors.md). This module's job
is the lighter check the UI should always be able to do: did the user
actually set the required env vars in `.env`?
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvCheck:
    name: str
    present: bool


@dataclass(frozen=True)
class ConnectorCheckResult:
    connector_id: str
    env_checks: list[EnvCheck]

    @property
    def all_present(self) -> bool:
        return all(c.present for c in self.env_checks)

    @property
    def missing(self) -> list[str]:
        return [c.name for c in self.env_checks if not c.present]


def check_connector_env(connector_id: str, requires_env: list[str]) -> ConnectorCheckResult:
    return ConnectorCheckResult(
        connector_id=connector_id,
        env_checks=[EnvCheck(name=v, present=bool(os.environ.get(v))) for v in requires_env],
    )
