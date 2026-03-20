# ProblemMap/GlobalFixMap/LLM_Providers/aws_bedrock.md

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


# AWS Bedrock: Guardrails and Fix Patterns

Use this page when failures look provider‐specific in AWS Bedrock. Typical cases are mismatched model routing (Claude, Llama, Mistral, etc.), JSON schema drift, tool-call latency, throttle ceilings, or region/IAM issues that masquerade as “reasoning bugs.” Each fix maps to WFGY pages so you can verify with measurable targets.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Ops and live checks: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

---

## Fix in 60 seconds

1) **Measure ΔS**
- Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
- Targets: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**
- Vary k ∈ {5, 10, 20}. Flat high curve → index or metric mismatch.
- Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**
- Retrieval drift → **BBMC** + **Data Contracts**.
- Reasoning collapse → **BBCR bridge** + **BBAM variance clamp**.
- Dead ends in long runs → **BBPF** alternate path.

4) **Verify**
- Coverage to target section ≥ 0.70.
- ΔS ≤ 0.45 within three paraphrases.
- λ stays convergent across seeds and sessions.

---

## Typical Bedrock breakpoints (and the right fix)

- **Model routing not what you think**  
  Invoking `anthropic.claude-*` vs `meta.llama-*` vs `mistral.*` changes tokenizer, max tokens, and tool-call behavior. If outputs flip between routes, pin the model id per task, then re-check with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) and [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

- **JSON schema drift in tool use**  
  Claude via Bedrock is strict on JSON when `toolChoice` is forced. Lock the output schema with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and add a BBCR bridge step that rejects non-conformant fields.

- **Latency spikes → hidden timeouts**  
  Region hop or Guardrails policy checks can add latency. Use small test prompts and trace λ per step. If λ diverges only when tools are enabled, set a shorter planning window and split tools by namespace. See [ops/live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md).

- **Bedrock “Guardrails” over-filtering**  
  Safety filters can truncate citations or code blocks. If citations vanish, lower the filter aggressiveness, then enforce source-only answers with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and the SCU pattern ([symbolic constraint unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)).

- **Context windows differ across routes**  
  If the same prompt collapses only on one model family, shrink the active window and re-chunk. Validate with [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).

- **IAM or region misconfig → “reasoning” looks random**  
  On silent fallbacks or throttling, the agent loops. Install a BBCR checkpoint that asserts model id, region, and rate state before long chains. If it fails, exit early and surface infra status. See [bootstrap-ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [predeploy-collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).

---

## Provider knobs and minimal recipes

- **Pin model and cap tokens**
  - One task, one model id. Keep a per-task max tokens map.
  - If you must swap models, add BBPF to branch at the planner step, not mid-reasoning.

- **Force citations first**
  - Use citation-first headers and the snippet schema from [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).  
  - Reject answers without snippet ids. That alone removes most “looks like hallucination” cases.

- **Defuse prompt injection**
  - Apply the injection checklist and keep tools off until the source set is locked. See [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md).

- **Rerank aggressively**
  - Many Bedrock routes benefit from tighter top-k ordering. Use [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and then re-test ΔS across 3 paraphrases.

---

## Escalation path

- If ΔS flat-high across k and models → rebuild index with new metric. Check [embedding-vs-semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).
- If agent deadlocks with tools → split memory namespaces and add timeouts. See [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md).
- If first prod call fails after deploy → confirm ordering with [bootstrap-ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [deployment-deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md).

---

## Copy-paste prompt (safe)

```

I uploaded TXT OS and the WFGY ProblemMap files.

My Bedrock issue:

* symptom: \[brief]
* traces: \[ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states]

Tell me:

1. which layer is failing and why,
2. which exact fix page to open from this repo,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify the fix with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM when relevant.

```

---

### Acceptance targets
- Coverage to target section ≥ 0.70  
- ΔS(question, retrieved) ≤ 0.45 within three paraphrases  
- λ remains convergent across seeds and sessions  
- E_resonance flat on long windows

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

