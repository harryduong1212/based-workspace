---
description: Group staged changes into logical commits and draft Conventional Commits messages, ready to apply.
argument-hint: [--input scope=<value>] [--input split=<value>]
---

<!-- Generated from recipes/git-commit.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_claude_code.py`. -->

## What this does
Reads `git diff --staged`, classifies the changes, and drafts one or more Conventional Commits messages — with the exact `git commit` commands ready to run. Replaces the legacy `.archived/workflows/git-collaboration/git-commit.md` (Phase D2 migration).

## Who it's for
Engineers who want to stop hand-typing commit prefixes and stop debating between `feat` and `chore` for the third time today.

## What you need
- Staged changes (`git add` something first).

## How to run
- **In Antigravity or Claude Code:** stage your changes, then say *"draft a commit message"* or run `/git-commit`.
- **CLI:** `python scripts/recipe_manager.py run git-commit --input scope=auth`
- **Multi-commit split:** `python scripts/recipe_manager.py run git-commit --input split=true`

## Example output

> **Single commit drafted:**
>
> ```
> feat(auth): add OAuth2 PKCE flow for the SPA
>
> Replaces the implicit-grant flow with PKCE so the SPA stops shipping a
> client secret. Server-side OAuth callbacks are unchanged.
> ```
>
> Apply with:
> ```
> git commit -m "feat(auth): add OAuth2 PKCE flow for the SPA" -m "Replaces the implicit-grant flow with PKCE so the SPA stops shipping a client secret. Server-side OAuth callbacks are unchanged."
> ```

## Agent

You draft Conventional Commits messages from the user's staged changes. You do not run `git commit` yourself — only draft messages and the exact command to apply them.

### Phase 1 — Inspect

1. Run `git diff --staged --stat` for the file-change summary.
2. Run `git diff --staged` for the full diff. If the diff exceeds ~2000 lines, summarize per-file rather than reading the full content.
3. If nothing is staged, stop and tell the user to `git add` first. Do not draft anything.

### Phase 2 — Classify

Pick the most specific Conventional Commits type that fits:

| Type | When |
|---|---|
| `feat` | New user-visible behavior |
| `fix` | Bug fix |
| `perf` | Performance improvement with no behavior change |
| `refactor` | Code change that neither adds nor fixes |
| `test` | Adding or updating tests |
| `docs` | Documentation only |
| `chore` | Build, tooling, dependencies, generated files |
| `ci` | CI/CD config |
| `style` | Formatting only (rare — usually means lint config changed) |

Scope: use `{input.scope}` if set; otherwise infer from the deepest common path of the staged files (e.g., changes in `src/auth/*` → scope `auth`). No scope is fine when changes span unrelated areas.

### Phase 3 — Draft

**Subject line** — `<type>(<scope>): <imperative summary>`. Under 72 characters. Lowercase, no trailing period.

**Body (when non-trivial)** — 1-3 short paragraphs. WHAT and WHY, not HOW. Wrap at 72.

**Footer** — `Closes #N` / `Refs PROJ-X` only when the diff or staged content makes the issue clear. Don't invent.

### Phase 4 — Split (when `{input.split}` is true)

Look for unrelated buckets in the staged changes — different scopes, different concerns, mixed types. For each bucket:
1. Draft a separate Conventional Commits message.
2. Output the `git reset` + `git add <files>` + `git commit` sequence to apply that commit, in order.

If the staged changes are already a single coherent unit, say so and produce just one commit even when `split=true`.

### Constraints

- Do **not** run `git commit` yourself. Output the exact commands; the user runs them.
- Use imperative mood: "add" not "added", "fix" not "fixes".
- Don't reference internal task tracking ("addresses comment from Claude") — commit messages outlive sessions.
- If you can't tell what the change does from the diff (e.g., minified output, generated code), say so and ask the user for one sentence of context rather than guessing.
