# Query Parsing Split

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


A field guide to diagnose and fix failures where the same user question turns into different queries across branches. Typical sources are HyDE, rewrite chains, keyword extraction, BM25 analyzers, and tool side expansions. The result is high recall but wrong ordering, unstable answers, or hybrid pipelines that underperform single retrievers.

**Read together with**
- Overview and short route → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-playbook.md)
- Hybrid fusion knobs → [hybrid_retrieval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/hybrid_retrieval.md)
- Ordering control → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)
- Trace and citation schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-traceability.md)
- ΔS probes → [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)
- Chunk window parity → [chunk_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the intended section  
- λ convergent across 3 paraphrases and 2 seeds  
- Dense vs sparse query parity recorded in trace, mismatch rate ≤ 5 percent

---

## Symptoms that point to parsing split

- Dense and sparse branches return different topics that both look relevant.
- Fused results are worse than the best single retriever.
- λ flips only when the HyDE rewrite is enabled or when keyword extraction runs.
- ΔS stays flat and high while top k overlap across branches is below 10 percent.
- Citations show mismatched analyzers or different casing rules.

---

## Canonical causes

1. **HyDE rewrite fed to dense only**  
   Sparse receives the user text while dense uses the hypothetical document.

2. **Keyword extraction fed to sparse only**  
   Dense receives full natural language while sparse gets boolean or phrase queries.

3. **Analyzer mismatch**  
   Lowercase, ascii fold, stemming, and punctuation stripping differ between write and read paths.

4. **Parentheses and operators interpreted differently**  
   Sparse parser treats parentheses and quotes as control tokens while dense treats them as text.

5. **Language mix**  
   Dense model trained on multilingual text while sparse index built with English analyzer.

---

## Unify the query before branching

Define a single normalized query object. Derive branch specific fields from it. Log the object into the trace for audits.

```json
{
  "q_base": "what are the latency limits of vector search on faiss ivf flat",
  "q_hyde": "A technical note that discusses latency limits of vector search using FAISS IVF Flat...",
  "keywords": ["latency", "vector search", "FAISS", "IVF Flat", "limits"],
  "policy": {
    "case": "lower",
    "fold": "ascii",
    "stopwords": "en_smart",
    "stemming": "porter"
  },
  "routing": {
    "dense": {"use": true, "text": "q_hyde"},
    "sparse": {"use": true, "keywords": true, "operator": "OR"}
  }
}
````

**Rules**

* Normalize casing and unicode fold according to `policy`.
* If HyDE is used, either feed the rewrite to both branches or to none.
* If keywords are used for sparse, also pass `q_base` as a soft clause to keep semantic context.
* Record `policy` and `routing` in each citation row.

---

## Minimal recipes

### Python pseudo plan

```python
def normalize_query(user_q, hyde=False, extract_kw=True):
    q_base = ascii_fold(user_q.lower())
    q_hyde = generate_hyde(q_base) if hyde else None
    kws = top_keywords(q_base) if extract_kw else []
    policy = {"case": "lower", "fold": "ascii", "stopwords": "en_smart", "stemming": "porter"}
    return {
        "q_base": q_base,
        "q_hyde": q_hyde,
        "keywords": kws,
        "policy": policy,
        "routing": {
            "dense": {"use": True, "text": q_hyde or q_base},
            "sparse": {"use": True, "keywords": bool(kws), "operator": "OR", "soft": q_base}
        }
    }

def run_branches(plan):
    dense_hits = dense_retriever.invoke(plan["routing"]["dense"]["text"], k=20)
    sparse_hits = bm25(plan["keywords"], operator=plan["routing"]["sparse"]["operator"], soft=plan["routing"]["sparse"]["soft"], k=50)
    return dense_hits, sparse_hits
```

### LCEL outline

```python
# 1) normalize once
# 2) pass the same policy into both branches
# 3) fuse and rerank with deterministic tiebreak
qplan = normalize_query(q, hyde=True, extract_kw=True)
dense = dense_chain.invoke(qplan["routing"]["dense"]["text"])
sparse = bm25_chain.invoke({"keywords": qplan["keywords"], "soft": qplan["q_base"]})
fused = fuse_linear(project(dense), project(sparse), alpha=0.55, k=20)
fused = optional_rerank(fused)
validate_citations(fused, policy=qplan["policy"])
```

### LlamaIndex outline

```python
plan = normalize_query(q, hyde=False, extract_kw=True)
dense = vector_index.as_retriever(similarity_top_k=20).retrieve(plan["routing"]["dense"]["text"])
sparse = bm25_retriever.retrieve(plan["keywords"], top_k=50, soft=plan["q_base"])
fused = fuse_linear(project(dense), project(sparse), alpha=0.6, k=20)
```

---

## ΔS and λ probes for parsing split

1. Run with HyDE off and log ΔS and λ.
2. Run with HyDE on for both branches and log again.
3. Run with HyDE on for dense only and compare. If this variant is worse while single dense is fine, the split is confirmed.
4. Compute top k overlap between branches. If below 10 percent and ΔS is flat, fix routing.

Helper → [deltaS\_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)

---

## Typical failures and exact fixes

* **Fused results worse than single**
  Normalize query, use the same rewrite for both branches, then fuse.
  Open: [hybrid\_retrieval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/hybrid_retrieval.md)

* **Sparse ignores important terms after rewrite**
  Keep the base text as a soft clause with lower weight.
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-playbook.md)

* **Citations show analyzer mismatch**
  Align analyzer and restamp the index.
  Open: [chunk\_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

* **Order flips between runs**
  Add cross encoder rerank and deterministic tiebreak.
  Open: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)

* **High similarity but wrong meaning**
  Rebuild with correct metric and pooling.
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Evaluation checklist

* Three paraphrases per question.
* Single dense, single sparse, fused.
* Record query object, policy, and routing.
* Target improvement for fused vs best single: ΔS drop by at least 0.05 and coverage rise by at least 0.05.
* Store the plan and results with a regression gate in CI.

---

## Copy paste validator prompt

```txt
You have TXTOS and the WFGY Problem Map loaded.

My issue is query parsing split. Current data:
- user question: "<text>"
- plan: {q_base, q_hyde, keywords, policy, routing}
- results: ΔS_dense=..., ΔS_sparse=..., ΔS_fused=..., topk_overlap=...

Return:
1) whether the plan keeps parity across dense and sparse,
2) the exact normalization and routing changes to try,
3) which fusion method and α or RRF k to use,
4) a JSON object to log in each citation row to keep audits stable.
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

