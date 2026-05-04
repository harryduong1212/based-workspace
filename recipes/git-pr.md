---
id: git-pr
name: Git PR Description
description: Draft a pull request title and description from the current branch's commits and diff against a target branch.
audience: tech
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [git, pr, code-review]

requires_skills:
  - wiki-changelog
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env: []

triggers:
  cli: git-pr
  chat:
    - "draft a PR description"
    - "create pull request description"
    - "git pr"

inputs:
  - name: target_branch
    type: string
    required: false
    description: Branch to diff against. Defaults to `main`.
  - name: issue_number
    type: string
    required: false
    description: Linked issue or ticket reference (e.g., "PROJ-412", "#287").

outputs:
  - name: pr_markdown
    type: markdown
    description: PR title plus body, ready to paste into the host (GitHub, Bitbucket, GitLab).

execution:
  type: agent
---

## What this does
Reads the current branch's commits and diff against a target branch, classifies the changes, and produces a pull request title and body — including a summary, change list, and breaking-change callouts — ready to paste into the host.

## Who it's for
Engineers who don't want to write the same "## Summary / ## Changes / ## Testing" boilerplate by hand on every PR. Replaces the legacy `.archived/workflows/git-collaboration/git-pr.md` (Phase D2 migration).

## What you need
- A working git checkout with commits ahead of the target branch.
- (Optional) A `.github/PULL_REQUEST_TEMPLATE.md` or `.github/pull_request_template.md` — if present, the agent uses its structure.

## How to run
- **In Antigravity or Claude Code:** say *"draft a PR description"* or run the `/git-pr` slash command.
- **CLI:** `python scripts/recipe_manager.py run git-pr --input target_branch=main --input issue_number=PROJ-412`

## Example output

> **Title:** `feat(auth): per-tenant rate limiting on the gateway`
>
> **## Summary**
> Adds a token-bucket rate limiter to the public API gateway to prevent noisy-neighbor incidents (PROJ-412). Per-tenant budget; per-endpoint quotas deferred.
>
> **## Changes**
> - 🆕 `gateway/ratelimit.py` — token-bucket implementation backed by Redis.
> - 🆕 `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers on every response.
> - 🔄 `gateway/middleware.py` — wires the limiter into the request path.
> - 🐛 `tests/gateway/test_redis_timeout.py` — covers the timeout case PR #251 missed.
>
> **## Related**
> Closes PROJ-412.
>
> **## Testing**
> - Unit: `pytest tests/gateway/`
> - Manual: hammered `/v1/echo` with `hey -n 5000 -c 50`; saw clean 429s past 1k req/min.

## Agent

You draft pull request descriptions from a branch's commits and diff. Your output is a single Markdown document: a one-line title, then the body.

### Phase 1 — Gather

1. Resolve the target branch:
   - If `{input.target_branch}` is set, use it.
   - Otherwise, prefer `main`, then `master`, then `develop` — the first one that exists locally.
2. Run:
   - `git log <target>..HEAD --oneline` — commit list.
   - `git diff <target>...HEAD --stat` — file change summary.
   - `git diff <target>...HEAD` — full diff (truncate to ~2000 lines for the prompt; mention truncation).
3. Read `.github/PULL_REQUEST_TEMPLATE.md` or `.github/pull_request_template.md` if either exists. If found, follow its section structure instead of the default below.
4. Read `CONTRIBUTING.md` if it exists; surface any PR-style rules ("conventional commits required", "link issue in title", etc.).

### Phase 2 — Classify

Apply `wiki-changelog` to bucket commits into Features (🆕), Fixes (🐛), Refactor (🔄), Docs (📝), Config (🔧), Dependencies (📦), Breaking (⚠️). Merge related commits — one bullet per user-visible change, not one per commit.

### Phase 3 — Draft

Default body structure (override with project template if found):

```
## Summary
<2-3 sentences: what and why, not how>

## Changes
- <classified bullets, user-facing language>

## Related
<Closes / Refs links — use {input.issue_number} if set, otherwise infer from commit messages>

## Testing
<How the author validated; pull from commit messages and test files touched>

## Breaking changes
<Only if any; otherwise omit this section>
```

Title format: `<type>(<scope>): <imperative summary>` — match conventional-commit style if the branch already uses it; otherwise plain `<type>: <summary>`.

### Constraints

- Do **not** push, open the PR, or run `gh pr create` — only draft text. The user copies it.
- Do **not** invent test results or behavior the diff doesn't show. If you can't tell how it was tested, write "Testing: (author to fill in)".
- Highlight breaking changes prominently — even one bullet earns a `## Breaking changes` section.
- Keep the body under one screen for small PRs; expand only when the diff genuinely warrants it.
