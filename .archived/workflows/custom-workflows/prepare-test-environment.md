---
description: Prepare test environment, generate mock data, and write early-stage automated test scripts to pave the way for development.
---

# 🧪 Test Environment Preparation

I will help you set up a robust testing foundation for your feature, including mock data strategy, environment configuration, and initial test automation scripts.

## Guardrails
- **No Data Leakage**: Never use real production data for mocks; use synthetic data generators (like Faker).
- **Environment Isolation**: Ensure test environments are isolated from development and production.
- **Maintainability**: Write tests and mocks that are easy to update as the feature evolves.
- **Tool-Agnostic**: Detect existing project tools (e.g., Prisma, MSW, Vitest, Pytest) before proposing new ones.

## Steps

### Step 1: Mock Data Strategy (Seed Data)
- **Action:** Analyze the Database Schema (from the Kickoff) and identify all required entities.
- **Objective:** Create a `seed_data.json` or equivalent script (e.g., Prisma Seed, SQL Seed) in `.docs/tests/mocks/`.
- **Details:** Ensure coverage for edge cases, null values, and complex relationships.

### Step 2: Environment Configuration
- **Action:** Identify required environment variables, local databases, or container configurations (e.g., `docker-compose.test.yaml`).
- **Objective:** Generate a `test_setup_guide.md` in `.docs/tests/` to help developers replicate the QA environment.

### Step 3: Automation Scaffolding
- **Action:** Scaffolding the initial test files (Empty test suites with TODOs) for the detected framework.
- **Objective:** Create a logical test structure that matches the API Spec and Sequence Diagrams.

### Step 4: Verification & Handover
- **Action:** Create a `test_plan.md` manifest in `.docs/tests/` that summarizes the testing strategy, mock locations, and automation targets.

## Principles
- **Early Testing**: Secure the quality foundation before a single line of feature code is written.
- **Shift Left**: Empower developers with ready-made mocks and test scaffolds.
- **Realistic Mocks**: Mocks must strictly adhere to the API Contract defined in `.api/`.

## Keywords
test prep, mock data, seed data, test environment, QA, automation scripts, test plan, feature initiation
