# Implementation Plan: SassyAI V2 Web Chatbot MVP

**Branch**: `001-rewrite-web-chatbot` | **Date**: 2026-02-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rewrite-web-chatbot/spec.md`

**Note**: This plan covers the MVP only: one backend service, one web frontend, no auth, no database, and in-memory session state.

## Summary

Deliver a minimal SassyAI V2 web chatbot composed of one Python backend service and one web frontend.
The backend exposes the chat API, applies persona and safety policy, routes generation through a
provider abstraction, and returns safe fallback responses on provider failures. The frontend offers
a classic chat UI with sarcasm level selection and a single active in-memory conversation.

## Technical Context

**Language/Version**: Python 3.12 (backend), HTML5/CSS3/JavaScript ES2023 (frontend)  
**Primary Dependencies**: FastAPI, Uvicorn, Pydantic, HTTP client for provider calls, pytest, pytest-cov  
**Storage**: In-memory session store only (no database)  
**Testing**: pytest unit tests for persona policy and provider adapter, API integration tests for chat flow  
**Target Platform**: Modern desktop/mobile browsers and a single Linux-hosted web service  
**Project Type**: web application  
**Performance Goals**: First reply or safe fallback returned within the configured timeout budget; normal chat interactions feel immediate in a single-session MVP  
**Constraints**: One backend service + one web frontend only; no auth; no database; in-memory session only; provider abstraction required; persona prompt must live in a versioned repo file; logs must exclude secrets and full prompts by default  
**Scale/Scope**: MVP for low-volume interactive usage, one active conversation per browser session, single-instance deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate Review

- **Web Scope Gate**: PASS. Scope is limited to a browser chat UI plus backend API and does not add any CLI surface.
- **Persona Source Gate**: PASS. The plan stores the canonical persona in a versioned repository file with optional examples alongside it.
- **Safety Calibration Gate**: PASS. The plan defines low/medium/high sarcasm levels and explicit refusal or neutralization for hateful or harassing content targeting protected characteristics.
- **Provider Abstraction Gate**: PASS. All LLM access is routed through a provider adapter selected by environment configuration.
- **Reliability/Observability Gate**: PASS. Timeout and provider failures return safe fallback messages, while latency and provider errors are logged without secrets or full prompt bodies.
- **Test Gate**: PASS. The plan includes failing-first coverage for persona policy, provider adapter behavior, and API chat flow.
- **Minimal Architecture Gate**: PASS. Architecture remains one backend service plus one web frontend with no auth and no database.

### Post-Design Gate Review

- **Web Scope Gate**: PASS. `contracts/chat-api.yaml` and `quickstart.md` define only the web chat path.
- **Persona Source Gate**: PASS. `research.md` and `data-model.md` define a versioned persona asset as the single source of truth.
- **Safety Calibration Gate**: PASS. `data-model.md` and `contracts/chat-api.yaml` define bounded sarcasm levels and refusal/fallback flags.
- **Provider Abstraction Gate**: PASS. `research.md` specifies an adapter interface and environment-driven provider selection.
- **Reliability/Observability Gate**: PASS. `research.md`, `contracts/chat-api.yaml`, and `quickstart.md` preserve safe fallback behavior and redacted logging.
- **Test Gate**: PASS. `quickstart.md` requires persona policy, provider adapter, and API chat flow tests.
- **Minimal Architecture Gate**: PASS. Project structure stays within one backend and one frontend; no complexity exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/001-rewrite-web-chatbot/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── chat-api.yaml
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   ├── chat/
│   ├── llm/
│   ├── safety/
│   ├── observability/
│   └── config/
├── persona/
│   ├── system_prompt.md
│   └── few_shot_examples.yaml
└── tests/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── app/
│   ├── chat/
│   ├── components/
│   └── services/
└── tests/
    └── smoke/
```

**Structure Decision**: Use a single Python backend service for API, policy, provider routing, and
in-memory session state plus a separate minimal web frontend for the classic chat interface. Keep
persona files versioned under the backend tree to make prompt changes reviewable. No additional
services, persistence layers, or authentication components are introduced in the MVP.

## Complexity Tracking

No constitution violations or complexity exceptions are required for this MVP plan.
