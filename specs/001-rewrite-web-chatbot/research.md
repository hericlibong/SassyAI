# Research: SassyAI V2 Web Chatbot MVP

## Decision 1: Use Python 3.12 for the backend runtime

- **Decision**: Implement the backend service in Python 3.12.
- **Rationale**: The existing repository is already Python-based, which reduces migration overhead and keeps the MVP aligned with current project skills and tooling.
- **Alternatives considered**:
  - Node.js: viable for web APIs but would add a second primary runtime during the rewrite.
  - Go: lightweight and fast but introduces a larger stack shift than the MVP needs.

## Decision 2: Use a minimal HTTP web framework for the backend API

- **Decision**: Use a minimal Python web framework centered on typed request and response models (FastAPI-class approach).
- **Rationale**: The feature needs one chat API, simple health checking, clear schemas, and straightforward testability. A lightweight typed API framework keeps the surface small and reviewable.
- **Alternatives considered**:
  - Flask: simpler but requires more manual schema and validation handling.
  - Django: too broad for a no-auth, no-database MVP.

## Decision 3: Keep the frontend as a minimal web UI without a heavy SPA framework

- **Decision**: Build the frontend as a classic chat interface using standard web assets (HTML, CSS, and browser JavaScript) in a dedicated `frontend/` directory.
- **Rationale**: The MVP needs a small chat interface, not a full application shell. Avoiding a heavy frontend framework keeps the rewrite focused on the product workflow rather than build complexity.
- **Alternatives considered**:
  - React or Vue: useful for larger apps but unnecessary for the first MVP slice.
  - Server-rendered templating only: workable, but a small client-side layer keeps chat updates simpler without introducing a second service.

## Decision 4: Persist conversation state in memory keyed by an ephemeral session identifier

- **Decision**: Keep one active chat session in backend memory, addressed by an ephemeral session identifier carried between frontend and backend.
- **Rationale**: This satisfies the no-database constraint while preserving multi-message context for the active browser session.
- **Alternatives considered**:
  - Database-backed storage: explicitly out of scope for the MVP.
  - Stateless single-turn chat: simpler, but it violates the requirement to preserve active-session conversation context.

## Decision 5: Store the canonical persona as versioned repository assets

- **Decision**: Store the persona in a committed `system_prompt.md` file, with optional few-shot examples in a separate versioned companion file.
- **Rationale**: The constitution requires the persona prompt to be the source of truth and reviewable in diffs. Separate files make behavioral changes explicit.
- **Alternatives considered**:
  - Inline persona strings in application code: too easy to duplicate and drift.
  - Environment-only persona configuration: not reviewable enough for the source-of-truth requirement.

## Decision 6: Enforce safety with explicit refusal or neutralization rules around generation

- **Decision**: Apply safety checks that block or neutralize hateful or harassing content targeting protected characteristics before unsafe output reaches the user.
- **Rationale**: The feature promises a sarcastic persona, but the constitution and spec require firm safety boundaries. Explicit refusal logic keeps the MVP deterministic and testable.
- **Alternatives considered**:
  - Trust provider safety alone: insufficient because provider behavior can vary.
  - Post-response moderation only: weaker than validating both request and candidate output paths.

## Decision 7: Use a provider adapter interface selected through environment variables

- **Decision**: Define one provider adapter contract and select the active provider through environment variables.
- **Rationale**: This keeps the API stable while allowing OpenAI first and Mistral/Gemini later without route rewrites.
- **Alternatives considered**:
  - Hard-code a single provider: simplest initially, but violates the pluggable-provider requirement.
  - Add multiple provider-specific routes: increases API surface without user benefit.

## Decision 8: Log latency and provider failures with redaction by default

- **Decision**: Record request timing and provider error metadata, but exclude secrets and full prompt bodies from default logs.
- **Rationale**: The MVP needs operational visibility without leaking sensitive inputs or credentials.
- **Alternatives considered**:
  - Full request/response logging: easier to debug but violates the observability requirements.
  - No operational logs: too opaque when provider failures occur.

## Decision 9: Test the MVP with focused unit and API integration coverage

- **Decision**: Cover persona policy, provider adapter behavior, and end-to-end API chat flow with pytest.
- **Rationale**: These are the constitution-mandated minimums and directly protect the highest-risk behavior.
- **Alternatives considered**:
  - UI-only manual testing: too weak for behavior that must remain stable.
  - Full browser automation in the MVP: potentially useful later, but heavier than needed for the first implementation slice.
