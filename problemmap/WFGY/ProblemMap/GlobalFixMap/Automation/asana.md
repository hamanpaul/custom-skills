# Asana — Guardrails and Fix Patterns

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

Use this page when your RAG or agent flow is orchestrated through **Asana** (rules, webhooks, custom apps) and behavior drifts: tasks duplicate, sections race, or citations don’t match the source.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the target section
- λ remains convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Webhooks or rules trigger **before** data/index is actually ready  
  Fix No.14: **Bootstrap Ordering** →  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First run after deploy crashes or uses the wrong secret  
  Fix No.16: **Pre-Deploy Collapse** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Parallel automations create circular waits (task → comment → external job → task)  
  Fix No.15: **Deployment Deadlock** →  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High cosine similarity but the retrieved text is not the intended meaning  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Citations don’t match snippets or “why this snippet?” is opaque  
  Fix No.8: **Retrieval Traceability** →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Standardize payloads with **Data Contracts** →  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval via external tools performs worse than single retriever  
  Pattern: **Query Parsing Split** →  
  [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Also review **Rerankers** →  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts are indexed but never surface  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Status rollups blend two sources into one narrative  
  Pattern: **Symbolic Constraint Unlock (SCU)** →  
  [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal Asana workflow checklist

1) **Warm-up fence**  
   Before any LLM step, call a health endpoint that verifies `VECTOR_READY`, `INDEX_HASH`, `secret_rev`.  
   If not ready, delay/requeue. Spec:  
   [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2) **Idempotency**  
   Build `dedupe_key = sha256(task.gid + wf_rev + index_hash)` and store it (custom field or external KV).  
   Drop duplicates on retries.

3) **RAG boundary contract**  
   Always pass `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`, `project_gid`.  
   Enforce **cite-then-explain**. Specs:  
   [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
   [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Observability probes**  
   Log ΔS(question, retrieved) and λ per stage; alert on ΔS ≥ 0.60 or divergent λ.  
   Overview map:  
   [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Single writer**  
   Route task/comments/field updates through one writer branch or one integration user with a mutex.  
   See:  
   [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

6) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before posting summaries back to Asana.  
   Eval spec:  
   [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy-paste prompt for the Asana LLM step

```

I uploaded TXT OS and the WFGY Problem Map files.
This Asana flow retrieved {k} snippets with fields {snippet\_id, section\_id, source\_url, offsets, project\_gid}.
Question: "{user\_question}"

Do:

1. Enforce cite-then-explain. If any citation is missing, stop and return which fix page to open.
2. Compute ΔS(question, retrieved). If ΔS ≥ 0.60, point me to the minimal structural fix:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output compact JSON:
   { "citations": \[...], "answer": "...", "λ\_state": "→|←|<>|×", "ΔS": 0.xx, "next\_fix": "..." }

```

---

## Common Asana gotchas

- **Webhook retries** produce duplicate tasks/comments  
  Use the `dedupe_key` and a KV lock; make writes idempotent.

- **Project/section renames** break downstream references  
  Pass `project_gid` and `section_id` explicitly in the data contract.

- **Parallel rules** edit the same fields  
  Funnel edits through a single writer branch or queue.

- **External rate limits** destabilize hybrids  
  Prefer dense retriever + reranking, keep per-retriever params logged.

---

## When to escalate

- ΔS remains ≥ 0.60 after chunk/retrieval fixes → rebuild index with explicit metric/normalization.  
  See:  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Same input yields different answers across runs → check version skew and memory desync.  
  See:  
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

