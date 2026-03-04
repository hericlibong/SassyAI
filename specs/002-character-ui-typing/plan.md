# Implementation Plan: Character UI Typing Upgrade

**Branch**: `002-character-ui-typing` | **Date**: 2026-03-04 | **Spec**: `/specs/002-character-ui-typing/spec.md`
**Input**: Feature specification from `/specs/002-character-ui-typing/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Upgrade the single-page web chat UI to a product-grade character style, add client-side word-by-word assistant reveal with Skip, and add utility controls (prompt chips, copy, reset, classification badge) while preserving the `/api/chat` contract and in-memory MVP constraints. The plan uses existing frontend modules for UI state transitions, keeps backend schema compatibility, and adds minimal prompt-guidance adjustments for FR/EN language consistency.

## Technical Context

**Language/Version**: Python 3.12 (backend), JavaScript ES modules + HTML/CSS (frontend)  
**Primary Dependencies**: FastAPI, Pydantic, Uvicorn, httpx (backend); browser Fetch + DOM APIs (frontend)  
**Storage**: In-memory session store only (no DB, no persistence)  
**Testing**: pytest + pytest-cov (backend contract/integration/unit); frontend verified via scenario testing  
**Target Platform**: Linux-hosted API + modern desktop/mobile browsers  
**Project Type**: Web application (frontend + backend service)  
**Performance Goals**: Typing indicator shown for 100% pending responses; skip reveals full remaining reply in <1s for most messages  
**Constraints**: Must keep `/api/chat` schema stable; single-page UX; no auth/DB; backend tests must remain green  
**Scale/Scope**: MVP single conversation per browser session, transient in-memory context, Option B visual refresh

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Gate 1 – Web chat product scope only**: PASS. Changes remain in `frontend/src` and minimal backend behavior guidance for chat replies.
- **Gate 2 – Persona prompt source of truth**: PASS. Language consistency updates are limited to prompt guidance flow, not ad-hoc scattered persona text.
- **Gate 3 – Sarcasm safety/calibration enforced**: PASS. Existing safety and sarcasm-level behavior remains intact; UI features do not bypass policy.
- **Gate 4 – Provider abstraction remains required**: PASS. No provider-specific route coupling introduced; `/api/chat` stays behind existing service/provider layer.
- **Gate 5 – Reliability/observability/tests**: PASS. Contract remains stable and planning includes backend regression tests before completion.

## Project Structure

### Documentation (this feature)

```text
specs/002-character-ui-typing/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   ├── chat/
│   ├── config/
│   ├── llm/
│   ├── observability/
│   └── safety/
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── app/
│   ├── chat/
│   └── services/
└── (no automated frontend tests currently)
```

**Structure Decision**: Use the existing web-application split (`backend/` + `frontend/`) and implement this feature primarily in `frontend/src/chat`, `frontend/src/styles.css`, and minimally in backend chat/prompt flow if language-guidance adjustment is required.

## Post-Design Constitution Check

- **Gate 1 – Web chat product scope only**: PASS. Phase 1 artifacts target only frontend chat UX and existing backend chat flow.
- **Gate 2 – Persona prompt source of truth**: PASS. Language consistency is planned through existing prompt pathway, preserving centralized persona governance.
- **Gate 3 – Sarcasm safety/calibration enforced**: PASS. No design artifact introduces bypasses for refusal/neutralization or sarcasm-level controls.
- **Gate 4 – Provider abstraction remains required**: PASS. Contracts preserve `/api/chat` and existing provider registry/service layering.
- **Gate 5 – Reliability/observability/tests**: PASS. Quickstart includes backend regression run and preserves fallback/error behavior expectations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
