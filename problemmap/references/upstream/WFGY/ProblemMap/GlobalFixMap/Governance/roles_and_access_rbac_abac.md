# Roles and Access (RBAC / ABAC) — Guardrails and Fix Pattern

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


This page defines **role-based access control (RBAC)** and **attribute-based access control (ABAC)** guardrails for AI pipelines.  
Without explicit access boundaries, LLMs may read from unintended sources, leak sensitive data, or bypass audit policy.

---

## When to use this page
- Your RAG or agent stack integrates multiple data stores with different sensitivity levels.  
- You cannot trace **who accessed what** across prompts, embeddings, or tool calls.  
- Evaluation runs fail because different users see different knowledge bases.  
- Compliance requires proof of **least privilege** but no policy schema exists.  

---

## Acceptance targets
- 100% of RAG data calls tagged with `role` or `attribute` context.  
- Coverage ≥ 0.95 of sensitive datasets behind access boundaries.  
- Audit trails record `who`, `what`, `when`, `ΔS`, `λ_state`.  
- Role drift probes show λ remains convergent across 3 paraphrases.  
- Exceptions logged with owner and expiry date.  

---

## Common failures → exact fixes

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Agents fetch data beyond allowed scope | missing RBAC fences | [policy_baseline.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/policy_baseline.md) |
| Two users get different citations | inconsistent ABAC checks | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Logs don’t show who triggered retrieval | no role injection | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Role drift causes schema injection | misplaced role attributes | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) |
| Sensitive snippets leak in chains | missing attribute check | [pii_handling_and_minimization.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/pii_handling_and_minimization.md) |

---

## Fix in 60 seconds

1. **Attach context**  
   Every retrieval call carries `{role, attribute_set, index_hash, ΔS, λ_state}`.  

2. **Enforce least privilege**  
   Roles map to dataset groups. Attributes refine down (e.g. geography, project).  

3. **Log every decision**  
   Audit trail logs query, ΔS, λ state, role, attributes, and snippet ids.  

4. **Probe role drift**  
   Run 3 paraphrases per role. If λ flips, enforce schema lock.  

---

## Minimal copy-paste checklist

- [ ] Define roles (admin, annotator, auditor, agent).  
- [ ] Define attributes (region, dataset sensitivity, project scope).  
- [ ] Attach `{role, attr}` to all tool and retrieval calls.  
- [ ] Enforce least privilege at ingestion and retrieval.  
- [ ] Log ΔS and λ_state by role.  
- [ ] Review and expire waivers.  

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

要我直接繼續幫你生出來嗎？
