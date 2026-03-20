# Retool — Guardrails and Fix Patterns

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

Use this when your stack uses **Retool** (Queries, Transformers, Workflows, Resources) and you see wrong snippets, unstable reasoning, mixed sources, or silent failures that look fine in logs.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Query returns plausible but wrong rows or snippets  
  Fix No.1: Hallucination and Chunk Drift →  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
  Also review the Retrieval Playbook →  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- High cosine similarity but meaning is wrong  
  Fix No.5: Embedding ≠ Semantic →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Some facts exist but never surface in search widgets or tables  
  Pattern: Vectorstore Fragmentation →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Citations missing or inconsistent between retriever result and LLM response  
  Fix No.8: Retrieval Traceability with Data Contracts →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Long chains flatten tone or drift logically in Workflows  
  Fix No.3 and No.9: Context Drift and Entropy Collapse →  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- App works in Preview but breaks after deploy or after environment switch  
  Fix No.16 and Infra family →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) ·
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- Confident tone but incorrect answers in AI components  
  Fix No.4: Bluffing and Overconfidence →  
  [Bluffing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)

---

## Minimal Retool pattern with WFGY checks

```js
// Retool App example: one LLM answer path with observable retrieval and WFGY checks

// 1) Retrieval query (REST or SQL). Keep params explicit and logged.
const k = 10;
const question = textInput_question.value;

// Example fetch to your retriever API
const retrieved = await retrieverApi.trigger({
  additionalScope: { question, k }   // ensure same tokenizer and metric across write/read
});

// 2) Assemble schema-locked prompt. Cite first, then explain.
const context = joinSnippets(retrieved.data);
const prompt = `
SYSTEM:
You must cite lines before any explanation.
TASK:
Answer the user's question using the provided context.
CONSTRAINTS:
- Do not mix sources
- Provide snippet_id for each citation
CONTEXT:
${context}
QUESTION:
${question}
`;

// 3) Call model
const answer = await llmApi.trigger({ additionalScope: { prompt }});

// 4) WFGY post-checks. Compute ΔS(question, context) and record trace table.
const metrics = await wfgyCheckApi.trigger({
  additionalScope: { question, context, answer: answer.data }
});

// 5) Fail fast when ΔS ≥ 0.60 or λ is divergent
if (metrics.data.deltaS >= 0.60 || metrics.data.lambda !== "→") {
  utils.showNotification("High semantic stress. See trace tab.", "warning");
  return { status: "needs_fix", ...metrics.data };
}

return { status: "ok", answer: answer.data, ...metrics.data };
````

**What this enforces**

* Retrieval is parameterized and observable in Retool Query logs.
* Prompt is schema locked with citation first.
* WFGY check runs after generation and can stop the run when ΔS is high or λ flips.
* Traces are kept as a snippet to citation table for audit.

Reference specs
[RAG Architecture and Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Retool specific gotchas

* Resource points to a different environment or secret than the indexer used. Pin versions and verify headers.
  See [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* Mixed metrics or normalization between ingestion code and query code in Workflows. Rebuild with explicit metric and unit normalization.
  See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Transformers silently reshape or re-rank without trace. Require cite first and include `snippet_id` headers.
  See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* Parallel queries cause ordering instability. Add a rerank step only after per-source ΔS ≤ 0.50.
  See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* Workflow scheduled runs build a fresh index incorrectly. Enforce idempotent builds with boot checks.
  See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## When to escalate

* ΔS stays ≥ 0.60 after chunk and retrieval fixes
  Work through the playbook and rebuild index parameters.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Answers flip between environments or sessions
  Verify version skew and session state.
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

