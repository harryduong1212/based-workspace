# Smoke Echo

> End-to-end smoke test for the workflow-dispatch path. Webhook → callback round-trip with no external creds.

<!-- Generated from recipes/smoke-echo.md. Do not edit directly — edit the source recipe and re-run `python scripts/sync_antigravity.py`. -->

## How to invoke

- CLI: `python scripts/recipe_manager.py run smoke-echo`
- Chat: "smoke echo", "test workflow dispatch"

---

## What this does
Validates the dispatcher → n8n webhook → callback path end-to-end. No external service required.

## Why it exists
A failure here means the workflow execution model itself is broken before any real recipe (daily-briefing, etc.) can run. Use this any time the n8n integration changes (image upgrade, encryption key rotation, host port shift) to verify the loop still works.
