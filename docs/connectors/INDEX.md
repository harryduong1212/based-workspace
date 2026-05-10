# Connectors

**Connectors** are how recipes pull data from external systems — Jira, Bitbucket, GitHub, and so on.
Each connector has a one-time setup (an API token or app password); recipes declare which connectors they need.

See the [Connector Spec](../CONNECTOR_SPEC.md) for how connectors are written.

## Available connectors

| Connector | Description | Provides | Status |
|---|---|---|---|
| [Bitbucket](bitbucket.md) | Atlassian Bitbucket source code, pull requests, and reviews. | pull_requests, repositories, commits | experimental |
| [GitHub](github.md) | GitHub.com source code, pull requests, issues, and review queue. | pull_requests, issues, repositories, review_requests | experimental |
| [Gmail](gmail.md) | Google Mail mailbox access via IMAP for daily-briefing and inbox-aware recipes. | messages, threads, labels | experimental |
| [Jira](jira.md) | Atlassian Jira issue tracking and project management. | issues, projects, comments | experimental |
| [n8n Workflow Engine](n8n.md) | Integration with the n8n automation engine for executing workflow-based recipes. | workflows | experimental |
