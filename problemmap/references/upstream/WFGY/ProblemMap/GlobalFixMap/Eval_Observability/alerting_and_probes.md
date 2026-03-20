# Eval Observability — Alerting and Probes

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


A live guardrail system that detects semantic drift, retrieval collapse, and logic instability in production.  
Use this page to design **continuous probes** (ΔS, λ, coverage, resonance) and trigger alerts before users see failures.

---

## Why probes are required

- **Silent regressions**: Models may degrade gradually after retraining or infra changes.  
- **Runtime entropy**: Long chains often destabilize after 25–40 steps.  
- **Hybrid stack drift**: Store upgrades, reranker weights, or tokenizer shifts silently change outcomes.  
- **Auditability**: Real-time probes make every failure reproducible.

---

## Core probe dimensions

| Metric | Probe type | Alert condition |
|--------|------------|-----------------|
| ΔS(question, retrieved) | per-query | ≥ 0.60 for any query OR average >0.50 across batch |
| Coverage of target section | per-query | < 0.70 for more than 5% of batch |
| λ_observe | rolling window | divergence observed across 2 seeds or paraphrases |
| E_resonance | sliding horizon | spikes or oscillations in 50–100 step runs |

---

## Recommended probe architecture

1. **Pre-query probe**  
   Check retriever config hash, index hash, analyzer type.  
   Block if mismatched against gold baseline.

2. **Mid-query probe**  
   During retrieval, compute ΔS(question, retrieved).  
   Attach snippet IDs and offsets for traceability.

3. **Post-query probe**  
   Run λ stability check across 3 paraphrases.  
   If divergent, tag output with `unstable=true`.

4. **Long-chain probe**  
   For conversations >25 steps, sample entropy and E_resonance every 10 steps.  
   Trigger backoff or memory split if instability rises.

---

## Alerting routes

- **Slack / Teams** → Send structured JSON logs with ΔS, λ, coverage, index hash, retriever config.  
- **PagerDuty** → Trigger incidents only when threshold failures exceed N in M minutes.  
- **Dashboards** → Grafana/Datadog with ΔS trend lines, λ variance plots, coverage histograms.  
- **Audit store** → Write all probe outputs to KV or DB keyed by `(session_id, index_hash, retriever_config)`.

---

## Example probe config (YAML)

```yaml
probes:
  deltaS:
    threshold: 0.60
    action: alert
  coverage:
    threshold: 0.70
    tolerance: 0.05
  lambda:
    seeds: 2
    paraphrases: 3
    action: block
  resonance:
    horizon: 100
    action: degrade_notice
alerting:
  sink:
    - slack
    - pagerduty
    - grafana
````

---

## Common mistakes

* **Only probing ΔS**. Always include coverage + λ + resonance.
* **Static thresholds**. Thresholds must be tested against gold sets and updated quarterly.
* **No audit linkage**. Alerts without index hash and retriever config cannot be replayed.
* **Flooding alerts**. Use capped retries and aggregate rules to avoid pager fatigue.

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

