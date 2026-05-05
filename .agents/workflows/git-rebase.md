# Git Rebase Plan

> Plan an interactive rebase — propose the pick/squash/reword/drop sequence and the exact commands, with a backup branch first.

<!-- Generated from recipes/git-rebase.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_antigravity.py`. -->

## How to invoke

- CLI: `python scripts/recipe_manager.py run git-rebase`
- Chat: "plan a rebase", "clean up commit history", "git rebase"

---

## What this does
Reads the branch's commit history, asks what you want to clean up, and produces the exact `git rebase -i` plan with a `pick/squash/reword/drop` action per commit and the wrapper commands (backup branch, rebase, force-push warning). Replaces the legacy `.archived/workflows/git-collaboration/git-rebase.md` (Phase D2 migration).

## Who it's for
Anyone with a messy "WIP / WIP / fix typo / actual feature" branch about to open a PR.

## What you need
- A branch with commits ahead of the base. Ideally not yet pushed (or the user understands the force-push implication).

## How to run
- **In Antigravity or Claude Code:** say *"plan a rebase"* or run `/git-rebase`.
- **CLI:** `python scripts/recipe_manager.py run git-rebase --input goal="squash the 4 WIP commits, reword the feat commit"`
- **Human review:** the recipe never starts the rebase itself. It produces a plan; the user runs it.

## Example output

> **Rebase plan — `feature/oauth-pkce` onto `main`**
>
> 7 commits ahead of `main`. Branch is **not yet pushed** — safe to rebase without coordination.
>
> **Proposed todo-list:**
> ```
> pick   a1b2c3d feat(auth): add OAuth2 PKCE flow for the SPA
> squash 4e5f6g7 wip
> squash 8h9i0j1 wip — try cookie path
> squash 2k3l4m5 fix typo in README
> reword 6n7o8p9 docs(auth): update README with PKCE setup
> pick   abc1234 test(auth): cover replay-attempt path
> drop   def5678 experiment: rotate JWKS on every request
> ```
>
> **Apply (after reviewing):**
> ```
> git switch -c feature/oauth-pkce-backup-2026-05-04   # backup
> git switch feature/oauth-pkce
> GIT_SEQUENCE_EDITOR=':' git rebase -i main           # opens with the todo above pre-set
> # ... resolve any conflicts as they appear ...
> git log --oneline main..HEAD                         # verify
> ```
>
> **If anything goes wrong:** `git rebase --abort`, then `git switch feature/oauth-pkce-backup-2026-05-04` to recover.

## Agent

You plan an interactive rebase. You don't run it.

### Phase 1 — Survey

1. Resolve the base:
   - If `{input.base}` is set, use it.
   - Otherwise, prefer `main`, then `master`, then `develop` — the first that exists.
2. Run:
   - `git log --oneline <base>..HEAD` — the commit list to rebase.
   - `git status` — confirm working tree clean. If dirty, stop and tell the user to commit or stash first.
   - `git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null` — has the branch been pushed? If yes, flag the force-push consequence.
3. Read the user's goal from `{input.goal}` if set; otherwise ask.

### Phase 2 — Plan

Output a Markdown report:

1. **Header.** Branch name, base, commit count, push status (with force-push warning when applicable).
2. **Proposed todo-list.** One line per commit with the action (`pick`, `squash`, `fixup`, `reword`, `edit`, `drop`) and the existing subject. Ordered as the rebase will see them (oldest first).
3. **Rationale.** One short sentence per non-`pick` action explaining why.
4. **Apply commands.** Exact shell sequence: backup branch (`git switch -c <branch>-backup-<date>`), then `git rebase -i <base>` — note: when the user is OK with the proposed todo-list as-is, suggest `GIT_SEQUENCE_EDITOR=':' git rebase -i <base>` so the editor doesn't open. Otherwise, plain `git rebase -i <base>` and they'll edit interactively.
5. **Recovery.** `git rebase --abort` mid-rebase, or `git reset --hard <backup-branch>` if already finished and unhappy.

### Constraints

- **Always** propose the backup branch first. Use today's date in the suffix.
- **Never** run the rebase yourself. Output commands only.
- If the branch has been pushed and shared with others, lead with the consequence: a force-push will rewrite history that collaborators may have already pulled.
- Don't `drop` a commit unless the user's goal explicitly says so. When unclear, propose `pick` and call out the candidate for the user to confirm.
- Keep the todo-list grouped logically: squash WIPs together near the commit they belong to; rewords near the keepers.
