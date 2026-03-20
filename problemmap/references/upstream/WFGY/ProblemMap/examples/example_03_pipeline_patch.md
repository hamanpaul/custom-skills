# Example 03 — Pipeline Patch: Intersection + Rerank (No.1 & No.4)

**Goal**  
Harden retrieval so answers cite the **right** chunks. We combine lexical and semantic views, take the **intersection** (with a safe fallback), then **rerank** by cosine and **cut the tail** at the score knee.

**Problem Map link**  
- **No.1 Hallucination & Chunk Drift** — wrong spans sneak in when chunk borders don’t match entities/constraints.  
- **No.4 Tail Noise** — low-relevance passages dilute the prompt and push the model to stitch.

**Outcome**  
- Higher citation hit rate and fewer off-topic chunks in the prompt  
- Same token budget, better signal  
- Deterministic selection rules you can tune and test

---

## 1) Inputs

Use the same structure as Example 01:
- `data/chunks.json` — array of `{id, page, text}`  
- You can keep the tiny toy corpus or point to your own

> Tip: If your corpus is large, run this on a 200–500 chunk slice first to verify behavior.

---

## 2) Path A — Python (rank-bm25 + sentence-transformers, CPU-friendly)

### Install

```bash
pip install numpy rank-bm25 sentence-transformers faiss-cpu
````

### Script: `hybrid_retrieve.py`

```python
# hybrid_retrieve.py -- lexical ∩ semantic -> rerank -> knee cutoff
import json, os, sys, math
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import faiss

TOPK_LEX = 40      # lexical candidate pool
TOPK_SEM = 40      # semantic candidate pool
TOPK_FINAL = 8     # final picks after rerank
KNEE_MIN = 4       # at least this many survive before knee

def load_chunks(path):
    C = json.load(open(path, encoding="utf8"))
    texts = [c["text"] for c in C]
    ids = [c["id"] for c in C]
    return C, texts, ids

def build_lex(texts):
    toks = [t.lower().split() for t in texts]
    return BM25Okapi(toks), toks

def build_sem(texts):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embs = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs.astype(np.float32))
    return model, embs, index

def score_lex(bm25, toks, q):
    return bm25.get_scores(q.lower().split())

def score_sem(model, index, q, topn):
    qv = model.encode([q], normalize_embeddings=True)
    sim, idx = index.search(qv.astype(np.float32), topn)
    return sim[0], idx[0]

def knee_cut(scores_sorted_desc, min_keep=KNEE_MIN):
    """Find largest drop (relative) to cut the tail. Always keep at least min_keep."""
    if len(scores_sorted_desc) <= min_keep:
        return len(scores_sorted_desc)
    drops = []
    for i in range(1, len(scores_sorted_desc)):
        prev, cur = scores_sorted_desc[i-1], scores_sorted_desc[i]
        if prev <= 1e-9: drops.append(0.0)
        else: drops.append((prev - cur) / max(prev, 1e-9))
    knee = max(range(1, len(scores_sorted_desc)), key=lambda i: drops[i-1])
    return max(min_keep, knee)

def retrieve_hybrid(chunks, texts, ids, bm25, toks, model, index, q):
    # 1) lexical top pool
    lex_scores = score_lex(bm25, toks, q)
    lex_top_idx = np.argsort(lex_scores)[::-1][:TOPK_LEX]

    # 2) semantic top pool
    sem_sims, sem_idx = score_sem(model, index, q, TOPK_SEM)
    sem_top_idx = sem_idx

    # 3) intersection, then union fallback
    cand = list(set(lex_top_idx).intersection(set(sem_top_idx)))
    if len(cand) < TOPK_FINAL:
        cand = list(set(list(lex_top_idx) + list(sem_top_idx)))

    cand = np.array(cand)
    # 4) rerank by cosine against query vector
    qv = model.encode([q], normalize_embeddings=True)[0]
    embs = index.reconstruct_n(0, index.ntotal)  # faiss flat, safe to reconstruct
    sims = embs[cand] @ qv

    order = np.argsort(sims)[::-1]
    cand, sims = cand[order], sims[order]

    # 5) knee cutoff then top K
    keep = knee_cut(sims.tolist(), min_keep=min(KNEE_MIN, TOPK_FINAL))
    picks = cand[:max(keep, TOPK_FINAL)][:TOPK_FINAL]
    out = [{"id": ids[i], "text": texts[i], "score": float(sims[list(cand).index(i)])} for i in picks]
    return out

