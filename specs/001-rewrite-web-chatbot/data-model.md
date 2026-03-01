# Data Model: SassyAI V2 Web Chatbot MVP

## Chat Session

**Purpose**: Represents one active in-memory conversation for a browser session.

**Fields**:

- `session_id`: Unique ephemeral identifier for the active chat session.
- `sarcasm_level`: Current tone setting (`low`, `medium`, `high`).
- `messages`: Ordered list of chat messages in the session.
- `created_at`: Timestamp for session creation.
- `updated_at`: Timestamp for the most recent message or setting change.
- `status`: Session lifecycle state (`active`, `expired`).

**Validation Rules**:

- `session_id` MUST be present once a session exists.
- `sarcasm_level` MUST be one of `low`, `medium`, or `high`.
- `messages` MUST preserve insertion order.
- `status` MUST default to `active` and change to `expired` only when memory is cleared or the service restarts.

**Relationships**:

- One Chat Session contains many Chat Messages.
- One Chat Session references one active Persona Profile and one active Provider Setting at request time.

**State Transitions**:

- `active -> expired`: Triggered by memory eviction, restart, or explicit session reset.

## Chat Message

**Purpose**: Represents one message in the visible transcript.

**Fields**:

- `message_id`: Unique identifier within the session.
- `session_id`: Parent session reference.
- `role`: Message speaker (`user`, `assistant`, `system`).
- `content`: Text shown or processed for the message.
- `classification`: Outcome label (`normal`, `refused`, `neutralized`, `fallback`).
- `created_at`: Timestamp of message creation.

**Validation Rules**:

- `content` MUST contain non-empty text after trimming.
- `role` MUST be one of the allowed speaker values.
- `classification` MUST align with the response handling path.

**Relationships**:

- Many Chat Messages belong to one Chat Session.

## Persona Profile

**Purpose**: Defines the canonical sarcastic style rules used for every response.

**Fields**:

- `persona_version`: Repository-tracked version identifier for the active persona assets.
- `system_prompt_text`: Canonical prompt text loaded from the versioned prompt file.
- `example_set`: Optional set of example exchanges used to reinforce tone.
- `allowed_levels`: Supported sarcasm calibration values.
- `safety_rules`: Non-negotiable refusal or neutralization rules.

**Validation Rules**:

- `system_prompt_text` MUST come from the versioned prompt asset.
- `allowed_levels` MUST include exactly `low`, `medium`, and `high` for the MVP.
- `safety_rules` MUST explicitly prohibit hateful or harassing content targeting protected characteristics.

**Relationships**:

- One Persona Profile is applied across many Chat Sessions.

## Provider Setting

**Purpose**: Captures which approved LLM provider is active for the running deployment.

**Fields**:

- `provider_name`: Selected provider identifier.
- `model_name`: Active model designation for the selected provider.
- `timeout_seconds`: Maximum wait time before fallback behavior is triggered.
- `credentials_present`: Boolean indicator that required credentials are configured.
- `status`: Availability state (`ready`, `degraded`, `disabled`).

**Validation Rules**:

- `provider_name` MUST map to an approved adapter implementation.
- `timeout_seconds` MUST be greater than zero.
- `credentials_present` MUST be true before live provider calls are attempted.

**Relationships**:

- One Provider Setting can serve many Chat Sessions during a deployment.

## Chat Request / Chat Response

**Purpose**: Defines the external request and reply payloads for the chat API.

**Chat Request Fields**:

- `message`: The visitor's latest prompt.
- `sarcasm_level`: Desired tone for the reply.
- `session_id`: Optional existing session reference.

**Chat Response Fields**:

- `session_id`: Active session identifier.
- `reply`: Reply text returned to the frontend.
- `classification`: Result label (`normal`, `refused`, `neutralized`, `fallback`).
- `sarcasm_level`: Effective tone applied for the response.
- `message_count`: Total number of messages now stored in the session.

**Validation Rules**:

- `message` MUST reject empty or whitespace-only submissions.
- Missing `session_id` MUST create a new active session.
- `classification` MUST tell the frontend whether the reply is normal, safety-limited, or fallback-generated.
