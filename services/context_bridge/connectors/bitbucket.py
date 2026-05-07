"""Bitbucket connector adapter — PR payload → (source_id, content, metadata)."""
from __future__ import annotations
from typing import Iterator


def adapt(payload: dict) -> Iterator[tuple[str, str, dict]]:
    """Yield one tuple per PR in `values[]`. Skips PRs without an `id`.

    `content` is title + description + concatenated comments (when the
    fixture or API response inlines them). `metadata` captures state,
    author, source branch, and the bare title for display.

    Bitbucket Cloud puts comments on a separate endpoint; both inlined
    `comments` arrays and absent ones are tolerated.
    """
    for pr in payload.get("values", []) or []:
        pr_id = pr.get("id")
        if pr_id is None:
            continue
        title = (pr.get("title") or "").strip()
        description = (pr.get("description") or "").strip()

        comments_raw = pr.get("comments") or []
        comment_lines = []
        for c in comments_raw:
            author = (c.get("user") or {}).get("display_name") or "?"
            body = ((c.get("content") or {}).get("raw") or "").strip()
            if not body:
                body = (c.get("body") or "").strip()
            if body:
                comment_lines.append(f"{author}: {body}")

        parts = []
        if title:
            parts.append(title)
        if description:
            parts.append(description)
        if comment_lines:
            parts.append("Comments:\n" + "\n".join(comment_lines))
        content = "\n\n".join(parts)

        metadata = {
            "title": title,
            "state": pr.get("state"),
            "author": (pr.get("author") or {}).get("display_name"),
            "branch": ((pr.get("source") or {}).get("branch") or {}).get("name"),
        }
        yield (str(pr_id), content, metadata)
