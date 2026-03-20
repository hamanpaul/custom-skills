# Tokenizer Mismatch — Language & Locale Guardrail

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


A focused repair when your **query tokenizer** and **corpus tokenizer** are not aligned.
Applies to BPE, WordPiece, SentencePiece, unigram, or custom analyzers in search engines.

## What this page is

* A fast route to locate and fix **tokenizer drift** across query, chunking, embedding, and store.
* Concrete checks with measurable acceptance targets.
* Zero infra change needed. You can verify with a tiny gold set.

## When to use

* High similarity yet wrong meaning on multilingual or accented inputs.
* Citations look correct to the eye but offsets mismatch the quoted text.
* Coverage drops after switching models or embeddings vendor.
* Hyphen, apostrophe, or CJK punctuation behaves inconsistently.
* Numbers, units, or hashtags fragment differently between query and corpus.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Boundary and chunk checks: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Hallucination fences: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45 on three paraphrases
* Coverage of target section ≥ 0.70
* λ remains convergent across two seeds
* **OOV drift**: query vs corpus OOV ratio difference ≤ 5% on the gold set
* **Split parity**: median token count difference ≤ 1 across query vs corpus for the same string

---

## Symptoms → root cause

| Symptom                                                     | You likely have                                                            |
| ----------------------------------------------------------- | -------------------------------------------------------------------------- |
| Correct section exists but citations point a few chars away | Unicode normalization mismatch (NFC vs NFKC), half-width vs full-width CJK |
| High similarity but wrong variant of the word               | Casing or accent strip mismatch between embedder and index analyzer        |
| Thai, Lao, Khmer queries fail on recall                     | Word-boundary segmenter missing or different between stages                |
| JSON keys or code identifiers shatter                       | Non-letter symbol rules differ across pipelines                            |
| Numbers and units split unpredictably                       | Locale-specific rules for punctuation and decimals differ                  |

Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Fix in 60 seconds

1. **Measure ΔS and OOV**

* Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
* Log OOV ratio for query and for the retrieved snippet using the **same** tokenizer that produced your embeddings.

2. **Probe split parity**

* For a 20-item gold set, record token counts under:
  a) query tokenizer, b) corpus tokenizer used at chunk time, c) embedder’s reference tokenizer (if exposed).
* If median difference > 1, you have split drift.

3. **Lock normalization and casing**

* Pick one normalization (NFC or NFKC). Apply consistently at: ingestion, chunking, embedding, query.
* Pick one casing rule (lower or preserve) and keep it identical.

4. **Rebuild or re-embed only what is needed**

* If embedder expects lowercase + NFKC, rebuild chunks that violate it.
* If search side uses BM25, align its analyzer with the embedder’s text pre-rules.

5. **Verify**

* Coverage ≥ 0.70 and ΔS ≤ 0.45 on three paraphrases.
* OOV drift ≤ 5%. Split parity within threshold.

---

## Minimal checks by language family

* **CJK**

  * Normalize full-width punctuation and digits.
  * Use a consistent segmenter for Chinese and Japanese or stick to character-level with bigram fallback.
  * Ensure the same rule applies during chunking and embedding.

* **Arabic / Hebrew (RTL)**

  * Normalize diacritics per a single rule set.
  * Keep shaping and presentation forms normalized before embedding.
  * Be strict on punctuation mirroring only at render time, not in stored text.

* **Indic scripts / Thai / Khmer**

  * Use a deterministic word-boundary segmenter at both ingestion and query.
  * Test numerals and units. Some locales vary decimal separators.

* **Accented Latin**

  * Decide: keep accents or strip accents. Do not mix.
  * Keep hyphen and apostrophe policy identical across all stages.

---

## Map to Problem Map

* Wrong-meaning hits despite high similarity
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Citations off by a few characters
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* Recall collapses on long chains or mixed locales
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## Store and stack notes

* Vector store selection will not fix tokenizer drift, but some stores add analyzers for hybrid search. If you use them, align rules with the embedder.
  Quick refs:
  [faiss.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md) ·
  [weaviate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/weaviate.md) ·
  [qdrant.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/qdrant.md) ·
  [milvus.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/milvus.md) ·
  [pgvector.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/pgvector.md) ·
  [elasticsearch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md)

---

## Repro script outline (pseudocode)

```txt
input: gold_set = [{text, anchor_id}]
for each item:
  q_tokens = query_tokenizer(item.text)
  a_text   = load_anchor_text(anchor_id)
  a_tokens = corpus_tokenizer(a_text)
  split_diff = |len(q_tokens) - len(a_tokens)|
  log(split_diff, OOV_q, OOV_a)

run retrieval for item.text → retrieved_snippet
compute ΔS(question, retrieved_snippet), ΔS(retrieved_snippet, anchor)
accept if ΔS ≤ 0.45 and split_diff ≤ 1 and OOV drift ≤ 5%
```

---

## Copy-paste prompt for the LLM step

```
I uploaded TXT OS and the WFGY Problem Map.

My symptom: tokenizer mismatch suspicions in Language & Locale.
Traces: ΔS(question,retrieved)=..., OOV_q=..., OOV_a=..., split_diff=...

Tell me:
1) which layer is failing and why,
2) the exact WFGY page to open from this repo,
3) the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible test to verify the fix with 20 gold items.

Use BBMC/BBCR/BBAM only when relevant.
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

