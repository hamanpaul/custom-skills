# Duplication and Near Duplicate Collapse — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **RAG_VectorDB**.  
  > To reorient, go back here:  
  >
  > - [**RAG_VectorDB** — vector databases for retrieval and grounding](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when **the same passage floods your top k** under different snippet IDs or slightly different text, which blocks coverage of other relevant sections. This often happens after PDF or HTML exports, aggressive chunk overlap, HyDE variants, or multi store merges.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Ordering control: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Normalization and scaling: [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md)  
- Vector store fragmentation: [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)  
- Hybrid fusion weights: [hybrid_retriever_weights.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md)  
- Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Traceability: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Core acceptance

- ΔS(question, retrieved) ≤ 0.45 across 3 paraphrases and 2 seeds.  
- Coverage ≥ 0.70 to the target section after dedupe and rerank.  
- **Dup collapse rate** between raw top k and final top k ≥ 0.35 when duplicates are present.  
- **Unique doc ratio** in final top k ≥ 0.60 unless a single source is the explicit target.  
- λ stays convergent when candidate order varies by seed.

---

## Symptoms → likely cause → open this

- Many top hits are visually identical with different IDs  
  → no canonical snippet key and no text level hashing  
  → keep reading this page, then enforce [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Small wording changes create new embeddings that crowd others  
  → near duplicate threshold missing or too loose  
  → enable SimHash or MinHash and a locality threshold

- Same passage from multiple pipelines or formats  
  → store fragmentation or mixed analyzers  
  → [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)

- Duplicates dominate after hybrid fusion  
  → weight fusion happens before dedupe, or per retriever dedupe is off  
  → fix workflow order here, then see [hybrid_retriever_weights.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md)

---

## Canonicalization and collapse in five steps

1) **Canonical form for text**  
   Normalize unicode, lowercase if schema allows, collapse whitespace, remove soft hyphens, fix PDF hyphen splits, strip boilerplate headers and footers.

2) **Stable snippet identity**  
   Define `snippet_id = sha256(doc_id + section_id + canonical_text_hash64)`.  
   If sectioning is absent, derive `section_id` from a structural anchor like heading path or DOM XPath.

3) **Near duplicate keys**  
   Compute both a **content hash** and a **locality sensitive signature**.  
   - Content hash: xxh64 of canonical text.  
   - Near duplicate: SimHash on token 3 grams or MinHash of shingles.  
   Keep `(content_hash, simhash_64, minhash_128)`.

4) **Collapse policy**  
   When candidates tie by identity or near identity, keep one representative and merge evidence.  
   Tie break by citation completeness, source authority, and recency.  
   Record a `collapsed_ids` list for audit.

5) **Order of operations**  
   Retrieve k per retriever → normalize scores → **dedupe within each retriever** → fuse sets → **dedupe fused set** → rerank with cross encoder → answer.

---

## Minimal reference recipe

```

dedupe:
canonicalize:
unicode\_nfkc: true
lowercase: true
collapse\_spaces: true
strip\_soft\_hyphen: true
fix\_pdf\_hyphen\_split: true
strip\_headers\_footers: true

identity\_key:
fields: \[doc\_id, section\_id, canonical\_text\_hash64]

near\_duplicate:
simhash\_bits: 64
simhash\_hamming\_max: 3
minhash\_bands: 16
minhash\_rows: 8
jaccard\_min: 0.92

tie\_break:
order: \[citation\_coverage, source\_authority, recency, shorter\_span\_first]

pipeline:
per\_retriever\_dedupe: true
post\_fusion\_dedupe: true
rerank\_top\_n: 100
final\_k: 15

```

---

## Observability you must log

- Count of raw candidates, per retriever.  
- Count collapsed by identical content.  
- Count collapsed by near duplicate threshold with examples.  
- Source mix histogram before and after dedupe.  
- ΔS and λ states at retrieve, fuse, dedupe, rerank, answer.  
- Top reasons for tie breaks.

---

## Common gotchas

- PDF exports shift soft hyphens and page headers which break identity keys.  
- DOM based section IDs change on each build. Prefer heading path or a stable anchor map.  
- Reranker input uses the non canonical text while dedupe used canonical, which causes post rerank duplication. Use the same canonical text for both.  
- HyDE creates multiple paraphrases that survive without a collapse pass. Dedupe after HyDE.  
- Dedupe only at document level while answers cite passages. Always dedupe at snippet level.

---

## Verification

- On a gold set of 100 questions with duplicates seeded:  
  - Dup collapse rate ≥ 0.35.  
  - Unique doc ratio ≥ 0.60.  
  - Coverage ≥ 0.70 and ΔS ≤ 0.45.  
  - λ remains convergent when candidate order is shuffled.

---

## Copy paste prompt for the LLM step

```

You have TXTOS and WFGY Problem Map loaded.

Take the fused candidate set and:

1. Collapse duplicates by snippet\_id and near duplicates by simhash and minhash thresholds.
2. For each kept snippet, merge citations and keep the most complete citation fields.
3. Return top 15 after cross encoder rerank, enforce cite then explain.

Output:
{
"kept": \[{ "snippet\_id": "...", "source\_url": "...", "collapsed\_ids": \["...","..."] }],
"ΔS": 0.xx,
"λ\_state": "...",
"notes": "why certain groups collapsed"
}

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

