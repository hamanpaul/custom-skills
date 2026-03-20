# Locale Drift & Normalization — Guardrails and Fix Pattern

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


A focused fix for **locale-specific normalization bugs** that break retrieval or cause answers to flip between runs. Use this page to align **Unicode form, width, accents, digits, quotes, spaces, casing** across **ingest, index, query, and display**. No infra change required.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* OCR and parsing checks: [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
* Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Tokenizer alignment: [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)
* Code-switching in one query: [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Rerank determinism: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## When to use this page

* Same page looks identical to the eye, yet retrieval misses or ranks it differently.
* Queries with **accented vs unaccented** forms return different snippets.
* **Half-width vs full-width** characters change similarity scores.
* **Arabic-Indic digits** or **CJK punctuation** break matches.
* **Smart quotes** vs straight quotes fragment hits.
* **Turkish I** or locale-aware casing flips λ between runs.
* NBSP or narrow spaces split tokens unpredictably.

## Core acceptance targets

* ΔS(question, retrieved) ≤ **0.45** in the native locale, ≤ **0.50** after cross-locale normalization.
* Coverage of target section ≥ **0.70** on three paraphrases.
* λ remains **convergent** across three locale variants of the same question.
* No analyzer drift between **ingest** and **query** paths in hybrid pipelines.

---

## Symptoms → Likely cause → Open this

| Symptom                                           | Likely cause                                                    | Open this                                                                                                                                                                                                       |
| ------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Visually identical text but no hit                | Unicode form mismatch **NFD vs NFC**                            | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)  |
| Hits split between copies of the same doc         | **Width folding** not applied, **full-width** vs **half-width** | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                                                                                                             |
| Accented vs plain query return different snippets | Accent folding policy inconsistent                              | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)                                                                                                    |
| Numbers in Arabic-Indic scripts never match       | Digit class mismatch or analyzer not locale aware               | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)                                                                             |
| Quotes or hyphens break phrase queries            | **Smart quotes**, **em/quasi hyphens**, Unicode confusables     | [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)                                                                                                       |
| Same prompt, answers flip by locale               | Casing rules differ, **tr** locale I/i special case, λ unstable | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Token counts explode on CJK                       | NBSP, narrow no-break, or **ideographic space** not normalized  | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                                                                                                             |

---

## 60-second fix checklist

1. **Normalize at ingest and query**
   Apply in this order: **Unicode NFC**, width fold, digit fold to ASCII, smart-punct to ASCII, collapse exotic spaces, then **locale-aware casefold**. Keep the original text for display.

2. **Dual-key storage**
   Store both `visual_text` and `search_text`. Index BM25 on `search_text`. Keep `visual_text` for citations and display. Schema in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Embed both views when needed**
   For high-variance locales, create embeddings for **raw** and **normalized** text. Track which path produced the hit inside the snippet payload. See guidance in [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

4. **Align analyzers**
   Ensure the **same analyzer** and token rules for **ingest** and **query** in hybrid retrieval. Verify with three paraphrases and two seeds. If λ flips, pin headers and apply a BBAM variance clamp.

5. **Gold set verification**
   Run a 20-item multilingual gold set. Require ΔS ≤ 0.45 native and ≤ 0.50 normalized, coverage ≥ 0.70, λ convergent.

---

## Minimal adapter spec

* Payload must carry: `locale`, `unicode_form`, `width_fold`, `digit_class`, `space_class`, `accent_fold`, `case_mode`.
* Snippet must include both `visual_text` and `search_text` plus `normalization_trace`.
* Reject answers if citation `visual_text` and `search_text` disagree on offsets.

See schema patterns in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and tracing in [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

My bug smells like locale drift.
Question variants: {q_native, q_no_accents, q_width_folded}.
Traces: ΔS_native=..., ΔS_normalized=..., λ states across three variants.

Tell me:
1) which normalization step is missing and why,
2) the exact WFGY page to open,
3) the smallest change to push ΔS ≤ 0.45 native and ≤ 0.50 normalized,
4) a reproducible test with 3 paraphrases and 2 seeds.
Use BBMC/BBCR/BBAM when relevant.
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

