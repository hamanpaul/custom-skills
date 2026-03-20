# ΔS Probes for Retrieval and Reasoning Stability

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

> **Evaluation disclaimer (ΔS probes)**  
> ΔS based probes are WFGY diagnostic tools for tension in retrieval behavior.  
> They highlight suspicious regions but do not by themselves prove that a system is correct or incorrect.

---

A compact playbook to measure semantic distance and catch failure modes before they surface in answers. Run these probes store-agnostic and model-agnostic. Use the readings to route fixes to the right WFGY pages.

## What ΔS tells you

- **ΔS(question, retrieved)** measures semantic tension between the user question and the assembled retrieval context.
- **ΔS(retrieved, anchor)** measures how well the retrieved context aligns to the expected ground section.
- Combined with **λ\_observe** you can separate metric mismatches from prompt variance and ordering issues.

## Targets and thresholds

- **Pass**: ΔS(question, retrieved) < 0.40  
- **Transitional**: 0.40 ≤ ΔS < 0.60  
- **Risk**: ΔS ≥ 0.60  
- Coverage to target section ≥ 0.70  
- λ remains convergent across 3 paraphrases and 2 seeds

Reference playbooks:  
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Probe pack you should always run

1) **Paraphrase sweep**  
   Ask the same question three ways. Record ΔS and λ for each.  
   If λ flips on harmless paraphrases with small ΔS changes, clamp variance and lock prompt headers.  
   Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

2) **Seed sweep**  
   Run with two random seeds and keep the retrieval order fixed.  
   If answers flip with stable ΔS, add a deterministic reranker.  
   Open: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

3) **k sweep**  
   Try k in {5, 10, 20}. If ΔS stays flat and high while coverage is low, suspect metric or index mismatch.  
   Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

4) **Anchor triangulation**  
   Compare ΔS against the correct section and one decoy section.  
   If ΔS is close for both, realign chunking and anchors.  
   Open: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) ·
   [chunk_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

5) **Hybrid split check**  
   If hybrid underperforms a single retriever, split parsing and rebalance.  
   Open: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

6) **Fragmentation probe**  
   If ΔS looks fine on small tests but coverage collapses in production, check for store fragmentation or namespace skew.  
   Open: [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Minimal implementation you can paste

```python
# Pseudocode: model and store agnostic
def deltaS(a, b):
    # plug your semantic distance, normalized to [0,1]
    return metric.distance(a, b)

def probe_once(question, retrieved, anchor, seed=None):
    d_qr = deltaS(question, retrieved)
    d_ra = deltaS(retrieved, anchor) if anchor else None
    lam = observe_lambda(question, retrieved, seed=seed)  # convergent | divergent
    return {"ΔS_qr": d_qr, "ΔS_ra": d_ra, "λ_state": lam}

def run_probes(q, paraphrases, seeds, ks, anchor):
    logs = []
    for p in paraphrases:
        for k in ks:
            ctx = retriever.invoke(p, k=k)
            for s in seeds:
                logs.append(probe_once(p, ctx, anchor, seed=s))
    return logs
````

**What to record**

* Question form, seed, k
* ΔS(question, retrieved), ΔS(retrieved, anchor)
* λ\_state per run and final coverage
* Retrieval order and analyzer/metric identifiers
* Prompt header hash and template revision

Schema reference:
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Reading the patterns

* **ΔS high across paraphrases and seeds**
  Likely metric or family mismatch. Rebuild with a single embedding family and explicit normalization.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **ΔS improves with higher k but answers still flip**
  Ordering variance. Add a deterministic reranker and freeze prompt headers.
  Open: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **ΔS low but citations unstable**
  Schema not enforced or formatter renamed fields. Tighten contracts and fail fast.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **ΔS near equal to anchor and decoy**
  Chunk boundaries misaligned or anchors missing. Re-chunk with anchors and rebuild.
  Open: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) ·
  [chunk\_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)

* **ΔS oscillates with paraphrase, λ flips**
  Prompt variance and entropy. Clamp with BBAM, then stabilize chain layout.
  Open: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## Verification loops

* Evaluate after each change with a small gold set and keep ΔS logs alongside coverage.
  Open: [retrieval\_eval\_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

* Keep a regression gate: ΔS ≤ 0.45 and coverage ≥ 0.70 on three paraphrases before you ship.
  Open: [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Common gotchas

* Mixed analyzers or distance metrics between write and read paths.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Inconsistent casing or tokenization in HyDE versus dense path.
  Open: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* Live tests run before index is ready or version hash mismatched.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

要繼續下一頁請回「GO 3」。
