"""Walks `.archived/skills/<category>/<skill>/SKILL.md` and yields parsed docs.

Each SKILL.md has YAML frontmatter (name, description, risk, source,
date_added) plus a Markdown body. The indexer parses the frontmatter and
returns a flat `SkillDoc` record per file — the embedder later turns each
record's `text_for_embedding` into a 384-dim vector.

Kept dependency-light: only stdlib + PyYAML. No FastMCP / Qdrant here so
this module is trivially unit-testable.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Iterable, Iterator

import yaml


# `description` from frontmatter is the headline signal; we also include the
# first chunk of the body so semantic queries can match on examples / "use
# this when" prose. Cap at 800 chars (≈ 200 BPE tokens) so description +
# body stays well under bge-small's 512-token context — some skill bodies
# are code-heavy and dense, so a tight cap matters.
_BODY_CHARS_FOR_EMBED = 800

# Combined description + body is hard-capped before sending to the embedder.
# bge-small-en-v1.5 has a 512-token context; llama-swap errors strictly on
# overflow rather than silently truncating. A few skills have unusually long
# descriptions (200+ words) or code-heavy bodies where chars/token is low,
# so we trim the final text to ~1500 chars (~400 tokens with headroom).
_TEXT_FOR_EMBEDDING_MAX = 1500

_FRONTMATTER_DELIM = "---"


@dataclasses.dataclass(frozen=True)
class SkillDoc:
    """One indexable skill — what we hand to the embedder + store."""

    name: str
    description: str
    category: str
    path: str  # repo-relative SKILL.md path, stable id surrogate
    risk: str
    source: str
    body_excerpt: str  # body trimmed to ~1200 chars for embedding

    @property
    def text_for_embedding(self) -> str:
        """The string that goes through bge-small. Description leads because
        the user's natural query ("how do I X") looks like a description, not
        like a name or path. Hard-capped to _TEXT_FOR_EMBEDDING_MAX so a long
        description + body never blows past bge-small's 512-token context
        (llama-swap errors strictly on overflow rather than truncating)."""
        text = f"{self.description}\n\n{self.body_excerpt}".strip()
        if len(text) > _TEXT_FOR_EMBEDDING_MAX:
            text = text[:_TEXT_FOR_EMBEDDING_MAX]
        return text

    def payload(self) -> dict[str, object]:
        """What we store alongside the vector — surfaced back to the caller
        verbatim, so keep it small (no full body)."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "path": self.path,
            "risk": self.risk,
            "source": self.source,
        }


def parse_skill_md(text: str, *, path: str, category: str) -> SkillDoc | None:
    """Parse one SKILL.md. Returns None if frontmatter is missing/unreadable —
    skills without proper metadata are skipped silently rather than crashing
    a full reindex on one bad file. Caller can `len(docs)` to count what
    survived."""
    if not text.startswith(_FRONTMATTER_DELIM):
        return None

    # `---\n<yaml>\n---\n<body>` — split on the second delimiter only.
    rest = text[len(_FRONTMATTER_DELIM):].lstrip("\n")
    end_idx = rest.find(f"\n{_FRONTMATTER_DELIM}")
    if end_idx == -1:
        return None
    fm_text = rest[:end_idx]
    body = rest[end_idx + len(_FRONTMATTER_DELIM) + 1 :].lstrip("\n")

    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None

    name = str(fm.get("name") or "").strip()
    description = str(fm.get("description") or "").strip()
    if not name or not description:
        # name + description are load-bearing for search; skip silently.
        return None

    return SkillDoc(
        name=name,
        description=description,
        category=category,
        path=path,
        risk=str(fm.get("risk") or "unknown"),
        source=str(fm.get("source") or "unknown"),
        body_excerpt=body[:_BODY_CHARS_FOR_EMBED],
    )


def walk_skills(skills_dir: Path) -> Iterator[SkillDoc]:
    """Yield one SkillDoc per readable SKILL.md under
    `<skills_dir>/<category>/<skill-name>/SKILL.md`. Order is filesystem-
    dependent — collection upserts are by stable id, so order doesn't matter."""
    if not skills_dir.exists():
        return
    for category_dir in sorted(skills_dir.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        for skill_dir in sorted(category_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            try:
                text = skill_md.read_text(encoding="utf-8")
            except OSError:
                continue
            doc = parse_skill_md(
                text,
                path=str(skill_md.relative_to(skills_dir.parent.parent))
                if skills_dir.parent.parent in skill_md.parents
                else str(skill_md),
                category=category,
            )
            if doc is not None:
                yield doc


def index_skills(skills_dir: Path) -> list[SkillDoc]:
    """Eager wrapper around `walk_skills` — convenient for callers that need
    to know the total count up-front (e.g. CLI progress display)."""
    return list(walk_skills(skills_dir))


def stable_point_id(doc: SkillDoc) -> int:
    """Qdrant requires int or UUID point ids. We hash `category/name` to a
    64-bit positive int so reindexing the same skill upserts (replaces)
    rather than duplicating. SHA-1 is fine here — no security need, just
    deterministic bucketing."""
    import hashlib

    key = f"{doc.category}/{doc.name}".encode("utf-8")
    digest = hashlib.sha1(key, usedforsecurity=False).digest()
    # Top 8 bytes as unsigned int — keeps within positive int64.
    return int.from_bytes(digest[:8], "big") & ((1 << 63) - 1)


# Backwards-friendly alias for callers that iterate without needing the list.
def iter_skills(skills_dir: Path) -> Iterable[SkillDoc]:
    return walk_skills(skills_dir)
