---
description: Automatically group changes into logical features and generate conventional commits
---

# Auto-Feature Committer

I will analyze your working directory, group your unstaged and staged changes into discrete logical units, and automatically create conventional commits for each distinct feature, fix, or update.

## Guardrails
- NEVER use `git add .` or commit all changes as a single monolithic block if they represent different logical updates.
- Adhere strictly to the "One commit = one logical change" principle.
- Follow Conventional Commits format.
- Keep the subject line under 72 characters.
- Do not modify the code; only stage and commit existing changes.

## Steps

### 1. Scan the Workspace
First, understand the full scope of uncommitted work:
- Run `git status` to see all modified, deleted, and untracked files.
- Run `git diff` and `git diff --cached` to analyze the actual code changes.

### 2. Group Changes into Logical Units
Analyze the diffs and group related files together. For example, if there are updates to a REST controller, its corresponding service, and a database migration, group those as one "feature". If there is also an unrelated bump in `pom.xml` dependencies, separate that into a "chore".

### 3. Determine Commit Type & Scope per Group
For each logical group, select the appropriate type and scope:

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Build, tooling, dependencies |
| `ci` | CI/CD changes |

*Scope:* Identify the component (e.g., `api`, `auth`, `db`, `config`).

### 4. Formulate the Commit Strategy
Present a quick summary of the planned commits to the user before executing. 
Format:
1. `feat(auth): add JWT validation logic` (Files: `AuthController.java`, `TokenService.java`)
2. `chore(deps): update Hazelcast version` (Files: `pom.xml`)
3. `test(api): add unit tests for user endpoints` (Files: `UserControllerTest.java`)

### 5. Execute Iterative Staging and Committing
Once the strategy is clear (or explicitly approved by the user):
For each logical group:
1. Run `git add <specific-file-1> <specific-file-2>` to stage only the files for this specific group.
2. Generate the commit message using the format `<type>(<scope>): <description>`.
   - Use imperative mood ("add" not "added").
   - Don't capitalize the first letter.
   - No period at the end.
3. If the change is complex, include a body explaining WHAT and WHY, wrapping at 72 characters.
4. Run `git commit -m "<message>"` (or `-m` with body).
5. Repeat until all identified logical groups are committed.

## Principles
- Precision over speed: It is better to have 5 clean, distinct commits than 1 messy one.
- Reference issues when relevant (e.g., `fixes #123`) in the body.

## Reference
- [Conventional Commits](https://www.conventionalcommits.org/)
- Run `git log --oneline -10` to see recent commit style