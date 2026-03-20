# Hallucination Re-entry: Guardrails and Fix Pattern

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


A “re-entry” is when a model repeats a previously corrected false claim later in the run or in a new turn.  
This page localizes re-entry causes and gives a minimal, testable repair plan.

---

## Symptoms

| Symptom | What you see |
|---|---|
| Corrected once, comes back later | Old claim resurfaces after a few steps or a new tool call |
| Cite-then-explain violated | Answer asserts conclusion before citing the corrected snippet |
| Reruns flip | Same prompt order, different run re-asserts the wrong claim |
| Memory relapse | Cross-turn memory re-injects the debunked statement |
| Hybrid retrieval drift | HyDE + BM25 changes top-k ordering and re-pulls the wrong chunk |

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ convergent across 3 paraphrases and 2 seeds  
- Re-entry rate = 0 on a 20-case regression set

---

## Structural fixes (Problem Map)

- Snippet and citation locks  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  → Citation-first recipe: [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md)

- Ordering control and hybrid stability  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
  → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

- Memory isolation and fences  
  → [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)  
  → [pattern_memory_desync.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)  
  → [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md)

- Entropy and chain control  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Pattern deep dive  
  → [pattern_hallucination_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

---

## Why re-entry happens

1) **No hard contract for citations**  
   Model can answer without binding to `snippet_id` or `section_id`.

2) **Prompt header drift**  
   Header reorder flips λ state and reopens earlier branches.

3) **Hybrid order instability**  
   HyDE or BM25 changes top-k; the older wrong chunk returns to rank 1.

4) **Memory namespace collision**  
   Corrected state is not isolated; prior summary re-injects the error.

5) **Reranker variance**  
   Non-deterministic tie-breakers reorder near-duplicates.

---

## Fix in 60 seconds

1. **Lock cite-then-explain**  
   Enforce a snippet contract in every reasoning step.  
   See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

2. **Deterministic reranking**  
   Freeze analyzer and tie-break rules. Probe k ∈ {5,10,20}.  
   See [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

3. **Memory fences**  
   Split namespaces: `facts/`, `debunks/`, `plans/`. Write debunk hashes into `debunks/`.  
   See [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md).

4. **Clamp variance with BBAM**  
   If λ flips across paraphrases, apply BBAM and re-run with fixed headers.

5. **Bridge with BBCR**  
   Summarize the correction into a single anchored statement and require future turns to import it before reasoning.

---

## Minimal schema addendum

Add these fields to your snippet payload and logs:

```json
{
  "snippet_id": "S123",
  "section_id": "CH2.3",
  "source_url": "https://...",
  "offsets": [221, 348],
  "tokens": 256,
  "debunk_hash": "sha256(<claim_text + snippet_id>)"
}
````

The LLM must include `debunk_hash` in its final JSON if it overturns a claim. On future turns, reject answers that assert a claim whose hash is already present in `debunks/`.

---

## Verification

* Run 20 paraphrases on the same case set.
* Require: ΔS(question, retrieved) ≤ 0.45 and λ convergent on two seeds.
* Zero tolerance for re-entry across all 20 cases.
* If any case fails, inspect reranker tie-break and memory fence writes.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We corrected a false claim earlier, but it reappeared later.
Inputs:
- question: "{q}"
- current snippets: [{snippet_id, section_id, source_url}]
- prior debunks: [{debunk_hash, claim_text, snippet_id}]
- ΔS and λ traces across 3 paraphrases

Do:
1) Identify which layer caused re-entry (schema, retrieval, rerank, memory, reasoning).
2) Apply the minimal fix referencing:
   retrieval-traceability, data-contracts, rerankers, memory_fences_and_state_keys.
3) Return a JSON plan with:
   { "citations": [...], "answer": "...", "ΔS": 0.xx, "λ_state": "...",
     "debunk_hashes_used": [...], "next_fix": "..." }
4) Refuse to output an answer if citations are missing or conflict with debunks.
```

---

## When to escalate

* Re-entry persists after fences and deterministic rerank
  → re-check hybrid split: [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

* Cross-turn relapse in long dialogs
  → audit joins and entropy: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* Agent handoff resurrects old claims
  → isolate memory and roles: [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)

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

