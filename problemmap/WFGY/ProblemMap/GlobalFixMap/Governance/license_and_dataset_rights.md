# License and Dataset Rights — Guardrails and Fix Pattern

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


This page tracks **legal and licensing risks** in AI systems.  
If datasets, embeddings, or outputs rely on unverified sources, you risk compliance violations, takedowns, or IP litigation.  
Use this guide to enforce clear rights boundaries across ingestion, training, and generation.

---

## When to use this page
- You do not know the license of a dataset included in your retrieval or training pipeline.  
- Mixed rights (MIT, Apache, proprietary, unknown) exist in the same corpus.  
- Legal review requires proof that generated answers respect dataset terms.  
- Audit asks for compliance with GDPR/CCPA or publisher licensing.  

---

## Acceptance targets
- 100% of datasets tagged with a license identifier.  
- ≥ 95% coverage of ingestion checks include license + attribution metadata.  
- ΔS stability maintained when filtering licensed vs. non-licensed subsets.  
- Audit logs capture `license_id`, `rights_holder`, `expiry`.  
- LLM refuses or flags outputs when license terms are violated.  

---

## Common failures → exact fixes

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Snippets from unknown or scraped sources appear | dataset missing license metadata | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Open source corpus mixes with paid corpus | no role/rights separation | [roles_and_access_rbac_abac.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/roles_and_access_rbac_abac.md) |
| Model answers cite restricted publishers | no attribution enforcement | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Generated outputs reuse licensed patterns | prompt injection bypassing rights filter | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) |
| Training run includes expired or revoked dataset | missing expiry validation | [policy_baseline.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/policy_baseline.md) |

---

## Fix in 60 seconds

1. **Tag every dataset**  
   Attach `{license_id, rights_holder, expiry, attribution_required}` at ingestion.  

2. **Separate corpora**  
   Open source vs. proprietary vs. paid corpora must remain in distinct retrieval indices.  

3. **Enforce attribution**  
   Require citation-first prompting for any licensed corpus.  

4. **Audit pipeline**  
   Store logs with dataset version, license, and usage context.  

5. **Expiry enforcement**  
   Block or purge expired corpora automatically.  

---

## Minimal compliance checklist

- [ ] Every ingestion pipeline requires license metadata.  
- [ ] RBAC + ABAC enforced to keep datasets separated.  
- [ ] Retrieval schema logs license_id with every snippet.  
- [ ] Expiry checks run nightly.  
- [ ] Audit reports exportable on request.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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

