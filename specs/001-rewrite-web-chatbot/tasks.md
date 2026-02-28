---
description: "Task list for SassyAI V2 Web Chatbot MVP implementation"
---

# Tasks: SassyAI V2 Web Chatbot MVP

**Input**: Design documents from `/specs/001-rewrite-web-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Include persona policy, provider adapter, and API chat flow tests. Tests are REQUIRED by the constitution and feature scope.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web chatbot (default)**: `backend/src/`, `frontend/src/`
- **Tests**: `backend/tests/contract/`, `backend/tests/integration/`, `backend/tests/unit/`, `frontend/tests/smoke/`
- **Persona assets**: `backend/persona/`
- Paths below assume the minimal one-backend + one-frontend MVP structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the backend/frontend workspace for the MVP rewrite

- [x] T001 Create backend package skeleton in `backend/src/__init__.py`, `backend/src/api/__init__.py`, `backend/src/chat/__init__.py`, `backend/src/llm/__init__.py`, `backend/src/safety/__init__.py`, `backend/src/observability/__init__.py`, and `backend/src/config/__init__.py`
- [x] T002 Create backend test package skeleton in `backend/tests/contract/__init__.py`, `backend/tests/integration/__init__.py`, and `backend/tests/unit/__init__.py`
- [x] T003 [P] Create frontend chat app shell in `frontend/src/index.html`, `frontend/src/app/main.js`, `frontend/src/chat/chat-app.js`, and `frontend/src/services/chat_api.js`
- [x] T004 [P] Add backend dependency and test runner manifests in `backend/requirements.txt` and `backend/pytest.ini`
- [x] T005 [P] Add frontend styling and smoke test placeholders in `frontend/src/styles.css` and `frontend/tests/smoke/chat_mvp_smoke.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Define shared request and response schemas in `backend/src/api/schemas.py`
- [ ] T007 [P] Add versioned persona assets in `backend/persona/system_prompt.md` and `backend/persona/few_shot_examples.yaml`
- [ ] T008 [P] Implement persona asset loader in `backend/src/chat/persona_loader.py`
- [ ] T009 [P] Implement provider adapter interface and provider registry in `backend/src/llm/providers.py`
- [ ] T010 [P] Implement environment-based runtime settings in `backend/src/config/settings.py`
- [ ] T011 [P] Implement in-memory session repository for active conversations in `backend/src/chat/session_store.py`
- [ ] T012 Implement baseline safety policy rules and sarcasm-level definitions in `backend/src/safety/policy.py`
- [ ] T013 Implement fallback response helpers for timeout and provider errors in `backend/src/chat/fallbacks.py`
- [ ] T014 Implement redacted latency/error logging utilities in `backend/src/observability/logger.py`
- [ ] T015 Implement backend application factory and health endpoint in `backend/src/api/app.py` and `backend/src/api/routes/health.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Start a Sarcastic Chat (Priority: P1) 🎯 MVP

**Goal**: Deliver the core web chat experience with multi-turn in-memory conversation and selectable sarcasm level.

**Independent Test**: Open the chat UI, send an initial message at `medium`, send a follow-up in the same session, and confirm both replies appear in one transcript while preserving the selected sarcasm level.

### Tests for User Story 1 (REQUIRED) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T016 [P] [US1] Add POST `/api/chat` contract test in `backend/tests/contract/test_chat_api_contract.py`
- [ ] T017 [P] [US1] Add multi-turn API chat flow integration test in `backend/tests/integration/test_chat_flow.py`
- [ ] T018 [P] [US1] Add persona policy unit test for low/medium/high behavior in `backend/tests/unit/test_persona_policy.py`

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement chat orchestration service for normal replies in `backend/src/chat/service.py`
- [ ] T020 [P] [US1] Implement chat API route handler in `backend/src/api/routes/chat.py`
- [ ] T021 [P] [US1] Implement browser API client for chat requests in `frontend/src/services/chat_api.js`
- [ ] T022 [P] [US1] Implement chat transcript UI and sarcasm level selector in `frontend/src/chat/chat-app.js`
- [ ] T023 [US1] Wire backend route registration in `backend/src/api/app.py`
- [ ] T024 [US1] Wire frontend bootstrap and layout assets in `frontend/src/app/main.js`, `frontend/src/index.html`, and `frontend/src/styles.css`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Recover Gracefully from Provider Failure (Priority: P2)

**Goal**: Keep the chat usable when the LLM provider times out or errors by returning a safe fallback response.

**Independent Test**: Simulate provider timeout and provider error paths, then confirm the UI shows a safe fallback reply and the same session can send another message immediately.

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T025 [P] [US2] Add provider adapter timeout and error unit tests in `backend/tests/unit/test_provider_adapter.py`
- [ ] T026 [P] [US2] Add fallback API integration test in `backend/tests/integration/test_chat_fallback.py`

### Implementation for User Story 2

- [ ] T027 [P] [US2] Implement primary provider adapter with timeout handling in `backend/src/llm/openai_provider.py`
- [ ] T028 [US2] Extend runtime provider selection and timeout configuration in `backend/src/config/settings.py`
- [ ] T029 [US2] Apply fallback classification and retry-safe session behavior in `backend/src/chat/service.py`
- [ ] T030 [US2] Render fallback state messaging in `frontend/src/chat/chat-app.js`

**Checkpoint**: At this point, User Stories 1 and 2 should both work independently

---

## Phase 5: User Story 3 - Keep Sarcasm Safe (Priority: P3)

**Goal**: Enforce refusal or neutralization for hateful or harassing content targeting protected characteristics while preserving bounded sarcasm elsewhere.

**Independent Test**: Submit unsafe prompts and confirm the API and UI return a refusal or neutralized response; submit a safe prompt afterward and confirm bounded sarcasm still works.

### Tests for User Story 3 (REQUIRED) ⚠️

- [ ] T031 [P] [US3] Add safety policy unit tests for protected-characteristic cases in `backend/tests/unit/test_safety_policy.py`
- [ ] T032 [P] [US3] Add safety refusal integration test in `backend/tests/integration/test_chat_safety.py`

### Implementation for User Story 3

- [ ] T033 [P] [US3] Extend moderation rules for refusal and neutralization decisions in `backend/src/safety/policy.py`
- [ ] T034 [US3] Apply refusal and neutralization classifications in `backend/src/chat/service.py`
- [ ] T035 [US3] Render refusal and neutralized states in `frontend/src/chat/chat-app.js`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finalize cross-story quality, docs, and validation support

- [ ] T036 [P] Add health endpoint contract coverage in `backend/tests/contract/test_health_api_contract.py`
- [ ] T037 [P] Add observability redaction tests in `backend/tests/unit/test_observability_logger.py`
- [ ] T038 [P] Document local setup and environment variables in `README.md`
- [ ] T039 [P] Record MVP quickstart verification notes in `frontend/tests/smoke/chat_mvp_smoke.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion and establishes the MVP slice
- **User Story 2 (Phase 4)**: Depends on Foundational completion and integrates with User Story 1 chat flow
- **User Story 3 (Phase 5)**: Depends on Foundational completion and extends User Story 1 chat flow with safety controls
- **Polish (Phase 6)**: Depends on the completion of all desired user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - no dependency on later stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) but assumes User Story 1 chat flow exists for fallback handling
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) but assumes User Story 1 chat flow exists for refusal and neutralization handling

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Backend policy and service logic precede API or UI wiring
- API route behavior precedes frontend UX polish
- Each story must end in a demonstrably testable slice before moving on

