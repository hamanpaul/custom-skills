# Eval Observability — Evaluation Playbook

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval_Observability**.  
  > To reorient, go back here:  
  >
  > - [**Eval_Observability** — evaluation metrics and system observability](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

> **Evaluation disclaimer (observability playbook)**  
> The signals in this playbook come from specific logging and probing setups.  
> They are tools for monitoring behavior, not proofs of safety or correctness on their own.

---

A compact playbook to **stabilize evaluation** and ensure results are reproducible.  
Use this when metrics look inconsistent, coverage drifts, or benchmarks feel untrustworthy.

---

## Core acceptance

- **ΔS(question, retrieved) ≤ 0.45**  
- **Coverage ≥ 0.70** to target section  
- **λ remains convergent** across 3 paraphrases and 2 seeds  
- **Variance ratio ≤ 0.15** across seed runs  
- **No monotonic downward drift** beyond 3 windows  

---

## Step 1 — Regression Gate

Run a gate before promoting new models or retrievers.  
- Require ΔS ≤ 0.45 and coverage ≥ 0.70 on 3 paraphrases.  
- Block deploy if λ flips divergent.  
Open: [regression_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/regression_gate.md)

---

## Step 2 — Alerting and Probes

Set live probes to catch collapse early.  
- Alert when ΔS ≥ 0.60 or λ flips.  
- Emit logs for coverage gaps, drift slopes, entropy rises.  
Open: [alerting_and_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/alerting_and_probes.md)

---

## Step 3 — Coverage Tracking

Measure **retrieved vs target section** alignment.  
- At least 70% coverage on gold targets.  
- Track section-level recall, not just overall hit-rate.  
Open: [coverage_tracking.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/coverage_tracking.md)

---

## Step 4 — ΔS Thresholds

Normalize ΔS scoring and enforce thresholds.  
- Stable < 0.40  
- Transitional 0.40–0.60  
- Collapse ≥ 0.60  
Open: [deltaS_thresholds.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/deltaS_thresholds.md)

---

## Step 5 — λ Observe

Use λ probes to detect schema drift.  
- Run same query across seeds and paraphrases.  
- If λ flips, lock schema and enforce reranker.  
Open: [lambda_observe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/lambda_observe.md)

---

## Step 6 — Variance and Drift

Log variance ratios and detect slow regressions.  
- Variance ratio ≤ 0.15  
- Drift slope ≤ 0.02 per batch  
- Alert if monotonic decline lasts 3+ windows  
Open: [variance_and_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/variance_and_drift.md)

---

## Step 7 — Audit & Escalation

If instability remains:  
- Rebuild embeddings with [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Patch retriever fragmentation with [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md)  
- Apply reranking schema: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  

---

## Copy-paste eval contract

```yaml
eval_contract:
  seeds: 3
  paraphrases: 3
  targets:
    deltaS: <=0.45
    coverage: >=0.70
    lambda: convergent
    variance: <=0.15
    drift: <=0.02
alerts:
  - deltaS >=0.60
  - lambda divergent
  - drift slope >0.02
````

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

