---
description: Maps the interaction flow between users, system components, and third-party services.
---

# 🔄 Sequence Diagram Generation

You are the Orchestrator coordinating the `@senior-architect-v2` to visualize the system interactions required to fulfill the feature's business logic. This workflow typically runs in parallel with API Specification generation.

You MUST STRICTLY adhere to the following execution flow:

### Step 1: Actor and Component Identification
- **Input:** The SRS file (`.docs/specs/[feature_name]_srs.md`) and Database Schema (`.docs/db/[feature_name]_schema.md`).
- **Action:** Identify all participating entities in the feature flow. This includes the User (Client/Frontend), API Gateway, Backend Services, Database, and any external third-party integrations (e.g., Payment Gateways, Email Services).
- **Output:** A list of sequence diagram participants.

### Step 2: Flow Mapping
- **Input:** The Flow of Events section from the SRS and the participants from Step 1.
- **Action:** Translate the business logic into chronological technical calls. Map out synchronous and asynchronous operations, loops, and conditional logic (alt/else blocks) for error handling.
- **Output:** A step-by-step technical interaction flow.

### Step 3: Mermaid Generation
- **Input:** The technical flow from Step 2.
- **Action:** Generate a precise `Mermaid` sequence diagram (`mermaid sequenceDiagram`). Use standard conventions (solid lines for requests, dotted lines for responses, activation boxes for processing). Include alternative paths for failure states defined in the SRS.
- **Output:** A Mermaid sequence diagram code block.

### Step 4: Verification & Checkpoint
- **Action:**
  1. Display the generated Mermaid Sequence Diagram on the screen.
  2. Wait for the parallel API Spec generation to complete (if applicable) before requiring the user to type `Approve`.

### Step 5: Artifact Storage
- **Action:**
  1. Ensure the `.docs/sequence-diagrams/` directory exists.
  2. Save the Mermaid diagram and explanatory text to `.docs/sequence-diagrams/[feature_name]_sequence.md`.