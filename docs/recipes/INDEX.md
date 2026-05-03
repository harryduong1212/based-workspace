# Recipes

A **recipe** is a self-contained task you can run from chat, the CLI, or on a schedule.
Each one wraps an AI prompt, an n8n workflow, or an agent — but you don't need to know which.
Pick the recipe whose description matches what you want done.

## How to run a recipe

- **In Antigravity or Claude** — say one of the recipe's chat triggers (e.g., *"morning briefing"*).
- **From the terminal** — `python scripts/recipe_manager.py run <id>`
- **On a schedule** — recipes with a `schedule:` trigger run automatically once n8n is wired up.

See the [Recipe Spec](../RECIPE_SPEC.md) for how recipes are written.

## For everyone

| Recipe | Description | Status | Tags |
|---|---|---|---|
| [Daily Briefing](daily-briefing.md) | Morning summary of your Jira tickets and Bitbucket PRs. | experimental | briefing, jira, bitbucket, daily |

## For non-technical users

*(none yet)*

## For technical users

*(none yet)*
