#!/usr/bin/env python3
"""Connector Manager CLI — list, show, lint, and sync the connector registry."""

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import utils

ROOT_DIR = Path(utils.BASE_DIR)
CONNECTORS_DIR = ROOT_DIR / "connectors"
CONNECTORS_REGISTRY = CONNECTORS_DIR / "registry.json"

VALID_STATUS = {"experimental", "stable", "deprecated"}
VALID_AUTH = {"api_token", "oauth2", "basic", "bearer", "none"}
REQUIRED_FIELDS = ("id", "name", "description", "status", "provides", "auth_type", "requires_env")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_connector(path):
    content = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        raise ValueError("missing or malformed frontmatter")
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def load_all_connectors():
    if not CONNECTORS_DIR.exists():
        return
    for path in sorted(CONNECTORS_DIR.glob("*.md")):
        try:
            fm, body = parse_connector(path)
            yield path, fm, body, None
        except Exception as e:
            yield path, None, None, str(e)


def lint_connector(path, fm, parse_err):
    errors = []
    if parse_err:
        errors.append(parse_err)
        return errors

    for field in REQUIRED_FIELDS:
        if not fm.get(field):
            errors.append(f"missing required field: {field}")

    if fm.get("id") and fm["id"] != path.stem:
        errors.append(f"id '{fm['id']}' does not match filename stem '{path.stem}'")

    status = fm.get("status")
    if status and status not in VALID_STATUS:
        errors.append(f"status must be one of {sorted(VALID_STATUS)}; got {status!r}")

    auth = fm.get("auth_type")
    if auth and auth not in VALID_AUTH:
        errors.append(f"auth_type must be one of {sorted(VALID_AUTH)}; got {auth!r}")

    provides = fm.get("provides")
    if provides is not None and not isinstance(provides, list):
        errors.append("provides must be a list")

    requires_env = fm.get("requires_env")
    if requires_env is not None and not isinstance(requires_env, list):
        errors.append("requires_env must be a list")

    return errors


def cmd_list(args):
    rows = []
    for path, fm, _body, err in load_all_connectors():
        if err or not fm:
            continue
        if args.status and fm.get("status") != args.status:
            continue
        if args.tag and args.tag not in (fm.get("tags") or []):
            continue
        rows.append((
            fm.get("id", "?"),
            fm.get("status", "?"),
            fm.get("auth_type", "?"),
            fm.get("description", ""),
        ))

    if not rows:
        print("(no connectors)")
        return

    id_w = max(len("ID"), max(len(r[0]) for r in rows))
    st_w = max(len("STATUS"), max(len(r[1]) for r in rows))
    auth_w = max(len("AUTH"), max(len(r[2]) for r in rows))
    print(f"{'ID':<{id_w}}  {'STATUS':<{st_w}}  {'AUTH':<{auth_w}}  DESCRIPTION")
    print(f"{'-'*id_w}  {'-'*st_w}  {'-'*auth_w}  {'-'*20}")
    for cid, st, auth, desc in rows:
        print(f"{cid:<{id_w}}  {st:<{st_w}}  {auth:<{auth_w}}  {desc}")


def cmd_show(args):
    target = CONNECTORS_DIR / f"{args.id}.md"
    if not target.exists():
        print(f"Connector not found: {args.id}")
        sys.exit(1)
    print(target.read_text(encoding="utf-8"))


def cmd_lint(args):
    file_ids = set()
    seen_ids = {}
    total_errors = 0
    any_connector = False

    for path, fm, _body, err in load_all_connectors():
        cid = (fm or {}).get("id") or path.stem
        if args.id and cid != args.id:
            continue
        any_connector = True
        errors = lint_connector(path, fm or {}, err)

        if fm and fm.get("id"):
            file_ids.add(fm["id"])
            if fm["id"] in seen_ids:
                errors.append(f"duplicate id (also defined in {seen_ids[fm['id']].name})")
            else:
                seen_ids[fm["id"]] = path

        if not errors:
            print(f"OK    {cid}")
        else:
            for e in errors:
                print(f"ERR   {cid}: {e}")
        total_errors += len(errors)

    if args.id:
        if not any_connector:
            print(f"Connector not found: {args.id}")
            sys.exit(1)
    else:
        registry_ids = set()
        if CONNECTORS_REGISTRY.exists():
            data = utils.load_json(str(CONNECTORS_REGISTRY))
            for entry in data.get("connectors", []):
                cid = entry.get("id")
                if cid:
                    registry_ids.add(cid)
                entry_path = ROOT_DIR / (entry.get("path") or "")
                if entry.get("path") and not entry_path.exists():
                    print(f"ERR   registry: '{cid}' points at missing file: {entry.get('path')}")
                    total_errors += 1
        else:
            print("ERR   registry: connectors/registry.json missing")
            total_errors += 1

        for cid in sorted(registry_ids - file_ids):
            print(f"ERR   registry: entry '{cid}' has no matching file in connectors/")
            total_errors += 1
        for cid in sorted(file_ids - registry_ids):
            print(f"ERR   {cid}: file is not listed in registry.json")
            total_errors += 1

    print()
    print(f"Total: {total_errors} error(s).")
    sys.exit(1 if total_errors else 0)


def cmd_sync(args):
    entries = []
    for path, fm, _body, err in load_all_connectors():
        if err or not fm:
            print(f"SKIP  {path.name}: {err or 'parse failure'}")
            continue
        entries.append({
            "id": fm.get("id"),
            "name": fm.get("name"),
            "description": fm.get("description"),
            "status": fm.get("status"),
            "provides": fm.get("provides") or [],
            "tags": fm.get("tags") or [],
            "path": f"connectors/{path.name}",
        })
    entries.sort(key=lambda e: e["id"] or "")

    registry = {
        "version": "1.0.0",
        "type": "connector_registry",
        "connectors": entries,
    }

    if args.check:
        existing = utils.load_json(str(CONNECTORS_REGISTRY)) if CONNECTORS_REGISTRY.exists() else {}
        if existing.get("connectors") != entries:
            print("Registry out of sync. Run 'connector_manager.py sync' to regenerate.")
            sys.exit(1)
        print("Registry in sync.")
        return

    CONNECTORS_DIR.mkdir(parents=True, exist_ok=True)
    utils.save_json(str(CONNECTORS_REGISTRY), registry)
    rel = CONNECTORS_REGISTRY.relative_to(ROOT_DIR)
    print(f"Wrote {rel} ({len(entries)} connector(s)).")


def main():
    parser = argparse.ArgumentParser(description="Connector Manager")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List connectors")
    p_list.add_argument("--status", choices=sorted(VALID_STATUS))
    p_list.add_argument("--tag")

    p_show = sub.add_parser("show", help="Print a connector file")
    p_show.add_argument("id")

    p_lint = sub.add_parser("lint", help="Validate connector files and registry")
    p_lint.add_argument("id", nargs="?")

    p_sync = sub.add_parser("sync", help="Regenerate connectors/registry.json")
    p_sync.add_argument("--check", action="store_true", help="Verify registry matches current connectors")

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "show":
        cmd_show(args)
    elif args.cmd == "lint":
        cmd_lint(args)
    elif args.cmd == "sync":
        cmd_sync(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
