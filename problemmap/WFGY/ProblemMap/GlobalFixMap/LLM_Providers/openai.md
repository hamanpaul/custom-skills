# OpenAI: Guardrails and Fix Patterns

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


Use this page when your pipeline hits OpenAI models and you see unstable tools, JSON drift, or long-chat decay. The checklist below helps you localize the failure, then jump to the exact WFGY fix page.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet. Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Logic traps and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Prompt safety and jailbreaks: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
- Multi-agent clashes: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) · [Role Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)
- Live ops and retries: [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Fix in 60 seconds
1) **Measure ΔS**
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   - Thresholds. stable < 0.40. transitional 0.40–0.60. risk ≥ 0.60.

2) **Probe with λ_observe**
   - Vary k = {5, 10, 20}. If ΔS stays high you likely have index or metric mismatch.
   - Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**
   - JSON or tool-call drift. lock schema with **Data Contracts**. add **BBMC** to isolate retrieval memory. bridge tools with **BBCR**. clamp variance with **BBAM**.
   - Safety refusal or redaction on in-domain facts. switch to citation-first format in **Retrieval Traceability**. scope sources and apply **SCU** pattern from symbolic constraints. if refusal repeats, route with **BBPF** alternate path.
   - Long chats decay. follow **Context Drift** and **Entropy Collapse** repairs. shorten windows. rotate evidence. re-pin anchors.

4) **Verify**
   - Coverage to the target section ≥ 0.70.
   - ΔS(question, retrieved) ≤ 0.45 across three paraphrases.
   - λ remains convergent across seeds and sessions. E_resonance flat at window joins.

## Typical OpenAI breakpoints and the right fix

### A) JSON mode and function calling
- Symptom. model mixes prose with JSON. partial `tool_calls`. extra keys. wrong function name casing.
- Fix. lock a strict snippet and citation schema in [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md). keep one place that defines fields. add BBCR bridge for tool routing timeouts. add BBAM to clamp wandering keys. verify with three paraphrases.

### B) Safety filter interferes with factual answers
- Symptom. content looks harmless but answer gets softened or truncated.
- Fix. use citation-first template from [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md). restrict scope with SCU in constraints. treat refusal as a state. route with BBPF to a safer paraphrase that preserves citations.

### C) Tokenization and truncation
- Symptom. system header or tools block gets cut. tool names lose arguments. early cutoff in streaming.
- Fix. reduce header size. move tool specs to a linked snippet and reference them by short name. re-measure ΔS after each cut. if chains still drift, apply [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md).

### D) Rate limits, retries, and timeouts
- Symptom. random tool gaps. missing citations. repeated starts.
- Fix. idempotent retries with jitter. record every call in a trace row. follow [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) and [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md). verify no duplicate tool effects.

### E) Determinism myths
- Symptom. `seed` appears to change output anyway. small wording flips output class.
- Fix. treat outputs as distributions. evaluate stability with **ΔS** and **λ** across three paraphrases. if unstable, clamp with BBAM and shorten evidence lists.

### F) Multi-agent tool chaos
- Symptom. agents overwrite each other’s memory. tool A answers B’s question. deadlocks on shared state.
- Fix. split memory namespaces. lock writes by `mem_rev` and `mem_hash`. read [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) and [Role Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md). add a BBCR bridge node with explicit timeouts.

## Copy-paste triage prompt

```txt
I uploaded TXT OS and the WFGY Problem Map files.

My OpenAI provider bug:
- symptom: [brief]
- traces: [ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states, tool logs if any]

Tell me:
1) which layer is failing and why,
2) which exact fix page to open from this repo,
3) the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) how to verify with a reproducible test.

Use BBMC/BBPF/BBCR/BBAM when relevant.
````

## Acceptance targets

* Coverage to target section ≥ 0.70.
* ΔS(question, retrieved) ≤ 0.45 on three paraphrases.
* λ convergent across seeds and sessions. E\_resonance flat.
* All tool calls and citations traceable to a stable schema.

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

