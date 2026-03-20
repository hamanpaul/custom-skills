# Chroma: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **VectorDBs_and_Stores**.  
  > To reorient, go back here:  
  >
  > - [**VectorDBs_and_Stores** — vector indexes and storage backends](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A compact field guide to stabilize Chroma setups in RAG, pipelines, and agents. Use this to localize the failing layer and jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Retrieval knobs end to end: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet and how to trace it: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding versus meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Fragmented stores and many tiny collections: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Hybrid query splits (HyDE vs BM25): [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
- Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   Vary top-k in {5, 10, 20}. Chart ΔS vs k. Flat high curve implies index or metric mismatch.  
   Reorder prompt headers. If ΔS spikes, lock the schema with Data Contracts.

3) **Apply the module**  
   - Retrieval drift → **BBMC** + **Data Contracts**.  
   - Reasoning collapse → **BBCR bridge** + **BBAM** variance clamp.  
   - Dead ends in long runs → **BBPF** alternate path.

4) **Acceptance**  
   Coverage to target section ≥ 0.70.  
   ΔS ≤ 0.45 across three paraphrases.  
   λ remains convergent. Logs and traces reproducible.

## Chroma specific breakpoints and the right repair

### 1) Embedding model mismatch
**Symptoms**: good lexical match yet wrong neighbors, or shape errors after a model swap.  
**Why**: collection was built with one embedding model and queried with another, or dimensions changed.  
**Fix**: pin the embedding model inside your data contract and collection metadata. Re-embed and rebuild the collection. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

### 2) Distance metric inconsistency
**Symptoms**: ordering looks inverted, distances are not comparable across collections.  
**Why**: default metric differs between old and new builds, or mixed cosine vs L2.  
**Fix**: declare the metric at collection create time and keep it in the contract. Rebuild if historic data used a different metric. Then tune ordering with [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

### 3) Persist directory contention or corruption
**Symptoms**: intermittent read errors, empty results after crash, slow queries on warm start.  
**Why**: multiple writers on the same `persist_directory`, partial flush, or version skew.  
**Fix**: one writer policy. Backup the directory, run a clean rebuild, then enable idempotent ingestion with hashes in metadata. Monitor with [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md).

### 4) Upsert vs add and ID hygiene
**Symptoms**: duplicated documents or silent stale content.  
**Why**: `add` used for updates, unstable IDs, missing deterministic hash.  
**Fix**: use `upsert` for refresh, keep stable IDs, store `doc_sha` in metadata, enforce uniqueness in your loader. Verify with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

### 5) Filter semantics and type drift
**Symptoms**: empty query results even when the document exists.  
**Why**: `where` filter types do not match stored metadata, or nested keys vary by loader.  
**Fix**: lock a minimal metadata schema in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). Validate on ingestion. Add a trace that prints the final `where` used per query.

### 6) Fragmentation across many collections
**Symptoms**: high recall globally yet poor top-k for any single collection.  
**Why**: topic splits created tiny indices with weak neighborhood structure.  
**Fix**: consolidate. Use a parent collection per corpus and a facet in metadata. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md). Add a reranker pass.

### 7) Concurrency and ingestion order
**Symptoms**: occasional out of date views after bulk loads.  
**Why**: parallel writers finishing without a final sync, or mixed loaders.  
**Fix**: serialize final commit, persist once, then start serving. Re-run a canary query set and verify ΔS and coverage.

## Copy-paste prompt for the AI
```

I uploaded TXT OS and the WFGY Problem Map files, and I am using Chroma.

symptom: \[brief]
traces: \[ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states, k curves]

Tell me:

1. which layer is failing and why,
2. which exact WFGY page to open from this repo,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the fix with a reproducible test.
   Use BBMC/BBPF/BBCR/BBAM when relevant.

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

