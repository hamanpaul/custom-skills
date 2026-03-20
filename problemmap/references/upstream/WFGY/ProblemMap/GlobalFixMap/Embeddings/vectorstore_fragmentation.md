# Vectorstore Fragmentation: Guardrails and Fix Patterns

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


A focused guide to detect and repair fragmented vector indexes. Use this when recall looks fine in pockets yet end answers miss the correct section or flip unpredictably. The fixes below are store agnostic and verified with ΔS, λ, and coverage targets.

## When to use this page

* Same query returns different top-k from different namespaces or shards
* Correct facts exist but only appear after raising k a lot
* High recall on a few documents while others are invisible
* Nightly re-embeds or per-tenant splits changed results without code changes

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of the target section ≥ 0.70
* λ remains convergent across 3 paraphrases and 2 seeds
* Top-k ordering stable after consolidation

---

## Fast triage → open these first

* Retrieval knobs end to end → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Wrong-meaning hits despite high similarity → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Why this snippet and how to cite → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Reranking to stabilize order → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Semantic chunking checklist → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* FAISS and metric pitfalls → [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)

---

## Symptom → likely cause

* Good recall inside one namespace but misses across the corpus
  Likely cause: per-tenant or time-sliced indexes with no cross-merge fence

* Raising k surfaces the right doc only at large k values
  Likely cause: shard skew or HNSW params diverged across partitions

* A doc updated many times becomes “hard to find”
  Likely cause: orphaned vectors from previous revisions not tombstoned

* Same corpus embedded by two models mixes in one store
  Likely cause: mixed dimension or normalization mismatch

* Hybrid BM25 + vector works worse than either alone
  Likely cause: analyzers differ per index, weights not calibrated

---

## Fix in 60 seconds

1. **Measure ΔS and coverage**
   Run the query against each namespace or shard. Log ΔS(question, retrieved) and coverage to the anchor section. If one partition is strong and others flat, you have fragmentation.

2. **Clamp λ with a stable header**
   Apply citation-first schema and fixed header order to avoid prompt-side variance. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

3. **Consolidate and re-rank**
   Merge results across partitions, then apply a single deterministic reranker. See [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

4. **Verify**
   Coverage ≥ 0.70 on three paraphrases, ΔS ≤ 0.45, and top-k list stable across seeds.

---

## Root causes checklist

* Multiple namespaces per tenant without a union stage
* Mixed embedding models or mixed dimensions in one index
* Divergent metric or normalization per index
* HNSW or IVF params drift between shards
* Update pipeline creates new vectors but does not delete old ones
* TTL or retention policies silently evict sections
* Hybrid analyzer or tokenizer differs across stores
* Background jobs re-embed only a subset of the corpus

---

## Minimal repair playbook

**A) Contract your ingestion**

* Single writer. Idempotent writes with `doc_id`, `section_id`, `rev`, `index_hash`.
* Dedupe key = `sha256(normalized_text + source_id + section_id + rev)`.
* Enforce the same embedding model and normalization everywhere.

**B) Build a union retriever**

* Query all active partitions. Concatenate candidates with a common score scale.
* Apply one reranker with a fixed seed and top-k cap.
* Log partition id per hit for auditing.

**C) Tombstone and compact**

* On update, tombstone previous `(doc_id, section_id, rev)` vectors.
* Run a compaction job to drop orphaned vectors and re-index stats.

**D) Re-embed if metrics disagree**

* If ΔS stays high and flat while you vary k, rebuild with a consistent metric.
* Use the checklist in [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md).

---

## Copy-paste probes

**Three-paraphrase probe**

```
Ask the same question in 3 paraphrases.
For each partition p in {p1..pn}:
  retrieve top-20 → compute ΔS and coverage to the known anchor
Compare variance across partitions. Flag any partition with coverage < 0.50 or ΔS > 0.60.
```

**Orphan sweep**

```
List vectors where (doc_id, section_id) exists with multiple rev but only latest rev is in the document store.
If count_old > 0, schedule tombstone + compaction.
```

**Hybrid calibration**

```
Hold out 50 queries with gold anchors.
Grid search weights α ∈ [0.1..0.9] for vector vs bm25.
Pick α that maximizes coverage@k and stabilizes λ across seeds.
```

---

## Escalation paths

* Still flat after consolidation and reranking
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Order unstable even with a single partition
  Open: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* Suspected FAISS metric or index skew
  Open: [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)

* Payload lacks fields to audit “why this snippet”
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Verification checklist

* Coverage ≥ 0.70 on the gold anchor across 3 paraphrases
* ΔS(question, retrieved) ≤ 0.45
* λ does not flip when you reseed or reorder harmless headers
* Top-k overlap across partitions ≥ 0.8 after consolidation

---

## Copy-paste prompt for the LLM step

```txt
You have TXT OS and WFGY Problem Map loaded.

My issue smells like vectorstore fragmentation.
Traces:
- partitions: [p1, p2, ...]
- ΔS per partition: [...]
- coverage per partition: [...]
- model/metric/normalization: [...]

Tell me:
1) which layer is failing and why,
2) which WFGY page to open next,
3) the minimal structural fix to push ΔS ≤ 0.45 and reach coverage ≥ 0.70,
4) a short verification plan across 3 paraphrases and 2 seeds.
Use BBMC, BBPF, BBCR, BBAM as needed.
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

