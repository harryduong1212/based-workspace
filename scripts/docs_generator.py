#!/usr/bin/env python3
"""Generate docs/recipes/ and docs/connectors/ from .agents/ source files."""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

ROOT_DIR = Path(utils.BASE_DIR)
RECIPES_DIR = ROOT_DIR / "recipes"
CONNECTORS_DIR = ROOT_DIR / "connectors"
DOCS_RECIPES = ROOT_DIR / "docs" / "recipes"
DOCS_CONNECTORS = ROOT_DIR / "docs" / "connectors"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_md(path):
    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, content
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def _kv_table(rows):
    if not rows:
        return []
    out = ["| | |", "|---|---|"]
    for k, v in rows:
        out.append(f"| **{k}** | {v} |")
    out.append("")
    return out


def render_recipe_doc(fm, body):
    name = fm.get("name", fm.get("id", "?"))
    desc = fm.get("description", "")
    audience = fm.get("audience", "?")
    status = fm.get("status", "?")
    cost = fm.get("cost")
    tags = fm.get("tags") or []
    triggers = fm.get("triggers") or {}
    connectors = fm.get("requires_connectors") or []
    skills = fm.get("requires_skills") or []
    workflows = fm.get("requires_workflows") or []

    badges = [f"**Audience:** {audience}", f"**Status:** {status}"]
    if cost:
        badges.append(f"**Cost:** {cost}")

    lines = [f"# {name}", "", f"> {desc}", ">", f"> {' · '.join(badges)}", ""]

    rows = []
    if tags:
        rows.append(("Tags", ", ".join(tags)))
    if connectors:
        rows.append(("Requires data from", ", ".join(connectors)))
    if skills:
        rows.append(("Skills loaded", ", ".join(f"`{s}`" for s in skills)))
    if workflows:
        rows.append(("Workflows used", ", ".join(f"`{w}`" for w in workflows)))

    triggers_parts = []
    if triggers.get("cli"):
        triggers_parts.append(f"CLI: `{triggers['cli']}`")
    chat = triggers.get("chat")
    if chat:
        if isinstance(chat, list):
            triggers_parts.append("Chat: " + ", ".join(f'"{c}"' for c in chat))
        else:
            triggers_parts.append(f'Chat: "{chat}"')
    if triggers.get("schedule"):
        triggers_parts.append(f"Schedule: `{triggers['schedule']}`")
    if triggers_parts:
        rows.append(("Triggers", " · ".join(triggers_parts)))

    lines.extend(_kv_table(rows))
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    return "\n".join(lines)


def render_connector_doc(fm, body):
    name = fm.get("name", fm.get("id", "?"))
    desc = fm.get("description", "")
    status = fm.get("status", "?")
    auth_type = fm.get("auth_type", "?")
    provides = fm.get("provides") or []
    tags = fm.get("tags") or []
    requires_env = fm.get("requires_env") or []
    n8n_workflow = fm.get("n8n_workflow")

    lines = [
        f"# {name}",
        "",
        f"> {desc}",
        ">",
        f"> **Status:** {status} · **Auth:** {auth_type}",
        "",
    ]

    rows = []
    if provides:
        rows.append(("Provides", ", ".join(provides)))
    if requires_env:
        rows.append(("Required env vars", ", ".join(f"`{e}`" for e in requires_env)))
    if n8n_workflow:
        rows.append(("n8n workflow", f"`{n8n_workflow}`"))
    if tags:
        rows.append(("Tags", ", ".join(tags)))

    lines.extend(_kv_table(rows))
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    return "\n".join(lines)


def render_recipes_index(recipes):
    lines = [
        "# Recipes",
        "",
        "A **recipe** is a self-contained task you can run from chat, the CLI, or on a schedule.",
        "Each one wraps an AI prompt, an n8n workflow, or an agent — but you don't need to know which.",
        "Pick the recipe whose description matches what you want done.",
        "",
        "## How to run a recipe",
        "",
        "- **In Antigravity or Claude** — say one of the recipe's chat triggers (e.g., *\"morning briefing\"*).",
        "- **From the terminal** — `python scripts/recipe_manager.py run <id>`",
        "- **On a schedule** — recipes with a `schedule:` trigger run automatically once n8n is wired up.",
        "",
        "See the [Recipe Spec](../RECIPE_SPEC.md) for how recipes are written.",
        "",
    ]

    by_audience = {}
    for fm in recipes:
        aud = fm.get("audience", "tech")
        by_audience.setdefault(aud, []).append(fm)

    section_order = [
        ("both", "For everyone"),
        ("non-tech", "For non-technical users"),
        ("tech", "For technical users"),
    ]

    for aud_key, label in section_order:
        items = sorted(by_audience.get(aud_key, []), key=lambda r: r.get("id", ""))
        lines.append(f"## {label}")
        lines.append("")
        if not items:
            lines.append("*(none yet)*")
            lines.append("")
            continue
        lines.append("| Recipe | Description | Status | Tags |")
        lines.append("|---|---|---|---|")
        for fm in items:
            name = fm.get("name", fm.get("id", "?"))
            rid = fm.get("id", "?")
            desc = fm.get("description", "")
            status = fm.get("status", "?")
            tags = ", ".join(fm.get("tags") or [])
            lines.append(f"| [{name}]({rid}.md) | {desc} | {status} | {tags} |")
        lines.append("")

    return "\n".join(lines)