def main(chunks_path, query):
    chunks, texts, ids = load_chunks(chunks_path)
    bm25, toks = build_lex(texts)
    model, embs, index = build_sem(texts)
    picks = retrieve_hybrid(chunks, texts, ids, bm25, toks, model, index, query)
    print(json.dumps({"q": query, "picks": picks}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python hybrid_retrieve.py data/chunks.json \"your question\"")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
```

### Run

```bash
python hybrid_retrieve.py data/chunks.json "What is X and how is it constrained?"
```

**Pass criteria**

* The output `picks` includes the chunk(s) that actually define X
* Low-signal paragraphs (e.g., “unrelated protocol”) should be cut by the knee

---

## 3) Path B — Node (no external packages, CPU-only)

We’ll keep Node dependency-free for portability.
For real workloads, swap in `@xenova/transformers` for embeddings and a BM25 lib; the logic stays identical.

### Script: `hybrid_retrieve.mjs`

```js
// hybrid_retrieve.mjs -- lexical overlap ∩ simple semantic → rerank → knee
import fs from "node:fs";

// --- tiny helpers (dependency-free) ---
function tokenize(s) { return s.toLowerCase().split(/\W+/).filter(Boolean); }
function dot(a,b){ let s=0; for(let i=0;i<a.length;i++) s+=a[i]*b[i]; return s; }
function norm(a){ return Math.sqrt(dot(a,a)) || 1; }
function cosine(a,b){ return dot(a,b)/(norm(a)*norm(b)); }

// naive "embedding": average of hashed one-hot bins (works as a stand-in)
const D = 512;
function hashEmbed(text){
  const v = new Array(D).fill(0);
  for(const w of tokenize(text)){
    const h = Math.abs([...w].reduce((a,c)=>((a<<5)-a + c.charCodeAt(0))|0, 0)) % D;
    v[h] += 1;
  }
  // l2 normalize
  const n = norm(v); return v.map(x => x/n);
}

function bm25Lite(queryTokens, docTokens, avgdl, k1=1.5, b=0.75){
  // very lite BM25: IDF omitted here; we approximate with normalized term overlap + length norm
  const overlap = docTokens.filter(t => queryTokens.has(t)).length;
  const dl = docTokens.length || 1;
  const num = overlap * (k1 + 1);
  const den = overlap + k1 * (1 - b + b * (dl / avgdl));
  return den ? num/den : 0;
}

function kneeCut(scoresDesc, minKeep=4){
  if(scoresDesc.length <= minKeep) return scoresDesc.length;
  let best=1, bestDrop=-1;
  for(let i=1;i<scoresDesc.length;i++){
    const prev = scoresDesc[i-1], cur = scoresDesc[i];
    const drop = (prev - cur) / Math.max(prev, 1e-9);
    if(drop > bestDrop){ bestDrop = drop; best = i; }
  }
  return Math.max(minKeep, best);
}

// --- main hybrid ---
function hybridRetrieve(chunks, q, TOPK_LEX=40, TOPK_SEM=40, TOPK_FINAL=8){
  const qTok = new Set(tokenize(q));
  const tokens = chunks.map(c => tokenize(c.text));
  const avgdl = tokens.reduce((a,t)=>a+t.length,0) / Math.max(tokens.length,1);

  // lexical pool
  const lexScores = tokens.map(t => bm25Lite(qTok, t, avgdl));
  const lexOrder = [...lexScores.keys()].sort((a,b)=>lexScores[b]-lexScores[a]).slice(0, TOPK_LEX);

  // semantic pool (hash embeddings as stand-in; replace with real model later)
  const embs = chunks.map(c => hashEmbed(c.text));
  const qv = hashEmbed(q);
  const semScores = embs.map(v => cosine(v, qv));
  const semOrder = [...semScores.keys()].sort((a,b)=>semScores[b]-semScores[a]).slice(0, TOPK_SEM);

  // intersection then union fallback
  const setLex = new Set(lexOrder), setSem = new Set(semOrder);
  let cand = [...new Set(lexOrder.filter(i => setSem.has(i)))];
  if(cand.length < TOPK_FINAL) cand = [...new Set([...lexOrder, ...semOrder])];

  // rerank by cosine, knee cutoff
  const rescored = cand.map(i => [i, semScores[i]]).sort((a,b)=>b[1]-a[1]);
  const scores = rescored.map(x => x[1]);
  const keep = kneeCut(scores, Math.min(4, TOPK_FINAL));
  const picks = rescored.slice(0, Math.max(keep, TOPK_FINAL)).slice(0, TOPK_FINAL).map(([i,s]) => ({
    id: chunks[i].id, text: chunks[i].text, score: s
  }));
  return picks;
}

// CLI
if (import.meta.url === `file://${process.argv[1]}`) {
  const [chunksPath, ...qparts] = process.argv.slice(2);
  if (!chunksPath || qparts.length === 0) {
    console.error("usage: node hybrid_retrieve.mjs data/chunks.json \"your question\"");
    process.exit(1);
  }
  const chunks = JSON.parse(fs.readFileSync(chunksPath,"utf8"));
  const q = qparts.join(" ");
  const picks = hybridRetrieve(chunks, q);
  console.log(JSON.stringify({ q, picks }, null, 2));
}

export { hybridRetrieve };
```

### Run

```bash
node hybrid_retrieve.mjs data/chunks.json "What is X and how is it constrained?"
```

**Pass criteria** are the same as Python.
When you later swap in real embeddings, the behavior should improve while the control logic stays unchanged.

---

## 4) Wire into your guarded answer (from Example 01)

**Python** — replace your `retrieve()` with the hybrid function (keep the same prompt and trace rules).
**Node** — import `hybridRetrieve` and use its `picks` as your `chunks` in the prompt builder.

---

## 5) Verification checklist

* **Citation hit rate** increases (more answers cite the defining chunk ids)
* **Refusal is correct** when no relevant evidence exists
* **Prompt length** stays the same or shrinks (top-8 is enough after rerank)
* **Variance** across runs reduces (intersection stabilizes candidate set)

A quick way to confirm: re-run the triage from **Example 02**. You should see fewer `retrieval_drift` labels.

---

## 6) Why this works (in one paragraph)

Lexical scores reward explicit keyword overlap; semantic scores capture paraphrases and synonyms.
Taking the **intersection** forces candidates to be good in **both** views (high precision); when the intersection is too small, a **union fallback** avoids false refusals (recall).
A **cosine rerank** against the query enforces semantic closeness across mixed candidates, and the **knee cutoff** removes the low-value tail that tends to cause stitching.
You get a clean, testable selection before you ever call the model.

---

## 7) Common mistakes & quick fixes

* **Intersection returns 0** → increase the lexical/semantic pools to 80/80, or relax stopword removal.
* **Knee cuts too aggressively** → lower the drop sensitivity by requiring a larger relative drop (or set `KNEE_MIN = TOPK_FINAL`).
* **Still seeing off-topic chunks** → reduce chunk size so entity and constraints sit together; large chunks blur the signal.
* **Latency too high** → cache embeddings; prebuild FAISS; keep models in memory and warm them before serving (see Example 07).

---

## 8) Next steps

* Add a lightweight **cross-encoder reranker** (CPU-friendly) and compare with the cosine rerank.
* Move to **Eval** docs and measure changes on precision, refusal rate, and citation overlap across your question set.
* If you run on Ollama/LangChain, keep this control logic; just swap the embedding/model backends.

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

