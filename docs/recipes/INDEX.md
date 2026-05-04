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

| Recipe | Description | Status | Tags |
|---|---|---|---|
| [PR Review Prep](pr-review-prep.md) | Generate a structured review brief for a Bitbucket pull request, with the linked ticket context and past reviewer feedback already pulled in. | experimental | bitbucket, jira, code-review, pr |
| [Ticket to Feature](ticket-to-feature.md) | Turn a Jira ticket into a feature spec, API sketch, and open-questions list using related context from past tickets and PRs. | experimental | jira, bitbucket, feature-kickoff, planning |
