# Kimi (Moonshot) Guardrails and Fix Patterns

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


Use this page when failures look provider specific on Kimi. Examples include JSON mode drifting into prose, safety filters stripping citations, or streaming tool calls that stall. Each fix maps back to WFGY pages so you can verify with measurable targets.

**Core acceptance**

- ΔS(question, retrieved) ≤ 0.45  
- coverage ≥ 0.70 for the target section  
- λ remains convergent across 3 paraphrases

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Long threads and memory: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md), [Memory Coherence](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)  
- Logic collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Patterns: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md), [Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)  
- Ops: [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)  
- Multi-agent overview: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Fix in 60 seconds

1) **Measure ΔS**  
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   - Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   - Vary k = {5, 10, 20}. Flat high curve suggests index or metric mismatch.  
   - Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**  
   - Retrieval drift → BBMC + Data Contracts.  
   - Reasoning collapse → BBCR bridge + BBAM variance clamp.  
   - Dead ends in long runs → BBPF alternate path.

4) **Provider knobs to check first**  
   - Structured output mode on and schema fixed.  
   - Temperature and top_p conservative during diagnosis.  
   - Tool use set to serial if parallel calls cross-talk.  
   - Safety setting that removes citations set to a lower level during eval.

5) **Verify**  
   - Three paraphrases hold the same citations.  
   - λ convergent across seeds.  
   - E_resonance flat on long replies.

---

## Typical breakpoints and the right fix

- **JSON mode drifts into prose or extra commentary**  
  Lock a strict output schema with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). Add a BBCR “bridge” instruction that rejects non-JSON. If it still leaks, run a short two-turn repair using [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).

- **Chinese tokenizer quirks change similarity despite high cosine**  
  Treat it as metric mismatch. Use [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and add BM25 fallback in the [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md). Then re-rank with [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and anchor citations via [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

- **Safety filter strips citations or tool arguments**  
  Move citation text to a dedicated field in the schema and reference with IDs. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md). If the model “bluffs” when filtered, apply controls in [Bluffing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md).

- **Streaming tool calls stall or race**  
  Force single-tool steps and add timeouts. Trace with [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md). If agents fight over memory, see [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) and the memory patterns in [Memory Coherence](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md).

- **Long chat melts down after many pages**  
  Cut context windows at stable joins and verify with [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md). If replies “flip” across tabs, check [Memory Desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md).

- **Hybrid retrieval (HyDE + BM25) underperforms**  
  Look for query splits in [Pattern: Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md). Align the query parse and re-rank.

- **Non-English corpus drifts**  
  Follow the [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md). Normalize punctuation and numerals in chunking and traceability.

---

## Copy-paste prompt

```

I uploaded TXT OS and the WFGY Problem Map files.

My Kimi bug:
• symptom: \[brief]
• traces: \[ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states]

Tell me:

1. which layer is failing and why,
2. which exact fix page to open from this repo,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the fix with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM where relevant.

```

---

## Escalate when

- First call after deploy fails or tools fire before data is ready. See [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) and [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).  
- Deadlocks or version skew in prod. See [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md).

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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

