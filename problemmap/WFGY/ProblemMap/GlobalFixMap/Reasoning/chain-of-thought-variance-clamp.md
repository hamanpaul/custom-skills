# Chain of Thought Variance Clamp: Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Reasoning**.  
  > To reorient, go back here:  
  >
  > - [**Reasoning** — multi-step inference and symbolic proofs](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Reduce random drift in planning and multi step reasoning. This page gives a clamp recipe so your plan length, tool order, and citations stay stable across seeds and paraphrases.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end knobs  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Traceability and payload schema  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Related failures  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) ·
  [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md) ·
  [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md) ·
  [hallucination-reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/hallucination-reentry.md) ·
  [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md)

- Prompt fences  
  → [PromptAssembly memory fences & state keys](https://github.com/onestardao/WFGY/blob/main/ProblemMap/PromptAssembly/memory_fences_and_state_keys.md)

- Eval  
  → [eval_semantic_stability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_semantic_stability.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Same inputs, different plans | Tool order or step count changes by run |
| Paraphrase flips the answer | Harmless wording changes cause new chain or conclusion |
| JSON plan reshuffles | Fields reorder or optional fields go missing |
| Intermittent tool loops | One seed calls tools twice, another once |
| Cite then explain breaks | Citations disappear in long chains or only appear sometimes |

---

## Why variance explodes

1) **Unpinned headers**. Role and policy text move around between runs.  
2) **Loose schemas**. Plans allow free text where enums should exist.  
3) **No state keys**. Chains cannot carry `plan_rev`, `seed_id`, or `λ_target`.  
4) **Ranking variance**. Inputs to the chain are not deterministically ordered.  
5) **No bridges**. Cross window steps lack an anchor restatement.  
6) **High entropy**. Overlong prompts and mixed analyzers amplify randomness.

---

## Acceptance targets

- λ remains convergent across three paraphrases and two seeds  
- ΔS(question, plan_header) ≤ 0.45 and flat across seeds  
- Plan length variance ≤ 10 percent across two seeds  
- Tool call sequence identical for the same evidence set  
- Coverage of target section ≥ 0.70 with cite then explain intact

---

## Fix in 60 seconds

1) **Lock the header order and schema**  
   Pin system header segments and require cite then explain.  
   → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
   [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

2) **Attach state keys**  
   Carry `{plan_rev, seed_id, λ_target, index_hash, context_hash}` through each step.  
   → [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/PromptAssembly/memory_fences_and_state_keys.md)

3) **Apply BBAM variance clamp**  
   Two stage plan. Stage A generates the plan at low temperature with enumerated options and a deterministic tie break. Stage B executes the plan with normal temperature but cannot change step count or tool order unless it emits a structured re plan request.

4) **Deterministic ordering in inputs**  
   Sort snippets by `(doc_id, section_id, win_idx)` after rerank.  
   → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

5) **Add BBCR micro bridges at joins**  
   Restate the active anchor and the current step goal across window boundaries.  
   → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)

---

## Minimal clamp contract

Add this struct to your plan steps. Enforce it in tools and in the LLM planner.

```json
{
  "plan_rev": 3,
  "λ_target": "convergent",
  "seed_id": "s1",
  "index_hash": "faiss:7c91...",
  "context_hash": "sha1:b2ae...",
  "steps": [
    {"idx": 1, "tool": "retrieve", "args_schema": "strict", "may_branch": false},
    {"idx": 2, "tool": "analyze_snippets", "args_schema": "strict", "may_branch": false},
    {"idx": 3, "tool": "answer", "args_schema": "strict", "may_branch": false}
  ],
  "tie_break": "doc_id,section_id,win_idx"
}
````

Rules

* Stage A can only choose among enumerated step templates.
* Stage B cannot insert or remove steps. To change, it must emit `{replan:true, reason:"..."}` and stop.
* Tool args must be strict JSON with enums where applicable.

---

## Verification playbook

* Three paraphrase run with two seeds. λ stays convergent, plan length variance ≤ 10 percent.
* ΔS(question, plan\_header) ≤ 0.45 on both seeds.
* Citations appear before explanation in every run.
* Tie break yields the same snippet order across seeds.

If ΔS is flat and high, suspect index or metric mismatch.
→ [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
[chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

Goal: clamp chain-of-thought variance.

Inputs:
- question: "{q}"
- snippets: [{doc_id, section_id, win_idx, ΔS_to_question, source_url}]
- constraints: cite_then_explain=true, args_schema="strict"

Do:
1) Stage A (planner, low temperature 0.2–0.4):
   - Produce a fixed-length plan using the step templates {retrieve, analyze_snippets, answer}.
   - Order inputs deterministically by (doc_id, section_id, win_idx).
   - Output:
     {
       "plan_rev": n,
       "λ_target": "convergent",
       "seed_id": "{seed}",
       "steps": [{"idx":1,"tool":"retrieve"}, ...],
       "tie_break": "doc_id,section_id,win_idx"
     }

2) Stage B (executor):
   - Execute the plan without changing step count or order.
   - If a change is needed, stop and emit {"replan": true, "reason": "..."}.

3) Always return JSON:
   {
     "plan_rev": n,
     "answer": "... cite then explain ...",
     "λ_state": "convergent|divergent",
     "ΔS_plan_header": 0.xx,
     "coverage": 0.xx
   }
If λ is divergent or ΔS ≥ 0.60, include the exact fix page to open.
```

---

## Common gotchas

* Planner runs with a different header than executor. Keep a single pinned header block.
* Rerank uses a different analyzer than indexing. Normalize, then tie break deterministically.
* Tool schemas accept free text. Replace with enums and strict JSON.
* Bridges omitted at window boundaries. Re cite the anchor before continuing.
* Prompt injection or role drift unlocks free form steps. Lock system text and schema.
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

---

## When to escalate

* λ remains divergent after clamp and bridges
  → inspect long chain stability and collapse patterns.
  Open: [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) ·
  [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

* Live flip flops only in production
  → add live probes and slow ramp with backoff.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) ·
  [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

