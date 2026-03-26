---
name: n8n-global-deploy
description: Validates JSON output and pushes it to http://localhost:5678/api/v1/workflows
---

# n8n Global Deploy Skill

This skill allows the agent to validate JSON output and push it as a workflow to an n8n instance running at `http://localhost:5678/api/v1/workflows`.

- Always ensure the output matches the required n8n workflow format.
- Deploy automation directly to the endpoint defined.
