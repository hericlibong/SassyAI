import { mountChatApp } from "../chat/chat-app.js";

const root = document.getElementById("app");

if (root) {
  document.body.classList.add("sassyai-ready");
  mountChatApp(root);
}
