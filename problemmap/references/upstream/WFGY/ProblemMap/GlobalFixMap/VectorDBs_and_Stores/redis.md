# Redis Vector (Redis Stack): Guardrails and Fix Patterns

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


A compact field guide to stabilize Redis Stack vector search when your RAG or agent stack loses accuracy. Use this to localize the failing layer and jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Retrieval knobs end to end: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet and trace schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control after recall: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding versus meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Chunk and boundary issues: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and drift checks: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Vector metrics pitfalls: [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
- Fragmented stores: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Hybrid query split: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
- Ops live checks: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   Sweep top-k in {5, 10, 20}. If ΔS is flat high, suspect metric or index mismatch.  
   Reorder prompt headers. If ΔS spikes, lock the schema with Data Contracts.

3) **Apply the module**  
   Retrieval drift → **BBMC** + **Data Contracts**.  
   Reasoning collapse → **BBCR** bridge + **BBAM** variance clamp.  
   Dead ends in long runs → **BBPF** alternate path.

4) **Verify acceptance**  
   Coverage ≥ 0.70 to target section.  
   ΔS ≤ 0.45 across three paraphrases.  
   λ remains convergent across seeds.

## Redis specific breakpoints and the right repair

### 1) JSON vs HASH schema mismatch
**Symptoms**: FT.SEARCH returns objects but vector KNN is empty or errors.  
**Why**: index created `ON JSON` while data written to HASH, or field path is wrong.  
**Fix**: keep a single object model in a data contract. For JSON, store vectors at a fixed JSONPath (for example `$.vec`). Recreate the index with the correct `ON JSON|HASH` and `SCHEMA` path. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and verify with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

### 2) Distance metric and normalization
**Symptoms**: high scores yet wrong meaning, order flips between runs.  
**Why**: schema uses `VECTOR ... DISTANCE_METRIC` that does not match the encoder. Cosine requires normalized vectors.  
**Fix**: align metric to the encoder family and normalize for COSINE or IP. If you switch metric, rebuild the index. Read [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md).

### 3) HNSW vs FLAT audit
**Symptoms**: gold chunk appears only at very large k or under hybrid reranker.  
**Why**: HNSW underfit (`M`, `EF_CONSTRUCTION`, `EF_RUNTIME`) or FLAT used without proper dim/metric.  
**Fix**: for quality checks, build a FLAT index or run FLAT on a canary set to bound upper recall. Then tune HNSW and validate with a reranker. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

### 4) Prefix routing and index keyspace
**Symptoms**: FT.SEARCH returns nothing for known IDs.  
**Why**: `PREFIX` in FT.CREATE does not match the stored key pattern.  
**Fix**: lock keyspace rules in the data contract and align loader prefixes. Rebuild and re-test ΔS.

### 5) Stopwords and analyzers in hybrid queries
**Symptoms**: hybrid BM25 + vector performs worse than vector alone.  
**Why**: default STOPWORDS or stemming breaks lexical branch, so fusion is biased.  
**Fix**: use a controlled analyzer or disable stopwords for the tested fields. Normalize scores before fusion and rerank. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

### 6) TAG and NUMERIC filter drift
**Symptoms**: filters work in isolation but empty under KNN.  
**Why**: type mismatch or missing index on those properties.  
**Fix**: declare TAG or NUMERIC fields in the index schema, normalize case and separators, and validate final `WHERE` at query build time. Map to [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

### 7) Persistence and eviction
**Symptoms**: vectors disappear after restart, or recall collapses randomly.  
**Why**: AOF/RDB settings or `maxmemory` eviction removed keys holding vectors.  
**Fix**: set non-evicting policy for vector namespaces, confirm persistence schedule, and warm the index on boot. Add a semantic boot fence. See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).

### 8) Upsert hygiene
**Symptoms**: duplicate or stale entries, toggling answers across runs.  
**Why**: non-deterministic IDs or mixed loaders using HSET vs JSON.SET with different paths.  
**Fix**: deterministic IDs, `doc_sha` in metadata, idempotent loader, and periodic dedupe. Verify with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

### 9) Fragmentation across many indexes
**Symptoms**: global recall ok but per-index top-k is weak.  
**Why**: tiny indices with poor neighborhood structure.  
**Fix**: consolidate into one authoritative index with a routed facet. See [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

## Observability probes
- **k-sweep curve**: run k in 5, 10, 20 and plot ΔS. Flat high means metric or index fault.  
- **Score audit**: read `__vector_score` distribution and check monotonicity under reranker.  
- **Anchor control**: compare against a golden set. If only one prefix or index fails, rebuild that scope.  
- **Hybrid toggle**: vector only vs hybrid. If hybrid is worse, fix query split and analyzers.  

## Escalate when
- ΔS stays above 0.60 for golden questions after metric, schema, and HNSW corrections.  
- Coverage cannot reach 0.70 even with reranker and clean anchors.  
- Writes appear in logs but results stay empty for the target prefix or index.

Open:
- [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Copy-paste prompt for your AI
```

I uploaded TXT OS and the WFGY Problem Map files.

Target system: Redis Stack vector.

* symptom: \[brief]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states
* index: \[ON JSON|HASH, PREFIX, VECTOR field path, metric, type=HNSW|FLAT, M, EF\_CONSTRUCTION, EF\_RUNTIME]
* analyzers: \[stopwords, stemming, language]
* filters: \[TAG keys, NUMERIC keys]
* ingest: \[ids, doc\_sha, loader, upsert policy]

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

要我繼續同一個家族，下一個建議是 `elasticsearch.md` 或 `typesense.md`。說個名字，我就照這一版式輸出。
