#!/usr/bin/env python3
"""Recipe Manager CLI — list, show, lint, and sync the recipe registry."""

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
RECIPES_REGISTRY = RECIPES_DIR / "registry.json"
CONNECTORS_REGISTRY = ROOT_DIR / "connectors" / "registry.json"
SKILLS_REGISTRY = ROOT_DIR / ".archived" / "skills" / "registry.json"
WORKFLOWS_REGISTRY = ROOT_DIR / ".archived" / "workflows" / "registry.json"
MCP_CONFIG = ROOT_DIR / ".vscode" / "mcp.json"

VALID_AUDIENCE = {"non-tech", "tech", "both"}
VALID_STATUS = {"experimental", "stable", "deprecated"}
VALID_COST = {"low", "medium", "high"}
VALID_EXEC_TYPES = {"prompt", "workflow", "agent"}
VALID_IO_TYPES = {"string", "number", "bool", "markdown", "json"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_recipe(path):
    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        raise ValueError("missing or malformed frontmatter")
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def load_all_recipes():
    if not RECIPES_DIR.exists():
        return
    for path in sorted(RECIPES_DIR.glob("*.md")):
        try:
            fm, body = parse_recipe(path)
            yield path, fm, body, None
        except Exception as e:
            yield path, None, None, str(e)


def collect_ids_from_split_registry(root_path, item_key):
    """Walk a registry that splits per-category, returning the union of IDs."""
    ids = set()
    if not root_path.exists():
        return ids
    root = utils.load_json(str(root_path))
    for cat in root.get("categories", []):
        cat_path = ROOT_DIR / cat.get("registry_path", "")
        if not cat_path.exists():
            continue
        cat_data = utils.load_json(str(cat_path))
        for item in cat_data.get(item_key, []):
            for field in ("id", f"{item_key.rstrip('s')}_id", "name"):
                if item.get(field):
                    ids.add(item[field])
                    break
    return ids


def collect_mcp_servers():
    if not MCP_CONFIG.exists():
        return set()
    data = utils.load_json(str(MCP_CONFIG))
    return set((data.get("mcpServers") or {}).keys())


def collect_connector_ids():
    if not CONNECTORS_REGISTRY.exists():
        return None
    data = utils.load_json(str(CONNECTORS_REGISTRY))
    return {c.get("id") for c in data.get("connectors", []) if c.get("id")}


def lint_recipe(path, fm, body, parse_err, valid_skills, valid_workflows, valid_mcp, valid_connectors):
    errors, warnings = [], []
    if parse_err:
        errors.append(parse_err)
        return errors, warnings

    for field in ("id", "name", "description", "audience", "version", "status"):
        if not fm.get(field):
            errors.append(f"missing required field: {field}")

    if fm.get("id") and fm["id"] != path.stem:
        errors.append(f"id '{fm['id']}' does not match filename stem '{path.stem}'")

    if fm.get("audience") and fm["audience"] not in VALID_AUDIENCE:
        errors.append(f"audience must be one of {sorted(VALID_AUDIENCE)}; got {fm['audience']!r}")

    status = fm.get("status")
    if status and status not in VALID_STATUS:
        errors.append(f"status must be one of {sorted(VALID_STATUS)}; got {status!r}")

    if "cost" in fm and fm["cost"] not in VALID_COST:
        errors.append(f"cost must be one of {sorted(VALID_COST)}; got {fm['cost']!r}")

    triggers = fm.get("triggers") or {}
    if not any(triggers.get(k) for k in ("cli", "chat", "webhook", "schedule")):
        errors.append("triggers must declare at least one of: cli, chat, webhook, schedule")

    for inp in fm.get("inputs") or []:
        t = inp.get("type")
        if t and t not in VALID_IO_TYPES:
            errors.append(f"input '{inp.get('name','?')}' has invalid type {t!r}")
    for out in fm.get("outputs") or []:
        t = out.get("type")
        if t and t not in VALID_IO_TYPES:
            errors.append(f"output '{out.get('name','?')}' has invalid type {t!r}")

    execu = fm.get("execution") or {}
    etype = execu.get("type")
    if etype not in VALID_EXEC_TYPES:
        errors.append(f"execution.type must be one of {sorted(VALID_EXEC_TYPES)}; got {etype!r}")

    if etype == "prompt" and not re.search(r"^##\s+Prompt\s*$", body or "", re.MULTILINE):
        errors.append("execution.type=prompt requires a '## Prompt' section in the body")
    if etype == "agent" and not re.search(r"^##\s+Agent\s*$", body or "", re.MULTILINE):
        errors.append("execution.type=agent requires a '## Agent' section in the body")

    is_experimental = status == "experimental"

    for sid in fm.get("requires_skills") or []:
        if sid not in valid_skills:
            errors.append(f"requires_skills references unknown skill: {sid}")

    for wid in fm.get("requires_workflows") or []:
        if wid not in valid_workflows:
            errors.append(f"requires_workflows references unknown workflow: {wid}")

    for srv in fm.get("requires_mcp") or []:
        if srv not in valid_mcp:
            errors.append(f"requires_mcp references unknown MCP server: {srv}")

    if valid_connectors is None:
        for conn in fm.get("requires_connectors") or []:
            msg = f"requires_connectors references '{conn}' (no connector registry exists)"
            (warnings if is_experimental else errors).append(msg)
    else:
        for conn in fm.get("requires_connectors") or []:
            if conn not in valid_connectors:
                msg = f"requires_connectors references unknown connector: {conn}"
                (warnings if is_experimental else errors).append(msg)

    entrypoint = execu.get("entrypoint")
    if entrypoint and etype == "workflow":
        if not (ROOT_DIR / entrypoint).exists():
            msg = f"execution.entrypoint not found: {entrypoint}"
            (warnings if is_experimental else errors).append(msg)

    return errors, warnings


def cmd_list(args):
    rows = []
    for path, fm, _body, err in load_all_recipes():
        if err or not fm:
            continue
        if args.audience and fm.get("audience") not in (args.audience, "both"):
            continue
        if args.tag and args.tag not in (fm.get("tags") or []):
            continue
        rows.append((
            fm.get("id", "?"),
            fm.get("audience", "?"),
            fm.get("status", "?"),
            fm.get("description", ""),
        ))

    if not rows:
        print("(no recipes)")
        return

    id_w = max(len("ID"), max(len(r[0]) for r in rows))
    aud_w = max(len("AUD"), max(len(r[1]) for r in rows))
    st_w = max(len("STATUS"), max(len(r[2]) for r in rows))
    print(f"{'ID':<{id_w}}  {'AUD':<{aud_w}}  {'STATUS':<{st_w}}  DESCRIPTION")
    print(f"{'-'*id_w}  {'-'*aud_w}  {'-'*st_w}  {'-'*20}")
    for rid, aud, st, desc in rows:
        print(f"{rid:<{id_w}}  {aud:<{aud_w}}  {st:<{st_w}}  {desc}")


def cmd_show(args):
    target = RECIPES_DIR / f"{args.id}.md"
    if not target.exists():
        print(f"Recipe not found: {args.id}")
        sys.exit(1)
    print(target.read_text(encoding="utf-8"))


def _load_recipe_or_die(recipe_id):
    target = RECIPES_DIR / f"{recipe_id}.md"
    if not target.exists():
        print(f"Recipe not found: {recipe_id}")
        sys.exit(1)
    try:
        fm, body = parse_recipe(target)
    except Exception as e:
        print(f"Failed to parse {target.name}: {e}")
        sys.exit(1)
    return fm, body


_SECTION_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$\n(?P<body>.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL)


def _extract_section(body, title):
    if not body:
        return None
    for m in _SECTION_RE.finditer(body):
        if m.group("title").strip().lower() == title.lower():
            return m.group("body").strip()
    return None


def _execute_recipe(fm, body, inputs):
    execu = fm.get("execution") or {}
    etype = execu.get("type")
    bar = "=" * 60
    print()
    print(bar)
    print(f"  EXECUTE  {fm.get('id')}  type={etype}")
    if inputs:
        print(f"  inputs:  {inputs}")
    print(bar)

    if etype == "prompt":
        prompt = _extract_section(body, "Prompt")
        if prompt:
            preview = prompt[:300] + ("..." if len(prompt) > 300 else "")
            print("[STUB] Would invoke a single AI call with the loaded skills as context.")
            print("       Prompt preview:")
            for line in preview.splitlines():
                print(f"         | {line}")
        else:
            print("[STUB] No '## Prompt' section in body — nothing to invoke.")

    elif etype == "workflow":
        entrypoint = execu.get("entrypoint", "")
        ep_path = ROOT_DIR / entrypoint if entrypoint else None
        if ep_path and ep_path.exists():
            print(f"[STUB] Would POST to n8n webhook for: {entrypoint}")
        else:
            print(f"[STUB] Workflow entrypoint missing: {entrypoint or '(unset)'}")
            print("       Skipping execution — recipe is experimental.")

    elif etype == "agent":
        skills = fm.get("requires_skills") or []
        mcp = fm.get("requires_mcp") or []
        agent_prompt = _extract_section(body, "Agent")
        print(f"[STUB] Would launch an AI agent with:")
        print(f"         skills loaded   : {len(skills)} ({', '.join(skills) or '(none)'})")
        print(f"         MCP tools avail.: {', '.join(mcp) or '(none)'}")
        if agent_prompt:
            preview = agent_prompt[:200] + ("..." if len(agent_prompt) > 200 else "")
            print(f"         agent brief     : {preview}")
        else:
            print(f"         agent brief     : (no '## Agent' section)")

    else:
        print(f"[STUB] Unknown or missing execution.type: {etype!r}")

    print(bar)


def _parse_input_pairs(pairs):
    out = {}
    for p in pairs or []:
        if "=" not in p:
            print(f"Invalid --input value (expected key=value): {p}")
            sys.exit(2)
        k, v = p.split("=", 1)
        out[k.strip()] = v
    return out


def cmd_run(args):
    fm, body = _load_recipe_or_die(args.id)
    inputs = _parse_input_pairs(args.input)

    if fm.get("requires_human_review") and not args.dry_run:
        resp = input(f"Recipe '{fm.get('id')}' has requires_human_review=true. Proceed? [y/N] ").strip().lower()
        if resp != "y":
            print("Aborted.")
            sys.exit(0)

    print(f"Running recipe: {fm.get('id')}")
    _execute_recipe(fm, body, inputs)
    if args.dry_run:
        print()
        print("(dry-run)")


def cmd_lint(args):
    valid_skills = collect_ids_from_split_registry(SKILLS_REGISTRY, "skills")
    valid_workflows = collect_ids_from_split_registry(WORKFLOWS_REGISTRY, "workflows")
    valid_mcp = collect_mcp_servers()
    valid_connectors = collect_connector_ids()

    seen_ids = {}
    total_errors = total_warnings = 0
    any_recipe = False

    for path, fm, body, err in load_all_recipes():
        rid = (fm or {}).get("id") or path.stem
        if args.id and rid != args.id:
            continue
        any_recipe = True
        errors, warnings = lint_recipe(path, fm or {}, body, err, valid_skills, valid_workflows, valid_mcp, valid_connectors)

        if fm and fm.get("id"):
            if fm["id"] in seen_ids:
                errors.append(f"duplicate id (also defined in {seen_ids[fm['id']].name})")
            else:
                seen_ids[fm["id"]] = path

        if not errors and not warnings:
            print(f"OK    {rid}")
        else:
            for e in errors:
                print(f"ERR   {rid}: {e}")
            for w in warnings:
                print(f"WARN  {rid}: {w}")
        total_errors += len(errors)
        total_warnings += len(warnings)

    if not any_recipe:
        print("(no recipes)" if not args.id else f"Recipe not found: {args.id}")
        sys.exit(1 if args.id else 0)

    print()
    print(f"Total: {total_errors} error(s), {total_warnings} warning(s).")
    sys.exit(1 if total_errors else 0)


def cmd_sync(args):
    entries = []
    for path, fm, _body, err in load_all_recipes():
        if err or not fm:
            print(f"SKIP  {path.name}: {err or 'parse failure'}")
            continue
        entries.append({
            "id": fm.get("id"),
            "name": fm.get("name"),
            "description": fm.get("description"),
            "audience": fm.get("audience"),
            "status": fm.get("status"),
            "tags": fm.get("tags") or [],
            "path": f"recipes/{path.name}",
        })
    entries.sort(key=lambda e: e["id"] or "")

    registry = {
        "version": "1.0.0",
        "type": "recipe_registry",
        "recipes": entries,
    }

    if args.check:
        existing = utils.load_json(str(RECIPES_REGISTRY)) if RECIPES_REGISTRY.exists() else {}
        if existing.get("recipes") != entries:
            print("Registry out of sync. Run 'recipe sync' to regenerate.")
            sys.exit(1)
        print("Registry in sync.")
        return

    RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    utils.save_json(str(RECIPES_REGISTRY), registry)
    rel = RECIPES_REGISTRY.relative_to(ROOT_DIR)
    print(f"Wrote {rel} ({len(entries)} recipe(s)).")


def main():
    parser = argparse.ArgumentParser(description="Recipe Manager")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List recipes")
    p_list.add_argument("--audience", choices=sorted(VALID_AUDIENCE))
    p_list.add_argument("--tag")

    p_show = sub.add_parser("show", help="Print a recipe file")
    p_show.add_argument("id")

    p_lint = sub.add_parser("lint", help="Validate recipe references")
    p_lint.add_argument("id", nargs="?")

    p_sync = sub.add_parser("sync", help="Regenerate recipes/registry.json")
    p_sync.add_argument("--check", action="store_true", help="Verify registry matches current recipes")

    p_run = sub.add_parser("run", help="Run a recipe (executes per execution.type; currently stubbed)")
    p_run.add_argument("id")
    p_run.add_argument("--input", action="append", help="key=value pair, can be repeated")
    p_run.add_argument("--dry-run", action="store_true", help="Show execution plan without invoking real dispatchers")

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "show":
        cmd_show(args)
    elif args.cmd == "lint":
        cmd_lint(args)
    elif args.cmd == "sync":
        cmd_sync(args)
    elif args.cmd == "run":
        cmd_run(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
