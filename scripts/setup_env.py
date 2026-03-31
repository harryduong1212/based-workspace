import json
import secrets
import string
from pathlib import Path

def generate_secure_password(length=16):
    """Generate a secure random password containing uppercase, lowercase, and digits."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def init_workspace_security():
    # Paths relative to the script's root (one level up from 'scripts/')
    workspace_root = Path(__file__).resolve().parent.parent
    
    env_file = workspace_root / ".env"
    vscode_dir = workspace_root / ".vscode"
    mcp_file = vscode_dir / "mcp.json"

    # Ensure directories exist
    vscode_dir.mkdir(parents=True, exist_ok=True)

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
AI_BACKEND_TYPE=gemini
"""
    env_file.write_text(env_content, encoding="utf-8")
    print(f"[+] Security configuration created at: {env_file}")

    # 2. Process mcp.json file
    mcp_data = {"mcpServers": {}}
    
    # Read existing file if it exists
    if mcp_file.exists():
        try:
            mcp_data = json.loads(mcp_file.read_text(encoding="utf-8"))
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
    mcp_file.write_text(json.dumps(mcp_data, indent=2), encoding="utf-8")
    print(f"[+] Connection string synchronized to: {mcp_file}")
    print("[*] Setup complete. Database password is now secured and synchronized.")

if __name__ == "__main__":
    init_workspace_security()