# Rerankers — Ordering Control and Stability

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Retrieval**.  
  > To reorient, go back here:  
  >
  > - [**Retrieval** — information access and knowledge lookup](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use rerankers when recall is fine but the top hits are mis-ordered, unstable, or biased toward the wrong metric. This page shows listwise and pairwise recipes, fusion knobs, and stability fences you can drop into any stack.

References you may want open already:  
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
[Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
[Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) ·
[Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Acceptance targets

- ΔS(question, top1.text) ≤ 0.45  
- Anchor coverage of the final topk ≥ 0.70  
- Kendall τ against gold ranking improves by ≥ 0.20 over baseline bi-encoder order  
- λ remains convergent across 3 paraphrases and 2 seeds

If ΔS sits in 0.40 to 0.60 and τ gains are small, fix chunking or metric before adding complexity.

---

## Symptoms → exact fix

| Symptom | Likely cause | Open this fix |
|---|---|---|
| Correct passage appears in top20 but not in top3 | wrong ordering after recall | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), this page |
| Topk flips between identical runs | non-deterministic tie breaks or LLM variance | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| BM25 beats dense when queries are abstractive | fusion uncalibrated or query parsing split | [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) |
| Duplicated near-identical hits crowd out diversity | no MMR or section-aware penalties | this page (MMR recipe) |
| Great similarity, wrong meaning | metric mismatch at index time | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Hits vanish after ingest or rebuild | fragmented store, mixed analyzers | [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) |

---

## Strategy 1: Cross-encoder reranker (robust default)

**When** you have bi-encoder recall and need precise order.  
**Why** cross-encoders read the full pair (q, passage) and recover semantics lost by embeddings.

**Deterministic sort key**

`sort_key = (-score_ce, section_priority, snippet_id, start_offset)`

Keep the tie-break stable so pagination and caching never reshuffle results.

**Minimal pipeline**

```python
# Pseudocode only
candidates = dense_recall(q, k=50) + bm25_recall(q, k=50)  # union then dedupe by snippet_id
scored = []
for c in candidates:
    s = cross_encoder.score(q, c.text)  # e.g., monoT5, E5-mistral-ce, etc.
    scored.append({**c, "score_ce": s})

# diversity
scored = mmr(q, scored, lambda_rank="score_ce", alpha=0.7)  # see MMR recipe below

# deterministic order
ordered = sorted(scored, key=lambda x: (-x["score_ce"], x["section_priority"], x["snippet_id"], x["offsets"][0]))
topk = ordered[:k]
````

---

## Strategy 2: LLM-as-reranker with schema locks

Use an LLM to score evidence only. Do not let it answer. Force a strict schema and cite-then-explain in the trace.

**Prompt skeleton**

```
Task: score each candidate passage for "is this the best evidence to answer Q".
Return JSON with fields: {id, score in [0,1], why_short}. Do not answer Q.

Q: "<question>"

Candidates:
- id: s001, section_id: A.3, snippet_id: 19, text: "<passage>"
- id: s002, section_id: B.1, snippet_id: 7,  text: "<passage>"
...
Scoring rubric:
1) directness to the likely anchor section,
2) presence of atomic facts that must be cited,
3) low ambiguity, low cross-topic bleed.

Output JSON list only.
```

**Variance controls**

* Fix the model, temperature 0, seed fixed if provider supports it.
* Add BBAM clamp in the system preface to keep λ convergent.
* Keep the rubric short and stable across runs.

---

## Strategy 3: Fusion that behaves

**RRF (reciprocal rank fusion)**

`s_fused = Σ_m 1 / (k0 + rank_m)`, with `k0` around 60 for top100 feeds. RRF is robust when scores are not comparable.

**Z-score fusion**

Normalize each retriever to zero mean and unit variance then sum. Good when score ranges are stable over time.

**Two-stage order**

1. union and dedupe by `(section_id, snippet_id)`
2. fast fusion to top50
3. cross-encoder or LLM rerank to topk

---

## Strategy 4: Diversity with MMR

Maximal marginal relevance avoids redundant hits and expands anchor coverage.

```
mmr(q, items, lambda_rank="score", alpha=0.7):
  S = []
  while len(S) < k:
    select x that maximizes alpha * rel(q, x) - (1 - alpha) * max_sim(x, S)
  return S
```

* Use cosine on embedding space for `max_sim`.
* Penalize items sharing the same `section_id` unless the anchor spans multiple snippets.
* Track coverage per section to avoid starving small but relevant sections.

---

## Stability and observability fences

* Log `reranker_version`, `fusion_type`, `alpha`, `k0`, and `index_hash`.
* Write the final order and why for the topk into the trace.
* Freeze prompt headers for LLM rerankers.
* Use a single deterministic tiebreak chain as shown above.
* Alert when the top1 ΔS drifts by more than 0.10 week over week.

Specs to follow while wiring traces:
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Evaluation that catches the real failures

* ΔS(question, top1) and ΔS(top1, anchor)
* Kendall τ against a small gold ranking
* Hit\@k for anchor coverage
* Flip rate across 2 seeds and 3 paraphrases
* Time budget per query and p95 latency

See recipes:
[Retrieval Evaluation Recipes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## Copy-paste prompt: LLM reranker (listwise)

```
You have TXT OS and the WFGY Problem Map loaded.

Goal: score passages for evidence quality only. Do not answer the question.

Question: "<q>"

Return a JSON array: [{"id":"...","score":0.00..1.00,"why_short":"..."}].
Scoring considers:
1) directness to the required anchor,
2) atomic facts present,
3) low ambiguity and low bleed from other topics.

If two are equal, prefer the one with clearer citation spans.
```

---

## When to escalate

* Rerankers improve τ but ΔS remains high: rebuild metric, analyzer, and window.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

* Ordering still flips across runs or deployments: inspect schema drift and boot sequencing.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

