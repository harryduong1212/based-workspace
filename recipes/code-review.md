---
id: code-review
name: Code Review
description: Run a multi-dimensional code review (security, bugs, architecture, tests, readability, performance) over the current branch's diff or a specified file set.
audience: tech
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [code-review, quality, security]

about: >-
  Reviews the current branch's diff (or a scoped path set) along six axes —
  security, bugs, architecture, tests, readability, and performance — and
  returns severity-tagged findings with `file:line` citations and concrete
  fix suggestions. Local execution (no external API). Pair with the
  `comprehensive-review-full-review` skill to get the structured output
  schema the recipe targets. Advanced: pass `focus` to tilt weight toward
  one dimension; pass `--input-file diff=...` to review a saved patch
  instead of the live branch.
highlights:
  - Six review axes — finds beyond just "does it work?"
  - Severity-tagged output with file:line citations
  - Scope-flexible — branch diff, path set, or pre-saved patch
  - Provider-neutral; runs against your default dispatcher model
examples:
  - label: Review current branch vs main
    code: "claude /code-review"
  - label: Review a saved patch from CI
    code: "claude /code-review --input-file diff=/tmp/ci.patch"
  - label: Security-focused pass
    code: "claude /code-review focus=security"

requires_skills:
  - comprehensive-review-full-review
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env: []

triggers:
  cli: code-review
  chat:
    - "review this code"
    - "code review"
    - "review my changes"

inputs:
  - name: target_branch
    type: string
    required: false
    description: Branch to diff against. Defaults to `main`. Mutually exclusive with `paths`.
  - name: paths
    type: string
    required: false
    description: Space- or comma-separated file/directory paths to scope the review. Used when not reviewing branch diff.
  - name: focus
    type: string
    required: false
    description: Optional emphasis (e.g., "security", "performance", "tests"). When omitted, all dimensions are weighted equally.
  - name: diff
    type: string
    required: false
    description: Raw diff or file contents to review, inlined into the prompt. Typically supplied via `--input-file diff=<path>` (e.g., `git diff main..HEAD > /tmp/d.patch`). When empty, the recipe assumes a harness has the diff in context.

outputs:
  - name: review
    type: markdown
    description: Findings list grouped by severity, with file:line citations and concrete fix suggestions.

execution:
  type: prompt
---

## What this does
Reviews the diff on the current branch (or a specified file set) across six dimensions — security, bugs, architecture, tests, readability, performance — and returns findings ranked by severity with concrete fix suggestions. Replaces the legacy `.archived/workflows/testing-quality/code-review.md` (Phase D2 migration).

## Who it's for
Engineers who want a structured second-pass on changes before opening a PR, and reviewers who want a thorough first read of a branch they didn't write. Not a replacement for human review — flags candidates, doesn't approve.

## What you need
- A working git checkout, or a set of files to review.
- (Optional) Project linting config (`.eslintrc`, `pyproject.toml`, etc.) — the review will respect existing conventions when it can detect them.

## How to run
- **In Antigravity or Claude Code:** say *"review my changes"* or run the `/code-review` slash command.
- **CLI:**
  - Branch diff: `git diff main..HEAD > /tmp/d.patch && python scripts/recipe_manager.py run code-review --input target_branch=main --input-file diff=/tmp/d.patch`
  - Scoped: `python scripts/recipe_manager.py run code-review --input paths="src/auth/ src/api/" --input-file diff=/tmp/d.patch`
  - With focus: `python scripts/recipe_manager.py run code-review --input focus=security --input-file diff=/tmp/d.patch`
  - Stdin: `git diff main..HEAD | python scripts/recipe_manager.py run code-review --input-file diff=-`

## Example output

> **Code review — `feature/rate-limiting` vs `main`**
> 12 files changed, 487 insertions, 31 deletions. 4 findings.
>
> ### P0 — Must fix before merge
> - `gateway/ratelimit.py:42` — Redis `GET` is not wrapped in a timeout. PR #251 deadlocked the gateway from this exact pattern; wrap in `asyncio.wait_for(..., timeout=0.5)` and treat timeout as "no limit applied" with a warning log.
>
> ### P1 — Fix before next release
> - `gateway/middleware.py:81` — Rate-limit decision is computed before auth, so unauthenticated traffic burns the same bucket as authenticated. Move the limiter after `authenticate()` so the per-tenant key is real.
> - `tests/gateway/test_ratelimit.py:120` — Only happy-path is covered. Add a test for the Redis-down case and the `Retry-After` header value.
>
> ### P3 — Track in backlog
> - `gateway/ratelimit.py:18` — Magic number `60` for the window size. Pull into `RATE_WINDOW_SECONDS` near the top of the module.
>
> **Looks good.** Migration `0042_*.sql` is reversible and matches the rollback plan in PROJ-419. Test fixtures are clear.

## Prompt

You are a senior code reviewer. Produce a structured review of the supplied diff or file set across six dimensions: security, bugs/logic, architecture, tests, readability, performance.

### Inputs

- `{input.target_branch}` — branch to diff against, when reviewing a branch; otherwise empty.
- `{input.paths}` — explicit file/dir scope, when not reviewing a branch; otherwise empty.
- `{input.focus}` — optional emphasis dimension; when set, weight findings in that dimension first but still cover the others.

### Diff or file contents to review

```
{input.diff}
```

If the block above is empty, your harness should have the diff in context already; otherwise treat the block as the authoritative input and ignore claims about other files.

### Header line

Open the report with one line summarizing what was reviewed: branch + base when reviewing a branch, otherwise the path list, plus file count and finding count.

### Constraints

- Do **not** approve, score, or block. Stay descriptive — the human reviewer decides.
- Don't flag style issues already handled by the project's linter.
- If the diff is empty or the path set has no reviewable files, say so and stop — don't fabricate findings.
- Keep the entire review under one screen unless the diff genuinely warrants more.
- Close with a short **Looks good.** section (1-3 bullets) when there's something genuinely worth calling out; skip otherwise.
