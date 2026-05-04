---
description: Comprehensive orchestration from Raw Idea -> SRS Specification -> DB Schema -> API Specs -> Sequence Diagram -> Test Prep.
---

# 🚀 End-to-End Feature Pipeline (Comprehensive Project Initialization)

You are the Chief Orchestrator. Your mission is to take a [Raw Feature Idea] from the user, then automatically trigger sequential and parallel child workflows to transform that idea into a complete set of documentation and technical environments ready for development.

You MUST STRICTLY adhere to the following 5-step execution flow. You MUST use the Output Artifact of the previous step as the Input Context for the next step:

### Step 1: Specification & Business Logic Initialization (Single Source of Truth)
- **Action:** Trigger the `/generate-feature-spec` workflow based on the user's raw idea.
- **Objective:** For the PM, BA, and UX trio to collaborate and generate a standard Software Requirements Specification (SRS) file at `.docs/specs/`.
- **Checkpoint 1:** Pause execution. Display the `.docs/specs/[feature_name]_srs.md` file for user review. Wait for the user to type `Approve` before proceeding.

### Step 2: Data Architecture Foundation (Database Foundation)
- **Input:** The approved SRS file from Step 1.
- **Action:** Trigger the `/generate-db-schema` workflow. Save the Output at `.docs/db/`.
- **Objective:** Finalize table structures, data fields, and the Entity-Relationship Diagram (ERD).
- **Checkpoint 2:** Pause and display the Mermaid ERD diagram. Require the user to type `Approve` or provide edit comments before proceeding.

### Step 3: System Communication Design (Parallel Fan-Out)
- **Input:** The SRS file (from Step 1) and Database Schema (from Step 2).
- **Action (Stream 3A):** Trigger `/generate-api-spec` to finalize the API Contract and save Output at `.api/`.
- **Action (Stream 3B):** Trigger `/generate-sequence-diagram` to map the interaction flow and save Output at `.docs/sequence-diagrams/`. Both streams must execute simultaneously.
- **Checkpoint 3:** Consolidate and display the API Spec and Sequence Diagram on the screen. Require the user to type `Approve`.

### Step 4: Quality Assurance & Environment Prep (QA Prep)
- **Input:** All artifacts from Step 1, Step 2, and Step 3 (SRS, DB, API, Sequence).
- **Action:** Trigger the `/prepare-test-environment` workflow. Save the Test Plan at `.docs/tests/`.
- **Objective:** Require QA and Backend to generate mock data (Seed Data/Mocks) and write automated test scripts (Automation Scripts) to pave the way for Developers.

### Step 5: Consolidation & Packaging (Gather & Wrap-up)
- **Action (Verification):** Verify the existence of all files generated in the previous 4 steps.
- **Action (Manifestation):** Create a `[feature_name]_manifest.md` file in the `.docs/specs/` directory containing linked references to all technical files.
- **Final Output:** Display the message "🎉 Planning & Design phase is 100% complete."