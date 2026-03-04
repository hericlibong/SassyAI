# Data Model: Character UI Typing Upgrade

## 1) ChatTranscriptEntry
- **Purpose**: Represents one rendered message row in the frontend transcript.
- **Fields**:
  - `id` (string, required): Stable UI identifier.
  - `role` (enum: `user` | `assistant`, required)
  - `fullText` (string, required): Complete message payload.
  - `displayText` (string, required): Current visible text (progressive during reveal).
  - `classification` (enum: `normal` | `refused` | `neutralized` | `fallback`, default `normal`)
  - `state` (enum: `waiting` | `revealing` | `complete`, required for assistant rows)
  - `createdAt` (number/timestamp, required)
- **Validation rules**:
  - User entries are always `complete` on insertion.
  - Assistant entries begin as `waiting`, then become `revealing` and finally `complete`.
  - `displayText` must never exceed `fullText`.

## 2) RevealSession
- **Purpose**: Tracks progressive rendering lifecycle for a single assistant reply.
- **Fields**:
  - `messageId` (string, required): Linked assistant message entry.
  - `words` (array<string>, required): Tokenized assistant reply.
  - `currentWordIndex` (integer, min 0)
  - `isSkipped` (boolean, default false)
  - `intervalHandle` (runtime timer reference, nullable)
- **State transitions**:
  - `initialized` (implicit) -> `revealing` when response arrives.
  - `revealing` -> `complete` when all words emitted.
  - `revealing` -> `complete` immediately when `isSkipped=true`.

## 3) QuickPromptChip
- **Purpose**: Provides predefined high-value prompts for fast user interaction.
- **Fields**:
  - `id` (string, required)
  - `label` (string, required)
  - `prompt` (string, required, non-empty)
  - `languageHint` (enum: `fr` | `en` | `neutral`, optional)
- **Validation rules**:
  - Feature must expose 4–6 chips.
  - Prompt text must be submit-ready without backend schema changes.

## 4) BackendChatContract (existing, unchanged)
- **Purpose**: Existing API payload used by frontend behavior.
- **Request fields**:
  - `session_id` (optional string)
  - `message` (non-empty string)
  - `sarcasm_level` (`low` | `medium` | `high`)
- **Response fields**:
  - `session_id` (string)
  - `reply` (non-empty string)
  - `classification` (`normal` | `refused` | `neutralized` | `fallback`)
  - `sarcasm_level` (`low` | `medium` | `high`)
  - `message_count` (integer >= 1)
