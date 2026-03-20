# Eval RAG Precision & Recall — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval**.  
  > To reorient, go back here:  
  >
  > - [**Eval** — model evaluation and benchmarking](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

> **Evaluation disclaimer (RAG precision and recall)**  
> Precision and recall here are computed in a controlled RAG scenario with specific data and judgement rules.  
> They should be used to debug retrieval behavior, not as general claims about model intelligence.

---

This page defines how to measure **precision and recall** in RAG pipelines under the WFGY framework. It sets acceptance thresholds, common pitfalls, and structural fixes to keep evaluations meaningful and reproducible.

---

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval contract: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Embedding drift: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Hallucination boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

---

## Acceptance targets

* **Precision ≥ 0.75** at citation level
* **Recall ≥ 0.70** of gold anchor snippets
* **ΔS(question, retrieved) ≤ 0.45** for majority of pairs
* **λ remains convergent** across 3 paraphrases and 2 random seeds
* Evaluations must be **auditable & reproducible** with JSON logs

---

## Why precision/recall break in RAG

1. **Goldset drift**
   Anchors no longer align with the corpus after updates.
   → Fix: refresh goldsets with [goldset\_curation.md](./goldset_curation.md).

2. **Retrieval contract missing**
   Snippet payloads do not include section IDs or offsets.
   → Fix: enforce [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Precision false positives**
   Semantically near matches but wrong factual anchor.
   → Fix: rerank with [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

4. **Recall false negatives**
   Correct snippet exists but chunking or index prevents surfacing.
   → Fix: re-chunk corpus with [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md).

5. **Evaluation noise**
   Different seeds or paraphrases give unstable results.
   → Fix: clamp λ variance with [variance\_and\_drift.md](../Eval_Observability/variance_and_drift.md).

---

## Quick workflow

1. **Load goldset**
   Each gold QA item must cite `snippet_id`, `section_id`, `source_url`.

2. **Run retrieval**
   Collect top-k results (k = 5, 10, 20).

3. **Log ΔS & λ**
   For each query and paraphrase, record ΔS values and λ states.

4. **Compute metrics**

   * Precision = correct citations / total citations
   * Recall = correct citations / gold references

5. **Regression gate**
   Block deploy if precision < 0.75 or recall < 0.70.

---

## Example JSON log

```json
{
  "question": "What causes hallucination re-entry?",
  "gold": ["hallucination-reentry"],
  "retrieved": ["hallucination-reentry", "entropy-drift"],
  "precision": 0.50,
  "recall": 1.00,
  "ΔS": 0.38,
  "λ_state": "→"
}
```

---

## Common pitfalls

* **Evaluating only precision** → recall collapses unnoticed.
* **Counting fuzzy hits** as correct → ΔS may be high, but factually wrong.
* **No paraphrases tested** → λ instability hidden.
* **Relying on one seed** → fragile numbers that don’t generalize.

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

