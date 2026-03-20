# Airtable — Guardrails and Fix Patterns

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

Use this when your pipeline uses **Airtable** as the control plane or as the source-of-truth table for RAG/agents, and you see record drift, duplicated actions, or citations that don’t map back to records.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the intended section/record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Automations/webhooks fire **before** embeddings/index finish updating  
  Fix No.14: **Bootstrap Ordering** →  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First run after deploy reads wrong base or missing secret  
  Fix No.16: **Pre-Deploy Collapse** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Cross-table syncs create circular waits (record-upsert → external job → back to record)  
  Fix No.15: **Deployment Deadlock** →  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High cosine similarity, wrong **meaning** (good vector match, bad semantic match)  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- “Why this snippet?” cannot be explained; citations don’t line up with source cells  
  Fix No.8: **Retrieval Traceability** →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Standardize fields with **Data Contracts** →  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval (dense + formula/filter views + external reranker) gets worse than single retriever  
  Pattern: **Query Parsing Split** →  
  [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Also review **Rerankers** →  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts are in the base but never retrieved  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Two different records are merged into one narrative in the summary  
  Pattern: **Symbolic Constraint Unlock (SCU)** →  
  [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal Airtable workflow checklist

1) **Warm-up fence**  
   Verify `VECTOR_READY`, `INDEX_HASH`, `secret_rev`, and that `base_id/table_id/view_id` resolve before any LLM step.  
   Spec: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2) **Idempotency**  
   Create `dedupe_key = sha256(record_id + wf_rev + index_hash)` and store it (hidden field or external KV).  
   Reject duplicate writes/retries.

3) **RAG boundary contract**  
   Pass `record_id`, `base_id`, `table_id`, `view_id`, `field_map`, `source_url`, `offsets`, `tokens`.  
   Enforce **cite-then-explain**. Specs:  
   [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
   [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Observability probes**  
   Log ΔS(question, retrieved) and λ per stage; alert on ΔS ≥ 0.60 or divergent λ.  
   Overview: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Schema stability**  
   Avoid free-form field renames that break downstream contracts. Pin with `schema_rev` and check it at runtime.

6) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before posting back into Airtable.  
   Eval spec: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy-paste prompt for the Airtable LLM step

```

I uploaded TXT OS and the WFGY Problem Map files.
Airtable context:

* base\_id: {base}
* table\_id: {table}
* view\_id: {view}
* record\_id(s): {rids}
* fields: {field\_map}
  Question: "{user\_question}"

Do:

1. Enforce cite-then-explain. If any citation lacks record\_id/section/offsets, stop and tell me which fix page to open.
2. Compute ΔS(question, retrieved). If ΔS ≥ 0.60, point me to the minimal structural fix:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output compact JSON:
   { "citations":\[{"record\_id":"...", "field":"...", "offsets":\[s,e]}],
   "answer":"...", "λ\_state":"→|←|<>|×", "ΔS":0.xx, "next\_fix":"..." }

```

---

## Common Airtable gotchas

- **Formula fields** or **lookup/rollup** not updated yet when webhook fires  
  Add a delay or readiness probe; gate on `schema_rev` + `index_hash`.

- **Pagination/backfill** causes missed embeddings  
  Log the cursor; re-ingest until the cursor is exhausted; compare counts vs. expected.

- **Field renames** break contracts silently  
  Pin `schema_rev`; fail fast if it changes; include `field_map` in traces.

- **Attachment/text mix** leads to partial content**  
  Normalize: extract attachments to text with a fixed OCR gate before embedding.

- **Rate limits** destabilize hybrid retrieval  
  Prefer dense retriever + reranking; keep per-retriever params in logs.

---

## When to escalate

- ΔS stays ≥ 0.60 after chunk/retrieval fixes → rebuild index with explicit metric/normalization.  
  See: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Same inputs, different answers on different runs → check version skew and memory desync.  
  See: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

