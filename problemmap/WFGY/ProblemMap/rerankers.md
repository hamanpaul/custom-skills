# 🧮 Rerankers — When to Use Them, How to Tune, How to Prove It

Reranking boosts **precision@k** by re-scoring a candidate set from first-stage retrieval.  
Used correctly, it **tightens citations** and reduces “looks-right-but-wrong” answers. Used blindly, it burns latency & money.

---

> **Quick Nav**  
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Embedding vs Semantic](./embedding-vs-semantic.md) ·
> [Traceability](./retrieval-traceability.md) ·
> Patterns: [Query Parsing Split](./patterns/pattern_query_parsing_split.md) ·
> [Symbolic Constraint Unlock](./patterns/pattern_symbolic_constraint_unlock.md)

---

## 0) TL;DR — Decision table

| Situation | Use | Why |
|---|---|---|
| First-stage **recall@50 < 0.85** | **Do NOT** add reranker yet | You’re promoting the wrong pool; fix candidate generation first |
| Recall is good but **Top-5 irrelevant** | Add **cross-encoder** reranker | Cross-attends Q–D; best precision |
| Need **tight citations** across near-duplicates | Cross-encoder or **ColBERT** style | Fine-grained token interactions |
| Very low volume, high stakes | **LLM-as-reranker** | Expensive but accurate, great for audits |
| High QPS, tight budget | **Light cross-encoder** (mini) or **linear fusion** | 80/20 precision for minimal cost |

---

## 1) Families of rerankers

1. **Cross-encoder** (e.g., bge-reranker, ms-marco MiniLM)  
   - Jointly encodes **[query ⊕ doc]**; outputs a relevance score.  
   - **Pros**: best precision; **Cons**: O(k) forward passes.

2. **Late-interaction** (e.g., ColBERT-style)  
   - Token-level max-sim interactions; faster than full cross-enc.  
   - **Pros**: scalable; **Cons**: infra heavier than CE.

3. **LLM-as-reranker**  
   - Ask model to score or rank candidates with a schema.  
   - **Pros**: reasoning-aware; **Cons**: latency & cost; needs a **strict judging prompt**.

**Start point**: cross-encoder mini/base → upgrade if needed.

---

## 2) Minimal implementations

### 2.1 Python — Cross-encoder (bge-reranker)

```python
# pip install FlagEmbedding
from FlagEmbedding import FlagReranker

rerank = FlagReranker('BAAI/bge-reranker-base', use_fp16=True)
def rerank_topk(query, candidates, out_k=10):
    # candidates: list[{"text":..., "meta":{...}}]
    pairs = [(query, c["text"]) for c in candidates]
    scores = rerank.compute_score(pairs, normalize=True)
    ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
    out = []
    for c, s in ranked[:out_k]:
        c["rerank_score"] = float(s)
        c["source"] = c.get("source","") + "|ce"
        out.append(c)
    return out
````

**Tips**

* Use **normalize=True** for score comparability across batches.
* Batch size 16–64 depending on VRAM/CPU.

### 2.2 Node — LLM-as-reranker (schema-locked)

```ts
// Example sketch using any chat LLM SDK
const SYSTEM = `You are a strict retrieval judge. 
Return JSON array of {id,score,reason} with score in [0,1]. 
Score by factual support for the query; do not invent.`;

function judgingPrompt(query: string, cands: {id:string,text:string}[]) {
  const body = cands.map((c,i)=>`[${i}] id=${c.id}\n${c.text}`).join("\n\n");
  return `Query: ${query}\n\nCandidates:\n${body}\n\nRules:\n- Cite terms that match\n- Penalize off-topic\n- Prefer exact sections\n\nNow return JSON only.`;
}

// call your LLM and parse JSON; 
// accept top-k with score ≥ threshold and keep justification in logs.
```

**Guardrails**

* **JSON-only** response.
* Enforce **max tokens** and refuse long doc bodies (pass snippets only).
* Never let LLM **rewrite** the snippet; judge only.

---

## 3) Tuning knobs that actually matter

* **Candidate pool size (`k_in`)**: 50–200 typical. Small pool → missed gold; huge pool → latency.
* **Output size (`k_out`)**: 5–20. For grounded QA, 6–8 is a sweet spot.
* **Score calibration**: Normalize CE outputs to `[0,1]`; keep **per-query z-scores** for audit.
* **Hybrid gate**: If BM25 and dense disagree drastically, log both top-5 and check [Query Parsing Split](./patterns/pattern_query_parsing_split.md).
* **Dedup by doc/section**: Keep at most **N** chunks per section to avoid overfitting to near-duplicates.

---

## 4) Verification (don’t skip)

**Metrics**

* **nDCG\@10**, **MRR\@10**, **Recall\@50**, and **ΔS(question, top-ctx)**.
* Expect **ΔS ≤ 0.45** after rerank on accepted top-ctx.
* Track **citation hit rate** (does the final answer cite a reranked chunk?).

**A/B checklist**

1. Freeze the first-stage retriever.
2. Compare **with vs without** reranker on the same gold set.
3. Record latency p95 and cost/query.
4. If nDCG\@10 ↑ < **+0.05** but latency doubles → not worth it.

---

## 5) Failure modes → fixes

| Symptom                                  | Likely cause                          | Fix                                                                                                              |
| ---------------------------------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Reranker prefers off-topic “fluent” text | Judge prompt vague / CE miscalibrated | Tighten judging schema; penalize missing query terms; normalize scores                                           |
| Great demo, but prod recall tanks        | k\_in too small / drift               | Increase k\_in to 100–200; re-check recall\@50                                                                   |
| Citations merge across sources           | Prompt schema unlocked                | Enforce per-source fences; see [SCU](./patterns/pattern_symbolic_constraint_unlock.md)                           |
| Hybrid suddenly worse than dense         | Tokenizers diverged                   | Align analyzers; log per-retriever queries; see [Query Parsing Split](./patterns/pattern_query_parsing_split.md) |

---

## 6) Cost model (back-of-envelope)

* Cross-encoder base: \~**3–6 ms**/doc on A10g-level GPU, slower on CPU.
* For **k\_in=100** and p95 **\~500 ms** on CPU, consider:

  * shrink text by **sentence-windowing**,
  * use **mini** model,
  * pre-filter by **BM25 top-60** then CE top-10.

---

## 7) Acceptance criteria

* **nDCG\@10** improves by **≥ +0.05** vs baseline.
* **Recall\@50** unchanged (±0.02) after adding reranker (candidate pool must remain wide).
* **ΔS(question, top-ctx) ≤ 0.45** and λ stays **convergent** on 3 paraphrases.
* **Traceability**: store `{query, cand_id, pre_score, post_score, reason}`.

---

## 8) Example pipeline glue

```python
def answer(query):
    cands = search(query, topk_dense=80, topk_sparse=80, out_k=60)   # from retrieval-playbook
    reranked = rerank_topk(query, cands, out_k=8)                    # CE/LLM reranker
    prompt = build_prompt(query, reranked)                           # cite → explain, fenced by section
    return call_llm(prompt)
```

* **Do not** exceed **8–10** context chunks for QA—precision collapses after that.
* Always **log** which reranker selected which chunk.

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