### Parallel Opportunities

- `T003`, `T004`, and `T005` can run in parallel during Setup
- `T007` through `T011` can run in parallel during Foundational because they touch separate files
- In User Story 1, `T016`, `T017`, and `T018` can run in parallel; `T019`, `T020`, `T021`, and `T022` can then run in parallel
- In User Story 2, `T025` and `T026` can run in parallel; `T027` can proceed in parallel with `T028`
- In User Story 3, `T031` and `T032` can run in parallel; `T033` can proceed before `T034` and `T035`
- In Polish, `T036`, `T037`, `T038`, and `T039` can run in parallel

---

## Parallel Example: User Story 1

```bash
Task: "Add POST /api/chat contract test in backend/tests/contract/test_chat_api_contract.py"
Task: "Add multi-turn API chat flow integration test in backend/tests/integration/test_chat_flow.py"
Task: "Add persona policy unit test for low/medium/high behavior in backend/tests/unit/test_persona_policy.py"

Task: "Implement browser API client for chat requests in frontend/src/services/chat_api.js"
Task: "Implement chat transcript UI and sarcasm level selector in frontend/src/chat/chat-app.js"
```

## Parallel Example: User Story 2

```bash
Task: "Add provider adapter timeout and error unit tests in backend/tests/unit/test_provider_adapter.py"
Task: "Add fallback API integration test in backend/tests/integration/test_chat_fallback.py"

Task: "Implement primary provider adapter with timeout handling in backend/src/llm/openai_provider.py"
Task: "Extend runtime provider selection and timeout configuration in backend/src/config/settings.py"
```

## Parallel Example: User Story 3

```bash
Task: "Add safety policy unit tests for protected-characteristic cases in backend/tests/unit/test_safety_policy.py"
Task: "Add safety refusal integration test in backend/tests/integration/test_chat_safety.py"

Task: "Extend moderation rules for refusal and neutralization decisions in backend/src/safety/policy.py"
Task: "Render refusal and neutralized states in frontend/src/chat/chat-app.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate the MVP chat flow end-to-end
5. Demo the core web chatbot before adding failure and safety hardening

### Incremental Delivery

1. Finish Setup + Foundational to establish shared contracts, persona assets, provider abstraction, and in-memory session state
2. Deliver User Story 1 as the first usable web chatbot slice
3. Add User Story 2 to harden the product against provider outages
4. Add User Story 3 to complete safety enforcement without changing the core chat workflow
5. Finish with Polish tasks and final quickstart validation

### Parallel Team Strategy

1. One developer handles backend platform tasks (`T006`-`T015`) while another completes frontend shell work (`T003`, `T005`)
2. For User Story 1, split backend chat/API work (`T019`, `T020`, `T023`) from frontend UI work (`T021`, `T022`, `T024`)
3. For User Story 2 and User Story 3, keep tests and backend policy work parallel before UI message-state updates

---

## Notes

- All tasks use the required checklist format: checkbox, task ID, optional `[P]`, required `[US#]` in story phases, and explicit file paths
- User Story 1 is the suggested MVP scope
- User Story 2 and User Story 3 build on the same chat flow without introducing auth, a database, or extra services
- Provider abstraction, persona assets, and in-memory session constraints are treated as foundational, blocking work
- The task list is ready for immediate execution by an implementation agent
