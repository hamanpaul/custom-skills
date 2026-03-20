<!--
Search Anchor:
enterprise knowledge governance global fix map
rag knowledge governance policy layer
llm enterprise access control and pii
audit and traceability for rag
compliance and retention policy llm
data residency and regional shards
data sensitivity tagging and redaction
knowledge expiry and stale sop control
retention policy ttl queues and purge proof
enterprise policy eval for agents

When to use this folder:
mixed sensitivity corpora must prevent leakage
regional data residency is a hard requirement
stale sops and revoked policies show up in answers
legal retention and developer convenience drift
regulators want auditable access trails
need exports that show who saw which pii
residency and sensitivity tags not enforced at retrieval
policy only lives in docs not in code
rag stack must be policy true across tenants and regions
agents must not cross tenant or region fences

Core pages in this folder:
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/README.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance_audit.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_sensitivity.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md
ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md

Related structural fixes:
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/chunking-checklist.md
ProblemMap/ocr-parsing-checklist.md
ProblemMap/prompt-injection.md
ProblemMap/ops/live_monitoring_rag.md
ProblemMap/ops/debug_playbook.md
ProblemMap/GlobalFixMap/EvalObservability/README.md
ProblemMap/GlobalFixMap/EvaluationGuardrails/README.md
ProblemMap/GlobalFixMap/OpsDeploy/README.md

Governance scenarios:
tenant and role based access control for rag
region pinned retrieval and embeddings
policy aware prompt and tool layer
pii and secret redaction before indexing
knowledge expiry workflow for sops and policies
retention queues and deletion attestations
audit trail for who asked and what was cited
policy eval attached to each answer
weekly or quarterly compliance exports
governance gate before shipping a new stack
-->


# Enterprise Knowledge Governance — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

A compact hub to keep enterprise knowledge **safe, auditable, and policy-true** across RAG, agents, and long-running workflows.  
Use this folder to define the policy layer and route symptoms to the exact repair page. No infra change required.

---

## What this folder is
- A minimal but complete **policy layer** for RAG and agent stacks.
- Guardrails that prevent leakage and region violations.
- Copy-paste contracts for tagging, retrieval fences, and audits.
- Acceptance targets you can actually measure on live traffic.

---

## When to use this folder
- You have mixed-sensitivity corpora and must stop accidental leakage.  
- Regional data residency is a contract requirement.  
- Stale SOPs or outdated policies keep showing up in answers.  
- Legal retention vs developer convenience keeps drifting.  
- You need verifiable access trails and regulator-ready exports.  

---

## Orientation: pages and what they solve

<!--
Anchor Menu:
open: enterprise knowledge governance readme ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/README.md
open: access control page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md
open: audit and traceability page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md
open: compliance overview page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance.md
open: compliance audit checklist page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance_audit.md
open: data residency page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md
open: data sensitivity model page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_sensitivity.md
open: knowledge expiry page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md
open: retention policy page ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md

jump: retrieval traceability schema ProblemMap/retrieval-traceability.md
jump: data contracts and snippet schema ProblemMap/data-contracts.md
jump: chunking checklist page ProblemMap/chunking-checklist.md
jump: ocr parsing checklist page ProblemMap/ocr-parsing-checklist.md
jump: prompt injection page ProblemMap/prompt-injection.md

jump: live monitoring for rag page ProblemMap/ops/live_monitoring_rag.md
jump: debug playbook page ProblemMap/ops/debug_playbook.md

jump: eval observability readme ProblemMap/GlobalFixMap/EvalObservability/README.md
jump: evaluation and guardrails readme ProblemMap/GlobalFixMap/EvaluationGuardrails/README.md
jump: ops and deploy readme ProblemMap/GlobalFixMap/OpsDeploy/README.md
-->


