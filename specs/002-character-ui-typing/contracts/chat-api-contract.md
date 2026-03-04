# Chat API Contract (Unchanged)

Endpoint: `POST /api/chat`

## Request Body
```json
{
  "session_id": "optional-string",
  "message": "non-empty user message",
  "sarcasm_level": "low | medium | high"
}
```

## Response Body
```json
{
  "session_id": "string",
  "reply": "string",
  "classification": "normal | refused | neutralized | fallback",
  "sarcasm_level": "low | medium | high",
  "message_count": 1
}
```

## Contract Rules
- No new fields are introduced for this feature.
- Existing field semantics remain unchanged.
- Frontend typing reveal is strictly a client-side rendering behavior applied to `reply`.
