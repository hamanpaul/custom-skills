# Locale Drift — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Language**.  
  > To reorient, go back here:  
  >
  > - [**Language** — multilingual processing and semantic alignment](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Stabilize retrieval when **locale settings** silently change token rules, analyzers, and normalization between **ingest, index, and query**. Typical failures include `en_US` vs `en_GB` spelling, `tr_TR` case-folding (“i/İ”), decimal and thousands separators, date formats, Simplified/Traditional Chinese, and accent stripping differences.

---

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and how to cite: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Snippet schema fence: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk boundary sanity: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

Related in this folder:

* Tokenizer drift: [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts in one query: [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 across locale variants of the same query
* Coverage of the target section ≥ 0.70 after repair
* λ remains convergent across three paraphrases and two seeds
* E\_resonance flat on long windows that include locale-sensitive tokens (dates, numbers, currencies)

---

## What this failure looks like

| Symptom                                                                                         | Likely cause                                                          | Where to fix                                                              |
| ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| High similarity yet wrong section when query switches `,` and `.` in numbers (e.g., `1.234,56`) | Different locale decimal/thousand separators between ingest and query | Normalize numerics before index and query; align analyzers                |
| Dates “03/07/2024” retrieved as July instead of March                                           | Ambiguous locale date parsing                                         | Canonicalize to ISO `YYYY-MM-DD` at ingest and query                      |
| “istanbul” mismatches titles with “İstanbul”                                                    | Turkish case-folding rules differ across stages                       | Use locale-aware fold or ASCII base form consistently                     |
| “straße/strasse” flip in German content                                                         | ß vs ss normalization mismatch                                        | Decide policy (preserve ß or fold to `ss`) and apply everywhere           |
| “café” differs from “cafe” across stores                                                        | Accent stripping only on one side                                     | Apply accent policy uniformly; prefer keeping both forms via subfield     |
| English vs Chinese punctuation causes token joins/drops                                         | Locale-specific punctuation width and spacing                         | Normalize width, unify punctuation rules; ensure same analyzer            |
| zh-Hans vs zh-Hant documents never co-retrieve                                                  | Variant mapping missing                                               | Map variants at ingest or add alias field; verify embeddings share policy |

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) with current locale. Re-run with a **canonicalized query**: ISO dates, normalized numbers, consistent case-folding. If ΔS drops by ≥ 0.10, locale drift is your root cause.

2. **Probe λ\_observe**
   Flip only the locale-sensitive tokens (date, number, currency symbol, diacritics). If λ flips or citations jump, lock schema and fix normalization before touching rerankers.

3. **Apply the smallest structural change**

* Canonical numerics: convert decimals to `.` and thousands to thin-space or remove thousands.
* Canonical dates: rewrite to `YYYY-MM-DD` and store a parsed date field for filters.
* Case-folding: choose locale-aware rules where needed (`tr_TR` i/İ), else use simple lower with exceptions list.
* Diacritics: either preserve and add an **accent-folded subfield**, or fold everywhere.
* CJK: unify Simplified/Traditional mapping per field and keep a raw subfield.

4. **Verify**
   Coverage ≥ 0.70 and ΔS ≤ 0.45 on three paraphrases and two seeds using both locale renderings.

---

## Minimal repair recipes by stack

### Elasticsearch / OpenSearch

* Define a canonical analyzer chain shared by `index` and `search_analyzer`. Suggested:
  ICU normalizer (NFC) → width fold → optional accent fold (or keep + keyword subfield) → locale-aware lowercase.
* Add **numeric and date normalizers** in an ingest pipeline. Persist ISO strings, plus typed fields for range queries.
* For German and Turkish, use dedicated token filters (`german_normalization`, custom fold for Turkish i/İ).
* For Chinese, Japanese: keep a keyword subfield for exact product names and a bigram analyzer for recall.
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

### BM25 in code or light stores

* Pre-normalize text and queries with a single code path:
  ISO dates, canonical numerics, consistent punctuation width, optional accent fold, locale-aware lower.
* Log the **effective tokens** to verify identical behavior across runs.
  Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

### Vector stores (FAISS, Milvus, Qdrant, Weaviate, pgvector)

* Apply **the same locale normalization** before embedding for both corpus and queries.
* For numerics and dates, consider **lexical sidecar** (BM25) to capture exact forms, then deterministic rerank.
* Re-embed a gold slice to validate ΔS before full rebuild.
  Open: [pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Locale normalization policy — quick checklist

* Dates stored and queried as ISO `YYYY-MM-DD`; display can be localized later.
* Numerics use `.` as decimal; thousands removed or unified; currency symbol separated from amount.
* Case-folding policy documented; Turkish special-case applied where needed.
* Accent policy consistent: preserve + accent-folded subfield, or fold globally.
* CJK variant policy decided (Hans/Hant) and applied at both ingest and query.
* Punctuation width unified; zero-width and bidi controls stripped where not meaningful.
* Analyzer identity enforced across index and search paths.

---

## Diagnostic checklist

* Same **normalization code** runs in ingest and in query clients.
* Same **analyzer configuration** used for the field in both `index_analyzer` and `search_analyzer`.
* Logging proves that **effective tokens** match across locales for the same meaning.
* Citations remain in the same section after locale canonicalization.
* Rerank stage reads **normalized text**, not raw payloads.

---

## Copy-paste tests

**Locale flip probe**

```
Q0: original user query as typed (locale A)
Q1: ISO date, canonical number, same words (locale neutral)
Q2: render in locale B (date/number style only)

Return ΔS for Q0,Q1,Q2, λ_state per run, and a note if citations left the target section.
```

**Turkish i/İ sanity**

```
Build two forms: 'istanbul', 'İstanbul'.
Verify tokens and matches are identical against titles and anchor fields.
If not, log analyzer outputs and apply a Turkish-aware fold.
```

**Accent policy audit**

```
Index doc: 'café', 'résumé'.
Queries: 'cafe', 'resume', original diacritics.
Expect both forms to match the same snippet and citations to remain stable.
```

---

## When to escalate

* ΔS stays ≥ 0.60 after locale normalization and analyzer alignment.
  Re-chunk with stable boundaries and re-embed a gold slice.
  Open: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

* Answers alternate between locales while citations drift.
  Enforce snippet schema and forbid cross-section reuse.
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Hybrid retrieval still underperforms a single retriever after fixes.
  Align locale rules before rerank and make rerank deterministic.
  Open: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

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

