# Tasks: Character UI Typing Upgrade

**Input**: Design documents from `/specs/002-character-ui-typing/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Include targeted backend regression tests and a final backend pytest run as required by spec.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`)
- All tasks include exact file paths

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare baseline files and implementation scaffolding for this feature.

- [ ] T001 Review and align feature documentation references in specs/002-character-ui-typing/quickstart.md
- [ ] T002 Create frontend typing/reveal helper module in frontend/src/chat/reveal-controller.js
- [ ] T003 [P] Create frontend transcript state helper module in frontend/src/chat/transcript-state.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core changes that block all user stories.

**⚠️ CRITICAL**: Complete this phase before starting user story implementation.

- [ ] T004 Refactor chat shell composition and shared rendering entrypoints in frontend/src/chat/chat-app.js
- [ ] T005 Add shared message status badge mapping utility in frontend/src/chat/chat-app.js
- [ ] T006 Add language-consistency prompt guidance in backend/src/chat/service.py
- [ ] T007 Add backend unit coverage for updated prompt-language guidance in backend/tests/unit/test_persona_policy.py

**Checkpoint**: Foundation ready; user stories can be implemented.

---

## Phase 3: User Story 1 - Polished Character Chat Experience (Priority: P1) 🎯 MVP

**Goal**: Deliver Option B product-grade character chat presentation with clear transcript/actions and classification badge display.

**Independent Test**: Load UI and confirm upgraded layout, controls, and assistant status badges render without backend contract changes.

### Implementation for User Story 1

- [ ] T008 [US1] Implement Option B chat shell markup (header/body/actions regions) in frontend/src/chat/chat-app.js
- [ ] T009 [US1] Implement product-grade Option B styling tokens/layout for shell, transcript, and controls in frontend/src/styles.css
- [ ] T010 [US1] Render classification status badges for assistant messages using existing classification values in frontend/src/chat/chat-app.js
- [ ] T011 [US1] Verify `/api/chat` payload consumption remains unchanged in frontend/src/services/chat_api.js

**Checkpoint**: US1 is independently functional and demoable.

---

## Phase 4: User Story 2 - Simulated Live Reply Reveal (Priority: P1)

**Goal**: Add waiting indicator, word-by-word reveal flow, and Skip behavior for assistant responses.

**Independent Test**: Send prompt, observe waiting indicator, confirm progressive reveal, then Skip to immediate full response.

### Tests for User Story 2

- [ ] T012 [US2] Add integration test coverage for unchanged chat response contract after reveal-related frontend/backend updates in backend/tests/contract/test_chat_api_contract.py

### Implementation for User Story 2

- [ ] T013 [US2] Implement pending assistant placeholder and typing indicator state transitions in frontend/src/chat/chat-app.js
- [ ] T014 [US2] Implement word-by-word reveal engine (start/advance/complete) in frontend/src/chat/reveal-controller.js
- [ ] T015 [US2] Integrate reveal engine with transcript message state (`waiting` -> `revealing` -> `complete`) in frontend/src/chat/transcript-state.js
- [ ] T016 [US2] Implement Skip action wiring and idempotent completion behavior in frontend/src/chat/chat-app.js
- [ ] T017 [US2] Add reveal/typing visual states and Skip control styling in frontend/src/styles.css

**Checkpoint**: US2 independently delivers live-feel response rendering with Skip.

---

## Phase 5: User Story 3 - Faster Repeat Interactions (Priority: P2)

**Goal**: Add quick prompt chips, copy assistant response, and reset chat flow.

**Independent Test**: Use one prompt chip, copy one assistant message, reset transcript, and verify fresh conversation behavior.

### Implementation for User Story 3

- [ ] T018 [US3] Add 4-6 quick prompt chips and event handling in frontend/src/chat/chat-app.js
- [ ] T019 [US3] Implement assistant message copy action using Clipboard API in frontend/src/chat/chat-app.js
- [ ] T020 [US3] Implement reset chat behavior that clears transcript and resets session flow in frontend/src/chat/chat-app.js
- [ ] T021 [US3] Add prompt chip, copy button, and reset control styles in frontend/src/styles.css

**Checkpoint**: US3 utilities work independently without persistence/auth changes.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, regression validation, and documentation updates across stories.

- [ ] T022 [P] Align frontend accessibility labels/ARIA for new controls and indicators in frontend/src/chat/chat-app.js
- [ ] T023 [P] Update frontend usage notes to reflect new chat controls and reveal behavior in README.md
- [ ] T024 Run backend regression suite and confirm no failures in backend/tests/
- [ ] T025 Execute quickstart validation steps and record any mismatches in specs/002-character-ui-typing/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1 completion; blocks all user stories.
- **Phase 3 (US1)**: Depends on Phase 2.
- **Phase 4 (US2)**: Depends on Phase 2; can proceed after foundational completion and may run alongside US1 if staffed.
- **Phase 5 (US3)**: Depends on Phase 2; can proceed after foundational completion and may run alongside US1/US2 if staffed.
- **Phase 6 (Polish)**: Depends on completion of selected user stories.

### User Story Dependencies

- **US1 (P1)**: No dependency on other user stories.
- **US2 (P1)**: No strict dependency on US1; shares frontend shell/rendering entrypoints from foundational phase.
- **US3 (P2)**: No strict dependency on US1/US2; integrates with common transcript/session behavior.

### Within Each User Story

- Implement rendering/state foundations before control wiring.
- Validate story independently against its independent test criteria.
- Keep `/api/chat` contract unchanged across all stories.

### Parallel Opportunities

- `T002` and `T003` can run in parallel (separate helper modules).
- In Phase 6, `T022` and `T023` can run in parallel (different files).
- After Phase 2, US1/US2/US3 can be staffed in parallel with coordination on `frontend/src/chat/chat-app.js`.

---

## Parallel Example: User Story 2

```bash
# Parallelizable prep if separate contributors are available:
Task: "Implement word-by-word reveal engine in frontend/src/chat/reveal-controller.js"   # T014
Task: "Integrate reveal message state model in frontend/src/chat/transcript-state.js"     # T015
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate US1 independently before expanding scope.

### Incremental Delivery

1. Deliver US1 (visual/product quality baseline).
2. Deliver US2 (typing/reveal/skip interaction).
3. Deliver US3 (chips/copy/reset productivity features).
4. Finish with Phase 6 regression and quickstart validation.

### Parallel Team Strategy

1. One developer handles backend prompt-language and regression test tasks (`T006`, `T007`, `T012`, `T024`).
2. One developer handles UI styling/layout tasks (`T009`, `T017`, `T021`).
3. One developer handles interaction logic tasks (`T013`, `T014`, `T016`, `T018`-`T020`).
