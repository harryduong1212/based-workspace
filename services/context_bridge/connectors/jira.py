"""Jira connector adapter — issue payload → (source_id, content, metadata)."""
from __future__ import annotations
from typing import Iterator


def adapt(payload: dict) -> Iterator[tuple[str, str, dict]]:
    """Yield one tuple per issue. Skips issues without a `key`.

    `content` is summary + description + concatenated comments. `metadata`
    captures status, assignee, and the bare summary for display.
    """
    for issue in payload.get("issues", []) or []:
        key = issue.get("key")
        if not key:
            continue
        fields = issue.get("fields") or {}
        summary = (fields.get("summary") or "").strip()
        description = (fields.get("description") or "").strip()

        comments_raw = (fields.get("comment") or {}).get("comments") or []
        comment_lines = []
        for c in comments_raw:
            author = (c.get("author") or {}).get("displayName") or "?"
            body = (c.get("body") or "").strip()
            if body:
                comment_lines.append(f"{author}: {body}")

        parts = []
        if summary:
            parts.append(summary)
        if description:
            parts.append(description)
        if comment_lines:
            parts.append("Comments:\n" + "\n".join(comment_lines))
        content = "\n\n".join(parts)

        metadata = {
            "summary": summary,
            "status": (fields.get("status") or {}).get("name"),
            "assignee": (fields.get("assignee") or {}).get("displayName"),
        }
        yield (key, content, metadata)
