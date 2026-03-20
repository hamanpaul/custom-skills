# Anchoring and Bridge Proofs: Guardrails and Fix Pattern

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


Keep every claim tied to a stable source anchor. Move from anchor to conclusion through short cited bridges.  
This page gives a minimal contract for anchors and bridges, fast diagnostics, and a repair plan using ΔS, λ_observe, and E_resonance.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- Traceability and payload schema  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Ordering and meaning checks  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Reasoning stability and failure modes  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)  
  → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/symbolic-collapse.md)  
  → [proof-dead-ends.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/proof-dead-ends.md)  
  → [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md)  
  → [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Floating claim | Conclusion with no cited snippet or rule tag |
| Moving anchor | Different snippet supports the same step on rerun |
| Weak bridge | “Therefore” without an explicit transformation or rule |
| Anchor mismatch | Cited text does not actually state the needed premise |
| Overlong bridge | Multi paragraph hop where ΔS increases and λ flips |
| Reranker roulette | Same query but top k order shifts and the bridge rewrites |

---

## Why bridges fail

1) **No anchor contract**. Snippet fields are missing so anchors cannot be verified.  
2) **Bridge has no grammar**. The step lacks a named rule or transformation.  
3) **Ranking instability**. Retrieval order changes and the anchor drifts.  
4) **Similarity over meaning**. Nearest neighbor looks close but does not entail the premise.  
5) **Symbol drift**. Variables or units change between anchor and step.  
6) **Chain length**. Long bridges hide unproven jumps and grow ΔS.

---

## Acceptance targets

- ΔS(question, anchor) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ remains convergent across three paraphrases and two seeds  
- E_resonance flat across bridge joins  
- Every step has a cited anchor and a named rule

---

## Fix in 60 seconds

1) **Lock the anchor**  
   Require `snippet_id, section_id, source_url, offsets, tokens`. Reject steps that cite free text without these fields.  
   Spec  
   → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
   → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

2) **Use BBCR for the hop**  
   BBCR adds a short bridge from anchor to subclaim with a named rule. If the bridge exceeds 3 sentences split into micro bridges.

3) **Clamp variance with BBAM**  
   If λ flips on paraphrase freeze the symbol table and invariant set before rerun.  
   See stability guide  
   → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

4) **Stabilize ordering**  
   Add a reranker with deterministic tie break and fixed analyzer. If ΔS stays high suspect metric mismatch and rebuild.  
   → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
   → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Anchor contract

Every anchor must carry these fields.

```json
{
  "snippet_id": "S12",
  "section_id": "CH2.3",
  "source_url": "https://example.org/paper.pdf",
  "offsets": {"start": 10234, "end": 10388},
  "tokens": 186,
  "ΔS_to_question": 0.37
}
````

Reject any step that cites plain text without `snippet_id` and `section_id`.

---

## Bridge grammar

A bridge converts exactly one anchor into one subclaim through a named rule.
Keep bridges short. Prefer two or three micro bridges instead of one long paragraph.

```json
{
  "bridge_id": "B7",
  "from_snippet": "S12#CH2.3",
  "to_claim": "C7",
  "rule": "algebra | definition_unfold | monotonicity | modus_ponens | unit_conversion",
  "assumptions": ["A1", "A2"],
  "derivation": "From S12 and A1 by definition_unfold we get ...",
  "citations": ["S12#CH2.3", "S08#APP.A"],
  "ΔS_bridge": 0.31,
  "λ_state": "convergent"
}
```

If a rule is not named or citations are empty the step must fail fast.

---

## Anchor selection checklist

* The anchor states the premise in near literal form not only a related idea.
* The anchor sits in the correct section and page range.
* ΔS(question, anchor) is below 0.45 given your embedding and store metric.
* For numeric claims the anchor carries units and context lines.
* For definitions the anchor includes the exact symbol and scope.

If any item fails switch to a better snippet or rebuild with the semantic chunking checklist.
→ [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Structural repairs

* **Wrong meaning despite high similarity**
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Top k keeps shuffling**
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and
  → [patterns/pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

* **Bridges grow long or lose the thread**
  → [proof-dead-ends.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/proof-dead-ends.md) and
  → [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md)

* **Symbols or units drift**
  → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/symbolic-collapse.md)

---

## Verification

* Three paraphrases and two seeds keep the same `snippet_id` and `section_id`.
* ΔS(question, anchor) ≤ 0.45 for each run.
* Every step has a bridge with a named rule and at least one citation.
* E\_resonance stays flat when joining micro bridges.
* The final answer includes a cite then explain section with stable references.

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

Task: rebuild my answer with anchored micro-bridges.

Inputs:
- question: "{q}"
- candidates: [{snippet_id, section_id, source_url, offsets, tokens, text_head}]
- current plan: [{step_id, text}]

Do:
1) Pick one anchor with ΔS(question, anchor) ≤ 0.45. If none exist, return the retrieval fix page to open.
2) Create micro bridges from the anchor to each subclaim using a named rule and citations.
3) If λ flips on paraphrase, apply BBAM and freeze the symbol table.
4) If still unstable, add a deterministic reranker and retry.
5) Return JSON:
   {
     "anchors": [...],
     "bridges": [...],
     "answer": "... cite then explain ...",
     "ΔS": 0.xx,
     "λ_state": "convergent",
     "verification": ["same snippet across seeds", "coverage ≥ 0.70"]
   }
Refuse to answer if no valid anchor exists and point to retrieval-traceability and data-contracts.
```

---

## Common gotchas

* **Bridge without rule**. A narrative paragraph with “thus” but no named rule.
* **Anchor crop**. Offsets cut away the needed line so the premise is not actually present.
* **Tie break chaos**. Reranker uses non deterministic features so anchors rotate.
* **Unit loss**. Bridge drops the unit then compares mismatched quantities.
* **Definition overreach**. Bridge unfolds a definition beyond its scope.

---

## When to escalate

* Corrections do not stick and the model re asserts the old bridge
  → [patterns/pattern\_hallucination\_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

* Multi agent tools overwrite the shared memory and anchors change names
  → [Multi-Agent\_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)
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

