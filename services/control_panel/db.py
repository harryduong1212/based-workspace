"""SQLite-backed persistence for runs + recipe input history.

Single file at `<workspace>/.cache/control_panel.db`. WAL mode so the SSE
streamer (reading) can coexist with the run worker (writing) without
blocking. The connection is opened with `check_same_thread=False` because
runs spawn worker threads that write back into the DB.

Why SQLite (not Postgres or JSON):
- Stdlib only — no extra dep, no service to start.
- ACID safe under concurrent writes (run worker streaming + reads from UI).
- Single file, easy to back up or wipe (`rm runs.db*`).
- The volumes are small: O(1k) runs, O(100) input-history rows.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS runs (
        id          TEXT PRIMARY KEY,
        recipe_id   TEXT NOT NULL,
        model_ref   TEXT NOT NULL,
        inputs_json TEXT NOT NULL,
        status      TEXT NOT NULL,
        error       TEXT,
        output      TEXT NOT NULL DEFAULT '',
        started_at  TEXT NOT NULL,
        ended_at    TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS runs_by_recipe ON runs (recipe_id, started_at DESC)",
    "CREATE INDEX IF NOT EXISTS runs_by_started ON runs (started_at DESC)",
    """
    CREATE TABLE IF NOT EXISTS recipe_input_history (
        recipe_id   TEXT NOT NULL,
        input_name  TEXT NOT NULL,
        value       TEXT NOT NULL,
        updated_at  TEXT NOT NULL,
        PRIMARY KEY (recipe_id, input_name)
    )
    """,
]


_lock = threading.Lock()
_conn: sqlite3.Connection | None = None
_db_path: Path | None = None


@dataclass(frozen=True)
class RunRow:
    id: str
    recipe_id: str
    model_ref: str
    inputs: dict[str, str]
    status: str
    error: str | None
    output: str
    started_at: datetime
    ended_at: datetime | None


def _resolve_path(workspace_root: Path) -> Path:
    return workspace_root / ".cache" / "control_panel.db"


def init(workspace_root: Path) -> None:
    """Open / create the DB and apply schema. Idempotent — calling again
    with the same workspace is a no-op; with a different workspace, the old
    connection is closed cleanly first."""
    global _conn, _db_path
    with _lock:
        path = _resolve_path(workspace_root)
        if _conn is not None and _db_path == path:
            return
        if _conn is not None:
            _conn.close()
            _conn = None
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path), check_same_thread=False, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=NORMAL")
        for stmt in _SCHEMA:
            conn.execute(stmt)
        _conn = conn
        _db_path = path
        # Mark any runs left in 'running' state by a previous process as
        # abandoned — they'll never produce more output.
        _conn.execute(
            "UPDATE runs SET status='abandoned', ended_at=? "
            "WHERE status='running' AND ended_at IS NULL",
            (_now_iso(),),
        )


def close() -> None:
    """Test helper — close the singleton connection."""
    global _conn, _db_path
    with _lock:
        if _conn is not None:
            _conn.close()
        _conn = None
        _db_path = None


@contextmanager
def _cursor() -> Iterator[sqlite3.Cursor]:
    if _conn is None:
        raise RuntimeError("db.init() was not called")
    with _lock:
        cur = _conn.cursor()
        try:
            yield cur
        finally:
            cur.close()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.fromisoformat(s)


def _row_to_run(row: sqlite3.Row) -> RunRow:
    return RunRow(
        id=row["id"],
        recipe_id=row["recipe_id"],
        model_ref=row["model_ref"],
        inputs=json.loads(row["inputs_json"]) if row["inputs_json"] else {},
        status=row["status"],
        error=row["error"],
        output=row["output"] or "",
        started_at=datetime.fromisoformat(row["started_at"]),
        ended_at=_parse_iso(row["ended_at"]),
    )


def insert_run(
    *,
    run_id: str,
    recipe_id: str,
    model_ref: str,
    inputs: dict[str, str],
    started_at: datetime,
) -> None:
    with _cursor() as cur:
        cur.execute(
            "INSERT INTO runs (id, recipe_id, model_ref, inputs_json, status, output, started_at) "
            "VALUES (?, ?, ?, ?, 'running', '', ?)",
            (run_id, recipe_id, model_ref, json.dumps(inputs), started_at.isoformat(timespec="seconds")),
        )


def finish_run(*, run_id: str, status: str, output: str, error: str | None) -> None:
    with _cursor() as cur:
        cur.execute(
            "UPDATE runs SET status=?, output=?, error=?, ended_at=? WHERE id=?",
            (status, output, error, _now_iso(), run_id),
        )


def get_run_row(run_id: str) -> RunRow | None:
    with _cursor() as cur:
        row = cur.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
    return _row_to_run(row) if row else None


def recent_runs(limit: int = 25, recipe_id: str | None = None) -> list[RunRow]:
    sql = "SELECT * FROM runs"
    params: tuple[Any, ...] = ()
    if recipe_id is not None:
        sql += " WHERE recipe_id=?"
        params = (recipe_id,)
    sql += " ORDER BY started_at DESC LIMIT ?"
    params = (*params, int(limit))
    with _cursor() as cur:
        rows = cur.execute(sql, params).fetchall()
    return [_row_to_run(r) for r in rows]


def save_recipe_inputs(recipe_id: str, values: dict[str, str]) -> None:
    """Upsert each (recipe_id, input_name) → value. Empty values are deleted
    so the next render re-shows the placeholder rather than a blank input."""
    if not values:
        return
    now = _now_iso()
    with _cursor() as cur:
        for name, value in values.items():
            if value == "":
                cur.execute(
                    "DELETE FROM recipe_input_history WHERE recipe_id=? AND input_name=?",
                    (recipe_id, name),
                )
            else:
                cur.execute(
                    "INSERT INTO recipe_input_history (recipe_id, input_name, value, updated_at) "
                    "VALUES (?, ?, ?, ?) "
                    "ON CONFLICT (recipe_id, input_name) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                    (recipe_id, name, value, now),
                )


def get_recipe_inputs(recipe_id: str) -> dict[str, str]:
    with _cursor() as cur:
        rows = cur.execute(
            "SELECT input_name, value FROM recipe_input_history WHERE recipe_id=?",
            (recipe_id,),
        ).fetchall()
    return {r["input_name"]: r["value"] for r in rows}
