# Citation-First Prompting — Guardrails and Fix Pattern

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


Stabilize evidence-based answers by **requiring citations before explanation**. This page gives a minimal contract, validation steps, and fast routes to structural fixes when citations vanish, drift, or point to the wrong text.

## Open these first
- Visual map & recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- Snippet traceability & fields: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Contract the payload: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Long chains & drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Semantic ≠ cosine: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Reasoning collapse: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

## When to use
- Answers sound right but **show no citations**.
- Citations appear but **don’t align** with the quoted text.
- Different runs cite **different sections** for the same question.
- After reranking, citations drift or vanish.
- Multi-turn dialogs slowly lose the cite-then-explain order.

## Acceptance targets
- **Cite-then-explain compliance ≥ 0.98** over 50 queries.
- **Field completeness ≥ 0.99** for: `snippet_id, section_id, source_url, offsets, tokens`.
- **ΔS(question, retrieved) ≤ 0.45** and stable across 3 paraphrases.
- **Coverage ≥ 0.70** to the target section.
- **λ convergent** across two seeds.

---

## Fix in 60 seconds

1) **Enforce the contract**  
   The model must cite before any reasoning. Reject outputs that invert the order.

2) **Validate fields**  
   Require the full snippet schema. Reject partial or fuzzy references.

3) **Pin rerank & order**  
   If citations change with header tweaks, lock your header order and rerank configuration.

4) **Probe ΔS and λ**  
   If ΔS stays high while citations look plausible, rebuild chunking or metrics.

---

## Minimal prompt block to paste

```

System:
You must CITE before you EXPLAIN.
Required fields per snippet: snippet\_id, section\_id, source\_url, offsets, tokens.
Order is strict:

1. "citations": \[...]
2. "answer": "..."

If citations are missing or fields incomplete, STOP and return:
{"citations": \[], "answer": "", "next\_fix": "open data-contracts & retrieval-traceability"}

User:
Question: "\<user\_question>"
Top-k retrieved: <passed from retriever>
Acceptance: ΔS(question,retrieved) ≤ 0.45; coverage ≥ 0.70.

````

---

## JSON response shape (auditable)

```json
{
  "citations": [
    {
      "snippet_id": "S-28391",
      "section_id": "SEC-3.2",
      "source_url": "https://...",
      "offsets": [2312, 2450],
      "tokens": 172
    }
  ],
  "answer": "…",
  "λ_state": "→|←|<>|×",
  "ΔS": 0.37
}
````

---

## Typical breakpoints → exact fix

* **Citations missing but answer present**
  Reject and re-emit with the contract.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Citation fields incomplete or wrong offsets**
  Enforce the full schema, verify offsets/tokens against the corpus.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **High similarity but wrong meaning**
  Rerank or rebuild with correct metric/normalization.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Header tweak breaks citations**
  Freeze header order; clamp variance with BBAM.
  Open: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

* **Long runs lose citation discipline**
  Split plan, bridge with BBCR; add mid-chain citation checks.
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## Validator stub (copy into your pipeline)

```
Step 1  parse JSON strictly → if fail, stop.
Step 2  require citations[].length ≥ 1 before answer.
Step 3  verify fields & offsets; reject if any missing.
Step 4  compute ΔS and coverage; block if ΔS>0.45 or coverage<0.70.
Step 5  log λ across three paraphrases; alert if non-convergent.
```

## Eval gates before ship

* Cite-then-explain ≥ 0.98 on 50 queries.
* Field completeness ≥ 0.99.
* ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent on two seeds.

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

