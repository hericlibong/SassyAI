import { mountChatApp } from "../chat/chat-app.js";

const root = document.getElementById("app");

if (root) {
  mountChatApp(root);
}
