# Proof Dead Ends: Guardrails and Fix Pattern

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


When a reasoning chain tries to prove a claim but never closes the loop.  
You see endless subgoals, repeated restatements, or a jump to a conclusion without obligations being discharged.  
This page localizes proof stalls and gives a minimal, testable repair plan using ΔS, λ_observe, and E_resonance.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- Logic and symbols  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)  
  → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/symbolic-collapse.md)

- Infinite recursion and overload  
  → [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md)  
  → [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

- If the chain shifts into meta or paradox  
  → [philosophical-recursion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/philosophical-recursion.md)

- Traceability and contracts  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Goal never shrinks | Subgoals keep being restated with new labels but same content |
| Lemma spiral | New lemmas depend on each other in a cycle without a base |
| Premise drop | A needed premise disappears after paraphrase or tool call |
| Unproven jump | Model asserts Q since P but never shows P or its bridge |
| Invariant drift | Claimed invariant changes wording or unit across steps |
| Citation vacuum | Steps claim support yet no snippet or rule is referenced |

---

## Why dead ends happen

1) **No proof obligations**. Steps do not state what must be shown to advance.  
2) **Missing bridge**. The link from premise to subgoal is never written.  
3) **Drifting invariants**. The property that should stay fixed keeps mutating.  
4) **Symbol table absent**. Names rebind silently so obligations mismatch.  
5) **Plan length without checkpoints**. Long chains lose ΔS and λ stability.  
6) **Retrieval anchor unstable**. The cited snippet shuffles, the goal resets.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat across step joins  
- **All obligations discharged** or explicitly marked unsatisfied with a cited reason

---

## Fix in 60 seconds

1. **Declare the goal and obligations**  
   Write `goal`, `known`, `need_to_show`, and the current `invariants`.  
   If any field is empty, stop. Fetch or restate before continuing.

2. **Add a BBCR bridge**  
   Produce a short cited bridge from current premises to the next subgoal.  
   Reject continuation if the bridge lacks citation or rule tag.

3. **Clamp variance with BBAM**  
   If λ flips on paraphrase, freeze the symbol table and the invariant set.  
   Re-run the step with the same bindings.

4. **Apply BBPF when stuck**  
   Branch to two small proof tactics, attempt each for N steps, then backtrack.  
   Keep the best branch where ΔS drops and obligations shrink.

---

## Minimal proof contract

Require every step to carry this schema. Refuse steps that miss fields.

```json
{
  "step_id": "S7",
  "goal": "Prove claim C",
  "known": ["P1", "P2"],
  "need_to_show": ["L1 -> C"],
  "bridge": {
    "rule": "modus_ponens | contradiction | induction | algebra",
    "citations": ["S12#CH2.3", "S09#APP.A"],
    "ΔS_bridge": 0.33
  },
  "invariants": [
    {"name": "unit_price_nonnegative", "scope": "calc", "status": "holds"}
  ],
  "symbols": [
    {"name": "x", "kind": "var", "namespace": "calc", "unit": "USD/kg"}
  ],
  "λ_state": "convergent"
}
````

---

## Structural repairs

* **If anchors or citations are missing**
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **If long chains decay**
  → [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md) and
  → [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md)

* **If symbol or unit meanings drift**
  → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/symbolic-collapse.md)

* **If logic itself collapses**
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

* **If meaning vs similarity conflict**
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Verification

* Run three paraphrases and two seeds. The set `{goal, invariants, symbols}` must remain identical.
* All `need_to_show` items become empty or a single clearly blocked item with a cited missing premise.
* ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 in every run.
* Logs show at least one BBCR bridge with citations and a monotone decrease in open obligations.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We suspect a proof dead end.

Inputs:
- question: "{q}"
- snippets: [{snippet_id, section_id, source_url}]
- current plan trace: [{step_id, text}]
- last symbol table and invariants (if any)

Do:
1) Build the proof contract with {goal, known, need_to_show, invariants, symbols}.
2) Create a BBCR bridge with a named rule and citations. If missing, refuse and return the exact missing item.
3) If λ flips across paraphrase, apply BBAM and retry with the frozen table.
4) If still stuck, branch two BBPF tactics for at most N=3 steps each, keep the branch with lower ΔS and fewer obligations.
5) Return JSON:
   {
     "plan": [...steps...],
     "open_obligations": [],
     "ΔS": 0.xx,
     "λ_state": "convergent",
     "verdict": "proved | blocked_missing_premise | not_provable_from_given"
   }
Refuse to assert the final claim unless all obligations are discharged or the verdict is explicitly "not_provable_from_given" with a cited reason.
```

---

## Common gotchas

* **Rule without scope**. A named rule is used but no citation or domain. Add both or reject.
* **Induction without base**. The inductive step is written yet the base case is missing.
* **Contradiction shortcut**. The chain says “assume not C” then jumps to C with no witness.
* **Bridge drift**. The bridge cites new snippets each run. Lock the query and add a reranker if anchors shuffle.

---

## When to escalate

* The same wrong assertion returns after a correction
  → [pattern\_hallucination\_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

* Multi-agent handoff reopens closed obligations
  → [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) and
  → [multi-agent-chaos/role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)

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