def render_connectors_index(connectors):
    lines = [
        "# Connectors",
        "",
        "**Connectors** are how recipes pull data from external systems — Jira, Bitbucket, GitHub, and so on.",
        "Each connector has a one-time setup (an API token or app password); recipes declare which connectors they need.",
        "",
        "See the [Connector Spec](../CONNECTOR_SPEC.md) for how connectors are written.",
        "",
        "## Available connectors",
        "",
    ]
    if not connectors:
        lines.append("*(none yet)*")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Connector | Description | Provides | Status |")
    lines.append("|---|---|---|---|")
    for fm in sorted(connectors, key=lambda c: c.get("id", "")):
        name = fm.get("name", fm.get("id", "?"))
        cid = fm.get("id", "?")
        desc = fm.get("description", "")
        provides = ", ".join(fm.get("provides") or [])
        status = fm.get("status", "?")
        lines.append(f"| [{name}]({cid}.md) | {desc} | {provides} | {status} |")
    lines.append("")
    return "\n".join(lines)


def _collect(directory):
    out = []
    if not directory.exists():
        return out
    for path in sorted(directory.glob("*.md")):
        fm, body = parse_md(path)
        if fm:
            out.append((path, fm, body))
    return out


def _write_or_check(path, content, check_mode):
    rel = path.relative_to(ROOT_DIR)
    if check_mode:
        if not path.exists():
            print(f"DRIFT (missing) {rel}")
            return True
        existing = path.read_text(encoding="utf-8")
        if existing != content:
            print(f"DRIFT (changed) {rel}")
            return True
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"WROTE {rel}")
    return False


def _prune_stale(target_dir, valid_ids, check_mode):
    """Remove generated docs for ids that no longer exist in the source."""
    if not target_dir.exists():
        return False
    drifted = False
    keep = set(valid_ids) | {"INDEX"}
    for f in sorted(target_dir.glob("*.md")):
        if f.stem not in keep:
            rel = f.relative_to(ROOT_DIR)
            if check_mode:
                print(f"DRIFT (orphan) {rel}")
                drifted = True
            else:
                f.unlink()
                print(f"REMOVED {rel}")
    return drifted


def generate_recipes(check_mode=False):
    items = _collect(RECIPES_DIR)
    drifted = False
    for path, fm, body in items:
        rid = fm.get("id") or path.stem
        drifted |= _write_or_check(DOCS_RECIPES / f"{rid}.md", render_recipe_doc(fm, body), check_mode)
    drifted |= _write_or_check(
        DOCS_RECIPES / "INDEX.md",
        render_recipes_index([fm for _, fm, _ in items]),
        check_mode,
    )
    drifted |= _prune_stale(DOCS_RECIPES, [fm.get("id") or p.stem for p, fm, _ in items], check_mode)
    return drifted


def generate_connectors(check_mode=False):
    items = _collect(CONNECTORS_DIR)
    drifted = False
    for path, fm, body in items:
        cid = fm.get("id") or path.stem
        drifted |= _write_or_check(DOCS_CONNECTORS / f"{cid}.md", render_connector_doc(fm, body), check_mode)
    drifted |= _write_or_check(
        DOCS_CONNECTORS / "INDEX.md",
        render_connectors_index([fm for _, fm, _ in items]),
        check_mode,
    )
    drifted |= _prune_stale(DOCS_CONNECTORS, [fm.get("id") or p.stem for p, fm, _ in items], check_mode)
    return drifted


def main():
    parser = argparse.ArgumentParser(description="Generate docs/recipes/ and docs/connectors/ from .agents/ source files")
    parser.add_argument("--check", action="store_true", help="Verify docs are in sync; exit non-zero on drift")
    parser.add_argument("--recipes-only", action="store_true")
    parser.add_argument("--connectors-only", action="store_true")
    args = parser.parse_args()

    drifted = False
    if not args.connectors_only:
        drifted |= generate_recipes(args.check)
    if not args.recipes_only:
        drifted |= generate_connectors(args.check)

    if args.check and drifted:
        print()
        print("Docs are out of sync. Re-run without --check to regenerate.")
        sys.exit(1)


if __name__ == "__main__":
    main()
