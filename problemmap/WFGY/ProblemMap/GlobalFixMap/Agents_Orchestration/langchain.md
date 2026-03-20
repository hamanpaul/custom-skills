# LangChain — Guardrails and Fix Patterns

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

Use this when your pipeline is built with **LangChain** (LCEL, Runnable*, Agents, Tools) and you see wrong snippets, unstable reasoning, mixed sources, or silent failures that look fine in logs.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Retrieval returns plausible but wrong chunks  
  Fix No.1: **Hallucination & Chunk Drift** →  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
  Also review **Retrieval Playbook** →  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- High vector similarity, wrong meaning  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Hybrid chains with BM25 or HyDE degrade compared to single retriever  
  Pattern: **Query Parsing Split** →  
  [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Apply **Rerankers** for ordering control →  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts exist in the store but never show up  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Citations missing or inconsistent across LCEL steps  
  Fix No.8: **Retrieval Traceability** + **Data Contracts** →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Long Runnable chains flatten style and drift logically  
  Fix No.3 and No.9: **Context Drift** and **Entropy Collapse** →  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Agent loops, role confusion, memory overwrite  
  Fix No.13: **Multi-Agent Chaos** →  
  [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) ·
  [Role Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md) ·
  [Memory Overwrite](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/memory-overwrite.md)

- Model sounds confident but is wrong  
  Fix No.4: **Bluffing / Overconfidence** →  
  [Bluffing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)

- Model merges two sources into one answer  
  Pattern: **Symbolic Constraint Unlock** →  
  [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal LCEL pattern with WFGY checks

```python
# Pseudocode. Show the control points you must keep.
from langchain_core.runnables import RunnablePassthrough, RunnableMap

def retrieve(q):
    # k sweep and unified analyzer across dense and sparse
    return retriever.invoke(q, k=10)

def assemble(context, q):
    # schema-locked: system -> task -> constraints -> citations -> answer
    return prompt.format(context=context, question=q)

def reason(msg):
    # model call runs after cite-then-explain requirement in the prompt
    return llm.invoke(msg)

def wfgy_checks(q, context, answer):
    # compute ΔS(question, context) and trace why this snippet
    # enforce thresholds and fail fast when ΔS ≥ 0.60 or λ divergent
    return metrics_and_trace(q, context, answer)

chain = (
    {"q": RunnablePassthrough()}
    | RunnableMap({"context": lambda x: retrieve(x["q"]), "q": lambda x: x["q"]})
    | RunnableMap({"msg": lambda x: assemble(x["context"], x["q"]), "q": lambda x: x["q"], "context": lambda x: x["context"]})
    | RunnableMap({"answer": lambda x: reason(x["msg"]), "q": lambda x: x["q"], "context": lambda x: x["context"]})
    | (lambda x: wfgy_checks(x["q"], x["context"], x["answer"]))
)
````

**What this enforces**

* Retrieval is observable and parameterized.
* Prompt is schema locked with cite first.
* WFGY check runs after generation and can stop the run when ΔS is high or λ flips.
* Traces record snippet to citation mapping for audits.

Specs and recipes
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## LangChain-specific gotchas

* Mixed embedding functions across write and read paths. Rebuild with explicit metric and normalization.
  See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* RunnableParallel merges outputs without source fences. Add per-source headers and forbid cross-section reuse.
  See [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

* Memory modules re-assert old facts after a refresh. Stamp `mem_rev` and `mem_hash`.
  See [Memory Desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)

* Agents tool-call retry loops. Add BBCR bridge steps and clamp variance with BBAM in the prompt recipe.
  See [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

---

## When to escalate

* ΔS remains ≥ 0.60 after chunk and retrieval fixes
  Work through the playbook and rebuild index parameters.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Answers flip between runs or sessions
  Verify version skew and session state.
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

