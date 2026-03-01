import { sendChatMessage } from "../services/chat_api.js";

export function mountChatApp(root) {
  let sessionId = null;

  root.innerHTML = `
    <section class="chat-shell">
      <label>
        Sarcasm level
        <select data-role="sarcasm-level">
          <option value="low">Low</option>
          <option value="medium" selected>Medium</option>
          <option value="high">High</option>
        </select>
      </label>
      <div data-role="transcript" aria-live="polite"></div>
      <form data-role="chat-form">
        <input
          type="text"
          name="message"
          placeholder="Ask something..."
          autocomplete="off"
          required
        />
        <button type="submit">Send</button>
      </form>
    </section>
  `;

  const transcript = root.querySelector('[data-role="transcript"]');
  const form = root.querySelector('[data-role="chat-form"]');
  const input = form?.querySelector('input[name="message"]');
  const sarcasmLevel = root.querySelector('[data-role="sarcasm-level"]');

  const appendMessage = (role, content, classification = "normal") => {
    if (!transcript) {
      return;
    }
    const item = document.createElement("p");
    const prefix = classification === "fallback" ? `${role} [fallback]` : role;
    item.textContent = `${prefix}: ${content}`;
    transcript.appendChild(item);
  };

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input?.value.trim();
    if (!message) {
      return;
    }

    appendMessage("You", message);
    input.value = "";

    try {
      const payload = await sendChatMessage({
        message,
        sarcasmLevel: sarcasmLevel?.value || "medium",
        sessionId,
      });
      sessionId = payload.session_id;
      appendMessage("SassyAI", payload.reply, payload.classification);
    } catch (error) {
      const messageText =
        error instanceof Error ? error.message : "Chat request failed.";
      appendMessage("SassyAI", messageText, "fallback");
    }
  });
}
