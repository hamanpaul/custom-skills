# Goldset Curation — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval**.  
  > To reorient, go back here:  
  >
  > - [**Eval** — model evaluation and benchmarking](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A curated gold set is the foundation for evaluation stability. Without strict contracts on the gold data, all eval metrics become meaningless. This page defines how to build, audit, and maintain gold QA sets that align with WFGY acceptance targets.

---

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Payload fences: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Chunk coverage: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Semantic drift control: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## Acceptance targets for curated goldsets

* **Coverage ≥ 0.80** of target sections
* **ΔS(question, gold anchor) ≤ 0.35**
* **λ state stable** across 3 paraphrases and 2 seeds
* **No overlap**: each gold item maps to exactly one snippet and section

---

## Curation process

### 1. Select domains

* Identify domains relevant to the pipeline (finance, law, product docs).
* Ensure gold questions are drawn from actual user tasks.

### 2. Define anchors

* Each QA item must cite a **section ID** and **expected\_doc**.
* Anchors must reference stable problem map sections, not ephemeral text.

Example:

```json
{
  "id": "Q_0007",
  "question": "What causes hallucination re-entry after correction?",
  "answer_ref": "PM:patterns/pattern_hallucination_reentry",
  "expected_doc": "ProblemMap/patterns/pattern_hallucination_reentry.md",
  "section_id": "hallucination-reentry"
}
```

### 3. Add paraphrases

* Minimum 3 per question.
* Probe λ stability under phrasing variance.

```json
{
  "id": "Q_0007_P1",
  "question": "Why do hallucinations return after being corrected once?"
}
```

### 4. Validate citations

* Each gold item must include an **exact citation offset**.
* If offsets drift, the goldset is invalid until refreshed.

### 5. Apply regression gate

* No gold item should produce ΔS > 0.45 in baseline runs.
* Violations are logged and flagged for refresh.

---

## Common pitfalls and fixes

* **Gold overlaps across sections**
  → Fix: merge or re-scope questions, ensure one-to-one mapping.

* **Anchors point to unstable docs**
  → Fix: only link to long-lived WFGY ProblemMap pages.

* **Paraphrases flip λ**
  → Fix: clamp with BBAM variance controls and revalidate.

* **Coverage below 0.80**
  → Fix: expand questions until goldset covers every critical node.

---

## Quick workflow

1. Draft 20–30 candidate QA items.
2. Add 3 paraphrases each.
3. Link every item to an anchor section.
4. Run through `eval_harness.md`.
5. Drop items that fail regression gate.
6. Store final goldset in `datasets/gold/`.

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

