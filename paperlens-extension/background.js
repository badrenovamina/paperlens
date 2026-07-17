// background.js — Manifest V3 service worker
//
// This is a MOCK of what your real backend will do. Replace the body
// of handleExplanationRequest() with a fetch() to your own backend,
// which should: (1) call the Claude API to match the highlighted text
// against your concept library, (2) return a pre-rendered video URL on
// a match, or a short fallback explanation when there's no match yet.
//
// Matching below is a local, dependency-free upgrade from plain keyword
// search: it first checks for a literal mention of the concept name (fast,
// exact), and if there isn't one, falls back to cosine similarity over
// each concept's description so a paragraph that never says "osmosis" but
// talks about water crossing a membrane toward higher solute concentration
// still matches. This is lexical (bag-of-words) similarity, not neural
// embeddings — a real backend would likely swap this for an embeddings API
// call, which needs network access this mock intentionally avoids.

const CONCEPT_LIBRARY = [
  {
    keyword: 'osmosis',
    concept: 'Osmosis',
    videoUrl: chrome.runtime.getURL('videos/osmosis.mp4'),
    description:
      'osmosis water molecules move across a semipermeable membrane from an area ' +
      'of low solute concentration to high solute concentration diffusion ' +
      'equilibrium concentration gradient hypertonic hypotonic isotonic solvent ' +
      'solute permeable membrane cell water potential',
  },
    {
    // "diffusion" alone would risk colliding with Osmosis's own
    // description (which already says "diffusion"), so the keyword is
    // "facilitated" specifically, not the shared word.
    keyword: 'facilitated',
    concept: 'Facilitated Diffusion',
    videoUrl: chrome.runtime.getURL('videos/facilitated_diffusion.mp4'),
    description:
      'facilitated diffusion transport protein channel protein carrier ' +
      'protein glucose molecule passive transport concentration gradient ' +
      'specific molecule polar charged no ATP required membrane crossing',
  },
  {
    keyword: 'mitosis',
    concept: 'Mitosis',
    videoUrl: chrome.runtime.getURL('videos/mitosis.mp4'),
    description:
      'mitosis cell division chromosomes splitting nucleus duplicating replicating ' +
      'prophase metaphase anaphase telophase daughter cells identical genetic ' +
      'material somatic cells spindle fibers centromere',
  },
  {
    // "meiosis" shares real vocabulary with "mitosis" (chromosomes,
    // division), which is why the description below leans on the terms
    // that are specific to meiosis (homologous, haploid, gametes, crossing
    // over) rather than the ones both concepts have in common.
    keyword: 'meiosis',
    concept: 'Meiosis I vs Meiosis II',
    videoUrl: chrome.runtime.getURL('videos/meiosis.mp4'),
    description:
      'meiosis homologous chromosome pairs haploid diploid reduction division ' +
      'gametes sperm egg independent assortment crossing over genetic variation ' +
      'sister chromatids synapsis tetrad non-identical',
  },
  {
    keyword: 'transcription',
    concept: 'Transcription (DNA to mRNA)',
    videoUrl: chrome.runtime.getURL('videos/transcription.mp4'),
    description:
      'transcription DNA RNA polymerase messenger RNA mRNA gene expression ' +
      'nucleotides template strand coding strand transcribing genetic code ' +
      'protein synthesis nucleus ribosome translation',
  },
  {
    // Deliberately not "membrane" as the literal keyword — Osmosis's own
    // description already contains "semipermeable membrane", so a generic
    // "membrane" keyword here would wrongly fast-path-match osmosis text.
    keyword: 'phospholipid',
    concept: 'Cell Membrane Structure',
    videoUrl: chrome.runtime.getURL('videos/cell_membrane.mp4'),
    description:
      'phospholipid bilayer cell membrane hydrophilic head hydrophobic tail ' +
      'fluid mosaic model embedded protein selectively permeable barrier ' +
      'lipid molecules membrane structure amphipathic',
  },
  {
    // Substring stem so "mitochondria", "mitochondrion", and
    // "mitochondrial" all hit the literal fast path.
    keyword: 'mitochondri',
    concept: 'Mitochondria',
    videoUrl: chrome.runtime.getURL('videos/mitochondria.mp4'),
    description:
      'mitochondria mitochondrion powerhouse of the cell outer membrane ' +
      'inner membrane cristae folds matrix aerobic respiration ATP synthesis ' +
      'oxidative phosphorylation organelle energy production cellular respiration',
  },
];

