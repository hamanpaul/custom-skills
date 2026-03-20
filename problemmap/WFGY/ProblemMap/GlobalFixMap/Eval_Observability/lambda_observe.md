# Eval Observability — λ_observe

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

> **Evaluation disclaimer (λ_observe)**  
> λ_observe is a heuristic stability signal defined inside the WFGY framework.  
> It helps you notice drift and volatility but is not a formal guarantee of long term robustness.

---

A core probe for evaluating **semantic convergence** across multiple seeds, paraphrases, and retrieval variations.  
While ΔS measures semantic distance, **λ_observe** captures **stability vs divergence of reasoning paths**.

---

## Why λ_observe matters

- **Detect fragile reasoning**: Even when ΔS looks safe, λ divergence indicates unstable chains.  
- **Identify paraphrase sensitivity**: If λ flips across harmless rewordings, the system is brittle.  
- **Audit retrieval randomness**: Different seeds producing opposite λ signals reveal weak schema.  
- **Ensure eval reproducibility**: Stable λ means tests repeat reliably under small perturbations.

---

## λ state encoding

| Symbol | Meaning | Example failure |
|--------|---------|-----------------|
| **→**  | Forward convergence, stable path | Same citations and reasoning across paraphrases |
| **←**  | Backward collapse, early abort | Tool call retries, empty citations |
| **<>** | Split state, partial divergence | One paraphrase cites correct snippet, others miss |
| **×**  | Total collapse | Random answers, no citation alignment |

---

## Acceptance targets

- **Convergence rate ≥ 0.80** across 3 paraphrases × 2 seeds.  
- **No × states** tolerated in gold-set eval.  
- **Split states (<>): ≤ 10%** of test cases acceptable.  
- **Forward (→)** must dominate stable runs.

---

## Evaluation workflow

1. **Run triple paraphrase probe**  
   Ask the same question three ways. Collect λ states.  
2. **Repeat with two seeds**  
   Track variance.  
3. **Roll-up stats**  
   Compute convergence ratio, collapse frequency, divergence rate.  
4. **Escalation**  
   If λ <0.80 or × >0%, run root-cause: schema audit, retriever split, prompt ordering.

---

## Example probe schema

```json
{
  "query_id": "Q42",
  "runs": [
    {"paraphrase": 1, "seed": 123, "λ": "→"},
    {"paraphrase": 2, "seed": 123, "λ": "→"},
    {"paraphrase": 3, "seed": 123, "λ": "<>"},
    {"paraphrase": 1, "seed": 456, "λ": "→"},
    {"paraphrase": 2, "seed": 456, "λ": "×"},
    {"paraphrase": 3, "seed": 456, "λ": "→"}
  ]
}
````

---

## Common pitfalls

* **Only measuring ΔS** → misses hidden divergence.
* **Seed-fixed eval** → looks stable but fragile in production.
* **Ignoring split states** → small divergence often grows into collapse.
* **No per-query logs** → averages hide catastrophic single failures.

---

## Reporting recommendations

* **λ distribution table**: % of →, ←, <>, ×.
* **Convergence trend**: chart over time by eval batch.
* **Drift alerts**: trigger if convergence <0.80 or × appears.
* **Correlation**: track ΔS vs λ to spot mixed failures.

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

