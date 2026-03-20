# Emoji ZWJ & Grapheme Clusters: Guardrails and Fix Pattern

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


Stabilize retrieval and reasoning when user text contains emoji sequences, skin-tone modifiers, variation selectors, and ZWJ chains. The goal is to keep chunking, indexing, and evaluation aligned with grapheme clusters instead of raw code points.

## What this page is
- A compact repair guide for corpora and queries that contain emojis or complex grapheme clusters.
- Structural fixes that do not require infra change.
- Concrete steps with measurable acceptance targets.

## When to use
- Family or profession emojis break apart into multiple unrelated tokens.
- Skin tone or gender variants collapse to the base pictograph.
- Variation Selector-16 (FE0F) or ZWJ (U+200D) disappears during export.
- Top-k looks similar but answers flip on messages that include emojis.
- Citations fail to match because offsets count code points instead of graphemes.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Traceability and snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Chunking checklist: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
- Tokenizer mismatch in this folder: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)
- Width and punctuation pitfalls: [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage of target section ≥ 0.70
- λ stays convergent across three paraphrases and two seeds
- Offsets and spans are grapheme accurate in citations

---

## Typical symptoms → exact fix

| Symptom | Cause | Open this |
|---|---|---|
| 👨‍👩‍👧 breaks into four tokens and retrieval misses context | word-break at code points instead of grapheme clusters | [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md), [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Skin-tone or gender variants normalize to base emoji | aggressive folding or NFKD pipeline drops modifiers | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Offsets in citations do not match UI highlights | span counting by UTF-16 units or code points | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Answers flip when messages include emojis | tokenizer mismatch between embedder and store | [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md) |
| High similarity yet wrong meaning on chat logs | punctuation or ZWJ stripped during export | [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md), [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |

---

## 60-second fix checklist

1) **Normalize without destroying intent**  
   Use NFC only. Do not fold ZWJ U+200D, VS-16 U+FE0F, or skin-tone modifiers U+1F3FB–U+1F3FF.

2) **Grapheme-aware chunking**  
   Use ICU rules or a library that splits on grapheme clusters. Regex engines that support `\X` should prefer it over `.`.

3) **Index two tracks when needed**  
   Store `text_raw` and `text_search`. `text_raw` keeps exact clusters for citation. `text_search` may apply safe normalizations for recall.

4) **Tokenizer alignment**  
   Match embedder and store analyzers. If the store lacks grapheme awareness, rerank with a grapheme-aware stage.

5) **Traceability contract**  
   Snippet payload must carry `offset_grapheme_start`, `offset_grapheme_end`, and the exact substring for audit.

6) **Observability probes**  
   Log counts of ZWJ, VS-16, and skin-tone modifiers per snippet. Spikes often reveal faulty exporters.

---

## Deep diagnostics

- **Three-paraphrase probe**  
  Ask the same question three ways with and without emojis. If λ flips only when emojis appear, the tokenizer path is the root cause.

- **Anchor triangulation**  
  Compare ΔS to the intended message versus a decoy message that differs only by emoji variants. If scores are close, rebuild index with grapheme-aware chunking.

- **Exporter audit**  
  Validate that CSV, HTML, or PDF exporters preserve ZWJ and VS-16. Many pipelines silently drop them.

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map loaded.

My emoji issue:

* symptom: \[one line]
* traces: ΔS(question,retrieved)=..., λ states across 3 paraphrases, grapheme offsets present or missing.

Tell me:

1. the failing layer and why,
2. the exact WFGY page to open,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.
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

