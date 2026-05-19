"""Skill Discovery MCP — semantic search over `.archived/skills/<cat>/<skill>/SKILL.md`.

Exposes `find_skills(query, k)` as an MCP tool so agents can pull the most
relevant skill bodies for the current task instead of relying on hand-curated
`requires_skills` lists in recipes.

Backed by the same Qdrant instance the `memory` MCP uses, but a separate
collection (`based_skills` by default) — see roadmap D3.

Run as a module: `python -m services.skill_discovery_mcp`         # stdio server
                 `python -m services.skill_discovery_mcp reindex` # rebuild collection
"""
