# Chat UI Behavior Contract

## Assistant Message Display Lifecycle
1. On submit, user message is appended immediately.
2. While waiting for `/api/chat`, UI shows typing indicator.
3. On successful response, assistant row enters `revealing` state:
   - progressively reveals words from `reply`,
   - exposes Skip control while reveal is active.
4. On Skip, remaining words render immediately and state becomes `complete`.

## Utility Controls
- **Quick prompt chips**: 4–6 predefined prompts available at all times.
- **Copy action**: available on assistant messages; copies full message text.
- **Reset chat**: clears transcript UI and restarts in-memory chat flow for subsequent requests.
- **Status badge**: rendered from response `classification` per assistant message.

## Error/Edge Behavior
- If request fails, an assistant fallback message is shown and state becomes `complete`.
- Repeated Skip presses are idempotent once message is `complete`.
- Reset during waiting/revealing cancels active reveal state and clears transcript.
