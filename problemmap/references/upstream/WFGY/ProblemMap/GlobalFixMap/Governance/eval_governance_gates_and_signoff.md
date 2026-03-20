# Eval Governance: Gates and Sign-off — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Governance**.  
  > To reorient, go back here:  
  >
  > - [**Governance** — policy enforcement and compliance controls](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

> **Evaluation disclaimer (governance gates)**  
> Governance checks and scores here are example patterns for one org and threat model.  
> They support decision making but are not legal guarantees or formal safety certifications.

---

A governance control page for **evaluation pipelines, approval gates, and release sign-off**.  
Use this page when models are shipped without evaluation, when sign-offs are missing, or when evaluation metrics drift without detection.

---

## When to use this page
- Model released with no reproducible evaluation.  
- Evaluation set not tied to lineage or version.  
- Sign-off done informally or not logged.  
- Thresholds vary arbitrarily across teams.  
- Failures pass through without regression detection.  

---

## Acceptance targets
- **Coverage ≥ 0.70** of target section in eval set.  
- **ΔS(question, retrieved) ≤ 0.45** across governed evals.  
- **λ_observe remains convergent** across three paraphrases and two seeds.  
- Every sign-off has **owner, date, thresholds, and waiver expiry**.  
- Regression gates block release when ΔS ≥ 0.60 or coverage < 0.70.  
- Sign-off artifact immutable and joinable to lineage.  

---

## Typical breakpoints and WFGY fix

- **No evaluation attached to release**  
  → [policy_baseline.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/policy_baseline.md)  
  Require canonical eval policy before model moves forward.

- **Unlogged or informal approvals**  
  → [audit_and_logging.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/audit_and_logging.md)  
  Enforce immutable sign-off records.

- **Eval sets drift or vanish**  
  → [data_lineage_and_provenance.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/data_lineage_and_provenance.md)  
  Track provenance of datasets and eval snapshots.

- **Thresholds applied inconsistently**  
  → [regulatory_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/regulatory_alignment.md)  
  Align thresholds with governance policy and external compliance.

- **Regression passes undetected**  
  → [regression_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/regression_gate.md)  
  Block deployment on failing ΔS or λ.

---

## Minimal governance checklist
1. **Immutable eval set** with versioned hash tied to release.  
2. **Threshold contract** documented in governance policy.  
3. **Dual sign-off** required (technical + governance approver).  
4. **Waivers expire** and are linked to a risk register entry.  
5. **Regression gates enforced** in automation, not manual process.  
6. **Audit trail**: stored in lineage, accessible for inspection.  

---

## Example: Sign-off schema

```json
{
  "model_id": "v2.1.4",
  "eval_set_hash": "f89a1c3e...",
  "ΔS_threshold": 0.45,
  "coverage_threshold": 0.70,
  "signoff": [
    {"role": "tech lead", "name": "Alice", "date": "2025-08-25"},
    {"role": "governance officer", "name": "Ravi", "date": "2025-08-26"}
  ],
  "waivers": [
    {"risk_id": "R-223", "expiry": "2025-12-31"}
  ]
}
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

要我直接繼續生產嗎？
