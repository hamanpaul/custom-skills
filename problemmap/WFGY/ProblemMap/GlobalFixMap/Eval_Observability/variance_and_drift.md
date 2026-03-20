# Eval Observability — Variance and Drift

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


Variance and drift checks detect when evaluation scores are **unstable across runs** or when **semantic meaning slowly shifts** without clear boundary failures.  
These probes prevent "false confidence" in benchmarks by catching hidden instability.

---

## Why variance and drift matter

- **Variance**: Scores fluctuate heavily depending on seed, paraphrase, or retriever order. Averages hide the volatility.  
- **Drift**: Performance declines slowly across sessions, data refreshes, or version bumps. Looks fine short-term but collapses long-term.  
- **Silent regressions**: Systems pass local tests but fail in production due to unmonitored entropy rise.  

---

## Acceptance targets

- **Variance (σ/μ)** ≤ 0.15 across 3 seeds and 3 paraphrases.  
- **Drift slope**: Δscore per batch ≤ 0.02 absolute over 5+ eval windows.  
- **No monotonic downward slope** longer than 3 consecutive windows.  
- **Drift alerts** fire if ΔS average increases ≥ 0.10 compared to gold anchors.

---

## Detection workflow

1. **Collect runs across seeds**  
   - At least 3 seeds, 3 paraphrases.  
   - Log ΔS, λ, coverage, citations.  

2. **Compute variance**  
   - Calculate σ/μ for each metric.  
   - High variance = unstable eval → rerun with schema locks.  

3. **Track drift over time**  
   - Compare eval batch N vs N-1.  
   - Plot moving average.  
   - Alert if slope exceeds tolerance.  

4. **Root-cause analysis**  
   - If variance high → check retriever metrics, random seeding, rerankers.  
   - If drift detected → audit embeddings, re-chunk, verify data refresh.  

---

## Common pitfalls

- **Single-run evals**: Hides high variance. Always run multi-seed.  
- **Averages without spread**: Mean looks fine, variance reveals collapse.  
- **Ignoring slow drift**: Short tests OK, but 1–2 weeks later accuracy dies.  
- **Cross-store drift**: One vector DB stable, another drifts. Must track both.  

---

## Example reporting schema

```json
{
  "metric": "ΔS",
  "seed_runs": [0.38, 0.42, 0.44],
  "variance_ratio": 0.14,
  "drift_slope": +0.03,
  "alert": true
}
````

---

## Fix modules to open

* **Retriever instability** → [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* **Embedding mismatch** → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* **Fragmentation drift** → [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md)
* **Prompt instability** → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

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

