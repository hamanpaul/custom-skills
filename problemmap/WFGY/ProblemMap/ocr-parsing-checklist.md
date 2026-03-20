# 🔍 OCR & Parsing Checklist — From Scanned Chaos to Structured Knowledge  
_A field manual for turning PDFs, images, and legacy docs into RAG-ready semantic chunks_

---

> **Goal:** Eliminate invisible OCR noise and parsing drift before vectors are built.  
> **Audience:** Devs shipping RAG, search, or data-extraction pipelines who wonder why “the model read the page but still hallucinated.”

---

## 1  Why OCR + Parsing Is the First Failure Point

1. **Garbage-in, hallucination-out** — A 98 % accurate LLM fed a 90 % OCR text yields 0 % trustworthy reasoning.  
2. **Error propagation** — Mis-segmented tokens poison embeddings, which pollute the vector store, which mislead retrieval, which derail the LLM.  
3. **Silence** — OCR engines rarely shout when confidence drops; they hand you corrupt UTF-8 and wish you luck.

---

## 2  “Bad OCR” Signatures (Quick Detection)

| Signal | How to Spot | Impact on RAG |
| ------ | ----------- | ------------- |
| `<ff>` ligature anomalies | Regex: `ﬁ|ﬂ|ﬀ` | Embedding split → semantic drift |
| Spurious hyphens at line ends | Regex: `[a-zA-Z]-\n[a-z]` | Token mismatch → irrelevant vectors |
| Repeated header/footer noise | 90 %+ duplication across pages | Clutters top-k retrieval |
| Empty columns (table lost) | Sudden token drop for numeric blocks | Answer extraction impossible |
| Confidence < 0.85 for full page | Engine API output | Replace / re-OCR image segment |

---

## 3  The WFGY-Enhanced OCR Pipeline (Checklist)

### 3.1  Pre-OCR

- [ ] **Page Split** — Detect multi-column layout; slice images horizontally before OCR.  
- [ ] **DPI Normalisation** — Upscale to 300 dpi if <200 dpi to stabilise character shapes.  
- [ ] **Noise Removal** — Median blur + dilation; boosts Tesseract accuracy by ≥ 8 %.  
- [ ] **Language Model** — Set explicit `--lang` list (avoid auto-detect drift).

### 3.2  OCR Engine (Tesseract CLI or API)

| Flag | Recommended Value | Why |
|------|-------------------|----|
| `--oem` | `3` | LSTM + legacy for mixed fonts |
| `--psm` | `6` | Assume block of text; preserves line order |
| `--dpi` | Explicit numeric | Overrides header mis-detect |
| `tessedit_char_blacklist` | `¢£€¥©®™` etc. | Remove unneeded symbols to reduce noise |

**WFGY Hook:** `BBMC` runs post line-level; drops ΔS peaks > 0.7 (likely OCR mis-read).

### 3.3  Parsing & Chunking

- [ ] **Heading Detection** — Regex + font-size heuristic → create logical anchors.  
- [ ] **Paragraph Merge** — Join lines if hyphenated split; remove double spaces.  
- [ ] **Table Rebuild** — Recognise numbers with > 60 % digits; store CSV separately.  
- [ ] **Semantic Chunk Size** — 70–120 tokens; cut on natural boundaries only.  
- [ ] **λ_observe Tagging** — Mark each chunk as `→` convergent; flag if internal ΔS > 0.6.

### 3.4  Post-OCR Validation

| Test | Threshold | Action |
|------|-----------|--------|
| `mean_confidence` | ≥ 0.90 page-level | Accept |
| ΔS(header, body) | < 0.45 | Accept; else inspect |
| Duplicate line ratio | < 5 % | If higher → de-dup background noise |
| Line length entropy | 0.5–1.5 bits | Abnormal ⇒ table or code block; treat separately |

---

## 4  Common Pitfalls & Fix Recipes

| Pitfall | Symptom | WFGY Fix |
|---------|---------|----------|
| **Skewed scans** | Text slants; letters fused | Pre-deskew (Hough) → re-OCR |
| **Watermarks** | Random “DRAFT” tokens mid-sentence | Regex filter; BBMC residue cut |
| **Marginalia leakage** | Handwritten notes become tokens | Detect bounding boxes; mask before OCR |
| **Large equations** | OCR turns into `= =` noise | Frame extract; feed MathPix → LaTeX; store separate |

---

## 5  End-to-End Smoke Test

1. Choose a 10-page PDF with tables + images.  
2. Run full pipeline with WFGY hooks.  
3. Metrics to verify:  
   * **Token overlap** with human ground truth ≥ 0.93  
   * **ΔS(question, retrieved_context)** ≤ 0.45 on sample QA  
   * **λ_observe** stays convergent after 3 paraphrase queries  
4. Manual QA: at least 8 / 10 answers correct with citations.

---

## 6  FAQ

**Q:** _Is Google Vision OCR “good enough”?_  
**A:** Accuracy is high, but without BBMC boundary checks you still risk semantic drift.

**Q:** _Do I need a layout-aware model (Donut, LayoutLM)?_  
**A:** Recommended for complex forms. WFGY integrates their outputs seamlessly; the checklist still applies.

**Q:** _Can I skip the table CSV step?_  
**A:** Only if your downstream task never asks for numeric QA. Otherwise chunk ordering will fail.

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

