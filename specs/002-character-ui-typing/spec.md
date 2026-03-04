# Feature Specification: Character UI Typing Upgrade

**Feature Branch**: `002-character-ui-typing`  
**Created**: 2026-03-04  
**Status**: Draft  
**Input**: User description: "Upgrade the frontend chat UI to a character-driven Option B portfolio look, and add word-by-word typing reveal for AI replies (client-side simulation, no backend streaming). Keep `/api/chat` contract unchanged, keep single-page MVP constraints (no auth, no DB, in-memory only), add typing indicator + skip, quick prompt chips, AI message copy, reset chat, classification status badge, and improve FR/EN response-language consistency."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Polished Character Chat Experience (Priority: P1)

A visitor opens the chat page and experiences a product-grade, character-driven interface that feels intentional and modern while still being simple to use in a single page.

**Why this priority**: Visual quality and clarity are the primary user-facing goal of this feature and define whether the upgrade is successful.

**Independent Test**: Load the chat page and verify the upgraded layout, message styling, controls, and status badge are all visible and usable without changing any backend behavior.

**Acceptance Scenarios**:

1. **Given** a visitor opens the chat page, **When** the page renders, **Then** the interface reflects the new character-driven Option B design language with clearly separated input, transcript, and actions.
2. **Given** there is a chat classification result for a reply, **When** the assistant message appears, **Then** a status badge is shown in the message area for that reply.

---

### User Story 2 - Simulated Live Reply Reveal (Priority: P1)

A visitor sends a message and sees a typing indicator while waiting; once a full assistant response is received, the text appears word-by-word to simulate live generation, with an option to skip and reveal immediately.

**Why this priority**: This interaction change is the core behavioral requirement and central to the perceived responsiveness of the chat.

**Independent Test**: Send a prompt and confirm the waiting indicator appears, then verify the assistant response reveals word-by-word and the Skip control immediately reveals the remaining text.

**Acceptance Scenarios**:

1. **Given** a visitor sends a valid message, **When** the system is waiting for the assistant response, **Then** a typing indicator is displayed until the response is ready to reveal.
2. **Given** the assistant response reveal is in progress, **When** the visitor selects Skip, **Then** the full remaining assistant message is shown immediately in the same message bubble.
3. **Given** a visitor sends multiple messages in sequence, **When** each response is returned, **Then** each response follows the same reveal behavior without blocking subsequent interactions.

---

### User Story 3 - Faster Repeat Interactions (Priority: P2)

A visitor can quickly continue or restart conversations through prompt chips, copy assistant replies, and reset the current chat transcript.

**Why this priority**: These controls improve usability and perceived quality, but the product remains functional without them.

**Independent Test**: Use each utility control once (prompt chip, copy, reset) and verify each action produces the expected user-visible result.

**Acceptance Scenarios**:

1. **Given** the visitor sees quick prompt chips, **When** one chip is selected, **Then** its text is inserted and submitted (or ready to submit) as a new prompt flow.
2. **Given** an assistant message is visible, **When** the visitor uses the copy action, **Then** the full assistant message content is copied for external use.
3. **Given** the chat contains prior messages, **When** the visitor selects reset chat, **Then** the transcript clears and a fresh in-memory conversation state is started.

### Edge Cases

- The visitor clicks Skip before any reveal begins.
- The visitor clicks Skip repeatedly during an active reveal.
- The assistant response contains very short or very long text.
- Copy action is triggered on a message still revealing.
- Reset chat is triggered while a response is waiting or revealing.
- Quick prompt chips are used immediately after reset.
- User input language switches between French and English across consecutive turns.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The product MUST present a character-driven, portfolio-style single-page chat interface aligned with the requested Option B visual direction.
- **FR-002**: The product MUST keep the existing `/api/chat` request and response contract unchanged.
- **FR-003**: The product MUST display a typing indicator whenever a user message has been sent and a corresponding assistant response is still pending.
- **FR-004**: After a full assistant response is received, the product MUST reveal that response incrementally word-by-word in the chat transcript.
- **FR-005**: The product MUST provide a Skip control during incremental reveal so users can immediately show the remaining response text.
- **FR-006**: The product MUST include 4 to 6 quick prompt chips that help users start or continue common prompts.
- **FR-007**: Each assistant message MUST provide a copy action that copies that message content.
- **FR-008**: The product MUST provide a reset chat action that clears the visible transcript and reinitializes in-memory conversation context.
- **FR-009**: The product MUST display a status badge derived from the available classification result for each applicable assistant response.
- **FR-010**: The product MUST keep conversation state transient and in-memory only, with no authentication, no database-backed persistence, and no multi-page workflow introduced by this feature.
- **FR-011**: The product MUST produce assistant replies in the user’s active language (French or English), using the existing flow with only minimal behavior adjustments required to improve consistency.
- **FR-012**: The feature MUST not introduce regressions to existing backend behavior validated by the current backend automated tests.

### Key Entities *(include if feature involves data)*

- **Chat Transcript Entry**: A user or assistant message shown in order, including role, content, and display state (pending, revealing, complete).
- **Reveal Session**: The temporary state controlling word-by-word rendering for one assistant response, including progress and skip state.
- **Quick Prompt Chip**: A predefined suggested prompt item available from the chat UI for faster input.
- **Classification Status Badge**: A concise label attached to an assistant response to communicate its classification outcome.

## Assumptions

- The Option B reference is an approved visual direction available to the team and does not require redefining product scope.
- Existing classification output already provides enough information to derive a user-visible status badge label.
- Language consistency improvements can be achieved without changing the public backend API contract.
- Clipboard functionality uses standard browser capabilities available to supported users.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In stakeholder review, at least 90% of evaluators rate the updated chat interface as clearly more polished and production-ready than the prior version.
- **SC-002**: In acceptance testing, 100% of assistant replies show a visible waiting state before reveal and then display progressive word-by-word rendering.
- **SC-003**: In acceptance testing, Skip reveals the full remaining assistant response in under 1 second for at least 95% of tested replies.
- **SC-004**: In scripted bilingual testing, at least 95% of replies match the user’s input language (French or English) for the same turn.
- **SC-005**: Existing backend automated tests complete with no new failures after this feature is integrated.
