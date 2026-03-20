# Microsoft Power Automate — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Automation Platforms**.  
  > To reorient, go back here:  
  >
  > - [**Automation Platforms** — stabilize no-code workflows and integrations](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

Use this when your workflow is built with **Power Automate** (cloud flows, AI Builder, custom connectors) and you see wrong citations, unstable answers, mixed sources, or silent failures that “look green” in run history.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the intended section/record
- λ remains convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Output is plausible yet cites the wrong doc/snippet  
  Fix No.1: **Hallucination & Chunk Drift** →  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) ·  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Vector similarity looks fine, meaning is off  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Some facts exist in SharePoint/Dataverse but never surface in top-k  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Can’t explain *why* a snippet was chosen; run history shows only final text  
  Fix No.8: **Retrieval Traceability** with snippet schema →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Long chains or approvals flatten tone and drift logically  
  Fix No.3/No.9: **Context Drift** and **Entropy Collapse** →  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·  
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Flow passes in Test but fails after environment or connection swap  
  Infra: **Pre-Deploy/Bootstrap/Deadlock** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) ·  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- Confident tone with wrong answers in AI Builder actions  
  Fix No.4: **Bluffing/Overconfidence** →  
  [Bluffing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)

---

## Minimal Power Automate pattern with WFGY checks

Below is a compact flow outline. It enforces **cite-first schema**, **observable retrieval**, and a **ΔS/λ post-check**.

```txt
Trigger: When an HTTP request is received
Actions:
1) Initialize variable "k" = 10
2) Parse JSON "question" from request
3) HTTP → your retriever endpoint
   - Method: POST
   - Body: { "question": "@{variables('question')}", "k": "@{variables('k')}" }
4) Compose "context" = join(retrieved.snippets)
5) Compose "prompt" =
   SYSTEM: Cite lines before any explanation.
   TASK: Answer the user's question using the provided context.
   CONSTRAINTS:
   - Do not mix sources
   - Provide snippet_id for each citation
   CONTEXT:
   @{outputs('Compose_context')}
   QUESTION:
   @{variables('question')}
6) AI Builder / Custom Connector → LLM with "prompt"
7) HTTP → wfgyCheck (custom Azure Function)
   - Body: { "question": "@{variables('question')}",
             "context": "@{outputs('Compose_context')}",
             "answer": "@{outputs('LLM_action')}" }
8) Condition:
   If deltaS ≥ 0.60 OR lambda != "→"
      → Terminate flow (Warn) "High semantic stress. See trace log."
   Else
      → Return 200 with { answer, deltaS, lambda, coverage, citations[] }
````

**What this enforces**

* Retrieval parameters are explicit and logged in flow run details.
* Prompt is **schema-locked** with **cite-first**.
* WFGY check runs after generation and can **fail fast** when ΔS is high or λ flips divergent.
* Trace table (snippet\_id ↔ citation) is returned for audit.

Reference specs
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Power Automate specific gotchas

* **Environment or connection drift**: different Dataverse/SharePoint connections between ingestion and query. Pin connections per environment and re-verify secrets.
  See [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Throttling/parallel branches** change ordering of records. Add a **rerank** stage only after per-source ΔS ≤ 0.50.
  See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Parse JSON** actions silently drop fields, breaking snippet\_id propagation. Validate schemas and keep `snippet_id` mandatory.
  See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **Embedding metric mismatch** between ingestion code (Azure Function/Logic App) and query side. Normalize vectors and pin cosine vs. inner product.
  See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Scheduled flows** rebuild indices unintentionally. Make builds idempotent and gate by boot checks.
  See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## When to escalate

* ΔS remains ≥ 0.60 after chunking and retrieval fixes
  Work through the playbook, then rebuild the index with explicit metric flags and unit normalization.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Answers flip between Dev/UAT/Prod
  Verify version skew, connection references, and secrets.
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

