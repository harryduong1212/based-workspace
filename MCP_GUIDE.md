# Model Context Protocol (MCP) Server Guidelines

This document provides a comprehensive guide to understanding, managing, configuring, and securing MCP servers within the `based-workspace` environment. 

---

## 1. What is an MCP Server?
A **Model Context Protocol (MCP)** server acts as a bridge between an AI coding assistant (like Antigravity, Cursor, or VS Code Cline/Roo) and external tools, databases, or APIs. 

Instead of an AI relying entirely on built-in tools (like terminal access or file browsing), an MCP server provides *domain-specific capabilities*.

In this workspace, MCP servers are used to:
1. Provide isolated SQL read/write capabilities directly to your Postgres database (`postgres-memory`).
2. Search and pull external framework documentation (`context7`).
3. Search massive AST and open-source codebases (`grep_app`).

---

## 2. Where is it Configured?
All workspace-level MCP servers are defined in a single file:  
👉 **`.vscode/mcp.json`**

Whenever you add or modify a server in this file, your AI coding assistant will parse the JSON, start the defined scripts in the background, and inject their tools into the AI's context.

---

## 3. Best Practice: Securing MCP Secrets
By default, the `@modelcontextprotocol/server-postgres` package accepts a database connection string natively. 

**Anti-Pattern (Unsecure):**
```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-postgres",
    "postgresql://admin:super_secret_password@localhost:5432/ai_memory"
  ]
}
```
If you commit your `mcp.json` file to Git with this configuration, your database password is automatically exposed.

**The "Based Workspace" Pattern (Secure):**
We utilize dynamic `.env` loader scripts saved in the `scripts/` directory.

1. `setup_env.py` places a `.env` file containing the password in the workspace root.
2. `scripts/postgres-mcp.js` securely reads `.env` at runtime to construct the `postgresql://` string in memory.
3. `mcp.json` simply points to the wrapper node script without exposing any secrets:

```json
{
  "postgres-memory": {
    "command": "node",
    "args": [
      "scripts/postgres-mcp.js"
    ]
  }
}
```
*Always use wrapper scripts for any MCP servers that require passwords or API Keys (e.g. Supabase, AWS, etc.).*

---

## 4. Enabling & Disabling Servers
If you do not want an MCP server running (because it is missing, or you temporarily don't need its tools to save context length), you **do not** need to delete the JSON block entirely.

Simply prepend an underscore (`_`) to the key name. The AI client will safely ignore it.

**Enabled:**
```json
"grep_app": {
  "command": "node"
}
```
**Disabled:**
```json
"_grep_app": {
  "command": "node"
}
```

---

## 5. Adding New MCP Servers
You can find hundreds of open-source MCP servers for platforms like Slack, Google Drive, Postgres, GitHub, and more.

To add a new server:
1. Open `.vscode/mcp.json`.
2. Determine if it requires an API key. 
   - **If YES:** Create a `scripts/<your-server>-mcp.js` script to load the API key from your `.env` file.
   - **If NO:** Use `npx` directly in the `mcp.json` (as seen in the `context7` block).
3. Append it to the `"mcpServers"` object.
4. Reload your editor window (`Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on macOS -> `Developer: Reload Window`).

---

## 6. How to Test Your MCP Servers
Because MCP servers don't output visually to a terminal, you must "ask" your AI assistant to perform an action using them.

### Checklist for Testing:
- [ ] Is `mcp.json` properly formatted without red syntax errors?
- [ ] Did you reload the VS Code Window?
- [ ] Ask the LLM: *"Use your available MCP tools to list the database tables."*
- [ ] Ask the LLM: *"Can you fetch documentation regarding Next.js 15 using context7?"*
- [ ] Check if the AI acknowledges receiving tools/context from the server rather than just guessing.
