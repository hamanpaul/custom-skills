<!--
Search Anchor:
embedding metric mismatch
embedding cosine vs dot product mismatch
vector similarity metric mismatch
LLM embedding mismatch root cause
-->

# Metric Mismatch — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Embeddings**.  
  > To reorient, go back here:  
  >
  > - [**Embeddings** — vector representations and semantic search](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

Embedding metric mismatch is a structural error where the similarity metric used at retrieval time does not match the assumptions of the embedding model.  

Symptoms: top-k neighbors look plausible, but answers cite wrong sections or fail silently after switching distance metrics.

A focused fix when nearest neighbors look similar in cosine distance but your store runs L2 or dot, or the reverse. Use this page to localize the failure and rebuild the index with the right metric and normalization rules. No infra change needed.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Embedding vs meaning (Problem Map No.5): [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Traceability and cite first: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Fragmented stores pattern: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Reranking for safety net: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Chunking checklist: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of the correct section ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat on long windows

---

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Check metric alignment**  
   - What your embedder assumes: cosine or unit length vectors.  
   - What your store actually uses: L2, inner product, or cosine.  
   - If they disagree, rebuild with the correct metric or normalize on write and search.

3) **Normalize and lock**  
   - If using cosine, enforce L2 normalization at both index and query time.  
   - Fix text analyzer and casing before re-embed to avoid silent drift.  
   - Record `INDEX_HASH`, `EMBED_MODEL`, `METRIC`, `NORMALIZED=true|false` in metadata.

4) **Verify**  
   Run three paraphrases and two random seeds.  
   Require coverage ≥ 0.70 with λ convergent and ΔS ≤ 0.45.

---

## Failure signatures → likely cause → open this
- Top hits look semantically off while cosine test in a notebook seems fine  
  → Store runs L2 or dot with non normalized vectors.  
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Order of neighbors flips when you switch between dot and cosine on the same vectors  
  → Missing unit normalization or mixed write paths.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Hybrid retrieval underperforms a single retriever  
  → Metric split plus fragmented index or mixed analyzers.  
  Open: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Good recall but citations drift across runs  
  → Header reorder and λ flip, metric inconsistency amplifies the drift.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Quick reference — store defaults

> 版本與託管方案可能改變預設。以實際索引 schema 為準。

| Store | Typical default metric | Where to verify |
|---|---|---|
| FAISS | No fixed default. You must choose L2 or IP. Cosine via normalized IP. | Index type name, for example `IndexFlatL2`, `IndexFlatIP`. |
| Chroma | cosine | Client setting `distance_function`. |
| Qdrant | cosine | Collection config field `distance`. |
| Weaviate | cosine | Class schema `vectorIndexConfig.distance`. |
| Milvus | L2 for float vectors | Index params `metric_type` on the collection or index. |
| pgvector | No fixed default. Query operator decides. | `<->` L2, `<#>` inner product, `<=>` cosine. |
| Redis Vector Similarity | L2 | Index or HNSW param `DISTANCE_METRIC`. |
| Elasticsearch or OpenSearch | Often L2 on dense_vector unless set otherwise | Field mapping `similarity` set to `l2_norm`, `cosine`, or `dot_product`. |
| Pinecone | cosine | Index spec `metric`. |
| Typesense | cosine | Collection vector field `similarity`. |
| Vespa | euclidean unless changed | Schema `distance-metric` such as `euclidean`, `angular`, `dotproduct`. |

---

## Minimal rebuild checklist
- Lock tokenizer, casing, and Unicode NFC.  
- Recompute embeddings with a single model id and version string.  
- Apply L2 normalization if cosine is the target metric.  
- Rebuild the index with one metric only and write the metric into store metadata.  
- Add a preflight that fails if `query_metric != index_metric`.  
- Keep a 200 item gold set to validate ΔS and coverage before go live.

---

## Deep diagnostics
- **Three paraphrase probe**  
  Ask the same question three ways. If λ flips while metric is stable, fix headers. If ΔS stays high, suspect metric or normalization.

- **Anchor triangulation**  
  Compare ΔS to the correct section and to a decoy section. If both are close, re-embed after fixing analyzer and normalization.

- **Reranker cross check**  
  Run a cross encoder on top k. If reranker easily corrects the order, the base metric is likely the bottleneck.

---

## Copy paste prompt for your LLM step

```

I uploaded TXT OS and the WFGY Problem Map.

My issue: nearest neighbors look wrong. Suspect metric mismatch.
Traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states across 3 paraphrases.

Tell me:

1. which layer is failing and why,
2. the exact WFGY page to open from this repo,
3. the minimal steps to align metric and normalization,
4. a reproducible test with coverage ≥ 0.70 and ΔS ≤ 0.45.
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

