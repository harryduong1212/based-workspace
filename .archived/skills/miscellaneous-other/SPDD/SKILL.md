# SPDD: Spec, Planning, Development, and Deployment

**A multi-stage orchestration protocol for transforming raw ideas into production-ready code.**

---

## 🏗️ Stage 1: Research (Codebase Cartography)

**Mission:** Document and explain the codebase exactly as it exists today.

### Critical Rules:
- **Map, Don't Change:** Do not suggest improvements, refactorings, or architectural changes.
- **Pure Description:** Describe what exists, where it exists, and how components interact.
- **Full Context:** Read mentioned files in their entirety (no limit/offset).

### Workflow:
1. **Initial Analysis:** Read the target files fully.
2. **Decomposition:** Break down the inquiry into research areas (Routes, Database, UI, etc.).
3. **Execution:** Localize components, analyze current function, and identify existing patterns.
4. **Project State:**
   - **New Project:** Research and list best-in-class folder structures and libraries for the stack.
   - **Existing Project:** Identify technical debt or established patterns that must be respected.

---

## 📋 Stage 2: Implementation Planning (Spec Writing)

**Mission:** Create detailed, actionable implementation plans with zero ambiguity.

### Critical Rules:
- **Phase Validation:** Do not write the full plan at once; validate phase structure with the user first.
- **Pre-emptive Decisions:** Make all technical decisions before finalizing the plan.
- **Skepticism:** Be skeptical of vague requirements.

### Workflow:
1. **Context Check:** Review the research documentation generated in Stage 1.
2. **Phasing:** Divide work into incremental, testable phases.
3. **Detailing:** For every affected file, specify path, action (CREATE|MODIFY|DELETE), and logic/snippets.
4. **Success Criteria:** Define automated verification (scripts/tests) and manual verification (UI/UX).

---

## 🛠️ Stage 3: Implementation Execution (Precision Coding)

**Mission:** Implement the approved technical plan with surgical precision.

### Critical Rules:
- **Strict Adherence:** Follow the plan's intent while adapting to discovered realities.
- **Atomic Phases:** Complete one phase entirely before moving to the next.
- **Stop & Think:** If you find a spec error or code mismatch, STOP and report immediately.

### Workflow:
1. **Sanity Check:** Review the Spec and original Ticket. Ensure a clean environment.
2. **Execution:** Code following Clean Code patterns and the Spec's snippets.
3. **Verification:**
   - Execute "Automated Verification" after every phase.
   - Pause for manual user confirmation after every phase.
4. **Progress:** Update checkboxes in the Spec file as you advance.

---

## 🚀 Stage 4: Completion & Regression

**Mission:** Finalize the task and ensure system stability.

1. **Test Results:** Provide a final report of all test results.
2. **Regression:** Perform regression tests if requested.
3. **Next Steps:** Ask for the next task or deployment instructions.
