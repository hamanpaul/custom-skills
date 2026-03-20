# LangGraph: Guardrails and Fix Patterns

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

Use this page when your orchestration uses **LangGraph** (graph nodes, tool nodes, channels, subgraphs) and you see tool loops, wrong snippets, role mixing, or answers that flip between runs. The table maps symptoms to exact WFGY fix pages and gives a minimal recipe you can paste.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases and 2 seeds
- E_resonance stays flat on long windows

---

## Open these first

- Visual map and recovery  
  [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end retrieval knobs  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Why this snippet  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- Ordering control  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Embedding vs meaning  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Hallucination and chunk edges  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

- Long chains and entropy  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Structural collapse and recovery  
  [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

- Prompt injection and schema locks  
  [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

- Multi agent conflicts  
  [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

- Bootstrap and deployment ordering  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Snippet and citation schema  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Typical breakpoints and the right fix

- **Tool node returns free text instead of strict JSON**  
  Fix: lock arguments, echo schema, and gate on validation.  
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Edges create a loop or the run never reaches a terminal node**  
  Fix: add timeouts and BBCR bridge steps, log λ per hop, clamp variance with BBAM.  
  Open: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

- **High similarity yet wrong meaning**  
  Fix: metric or index mismatch, or mixed write and read embeddings.  
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Hybrid routes worse than a single retriever**  
  Fix: lock two stage query and add a deterministic reranker.  
  Open: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Facts exist in the store yet never surface**  
  Fix: fragmentation or sharding misalignment.  
  Open: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- **Citations missing or inconsistent across nodes**  
  Fix: require cite then explain and lock snippet fields.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Long running graphs change style and drift logically**  
  Fix: split subgraphs and rejoin with BBCR, measure entropy and stop when it rises.  
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- **Role confusion between planner and worker nodes**  
  Fix: stamp `mem_rev` and `mem_hash`, isolate namespaces, forbid cross section reuse.  
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Fix in 60 seconds

1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40 to 0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
   Do a k sweep in retrieval. Reorder prompt headers. If λ flips, lock the schema and clamp with BBAM.

3) **Apply the module**  
- Retrieval drift → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Reasoning collapse → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Hallucination re entry after a fix → [Pattern: Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

4) **Verify**  
   Coverage ≥ 0.70. ΔS ≤ 0.45. Three paraphrases and two seeds with λ convergent.

---

## Minimal LangGraph topology with WFGY checks

```python
# Pseudocode: focus on control points
from langgraph.graph import StateGraph, END

def retrieve(state):
    # k sweep and unified analyzer across dense and sparse
    return {"context": retriever.search(state["q"], k=10)}

def assemble(state):
    # schema-locked prompt with cite first
    msg = prompt.format(context=state["context"], question=state["q"])
    return {"msg": msg}

def reason(state):
    ans = llm.invoke(state["msg"])
    return {"answer": ans}

def wfgy_checks(state):
    # compute ΔS(question, context) and enforce thresholds
    # stop when ΔS ≥ 0.60 or λ divergent
    metrics = metrics_and_trace(state["q"], state["context"], state["answer"])
    if metrics["risk"]:
        return {"halt": True, "metrics": metrics}
    return {"metrics": metrics}

g = StateGraph(dict)
g.add_node("retrieve", retrieve)
g.add_node("assemble", assemble)
g.add_node("reason", reason)
g.add_node("wfgy_checks", wfgy_checks)

g.add_edge("retrieve", "assemble")
g.add_edge("assemble", "reason")
g.add_edge("reason", "wfgy_checks")
g.add_edge("wfgy_checks", END)

app = g.compile()
````

**What this enforces**

* Retrieval is observable and parameterized. Analyzer and metric are unified across paths.
* Prompt is schema locked with cite first. Snippet fields are required.
* Post generation WFGY checks can halt the run when ΔS is high or λ flips.

Specs and recipes
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## LangGraph specific gotchas

* Mixed embedding functions between write and read. Rebuild with explicit metric and normalization.
  See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Event storms caused by branching edges. Add idempotency keys and dedupe on `{source_id, mem_rev, index_hash}`.
  See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Subgraph recursion without a guard. Cap depth and time, insert BBCR bridge steps.
  See [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

* Memory modules re assert old facts after refresh. Stamp `mem_rev` and `mem_hash`.
  See [pattern\_memory\_desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)

* Streams are merged without source fences. Add per source headers and forbid cross section reuse.
  See [pattern\_symbolic\_constraint\_unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## When to escalate

* ΔS remains ≥ 0.60
  Rebuild the index using the checklists and verify with a small gold set.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Identical input yields different answers across runs
  Check version skew and session state.
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

要我接著做哪一個？建議順序：`crewai.md` → `smolagents.md` → `rewind_agents.md`（若你有其他優先順序，直接說 GO + 檔名）。
