
# SassyAI V2 — The Sarcastic Web Chatbot (LLM)

<p align="center">
  <img src="media/sassy_ai_picture.png" alt="SassyAI" width="520" />
</p>

SassyAI V2 is a **single-page web chatbot** with a sarcastic personality, powered by an LLM (OpenAI) and a versioned persona. It’s built as a clean portfolio project: **simple UI, real model, real UX polish**.

---

## What is SassyAI V2?

- **Web chat UI** (frontend static app) + **FastAPI backend**
- **LLM-backed sarcasm** with selectable levels: low / medium / high
- **Versioned persona** (`backend/persona/`) to control tone and consistency
- Built-in **safety**, **fallback**, and **provider abstraction**

---

## Features (V2)

### Chat experience (UI Option B)
- Product-style “character” UI (header + chips + clean transcript)
- Typing indicator while waiting for the backend
- Word-by-word assistant reveal with **Skip**
- Quick prompt chips (4–6)
- Per-message **Copy**
- **Reset chat**
- Classification badge per assistant message (normal / fallback / etc.)
- Brand logo in header + assistant avatar in chat

### Backend (FastAPI)
- `/api/chat` endpoint (simple JSON contract)
- Provider abstraction (registry)
- OpenAI **Responses API** integration (HTTP via `httpx`)
- Safety policy short-circuit (refuse/neutralize without calling the model)
- Fallback behavior on provider errors/timeouts

---

## Architecture

```text
backend/
  src/
    api/            # FastAPI app + routes
    chat/           # ChatService, session store, prompt assembly
    llm/            # Provider registry + OpenAI provider
    safety/         # Refuse/neutralize policy
  persona/
    system_prompt.md
    few_shot_examples.yaml

frontend/
  src/
    index.html
    styles.css
    chat/
      chat-app.js
      reveal-controller.js
      transcript-state.js
    services/
      chat_api.js
    assets/
      sassy_pic.png
````

**Persona governance**

* `backend/persona/system_prompt.md` is the base persona.
* `backend/persona/few_shot_examples.yaml` anchors tone with examples.
* Sarcasm level is enforced through a dedicated instruction.

---

## Run locally

### Prerequisites

* Python 3.12+
* A working OpenAI API key

### 1) Backend setup

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2) Backend environment variables

Create `backend/.env` (do NOT commit it):

```bash
SASSYAI_LLM_PROVIDER=openai
SASSYAI_MODEL_NAME=gpt-4o-mini
SASSYAI_PROVIDER_TIMEOUT_SECONDS=10
SASSYAI_OPENAI_API_KEY=replace-me
```

> Keep your API key private. Never place it in frontend code.

### 3) Run backend

```bash
cd backend
uvicorn src.api.app:app --host 127.0.0.1 --port 8000 --reload
```

### 4) Run frontend (static)

```bash
cd frontend/src
python -m http.server 5173 --bind 127.0.0.1
```

Open:

* `http://127.0.0.1:5173/index.html`

---

## Configuration

### Provider + model

SassyAI V2 is configured via environment variables:

* `SASSYAI_LLM_PROVIDER` (default: `openai`)
* `SASSYAI_MODEL_NAME` (example: `gpt-4o-mini`)
* `SASSYAI_PROVIDER_TIMEOUT_SECONDS` (example: `10`)
* `SASSYAI_OPENAI_API_KEY` (required)

### Persona files (versioned)

* `backend/persona/system_prompt.md`
* `backend/persona/few_shot_examples.yaml`

Updating these files changes the assistant’s behavior in a traceable way (git diff).

---

## Testing

Backend tests:

```bash
cd backend
pytest -q
```

---

## Deployment note (Hugging Face)

This repo currently runs as:

* **Backend**: FastAPI service (needs a runtime that can expose an HTTP API)
* **Frontend**: static assets served by a simple HTTP server

For Hugging Face:

* Store your API key as a **Secret** (never in git)
* Ensure the backend is reachable by the frontend (same Space or configured URL)
* If you deploy as a Space, you’ll likely serve both:

  * the FastAPI app
  * and the static frontend assets

(We’ll prepare a deployment-specific guide next.)

---

## Legacy CLI (Deprecated)

The original version of SassyAI was a CLI assistant built for the **Amazon Q Developer – Quack the Code** challenge. It’s kept for reference only.

Run legacy CLI:

```bash
python sassy_ai/main_cli.py
```

V2 development is governed by `.specify/memory/constitution.md` and focuses on the web chatbot.

---

## Origins (Amazon Q Challenge)

SassyAI started as a playful experiment during the Amazon Q challenge: generate sarcastic responses and ship an interactive experience fast.
V2 is the portfolio-grade rewrite: **real model provider, web UI, versioned persona, and clean architecture.**

---

## Contributing

PRs and issues are welcome. Please follow the engineering governance in:

* `.specify/memory/constitution.md`

---

## License

MIT

```
