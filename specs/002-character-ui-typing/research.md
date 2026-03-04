# Phase 0 Research: Character UI Typing Upgrade

## Decision 1: Keep `/api/chat` contract unchanged and implement reveal entirely client-side
- **Decision**: Preserve the existing request/response JSON shape and run word-by-word reveal using frontend-only display state.
- **Rationale**: The feature explicitly disallows backend streaming and contract changes; client-side simulation satisfies UX goals without API risk.
- **Alternatives considered**:
  - Add streaming endpoint: rejected because it violates constraints.
  - Add reveal metadata fields to API response: rejected because it changes contract for no functional backend need.

## Decision 2: Model assistant message display as transient UI states
- **Decision**: Use explicit UI states per assistant message (`waiting` → `revealing` → `complete`) with an interruptible Skip action.
- **Rationale**: A stateful render flow gives deterministic handling for skip, copy, and reset edge cases.
- **Alternatives considered**:
  - Timer-based global reveal outside message state: rejected due to race-condition risk across multiple responses.
  - Immediate full render plus CSS animation only: rejected because Skip and progressive content control would be unreliable.

## Decision 3: Language consistency via minimal prompt guidance in existing backend flow
- **Decision**: Add or refine a developer-style instruction in the existing prompt construction so replies follow the user message language (FR/EN) per turn.
- **Rationale**: This satisfies consistency requirements while preserving provider abstraction and endpoint schema.
- **Alternatives considered**:
  - Frontend-only translation hints: rejected because backend model behavior remains the source of actual reply language.
  - New explicit `language` API field: rejected because contract must remain unchanged.

## Decision 4: Reuse existing classification output for status badge rendering
- **Decision**: Render a concise UI badge from existing `classification` values (`normal`, `refused`, `neutralized`, `fallback`) returned by `/api/chat`.
- **Rationale**: No backend schema changes are needed; existing semantics already map to user-facing status cues.
- **Alternatives considered**:
  - Add separate badge field from backend: rejected as unnecessary contract change.
  - Infer status only from reply text: rejected as brittle and non-deterministic.

## Decision 5: Validate with existing backend tests plus focused manual frontend checks
- **Decision**: Run current backend pytest suite for regression safety and execute quickstart scenario checks for UI behavior.
- **Rationale**: Backend test coverage already protects contract and chat flow; frontend currently has no automated harness in this repository.
- **Alternatives considered**:
  - Introduce new frontend test framework in this feature: rejected as out of scope for a UI behavior upgrade.
