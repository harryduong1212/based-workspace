---
description: Create new stack-agnostic workflows for the Antigravity repository
---

# Workflow Creator

I will help you create a new workflow that follows our stack-agnostic, question-driven philosophy and ensures it is correctly categorized within the repository.

## Guardrails
- Every workflow MUST be stack-agnostic.
- Never hardcode specific frameworks, libraries, or tools.
- Always include a stack detection step.
- Always include clarifying questions.
- Keep workflows focused on a single task.

## Categories

New workflows should be assigned to one of the following categories:
- **🔧 Development**
- **🔀 Git & Collaboration**
- **🧪 Testing & Quality**
- **🐛 Debugging**
- **🔒 Security**
- **📚 Documentation**
- **🚀 Deployment**
- **⚙️ Configuration**
- **🗄️ Database**
- **🤖 AI & LLM**
- **🎨 Creative & UI**
- **♿ Accessibility**
- **🎯 Custom Workflows**

## Steps

### 1. Define the Workflow
Gather information:
- **Name**: kebab-case identifier (e.g., `git-commit`, `debug-error`)
- **Category**: Select from the list above.
- **Description**: One-line summary (5-10 words).
- **Purpose**: What problem does this workflow solve?

### 2. Follow the Template Structure

Every workflow must have these sections:

```markdown
---
description: [5-10 word description]
---

# Workflow Name

Brief intro: what this accomplishes and when to use it.

## Guardrails
- What to AVOID doing
- Scope boundaries
- Critical constraints

## Steps

### 1. Understand Context
Ask clarifying questions:
- What is the goal?
- What constraints exist?
- What's the expected outcome?

### 2. Analyze Project
Detect existing stack:
- Check relevant config files
- Identify framework, tools, patterns
- Look at existing code for conventions

### 3. [Core Implementation Steps]
Describe WHAT to do, not exact code.
Let AI generate appropriate implementation.

### 4. Verify
- How to confirm success
- What to test

## Principles
- Universal best practices

## Reference
- Links to relevant documentation
```

### 3. Validate Against Core Principles

Ensure your workflow follows:

| Principle | Check |
|-----------|-------|
| Stack-Agnostic | Does it work with ANY framework? |
| Question-Driven | Does it ask clarifying questions? |
| Single Responsibility | Does it do ONE thing well? |
| Progressive Disclosure | Does it start minimal, expand on demand? |
| Composable | Can it combine with other workflows? |

### 4. Create the Staging File
Create the workflow file in the root of the archived workflows directory:
```text
.archived/workflows/<name>.md
```

### 5. Register in WORKFLOWS.md
Add an entry to the appropriate category section in [WORKFLOWS.md](../../WORKFLOWS.md). 
Use the following format for the table row:
```markdown
| [<name>](.archived/workflows/<name>.md) | `/<name>` | <description> |
```
> [!NOTE]
> The link should point to the root level initially; the reorganization script will update it to the final hierarchical path.

### 6. Categorize and Reorganize
Run the reorganization script to move the file to its final destination and update the index:
```powershell
python scripts/reorganize_workflows_safe.py
```

### 7. Final Verification
1. Verify the file has been moved to `.archived/workflows/<category-slug>/<name>.md`.
2. Check [WORKFLOWS.md](../../WORKFLOWS.md) to ensure the link has been updated correctly.
3. Test the slash command `/ <name>` (if in an environment that supports it).

## Common Mistakes to Avoid

### ❌ DON'T: Hardcode frameworks
```markdown
### Install Dependencies
npm install react tailwindcss
```

### ✅ DO: Detect and adapt
```markdown
### Analyze Project Stack
- Check for existing UI framework
- Check for existing CSS approach
If unclear, ask the user which they prefer.
```

### ❌ DON'T: Provide boilerplate code
```markdown
Create `Button.tsx`:
import React from 'react'
export const Button = () => <button>Click</button>
```

### ✅ DO: Describe what to create
```markdown
Create a button component that:
- Accepts variant props (primary, secondary)
- Follows the project's existing component patterns
- Uses the project's styling approach
```

## Reference
- See existing workflows in `.archived/workflows/` for examples.
- Check [RULES.md](../../RULES.md) for global project guidelines.
