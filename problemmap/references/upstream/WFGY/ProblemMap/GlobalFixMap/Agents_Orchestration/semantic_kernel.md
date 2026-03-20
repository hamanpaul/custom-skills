# Semantic Kernel — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Agents & Orchestration**.  
  > To reorient, go back here:  
  >
  > - [**Agents & Orchestration** — orchestration frameworks and guardrails](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

Use this when your pipeline uses **Semantic Kernel** planners, function tools, memories, or skills and you see wrong snippets, plan drift, tool loops, or JSON shape errors. The checks below localize the fault, then route to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Hybrid order control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Hallucination and chunk drift: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Prompt injection fences: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
- Long chain failures: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Agent role conflicts: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 for the intended section
- λ remains convergent across three paraphrases and two seeds

---

## Fix in 60 seconds

1) **Measure ΔS**  
Compute ΔS(question, retrieved) and ΔS(retrieved, anchor). Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Clamp the planner**  
Freeze the planner schema. Require task → constraints → tools → cite then explain. If plan text changes order between runs, lock headers and set deterministic seeds.

3) **Apply the module**  
- Retrieval drift → BBMC with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- JSON tool variance → tighten schemas and apply [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) fences  
- Long plans degrade → insert BBCR bridges and cap step depth per segment

4) **Verify**  
Three paraphrases reach ΔS ≤ 0.45 and coverage ≥ 0.70. λ stays convergent.

---

## Typical Semantic Kernel breakpoints → exact fixes

- **Planner invents tools or repeats steps**  
  Lock tool registry. Enforce idempotent effects with keys.  
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Memory recalls stale facts after refresh**  
  Split namespaces and stamp `mem_rev`, `mem_hash`.  
  Open: [patterns: memory desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)

- **High similarity yet wrong meaning**  
  Metric or analyzer mismatch across write and read paths.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Hybrid retrievers worse than single**  
  Query parsing split and misweighted rerank.  
  Open: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Tool call JSON fails silently**  
  Require strict argument schema. Echo schema at each call.  
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

---

## Minimal SK pattern with WFGY gates

```txt
Planner:
  1) Task
  2) Constraints: cite-first, snippet schema, tool JSON strict
  3) Tools with idempotency keys
  4) Answer: cite then explain

Runtime:
  - Retrieve(k = 10 with unified analyzer)
  - Assemble(prompt with headers in fixed order)
  - Reason(model call)
  - WFGY gate: compute ΔS, record λ, verify coverage
  - If ΔS ≥ 0.60 or λ divergent, stop and return fix tip
````

**What this enforces**

* Deterministic header order across steps
* Observable retrieval with stable metric
* Schema locked citations
* A stop gate when structure collapses

---

## SK specific gotchas

* Planner temperature is non zero while tools expect strict JSON. Set low variance and validate before acting.
* Memories are written by multiple skills without namespace fences. Use separate namespaces and revision stamps.
* Rerun of the same plan writes duplicate side effects. Add idempotency keys before external actions.

---

## When to escalate

* ΔS stays ≥ 0.60 after chunk and retrieval fixes
  Rebuild index and recheck analyzers.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Answers flip between sessions with unchanged inputs
  Check version skew and deploy order.
  Open: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

