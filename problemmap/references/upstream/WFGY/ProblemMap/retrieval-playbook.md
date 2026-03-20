# 🔎 Retrieval Playbook — Practical, Measurable, Fix-first

> The goal: **consistent, explainable** retrieval that makes reasoning easy.  
> This playbook gives you a **minimal, testable** setup across OCR → chunk → embed → index → retrieve → prompt, with **failure probes** and **repair steps**. No hype—only what ships.

---

> **Quick Nav**  
> [OCR/Parsing Checklist](./ocr-parsing-checklist.md) ·
> [Chunking Checklist](./chunking-checklist.md) ·
> [Embedding vs Semantic](./embedding-vs-semantic.md) ·
> [Traceability](./retrieval-traceability.md) ·
> [Rerankers](./rerankers.md) ·
> Patterns: [Query Parsing Split](./patterns/pattern_query_parsing_split.md) ·
> [Vectorstore Fragmentation](./patterns/pattern_vectorstore_fragmentation.md) ·
> [Symbolic Constraint Unlock](./patterns/pattern_symbolic_constraint_unlock.md)

---

## 0) Executive summary

1. **Generate clean candidates** (dense/sparse/hybrid) with traceable IDs.  
2. **Measure** with ΔS + recall@k before adding complexity.  
3. **Add reranking** only when first-stage recall is **consistently ≥0.85** for your task.  
4. **Lock prompt schema** (cite → explain) and **forbid cross-source merges**.  
5. **Regression-guard** with small golden sets (10–50 Q/A).

---

## 1) Candidate generation (first-stage)

### 1.1 Choose a primary retriever
- **Dense (embeddings)**: good default for semantic matches across paraphrases.  
- **Sparse (BM25/SPLADE)**: strong for exact terms, code, and rare tokens.  
- **Hybrid**: *reciprocal rank fusion (RRF)* of dense + sparse is robust to query style.

**Rule of thumb**
- Start **dense** for general docs; add **BM25** for code/legal/IDs.  
- If hybrid hurts recall, check **tokenization & analyzer drift** → see *Query Parsing Split*.

### 1.2 Index hygiene (FAISS/Elasticsearch/Qdrant/Chroma)
- **Normalize** vectors on **both write & read** if using cosine.  
- Pin the **metric type** (cosine vs inner product) in code & metadata.  
- Persist **doc_id / section_id / line_span** with each vector.  
- Verify **index cardinality = sum(chunks)**; add a one-liner count check in CI.

---

## 2) Minimal reference pipelines

### 2.1 Python — FAISS (dense) + BM25 (hybrid via RRF)

```python
# pip install sentence-transformers rank_bm25 faiss-cpu numpy
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import faiss, numpy as np

# 1) data
chunks = [...]                  # list[str], pre-chunked sentences/sections
meta   = [...]                  # list[dict], each with {doc_id, section_id, span}

# 2) encoder (cosine → L2-normalize)
enc = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
X = enc.encode(chunks, normalize_embeddings=True)
index = faiss.IndexFlatIP(X.shape[1])         # inner product == cosine on normalized vectors
index.add(X.astype(np.float32))

# 3) sparse side
tokenized = [c.split() for c in chunks]
bm25 = BM25Okapi(tokenized)

def rrf(ranks, k=60):
    # ranks: list of lists of (idx, rank_position starting at 1)
    from collections import defaultdict
    score = defaultdict(float)
    for rr in ranks:
        for idx, rp in rr:
            score[idx] += 1.0 / (k + rp)
    return sorted(score.items(), key=lambda x: -x[1])

def search(query, topk_dense=50, topk_sparse=50, out_k=20):
    qv = enc.encode([query], normalize_embeddings=True).astype(np.float32)
    d_s, d_i = index.search(qv, topk_dense)
    # ranks as (idx, rankpos)
    dense_rank  = [(int(i), r+1) for r, i in enumerate(d_i[0])]
    sparse_rank = []
    for r, idx in enumerate(bm25.get_top_n(query.split(), list(range(len(chunks))), n=topk_sparse)):
        sparse_rank.append((idx, r+1))
    fused = rrf([dense_rank, sparse_rank])
    out = []
    for idx, _ in fused[:out_k]:
        out.append({"text": chunks[idx], "meta": meta[idx], "source":"hybrid"})
    return out

res = search("how to reset billing cycle")
````

**Sanity checks**

* After encoding: assert `np.abs(np.linalg.norm(X[0]) - 1.0) < 1e-3`
* After add: `index.ntotal == len(chunks)`
* For sparse-only: if **IDs/code** outperform dense, keep hybrid.

### 2.2 Node (TypeScript) — Elastic BM25 + Dense store

```ts
// pnpm add @elastic/elasticsearch @huggingface/inference cosine-similarity
import { Client } from "@elastic/elasticsearch";
import { HfInference } from "@huggingface/inference";
import cosine from "cosine-similarity";

