"""Markdown rendering helper. Lazy-imports `markdown` so the package stays
importable when UI deps aren't installed."""
from __future__ import annotations


def render_markdown(text: str) -> str:
    """Render `text` to HTML with sensible extensions for recipe bodies."""
    import markdown  # local import — see module docstring

    return markdown.markdown(
        text or "",
        extensions=["fenced_code", "tables", "toc", "sane_lists"],
        output_format="html5",
    )
