<!--
Sync Impact Report
- Version change: 1.0.0 -> 2.0.0
- Modified principles:
  - I. CLI Contract Is Stable -> I. Web Chat Product Scope Is Mandatory
  - II. Theme Data Consistency Is Mandatory -> II. Persona Prompt Is Source of Truth
  - III. Tests Protect Behavior (NON-NEGOTIABLE) -> III. Sarcasm Safety and Calibration Are Enforced
  - IV. Observability and Explicit Failures -> IV. LLM Provider Abstraction Is Required
  - V. Simplicity and Reviewable Changes -> V. Reliability, Observability, and Tests Are Non-Negotiable
- Added sections:
  - V2 Architecture Constraints
- Removed sections:
  - Operational Constraints
- Templates requiring updates:
  - ✅ updated `.specify/templates/plan-template.md`
  - ✅ updated `.specify/templates/spec-template.md`
  - ✅ updated `.specify/templates/tasks-template.md`
  - ⚠ pending `.specify/templates/commands/*.md` (directory not present in this repository)
  - ✅ updated `README.md`
- Follow-up TODOs:
  - None
-->
# SassyAI Constitution

## Core Principles

### I. Web Chat Product Scope Is Mandatory
- SassyAI V2 is a web chatbot product with a classic chat interface (frontend) and a backend chat
  service; this is the only in-scope runtime architecture.
- CLI features and command surfaces are deprecated and MUST NOT receive new product features.
- New work MUST target browser-based chat UX and backend chat APIs rather than terminal workflows.

Rationale: A single product direction prevents split effort and enables a coherent V2 rewrite.

### II. Persona Prompt Is Source of Truth
- Sarcastic behavior MUST be controlled by a dedicated system prompt artifact stored in the
  repository (with optional few-shot examples).
- Persona prompt artifacts MUST be versioned and reviewable in pull requests; runtime-only persona
  changes are prohibited.
- Chat generation pathways MUST reference the managed persona artifact instead of duplicating
  persona text in scattered code paths.

Rationale: Versioned persona control keeps tone consistent and makes behavioral changes auditable.

### III. Sarcasm Safety and Calibration Are Enforced
- The product MUST support defined sarcasm calibration levels (for example: low/medium/high) with
  predictable behavioral differences.
- Sarcastic output MUST NOT include hate or harassment targeting protected characteristics.
- Unsafe user requests or unsafe model outputs MUST trigger refusal or neutralization behavior
  rather than uncensored delivery.

Rationale: The product tone is core value, but it must remain safe and policy-compliant.

### IV. LLM Provider Abstraction Is Required
- The backend MUST call LLMs through a provider abstraction layer rather than provider-specific
  logic embedded directly in route handlers.
- Provider selection and credentials MUST be configured via environment variables.
- The abstraction MUST allow adding providers (e.g., OpenAI, Mistral, Gemini) without breaking the
  chat API contract.

Rationale: Pluggability reduces vendor lock-in and keeps integrations maintainable.

### V. Reliability, Observability, and Tests Are Non-Negotiable
- Backend timeout/provider failures MUST be handled gracefully with safe fallback responses; user
  paths MUST NOT crash or expose stack traces.
- Observability MUST capture request latency and provider errors while never logging secrets and
  never logging full prompts by default.
- Every behavior change MUST include tests for persona policy enforcement, provider adapter
  behavior, and API-level chat flow outcomes.

Rationale: Robust error handling and targeted tests protect user experience in LLM-dependent flows.

## V2 Architecture Constraints

- Architecture MUST start with one backend service and one frontend web UI.
- Premature microservice decomposition is prohibited unless a constitution amendment or approved
  complexity exception justifies it.
- Service boundaries, prompt assets, and provider configs MUST remain explicit and source
  controlled.

## Development Workflow & Quality Gates

1. Define scope in `spec.md`, including web chat UX impact, persona prompt changes, provider
   abstraction impact, and safety/fallback behavior.
2. Add or update tests first for persona policy, provider adapter behavior, and API-level chat
   flow.
3. Implement the smallest viable change set in the backend/frontend split without introducing new
   services.
4. Validate timeout/error paths and confirm safe fallback behavior without stacktrace exposure.
5. Validate observability outputs for latency/errors and confirm logs exclude secrets and full
   prompts by default.
6. Reviewers MUST block merges when any Constitution principle is violated without an approved,
   documented exception.

## Governance

- This Constitution takes precedence over conflicting workflow notes or templates.
- Amendments require a pull request that includes: proposed change text, impacted templates/docs,
  migration steps (if any), and version bump rationale.
- Versioning policy for this document follows semantic intent:
  - MAJOR: Removes or redefines a principle in a backward-incompatible way.
  - MINOR: Adds a new principle/section or materially expands governance requirements.
  - PATCH: Clarifies wording, fixes typos, or improves precision without changing obligations.
- Compliance review is required in every implementation plan and pull request; unresolved
  violations block approval.

**Version**: 2.0.0 | **Ratified**: 2026-02-26 | **Last Amended**: 2026-02-26
