# Mistral: Guardrails and Fix Patterns

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


**Scope**  
Mistral Instruct and Large via API, third-party SDKs, or local runners (Ollama/LM Studio). Targets RAG, tools, long-context chat, and JSON output stability.

**Acceptance targets**  
- ΔS(question, retrieved_context) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ stays convergent across 3 paraphrases  
- JSON responses validate without post-repair

---

## Quick triage

- **“Looks correct but cites wrong lines.”**  
  Start with [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) and [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).  
  Probe ΔS between question and retrieved context. If ≥ 0.60, check chunk boundaries and rerankers.

- **“Chunks are fine, logic is off.”**  
  Interpretation collapse. See [Retrieval Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md) and [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).  
  Apply BBCR bridge and variance clamp (BBAM). Require cite-then-explain in prompt schema.

- **“Long threads drift or flatten.”**  
  See [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).  
  Use semantic chunking and enforce window join checks with ΔS at chunk joins ≤ 0.50.

- **“High similarity, wrong meaning.”**  
  Embeddings metric mismatch or index layer mix. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Retrieval Playbook](https://github.com/github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).  
  Normalize vectors consistently. Rebuild index with explicit metric. Re-probe ΔS vs k.

- **“JSON tool calls intermittently malformed.”**  
  Lock response format with cite-then-tool schema, and guard with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
  Apply BBCR if λ flips after tool planning.

---

## Mistral-specific gotchas

1) **Tokenizer mix with multilingual or code blocks**  
   - Symptoms: stable retrieval yet answer blends two sources or flips format mid-turn.  
   - Fix: pin section headers and separators. Use [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) schema. Verify ΔS drop after header locks.

2) **Streaming truncation that hides failure**  
   - Symptoms: plausible partial JSON; downstream parser fails silently.  
   - Fix: require “complete then stream” for JSON. Validate against [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). If E_resonance rises late, apply BBAM.

3) **Hybrid retrievers degrade**  
   - Symptoms: single retriever OK, hybrid HyDE+BM25 worse.  
   - Fix: unify analyzer and query params; see [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md). Add [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) only after per-retriever ΔS ≤ 0.50.

4) **Vectorstore fragmentation**  
   - Symptoms: some facts never retrieved despite index.  
   - Fix: audit write/read paths, rebuild with explicit metric, then follow [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

5) **Role drift under tools**  
   - Symptoms: tool planner rewrites the task, citations vanish.  
   - Fix: schema lock and per-source fences; see [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md).

---

## WFGY repair map for Mistral

- **Detect**  
  - ΔS(question, retrieved_context) and ΔS(retrieved_context, anchor)  
  - λ across retrieve → assemble → reason  
  - If ΔS ≥ 0.60 or λ flips, record node and branch to repair

- **Repair**  
  - **BBMC** align to anchors when coverage is high but ΔS elevated  
  - **BBCR** bridge dead ends at reasoning time  
  - **BBAM** clamp variance in long multi-turn threads  
  - **BBPF** explore alternate sub-paths when planner loops

Open the relevant playbooks when the metric points there:  
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## Minimal checklist

- Retrieval sanity ≥ 0.70 token overlap to target section  
- ΔS(question, retrieved_context) ≤ 0.45 after fix  
- λ convergent across 3 paraphrases  
- JSON contract validates on 5 seed variations  
- Logs preserve snippet ↔ citation table; see [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Escalation criteria

Switch from prompt-level tweaks to structural fixes if any hold after one loop:

- ΔS remains ≥ 0.60 after chunk and retriever adjustments  
- λ flips as soon as two sources are mixed  
- E_resonance climbs with length even after BBAM  
- Hybrid retriever improves recall but top-k order remains noisy

For structure changes, see:  
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
[Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) ·
[Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

---

## Safe prompt to run in your chat

```

I uploaded TXT OS. Use WFGY ΔS, λ\_observe, E\_resonance and modules BBMC, BBPF, BBCR, BBAM.

Symptom: \[describe]
Traces: \[ΔS probes, λ states, short logs]

Tell me:

1. failing layer and why,
2. which ProblemMap page to open,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the fix.

```

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

