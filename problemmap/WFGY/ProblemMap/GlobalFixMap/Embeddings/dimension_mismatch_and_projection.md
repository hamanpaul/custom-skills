# Dimension Mismatch and Projection — Guardrails and Fix Patterns

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


Use this page when vectors fail at write or retrieval due to mismatched dimensions or when a projection adapter silently degrades meaning. The goal is to align model output size, store configuration, and any projection layer, then verify with ΔS, coverage, and λ.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Schema and audits: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Wrong meaning despite high similarity: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* FAISS metric and index traps: [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)

## When to use this page

* Client or batch embedder outputs 768 but the store is configured for 1024
* A projection layer or PCA was introduced and recall dropped
* Mixing two models with different dimensions caused invalid writes or runtime coercion
* ANN parameters trained on one dimension are reused after a dimension change
* Quantization artifacts after projection changed neighbor order

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows

---

## Symptom → likely cause

* Writes fail or vectors padded or truncated automatically
  Likely cause. Store dimension differs from embedder output or client uses a different model id than the index.

* Recall ok on a subset but anchor never ranks in top 3
  Likely cause. Projection matrix or PCA learned on a different distribution. Mismatch between train corpus and live traffic.

* Top k changes after quantization or IVF training
  Likely cause. Product quantizer or HNSW graph trained before the dimension change. Requires retrain.

* Different tenants see different quality after a migration
  Likely cause. Some partitions still encode with the old dimension. Mixed collections without a union rerank.

---

## Fix in 60 seconds

1. **Stop mixed writes**
   Fail fast when `vector_dim != store_dim`. Never coerce with pad or slice.

2. **Lock dimension in the contract**
   Record `dim`, `embed_model`, `embed_rev`, `projection_name`, `projection_rev`, `quantize=true|false`. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Rebuild the index**
   If dimension changed or projection changed, re-embed. Retrain ANN and PQ on the new vectors. Do not reuse old graphs.

4. **Verify**
   Three paraphrases and two seeds. Require coverage ≥ 0.70 and ΔS ≤ 0.45 before cutover.

---

## Safe projection patterns

* **No projection preferred**
  Use a single model family per collection. Create another collection for a different model or dim.

* **If projection is required**

  * Learn a linear map on matched pairs. Solve `W = argmin‖WX − Y‖² + λ‖W‖²` on a representative corpus.
  * Normalize both spaces consistently. If the target uses cosine, L2 normalize after projection.
  * Validate with a held out gold set and ΔS thresholds. Reject if recall drops more than 3 percent.

* **PCA or down projection**

  * Fit PCA only on the target distribution. Fix the component count and version it.
  * Rebuild ANN structures with the projected vectors.

* **Cross model blends**

  * Do not mix dimensions in one store. Use a union retriever then a single deterministic reranker on top k.

---

## Minimal probes

```
Probe A — hard dimension check
- Assert len(vec) == store_dim at write and at query. Abort otherwise.

Probe B — projection identity drift
- For N samples, compute ΔS(orig, projected). If median ΔS > 0.15, projection is too lossy for your task.

Probe C — ANN retrain necessity
- Compare recall@k before and after retraining ANN on projected vectors. If recall jumps only after retrain, previous graph was stale.

Probe D — quantization sanity
- Toggle quantization off for a 1k sample. If order stabilizes and ΔS drops, retrain PQ with the new dimension or disable for critical paths.
```

---

## Contract fields to add

```json
{
  "embed_model": "model-id",
  "embed_rev": "2025-08-01",
  "dim": 768,
  "projection_name": "linear_W_1024to768",
  "projection_rev": "v2",
  "normalize_l2": true,
  "ann_index": "hnsw",
  "ann_rev": "hnsw_v5",
  "quantize": false
}
```

---

## Minimal rebuild playbook

* Freeze writers and export current contracts
* Re-embed with the target model and dimension
* Retrain ANN or PQ on the new vectors
* Dual read and union rerank for one week
* Cutover only if coverage and ΔS meet targets on the gold set

---

## Verification protocol

* Ten question gold set with exact anchors
* Three paraphrases and two seeds per question
* Pass if coverage ≥ 0.70 and ΔS ≤ 0.45 with λ convergent
* Store traces with `dim`, `projection_name`, `ann_rev`, and `quantize`

---

## Copy paste prompt for the LLM step

```
TXT OS and WFGY Problem Map are loaded.

My issue: dimension mismatch or projection degraded recall.
Traces:
- dim: source=..., store=...
- projection: name=..., rev=...
- ΔS(question,retrieved)=..., coverage=..., λ across 3 paraphrases

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open,
3) the minimal structural fix to align dimensions or projection,
4) a verification plan to reach coverage ≥ 0.70 and ΔS ≤ 0.45.
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

