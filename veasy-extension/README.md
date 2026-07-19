# Veasy — Highlight to Explain (v1, growing concept library)

A working Chrome/Edge (Manifest V3) extension: detect a highlighted
selection, show an "Explain" button, and open a popup panel that plays a
real, pre-rendered animated video explaining the underlying concept — or
a text fallback when nothing in the library matches yet.

## How to load it and try it

1. Open `chrome://extensions` (or `edge://extensions` in Edge).
2. Turn on **Developer mode** (top right toggle).
3. Click **Load unpacked**, and select this `veasy-extension` folder.
4. Visit any normal page — start with something simple like a Wikipedia
   article, not a research site yet, since some research sites have
   stricter page security policies that are worth debugging separately
   from your core UI logic.
5. Highlight a sentence of at least ~12 characters. A "▶ Explain" button
   should appear just below your selection.
6. Click it. A panel opens, shows "Finding the best explanation…" for
   about a second, then shows a result.
7. Try highlighting text about any of the concepts currently in the
   library — osmosis, mitosis, meiosis, transcription, cell membrane
   structure, mitochondria, facilitated diffusion, DNA replication,
   translation, glycolysis, or ATP synthase — you'll get a real video,
   even if the highlighted text doesn't say the concept name explicitly
   (matching also works on paraphrases, not just exact keywords). Any
   other text gives you a text-fallback response.

## What's real vs. what's still mocked

**Real (built):**
- Selection detection and button placement
- Popup panel open/close, loading state, result rendering (video or text)
- Message-passing architecture: content script → background service worker
  (this is the correct pattern — it avoids page Content-Security-Policy
  issues you'd otherwise hit trying to fetch() directly from a content
  script on a strict site)
- 11 real, pre-rendered concept videos, each reviewed for scientific
  accuracy before being added to the library (see the individual
  `*_animation.py` scripts in the parent folder for the science notes)
- Matching: a literal keyword check first, then a local cosine-similarity
  fallback over each concept's description — no network call, runs
  entirely in the browser (see `background.js` for the full explanation)

**Mocked (needs a real backend next):**
- `background.js` → the text-fallback branch of `handleExplanationRequest()`
  still returns a canned stand-in string instead of a real explanation.
  Replacing this needs a backend endpoint (Vercel/Cloudflare function)
  that calls the Claude API server-side — never embed an API key directly
  in this extension's code, since it's fully inspectable by anyone who
  installs it.

## Known rough edges to expect

- Button/panel don't reposition on scroll — they just disappear. Fine for
  a demo, worth polishing later.
- No handling yet for selections that span multiple paragraphs/elements
  in complex page layouts (getClientRects() covers most cases but not all).
- `host_permissions: ["*://*/*"]` is intentionally broad for testing.
  **Before publishing to the Chrome Web Store, narrow this** to the
  specific sites actually supported — broad host permissions draw more
  scrutiny in the Web Store review process.
- No styling has been tested against dark-mode sites yet — the panel
  currently assumes a light page background.
- The concept library currently covers 11 of the 44 concepts listed in
  `cell_biology_concepts.md` (all 12 starred ones, minus none — the
  starred list is done; the remaining ~32 are future growth).

## Suggested next steps

1. Build the real Claude-backed text fallback (needs a backend — see
   above), so highlights that don't match the video library still get a
   genuinely useful explanation instead of a canned stand-in.
2. Narrow `host_permissions` and prepare Chrome Web Store listing assets
   (icon, screenshots, privacy policy) ahead of publishing.
3. Keep growing the concept library beyond the initial 12.
