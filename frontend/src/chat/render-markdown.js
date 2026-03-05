import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import DOMPurify from "https://cdn.jsdelivr.net/npm/dompurify@3.1.7/dist/purify.es.mjs";

marked.setOptions({
  gfm: true,
  breaks: true,
});

export function renderSafeMarkdown(markdownText) {
  const unsafeHtml = marked.parse(String(markdownText || ""));
  return DOMPurify.sanitize(unsafeHtml, {
    USE_PROFILES: { html: true },
    FORBID_TAGS: ["script", "style", "iframe", "object", "embed", "link", "meta"],
    FORBID_ATTR: ["style"],
  });
}
