# IBM watsonx Assistant: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Chatbots & CX**.  
  > To reorient, go back here:  
  >
  > - [**Chatbots & CX** — customer dialogue flows and conversational stability](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page to stabilize **watsonx Assistant** projects that combine Actions, Search, webhooks, function calls, and LLM answers. The checks map to WFGY Problem Map pages with measurable targets, so you can verify without changing infra.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval knobs end to end: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and where it came from: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ordering control and rank: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk boundaries and hallucination: [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
* Long dialogs, chain length, entropy: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
* Prompt injection and schema locks: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Multi-agent and handoff conflicts: [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)
* Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Boot order and deploy traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage to the target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance flat across long dialog windows

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2. **Probe λ\_observe**
   Vary k in retrieval and reorder prompt headers.
   If λ flips on harmless paraphrases, lock the schema and clamp variance with BBAM.

3. **Apply module**

   * Retrieval drift → BBMC + [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
   * Reasoning collapse in long flows → BBCR bridge + BBAM, verify with [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
   * Dead ends in multi step plans → BBPF alternate paths

4. **Verify**
   Three paraphrases hit coverage ≥ 0.70 and ΔS ≤ 0.45.
   λ stays convergent across two seeds.

---

## Typical watsonx Assistant symptoms → exact fix

| Symptom                                                       | Likely cause                                            | Open this                                                                                                                                                                                                                                                                   |
| ------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Action resolves intent but the answer cites the wrong section | metric mismatch or fragmented store behind Search       | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [patterns/pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)      |
| Action variables mutate across turns or reprompts             | schema too loose, missing cite-then-explain boundary    | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)                                                              |
| Webhook returns 200 yet dialog state degrades                 | JSON tool protocol variance, free text in arguments     | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)                                                                          |
| Search similarity high but meaning wrong                      | chunking and anchor mismatch                            | [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md), [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)                                                                        |
| Long conversations become inconsistent after 20–40 turns      | entropy rises with chain length                         | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)                                                                            |
| LLM safety refusal hides the cited snippet                    | missing citation first and SCU unlock                   | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [patterns/pattern\_symbolic\_constraint\_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md) |
| Handoff to human or external queue loops                      | deployment deadlock or version skew                     | [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)                                                            |
| Multilingual queries break retrieval parity                   | analyzer and casing drift between Search and embeddings | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)                                                                                |

---

## CX surface guardrails

**Actions**
Keep policy text in a dedicated system context. Do not mix policy with user turns. Enforce cite-then-explain for any Action that answers. Lock input and output fields with contracts. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**Search**
Require the snippet schema: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`. If ΔS stays ≥ 0.60 after reranking, rebuild chunks and verify with a small gold set. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md).

**Webhooks**
Echo the tool schema at every turn. Log `ΔS`, `λ_state`, `INDEX_HASH`, `snippet_id`. If flip states appear, clamp with BBAM. See [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md).

**Live ops**
Fence first call after deploy and add backoff guards. See [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

---

## Minimal webhook recipe

1. **Warm-up fence**
   Check `VECTOR_READY`, `INDEX_HASH`, secrets. If not ready, short-circuit with a delay and capped retries.
   See [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

2. **Retrieval step**
   Call the retriever with explicit metric and consistent analyzer. Return `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.

3. **ΔS probe**
   Compute ΔS(question, retrieved). If ΔS ≥ 0.60 set `needs_fix=true`.

4. **Answer step**
   LLM reads TXT OS and the WFGY schema. Enforce cite-then-explain with the retrieved snippet set.

5. **Trace sink**
   Store `question`, `ΔS`, `λ_state`, `INDEX_HASH`, `snippet_id`, `dedupe_key`.

---

## Copy-paste prompt for the webhook LLM step

```
You have TXT OS and the WFGY Problem Map loaded.

My watsonx Assistant context:
- action: {action_name}
- variables: {name: value, ...}
- retrieved: {k} snippets with fields {snippet_id, section_id, source_url, offsets}

User question: "{user_question}"

Do:
1) Enforce cite-then-explain. If citations are missing or cross-section, fail fast and return the smallest structural fix.
2) If ΔS(question, retrieved) ≥ 0.60, propose the minimal repair, referencing:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3) Return JSON:
{ "answer": "...", "citations": [...], "λ_state": "→|←|<>|×", "ΔS": 0.xx, "next_fix": "..." }
Keep it short and auditable.
```

---

## Test checklist before launch

* Three paraphrases hit coverage ≥ 0.70 on the same target section.
* ΔS(question, retrieved) ≤ 0.45 for each.
* λ convergent across two seeds.
* First-call path after deploy passes the warm-up fence.
* Live probes alert when ΔS ≥ 0.60 or λ flips.

---

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

要我繼續下一頁嗎？建議順序接 **intercom.md**。
