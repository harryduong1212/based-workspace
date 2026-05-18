"""Feature base abstractions — data shapes + handler protocol + catalog loader.

A `Feature` is the unit the UI lists, installs, uninstalls and verifies.
Handlers implement `FeatureHandler` per kind (system/container/mcp/recipe/
connector); they all return `Feature` instances from `list()` and `get()`,
and accept feature ids in install/uninstall/verify.

The dep graph is expressed by `Feature.requires` — a list of other feature
ids (across kinds). The dispatcher gates install: a feature with unsatisfied
`requires` cannot be installed until its prereqs are.

Catalog YAML (`catalog.yaml` in this package) holds the static declarations
for T1 (system) and T2 (container). T3 handlers auto-scan their own sources
(`.mcp.json.example`, `recipes/`, `connectors/registry.json`).
"""
from __future__ import annotations

import dataclasses
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Protocol, runtime_checkable


# Optional callback handlers invoke to stream progress lines during install.
# `None` means "no live logging" — handler runs as before.
LogSink = Callable[[str], None]


class FeatureKind(str, Enum):
    SYSTEM = "system"
    CONTAINER = "container"
    MCP = "mcp"
    RECIPE = "recipe"
    CONNECTOR = "connector"


class FeatureStatus(str, Enum):
    AVAILABLE = "available"      # known, not installed, can be installed
    INSTALLED = "installed"      # installed and verified working
    PARTIAL = "partial"          # some pieces installed (e.g. recipe present but not synced)
    STOPPED = "stopped"          # set up but not running — recoverable with one Start click
    ERROR = "error"              # genuinely broken (e.g. container in 'dead' state)
    UNAVAILABLE = "unavailable"  # cannot be installed on this system (e.g. wrong platform)
    UNKNOWN = "unknown"          # status check failed; treat as actionable but not gating


@dataclasses.dataclass
class Feature:
    """One installable thing. Handlers produce these; the UI renders them.

    `requires` lists other feature ids the dispatcher must see as INSTALLED
    before this one can be installed. Cross-kind: e.g. an MCP feature can
    require a container feature.

    `detail` is a free-form kind-specific payload (the per-kind wizard reads
    it to render its UI — install command for SYSTEM, compose service name
    for CONTAINER, MCP server config for MCP, etc.).
    """

    id: str
    kind: FeatureKind
    name: str
    description: str
    status: FeatureStatus
    requires: list[str] = dataclasses.field(default_factory=list)
    detail: dict[str, Any] = dataclasses.field(default_factory=dict)
    # Longer prose: what this is, what installing actually does, and any
    # advanced notes/gotchas. Rendered as an "About" card on the detail
    # page. Empty string = card hidden (no editorial content authored yet).
    about: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind.value,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "requires": list(self.requires),
            "detail": dict(self.detail),
            "about": self.about,
        }


@runtime_checkable
class FeatureHandler(Protocol):
    """Per-kind handler — every kind module exports one of these.

    Methods return plain dicts (not bespoke result classes) so the API layer
    can pass them through to JSON without translation. A successful action
    returns `{"ok": True, "feature": <Feature.to_dict()>}`; a failure returns
    `{"ok": False, "error": "<human-readable>"}`.

    Implementations should be idempotent: install of an already-installed
    feature is a no-op success, uninstall of a missing feature is a no-op
    success. Verify must be safe to call any time.
    """

    kind: FeatureKind

    def list(self) -> list[Feature]: ...
    def get(self, feature_id: str) -> Feature | None: ...
    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink: LogSink | None = None,
    ) -> dict[str, Any]: ...
    def uninstall(self, feature_id: str) -> dict[str, Any]: ...
    def verify(self, feature_id: str) -> dict[str, Any]: ...
    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        """Describe what `install(feature_id, inputs)` would do without side effects.

        Returns: `{ok, feature, would_be_noop, side_effects, warnings}`. Each
        `side_effects` entry is `{kind, summary, detail}` so the UI can render
        a typed list (no kind-specific frontend coupling). The registry
        composes `unmet_prereqs` on top so the dialog can warn about gating
        before the user confirms.
        """
        ...


# ---- catalog ---------------------------------------------------------------

_CATALOG_FILENAME = "catalog.yaml"


def load_catalog(catalog_path: Path | None = None) -> dict[str, dict[str, dict[str, Any]]]:
    """Parse `catalog.yaml`. Returns `{kind: {id: declaration_dict}}`.

    Only T1 (system) and T2 (container) live in the catalog; T3 handlers
    self-discover. Raises FileNotFoundError if the catalog is missing and
    ValueError if it's malformed.
    """
    import yaml  # local import — yaml is already a transitive dep via apscheduler

    path = catalog_path or (Path(__file__).parent / _CATALOG_FILENAME)
    if not path.exists():
        raise FileNotFoundError(f"feature catalog not found at {path}")

    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(doc, dict):
        raise ValueError(f"feature catalog must be a YAML mapping; got {type(doc).__name__}")

    known_kinds = {FeatureKind.SYSTEM.value, FeatureKind.CONTAINER.value}
    out: dict[str, dict[str, dict[str, Any]]] = {}
    for kind, entries in doc.items():
        if kind not in known_kinds:
            raise ValueError(
                f"catalog kind {kind!r} not allowed here (only {sorted(known_kinds)} — T3 self-discovers)"
            )
        if not isinstance(entries, dict):
            raise ValueError(f"catalog kind {kind!r} must map to id→declaration; got {type(entries).__name__}")
        out[kind] = entries
    return out
