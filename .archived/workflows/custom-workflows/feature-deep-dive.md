---
description: Generates a standardized architecture deep-dive document to deconstruct a specific feature's codebase.
---

# 🏗️ Architecture Deep-Dive & Feature Deconstruction

You are the Orchestrator coordinating specialized architectural AI agents to analyze and break down a specific feature within the codebase.

## Required Skills

| Agent | Role |
| :--- | :--- |
| **`@custom-senior-architect`** | Maps end-to-end technical flows and identifies system components. |
| **`@workspace-analyzer`** | Conducts deep repository scans to identify the critical path and technical debt. |

## Guardrails

- **Complete Traceability**: Never skip error handling or alternative logic paths during deconstruction.
- **Side-Effect Identification**: Explicitly look for cross-component side effects (e.g., shared state, event triggers).
- **Read-Only Mode**: Do not modify any code; the goal is pure architectural understanding.

## Execution Flow

### Step 1: Initialization & Scoping
... (rest of the steps) ...

## 📄 Artifact Template: Feature Deep-Dive

When Step 5 is reached, use the following structure for the final document at `.docs/architecture/[feature_name]_deep_dive.md`:

```markdown
# Architecture Deep-Dive: [Feature Name]

## 1. Executive Summary
[High-level overview of the feature's purpose and impact]

## 2. Scoped File Structure
[Annotated directory tree from Step 2]

## 3. Logical Component Breakdown
[Table of components, responsibilities, and deep-dive prompts from Step 3]

## 4. Execution Sequence
[Textual sequence diagram from Step 4]

## 5. Architectural Insights
### Challenges & Trade-offs
- [Challenge 1]
- [Challenge 2]

### Technical Debt & Recommendations
- [Finding 1]
- [Finding 2]
```