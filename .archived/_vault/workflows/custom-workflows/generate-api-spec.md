---
description: Generates standardized API contracts based on the SRS and Database Schema.
---

# 🔌 API Specification Generation

You are the Orchestrator coordinating the `@backend-architect` to define the API layer. This workflow typically runs in parallel with the Sequence Diagram generation.

You MUST STRICTLY adhere to the following execution flow:

### Step 1: Endpoint Identification
- **Input:** The SRS file (`.docs/specs/[feature_name]_srs.md`) and Database Schema (`.docs/db/[feature_name]_schema.md`).
- **Action:** Map the required user actions and data interactions to specific RESTful endpoints, GraphQL mutations/queries, or tRPC procedures. Define HTTP methods, route paths, and authentication requirements for each.
- **Output:** A list of required API endpoints.

### Step 2: Contract Definition
- **Input:** The list of endpoints from Step 1.
- **Action:** Define the exact request payloads (headers, parameters, body) and response payloads (success and error states). Ensure alignment with the database schema types and the SRS Data Dictionary constraints.
- **Output:** Detailed request and response structures.

### Step 3: OpenAPI/Swagger Generation
- **Input:** The defined contracts from Step 2.
- **Action:** Format the API specification into standard OpenAPI 3.0 (YAML or JSON) format. Include detailed descriptions, example payloads, and proper status code documentation (200, 400, 401, 403, 404, 500).
- **Output:** A complete OpenAPI specification.

### Step 4: Verification & Checkpoint
- **Action:**
  1. Display a summary of the generated API endpoints.
  2. Wait for the parallel Sequence Diagram generation to complete (if applicable) before requiring the user to type `Approve`.

### Step 5: Artifact Storage
- **Action:**
  1. Ensure the `.api/` directory exists.
  2. Save the specification to `.api/[feature_name]_api_spec.yaml` (or `.json` / `.md` depending on project standards).