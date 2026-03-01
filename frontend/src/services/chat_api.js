const CHAT_API_PATH = "http://127.0.0.1:8000/api/chat";

export async function sendChatMessage({ message, sarcasmLevel, sessionId } = {}) {
  const response = await fetch(CHAT_API_PATH, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      sarcasm_level: sarcasmLevel,
      session_id: sessionId,
    }),
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.message || "Chat request failed.");
  }

  return payload;
}
