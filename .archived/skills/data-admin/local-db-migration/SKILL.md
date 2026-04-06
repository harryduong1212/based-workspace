---
name: local-db-migration
description: Manages schema migrations and vector initialization for the based-workspace-postgres container.
---

# Local DB Migration Skill

This skill provides instructions for managing the local PostgreSQL database used for AI memory and vector storage.

## Core Responsibilities
- **Initialize Vector Store:** Ensure the `vector` extension is enabled in the `ai_memory` database.
- **Manage Schema:** Execute SQL migration scripts to define and update tables for vector embeddings and contextual memory.
- **Connection Management:** Utilize the `postgres-memory` MCP tool to interact with the database at `postgresql://admin:password@localhost:5432/ai_memory`.

## Standard Procedures

### 1. Vector Initialization
Always verify that the pgvector extension exists before performing vector operations:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Migration Execution
When a new migration is required:
1. Create a new `.sql` file in a `migrations/` subdirectory (if not already existing).
2. Use the `postgres-memory.query` tool to execute the contents of the migration file.
3. Record the migration version in a dedicated `schema_migrations` table.

## Constraints
- Only target the `based-workspace-postgres` container.
- Do not modify databases other than `ai_memory` unless explicitly instructed.
