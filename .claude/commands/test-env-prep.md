---
description: Scaffold a test environment for a feature — mock data fixtures, environment-config docs, and empty test files matching the framework already in use.
argument-hint: --input feature=<value> [--input spec_path=<value>]
---

<!-- Generated from recipes/test-env-prep.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_claude_code.py`. -->

## What this does
Detects the project's existing test framework and writes a starter set of mock fixtures, an env-setup guide, and empty test files (with TODO bodies) matching that framework. Replaces the legacy `.archived/workflows/custom-workflows/prepare-test-environment.md` (Phase D2 migration).

## Who it's for
Engineers starting a feature who want test scaffolding committed before writing implementation code, so the test surface is shaped by the spec — not by what was easy to test after the fact.

## What you need
- A working checkout of the target project.
- (Optional) An SRS, API spec, or ticket export at `{input.spec_path}` to drive fixture shape and test naming.

## How to run
- **In Antigravity or Claude Code:** say *"prepare test environment for auth/oauth-pkce"* or run `/test-env-prep`.
- **CLI:** `python scripts/recipe_manager.py run test-env-prep --input feature=auth/oauth-pkce --input spec_path=.docs/specs/PROJ-412_srs.md`
- **Human review:** runner pauses before writing files; review the plan, then approve.

## Example output

> **Test scaffold for `auth/oauth-pkce`**
>
> Detected: pytest, factory_boy, pytest-asyncio.
>
> Created:
> - `tests/auth/test_oauth_pkce.py` — 6 empty test functions covering happy path, expired code, replay attempt, mismatched verifier, missing PKCE params, and JWKS rotation.
> - `tests/auth/fixtures/oauth_clients.json` — 3 client records (web SPA, mobile, server-to-server).
> - `tests/auth/fixtures/jwks.json` — 2 keys with realistic kid/kty.
> - `.docs/tests/oauth_pkce_setup.md` — env vars, mock OAuth provider, how to run the suite.
>
> **Next:** fill the `# TODO` bodies as implementation lands.

## Agent

You scaffold the test surface for a feature. Your output is files written to disk plus a one-page test plan. You do not implement the feature itself.

### Phase 1 — Detect

1. Identify the test framework already in use:
   - JS/TS: look for `vitest`, `jest`, `playwright` in `package.json`.
   - Python: look for `pytest` (`pyproject.toml`, `pytest.ini`, `setup.cfg`).
   - Go: standard `testing` package; check `go.mod`.
   - Other: Ruby/RSpec, Rust/cargo test, etc.
2. Identify mock-data conventions in the existing test suite:
   - Fixture format (JSON, YAML, factory functions).
   - Where fixtures live (`tests/fixtures/`, `__fixtures__/`, framework-specific paths).
3. Read `{input.spec_path}` if set. Otherwise, infer scope from `{input.feature}` and any SRS/API doc in `.docs/`.

### Phase 2 — Plan

Draft a Markdown plan covering:
1. **Test list** — function/test names matching detected framework conventions, one per acceptance criterion or API endpoint. Cover happy path, error paths, and 1-2 edge cases.
2. **Fixtures** — entities the tests will need; where each fixture file goes; one realistic record per shape.
3. **Environment** — env vars, containers, mock external services, anything needed to run the suite locally.
4. **File list** — exact paths the recipe will write.

Pause and present the plan. Wait for the user to type `Approve`, `Edit`, or `Reject` before writing any file.

### Phase 3 — Scaffold

After approval:
1. Write fixture files with realistic synthetic data — never real production data, never real PII patterns. Use `Faker`-style values.
2. Write empty test files. Each test function has a clear name and a `# TODO: <one-line intent>` body — no asserts that will pass vacuously.
3. Write `.docs/tests/<feature_slug>_setup.md` (where `<feature_slug>` is the slugified form of `{input.feature}` — e.g., `auth/oauth-pkce` → `auth_oauth_pkce`) with the env-setup recipe.
4. Output the final file list, line counts, and a "Next" line pointing at the first TODO to fill.

### Constraints

- **Synthetic data only.** No real names, emails, IDs from the production codebase or real users.
- **Match detected conventions.** Don't introduce a new test framework or fixture style if the project already has one.
- **Empty bodies, not vacuous passes.** A `pass` is fine; an `assert True` is not — it implies coverage that doesn't exist.
- **No implementation code.** Scaffold only.
