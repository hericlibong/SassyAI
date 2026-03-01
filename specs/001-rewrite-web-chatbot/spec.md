# Feature Specification: SassyAI V2 Web Chatbot MVP

**Feature Branch**: `001-rewrite-web-chatbot`  
**Created**: 2026-02-27  
**Status**: Draft  
**Input**: User description: "SassyAI V2 rewrite: build a web chatbot (frontend chat UI + backend
chat API) powered by an LLM. Core requirements: persona is the source of truth, sarcasm
calibration levels, safety refusals/neutralization, provider abstraction, robust fallback,
observability, and MVP scope limited to no auth, no database, in-memory conversation only."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start a Sarcastic Chat (Priority: P1)

A visitor opens the web chat, sends a message, and receives a sarcastic reply that matches the
selected tone while preserving the active conversation during the current session.

**Why this priority**: This is the core product value and the minimum usable V2 experience.

**Independent Test**: Open the chat, choose a sarcasm level, send an initial message, then send a
follow-up and confirm both replies appear in the same active conversation.

**Acceptance Scenarios**:

1. **Given** a visitor opens the chat page, **When** they send their first message, **Then** they
   receive a reply in the chat transcript without leaving the page.
2. **Given** an active conversation already contains prior messages, **When** the visitor sends a
   follow-up, **Then** the next reply reflects the current session context and stays in the same
   transcript.

---

### User Story 2 - Recover Gracefully from Provider Failure (Priority: P2)

A visitor continues using the chat even when the language model is slow or unavailable because the
product returns a safe fallback message instead of breaking the experience.

**Why this priority**: Reliability directly affects trust and keeps the MVP usable under degraded
conditions.

**Independent Test**: Simulate a provider timeout or error and confirm the visitor receives a safe
fallback reply and can immediately submit another message.

**Acceptance Scenarios**:

1. **Given** the language model provider times out or returns an error, **When** the visitor sends a
   message, **Then** the chat shows a safe fallback reply and remains ready for the next message.

---

### User Story 3 - Keep Sarcasm Safe (Priority: P3)

A visitor receives humor that stays within defined boundaries because hateful or harassing content
targeting protected characteristics is refused or neutralized before it reaches the chat transcript.

**Why this priority**: The product tone matters, but unsafe behavior creates unacceptable product
and trust risk.

**Independent Test**: Submit prompts that target protected characteristics and confirm the system
returns a refusal or neutralized response instead of abusive content.

**Acceptance Scenarios**:

1. **Given** a visitor submits hateful or harassing content targeting a protected characteristic,
   **When** the system evaluates the request, **Then** the product refuses or neutralizes the
   response before any unsafe content is shown.
2. **Given** a normal request that does not violate policy, **When** the system produces a response,
   **Then** the product keeps the sarcastic tone within the selected calibration level.

### Edge Cases

- A visitor submits an empty message or whitespace only.
- A visitor selects an unsupported sarcasm level.
- The active session is refreshed or lost and in-memory conversation history disappears.
- A request combines a valid question with unsafe hateful or harassing language.
- The provider fails after several messages in the same active conversation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The product MUST provide a web chat experience where visitors can send messages and
  receive replies in a single conversation view.
- **FR-002**: The product MUST preserve conversation context for the duration of the active session.
- **FR-003**: The product MUST offer three sarcasm calibration levels: low, medium, and high.
- **FR-004**: The product MUST apply the selected sarcasm calibration level consistently across
  replies in the same active session unless the visitor changes the level.
- **FR-005**: The product MUST use a versioned persona definition, including a canonical system
  prompt and optional example set, as the single source of truth for reply style.
- **FR-006**: The product MUST refuse or neutralize hateful or harassing content targeting
  protected characteristics before it is shown to the visitor.
- **FR-007**: The product MUST support switching among approved language model providers through
  configuration without changing the user-facing chat workflow.
- **FR-008**: The product MUST return a safe fallback message when the language model provider
  times out or fails, and the visitor MUST be able to continue chatting afterward.
- **FR-009**: The product MUST record chat latency and provider failure events without storing
  secrets or full prompts in default logs.
- **FR-010**: The MVP MUST not require user authentication.
- **FR-011**: The MVP MUST not require database-backed storage.
- **FR-012**: The MVP MUST limit conversation memory to the active in-memory session only.

### Key Entities *(include if feature involves data)*

- **Chat Session**: A visitor's active conversation state, including current transcript and selected
  sarcasm level for the current session only.
- **Chat Message**: A single user or assistant entry shown in the transcript, including content,
  speaker role, and sequence order.
- **Persona Profile**: The versioned definition of sarcastic behavior, including the canonical style
  rules and optional examples that shape replies.
- **Provider Setting**: The selected approved language model source used to generate replies for a
  given deployment.

## Assumptions

- The MVP serves unauthenticated visitors and supports one active conversation per browser session.
- Session history is intentionally transient and may be lost when the browser session ends or the
  service restarts.
- At least one approved language model provider is available at launch, and additional providers can
  be enabled later without changing the visitor workflow.

## Constitution Alignment *(mandatory)*

### Web Product Scope Impact

- Frontend chat UX impact: Introduces the primary V2 experience as a classic chat interface with a
  conversation transcript, message input, sarcasm level selection, and visible fallback or refusal
  states.
- Backend chat API impact: Introduces the server-side chat contract that accepts a visitor message,
  returns a reply, and preserves active-session context without requiring sign-in.
- CLI impact: None for new product scope; this feature establishes the web chatbot as the V2
  replacement path.

### Persona Prompt Governance

- Prompt assets updated: A canonical versioned persona definition and optional example set govern
  all sarcastic reply behavior.
- Persona consistency checks: All chat replies are evaluated against the same managed persona source
  so behavior changes are intentional and reviewable.
- Sarcasm calibration plan: Low, medium, and high levels are defined as distinct but bounded tone
  settings and are validated through scripted acceptance scenarios.

### Safety, Provider, and Reliability

- Safety handling: Requests or outputs that include hateful or harassing content targeting protected
  characteristics are blocked, refused, or neutralized before display.
- Provider abstraction impact: Approved language model providers can be swapped through
  configuration while preserving the same visitor experience and feature scope.
- Failure behavior: Provider timeouts and errors return a safe fallback reply, keep the chat usable,
  and never expose crash details to the visitor.
- Observability plan: Request latency and provider failures are captured for operations review while
  excluding secrets and full prompts from default logs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of test participants can open the chat, send a first message, and
  receive a reply within 30 seconds during acceptance testing.
- **SC-002**: In failure simulations, 100% of provider timeout and provider error cases return a
  safe fallback reply and allow the visitor to submit another message immediately.
- **SC-003**: In scripted safety tests, 100% of hateful or harassing prompts targeting protected
  characteristics are refused or neutralized before any unsafe content is shown.
- **SC-004**: In review sessions using a shared prompt set, evaluators correctly distinguish low,
  medium, and high sarcasm responses in at least 90% of cases without policy violations.
