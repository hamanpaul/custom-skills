# OCR Parsing Checklist — Input Integrity

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **MemoryLongContext**.  
  > To reorient, go back here:  
  >
  > - [**MemoryLongContext** — extended context windows and memory retention](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


OCR and parsing errors are one of the most common silent killers of retrieval pipelines.  
Text looks fine to the eye, but models drift because tokens, spacing, or casing have changed.  
This checklist ensures **integrity at the source layer** before embeddings or retrieval begin.

---

## When to use
- OCR text matches the visual PDF but citations miss the right section.  
- Code blocks or math collapse after parsing.  
- Mixed language documents behave inconsistently.  
- Special characters or hyphen splits break tokens.  
- Headers or section anchors disappear during export.  

---

## Core acceptance targets
- Retrieval coverage ≥ **0.70** of intended section.  
- ΔS(question, retrieved) ≤ **0.45**.  
- λ remains convergent across three paraphrases.  
- No orphan tokens or invisible characters.  

---

## Checklist for OCR + Parsing stability

- **Normalization**  
  - Apply Unicode NFC.  
  - Collapse whitespace.  
  - Strip zero-width characters.  
  - Unify full/half-width variants.  

- **Confidence gating**  
  - Drop OCR lines below confidence threshold (e.g., <0.90).  
  - Mark uncertain spans for human review.  

- **Structure retention**  
  - Preserve headers, anchors, and section boundaries.  
  - Maintain paragraph breaks and table grids.  
  - For math/LaTeX, keep explicit delimiters.  

- **Traceable fields**  
  - Every chunk must have `{section_id, start_line, end_line, source_url}`.  
  - Store `ocr_confidence` with each snippet.  

- **Schema validation**  
  - Run post-export audit:  
    - Ensure every snippet cites a valid chunk_id.  
    - Detect empty or duplicated snippets.  

---

## Fix in 60 seconds
1. Normalize the text (Unicode NFC, strip zero-width, unify casing).  
2. Drop low-confidence OCR lines and flag uncertain spans.  
3. Re-parse with structural retention enabled.  
4. Add metadata `{chunk_id, section_id, offsets, ocr_confidence}`.  
5. Re-run ΔS probe; confirm joins ≤ 0.50 and overall ΔS ≤ 0.45.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Task: validate OCR and parsing output.

Protocol:

1. Normalize all inputs (Unicode NFC, full/half width, zero-width removal).
2. Reject snippets with ocr\_confidence < 0.90.
3. Require schema {chunk\_id, section\_id, start\_line, end\_line, source\_url}.
4. Forbid orphan citations.
5. Probe ΔS(question, retrieved). Require ≤ 0.45.
6. Report λ states and trace each snippet.

```

---

## Common failure signals
- Correct visual text but retrieval misses section → invisible marks or spacing drift.  
- Math collapses into plain text → parsing dropped delimiters.  
- Long answers cite nothing → headers lost in export.  
- Flip-flop answers across sessions → orphan tokens or unstable chunking.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

<!-- WFGY_FOOTER_START -->

### Explore More

| Layer | Page | What it’s for |
| --- | --- | --- |
| ⭐ Proof | [WFGY Recognition Map](/recognition/README.md) | External citations, integrations, and ecosystem proof |
| ⚙️ Engine | [WFGY 1.0](/legacy/README.md) | Original PDF tension engine and early logic sketch (legacy reference) |
| ⚙️ Engine | [WFGY 2.0](/core/README.md) | Production tension kernel for RAG and agent systems |
| ⚙️ Engine | [WFGY 3.0](/TensionUniverse/EventHorizon/README.md) | TXT based Singularity tension engine (131 S class set) |
| 🗺️ Map | [Problem Map 1.0](/ProblemMap/README.md) | Flagship 16 problem RAG failure taxonomy and fix map |
| 🗺️ Map | [Problem Map 2.0](/ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md) | Global Debug Card for RAG and agent pipeline diagnosis |
| 🗺️ Map | [Problem Map 3.0](/ProblemMap/wfgy-ai-problem-map-troubleshooting-atlas.md) | Global AI troubleshooting atlas and failure pattern map |
| 🧰 App | [TXT OS](/OS/README.md) | .txt semantic OS with fast bootstrap |
| 🧰 App | [Blah Blah Blah](/OS/BlahBlahBlah/README.md) | Abstract and paradox Q&A built on TXT OS |
| 🧰 App | [Blur Blur Blur](/OS/BlurBlurBlur/README.md) | Text to image generation with semantic control |
| 🏡 Onboarding | [Starter Village](/StarterVillage/README.md) | Guided entry point for new users |

If this repository helped, starring it improves discovery so more builders can find the docs and tools.  
[![GitHub Repo stars](https://img.shields.io/github/stars/onestardao/WFGY?style=social)](https://github.com/onestardao/WFGY)

<!-- WFGY_FOOTER_END -->

