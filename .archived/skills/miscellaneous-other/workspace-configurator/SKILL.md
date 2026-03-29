---
name: workspace-configurator
description: Invisible orchestrator that configures the active workspace context based on the user's natural language intent.
---

# Workspace Configurator

## Purpose

You are the context router for this workspace. When a user begins a new task, shifts domains, or explicitly requests tools, you silently determine which skills should be active and load them via the workspace manager script. You are the **only** mechanism the agent may use to change the active skill surface.

## Trigger Conditions

Activate this skill when **any** of the following are true:

1. The user assigns a **new high-level objective** (e.g. "Let's build a REST API in Java", "Help me create an n8n workflow").
2. The user **shifts the project domain** (e.g. from frontend work to database optimization).
3. The user **explicitly asks** for tools, skills, or capabilities (e.g. "Load the Java tools", "I need PostgreSQL skills").
4. The currently loaded skills are **clearly mismatched** for the conversation context.

**Do NOT activate** for minor follow-ups within an already well-matched context.

## Action Plan

### Step 1 — Identify the Domain

Read the top-level skill registry at `.archived/skills/registry.json`. Match the user's intent against the `domain_tags` arrays to identify 1–2 relevant category IDs.

### Step 2 — Select Skills

Read the specific category's `registry.json` (at the path listed in the top-level registry). Scan the `tags`, `description`, and `id` fields of every skill in that category. Select **2–4** highly relevant skill IDs that best serve the user's task.

**Selection criteria (in order of priority):**
1. Direct match on skill `id` or `tags` to the user's request.
2. Complementary coverage (e.g. a language skill + a framework skill + a database skill).
3. Avoid loading more than 4 skills — context overload degrades quality.

### Step 3 — Execute the Loader

Run exactly this terminal command:

```
python scripts/workspace_manager.py --skills "<id1>,<id2>,<id3>"
```

Replace `<id1>,<id2>,<id3>` with the comma-separated skill IDs from Step 2.

### Step 4 — Confirm Silently

After execution, briefly note which skills were loaded in your response (one line is sufficient). Do not dump the full registry contents.

## Strict Constraints

> [!CAUTION]
> **NEVER** manipulate symlinks, copy files, or modify anything inside `.agents/` directly.
> The workspace manager script is the **exclusive** interface for loading context.
> Violating this constraint will corrupt the workspace state.

- You must ONLY load context by executing `python scripts/workspace_manager.py`.
- Never hard-code skill paths — always look them up via the registry files.
- Never remove the `workspace-configurator` directory from `.agents/skills/`.
- If a requested skill ID cannot be found, inform the user and suggest alternatives from the registry.

## Quick Reference — Profile Shorthand

If the user mentions a role by name, check `scripts/profiles.json` for a matching profile and use `--profile` instead:

```
python scripts/workspace_manager.py --profile java-backend-dev
```

Available profiles are listed in `scripts/profiles.json`.
