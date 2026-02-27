# Quickstart: SassyAI V2 Web Chatbot MVP

## Goal

Validate the MVP implementation for the SassyAI V2 web chatbot with one backend service and one web frontend.

## Prerequisites

- Python 3.12 available locally.
- A configured provider selection in environment variables.
- Credentials present only for the selected provider.
- No database or authentication setup is required.

## Required Configuration

Set environment values before running the backend:

- `SASSYAI_LLM_PROVIDER`: Active provider identifier.
- `SASSYAI_MODEL_NAME`: Model name for the active provider.
- `SASSYAI_PROVIDER_TIMEOUT_SECONDS`: Timeout budget before fallback behavior.
- Provider-specific credentials for the chosen provider only.

The implementation must also load the persona assets from the versioned repository files under
`backend/persona/`.

## Run the MVP Locally

1. Start the backend service.
2. Open the web frontend.
3. Load the chat UI in a browser.
4. Send an initial message with sarcasm level set to `medium`.
5. Send a follow-up message and confirm the conversation continues in the same active session.

## Acceptance Validation

### Persona and Tone

1. Send the same neutral prompt using `low`, `medium`, and `high` sarcasm levels.
2. Confirm the replies remain recognizably different in tone while staying within policy.
3. Confirm the active persona behavior matches the versioned prompt assets rather than ad hoc copy.

### Safety

1. Send a prompt containing hateful or harassing content targeting a protected characteristic.
2. Confirm the UI shows a refusal or neutralized reply.
3. Confirm no unsafe content is shown verbatim as the assistant reply.

### Reliability

1. Simulate a provider timeout or provider error.
2. Confirm the chat returns a safe fallback reply.
3. Confirm the visitor can immediately send another message afterward.

## Test Suite Expectations

Run the automated tests before review:

1. Persona policy unit tests.
2. Provider adapter unit tests.
3. API-level chat flow integration tests.

All three suites must pass before the MVP is considered ready for implementation review.

## Observability Checks

1. Trigger at least one successful chat request and one provider failure.
2. Confirm logs include request latency and provider failure metadata.
3. Confirm logs do not include secrets.
4. Confirm logs do not include full prompt bodies by default.
