"""Features module — install/uninstall/verify per feature kind.

A "feature" is anything a user can install to make based-workspace work,
spanning three tiers:

- T1 (system): host binaries — Podman, Python, Node, Git, gitleaks hook.
  Detect-only; the wizard prints an install command, never runs sudo.
- T2 (container): podman-compose services — Postgres, n8n, Qdrant,
  llama-swap, MCP Inspector. Managed via `podman compose` actions.
- T3 (application): MCP servers, recipes, connectors. Each has a custom
  install flow personalised in the UI (see `MCPSetupWizard`, etc.).

Public surface — re-exported from this package:

  - Feature, FeatureKind, FeatureStatus  (dataclasses + enums in `base`)
  - FeatureHandler                       (Protocol all kind-handlers obey)
  - load_catalog                         (parses `catalog.yaml` for T1+T2)
"""
from __future__ import annotations

from .base import Feature, FeatureHandler, FeatureKind, FeatureStatus, load_catalog

__all__ = [
    "Feature",
    "FeatureHandler",
    "FeatureKind",
    "FeatureStatus",
    "load_catalog",
]
