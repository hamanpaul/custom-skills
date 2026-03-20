# Update and Index Skew: Guardrails and Fix Patterns

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


A repair guide for pipelines where fresh content does not show up, shards disagree after a redeploy, or recall drops right after a routine job. Use this page to localize drift between ingestion, embedding, and index structures, then lock ordering and verify with ΔS, coverage, and λ.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability and cite first: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Payload schema and ingestion locks: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Metric or FAISS traps: [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
* Boot order and deploy failures: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Live ops and debugging: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## When to use this page

* New docs appear in object store but not in retrieval
* Some tenants or shards recall fine while others look stale
* After a redeploy, recall falls or top k order flips
* Index reports healthy yet coverage to anchors is low
* ANN rebuild completes but neighbor order looks random

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of the target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows

---

## Symptom to likely cause

* Fresh content missing for hours
  Likely cause: ingestion watermark stuck or write path non idempotent. Open [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

* One shard good and another flat
  Likely cause: mixed analyzer or model rev, or ANN params diverged. Open [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

* Recall drops after nightly job
  Likely cause: index rebuilt with a different metric or normalization policy. Open [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md).

* Top k flips after deploy
  Likely cause: header reorder or citation schema drift that amplifies store skew. Open [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

* Writes succeed but queries truncate or pad vectors
  Likely cause: dimension mismatch after model swap. Open [dimension\_mismatch\_and\_projection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/dimension_mismatch_and_projection.md).

---

## Fix in 60 seconds

1. **Read the watermarks**
   For each stage write a simple count and last processed id or time. Compare `DOC_COUNT`, `EMB_COUNT`, `IDX_COUNT`. Any gap indicates skew.

2. **Pin versions and abort on mismatch**
   Ingest refuses rows if any of these differ from the contract or store metadata: `embed_model`, `embed_rev`, `dim`, `metric`, `normalize_l2`, `analyzer_rev`, `ann_rev`, `index_hash`. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Rebuild the broken segment**
   Re-embed and re-index the affected shard or time window. Retrain ANN and PQ on the new vectors. Do not reuse old graphs.

4. **Clamp λ on the prompt side**
   Use citation first and fixed header order to avoid prompt variance while you repair the store. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

5. **Verify**
   Three paraphrases and two seeds. Require coverage ≥ 0.70 and ΔS ≤ 0.45 on the gold anchors.

---

## Root causes checklist

* Non idempotent upserts by `(doc_id, section_id, rev)`
* Background jobs race with live writers
* Mixed `embed_model` or `normalize_l2` across namespaces
* ANN params not retrained after rebuild
* Analyzer or tokenizer version differs across shards
* TTL or retention silently dropped sections
* Partial deploy cut over while index still training
* Streaming path uses a different preprocessor than batch

---

## Minimal probes

```
Probe A — watermark audit
For each stage {ingest, embed, index}:
  read COUNT and LAST_TS
Expect ingest ≥ embed ≥ index with small gaps. Any large gap is skew.

Probe B — version parity
Sample 1k rows per shard and tabulate:
  embed_model, embed_rev, dim, metric, normalize_l2, analyzer_rev, ann_rev
Any heterogeneity inside one collection is a fail.

Probe C — recall delta
Run the same 50 gold queries before and after shard rebuild.
Require coverage gain ≥ 0.10 if the shard was failing.

Probe D — ANN sanity
Toggle reranker on and off at k=20.
If reranker recovers most anchors while base k misses, retrain ANN or rebuild.
```

---

## Contract fields to add

```json
{
  "doc_id": "stable",
  "section_id": "stable",
  "rev": "v2025-08-28",
  "ingest_ts": "2025-08-28T10:42:00Z",
  "embed_model": "exact-id",
  "embed_rev": "hash-or-date",
  "dim": 768,
  "metric": "cosine",
  "normalize_l2": true,
  "analyzer_rev": "text-preproc-v3",
  "ann_index": "hnsw",
  "ann_rev": "hnsw_v5",
  "index_hash": "sha256:...",
  "partition": "tenant_a|shard_03",
  "write_path": "batch|stream",
  "tombstone": false
}
```

---

## Operational guardrails

* Single writer per partition and idempotent upsert
* Preflight that halts when `store.metric != contract.metric` or `dim` mismatches
* Blue green or shadow collection for any rebuild, with union retriever and deterministic rerank during cutover
* Scheduled drift sweep that compares watermarks and ΔS across partitions
* Alerts on ΔS ≥ 0.60 or λ flip rate spikes on live traffic

---

## Verification checklist

* Coverage ≥ 0.70 and ΔS ≤ 0.45 on a ten question gold set
* λ convergent across two seeds and three paraphrases
* Top k overlap across seeds ≥ 0.8 after the fix
* Watermarks aligned for ingest, embed, and index within your SLO window

---

## Copy paste prompt for the LLM step

```
TXT OS and the WFGY Problem Map are loaded.

My issue: updates not reflected or recall dropped after a job.
Traces:
- watermarks: ingest=..., embed=..., index=...
- versions: embed_model=..., embed_rev=..., metric=..., ann_rev=...
- ΔS(question,retrieved)=..., coverage=..., λ across 3 paraphrases

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open next,
3) the minimal structural fix to remove skew and pass targets,
4) a short verification plan for coverage ≥ 0.70 and ΔS ≤ 0.45.
Use BBMC, BBCR, BBPF, BBAM when relevant.
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