| Page | What it solves | Typical symptom |
|------|----------------|-----------------|
| [access_control.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md) | Role, tenant, region, sensitivity intersections at retrieval time | Answer cites a snippet the user cannot see |
| [audit_and_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md) | Immutable trails for who asked, what was cited, why it was allowed | Regulator asks for proof and you cannot produce it |
| [compliance.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance.md) | End-to-end policy surface and controls | Policy defined in docs but not enforced in code |
| [compliance_audit.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance_audit.md) | Audit checklists and export packs | You cannot prove who accessed PII last quarter |
| [data_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md) | Region pinning for shards, embeddings, logs | Cross-region egress appears in billing or logs |
| [data_sensitivity.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_sensitivity.md) | Sensitivity model and redaction gates | PII or secrets slip through after parsing |
| [knowledge_expiry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md) | Freshness and deprecation workflow | Bot answers with outdated SOP or revoked policy |
| [retention_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md) | TTL queues, deletion attestations, proof of purge | Items that should be gone still show up in runs |

---

## Acceptance targets

- Zero unauthorized citation of PII or restricted snippets in production evals  
- Policy tags present on ≥ 0.95 of onboarded documents  
- Residency violations equal 0 across seven days of traffic  
- Retention SLA respected for 100 percent of expired items inside 24 hours  
- Every answer carries a trace with `citations`, `ΔS`, `λ_state`, `policy_eval`

---

## Map symptoms → structural fixes

| Symptom | Open this |
|--------|-----------|
| Wrong snippet shows up from a restricted area | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Prompt or tool bypasses policy and leaks PII | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) · lock tool args in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Sensitive text survives parsing and chunking | [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) · [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md) |
| Live runs drift from policy or regions | [ops/live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) |

---

## 60-second setup checklist

1) **Tag the corpus**  
   Attach `sensitivity`, `region`, `owner`, `retention_tier` to every doc. Enforce schema with [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

2) **Fence retrieval**  
   Require the intersection of `{tenant_id, role, region, sensitivity}` at retrieve time and drop non-matching snippets. Verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

3) **Pin residency**  
   Keep embeddings and shards in the source region. Block cross-region egress unless policy allows. See [data_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md).

4) **Retention jobs**  
   Create TTL queues per `retention_tier`. Write a deletion log with `doc_id`, `hash`, `time`, `actor`. See [retention_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md).

5) **Audit everything**  
   Emit `actor`, `question`, `citations`, `ΔS`, `λ_state`, `policy_eval`, `region` for each answer. Route to an immutable sink. See [audit_and_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md).

---

## Copy-paste policy probe for your LLM step

```txt
You have TXT OS and WFGY pages loaded.

Question: "{user_question}"
Context carries fields {sensitivity, region, retention_tier, owner} for each snippet.

Do:
1) Enforce cite-then-explain. Refuse if a cited snippet breaks role or region.
2) Return {"citations":[...], "policy_eval":{"allow":true|false,"reason":"..."}, "ΔS":0.xx, "λ_state":"→|←|<>|×"}.
3) If blocked, output the smallest change to comply and the exact WFGY page to open.
````

---

## FAQ

**Q: We tag sensitivity at ingest but leaks still happen. What now?**
A: Enforce the tag at **retrieve time** too. Use access intersections `{tenant_id, role, region, sensitivity}` and verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

**Q: Our vendor requires EU residency. How do we prove compliance?**
A: Pin vectors, shards, and logs to EU regions and export an egress report weekly. Steps in [data\_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md).

**Q: Outdated SOPs keep showing up. Where is the crack?**
A: You need a freshness control. Mark deprecated docs and enforce a deny-list at retrieval. See [knowledge\_expiry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md).

**Q: Legal wants proof of deletion after TTL.**
A: Implement TTL queues and write deletion attestations to an immutable sink. Details in [retention\_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md).

**Q: We cannot reconstruct who saw which PII last quarter.**
A: Add the audit contract from [audit\_and\_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md). Every answer should log `actor`, `citations`, `ΔS`, `λ_state`, `policy_eval`, `region`.

**Q: Prompt injection bypassed our fences.**
A: Tighten tool schemas and add role-ordered templates. See [prompt\_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) and the contracts in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**Q: Coverage is high but restricted snippets sometimes get ranked.**
A: Coverage is not policy. Add **policy\_eval** to the trace and drop candidates before rerank. Use [access\_control.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md).

**Q: How do we set pass or fail before release?**
A: Use a governance gate: zero restricted citations, zero residency violations, coverage ≥ 0.70, ΔS ≤ 0.45, and audit completeness 100 percent for a 7-day canary.

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

