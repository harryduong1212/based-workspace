"""mem0-backed MCP server — recipe-facing id is `memory`.

Exposes `search_memory` and `add_memory` tools. Backend stack:
  - vector store: Qdrant (services/control_panel/features/catalog.yaml)
  - embedder:    bge-small via llama-swap (OpenAI-compatible URL)
  - fact LLM:    Gemma via llama-swap

Run as `python -m services.memory_mcp` (stdio transport).
"""
