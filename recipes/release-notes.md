---
id: release-notes
name: Release Notes
description: Generate release notes for a tag-to-tag (or tag-to-HEAD) range — classified into Features, Fixes, Breaking changes, and the rest, ready to paste into GitHub/GitLab.
audience: tech
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [release, changelog, git]

requires_skills:
  - wiki-changelog
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env: []

triggers:
  cli: release-notes
  chat:
    - "draft release notes"
    - "changelog since"
    - "release notes for"

inputs:
  - name: from_ref
    type: string
    required: false
    description: Starting ref (tag, SHA, or branch). When omitted, uses the previous tag reachable from `to_ref`.
  - name: to_ref
    type: string
    required: false
    description: Ending ref. Defaults to `HEAD`.
  - name: title
    type: string
    required: false
    description: Optional release title (e.g., "v1.4.0 — auth overhaul"). When omitted, uses the resolved `to_ref`.
  - name: format
    type: string
    required: false
    description: "`markdown` (default) or `github` (GitHub-flavored release body with collapsible Contributors section)."

outputs:
  - name: release_notes
    type: markdown
    description: Release notes body — title, summary, classified change list, breaking-changes callout, contributors.

execution:
  type: agent
---

## What this does
Reads the commits between two refs (defaulting to "previous tag → HEAD"), classifies each into Features / Fixes / Refactor / Docs / Performance / Breaking, and produces a release notes body ready to paste into a GitHub release, GitLab tag note, or `CHANGELOG.md` entry.

## Who it's for
Anyone tagging a release who doesn't want to hand-classify 30 commits into the right buckets, write the user-facing summary line, and chase down who contributed.

## What you need
- A git checkout with the relevant commits and tags reachable.

## How to run
- **In Antigravity or Claude Code:** say *"draft release notes for v1.4.0"* or run `/release-notes`.
- **CLI:**
  - Default (previous tag → HEAD): `python scripts/recipe_manager.py run release-notes`
  - Specific range: `python scripts/recipe_manager.py run release-notes --input from_ref=v1.3.0 --input to_ref=v1.4.0 --input title="v1.4.0 — auth overhaul"`
  - GitHub format: `python scripts/recipe_manager.py run release-notes --input format=github`

## Example output

> # v1.4.0 — auth overhaul
>
> **Summary.** Replaces the implicit-grant OAuth flow with PKCE on the SPA, adds per-tenant rate limiting on the gateway, and removes the legacy session-token storage flagged by the security audit.
>
> ## ⚠️ Breaking changes
> - `POST /v1/auth/login` no longer returns a session cookie. Clients must complete the PKCE flow at `/oauth/authorize` and use the resulting bearer token. See migration notes in `docs/auth/migration-1.4.md`.
>
> ## 🆕 Features
> - Per-tenant rate limiting on the gateway with `X-RateLimit-*` headers (PROJ-412).
> - Audit log retention controls now configurable per workspace (PROJ-419).
>
> ## 🐛 Fixes
> - Redis lookup deadlock under load — token validation now wraps in a 500ms timeout (PR #251).
> - `tests/auth/test_token_revocation` flakiness — race in fixture teardown.
>
> ## 🔄 Refactor
> - `auth/middleware.py` now reads config via dependency injection rather than module globals.
>
> ## 📝 Docs
> - PKCE migration guide and updated OAuth quickstart.
>
> ## Contributors
> @harryduong1212, @reviewer-a, @reviewer-b — thank you.

## Agent

You generate release notes from a git commit range. Output is a single Markdown document. You do not push, tag, or open a release — only draft.

### Phase 1 — Resolve the range

1. **`to_ref`**: use `{input.to_ref}` if set; otherwise `HEAD`.
2. **`from_ref`**: use `{input.from_ref}` if set; otherwise resolve the previous tag reachable from `to_ref`:
   - `git describe --tags --abbrev=0 <to_ref>^` — gives the most recent tag strictly before `to_ref`.
   - If no prior tag exists, fall back to the merge-base with `main` (or `master`/`develop`) and note the assumption in the output.
3. Verify both refs exist: `git rev-parse <ref>`. If either fails, stop and tell the user.
4. **Title**: use `{input.title}` if set; else use the resolved `to_ref`.

### Phase 2 — Gather

- `git log --pretty='%H%x09%an%x09%s%x09%b%x00' <from>..<to>` — full commit list with author, subject, body. Null-byte separator avoids subject/body confusion.
- `git diff --stat <from>..<to>` — high-level scope (file-change summary, useful for the summary line).
- Read `.github/release.yml` if present (GitHub release-notes config); honor any author/label exclusions it declares.

### Phase 3 — Classify

Apply `wiki-changelog` to bucket each commit into one of:
- 🆕 **Features** — `feat:` commits and new user-visible behavior
- 🐛 **Fixes** — `fix:` commits and bug fixes from non-conventional commits
- ⚡ **Performance** — `perf:` commits
- 🔄 **Refactor** — `refactor:` commits with no behavior change
- 📝 **Docs** — `docs:` commits
- 🔧 **Chore / CI / Build** — fold into one collapsed section
- ⚠️ **Breaking changes** — any commit with `BREAKING CHANGE:` in the body, or `<type>!:` syntax

Merge related commits — one user-facing bullet per coherent change, not one per commit. Cite ticket / PR references where they appear in the commit message ("PROJ-412", "PR #251", "fixes #287").

### Phase 4 — Draft

Default body shape:

```
# <title>

**Summary.** <2-3 sentence narrative — what shipped and why; surface the user-facing story, not the commit-graph view>

## ⚠️ Breaking changes        # only if any
- ...

## 🆕 Features
- ...

## 🐛 Fixes
- ...

## ⚡ Performance              # only if any
- ...

## 🔄 Refactor                 # only if non-trivial
- ...

## 📝 Docs                     # only if any
- ...

## Contributors
<unique authors from the range, @-handled — pull names from `git log --pretty='%an'`; deduplicate>
```

When `{input.format}` is `github`, additionally:
- Wrap the Refactor / Docs / Chore sections in `<details><summary>...</summary>...</details>` so the release page stays scannable.
- Append a `**Full Changelog:** https://github.com/<repo>/compare/<from>...<to>` line — leave `<repo>` as a placeholder if you can't infer it from `git remote -v`.

### Constraints

- **Do not** invent commits, tickets, or behavior the diff doesn't show.
- **Do not** push tags or run `gh release create` — only draft text.
- **Highlight breaking changes prominently.** Even one earns the ⚠️ section above Features.
- **Skip empty sections.** If there are no Performance commits, omit the section entirely.
- If the resolved range is empty (zero commits), say so and stop — don't fabricate.
- Cap individual bullets at one screen-line each. Detail belongs in linked sub-docs or commit bodies, not the release notes.
