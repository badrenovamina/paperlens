# PaperLens — Extension Scaffold (v0.1, mocked backend)

This is a working Chrome/Edge (Manifest V3) extension shell that does the
part that has to run in the browser: detect a highlighted selection, show
an "Explain" button, and open a popup panel. The backend call is currently
**mocked** in `background.js` so you can see the entire UI flow before any
real server or Claude API integration exists.

## How to load it and try it

1. Open `chrome://extensions` (or `edge://extensions` in Edge).
2. Turn on **Developer mode** (top right toggle).
3. Click **Load unpacked**, and select this `paperlens-extension` folder.
4. Visit any normal page — start with something simple like a Wikipedia
   article, not a research site yet, since some research sites have
   stricter page security policies that are worth debugging separately
   from your core UI logic.
5. Highlight a sentence of at least ~12 characters. An "▶ Explain" button
   should appear just below your selection.
6. Click it. A panel opens, shows "Finding the best explanation…" for
   about a second, then shows a result.
7. Try highlighting text containing the word **"osmosis"**, **"mitosis"**,
   or **"transcription"** — you'll get the mocked "video" response
   (it won't actually play, since `videoUrl` points to a placeholder).
   Any other text gives you the mocked text-fallback response.

## What's real vs. mocked right now

**Real (built):**
- Selection detection and button placement
- Popup panel open/close, loading state, result rendering (video or text)
- Message-passing architecture: content script → background service worker
  (this is the correct pattern — it avoids page Content-Security-Policy
  issues you'd otherwise hit trying to fetch() directly from a content
  script on a strict site)

**Mocked (needs your real backend next):**
- `background.js` → `handleExplanationRequest()` — right now this just
  keyword-matches against 3 hardcoded concepts and fakes network delay.
  Replace this function's body with a `fetch()` call to your own backend
  endpoint (Vercel/Cloudflare function), which does the real work:
  1. Calls the Claude API with the highlighted text + your concept list
     (see the matching prompt pattern in `cell_biology_concepts.md`)
  2. Looks up the matched concept's real video URL in your storage
     (Supabase/R2) — or returns a short Claude-generated fallback
     explanation if nothing matches yet
  3. Returns `{ type: 'video', concept, videoUrl }` or
     `{ type: 'text', concept, text }` — the content script already
     knows how to render both shapes, so no frontend changes needed.

## Known rough edges to expect (this is v0.1, not v1)

- Button/panel don't reposition on scroll — they just disappear. Fine for
  a demo, worth polishing later.
- No handling yet for selections that span multiple paragraphs/elements
  in complex page layouts (getClientRects() covers most cases but not all).
- `host_permissions: ["*://*/*"]` is intentionally broad for testing.
  Before you publish, narrow this to the specific research sites you
  actually support — broad host permissions also draw more scrutiny in
  the Chrome Web Store review process.
- No styling has been tested against dark-mode sites yet — the panel
  currently assumes a light page background.

## Suggested next step

Wire up one real backend endpoint (even a very simple one) that does
step 1–3 above for just the 12 starred concepts from
`cell_biology_concepts.md`, and swap it into `background.js`. That gives
you a genuinely working end-to-end demo on real content, not just mocks.
