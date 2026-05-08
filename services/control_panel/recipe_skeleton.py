"""Templated recipe skeletons for the Create flow.

A new recipe gets a hand-shaped body with TODO markers per section so the
audit doesn't fail on day one and the user has clear places to fill in.
"""
from __future__ import annotations

import yaml


SUPPORTED_EXECUTION_TYPES = ("prompt", "agent", "workflow")


def build_skeleton(
    *,
    recipe_id: str,
    name: str,
    description: str,
    audience: str,
    tags: list[str],
    execution_type: str,
) -> str:
    if execution_type not in SUPPORTED_EXECUTION_TYPES:
        raise ValueError(f"unsupported execution type: {execution_type!r}")

    fm = {
        "id": recipe_id,
        "name": name,
        "description": description,
        "audience": audience,
        "version": "0.1.0",
        "status": "experimental",
        "cost": "low",
        "requires_human_review": False,
        "tags": list(tags),
        "requires_skills": [],
        "requires_workflows": [],
        "requires_connectors": [],
        "requires_mcp": [],
        "requires_env": [],
        "triggers": {"cli": recipe_id},
        "inputs": [],
        "outputs": [
            {"name": "result", "type": "markdown", "description": "TODO: describe the recipe's output."}
        ],
        "execution": {"type": execution_type},
    }
    fm_yaml = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).rstrip("\n")
    body = _BODY_TEMPLATES[execution_type].format(id=recipe_id)
    return f"---\n{fm_yaml}\n---\n\n{body}\n"


_PROMPT_BODY = """## What this does
TODO: 2–3 sentences on what this recipe produces and the moment it's useful.

## Who it's for
TODO: identify the typical user.

## What you need
- TODO: prerequisites (env vars, connectors, services running).

## How to run
- **In Antigravity / Claude Code:** _trigger phrase or slash command_
- **CLI:** `python scripts/recipe_manager.py run {id}`

## Example output
> TODO: a short illustrative example.

## Prompt

You are a TODO. Produce a TODO.

### Inputs

TODO: list the inputs the prompt expects (matches the `inputs:` block in frontmatter).

### Constraints

- TODO
"""

_AGENT_BODY = """## What this does
TODO: describe the agent's goal and the boundary of its autonomy.

## Who it's for
TODO

## What you need
- TODO: skills, MCP servers, and environment this agent depends on.

## How to run
- **CLI:** `python scripts/recipe_manager.py run {id}`

## Agent

You are a TODO operating in a loop. On each step:

1. TODO: describe one observation.
2. TODO: describe one action.
3. Stop when TODO.

### Tools available

TODO: list the tools / skills / MCP this agent can use, and when each is appropriate.

### Stopping criteria

- TODO
"""

_WORKFLOW_BODY = """## What this does
TODO: describe the workflow this recipe orchestrates (n8n / external).

## Who it's for
TODO

## What you need
- TODO: env vars, n8n credentials, webhook URLs.

## How to run
- **CLI:** `python scripts/recipe_manager.py run {id}`

## Workflow

The workflow lives in `n8n-workflows/{id}.n8n`. Inputs are POSTed to the
trigger webhook; outputs are returned synchronously when the workflow
finishes.
"""


_BODY_TEMPLATES = {
    "prompt": _PROMPT_BODY,
    "agent": _AGENT_BODY,
    "workflow": _WORKFLOW_BODY,
}
