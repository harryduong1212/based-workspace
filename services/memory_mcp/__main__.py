"""Entry point — `python -m services.memory_mcp` (stdio transport)."""
from .server import app

if __name__ == "__main__":
    app.run()
