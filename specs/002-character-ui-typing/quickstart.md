# Quickstart: Character UI Typing Upgrade

## Prerequisites
- Python environment with backend dependencies installed:
  - `pip install -r /home/hericdev/CHALLENGES/backend/requirements.txt`
- Provider environment variables set (same as existing backend setup).

## Run locally
1. Start backend:
   - `cd /home/hericdev/CHALLENGES/backend`
   - `uvicorn src.api.app:app --host 127.0.0.1 --port 8000 --reload`
2. Start frontend static host:
   - `cd /home/hericdev/CHALLENGES/frontend/src`
   - `python -m http.server 5173 --bind 127.0.0.1`
3. Open:
   - `http://127.0.0.1:5173/index.html`

## Validate feature behavior
1. Confirm updated Option B style chat shell appears with transcript and controls.
2. Send a prompt and verify:
   - typing indicator appears while awaiting backend response,
   - assistant message reveals word-by-word,
   - Skip immediately reveals full remaining text.
3. Verify utility controls:
   - quick prompt chips (4–6) trigger prompt flow,
   - copy button copies assistant message text,
   - reset clears transcript and starts fresh in-memory chat.
4. Verify status badge:
   - assistant messages display a badge mapped from `classification`.
5. Verify language behavior:
   - English prompt -> English reply,
   - French prompt -> French reply.

## Regression checks
1. Run backend tests:
   - `cd /home/hericdev/CHALLENGES/backend`
   - `pytest`
2. Confirm no contract regressions on `/api/chat`.
