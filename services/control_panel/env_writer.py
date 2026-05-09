"""Read + atomic-write workspace `.env` for the connector env editor.

Format is the lowest-common-denominator dotenv shape: `KEY=VALUE` per line, blank
lines and `# comments` preserved. Quoting is preserved on read (we round-trip
the original line whenever a key isn't being updated). On update, values are
serialized as `KEY=VALUE` without quoting unless the value contains whitespace
or a `#`, in which case it's wrapped in double quotes.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class EnvLine:
    raw: str          # original line as read (without trailing newline)
    key: str | None   # key when the line is a KEY=VALUE assignment, else None


def parse_env_text(text: str) -> tuple[list[EnvLine], dict[str, str]]:
    """Return (line index, key→value dict)."""
    lines: list[EnvLine] = []
    values: dict[str, str] = {}
    for raw in text.splitlines():
        stripped = raw.lstrip()
        if not stripped or stripped.startswith("#"):
            lines.append(EnvLine(raw=raw, key=None))
            continue
        head, sep, rest = raw.partition("=")
        key = head.strip()
        if not sep or not key or not _looks_like_key(key):
            lines.append(EnvLine(raw=raw, key=None))
            continue
        # Strip optional `export ` prefix without dropping it from the raw line.
        if key.startswith("export "):
            key = key[len("export "):].strip()
        values[key] = _unquote(rest.strip())
        lines.append(EnvLine(raw=raw, key=key))
    return lines, values


def _looks_like_key(s: str) -> bool:
    s = s.removeprefix("export ").strip()
    return bool(s) and (s[0].isalpha() or s[0] == "_") and all(c.isalnum() or c == "_" for c in s)


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _quote(value: str) -> str:
    if value == "" or any(c.isspace() for c in value) or "#" in value or "$" in value:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def render_env_text(lines: list[EnvLine], updates: dict[str, str]) -> str:
    """Apply `updates` to the line index. Existing keys are rewritten in place;
    new keys are appended at the end (in iteration order)."""
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        if line.key is not None and line.key in updates:
            seen.add(line.key)
            new_val = updates[line.key]
            prefix = "export " if line.raw.lstrip().startswith("export ") else ""
            out.append(f"{prefix}{line.key}={_quote(new_val)}")
        else:
            out.append(line.raw)
    new_keys = [k for k in updates if k not in seen]
    if new_keys:
        if out and out[-1] != "":
            out.append("")
        for k in new_keys:
            out.append(f"{k}={_quote(updates[k])}")
    text = "\n".join(out)
    if not text.endswith("\n"):
        text += "\n"
    return text


def update_env_file(env_path: Path, updates: dict[str, str]) -> None:
    """Atomically write `updates` to `env_path`. Creates the file if missing."""
    if not updates:
        return
    if env_path.exists():
        existing = env_path.read_text(encoding="utf-8")
    else:
        existing = ""
    lines, _ = parse_env_text(existing)
    new_text = render_env_text(lines, updates)
    env_path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".env.", suffix=".tmp", dir=str(env_path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(new_text)
        os.replace(tmp, env_path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def read_env_values(env_path: Path) -> dict[str, str]:
    """Return parsed values from .env (empty dict if missing)."""
    if not env_path.exists():
        return {}
    _, values = parse_env_text(env_path.read_text(encoding="utf-8"))
    return values


def filter_to_allowed(updates: dict[str, str], allowed: Iterable[str]) -> dict[str, str]:
    """Drop any key not in `allowed`. Used as a safety filter to ensure the
    connector env editor can only write the connector's declared `requires_env`."""
    allow = set(allowed)
    return {k: v for k, v in updates.items() if k in allow}
