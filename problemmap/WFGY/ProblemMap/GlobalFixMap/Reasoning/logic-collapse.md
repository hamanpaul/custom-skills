# Logic Collapse: Guardrails and Fix Pattern

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


When deduction chains flatten into platitudes, contradict earlier steps, or bypass citation locks, you have a logic collapse.  
This page localizes causes and gives a minimal, testable repair plan driven by ΔS, λ_observe, and WFGY modules.

---

## Symptoms

| Symptom | What you see |
|---|---|
| Deduction flips mid chain | Step t says A, step t+3 assumes not A |
| Cite after claim | Answer states conclusion first, citations appear later or mismatch |
| Tool result ignored | Structured tool output is not integrated into the final proof |
| Branch mixing | Two hypotheses or roles leak into one stream without arbitration |
| Infinite hedging | Long text, no invariant, no auditable steps |
| JSON schema drift | Different steps produce different fields for the same contract |

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat on long windows  
- Zero contradictions across the final plan and the citations

---

## Structural fixes (Problem Map)

- Cite first, then reason  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  → [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md)

- Stabilize ordering and reduce variance  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Prevent symbolic leakage and unlock constrained proof  
  → [patterns/pattern_symbolic_constraint_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

- Long chain stability and entropy control  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- If the claim keeps returning after correction  
  → [patterns/pattern_hallucination_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

- Multi agent conflicts and role drift  
  → [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)  
  → [multi-agent-chaos/role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)

---

## Why logic collapses

1) **No invariant**. There is no explicit statement of what must stay true across steps.  
2) **Citation contract missing**. The model is allowed to assert before binding to `snippet_id` and `section_id`.  
3) **Header drift flips λ**. Reordered system or tool headers produce different branches on each run.  
4) **Branch contamination**. Hypothesis A and B are not isolated, the plan merges silently.  
5) **Unruly tool I/O**. Free text is accepted where strict JSON was required.  
6) **Hybrid retrieval shuffle**. The top k changes and the proof silently re-anchors.

---

## Fix in 60 seconds

1. **Pin the invariant**  
   Add a short invariant header, for example:  
   `Invariant: conclusions must cite snippet_id and section_id before any reasoning.`

2. **Enforce cite-first**  
   Require the model to produce citations first, then the explanation.  
   See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md).

3. **Clamp variance with BBAM**  
   If λ flips across paraphrases, apply BBAM to keep one path stable.

4. **Bridge gaps with BBCR**  
   Summarize the current state into a compact, cited bridge, then continue reasoning on top of that single bridge.

5. **Lock schema and ordering**  
   Freeze headers, tool schemas, and reranker tie breaks.  
   See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

---

## Minimal step contract

Add this object to every step output. Reject the step if any field is missing.

```json
{
  "step": 7,
  "invariant": "cite-first, no cross-branch mixing",
  "citations": [
    { "snippet_id": "S17", "section_id": "CH3.2", "source_url": "https://...", "offsets": [102, 188] }
  ],
  "claim": "X implies Y under condition Z",
  "justification": "Short, refers to citations only",
  "λ_state": "convergent",
  "ΔS_q_snip": 0.31,
  "next_action": "verify Z across S24",
  "guardrails": { "schema_version": "v1", "tie_break": "stable" }
}
````

---

## Verification

* Three paraphrase probe, two seeds.
* Require ΔS(question, retrieved) ≤ 0.45 and λ convergent in all runs.
* No contradictions between any step claim and earlier steps.
* If any run fails, inspect header ordering and reranker tie breaks, then re-run.

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We suspect a logic collapse.
Inputs:
- question: "{q}"
- current snippets: [{snippet_id, section_id, source_url}]
- last 6 steps with {claim, citations, λ_state, ΔS_q_snip}

Do:
1) State a one line invariant for this task.
2) Produce citations first. If citations are missing or conflict, stop and output the minimal fix.
3) Apply BBCR to create a single cited bridge, then continue reasoning for at most 5 steps.
4) If λ flips across a paraphrase, apply BBAM and retry once.
5) Return JSON:
   { "invariant": "...", "steps": [...], "final_answer": "...",
     "ΔS": 0.xx, "λ_state": "convergent", "next_fix": "..." }
Refuse to output a final answer if any step lacks citations.
```

---

## When to escalate

* The chain keeps diverging after BBAM and bridge steps
  → audit for symbolic failure: [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md)

* The claim reappears after correction
  → see re-entry pattern: [patterns/pattern\_hallucination\_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

* Runs diverge only when agents hand off
  → isolate roles and memory: [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

* Long dialogs lose structure past window joins
  → stabilize joins and entropy: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

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

