# Apache Airflow — Guardrails and Fix Patterns

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


Use this when your workflow is orchestrated by **Apache Airflow** (DAGs with PythonOperators, Sensors, KubernetesPodOperator, etc.). If pipelines succeed but the **answers are wrong**, citations miss, or behavior differs between **ad-hoc runs** and **scheduled runs**, anchor your diagnosis here.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Output sounds right but cites the wrong snippet/section  
  Fix No.1: **Hallucination & Chunk Drift** →  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) ·  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- High vector similarity yet wrong meaning  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Facts are indexed but never show up in top-k (prod vs. local)  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- “Why this snippet?” is untraceable across tasks/pods  
  Fix No.8: **Retrieval Traceability** + snippet/citation schema →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Long multi-task chains drift or flatten over time  
  Fix No.3/No.9: **Context Drift** and **Entropy Collapse** →  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·  
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- DAG runs succeed but first “cold start” call fails after deploy  
  Infra family: **Pre-Deploy / Bootstrap / Deadlock** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) ·  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- Confident tone with wrong claims  
  Fix No.4: **Bluffing / Overconfidence** →  
  [Bluffing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)

---

## Minimal Airflow pattern with WFGY checks

A compact pattern that preserves **cite-first schema**, **observable retrieval**, and **ΔS/λ** validation across tasks and pods.

```txt
Task A — Ingest/OCR (PythonOperator or KubernetesPodOperator)
- Normalize PDFs/images. Drop low-confidence OCR lines.
- Emit: doc_id, section_id, text, anchors

Task B — Chunk & Index (PythonOperator)
- Semantic chunking by section/sentence. Unit-normalize embeddings.
- Persist with explicit metric flag (cosine vs inner product).

Task C — Retrieve (PythonOperator)
- Input: { question, k }
- Output: snippets[] = { snippet_id, text, source, section_id }
- Store in durable cache keyed by run_id/request_id.

Task D — Assemble & Call LLM (PythonOperator)
SYSTEM:
  Cite lines before explanation. Per-source fences. No cross-section reuse.
CONTEXT:
  <joined snippets with snippet_id + source + text>
QUESTION:
  <user question>

Task E — WFGY Post-check (PythonOperator)
- Body: { question, context, answer }
- Compute ΔS and λ; measure coverage.
- Emit: { deltaS, lambda, coverage, notes }

Task F — Gate & Notify (BranchPythonOperator)
IF deltaS ≥ 0.60 OR lambda != "→"
  → route to remediation with trace table (snippet_id↔citation)
ELSE
  → deliver { answer, citations[], deltaS, lambda, coverage }
````

Reference specs:
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Airflow-specific gotchas

* **K8sPodOperator image skew**: embeddings or tokenizers differ between images. Pin exact versions and verify unit normalization at write/read.
  See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Race between retriever warm-up and first LLM call**: scheduled runs start before vectorstore is hydrated. Add bootstrap fences and health checks.
  See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Unbounded prompt assembly** inside operators: prompt fields drift. Centralize schema in one utility and import it across tasks to keep order stable.
  See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **Large artifacts in XCom**: truncate prompts or lose attachments. Store blobs (snippets, PDFs) in object storage; pass only `request_id` through XCom.

* **MMR/rerank differences** by environment: ensure identical tokenizer/analyzer across retriever and reranker, then lock ordering after per-source ΔS ≤ 0.50.
  See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## When to escalate

* ΔS remains ≥ 0.60 after chunk/retrieval fixes → rebuild index with explicit metric flag, verify cosine vs. IP end-to-end, and re-probe ΔS vs k (aim ≤ 0.45).
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Session-to-session flips between backfills and scheduled runs → stamp and check `mem_rev`/`mem_hash` and pin image digests per task.
  [Patterns: Memory Desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)

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

