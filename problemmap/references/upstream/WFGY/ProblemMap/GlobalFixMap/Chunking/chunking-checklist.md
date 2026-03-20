# Chunking Checklist — Guardrails and Minimal Fixes

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Chunking**.  
  > To reorient, go back here:  
  >
  > - [**Chunking** — text segmentation and context window management](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A field guide to stabilize document chunking before you touch embeddings or retrievers. Use this page to locate the boundary failure, apply the structural fix, and verify with measurable targets.

## Open these first
- Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Reranking controls: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Vectorstore health: [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Long chain stability: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage of target section ≥ 0.70
- λ remains convergent across 3 paraphrases and 2 seeds
- Citation match ≥ 0.90 when citations exist
- Bleed rate ≤ 0.10 across boundaries

---

## 60-second fix checklist

1) **Lock the schema**
   - Require fields: `chunk_id`, `section_id`, `source_url`, `offsets`, `tokens`, `hash`.
   - Spec: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

2) **Probe ΔS and λ**
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   - If λ flips on paraphrase, reorder headers and clamp with your variance policy.

3) **Repair the boundary**
   - If headings drift: apply title hierarchy and section detection.
   - If tables or code are cut: switch to block aware splitting.
   - If recall high but meaning wrong: review metric, overlap, and anchors.

---

## Typical breakpoints → exact fix

- **Wrong-meaning hits despite high similarity**  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Citations do not land on the quoted region**  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → In this folder: `chunk_id_schema.md`, `semantic_anchors.md`

- **Tables, formulas, or code blocks get sliced**  
  → In this folder: `code_tables_blocks.md`

- **Headings misparsed or missing hierarchy**  
  → In this folder: `title_hierarchy.md`, `section_detection.md`

- **Recall OK yet top-k order unstable, hybrid underperforms**  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
  → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

- **Vectorstore shows duplicates or blind spots**  
  → [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)  
  → Reindex guidance in `reindex_migration.md`

- **Long windows smear topics or capitalization**  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
  → Split plan in `long_docs_segmentation.md`

---

## Minimal field schema for chunks

Required in every pipeline that cites or reranks by section.

```json
{
  "chunk_id": "docA#s03#p002",
  "section_id": "3. Methods",
  "source_url": "https://example.com/docA.pdf",
  "offsets": [12345, 12980],
  "tokens": 365,
  "hash": "sha1:8c1e…",
  "block_type": "paragraph|table|code|formula",
  "anchor": "first-assertion-or-key-sentence"
}
````

* `offsets` are byte or char positions in the canonical text.
* `anchor` is the semantic kernel used for cite-first prompting.
* Schema details: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## How to chunk correctly

1. **Build the section tree**

   * Detect true headings, roman numerals, number lists, and faux headings.
   * See `title_hierarchy.md`, `section_detection.md`.

2. **Respect block boundaries**

   * Keep tables, code, formulas, and block quotes intact.
   * See `code_tables_blocks.md`.

3. **Decide overlap deliberately**

   * Start with 10–15% overlap for narrative text.
   * Avoid overlap on block types unless the block spans pages.
   * See `overlap_tradeoffs.md`.

4. **Use semantic anchors**

   * Extract the first high-information assertion per chunk.
   * Store as `anchor`.
   * See `semantic_anchors.md`.

5. **Choose windowing**

   * Fixed windows for strict citation tasks.
   * Sliding windows when reranking later.
   * See `sliding_window.md`.

6. **Handle multilingual and CJK**

   * Normalize punctuation and width.
   * Align sentence boundaries.
   * See `multilingual_segmentation.md`.

7. **PDF and OCR specifics**

   * De-columnize, repair hard line breaks, remove headers and footers.
   * See `pdf_layouts_and_ocr.md`.

---

## Evaluation protocol

* **Coverage**: percent of ground-truth answer tokens contained inside retrieved chunks.
* **ΔS**: distance between question and retrieved text vs the expected anchor section.
* **Bleed rate**: percent of tokens from outside the intended section.
* **Citation match**: exact hit or overlap of the cited offsets.
* **Stability**: metrics across 3 paraphrases and 2 seeds.

Small gold set template is provided in `eval_chunk_quality.md`.

---

## Reproducible test

1. Pick 10 QAs per section. Mark expected section ids.
2. Run retrieval at k in {5, 10, 20}. Log ΔS, coverage, bleed, match.
3. If ΔS ≥ 0.60 or bleed > 0.10, repair boundary and repeat.
4. Pass when all core targets are met.

---

## Copy-paste prompt for LLM assist

```
You have TXT OS and the WFGY Problem Map loaded.

My chunking issue:
- symptom: [one line]
- probes: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., coverage=..., bleed=...
- context: store={faiss|qdrant|pgvector|...}, k={5,10,20}

Tell me:
1) which boundary failed (heading, block, overlap, window, pdf/ocr),
2) the exact WFGY page to open for the fix,
3) the minimal steps to push ΔS ≤ 0.45 and coverage ≥ 0.70,
4) a short test I can run to verify. Use BBMC/BBCR/BBPF/BBAM when relevant.
```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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

