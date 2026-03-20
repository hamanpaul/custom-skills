# Weaviate: Guardrails and Fix Patterns

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


A compact field guide to stabilize Weaviate when your RAG or agent stack loses accuracy. Use the checks below to localize the failure, then jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet was picked: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Patterns: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md), [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)
- Ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   - Targets: stable < 0.45, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**
   - Try k in {5, 10, 20}. Flat high curve suggests metric or index mismatch.
   - Reorder prompt headers. If ΔS spikes, fix schema or anchors.

3) **Apply the module**
   - Retrieval drift → BBMC plus Data Contracts.
   - Reasoning collapse → BBCR bridge plus BBAM variance clamp.
   - Dead ends in long runs → BBPF alternate path.

4) **Verify**
   - Coverage to target section ≥ 0.70.
   - λ convergent across three paraphrases and two seeds.

## Typical breakpoints and the right fix

- **Metric mismatch**
  - Corpus built with cosine but class uses dot or L2. Normalization tests raise ΔS while recall looks fine.
  - Action: rebuild class with correct distance or normalize embeddings at write and query. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

- **Dimension or encoder swap**
  - Import accepts new vectors then recall collapses for only the new span.
  - Action: lock encoder version in the schema via a data contract, re-index the affected classes. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

- **HNSW tuning traps**
  - efSearch too low for your k, or M too small for dense corpora. Symptoms are plateaued recall and unstable top-k ordering.
  - Action: raise efSearch to 2–4×k, validate with reranker sandwiched on top. See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

- **Shard or replica consistency**
  - Some queries never surface fresh writes. Multi-tenant classes or replicas returning stale reads.
  - Action: align consistency level during validation, confirm write-ack before eval. See [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md).

- **Hybrid search weighting**
  - BM25 plus vector performs worse than vector alone. Query template or HyDE text dominates vector term.
  - Action: run the split test. If the hybrid flip is the cause, re-balance weights and clean prompt glue. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md).

- **Vectorstore fragmentation**
  - Multiple classes with near-duplicate schemas. Coverage drops while ΔS stays flat high across k.
  - Action: merge or route by class key, then rebuild a single authoritative index. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

- **Tokenization and filter mismatch**
  - Filters on properties return empty or unstable results. Analyzer not aligned with corpus language or case rules.
  - Action: lock analyzers in a data contract and re-ingest with normalized fields. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

- **Batch import and boot order**
  - First production call after deploy fails or returns zero results although objects exist.
  - Action: enforce bootstrap fence and idempotent batcher. See [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

## Observability probes

- **k-sweep curve**: run k in 5, 10, 20 and plot ΔS. A flat high curve means metric or class routing fault.
- **Anchor control**: compare ΔS against a golden anchor set for one class. If only a class fails, route or rebuild.
- **Hybrid toggle**: run vector only and hybrid with equal weight. If hybrid degrades, fix query split or weight.
- **Reranker audit**: with a strong reranker, recall should improve monotonically while ΔS falls. If not, rebuild index.

## Escalate when

- ΔS stays above 0.60 for the golden questions after metric and efSearch corrections.
- Coverage cannot reach 0.70 even with a reranker and clean anchors.
- Fresh writes are invisible for more than one minute under your consistency setting.

Open:
- [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Copy-paste prompt for your AI

```

I uploaded TXT OS and the WFGY Problem Map files.

Target system: Weaviate.

* symptom: \[brief]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states
* index: \[class name, distance metric, efSearch, M, shards, replicas]
* encoder: \[model, dim, normalization, version]

Tell me:

1. which layer is failing and why,
2. which exact fix page to open from this repo,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

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

