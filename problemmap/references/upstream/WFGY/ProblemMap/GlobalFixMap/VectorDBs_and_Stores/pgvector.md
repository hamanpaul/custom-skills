# pgvector: Guardrails and Fix Patterns

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


A compact repair guide for Postgres + pgvector when RAG or agents lose accuracy. Use this to localize the failing layer and jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet and how to trace it: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding versus meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Vector metrics pitfalls: [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
- Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Targets: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   Sweep k in {5, 10, 20}. If ΔS is flat high across k, suspect metric or index mismatch.  
   Reorder prompt headers. If ΔS spikes, lock schema with Data Contracts.

3) **Apply the module**  
   Retrieval drift → **BBMC** + **Data Contracts**.  
   Reasoning collapse → **BBCR** bridge + **BBAM** variance clamp.  
   Dead ends in long runs → **BBPF** alternate path.

4) **Verify acceptance**  
   Coverage ≥ 0.70 to target section. ΔS ≤ 0.45 across three paraphrases. λ convergent across seeds.

## pgvector breakpoints and the right repair

**1) Opclass mismatch**  
- Symptom: high similarity yet wrong meaning.  
- Why: using `vector_l2_ops` with cosine-trained embeddings or `vector_ip_ops` without normalization.  
- Fix: align opclass with the encoder. Normalize when using IP. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

**2) Index type underfit**  
- Symptom: gold chunk appears only at large k.  
- Why: IVFFLAT lists too small or probes too low. HNSW `ef_search` under-tuned.  
- Fix: IVFFLAT tune `lists` at build and `probes` at query. HNSW raise `ef_search` to 2–4×k and review `m`. Validate with [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and add [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

**3) Training and stats**  
- Symptom: unstable top-k after bulk load.  
- Why: IVFFLAT trained on too few samples or skipped `ANALYZE`.  
- Fix: retrain IVFFLAT with a large sample, `ANALYZE`, then re-test ΔS and coverage.

**4) Dimension or encoder swap**  
- Symptom: inserts fail or new rows behave erratically in search.  
- Fix: ensure vector dim matches column dim. Lock encoder version in a data contract and re-embed the changed span. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**5) Normalization discipline**  
- Symptom: cosine search acts like random at small k.  
- Fix: store normalized vectors or normalize at query for cosine or IP. Rebuild index after policy change. See [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md).

**6) JSONB filters and plan drift**  
- Symptom: filtered search returns empty or slow.  
- Fix: lock metadata schema in data contracts. Add GIN index on JSONB keys used in `WHERE`. Verify plan uses vector index then filter. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

**7) Fragmentation across schemas or tables**  
- Symptom: global recall looks fine but per-scope top-k is weak.  
- Fix: consolidate into one authoritative table with a facet column. Rebuild index and add a reranker. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

**8) Upsert hygiene**  
- Symptom: duplicates or stale rows after `ON CONFLICT`.  
- Fix: deterministic IDs, `doc_sha` in metadata, idempotent loader, periodic dedupe. Validate with golden queries. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

**9) Hybrid lexical plus vector**  
- Symptom: hybrid performs worse than either alone.  
- Fix: normalize scores, fuse post-retrieval, then rerank with a cross-encoder. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

**10) Maintenance and boot fences**  
- Symptom: first prod call after deploy returns thin results.  
- Fix: enforce bootstrap fence, finish index build, `VACUUM` after heavy churn, confirm visibility after commit. See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).

## Observability probes
- k-sweep curve: 5, 10, 20 and plot ΔS. Flat high suggests metric or index fault.  
- Index audit: `EXPLAIN ANALYZE` should show IVFFLAT or HNSW usage. If planner skips it, fix stats and filters.  
- Anchor control: compare against a golden anchor set. If only one table or schema fails, rebuild that scope.  
- Reranker audit: with a strong reranker, recall improves and ΔS falls. If not, rebuild.

## Copy-paste prompt for your AI
```

I uploaded TXT OS and the WFGY Problem Map files.

Target system: Postgres + pgvector.

* symptom: \[brief]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states
* index: \[type=ivfflat|hnsw, lists/probes or m/ef\_search, opclass, dim, normalized?]
* filters: \[JSONB keys, indexes, example WHERE]
* ingest: \[ids, doc\_sha, upsert policy]

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
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” and the OS boots |

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

