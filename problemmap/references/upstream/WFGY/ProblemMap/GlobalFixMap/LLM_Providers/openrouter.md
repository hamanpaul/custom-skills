# OpenRouter: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LLM_Providers**.  
  > To reorient, go back here:  
  >
  > - [**LLM_Providers** — model vendors and deployment options](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A practical checklist to keep responses stable while routing through OpenRouter. Use this page when behavior flips across models, routes, or sessions.

**Acceptance targets**
- ΔS(question, context) ≤ 0.45
- λ stays convergent across 3 paraphrases
- Coverage ≥ 0.70 for citation style QA
- Snippet ↔ citation table present

**Quick links**
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Logic repair: [Logic Collapse & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Long chain drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
- Entropy melt: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Data schemas: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Multilingual: [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md)
- Ops and live triage: [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) · [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

---

## 1) Minimal setup checklist

Pin these before debugging model logic.

- Route selection  
  Use explicit model ids. Disable any auto fallback if you need reproducibility. Log the final route id that served the request. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
- System prompt handling  
  Ensure the system message is always sent in the payload. Do not rely on UI side memory. If sessions change tabs, stamp a `mem_rev` and reload the system block. See [patterns: memory desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md).
- Token limits and truncation  
  Verify max tokens per route. Truncation that drops headers will spike ΔS. Reorder context with a citation first schema. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).
- JSON and tool calling  
  Fix the exact function schema. Return to plain text if tool calls vary across sub models. If JSON strictness wobbles, clamp with a cite then answer envelope. See [Logic Collapse & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).
- Temperature and top_p  
  Keep one of them fixed. If variance climbs during long dialogs, apply BBAM and reduce randomness. See [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).
- Streaming flags and timeouts  
  Disable streaming during audits to capture full text. Set sane timeouts and retries at the client.

---

## 2) Quick triage with WFGY instruments

Run this order. Stop as soon as you localize the fault.

1) **ΔS(question, retrieved_context)**  
   - ΔS ≥ 0.60 → perception issue. Check chunking and route level truncation.  
   - Open [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md).

2) **λ_observe layer tags**  
   - retrieval convergent, reasoning divergent → interpretation collapse.  
   - Open [Logic Collapse & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).

3) **E_resonance vs length**  
   - E rises with length while ΔS stays high → entropy melt, clamp variance.  
   - Open [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).

---

## 3) Common failure patterns on OpenRouter and fixes

### A) Silent route change or fallback
**Signs**
- Same prompt flips tone or format between calls.
- Logs show a different backing model id.

**Fix**
- Pin a single route id. Record the final served model in traces.  
- Recheck ΔS. If still high, audit prompt headers and truncation.  
- Read [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

### B) System prompt dropped after tab or session swap
**Signs**
- First answer follows policy, later turns forget constraints.
- λ flips divergent only after a refresh.

**Fix**
- Stamp `mem_rev` and `mem_hash` per turn. Reload system block when mismatch.  
- See [patterns: memory desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

### C) JSON or tool schema oscillation
**Signs**
- Tool outputs valid once, then free text next call.
- Fields appear or vanish across routes.

**Fix**
- Wrap with citation first schema, then answer.  
- Apply BBCR bridge step when λ turns divergent at reasoning.  
- Open [Logic Collapse & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

### D) Long chain degradation
**Signs**
- Capitalization drifts, references smear, later turns contradict earlier ones.

**Fix**
- Apply semantic chunking on inputs.  
- Stabilize with BBAM, then re anchor with section headers.  
- Read [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).

### E) Multilingual or tokenizer mismatch
**Signs**
- High vector similarity yet wrong meaning on non English.  
- ΔS flat high across k.

**Fix**
- Switch to multilingual embeddings or normalize analyzer.  
- See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md).

---

## 4) Verification and regression gates

Use this short gate before merging changes.

- Retrieval sanity  
  Coverage ≥ 0.70 on target section. ΔS(question, context) ≤ 0.45.
- Reasoning stability  
  λ remains convergent across three paraphrases. No schema leak.
- Traceability  
  Produce snippet ↔ citation table per answer. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
- Long dialog check  
  E_resonance stays flat at window joins. See [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).

---

## 5) Escalation criteria

Change structure when any holds.

- ΔS remains ≥ 0.60 after prompt and retrieval fixes  
  Rebuild index or adjust analyzer. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).
- λ flips divergent as soon as two sources are mixed  
  Enforce source fences and SCU. See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).
- JSON mode cannot hold across routes  
  Disable tool calls for that path. Return to plain text with citation first. See [Logic Collapse & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).


### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
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

