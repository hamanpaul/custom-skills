# Script Mixing — Guardrails and Fix Pattern

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


Stabilize retrieval and reasoning when a single query or document spans multiple writing systems. Typical cases include CJK plus Latin, Arabic plus Latin, Indic plus Latin, or mixed fullwidth and halfwidth forms.

## What this page is
- A focused path to detect and repair cross-script confusion in retrieval and ranking.
- Field designs and checks that do not require infra changes.
- Exact jumps to Problem Map pages with measurable targets.

## When to use
- A single user query contains two scripts and recall drops.
- Citations look correct by eye but come from the wrong section when scripts differ.
- BM25 or lexical search beats embeddings on mixed-script inputs.
- Coverage looks fine in one language but collapses when users code-switch.
- Fullwidth punctuation or presentation forms break token boundaries.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability and snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) • [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Tokenizer mismatch checks: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Locale drift and normalization: [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)  
- Reranking recipes: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ stays convergent across three paraphrases and two seeds  
- E_resonance flat on long windows

---

## Typical symptoms → exact fix

- One query spans two scripts and nearest neighbors look irrelevant  
  → Normalize and split by script, then fuse scores. See [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md), [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- High similarity yet wrong meaning for mixed script names or brands  
  → Add a romanized and a native field. Lock citation schema. See [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- BM25 wins but flips order across runs  
  → Deterministic two-stage: lexical per script then cross-encoder rerank. See [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Fullwidth punctuation or Arabic presentation forms break tokens  
  → Unicode fold to NFC or NFKC, halfwidth normalization, ZWJ handling. See [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)

- HyDE plus BM25 splits the query and hurts hybrid performance  
  → Lock query plan and weights. See [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

---

## 60-second checklist

1) **Detect scripts**  
   Count Unicode scripts in query and top snippets. If more than one, set `mixed_script=true`.

2) **Normalize safely**  
   Apply NFC or NFKC. Convert fullwidth to halfwidth. Strip presentation forms where safe. Keep a raw field.

3) **Dual-field design**  
   For each text unit store:  
   - `text_raw`  
   - `text_norm` with case fold and width fold  
   - Optional `text_romanized` for CJK or Indic when users type Latin queries

4) **Parallel retrieval**  
   Run retrieval on `text_norm` and `text_romanized` when `mixed_script=true`. Merge with stable weights, then rerank with a cross-encoder.

5) **Schema lock**  
   Enforce cite-then-explain. Require `snippet_id`, `section_id`, `offsets`, `tokens`. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

6) **Verify**  
   Three paraphrases. ΔS ≤ 0.45 and λ convergent on two seeds.

---

## Minimal field plan you can copy

- Index three views per document section: `raw`, `norm`, `romanized`  
- Populate `romanized` only when the language has a common transliteration.  
- For lexical stores, select analyzers that respect script boundaries. For Elasticsearch specifics see [elasticsearch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md).  
- For vector stores, embed `norm` and keep a shallow rerank over `raw` to guard against over-aggressive folding.

---

## Query cookbook

- If query is Latin plus CJK, run two subqueries: Latin over `romanized`, CJK over `norm`. Fuse by learned weight or fixed 0.6:0.4.  
- If query contains Arabic with diacritics, run a folded pass and a diacritic-aware pass. Keep offsets separate to avoid citation drift.  
- For Thai or Khmer where token boundaries are implicit, add a shallow BM25 over syllable or dictionary segments, then rerank the top 200 with a cross-encoder.

---

## Copy-paste prompt

```

I uploaded TXT OS and the WFGY Problem Map.

My bug: script mixing in one query.

* symptom: citations jump to the wrong section when users mix scripts
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states across 3 paraphrases

Tell me:

1. the failing layer and why,
2. the exact WFGY page to open from this repo,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. a reproducible test to verify the fix.
   Use BBMC, BBCR, BBPF, BBAM when relevant.

```

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

