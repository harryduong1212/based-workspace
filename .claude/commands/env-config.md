---
description: Audit and tighten the project's environment-variable setup — .env hygiene, .env.example completeness, validation on startup, and CI/CD secret handling.
argument-hint: [--input focus=<value>]
---

<!-- Generated from recipes/env-config.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_claude_code.py`. -->

## What this does
Audits the current environment-variable setup — `.env` hygiene, `.env.example` completeness, runtime validation, CI/CD secret handling — and produces a fix list. Replaces the legacy `.archived/workflows/configuration/env-config.md` (Phase D2 migration).

## Who it's for
Engineers onboarding a project, security reviewers, anyone moving a service from "works on my machine" to "deployable."

## What you need
- A working checkout. The audit reads `.env*` files, `.gitignore`, framework config files, and CI workflow files.

## How to run
- **In Antigravity or Claude Code:** say *"audit env config"* or run `/env-config`.
- **CLI:** `python scripts/recipe_manager.py run env-config --input focus=secrets`

## Example output

> **Env config audit — `auth-service`**
>
> **🔴 .env hygiene**
> - `.env` is tracked in git. Add to `.gitignore` and rotate any key that's been pushed.
>
> **🟡 Documentation**
> - `JWT_SECRET` is read in `auth/middleware.py:42` but missing from `.env.example`.
> - `REDIS_TLS_CERT_PATH` is in `.env.example` but no longer referenced in code (dead).
>
> **🟢 Validation**
> - `config.py:18` validates required vars on startup — good.
>
> **🔴 CI/CD**
> - `.github/workflows/deploy.yml:34` echoes `$DATABASE_URL` to logs. Mask it (`::add-mask::`) or pass via secret context only.

## Agent

You audit a project's environment-variable configuration. Output is a Markdown report grouped into four areas. Be concrete — every finding cites a file:line.

### Phase 1 — Discover

1. List files: `.env`, `.env.local`, `.env.production`, `.env.example`, `.env.sample`. Note which exist.
2. Read `.gitignore`. Confirm `.env*` (or equivalents) are ignored.
3. Find every variable read in code: grep for `process.env.`, `os.environ`, `os.getenv`, `Deno.env.get`, `Bun.env.`, etc., across the project. Build a set of *referenced* names.
4. Find every variable declared in `.env*` files. Build a set of *declared* names.
5. Read framework config / settings files (`pyproject.toml`, `package.json` scripts, `config.py`, `settings.py`, `next.config.js`, etc.) to find startup validation hooks.
6. Read CI workflow files (`.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, etc.).

### Phase 2 — Audit (skip an area when `{input.focus}` is set and excludes it)

| Area | Check |
|---|---|
| **.env hygiene** | `.env*` files in `.gitignore`. No real secrets in `.env.example`. No tracked `.env` in git history (use `git log -- .env` to check). |
| **Documentation** | Every code-referenced variable appears in `.env.example` with a placeholder. Every `.env.example` variable is still referenced somewhere in code (otherwise it's dead). |
| **Validation** | Required variables are validated at startup. Missing values produce a clear, fail-fast error — not a runtime KeyError 30 minutes in. |
| **CI/CD** | Secrets come from the CI's secret store, not committed files. No `echo $SECRET` patterns. Different values per environment when applicable. |

### Phase 3 — Report

Group findings by area. Use severity emoji: 🔴 (must fix — leaked secret, no validation), 🟡 (should fix — drift, missing docs), 🟢 (looks good — call out positively when an area is clean).

### Constraints

- Do **not** print secret values from `.env` files. Reference variable names only.
- Do **not** modify any file. Recommend changes; the user applies them.
- If a project doesn't use a particular pattern (e.g., no CI yet), say so and skip that area cleanly — don't fabricate findings.
