function now() {
  return Date.now();
}

function createId(role) {
  return `${role}-${Math.random().toString(36).slice(2, 10)}`;
}

export function createTranscriptState() {
  const entries = [];

  const findEntry = (id) => entries.find((entry) => entry.id === id);

  return {
    addUserMessage(content) {
      const entry = {
        id: createId("user"),
        role: "user",
        fullText: content,
        displayText: content,
        classification: "normal",
        state: "complete",
        createdAt: now(),
      };
      entries.push(entry);
      return entry;
    },
    addAssistantPending() {
      const entry = {
        id: createId("assistant"),
        role: "assistant",
        fullText: "",
        displayText: "",
        classification: "normal",
        state: "waiting",
        createdAt: now(),
      };
      entries.push(entry);
      return entry;
    },
    setClassification(id, classification) {
      const entry = findEntry(id);
      if (entry) {
        entry.classification = classification || "normal";
      }
      return entry;
    },
    setRevealText(id, text) {
      const entry = findEntry(id);
      if (entry) {
        entry.displayText = text;
        entry.state = "revealing";
      }
      return entry;
    },
    completeAssistantMessage(id, text) {
      const entry = findEntry(id);
      if (entry) {
        entry.fullText = text;
        entry.displayText = text;
        entry.state = "complete";
      }
      return entry;
    },
    failAssistantMessage(id, text) {
      const entry = findEntry(id);
      if (entry) {
        entry.fullText = text;
        entry.displayText = text;
        entry.classification = "fallback";
        entry.state = "complete";
      }
      return entry;
    },
    getEntries() {
      return entries;
    },
    reset() {
      entries.length = 0;
    },
  };
}
