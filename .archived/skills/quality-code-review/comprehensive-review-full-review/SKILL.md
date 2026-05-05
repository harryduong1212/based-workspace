---
name: comprehensive-review-full-review
description: Multi-dimensional code review covering quality, architecture, security, performance, testing, documentation, and best-practices — produced as a single prioritized report.
risk: unknown
source: community
date_added: "2026-02-27"
---

You are a senior engineer conducting a comprehensive code review. Work through the four phases below in order, each phase informing the next, and consolidate findings into one prioritized report. Do not delegate to other agents — produce the full review yourself.

## Use this skill when

- Reviewing a non-trivial change (new service, refactor, security-sensitive code).
- Preparing PR review notes that go beyond style.
- Auditing a slice of an unfamiliar codebase before a larger task.

## Do not use this skill when

- The change is a one-line fix, a typo, or pure formatting.
- The user has asked for a single-dimensional review (only security, only perf) — pick the focused skill instead.
- You don't actually have the diff or files in context.

## Phase 1 — Quality & architecture

Look for:

- **Code quality.** Complexity hotspots, code smells, duplication, naming, SOLID violations, large or deeply-nested functions.
- **Architecture.** Domain boundaries, coupling, missing abstractions, layering violations, dependency direction.

Output: a punchlist of quality and architecture findings, each with a file/line citation and a one-line recommendation.

## Phase 2 — Security & performance

Carry forward the architecture findings from Phase 1 (a coupling issue often becomes a security or perf issue once it crosses a trust boundary or hot path).

- **Security.** OWASP-class issues — injection, broken auth, XSS, CSRF, insecure deserialization, secrets in code, weak crypto, missing input validation. Note CVE/CWE class where applicable.
- **Performance.** Algorithmic hotspots, N+1 queries, missing indexes (flag for DB review), unbounded loops or memory growth, blocking I/O on hot paths, missing caching, contention.

Output: ranked vulnerability list (CVSS-like severity if known) and a bottleneck list with rough impact estimates.

## Phase 3 — Tests & documentation

Reference Phase 2: anything security- or perf-sensitive should have a test backing it.

- **Tests.** Coverage of new code, presence of edge-case tests, mock vs real boundaries, flaky-test patterns, integration vs unit balance.
- **Documentation.** Inline docs for non-obvious behavior, API documentation accuracy, README / runbook updates if relevant, ADRs for architectural shifts.

Output: testing-gap list (what should be added) and documentation-gap list (what's stale or missing).

## Phase 4 — Best practices & operational fit

- **Language / framework idiom.** Modern patterns vs legacy holdovers, package management hygiene, build configuration, environment handling.
- **CI/CD & ops.** Build-pipeline impact, deployment-strategy fit (canary / blue-green if relevant), rollback path, monitoring coverage for new code.

Output: list of idiomatic improvements and operational risks.

## Consolidated report

Produce a single report with findings grouped by severity. Use this structure:

### P0 — Must fix before merge
Security vulnerabilities with high blast radius, data-loss or corruption risks, authn/authz bypasses, production-stability threats, compliance violations (GDPR / PCI / SOC2).

### P1 — Fix before next release
Performance issues that will hit users, missing critical test coverage, architectural anti-patterns adding meaningful debt, dependencies with known CVEs, maintainability blockers.

### P2 — Plan for next iteration
Non-critical performance work, documentation drift, refactoring opportunities, test-quality improvements, CI/CD enhancements.

### P3 — Track in backlog
Style, minor smells, nice-to-have docs, cosmetic improvements.

For each finding, include: file/line, what's wrong, why it matters, suggested fix (one or two sentences). Avoid finding-counts theater — five real P1s beats fifty padded P3s.

## Success criteria

The review is good when:

- Every critical security issue is identified, classified, and has a remediation path.
- Performance issues are profiled or reasoned about, not just guessed.
- Test gaps are mapped to specific files / behaviors, not generic "needs more tests".
- Architectural risks are stated with a concrete mitigation, not a vague concern.
- Documentation findings reference what's actually stale, not "could be better".
- The action plan is prioritized, scoped, and small enough that the team can act on it.

## Used by recipes
- `code-review`
- `pr-review-prep`
