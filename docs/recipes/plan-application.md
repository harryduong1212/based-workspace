# Plan a New Application

> Turn a raw application idea into a complete, reviewable design dossier — vision, architecture, core domain, tech stack, infrastructure, security, feature roadmap, test strategy, and ADRs — ready to hand off to the per-feature pipeline.
>
> **Audience:** tech · **Status:** experimental · **Cost:** low

| | |
|---|---|
| **Tags** | planning, architecture, design, application |
| **Skills loaded** | `application-blueprint` |
| **Triggers** | CLI: `plan-application` · Chat: "plan a new application", "design a new app" |

---

## What this does
Turns a raw application idea into a complete design dossier — ~10 app-level
artifacts generated in dependency order — ready to hand off to a per-feature
pipeline. Planning only: it designs, it does not build.

## Who it's for
Anyone starting a new application who wants the load-bearing decisions
(architecture, core domain, tech stack) made deliberately and written down
before any code exists — and wants those documents to stay maintainable as
the project evolves.

## What you need
- A `brief` — the raw application idea. That is the sole required input;
  the dossier is only as good as the brief plus any `constraints`.

## How to run
- **In Antigravity or Claude Code:** say *"plan a new application"* or run
  `/plan-application`. Checkpointed mode pauses for your approval between
  phases — this is where the interactive harness matters.
- **CLI (one-shot):**
  `python scripts/recipe_manager.py run plan-application --input mode=one-shot --input brief="a habit-tracking PWA"`

## Example output

> **docs/app-design/overview.md**
>
> <!-- plan-application:owned:start -->
> **What this is:** A habit-tracking PWA — offline-first, single-user.
> **Three decisions that matter:** (1) modular-monolith, not services;
> (2) local-first with IndexedDB + background sync; (3) TypeScript end to
> end.
>
> | Doc | Covers |
> |---|---|
> | architecture.md | System style, components, data flow |
> | feature-roadmap.md | 6 MVP features, prioritized |
> <!-- plan-application:owned:end -->
>
> ## Revision log
> - 2026-05-21: first draft

## Agent

You are running the `plan-application` recipe. The `application-blueprint`
skill owns the full methodology — the five-phase generation protocol, the
ten-artifact dossier, the per-artifact templates, the `mode` semantics, the
owned-section + ADR contracts, and the feature-roadmap handoff rule. Follow
it exactly. Do not restate it here.

Inputs bound for this run:

- `brief` = `{input.brief}` — the application idea to design from. If this
  is empty, stop with a clear error: there is nothing to design without it.
- `constraints` = `{input.constraints}` — bound the design by these when
  non-empty.
- `mode` = `{input.mode}` — apply the skill's `mode` semantics. Treat any
  value other than the literal `one-shot` as `checkpointed`.
- `out_dir` = `{input.out_dir}` — write the dossier here; default
  `docs/app-design/`.

Hard boundary: this recipe is **planning only**. Write nothing but the
dossier documents under `out_dir` — no code, no scaffold, no directory
tree, no config files, no git operations. Honor the owned-section and ADR
contracts; never clobber a pre-existing doc or rewrite an existing ADR.
