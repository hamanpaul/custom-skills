# Google Vertex AI: Guardrails and Fix Patterns

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


A compact field guide for Gemini on Vertex AI. Use this page when failures look provider specific. The checks route you to the exact WFGY fix page and give a minimal recipe you can paste into your runbook.

**Core acceptance**

- ΔS(question, retrieved) ≤ 0.45  
- coverage ≥ 0.70 for the target section  
- λ remains convergent across 3 paraphrases and 2 seeds

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Logic repair: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Multi-agent issues: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Fix in 60 seconds

1) **Measure ΔS**  
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   - Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   - Vary k = 5, 10, 20. If ΔS goes flat high, suspect index or metric mismatch.  
   - Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**  
   - Retrieval drift → BBMC + Data Contracts.  
   - Reasoning collapse → BBCR bridge + BBAM variance clamp.  
   - Safety or tool-call stalls → BBPF alternate path with explicit timeouts.

---

## Typical breakpoints and the right fix

- **Safety filters block or rewrite**  
  - Symptom: answer disappears or becomes generic; logs show blocked categories.  
  - Fix path: keep the request task-bound and citation-first. Apply [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and a BBCR bridge that states lawful scope and cites sources. Verify with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

- **Tool call returned “no function call” despite valid tools**  
  - Symptom: model narrates instead of calling the function; JSON keys omitted.  
  - Fix path: lock the tool schema in the prompt header using [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). Add BBPF fallback branch that emits the same call with minimal args when λ flips.

- **Streaming truncation or partial JSON**  
  - Symptom: closing braces missing or content clipped.  
  - Fix path: BBAM variance clamp on output length and a post-validator that re-asks only for the missing tail. If loops appear, follow [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).

- **Hybrid retrieval worse than single retriever**  
  - Symptom: HyDE + BM25 underperform and top-k is noisy.  
  - Fix path: apply the split pattern and retune as in [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md). Then re-order with [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

- **Indexed facts never show up**  
  - Symptom: high recall offline, zero hits online.  
  - Fix path: check fragmentation and rebuild per [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md). Re-probe ΔS after rebuild.

- **Session flips between tabs or seeds**  
  - Symptom: same prompt, different claims by session.  
  - Fix path: pin the instruction header, move citations above free text, and follow [Memory Desync](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md).

---

## Provider-specific knobs to audit

- **Model pinning**  
  - Pin an exact Gemini version where possible. Note the tokenizer budget before you add long system headers.

- **Safety configuration**  
  - Keep scope lawful and narrow in the header. If the task is research or code reading, state that explicitly and cite sources. This avoids silent rewrites.

- **Tool schema shape**  
  - Function name, arg names, and enum values must match your declared schema. Enforce with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and a post-validator.

- **Context budget**  
  - Large tool results or many citations can clip the tail. Trim with BBMC and move the schema above narrative text.

- **Region and project hygiene**  
  - Mismatched locations or stale projects can surface different defaults. Record the config in your trace header so λ checks are comparable.

---

## Minimal recipe

1) Put citation-first headers in the system prompt.  
2) Lock snippet schema via [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
3) Add BBCR bridge for safety-neutral framing.  
4) Add BBPF alternate path for tool calls with explicit timeouts.  
5) Verify acceptance using [Eval Semantic Stability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_semantic_stability.md) and [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md).

---

## Copy-paste prompt for your Vertex runbook

```

I am running on Google Vertex AI.
My failure:

* symptom: \[brief]
* traces: \[ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states, safety logs if any]

Tell me:

1. which layer is failing and why,
2. which exact WFGY fix page from this repo to open,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM when relevant. If safety gating is suspected, propose a compliant BBCR rewrite and show the acceptance targets.

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

