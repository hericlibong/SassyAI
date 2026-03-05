import { sendChatMessage } from "../services/chat_api.js";
import { createRevealController } from "./reveal-controller.js";
import { renderSafeMarkdown } from "./render-markdown.js";
import { createTranscriptState } from "./transcript-state.js";

const BADGE_LABELS = {
  normal: "Normal",
  refused: "Refused",
  neutralized: "Neutralized",
  fallback: "Fallback",
};

const QUICK_PROMPTS = [
  "Give me a quick productivity tip.",
  "Explain this bug in plain English.",
  "Aide-moi a reformuler ce message en francais.",
  "What should I build this weekend?",
  "Share a sarcastic but safe roast about procrastination.",
];

export function mountChatApp(root) {
  let sessionId = null;
  const revealControllers = new Map();
  const transcriptState = createTranscriptState();

  root.innerHTML = `
    <section class="chat-shell chat-shell-option-b">
      <header class="chat-header">
        <div>
          <h1>SassyAI V2</h1>
          <p>Character chat, one session, zero persistence.</p>
        </div>
        <div class="chat-header-controls">
          <label class="chat-control">
            <span>Sarcasm level</span>
            <select data-role="sarcasm-level">
              <option value="low">Low</option>
              <option value="medium" selected>Medium</option>
              <option value="high">High</option>
            </select>
          </label>
          <button type="button" data-role="reset-chat" aria-label="Reset current chat">Reset chat</button>
        </div>
      </header>
      <div class="quick-prompts" data-role="quick-prompts" role="group" aria-label="Quick prompts"></div>
      <div data-role="transcript" role="log" aria-live="polite" aria-atomic="false" aria-label="Chat transcript"></div>
      <form data-role="chat-form" class="chat-form">
        <input
          type="text"
          name="message"
          placeholder="Ask something..."
          autocomplete="off"
          aria-label="Message input"
          required
        />
        <button type="submit" aria-label="Send message">Send</button>
      </form>
    </section>
  `;

  const transcript = root.querySelector('[data-role="transcript"]');
  const quickPrompts = root.querySelector('[data-role="quick-prompts"]');
  const form = root.querySelector('[data-role="chat-form"]');
  const input = form?.querySelector('input[name="message"]');
  const sarcasmLevel = root.querySelector('[data-role="sarcasm-level"]');
  const resetButton = root.querySelector('[data-role="reset-chat"]');

  const stopReveals = () => {
    for (const controller of revealControllers.values()) {
      controller.stop();
    }
    revealControllers.clear();
  };

  const renderQuickPrompts = () => {
    if (!quickPrompts) {
      return;
    }
    quickPrompts.innerHTML = "";
    QUICK_PROMPTS.forEach((prompt) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "prompt-chip";
      button.dataset.prompt = prompt;
      button.setAttribute("aria-label", `Use quick prompt: ${prompt}`);
      button.textContent = prompt;
      quickPrompts.appendChild(button);
    });
  };

  const createMessageNode = (entry) => {
    const item = document.createElement("article");
    item.className = `chat-message chat-message-${entry.role}`;
    item.dataset.messageId = entry.id;

    const messageHeader = document.createElement("header");
    messageHeader.className = "chat-message-header";

    const roleLabel = document.createElement("span");
    roleLabel.className = "chat-message-role";
    roleLabel.textContent = entry.role === "user" ? "You" : "SassyAI";
    messageHeader.appendChild(roleLabel);

    if (entry.role === "assistant") {
      const badge = document.createElement("span");
      badge.className = `chat-status-badge chat-status-${entry.classification}`;
      badge.textContent = BADGE_LABELS[entry.classification] || BADGE_LABELS.normal;
      messageHeader.appendChild(badge);
    }

    item.appendChild(messageHeader);

    const body = document.createElement("div");
    body.className = "chat-message-body";

    if (entry.role === "assistant" && entry.state === "waiting") {
      const typing = document.createElement("span");
      typing.className = "typing-indicator";
      typing.textContent = "SassyAI is typing";
      body.appendChild(typing);
    } else if (entry.role === "assistant" && entry.state === "complete") {
      body.classList.add("chat-markdown");
      body.innerHTML = renderSafeMarkdown(entry.displayText);
    } else {
      body.textContent = entry.displayText;
    }

    item.appendChild(body);

    if (entry.role === "assistant") {
      const actions = document.createElement("div");
      actions.className = "chat-message-actions";

      if (entry.state === "revealing") {
        const skip = document.createElement("button");
        skip.type = "button";
        skip.dataset.action = "skip";
        skip.dataset.messageId = entry.id;
        skip.setAttribute("aria-label", "Skip typing reveal");
        skip.textContent = "Skip";
        actions.appendChild(skip);
      }

      if (entry.state === "complete" && entry.displayText) {
        const copy = document.createElement("button");
        copy.type = "button";
        copy.dataset.action = "copy";
        copy.dataset.messageId = entry.id;
        copy.setAttribute("aria-label", "Copy assistant message");
        copy.textContent = "Copy";
        actions.appendChild(copy);
      }

      if (actions.children.length > 0) {
        item.appendChild(actions);
      }
    }

    return item;
  };

  const renderTranscript = () => {
    if (!transcript) {
      return;
    }
    transcript.innerHTML = "";
    transcriptState.getEntries().forEach((entry) => {
      transcript.appendChild(createMessageNode(entry));
    });
    transcript.scrollTop = transcript.scrollHeight;
  };

  const submitPrompt = async (message) => {
    transcriptState.addUserMessage(message);
    const pending = transcriptState.addAssistantPending();
    renderTranscript();

    try {
      const payload = await sendChatMessage({
        message,
        sarcasmLevel: sarcasmLevel?.value || "medium",
        sessionId,
      });
      sessionId = payload.session_id;
      transcriptState.setClassification(pending.id, payload.classification);
      const controller = createRevealController({
        text: payload.reply,
        onUpdate: (visibleText) => {
          transcriptState.setRevealText(pending.id, visibleText);
          renderTranscript();
        },
        onComplete: (fullText) => {
          transcriptState.completeAssistantMessage(pending.id, fullText);
          revealControllers.delete(pending.id);
          renderTranscript();
        },
      });
      revealControllers.set(pending.id, controller);
      controller.start();
    } catch (error) {
      const messageText =
        error instanceof Error ? error.message : "Chat request failed.";
      transcriptState.failAssistantMessage(pending.id, messageText);
      revealControllers.delete(pending.id);
      renderTranscript();
    }
  };

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input?.value.trim();
    if (!message) {
      return;
    }
    if (input) {
      input.value = "";
    }
    await submitPrompt(message);
  });

  quickPrompts?.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    const prompt = target.dataset.prompt;
    if (!prompt || !input) {
      return;
    }
    input.value = prompt;
    form?.requestSubmit();
  });

  transcript?.addEventListener("click", async (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    const action = target.dataset.action;
    const messageId = target.dataset.messageId;
    if (!messageId) {
      return;
    }
    if (action === "skip") {
      revealControllers.get(messageId)?.skip();
      return;
    }
    if (action === "copy") {
      const entry = transcriptState.getEntries().find((item) => item.id === messageId);
      if (!entry || !entry.displayText) {
        return;
      }
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(entry.displayText);
      }
    }
  });

  resetButton?.addEventListener("click", () => {
    stopReveals();
    sessionId = null;
    transcriptState.reset();
    renderTranscript();
    input?.focus();
  });

  renderQuickPrompts();
  renderTranscript();
}
