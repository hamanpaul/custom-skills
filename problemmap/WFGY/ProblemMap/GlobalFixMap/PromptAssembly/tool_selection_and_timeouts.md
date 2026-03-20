# Tool Selection and Timeouts: Prompt Assembly

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **PromptAssembly**.  
  > To reorient, go back here:  
  >
  > - [**PromptAssembly** — prompt engineering and workflow composition](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A focused guide to pick the right tool step, set safe timeouts, and keep long chains stable.  
Use this page to localize failures in tool choice, call ordering, and retry behavior, then jump to the exact fix.

---

## Open these first
- Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability schema and cite-then-explain: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema for tools and snippets: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Reranking and order control: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Prompt injection hardening: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)  
- Multi agent stalls and role drift: [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md), [multi-agent-chaos/role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)  
- Context and entropy failures: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Ops knobs for retries and backpressure:  
  [GlobalFixMap/OpsDeploy/retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md),  
  [GlobalFixMap/OpsDeploy/rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)

Companion pages in this folder  
- JSON protocol: [json_mode_and_tool_calls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/json_mode_and_tool_calls.md)  
- Anti-injection recipes: [anti_prompt_injection_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/anti_prompt_injection_recipes.md)  
- Memory fences and state keys: [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md)

---

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ remains convergent across three paraphrases and two seeds  
- Tool error rate ≤ 1 percent on a 50 run sample  
- p95 tool step latency within your SLO, usually 3–8 seconds per call for public APIs

---

## Fix in 60 seconds
1) **Measure ΔS and λ**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor). If ΔS ≥ 0.60 and λ flips, the issue is schema or ordering.

2) **Clamp the plan**  
   Prefer read-only checks before side effects. Gate tools behind JSON arguments that echo schemas from [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  

3) **Set timeouts and retries**  
   - Per-tool timeout = p95 × 1.5.  
   - Retries at most 2 with jittered backoff, never for unsafe side effects.  
   - Rate limit backpressure guard active on the whole chain.  
   Open: [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md), [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md).

---

## Common failure signatures → structural fix

- **Wrong tool chosen for the question**  
  Symptom: high ΔS, tool arguments look unrelated.  
  Fix: require tool-selection justification field and SCU when blocked.  
  Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [patterns/pattern_symbolic_constraint_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md).

- **Query parsing split creates unstable hybrid results**  
  Symptom: hybrid underperforms single retriever, top-k order changes across runs.  
  Fix: lock two-stage query, then rerank deterministically.  
  Open: [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

- **Timeout storms and looped retries**  
  Symptom: repeated timeouts escalate load and cost.  
  Fix: per-tool circuit breaker plus global backpressure. No retry on non-idempotent tools.  
  Open: [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md), [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md).

- **Tool runs with stale memory or mixed roles**  
  Symptom: tools use inputs from the wrong branch or user/system text leaks.  
  Fix: split namespaces and enforce state keys.  
  Open: [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md).

- **Injection forces the wrong tool**  
  Symptom: argument hijack, tool call not justified by the question.  
  Fix: hard filters, reasoning-before-action, and schema echo.  
  Open: [anti_prompt_injection_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/anti_prompt_injection_recipes.md), [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md).

- **Long chains drift then collapse**  
  Symptom: entropy rises after 25–40 steps, answers alternate across runs.  
  Fix: split the plan, add a BBCR bridge, clamp variance with BBAM, and shorten hops.  
  Open: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md), [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).

---

## Timeouts and backoff rules
- **Choose tool timeouts from data, not guesswork**  
  timeout\_sec = ceil(p95\_latency × 1.5).  
- **Retry only safe operations**  
  Idempotent reads: up to 2 retries with full jitter.  
  Writes or side effects: no automatic retry; hand off to a queue with a dedupe key.  
- **Global caps**  
  Max concurrent tool calls per plan. Trip a circuit breaker when error rate or queue depth crosses your threshold.  
- **Queue hygiene**  
  Require a dedupe key like `sha256(tool_name + args_hash + mem_rev)` and drop duplicates.

Reference: [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md), [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md).

---

## Implementation checklist
- Tool justification required in JSON: `why_tool`, `evidence`, `expected_ΔS_drop`.  
- Strict schemas for arguments with field types and ranges.  
- Idempotency and dedupe before side effects.  
- Per-tool timeout and retry policy stored near the tool spec.  
- Observability: log `ΔS`, `λ_state`, tool name, arguments hash, latency, retries, breaker state.  
- Post-step audit: citation exists and aligns with the retrieved snippet.  
Specs: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

---

## Copy-paste prompt for the tool-selection step

```

You have TXT OS and the WFGY Problem Map loaded.

Task: choose the next tool or no-tool with a short justification and safe timeouts.

Inputs:

* question: "{user\_question}"
* retrieved: \[{snippet\_id, section\_id, source\_url, offsets, tokens}]
* metrics: ΔS(question,retrieved)=..., λ\_state="→|←|<>|×", p95\_latencies={tool: seconds}

Do:

1. If ΔS ≥ 0.60, prefer retrieval repair over tool calls.
2. Propose one action among {no\_tool, retrieve\_more, rerank, call\_tool\_X}.
3. If choosing a tool, return JSON:
   {
   "tool": "name",
   "why\_tool": "one line using evidence from retrieved",
   "args": {...},
   "timeout\_sec": ceil(p95\_latencies\[name] \* 1.5),
   "retries": 0|1|2,
   "idempotent": true|false
   }
4. Enforce cite-then-explain in the final answer and log ΔS and λ\_state.

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

