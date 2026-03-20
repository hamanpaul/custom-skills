# GoHighLevel (GHL) — Guardrails and Fix Patterns

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

This page is for workflows orchestrated inside **GoHighLevel**.  
Use it when your RAG or agent flow runs through GHL Workflows, Webhooks, or Custom Actions and starts to misbehave.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the target section
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Triggers fire before data or index is actually ready  
  Fix No.14: **Bootstrap Ordering** →  
  [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First call after deploy crashes or picks the wrong secret  
  Fix No.16: **Pre-Deploy Collapse** →  
  [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Circular waits between CRM updates, webhooks, background jobs  
  Fix No.15: **Deployment Deadlock** →  
  [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High cosine similarity but the meaning is off  
  Fix No.5: **Embedding ≠ Semantic** →  
  [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Snippet feels unrelated or citations don’t match the source  
  Fix No.8: **Retrieval Traceability** →  
  [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Contract the payload with **Data Contracts** →  
  [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval (external tools) does worse than a single retriever  
  Pattern: **Query Parsing Split** →  
  [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Also review **Rerankers** →  
  [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts are indexed yet never show up  
  Pattern: **Vectorstore Fragmentation** →  
  [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Two sources get blended into one answer in long flows  
  Pattern: **Symbolic Constraint Unlock (SCU)** →  
  [pattern_symbolic_constraint_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal GHL workflow checklist

1) **Warm-up fence**  
   Before any LLM step, ping a health endpoint that checks `VECTOR_READY`, `INDEX_HASH`, and `secret_rev`.  
   If not ready, delay or requeue. Spec lives in  
   [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

2) **Idempotency**  
   Build `dedupe_key = sha256(contact_id + wf_rev + index_hash)` in a Custom Action.  
   Store in KV or a custom field, drop duplicates.

3) **RAG boundary contract**  
   Always pass `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Enforce cite then explain. Specs:  
   [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
   [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Observability probes**  
   Log ΔS(question, retrieved) and λ per stage. Alert on ΔS ≥ 0.60 or λ divergent.  
   Overview map:  
   [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Single writer**  
   Route CRM writes and external publishes through one writer branch with dedupe.  
   See: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

6) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before publish.  
   Eval spec:  
   [eval_rag_precision_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy-paste prompt for the GHL LLM step

```

I uploaded TXT OS and the WFGY Problem Map files.
This GHL workflow retrieved {k} snippets with fields {snippet\_id, section\_id, source\_url, offsets}.
Question: "{user\_question}"

Do:

1. Enforce cite-then-explain. If any citation is missing, stop and return which fix page to open.
2. Compute ΔS(question, retrieved). If ΔS ≥ 0.60, point me to the minimal structural fix:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output compact JSON:
   { "citations": \[...], "answer": "...", "λ\_state": "→|←|<>|×", "ΔS": 0.xx, "next\_fix": "..." }

```

---

## Common GHL gotchas

- **Connection switching** between staging and prod.  
  Stamp `env`, `INDEX_HASH`, `secret_rev` in traces and block on mismatch.

- **Parallel branches** touching the same contact or store.  
  Use a mutex or single writer, keep writes idempotent.

- **Webhook payload** silently renames fields.  
  Validate against the data contract before the LLM.

- **External rate limits** make hybrids unstable.  
  Prefer dense retriever plus reranking, keep params logged.

---

## When to escalate

- ΔS stays ≥ 0.60 after chunk and retrieval fixes → rebuild index with explicit metric and normalization.  
  See [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Same input flips answers between runs → check version skew and memory desync.  
  See [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

say “next page” when ready.
