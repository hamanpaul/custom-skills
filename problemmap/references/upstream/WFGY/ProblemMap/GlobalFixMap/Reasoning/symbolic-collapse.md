# Symbolic Collapse: Guardrails and Fix Pattern

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


When symbols, roles, units, or variables drift in meaning across steps, the chain collapses even if individual sentences look fluent.  
This page localizes symbolic failures and gives a minimal, testable repair plan using ΔS, λ_observe, and E_resonance.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- Cite first and make it auditable  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  → [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md)

- Lock constraints and unlock safely  
  → [pattern_symbolic_constraint_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

- If logic also drifts  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Variable alias collision | `x` means “price” at step 3 and “index” at step 7 |
| Unit flip | km vs miles, USD vs EUR, or 0-1 vs 0-100 score scales without notice |
| Role leak | Tool output fields are reused as different roles in later steps |
| Type drift | A list becomes a dict halfway, downstream steps still “pass” |
| Anchor rename | Entity “A Inc.” becomes “Alpha” with no traceable mapping |
| Quantifier slip | “Some” turns into “all” when summarizing two steps later |
| Schema split | Same object has different required fields across steps |

---

## Why symbolic collapse happens

1) **No symbol table**. Meanings live only in prose and mutate under paraphrase pressure.  
2) **Missing namespace**. Agent or tool outputs write into global scope.  
3) **Unit contract absent**. The pipeline accepts values without unit or scale tags.  
4) **Constraint unlock without fences**. The model invents aliases to escape constraints.  
5) **Header drift flips λ**. Reordered headers produce distinct symbol bindings per run.  
6) **Hybrid retrieval shuffle**. The anchor snippet changes and symbols rebind silently.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance flat at joins and handoffs  
- **Zero symbol drift** across steps when checked against a symbol table

---

## Fix in 60 seconds

1. **Create a symbol table**  
   Add an explicit table with `name`, `kind` (var, role, unit, entity), `namespace`, `definition`, `source_snippet`, `allowed_values`.

2. **Enforce cite-first and schema-locked steps**  
   Require citations before any symbol is used. Enforce unambiguous fields.  
   See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

3. **Clamp variance with BBAM**  
   If λ flips after paraphrase, apply BBAM to hold one binding set stable.

4. **Bridge with BBCR**  
   Produce a short, cited bridge that restates the symbol table and the current state, then continue reasoning on top of that bridge only.

5. **Lock namespaces**  
   Prefix every symbol with a scope `agent.role.symbol` or `tool.name.field`. Reject writes outside the declared namespace.

---

## Minimal symbol table contract

Every plan step must carry the table and refuse execution on mismatch.

```json
{
  "symbols": [
    {
      "name": "x",
      "kind": "var",
      "namespace": "calc.pricing",
      "definition": "unit price per kg",
      "unit": "USD/kg",
      "source_snippet": "S12#CH2.3",
      "allowed_values": "real >= 0"
    },
    {
      "name": "R",
      "kind": "role",
      "namespace": "agent.verifier",
      "definition": "checks unit and citation before approval",
      "allowed_values": ["approve","reject","fix"]
    }
  ],
  "schema_version": "v1"
}
````

Reject the step if any field changes without a cited reason.

---

## Structural repairs

* **Unit and scale discipline**
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **Ordering stability**
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Constraint unlock with fences**
  → [pattern\_symbolic\_constraint\_unlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

* **Long window stability**
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **If meaning vs similarity conflict**
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **If logic also fails**
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

---

## Verification

* Three paraphrases, two seeds. All runs must keep the **same** symbol table.
* ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 in every run.
* No unit or namespace change without a cited justification that points to a specific snippet.
* Report a diff of the symbol table between steps; the diff must be empty or fully justified.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We suspect a symbolic collapse.

Inputs:
- question: "{q}"
- current snippets: [{snippet_id, section_id, source_url}]
- last symbol table (if any)
- last steps with {claim, citations, λ_state, ΔS}

Do:
1) Build a symbol table with {name, kind, namespace, definition, unit, source_snippet, allowed_values}.
2) Cite first, then restate the claim using only table symbols.
3) If λ flips across a paraphrase, apply BBAM. If content diverges, produce a BBCR bridge that freezes the table.
4) Output JSON:
   { "symbols": [...], "steps": [...], "final_answer": "...",
     "ΔS": 0.xx, "λ_state": "convergent", "table_diff": [] }
Refuse the final answer if any step uses a symbol that is not in the table.
```

---

## Common gotchas

* **Alias creep**. The model introduces “alpha” for A without binding it to the table. Reject and force a mapping row.
* **Silent unit conversion**. Numbers change scale between steps. Require `unit` and `scale` fields.
* **Cross-agent overwrite**. Handoffs write to shared names. Use strict namespaces and a write fence.
* **Hybrid retrieval reorder**. Top-k changes on rerun. Lock query and tie breaks, or add a reranker.

---

## When to escalate

* Table stays unstable after BBAM and a bridge
  → audit logic and role discipline: [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) and
  → multi-agent role isolation: [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) and [role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)

* The same wrong claim returns after correction
  → [pattern\_hallucination\_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

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

