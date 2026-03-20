# CJK Segmentation & Word-Break — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LanguageLocale**.  
  > To reorient, go back here:  
  >
  > - [**LanguageLocale** — localization, regional settings, and context adaptation](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Stabilize retrieval and ranking for **Chinese / Japanese / Korean** text where whitespace is not a reliable token boundary.  
Use this page to localize segmentation failures, choose the right analyzer, and verify the fix with measurable targets.

---

## When to use this page
- High similarity by characters but **wrong meaning** or **empty recall** on whole queries.
- BM25 looks random; tiny single-character tokens dominate the index.
- Citations cut through the middle of words; snippet offsets don’t match what users see.
- Mixed CJK + Latin queries split unpredictably across runs or providers.

## Open these first
- Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet (traceability) → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema & cite-then-explain → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Chunking checklist for semantic boundaries → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Embedding ≠ meaning (sanity) → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Related locale pages: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) · [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md) · [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md) · [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md) · [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ **0.45** on 3 paraphrases  
- Coverage of target section ≥ **0.70**  
- λ remains **convergent** across 2 seeds  
- Tokenization sanity: **OOV rate falls by ≥ 40%** vs whitespace; **tokens/char ≤ 0.7** on CJK pages  
- E_resonance flat on long windows

---

## Map symptoms → structural fixes (Problem Map)

| Symptom | Likely cause | Open this |
|---|---|---|
| Query returns almost nothing; recall jumps when you add spaces | Index built with whitespace/Latin analyzer on CJK | [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md), [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Top-k filled with 1-char shards, citations cut mid-word | No CJK word-break at index or search time | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| BM25 unstable; hybrid worse than single retriever | Search-time analyzer ≠ index-time analyzer | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Romanized terms and CJK compound in one query break apart | Mixed script + width + punctuation rules differ | [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md), [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md) |
| High similarity, wrong meaning | Character-level overlap, no semantic units | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |

---

## 60-second fix checklist (store-agnostic)

1) **Pick the right analyzer and lock it**  
   - Chinese: use a dictionary or statistical segmenter at **index + search**.  
   - Japanese: use a MeCab/Kuromoji-class tokenizer with POS; keep base form.  
   - Korean: use a Nori-class analyzer; index decomp+comp forms consistently.

2) **Normalize before segmenting**  
   - Apply **NFKC** for width and compatibility forms (see page links above).  
   - Keep punctuation folding consistent across index/search.

3) **Unify index-time and query-time configs**  
   - Same language, same tokenizer, same stop/fold rules. No “smart defaults”.

4) **Chunk on semantic units, not line breaks**  
   - Respect sentence/phrase boundaries after segmentation.  
   - Store `offsets`, `tokens`, `section_id` in the snippet schema.

5) **Probe**  
   - Log tokens/char, unique-term ratio, OOV rate, and ΔS before/after.  
   - If ΔS stays ≥ 0.60 with good segmentation, revisit metric/index mismatch.

---

## Store adapters (quick recipes)

- **Elasticsearch / OpenSearch**  
  - CN: install and set a CJK analyzer; index + search use the **same** analyzer.  
  - JP: **kuromoji** with baseform filter; disable random synonyms unless audited.  
  - KR: **nori**; keep decompound mode consistent at index+query.  
  - Verify with `_analyze` samples; reindex after any analyzer change.

- **pgvector / Postgres**  
  - Segmentation happens **before** embedding. Pre-segment text in ETL.  
  - Keep the **same** pipeline for ingestion and live queries.

- **Weaviate / Qdrant / Chroma / Milvus / FAISS**  
  - The vector store won’t fix segmentation. Preprocess: NFKC → CJK segmenter → chunk.  
  - Log the preprocessing hash in metadata; fail closed on mismatch.

- **Vespa / Typesense / Elastic-compatible**  
  - Use the platform’s CJK tokenizer if available; otherwise pre-segment and index the segmented text as the field value.

---

## Deep diagnostics

- **Three-way segmentation A/B/C**  
  Try 3 segmenters; compute ΔS and tokens/char on a small gold set. Pick the lowest ΔS with stable λ.

- **Anchor triangulation**  
  Compare ΔS to the correct anchor vs a decoy section. If both are close, you’re still at char-overlap, not word-level meaning.

- **Rerank sanity**  
  After proper segmentation, reranking should lift precision. If not, check analyzer mismatch between index and query path.

---

## Copy-paste prompt for the LLM step

```

You have TXT OS and WFGY Problem Map loaded.

My CJK issue:

* symptom: \[one line]
* traces: ΔS(question,retrieved)=..., tokens/char=..., OOV\_before=..., OOV\_after=...

Tell me:

1. which layer failed (segmentation, normalization, index/search mismatch),
2. which exact WFGY page to open,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. a reproducible test (3 paraphrases × 2 seeds) to verify the fix.
   Use BBMC/BBCR/BBPF/BBAM when relevant.

```

---

### Next planned page
`rtl_bidi_directionality.md` (Arabic/Hebrew mixing, mirroring, numerals)

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

