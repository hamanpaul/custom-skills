# Eval Observability — Coverage Tracking

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

> **Evaluation disclaimer (coverage tracking)**  
> Coverage numbers here measure how much of a designed space you have touched under chosen tests.  
> High coverage does not guarantee absence of bugs or failures outside those tests.

---

A focused module to monitor **retrieval coverage** during eval and live runs.  
Coverage answers the key question: *“Did we retrieve enough of the right section to support the answer?”*

---

## Why coverage tracking matters

- **False negatives**: The right fact exists, but snippets cover too little of the section.  
- **Over-fragmentation**: Documents chunked too aggressively result in coverage <0.50 despite correct snippets.  
- **Hallucinations**: When coverage is low, LLMs often fill gaps with fabrications.  
- **Eval blind spots**: Benchmarks without coverage probes miss systematic recall failures.

---

## Core definition

Coverage is defined as:

```text
coverage = retrieved_tokens_in_target_section / total_tokens_in_target_section
````

* **Target section** = gold label or expected answer span.
* **Threshold** = minimum 0.70 in most RAG tasks.
* **Tolerance** = allow 5–10% batch queries below threshold before raising alert.

---

## Probe design

1. **Annotate gold sets**
   For each eval question, mark the expected source section IDs and token spans.

2. **Measure per-query coverage**
   Count how many tokens from expected span were retrieved.
   Normalize by total tokens in span.

3. **Batch aggregation**
   Track percentage of queries below threshold.
   Report average coverage ± variance.

4. **Drift detection**
   Compare against historical baseline (previous model or retriever version).
   If drop >0.05, escalate to retriever/infrastructure team.

---

## Alert thresholds

| Metric             | Warning    | Critical   |
| ------------------ | ---------- | ---------- |
| Per-query coverage | <0.70      | <0.60      |
| Batch pass rate    | <0.90      | <0.80      |
| Drift vs baseline  | drop >0.05 | drop >0.10 |

---

## Example probe code (pseudo)

```python
def track_coverage(retrieved, target_span):
    overlap = count_tokens(retrieved, target_span)
    coverage = overlap / len(target_span)
    return coverage

for q in eval_batch:
    cov = track_coverage(q.retrieved_tokens, q.gold_span)
    if cov < 0.70:
        alerts.append({"qid": q.id, "coverage": cov})
```

---

## Common pitfalls

* **Ignoring multi-section answers** → coverage must sum across all required sections.
* **Only measuring top-1 snippet** → always include top-k, otherwise underestimation occurs.
* **Static thresholds** → thresholds should adapt to doc size and retrieval depth.
* **No historical baseline** → without drift tracking, regressions pass unnoticed.

---

## Reporting dashboards

* **Histograms** of per-query coverage distribution.
* **Trend lines** for batch averages across eval sets.
* **Drift deltas** vs baseline runs.
* **Heatmaps** showing coverage by document or domain.

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

