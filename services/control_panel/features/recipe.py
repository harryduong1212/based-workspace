"""Tier 3 — Recipe features.

A recipe is "installed" when its source file in `recipes/<id>.md` has been
synced into both provider directories: `.claude/commands/<id>.md` (for Claude
Code) and `.agents/workflows/<id>.md` (for Antigravity). Source files always
ship in the repo, so "uninstall" is **deactivate** by default — provider files
get removed but `recipes/<id>.md` stays unless `inputs.delete_file=True`.

Status mapping
--------------
- INSTALLED   — source exists AND both provider files present
- PARTIAL     — source exists, one provider file present (drift or half-synced)
- AVAILABLE   — source exists, no provider files (cleanly deactivated)
- ERROR       — source exists but parse fails
- UNAVAILABLE — source missing (handler doesn't list these by design)
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .base import Feature, FeatureKind, FeatureStatus


# (argv) → (stdout_combined, returncode)
from typing import Callable

CommandRunner = Callable[[list[str]], tuple[str, int]]


def _default_runner(argv: list[str]) -> tuple[str, int]:
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=60, check=False)
        return (result.stdout or "") + (result.stderr or ""), result.returncode
    except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError) as e:
        return f"{type(e).__name__}: {e}", -1


def _parse_frontmatter_id(path: Path) -> str | None:
    """Return the `id:` field from YAML frontmatter, or None on error/absence."""
    import yaml

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    rid = fm.get("id") or path.stem
    return str(rid) if rid else None


def _parse_frontmatter_full(path: Path) -> dict[str, Any] | None:
    """Return the full frontmatter dict, or None on parse failure."""
    import yaml

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        fm = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


class RecipeFeatureHandler:
    """Handler for kind=recipe (Tier 3)."""

    kind = FeatureKind.RECIPE

    CLAUDE_DIR = Path(".claude/commands")
    AGENTS_DIR = Path(".agents/workflows")

    SYNC_SCRIPTS = (
        Path("scripts/sync_claude_code.py"),
        Path("scripts/sync_antigravity.py"),
    )

    def __init__(
        self,
        workspace_root: Path,
        runner: CommandRunner | None = None,
    ):
        self._root = Path(workspace_root)
        self._run = runner or _default_runner

    # ---- discovery -----------------------------------------------------

    def _recipes_dir(self) -> Path:
        return self._root / "recipes"

    def _claude_target(self, recipe_id: str) -> Path:
        return self._root / self.CLAUDE_DIR / f"{recipe_id}.md"

    def _agents_target(self, recipe_id: str) -> Path:
        return self._root / self.AGENTS_DIR / f"{recipe_id}.md"

    def _source_for(self, recipe_id: str) -> Path | None:
        """Return the recipes/<id>.md path if it exists, walking by frontmatter id."""
        # Fast path: filename matches id.
        direct = self._recipes_dir() / f"{recipe_id}.md"
        if direct.exists() and _parse_frontmatter_id(direct) == recipe_id:
            return direct
        # Slow path: scan all recipes for an `id:` frontmatter match.
        for path in sorted(self._recipes_dir().glob("*.md")):
            if _parse_frontmatter_id(path) == recipe_id:
                return path
        return None

    def _build(self, recipe_id: str, source: Path) -> Feature:
        fm = _parse_frontmatter_full(source)
        if fm is None:
            return Feature(
                id=recipe_id,
                kind=FeatureKind.RECIPE,
                name=recipe_id,
                description="(unparseable frontmatter)",
                status=FeatureStatus.ERROR,
                detail={"source": str(source.relative_to(self._root))},
            )

        claude_present = self._claude_target(recipe_id).exists()
        agents_present = self._agents_target(recipe_id).exists()

        if claude_present and agents_present:
            status = FeatureStatus.INSTALLED
        elif claude_present or agents_present:
            status = FeatureStatus.PARTIAL
        else:
            status = FeatureStatus.AVAILABLE

        return Feature(
            id=recipe_id,
            kind=FeatureKind.RECIPE,
            name=str(fm.get("name") or recipe_id),
            description=str(fm.get("description") or ""),
            status=status,
            requires=[],  # cross-feature deps (e.g. on MCP/connector) come from fm.requires_*;
                          # surfaced separately so the wizard can prompt, not block install
            detail={
                "source": str(source.relative_to(self._root)),
                "audience": fm.get("audience"),
                "tags": list(fm.get("tags") or []),
                "status_field": fm.get("status"),
                "execution_type": (fm.get("execution") or {}).get("type"),
                "in_claude": claude_present,
                "in_agents": agents_present,
                "requires_skills": list(fm.get("requires_skills") or []),
                "requires_workflows": list(fm.get("requires_workflows") or []),
                "requires_connectors": list(fm.get("requires_connectors") or []),
                "requires_mcp": list(fm.get("requires_mcp") or []),
                "requires_env": list(fm.get("requires_env") or []),
            },
            about=str(fm.get("about") or "").strip(),
            highlights=[str(h) for h in (fm.get("highlights") or [])],
            examples=[
                {"label": str(e.get("label", "")), "code": str(e.get("code", ""))}
                for e in (fm.get("examples") or [])
                if isinstance(e, dict)
            ],
            docs=str(fm.get("docs") or "").strip(),
        )

    # ---- handler protocol ---------------------------------------------

    def list(self) -> list[Feature]:
        out: list[Feature] = []
        for path in sorted(self._recipes_dir().glob("*.md")):
            rid = _parse_frontmatter_id(path)
            if rid is None:
                continue
            out.append(self._build(rid, path))
        return out

    def get(self, feature_id: str) -> Feature | None:
        source = self._source_for(feature_id)
        if source is None:
            return None
        return self._build(feature_id, source)

    def install(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
        log_sink=None,
    ) -> dict[str, Any]:
        """Run both sync scripts so this recipe (and all others) are projected
        into the provider dirs. Sync scripts are idempotent and prune stale
        files, which is the right behaviour for a "make it match source" install.
        """
        del inputs  # nothing per-install
        log = log_sink or (lambda _s: None)
        source = self._source_for(feature_id)
        if source is None:
            return {
                "ok": False,
                "error": f"no recipe with id {feature_id!r} found in {self.CLAUDE_DIR.parent.as_posix()}/",
            }

        errors = []
        for script in self.SYNC_SCRIPTS:
            argv = ["python3", str(self._root / script)]
            log(f"$ python3 {script.as_posix()}")
            out, rc = self._run(argv)
            for line in (out or "").rstrip().splitlines():
                log(line)
            log(f"{script.name} exit code: {rc}")
            if rc != 0:
                errors.append(f"{script.name} failed (rc={rc}): {out[-500:]}")

        feature = self._build(feature_id, source)
        if errors:
            return {"ok": False, "error": "; ".join(errors), "feature": feature.to_dict()}
        return {"ok": feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict()}

    def uninstall(
        self,
        feature_id: str,
        inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Default: deactivate (remove provider files only). Source stays.

        Pass inputs not supported here intentionally — destructive recipe-file
        deletion goes through the separate `delete-recipe` flow in the UI.
        """
        del inputs
        source = self._source_for(feature_id)
        if source is None:
            return {"ok": False, "error": f"unknown recipe {feature_id!r}"}

        removed: list[str] = []
        for target_path in (self._claude_target(feature_id), self._agents_target(feature_id)):
            if target_path.exists():
                try:
                    target_path.unlink()
                    removed.append(str(target_path.relative_to(self._root)))
                except OSError as e:
                    return {"ok": False, "error": f"could not delete {target_path}: {e}"}

        feature = self._build(feature_id, source)
        return {
            "ok": True,
            "noop": not removed,
            "removed": removed,
            "feature": feature.to_dict(),
        }

    def verify(self, feature_id: str) -> dict[str, Any]:
        feature = self.get(feature_id)
        if feature is None:
            return {"ok": False, "error": f"unknown recipe {feature_id!r}"}
        return {"ok": feature.status == FeatureStatus.INSTALLED, "feature": feature.to_dict()}

    def preview(self, feature_id: str, inputs: dict[str, Any] | None = None) -> dict[str, Any]:
        del inputs
        source = self._source_for(feature_id)
        if source is None:
            return {"ok": False, "error": f"unknown recipe {feature_id!r}"}
        feature = self._build(feature_id, source)

        side_effects: list[dict[str, Any]] = [
            {"kind": "run_script", "summary": "Run scripts/sync_claude_code.py",
             "detail": "Project all recipes into .claude/commands/"},
            {"kind": "run_script", "summary": "Run scripts/sync_antigravity.py",
             "detail": "Project all recipes into .agents/workflows/"},
            {"kind": "file_write", "summary": "Write provider files for this recipe",
             "detail": f".claude/commands/{feature_id}.md, .agents/workflows/{feature_id}.md"},
        ]

        warnings: list[str] = [
            "Sync is global: it touches all recipes, not just this one. "
            "Stale provider files (recipes that no longer exist in source) will be pruned."
        ]
        if feature.status == FeatureStatus.INSTALLED:
            warnings.append("Already installed — install will re-sync (no change unless source diverged).")

        requires_mcp = feature.detail.get("requires_mcp") or []
        requires_conn = feature.detail.get("requires_connectors") or []
        if requires_mcp:
            warnings.append(
                f"Recipe declares requires_mcp: {', '.join(requires_mcp)}. "
                "Install does not auto-install these — verify they're ready or the recipe will fail at run time."
            )
        if requires_conn:
            warnings.append(
                f"Recipe declares requires_connectors: {', '.join(requires_conn)}. "
                "Make sure their env vars are set."
            )

        return {
            "ok": True,
            "feature": feature.to_dict(),
            "would_be_noop": False,  # sync runs each time; idempotent but not noop
            "side_effects": side_effects,
            "warnings": warnings,
        }
