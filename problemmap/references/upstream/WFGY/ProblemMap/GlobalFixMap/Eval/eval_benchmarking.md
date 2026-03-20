# Eval Benchmarking — Protocols, Targets, and Reporting

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

> **Evaluation disclaimer (benchmarking)**  
> All scores and examples on this page are scenario specific debug signals.  
> They are not an official leaderboard or scientific proof and do not show that one model is always better.  
> Use them as local guidance for your own stack and re run the setup when you change models, data or prompts.

---

This page defines a clean, repeatable way to benchmark your pipeline and prove that a fix actually improved behavior. It uses the same WFGY instruments as everywhere else: ΔS for semantic stress, λ\_observe for stability, and E\_resonance for coherence over long windows.

## Open these first

* RAG map and recovery path: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Eval playbook and gates: [Eval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/eval_playbook.md) · [Regression Gate](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/regression_gate.md)
* ΔS and λ instruments: [deltaS\_thresholds.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/deltaS_thresholds.md) · [lambda\_observe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/lambda_observe.md)
* Coverage and drift: [coverage\_tracking.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/coverage_tracking.md) · [variance\_and\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/variance_and_drift.md)
* Gold construction: [Goldset Curation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/goldset_curation.md)
* Precision and recall: [Eval RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/eval_rag_precision_recall.md)
* Public benchmark page: [Benchmark vs GPT-5](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)

---

## Acceptance targets

Benchmark runs are accepted when all of the following pass:

* **Precision ≥ 0.80** on cited snippets
* **Recall ≥ 0.70** to target sections
* **ΔS(question, cited) ≤ 0.45** for 80 percent of pairs
* **λ remains convergent** across three paraphrases and two seeds
* **Run to run variance ≤ 0.10** for precision and recall
* **No regression** versus previous accepted run by more than 3 percent on any metric without a documented goldset change

---

## Benchmark protocols

### Protocol A: A versus A+WFGY

Purpose is to prove the benefit of the WFGY layer with the same base model and the same data.

* Same dataset, prompts, and retriever
* Arm 1 baseline without WFGY
* Arm 2 with WFGY Core and the Problem Map instruments
* Compare precision, recall, ΔS distribution, λ stability, latency

### Protocol B: Cross model control

Purpose is to show that gains are not tied to a single provider.

* Choose two or more providers from your production shortlist
* Keep gold, retriever, and prompts constant
* Run baseline and WFGY arms per provider
* Report deltas within provider and also pooled across providers

### Protocol C: Stress and stability

Purpose is to surface brittleness that simple single shot tests will hide.

* For each question, run three paraphrases and two seeds
* Expand k values in retrieval to 5, 10, 20
* Record λ states per step and ΔS histograms
* Accept only when variance and flip rates are within thresholds

---

## Dataset design

* Use at least **50 questions** spanning three difficulty bands
* Each question has gold snippets with offsets and token ranges
* Include **adversarial distractors** that look semantically close in the same index
* Mixed language tests require tokenizer checks and casing constraints
* For long context tasks, mark the join points for E\_resonance probes

See the construction details in [Goldset Curation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/goldset_curation.md).

---

## Metrics you must report

* **RAG**: precision, recall, ΔS mean and p90, λ flip rate, coverage
* **Reasoning**: correction stickiness after one steer, hallucination re-entry rate
* **Latency**: median and p90 per step (retrieve, rerank, reason)
* **Stability**: variance across paraphrases and seeds
* **Cost**: normalized tokens or API units per correct answer

Targets and field definitions are aligned with the pages linked in the Open section above.

---

## JSONL reporting schema

Each benchmark row is one question run in one arm. Use JSONL for easy diffing.

```json
{
  "suite": "v1_rag_core",
  "protocol": "A",
  "arm": "baseline" ,
  "provider": "openai",
  "model": "gpt-4o-mini-2025-07",
  "question_id": "q_042",
  "paraphrase": 2,
  "seed": 13,
  "k": 10,
  "precision": 0.86,
  "recall": 0.72,
  "coverage": 0.74,
  "ΔS_avg": 0.38,
  "ΔS_p90": 0.47,
  "λ_state_seq": ["→","→","→"],
  "λ_flip_rate": 0.0,
  "latency_ms": { "retrieve": 120, "rerank": 45, "reason": 930 },
  "tokens": { "in": 1850, "out": 420 },
  "hallucination_reentry": false,
  "notes": "meets thresholds"
}
```

For aggregation, compute means and p90 per protocol and arm, then produce deltas for A vs A+WFGY and for each provider in Protocol B.

---

## Minimal 60 second run

1. Pick 10 questions from the goldset with citations.
2. Run Protocol A comparing baseline vs WFGY on a single provider.
3. Record JSONL and compute precision, recall, ΔS, λ stability.
4. If any acceptance target fails, route to the right fix page:

   * Wrong meaning with high similarity → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
   * Messy ordering → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
   * No trace or mixed sources → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Common pitfalls and how to avoid them

* **Goldset ambiguity**
  Two valid snippets exist but only one is labeled. Expand gold with alt spans. See Goldset Curation.

* **Tokenizer and casing drift**
  Mixed language corpora collapse precision. Apply the multilingual checklist and keep analyzers consistent. See Data Contracts and Rerankers.

* **Hidden index skew**
  Flat high ΔS across k suggests metric or normalization mismatch. Rebuild index and verify with a small canary set. See RAG Playbook and Embedding vs Semantic.

* **Prompt header instability**
  λ flips when the header order changes. Lock schema and clamp variance with BBAM.

* **Eval leakage**
  Using dev answers in prompts inflates metrics. Keep a holdout split and rotate keys between runs.

---

## Publishing results

When you publish, include:

* Protocol tables with acceptance ticks
* ΔS histograms and λ flip rates per arm
* Precision and recall bars with error bands across paraphrases
* A short narrative mapping any failures to the exact Problem Map pages you used to fix them
* A link to your JSONL and the goldset diffs

Public examples and figures live here: [Benchmark vs GPT-5](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)

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

