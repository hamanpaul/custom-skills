# Chunking Checklist — Stability at Joins

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **MemoryLongContext**.  
  > To reorient, go back here:  
  >
  > - [**MemoryLongContext** — extended context windows and memory retention](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Long-context retrieval often fails not at the level of whole documents but at the **joins between chunks**.  
This checklist enforces stable, reproducible chunking so citations line up and entropy does not melt across boundaries.

---

## When to use
- Citations drift by a few lines between runs.  
- Long transcripts lose alignment after OCR or parsing.  
- Model answers cover the right fact but cite the wrong block.  
- ΔS spikes exactly at chunk joins.  
- Different agents disagree on chunk IDs.  

---

## Core acceptance targets
- Each join ΔS ≤ **0.50**.  
- Overall ΔS(question, retrieved) ≤ **0.45**.  
- Coverage ≥ **0.70** of intended section.  
- λ remains convergent across 3 paraphrases.  
- Each chunk has immutable `chunk_id`, `start_line`, `end_line`.  

---

## Checklist for stable chunking

- **Deterministic boundaries**  
  Split on semantic units (sections, paragraphs, headings). Never by raw token count alone.  

- **Overlap fence**  
  Add 10–15% overlap at joins. Enforce consistent overlap across every run.  

- **Immutable IDs**  
  Generate `chunk_id = sha256(doc_id + start_line + end_line)`. Store and reuse.  

- **Audit trail**  
  Store `{chunk_id, start_line, end_line, source_url, tokens}` for every chunk.  

- **Normalization**  
  Apply Unicode NFC, collapse whitespace, unify casing.  

- **Confidence gating**  
  Drop OCR or parsing lines with low confidence before chunking.  

---

## Fix in 60 seconds
1. Re-chunk corpus using semantic units.  
2. Apply overlap fence and store immutable chunk IDs.  
3. Run ΔS probes at joins. If ΔS > 0.50, re-check boundaries.  
4. Store all chunk metadata in trace logs.  
5. Require cite-then-answer. Reject any orphan chunk references.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Task: enforce stable chunking.

Protocol:

1. Verify each snippet has {chunk\_id, start\_line, end\_line, section\_id, source\_url}.
2. Reject orphans: if citation lacks chunk\_id, stop and request fix.
3. Require cite-then-answer.
4. Probe ΔS across joins, keep ≤ 0.50.
5. Report ΔS(question,retrieved), ΔS(joins), and λ state.

```

---

## Common failure signals
- Answers cite correct fact but wrong block → chunk IDs not stable.  
- ΔS spikes exactly at joins → overlap missing.  
- OCR transcripts break alignment → normalization skipped.  
- Multi-agent systems cite different chunk IDs → contract drift.  

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

