---
description: Transforms the Software Requirements Specification (SRS) into a finalized database schema and Entity-Relationship Diagram (ERD).
---

# 🗄️ Database Schema Generation

You are the Orchestrator coordinating the `@database-architect` to design the data layer based on the approved feature specification.

You MUST STRICTLY adhere to the following execution flow and use the Output Artifact of the previous step as the Input Context:

### Step 1: Entity & Relationship Extraction
- **Input:** The approved SRS file located at `.docs/specs/[feature_name]_srs.md`.
- **Action:** Analyze the Data Dictionary and Flow of Events to identify all required database entities, attributes, primary/foreign keys, and exact data types. Define constraints and indexing strategies for performance optimization.
- **Output:** A structured list of tables, columns, relationships, and constraints.

### Step 2: ERD Generation
- **Input:** The extracted entities and relationships from Step 1.
- **Action:** Generate a comprehensive Entity-Relationship Diagram using `Mermaid` syntax (`mermaid erDiagram`). Ensure all cardinalities (one-to-one, one-to-many, many-to-many) are accurately represented.
- **Output:** A Mermaid ERD code block.

### Step 3: Schema Script Creation
- **Input:** The entities and relationships from Step 1.
- **Action:** Write the actual SQL DDL (Data Definition Language) or ORM models (e.g., Prisma, TypeORM, SQLAlchemy) required to create these structures in the target database. Include necessary migrations if modifying an existing schema.
- **Output:** Executable schema definitions.

### Step 4: Verification & Checkpoint
- **Action:** 1. Display the generated Mermaid ERD diagram on the screen.
  2. Pause execution and require the user to type `Approve` or provide edit comments before proceeding to save.

### Step 5: Artifact Storage
- **Action:**
  1. Ensure the `.docs/db/` directory exists.
  2. Save the Mermaid ERD and schema definitions into `.docs/db/[feature_name]_schema.md`.
  3. If raw SQL or ORM files were generated, save them to the appropriate project directories and link them in the markdown file.