# Eval Observability — Metrics and Logging

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


A baseline schema and checklist for logging semantic metrics (ΔS, λ, coverage, E_resonance) during live runs.  
Use this page to enforce consistent telemetry so that offline eval and online observability align.

---

## Why log metrics?

- **Drift detection**: High ΔS or divergent λ states catch retrieval/logic errors early.  
- **Comparability**: Same schema across providers, stores, and orchestration layers.  
- **Debug loops**: Logged traces accelerate reproduction and diagnosis.  
- **Regression guards**: Simple thresholds protect pipelines before release.

---

## Core metrics to capture

| Metric | Definition | Thresholds |
|--------|------------|------------|
| ΔS(question, retrieved) | Semantic distance between query and retrieved snippet | Stable ≤ 0.45, Transitional 0.45–0.60, Risk ≥ 0.60 |
| Coverage | Fraction of gold/target section retrieved | ≥ 0.70 |
| λ_observe | State of reasoning flow (→ convergent, ← divergent, <> transitional, × collapse) | Must stay convergent across 3 paraphrases |
| E_resonance | Long-window entropy of reasoning steps | Should remain flat without spikes |

---

## Logging schema (JSON example)

```json
{
  "trace_id": "uuid",
  "timestamp": "2025-08-29T12:34:56Z",
  "question": "...",
  "retrieved": [
    {
      "snippet_id": "s1",
      "section": "intro",
      "source": "docA",
      "offsets": [120, 160],
      "ΔS": 0.42
    }
  ],
  "ΔS_overall": 0.44,
  "coverage": 0.72,
  "λ_state": "→",
  "E_resonance": 0.03,
  "index_hash": "abc123",
  "dedupe_key": "sha256(...)" 
}
````

---

## Quick probes

* **ΔS probe**: Recompute ΔS on each retrieval call. Alert if ≥ 0.60.
* **λ probe**: Run three paraphrases per eval batch, log λ\_state sequence.
* **Coverage probe**: Compare retrieved sections against gold or expected anchors.
* **E\_resonance probe**: Smooth entropy over 50–100 steps, alert if spike > 2× baseline.

---

## Storage tips

* Write logs to append-only store (e.g., KV or time-series DB).
* Deduplicate with `dedupe_key = sha256(question + index_hash + snippet_id)`.
* Keep 30–90 days rolling window for regression analysis.

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

