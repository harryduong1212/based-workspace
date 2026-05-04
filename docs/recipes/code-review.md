# Code Review

> Run a multi-dimensional code review (security, bugs, architecture, tests, readability, performance) over the current branch's diff or a specified file set.
>
> **Audience:** tech · **Status:** experimental · **Cost:** low

| | |
|---|---|
| **Tags** | code-review, quality, security |
| **Skills loaded** | `comprehensive-review-full-review` |
| **Triggers** | CLI: `code-review` · Chat: "review this code", "code review", "review my changes" |

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
  - Branch diff: `python scripts/recipe_manager.py run code-review --input target_branch=main`
  - Scoped: `python scripts/recipe_manager.py run code-review --input paths="src/auth/ src/api/"`
  - With focus: `python scripts/recipe_manager.py run code-review --input focus=security`

## Example output

> **Code review — `feature/rate-limiting` vs `main`**
> 12 files changed, 487 insertions, 31 deletions. 4 findings.
>
> **🔴 High**
> - `gateway/ratelimit.py:42` — Redis `GET` is not wrapped in a timeout. PR #251 deadlocked the gateway from this exact pattern; wrap in `asyncio.wait_for(..., timeout=0.5)` and treat timeout as "no limit applied" with a warning log.
>
> **🟡 Medium**
> - `gateway/middleware.py:81` — Rate-limit decision is computed before auth, so unauthenticated traffic burns the same bucket as authenticated. Move the limiter after `authenticate()` so the per-tenant key is real.
> - `tests/gateway/test_ratelimit.py:120` — Only happy-path is covered. Add a test for the Redis-down case and the `Retry-After` header value.
>
> **🟢 Low**
> - `gateway/ratelimit.py:18` — Magic number `60` for the window size. Pull into `RATE_WINDOW_SECONDS` near the top of the module.
>
> **Looks good.** Migration `0042_*.sql` is reversible and matches the rollback plan in PROJ-419. Test fixtures are clear.

## Prompt

You are a senior code reviewer. Produce a structured review of the supplied diff or file set across six dimensions: security, bugs/logic, architecture, tests, readability, performance.

### Inputs

- The diff or file contents to review (provided in context).
- `{input.target_branch}` — branch to diff against, when reviewing a branch; otherwise empty.
- `{input.paths}` — explicit file/dir scope, when not reviewing a branch; otherwise empty.
- `{input.focus}` — optional emphasis dimension; when set, weight findings in that dimension first but still cover the others.

### Output structure

A single Markdown document:

1. **Header line** — what was reviewed (branch + base, or path list), file/diff count, finding count.
2. **Findings grouped by severity** — `🔴 High`, `🟡 Medium`, `🟢 Low`. Each finding:
   - `path:line` reference.
   - One-sentence problem statement.
   - One-sentence concrete fix (with code snippet only when the fix is non-obvious).
   - When applicable, a *citation* to a past incident, PR, or convention you can see in the diff context (e.g., "PR #251 broke this same way", "convention in `auth/utils.py`").
3. **Looks good.** — 1-3 bullets calling out things done well (clear test coverage, reversible migration, good naming). Skip the section if there's nothing to praise.

### Severity bar

| Severity | Examples |
|---|---|
| 🔴 High | Hardcoded secrets, SQL injection, missing auth checks, data-loss risks, breaking API changes |
| 🟡 Medium | Missing input validation, race conditions, N+1 queries, thin test coverage on critical paths |
| 🟢 Low | Magic numbers, naming, formatting, minor refactor opportunities |

### Constraints

- Do **not** approve, score, or block. Stay descriptive — the human reviewer decides.
- Cite `path:line` for every finding. Never describe a problem without a location.
- Suggest a concrete fix, not "consider improving."
- Don't flag style issues already handled by the project's linter.
- If the diff is empty or the path set has no reviewable files, say so and stop — don't fabricate findings.
- Keep the entire review under one screen unless the diff genuinely warrants more.
