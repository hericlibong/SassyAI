import { sendChatMessage } from "../services/chat_api.js";

export function mountChatApp(root) {
  root.textContent = "SassyAI V2 chat shell";
  void sendChatMessage;
}