// Below this cosine score we treat it as "no real match" and fall back to
// a generic explanation rather than show an unrelated video. Calibrated
// against sample paragraphs: real matches scored 0.45-0.57, unrelated text
// scored 0.0, so this leaves a wide margin either way.
const MATCH_THRESHOLD = 0.15;

const STOPWORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
  'have', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the', 'this',
  'to', 'was', 'were', 'will', 'with', 'which', 'their', 'than', 'into',
  'across', 'over', 'also',
]);

// Crude suffix-stripping so "cells"/"cell", "chromosomes"/"chromosome",
// etc. count as the same term. Not a real stemmer — without this, plural
// vs. singular mismatches were quietly outscoring the correct concept in
// testing (a highlight mentioning "cells" scored higher against Mitosis's
// description than against Osmosis's, even in a sentence that literally
// said "osmosis," because Osmosis's description only had "cell").
function stem(word) {
  if (word.length > 4 && word.endsWith('ies')) return word.slice(0, -3) + 'y';
  if (word.length > 4 && word.endsWith('es')) return word.slice(0, -2);
  if (word.length > 3 && word.endsWith('s') && !word.endsWith('ss')) return word.slice(0, -1);
  if (word.length > 5 && word.endsWith('ing')) return word.slice(0, -3);
  if (word.length > 4 && word.endsWith('ed')) return word.slice(0, -2);
  return word;
}

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter((word) => word.length > 2 && !STOPWORDS.has(word))
    .map(stem);
}

function termFrequencyVector(tokens) {
  const vector = new Map();
  for (const token of tokens) {
    vector.set(token, (vector.get(token) || 0) + 1);
  }
  return vector;
}

function cosineSimilarity(vectorA, vectorB) {
  let dot = 0;
  let magA = 0;
  let magB = 0;
  for (const [term, count] of vectorA) {
    magA += count * count;
    if (vectorB.has(term)) dot += count * vectorB.get(term);
  }
  for (const count of vectorB.values()) magB += count * count;
  if (magA === 0 || magB === 0) return 0;
  return dot / (Math.sqrt(magA) * Math.sqrt(magB));
}

// Build (and cache) each concept's term-frequency vector once at startup.
for (const entry of CONCEPT_LIBRARY) {
  entry.vector = termFrequencyVector(tokenize(entry.description));
}

function matchConcept(text) {
  const lower = text.toLowerCase();

  // Fast path: an explicit mention of the concept name always wins,
  // regardless of similarity score — this preserves the old exact-match
  // behavior for the common case where the text just says "osmosis".
  const literalHit = CONCEPT_LIBRARY.find((entry) => lower.includes(entry.keyword));
  if (literalHit) return literalHit;

  // Fallback: no literal mention, so look for the closest concept by
  // description similarity — this is what catches a paragraph describing
  // osmosis without ever using the word.
  const highlightVector = termFrequencyVector(tokenize(text));
  let best = null;
  let bestScore = 0;
  for (const entry of CONCEPT_LIBRARY) {
    const score = cosineSimilarity(highlightVector, entry.vector);
    if (score > bestScore) {
      bestScore = score;
      best = entry;
    }
  }

  return bestScore >= MATCH_THRESHOLD ? best : null;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== 'PAPERLENS_GET_EXPLANATION') return;

  handleExplanationRequest(message.text)
    .then((result) => sendResponse({ result }))
    .catch((error) => sendResponse({ error: String(error) }));

  return true; // keep the message channel open for the async sendResponse
});

async function handleExplanationRequest(text) {
  // --- MOCK LOGIC — replace this whole function body with a real fetch ---
  await new Promise((resolve) => setTimeout(resolve, 900)); // simulate latency

  const match = matchConcept(text);

  if (match) {
    return { type: 'video', concept: match.concept, videoUrl: match.videoUrl };
  }

  return {
    type: 'text',
    concept: 'No animation yet for this one',
    text:
      `Stand-in explanation for: "${text.slice(0, 140)}${text.length > 140 ? '\u2026' : ''}" ` +
      `\u2014 in the real version this is where a Claude API call generates a short ` +
      `explanation, and logs this highlight as a candidate for your next animation.`,
  };
  // --- END MOCK LOGIC ---
}
