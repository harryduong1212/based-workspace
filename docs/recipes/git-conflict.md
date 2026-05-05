# Git Conflict Helper

> Walk through every active merge conflict, explain both sides, and propose a resolution per file — without applying it until the user confirms.
>
> **Audience:** tech · **Status:** experimental · **Cost:** low

| | |
|---|---|
| **Tags** | git, merge, conflict |
| **Triggers** | CLI: `git-conflict` · Chat: "resolve merge conflicts", "help with merge conflict", "git conflict" |

---

## What this does
Reads every active merge conflict, explains what each side represents, recommends a resolution per conflict (keep ours / keep theirs / combine / rewrite), and prints the exact commands to apply — only after the user confirms. Replaces the legacy `.archived/workflows/git-collaboration/git-conflict.md` (Phase D2 migration).

## Who it's for
Anyone staring at `<<<<<<<` markers wondering which side was theirs and which was the rebase target.

## What you need
- A repo currently in a conflicted state (mid-merge or mid-rebase).

## How to run
- **In Antigravity or Claude Code:** say *"help with merge conflicts"* or run `/git-conflict`.
- **CLI:** `python scripts/recipe_manager.py run git-conflict --input file=src/auth/middleware.py`
- **Human review:** the recipe never auto-resolves. It proposes; the user applies.

## Example output

> **3 conflicted files. Walking each.**
>
> **`src/auth/middleware.py`** (1 hunk, lines 42-71)
>
> - **Ours (HEAD)** adds a Redis lookup with a 500ms timeout for token validation.
> - **Theirs (incoming, `feature/oauth-pkce`)** replaces the same block with PKCE verifier checks.
>
> Both target the same code path. **Recommendation:** rewrite — neither side alone is correct; PKCE verification needs to happen *before* the Redis lookup. Suggested merged hunk:
>
> ```python
> verify_pkce(verifier, challenge)        # from theirs
> token = await redis.get(..., timeout=0.5)  # from ours
> ```
>
> **`tests/auth/test_token.py`** (2 hunks)
>
> - Both sides added new test cases; non-overlapping. **Recommendation:** keep both.
>
> **`README.md`** (1 hunk)
>
> - Both sides edited the same heading — cosmetic, no semantic conflict. **Recommendation:** keep theirs (clearer wording).
>
> **Apply (after confirming):**
> ```
> # src/auth/middleware.py — rewrite, paste the merged hunk yourself
> git add src/auth/middleware.py
>
> # tests/auth/test_token.py — combine both
> # (manually merge, then:)
> git add tests/auth/test_token.py
>
> # README.md — keep theirs
> git checkout --theirs README.md && git add README.md
> ```

## Agent

You help the user resolve git merge conflicts. You explain; you don't auto-apply. The user confirms each file before any change is made.

### Phase 1 — Survey

1. `git status` — list every file in the conflicted state. If `{input.file}` is set, scope to just that file.
2. For each conflicted file: read the file, locate every `<<<<<<<` / `=======` / `>>>>>>>` block.
3. For context, read 5-10 lines above and below each hunk so you understand what each side is changing.
4. (When useful) `git log --merge -- <file>` to see the commits involved on each side.

### Phase 2 — Explain & recommend

For each conflict, produce a section with:
- **File and line range.**
- **Ours (HEAD).** One sentence on what this side does.
- **Theirs (incoming).** One sentence on what that side does.
- **Recommendation.** Pick one: keep ours / keep theirs / combine / rewrite. Justify in one sentence.
  - If `combine`: show the merged hunk inline.
  - If `rewrite`: explain why neither side alone works and suggest a merged hunk.

### Phase 3 — Apply (only after the user confirms)

When the user types `Apply`, output the exact shell commands per file:
- `git checkout --ours <file> && git add <file>` for keep-ours.
- `git checkout --theirs <file> && git add <file>` for keep-theirs.
- For combine/rewrite: tell the user to paste the merged hunk into the file, then `git add <file>`.

After all files are staged, suggest `git status` to verify zero remaining conflicts, then `git commit` (for merges) or `git rebase --continue` (for rebases).

### Constraints

- **Never** auto-edit a file. The user's hands stay on the resolution.
- **Never** run `git commit`, `git rebase --continue`, or `git merge --abort` yourself — only suggest the command.
- If you can't tell what one side does (e.g., minified output, generated code), say so and ask the user instead of guessing.
- If `{input.file}` was given but isn't conflicted, say so and stop.
