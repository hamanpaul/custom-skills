# Eval Drift — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **RAG**.  
  > To reorient, go back here:  
  >
  > - [**RAG** — retrieval-augmented generation and knowledge grounding](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

> **Evaluation disclaimer (RAG drift)**  
> Drift signals here are measured inside specific RAG pipelines and datasets.  
> They are debugging indicators, not proof that a system will stay stable in all real workloads.

---

When evaluation metrics **swing unpredictably** across runs (precision, recall, ΔS, coverage) even though the data and index appear unchanged.  
This signals **eval drift**: your evaluation harness is not structurally stable.

---

## Open these first
- Recovery overview: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Eval acceptance rules: [Eval — Quality & Readiness Gates](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/README.md)  
- Precision & recall contract: [Eval RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)  
- Ordering control: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
- Pre-deploy safety: [Predeploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)  

---

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45 across 3 paraphrases  
- Coverage ≥ 0.70 per target section  
- λ convergent on 2 seeds, stable across runs  
- Variance of metrics ≤ 0.05 across replays  

---

## Typical symptoms → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Precision/recall varies ±0.20 each run | eval harness non-deterministic | [Eval Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md) |
| Identical queries give different metrics | bootstrap not fenced | [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) |
| Eval metrics collapse on fresh deploy | index not fully warmed | [Predeploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) |
| Coverage < 0.50 despite gold answers | embedding or chunk drift | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) |

---

## Fix in 60 seconds

1. **Lock seeds**  
   Fix random seeds at retrieval, reranker, and eval harness layers.  

2. **Fence bootstrap**  
   Require `VECTOR_READY==true` and index hash match before eval begins.  

3. **Replay 3 paraphrases**  
   Eval the same question with 3 paraphrases. Require ΔS variance < 0.05.  

4. **Cross-seed check**  
   Run two seeds. λ must remain convergent across both.  

5. **Regression gate**  
   Ship only if coverage ≥ 0.70 and precision/recall stable within 0.05.  

---

## Copy-paste eval harness snippet

```python
def eval_guardrails(question, retrieved, gold):
    ds_qr = deltaS(question, retrieved)
    ds_rg = deltaS(retrieved, gold)

    assert ds_qr <= 0.45, "ΔS drift detected"
    assert coverage(retrieved, gold) >= 0.70, "Coverage too low"
    assert lambda_state(retrieved) in {"→","←","<>"} , "λ divergent"

    return {
        "ΔS_qr": ds_qr,
        "ΔS_rg": ds_rg,
        "coverage": coverage(retrieved, gold),
        "λ": lambda_state(retrieved)
    }
````

---

## Diagnostic probes

* **Re-run variance test**: run eval 5 times, log precision/recall. Stddev >0.05 → unstable harness.
* **Anchor comparison**: compare ΔS to gold anchor vs decoy. If both similar, re-embed.
* **Deploy warm-up**: log `VECTOR_READY` and index hash before eval.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

