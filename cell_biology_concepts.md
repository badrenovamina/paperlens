# Cell Biology — MVP Concept Library (v1)

Purpose: this is the fixed list of concepts your matching step checks highlighted
text against. Anything that doesn't match closely falls back to a plain-text
Claude explanation (no video) until you've validated demand and built that concept out.

Each concept below should eventually become ONE pre-rendered animation (30–90 sec).
Start with the ⭐ ones — they're the highest-frequency concepts in intro papers/textbooks
and give you the most "wow" per hour invested.

## 1. Cell Structure & Organelles
- ⭐ Cell membrane structure (phospholipid bilayer)
- ⭐ Mitochondria & the "powerhouse of the cell" framing
- Nucleus & nuclear pore complex
- Endoplasmic reticulum (rough vs smooth)
- Golgi apparatus & vesicle trafficking
- Ribosomes (free vs membrane-bound)
- Lysosomes & cellular digestion
- Cytoskeleton (microtubules, actin filaments)

## 2. Membrane & Transport
- ⭐ Osmosis
- ⭐ Facilitated diffusion
- Simple diffusion
- Active transport (sodium-potassium pump)
- Endocytosis
- Exocytosis

## 3. Cell Division
- ⭐ Mitosis (all phases)
- ⭐ Meiosis I vs Meiosis II
- Cell cycle checkpoints (G1, S, G2, M)
- Cytokinesis
- Chromosome condensation
- Crossing over / genetic recombination

## 4. Molecular Biology — Central Dogma
- ⭐ DNA replication (semi-conservative)
- ⭐ Transcription (DNA → mRNA)
- ⭐ Translation (mRNA → protein at the ribosome)
- mRNA splicing (introns/exons)
- Codons & the genetic code
- tRNA & anticodon pairing
- Post-translational modification
- Mutation types (point, insertion, deletion)

## 5. Cellular Metabolism & Energy
- ⭐ Glycolysis (overview, not every intermediate)
- ⭐ ATP synthase / chemiosmosis
- Krebs cycle (overview)
- Electron transport chain
- Photosynthesis light reactions
- Photosynthesis Calvin cycle

## 6. Cell Communication & Signaling
- Signal transduction (ligand → receptor → response)
- G-protein coupled receptors
- Second messengers (cAMP)
- Apoptosis (programmed cell death)
- Cell-cell junctions (tight, gap, desmosomes)

## 7. Genetics Fundamentals
- Gene expression regulation (operons, promoters)
- Epigenetics / DNA methylation
- Dominant vs recessive alleles
- Punnett square logic
- Gene mutation → protein consequence

---

**Total: 44 concepts.** Build the 12 ⭐ ones first — that's a realistic first sprint and
covers the concepts that show up constantly across intro biology and biochem papers.

**Matching prompt pattern** (send to Claude API per highlight):
> "Here is a list of biology concepts: [list]. Here is a sentence from a research
> paper: '[highlighted text]'. Which single concept (if any) does this sentence
> most directly explain or rely on? Reply with just the concept name, or 'NONE'
> if nothing matches closely."
