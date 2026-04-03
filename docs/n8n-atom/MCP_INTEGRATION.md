# n8n-atom MCP Integration Guide

This guide explains how to connect your n8n-atom instance to AI Assistants (like Cursor, Claude Code, or Antigravity) using the Model Context Protocol (MCP), and how to create new n8n workflows that your AI can use as tools.

---

## 1. Core Architecture: Engine vs. Inspector

When working with MCP in this stack, there are two separate systems. **Do not confuse them.**

### The Engine: `n8n-atom-cli` 
*   **What it is:** The actual bridge between your AI Assistant and your n8n database.
*   **What it does:** It translates your `.n8n` workflow files into "Tools" that the AI understands. When the AI calls a tool, the CLI executes your workflow over the internal n8n REST API (using the localhost guard bypass).
*   **Status:** **Required.** This is what your AI configurations must point to.

### The Inspector: `mcp-inspector-atom8n`
*   **What it is:** A Web-based testing dashboard (forked from Anthropic).
*   **What it does:** It provides a browser interface at `http://localhost:6274` to manually test your workflows and see the raw JSON outputs. Because it is a Node.js/React application, it requires build artifacts (`build/index.js`) to function.
*   **Status:** **Optional (For Debugging only).** Your global AI configs should NEVER point to the inspector.

---

## 2. Global AI Configuration (`mcp.json`)

To allow your AI to use your n8n workflows as tools, you must update your global MCP configuration (e.g., in Cursor settings or `mcp_config.json`).

There are two ways to configure this depending on how you installed `n8n-atom`:

### Method A: Published Tool (Best for Quickstart Users)
If you did not download the GitHub repository and are running n8n purely via standard Docker images, use `npx` to fetch the CLI bridge dynamically from the internet.

```json
{
  "mcpServers": {
    "atom8n": {
      "command": "npx.cmd",  // Use npx.cmd on Windows, or just npx on macOS/Linux
      "args": [
        "-y",
        "n8n-atom-cli@latest",
        "mcp",
        "n8n-workflows/mcp-curl-get.n8n",  // Point to where you save your workflows
        "n8n-workflows/mcp-logger.n8n"
      ],
      "env": {
        "N8N_PORT": "5678"
      }
    }
  }
}
```

### Method B: Local Script (Best for Developers)
If you cloned the `n8n-atom` repository and want to run/modify the CLI bridge locally from the source files.

```json
{
  "mcpServers": {
    "atom8n": {
      "command": "node",
      "args": [
        "external/n8n-atom/packages/n8n-atom-cli/bin/n8n.mjs",
        "mcp",
        "external/n8n-atom/mcp-curl-get.n8n",
        "external/n8n-atom/mcp-logger.n8n"
      ],
      "env": {
        "N8N_PORT": "5678"
      }
    }
  }
}
```

*(Note: If you encounter `Cannot find package 'zod'` errors, you must run `npm install` inside the `packages/n8n-atom-cli/` directory!)*

---

## 3. Creating New Workflow Tools

The `n8n-atom` MCP server does NOT automatically expose every workflow in your n8n database to the AI. This is an intentional security design.

To create a new tool for your AI, follow these steps:

### Step 1: Build Visually using n8n
Do not try to code `.n8n` files manually. It is much faster and less error-prone to use the n8n UI.

1. Open your n8n dashboard (`http://localhost:5678`).
2. Create a new workflow.
3. **Crucial:** Add the **`Execute Workflow Trigger`** node as your starting point.
4. Open the Trigger node and define **Workflow Inputs** (e.g., text, numbers, booleans). 
   * *The `n8n-atom-cli` will automatically parse these inputs and use them to define the arguments the AI must provide!*
5. Build the rest of your automation logic.

### Step 2: Export to Workspace
1. While in the n8n UI, click the `...` menu in the top right corner.
2. Select **Download** to save the workflow as a `.n8n` file.
3. Move this file into your workspace (e.g., `n8n-workflows/my-new-tool.n8n`).

### Step 3: Register the Tool
1. Open your global `mcp.json` file.
2. Add the path of your newly downloaded `.n8n` file to the `args` array:
   ```json
       "args": [
         "mcp",
         "n8n-workflows/mcp-logger.n8n",
         "n8n-workflows/my-new-tool.n8n" // <--- Added here
       ]
   ```
3. Restart your AI Assistant (Cursor). It will instantly read the new file and recognize the new tool.