const es = new Client({ node: process.env.ES_URL! });
const hf = new HfInference(process.env.HF_TOKEN!);

// 1) BM25 query
async function bm25(query: string, topk=50) {
  const { hits } = await es.search({
    index: "chunks",
    size: topk,
    query: { match: { text: { query, operator: "and" } } },
    _source: ["text", "doc_id", "section_id", "span"]
  });
  return hits.hits.map((h, i) => ({ id: h._id, score: hits.max_score, r:i+1, src: h._source }));
}

// 2) Dense side (use same model for write+read)
async function embed(s: string) {
  const out = await hf.featureExtraction({
    model: "sentence-transformers/all-MiniLM-L6-v2",
    inputs: s
  });
  // L2 normalize
  const v = (out as number[]); 
  const norm = Math.sqrt(v.reduce((a,b)=>a+b*b,0)); 
  return v.map(x=>x/norm);
}
```

> Keep dense vectors in your KV/DB keyed by `chunk_id`; at query time compute cosine vs a small candidate pool (top-200 BM25), then RRF.

---

## 3) Retrieval observability (ΔS & λ)

* **ΔS(question, retrieved)** = `1 − cos(I, G)` with **I** = retrieved snippet embedding, **G** = anchor (title/expected section or gold answer).
* **Thresholds**: `<0.40` stable · `0.40–0.60` transitional · `≥0.60` action.
* **λ states**: `→` convergent · `←` divergent · `<>` recursive · `×` chaotic.

**Probe recipe**

1. Vary `k ∈ {5, 10, 20}`; plot ΔS vs k.
2. If curve **flat & high** → metric/normalization/index mismatch.
3. If **sharp drop** at higher k → retriever filter too strict; consider MMR or hybrid.

---

## 4) Prompt assembly: cite → explain (lock constraints)

* Keep **per-source fences** (no cross-source merges).
* **Order**: *system → task → constraints → citations → answer*.
* Force **cite-first**; explanation **must reference** citation IDs/lines.
* See: [Traceability](./retrieval-traceability.md) and *SCU Pattern*.

---

## 5) Reranking: when & how

Add a reranker only if:

* **Recall\@50 ≥ 0.85**, but Top-5 precision is weak, or
* You need **tight citation alignment** across near-duplicates.

Start with:

* **Cross-encoder** (bge-reranker-mini/base) for accuracy;
* Or **LLM rerank** for low volume, high precision needs.
  See: [Rerankers](./rerankers.md).

---

## 6) Acceptance criteria

* **Retrieval sanity**: ΔS(question, top-ctx) ≤ 0.45, coverage ≥ 0.70 of target section.
* **Traceability**: snippet ↔ citation table reproducible.
* **Stability**: same inputs over 3 paraphrases keep λ → convergent.
* **No SCU**: who-said-what does not merge across sources.

---

## 7) Common failures → repair

| Symptom                    | Likely cause                      | Fix                                                                                                              |
| -------------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Hybrid worse than single   | **Analyzer/tokenizer split**      | Align analyzers; log per-retriever queries; see [Query Parsing Split](./patterns/pattern_query_parsing_split.md) |
| Some facts never retrieved | **Fragmented store / id skew**    | Rebuild + shard audit; see [Vectorstore Fragmentation](./patterns/pattern_vectorstore_fragmentation.md)          |
| Citations cross-bleed      | **Prompt schema unlocked**        | Per-source fences + cite-first; see [SCU](./patterns/pattern_symbolic_constraint_unlock.md)                      |
| ΔS flat & high vs k        | **Metric/normalization mismatch** | Normalize embeddings; pin FAISS metric; see [Embedding vs Semantic](./embedding-vs-semantic.md)                  |

---

## 8) Tiny gold set (do this!)

Create **10–50** realistic Q/A with citation lines. Commit a `goldset.jsonl`:

```json
{"q":"How to reset billing cycle?","doc_id":"a","section":"billing","lines":[120,145],"a":"..."}
```

Run **recall\@50**, **nDCG\@10**, and **ΔS** on each PR.

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

