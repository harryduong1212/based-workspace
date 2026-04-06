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
3. The user **explicitly asks** for tools, skills, profiles, or capabilities (e.g. "Load the Java tools", "Switch to the writer profile").
4. The currently loaded skills are **clearly mismatched** for the conversation context.

**Do NOT activate** for minor follow-ups within an already well-matched context.

## Action Plan

### Step 1 — Profile Matching (Priority Route)
Before searching for individual skills, you must check if the user's request aligns with an established workspace profile.
1. Read the `scripts/profiles.json` file.
2. If the user explicitly mentions a profile name, or if their requested role strongly matches a profile key (e.g., `ai-ultimate`, `base-core`), execute the following command:
   `python scripts/workspace_manager.py --profile <profile_name>`
3. **If a profile is executed, skip directly to Step 5.** If no profile matches, proceed to Step 2.

### Step 2 — Identify the Domain (Skill Route)
Read the top-level skill registry at `.archived/skills/registry.json`. Match the user's intent against the `domain_tags` arrays to identify 1–2 relevant category IDs.

### Step 3 — Select Skills
Read the specific category's `registry.json` (at the path listed in the top-level registry). Scan the `tags`, `description`, and `id` fields of every skill in that category. Select **2–4** highly relevant skill IDs that best serve the user's task.

**Selection criteria (in order of priority):**
1. Direct match on skill `id` or `tags` to the user's request.
2. Complementary coverage (e.g. a language skill + a framework skill + a database skill).
3. Avoid loading more than 4 skills — context overload degrades quality.

### Step 4 — Execute the Skill Loader
Run exactly this terminal command:

```bash
python scripts/workspace_manager.py --clear --skills "<id1>,<id2>,<id3>"