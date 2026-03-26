import os
import json
import secrets
import string

def generate_secure_password(length=16):
    """Generate a secure random password containing uppercase, lowercase, and digits."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def init_workspace_security():
    # Paths relative to the script's root (one level up from 'scripts/')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    env_file = os.path.join(workspace_root, ".env")
    vscode_dir = os.path.join(workspace_root, ".vscode")
    mcp_file = os.path.join(vscode_dir, "mcp.json")

    # Ensure directories exist
    os.makedirs(vscode_dir, exist_ok=True)

    # 1. Generate password and write .env file
    db_password = generate_secure_password()
    env_content = f"""# PostgreSQL Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD={db_password}
POSTGRES_DB=ai_memory
POSTGRES_PORT=5432

# n8n Configuration
N8N_HOST=localhost
N8N_PORT=5678
NODE_ENV=production
WEBHOOK_URL=http://localhost:5678/
"""
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)
    print(f"[+] Security configuration created at: {env_file}")

    # 2. Process mcp.json file
    mcp_data = {"mcpServers": {}}
    
    # Read existing file if it exists
    if os.path.exists(mcp_file):
        try:
            with open(mcp_file, "r", encoding="utf-8") as f:
                mcp_data = json.load(f)
        except json.JSONDecodeError:
            print(f"[-] Error reading {mcp_file}. Initializing a new configuration.")
    
    if "mcpServers" not in mcp_data:
        mcp_data["mcpServers"] = {}

    # Update secure connection for postgres-memory
    mcp_data["mcpServers"]["postgres-memory"] = {
        "command": "node",
        "args": [
            "scripts/postgres-mcp.js"
        ]
    }

    # Add context7 if it does not exist in the configuration
    if "context7" not in mcp_data["mcpServers"]:
        mcp_data["mcpServers"]["context7"] = {
            "command": "npx",
            "args": [
                "-y",
                "@upstash/context7-mcp@latest"
            ]
        }

    # Write the updated mcp.json file
    with open(mcp_file, "w", encoding="utf-8") as f:
        json.dump(mcp_data, f, indent=2)
    print(f"[+] Connection string synchronized to: {mcp_file}")
    print("[*] Setup complete. Database password is now secured and synchronized.")

if __name__ == "__main__":
    init_workspace_security()