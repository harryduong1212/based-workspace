---
id: plan-application
name: Plan a New Application
description: >-
  Turn a raw application idea into a complete, reviewable design dossier —
  vision, architecture, core domain, tech stack, infrastructure, security,
  feature roadmap, test strategy, and ADRs — ready to hand off to the
  per-feature pipeline.
audience: tech
version: 0.1.0
status: experimental
cost: low
requires_human_review: false
tags: [planning, architecture, design, application]

about: >-
  The application tier above a per-feature pipeline. From a raw brief it
  produces a ~10-artifact design dossier — vision, architecture,
  core-domain, tech-stack, infrastructure, security, feature-roadmap,
  test-strategy, ADRs, overview — generated in dependency order so the
  architecture is settled before everything that leans on it. Planning
  only: no code, no scaffold. Ends by handing each MVP feature off to the
  feature pipeline. checkpointed mode pauses for approval between phases;
  one-shot runs straight through. Re-runs update under an owned-section
  contract and never clobber human notes.
highlights:
  - Ten app-level design artifacts from a single brief
  - Dependency-ordered — architecture settled before dependent docs
  - checkpointed (default) or one-shot generation
  - Owned-section contract — re-runs update cleanly, ADRs append-only
examples:
  - label: Checkpointed plan from a brief
    code: "claude /plan-application"
  - label: One-shot with constraints
    code: "python scripts/recipe_manager.py run plan-application --input mode=one-shot --input brief='a habit-tracking PWA' --input constraints='solo dev, TypeScript, ship in 6 weeks'"

requires_skills:
  - application-blueprint
requires_workflows: []
requires_connectors: []
requires_mcp: []
requires_env: []

triggers:
  cli: plan-application
  chat:
    - "plan a new application"
    - "design a new app"

inputs:
  - name: brief
    type: string
    required: true
    description: The raw application idea / problem statement to design from.
  - name: constraints
    type: string
    required: false
    description: >-
      Tech preferences, team size, timeline, scale, compliance — anything
      that should bound the design.
  - name: mode
    type: string
    required: false
    description: >-
      "checkpointed" (default) or "one-shot". checkpointed pauses for
      approval between phases; one-shot generates all artifacts in one pass.
      Any value other than "one-shot" is treated as checkpointed.
  - name: out_dir
    type: string
    required: false
    description: Output directory for the dossier. Defaults to docs/app-design/.

outputs:
  - name: dossier
    type: markdown
    description: >-
      The ~10-artifact design dossier under out_dir (vision, architecture,
      core-domain, tech-stack, infrastructure, security, feature-roadmap,
      test-strategy, adr/, overview).

execution:
  type: agent
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
