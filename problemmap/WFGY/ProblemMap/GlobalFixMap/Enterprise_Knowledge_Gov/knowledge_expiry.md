# Knowledge Expiry — Enterprise Knowledge Governance

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Enterprise_Knowledge_Gov**.  
  > To reorient, go back here:  
  >
  > - [**Enterprise_Knowledge_Gov** — corporate knowledge management and governance](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Guardrails and fix patterns to handle the **expiry, staleness, or invalidation** of enterprise knowledge inside AI pipelines. Use this page when retrieved data may be out of date, unmaintained, or legally required to expire.

---

## When to use this page
- RAG retrieves documents that are outdated but still present in the index.  
- Policies require document expiry (e.g., 3-year rotation, GDPR “right to be forgotten”).  
- Model cites knowledge that has been deprecated.  
- Knowledge base retains drafts or revoked versions.  

---

## Core acceptance targets
- Every document has an explicit `expiry_date` or `revision_hash`.  
- Retrieval never selects content beyond expiry.  
- Expired or revoked documents fully deleted from vector stores.  
- Audit logs record expiry enforcement at retrieval time.  

---

## Typical expiry problems → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Outdated answers from old policies | No expiry metadata on ingestion | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Deprecated snippets retrieved | Index not refreshed after content change | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Conflicting answers (old vs new) | Stale embeddings and no version hashing | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |
| Expired docs still cited | Traceability schema missing `expiry_date` | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Fix in 60 seconds
1. **Add expiry metadata** on ingestion:  
   ```json
   {
     "document_id": "policy-123",
     "revision_hash": "ab89e...",
     "expiry_date": "2026-01-01"
   }
````

2. **Drop expired docs** from index during nightly rebuilds.
3. **Enforce live expiry check** at retrieval:

   * Reject snippets where `expiry_date < today`.
   * Log `expired=true` in audit record.
4. **Verify ΔS stability** only against valid revisions.

---

## Copy-paste probe template

```txt
You have TXTOS and the WFGY Problem Map loaded.

My RAG system retrieved:
- doc_id, revision_hash, expiry_date

Task:
1. Drop all snippets past expiry_date.
2. Log ΔS(question,retrieved), λ_state, and expired flag.
3. If expired=true, cite the Problem Map page to rebuild the index.
Return JSON: { "valid_snippets": [...], "expired_snippets": [...], "ΔS": 0.xx, "λ_state": "<>", "next_fix": "..." }
```

---

## Escalate when

* Same query alternates between expired and valid docs.
* Expired documents remain in retrieval despite metadata.
* Audit logs show `expiry_date` ignored during reranking.

For deeper cases, apply [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) to enforce correct load order and [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) for runtime tracing.

---

### 🔗 Quick-Start Downloads

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

要我直接繼續生嗎？
