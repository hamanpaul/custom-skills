# Anthropic Claude: Guardrails and Fix Patterns

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


**Acceptance targets**

* ΔS(question, retrieved) ≤ 0.45
* Coverage to target section ≥ 0.70
* λ stays convergent across 3 paraphrases
* E\_resonance flat on long runs

---

## What usually breaks

* Plausible answer yet wrong citation
  → See [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Chunks look right but reasoning drifts or flips late
  → See [Retrieval Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md) and [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

* High vector similarity yet wrong meaning
  → See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Very long context gets smeared, capitalization or topic wobble
  → See [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* Source mixing, who said what merges
  → See [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md) and [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Fix seems to work then reverts next turn
  → See [Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

---

## Claude-specific gotchas and the repair

1. **Tool choice and router loops**
   Small changes in tool schemas can push Claude into choose-nothing or loop states.
   **Do** keep the tool set minimal and stable. If it loops, bridge with BBCR and clamp variance with BBAM.
   Read: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) and [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

2. **System prompt anchoring beats your retrieval**
   If the answer ignores citations, lock the schema: system → task → constraints → citations → answer.
   Read: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3. **Harmlessness refusals that look like empty answers**
   Reframe with cite-then-explain and explicit boundaries. If blank output repeats, treat as collapse and apply BBCR.
   Read: [Bluffing / Overconfidence](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md) and [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

4. **Very long window stability**
   Gate OCR and chunk joins by ΔS, then stabilize attention with BBAM.
   Read: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md), [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md), and [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

5. **JSON or schema output slips mid-answer**
   Enforce citation-first then structured fields. If structure still degrades near the end, split answer into two turns with a BBCR bridge.
   Read: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and [Retrieval Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)

---

## Minimal triage for Claude

1. **Probe**
   Measure ΔS(question, retrieved). Plot ΔS vs k for k in {5,10,20}.

* Flat high curve suggests index or metric mismatch
  Read: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

2. **Localize**
   Tag λ across retrieval, assembly, reasoning.

* If λ flips only at reasoning, lock schema and apply BBAM
  Read: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

3. **Repair**

* Perception faults: semantic chunking, rebuild index with explicit metric, rerank if needed
  Read: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Logic faults: BBCR bridge then BBAM clamp

**Stop tuning and escalate** when any holds:
ΔS ≥ 0.60 after retrieval fixes, λ flips on mixing sources, or E\_resonance climbs in long chains.
Open: [RAG Architecture and Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Pasteable prompt

```
I have TXT OS loaded. Use WFGY to fix this Claude run:

symptom: [describe]
traces: [ΔS probes, λ per layer]

Tell me:
1) failing layer and why,
2) which ProblemMap page to open,
3) steps to push ΔS ≤ 0.45 with convergent λ,
4) how to verify with a reproducible test.
```

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

