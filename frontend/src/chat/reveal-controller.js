export function createRevealController({
  text,
  onUpdate,
  onComplete,
  intervalMs = 75,
} = {}) {
  const words = String(text || "")
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  let currentIndex = 0;
  let timer = null;
  let completed = false;

  const complete = () => {
    if (completed) {
      return;
    }
    completed = true;
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    const fullText = words.join(" ");
    if (typeof onUpdate === "function") {
      onUpdate(fullText);
    }
    if (typeof onComplete === "function") {
      onComplete(fullText);
    }
  };

  const tick = () => {
    if (completed) {
      return;
    }
    currentIndex += 1;
    const visible = words.slice(0, currentIndex).join(" ");
    if (typeof onUpdate === "function") {
      onUpdate(visible);
    }
    if (currentIndex >= words.length) {
      complete();
    }
  };

  return {
    start() {
      if (completed) {
        return;
      }
      if (!words.length) {
        complete();
        return;
      }
      if (timer) {
        clearInterval(timer);
      }
      timer = setInterval(tick, intervalMs);
      tick();
    },
    skip() {
      complete();
    },
    stop() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
      completed = true;
    },
  };
}
