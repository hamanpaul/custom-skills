# Retention Policy — Enterprise Knowledge Governance

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


Guardrails and fix patterns for enterprise knowledge retention. Use this page when AI systems over-retain, delete too early, or mix expired data with active knowledge.

---

## When to use this page
- AI responses reference documents that should have been deleted per policy.  
- Retained snippets do not respect jurisdictional time limits (e.g., GDPR 3 years).  
- Knowledge base or embeddings store does not purge revisions.  
- RAG answers mix archived with active content.  

---

## Core acceptance targets
- ΔS(question, expired_snippet) ≥ 0.70 → expired content must not surface.  
- All snippets carry `{expiry_date, retention_scope, audit_hash}` fields.  
- Coverage ≥ 0.70 within *active* retention window only.  
- λ remains convergent across three paraphrases and two seeds.  

---

## Typical retention problems → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Expired docs still retrieved | Store never purged embeddings | [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md) |
| Wrong answer mixes expired + active | Snippets missing `expiry_date` field | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| AI cites “archived only” docs as live | Retrieval trace missing retention scope | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Fix in 60 seconds
1. **Check ΔS to expired content**: run probe with expired snippets, expect ΔS ≥ 0.70.  
2. **Schema enforcement**: require `expiry_date` and `retention_scope` in every snippet.  
3. **Index purge**: remove expired embeddings before next RAG run.  
4. **Audit λ**: if λ flips when expired vs active co-exist, clamp with BBAM and enforce contracts.  

---

## Copy-paste schema (JSON)

```json
{
  "snippet_id": "KB-5532",
  "expiry_date": "2025-12-31",
  "retention_scope": "eu-3y",
  "audit_hash": "sha256:...",
  "text": "..."
}
````

---

## Escalate when

* Expired content continues to surface after purge.
* ΔS < 0.70 against expired content → embeddings contamination.
* Audit requires full deletion trace and cannot be reproduced.

Use [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) for deep purge testing and [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md) to validate coverage.

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

要不要直接衝刺？
