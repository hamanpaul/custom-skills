<!--
Search Anchor:
chunking global fix map
rag chunking bugs
document chunking failures
chunk boundaries wrong
snippets cut mid thought
anchors missing sections skipped
chunk id schema stable ids
duplicate chunks across runs
chunk drift after reindex
chunking checklist preflight
code table block structure lost
markdown code tables blocks
section detection heading anchors
title hierarchy h1 h2 h3 outline
pdf layouts ocr chunking
two column pdf broken reading order
math formulas split across chunks
tables split or merged incorrectly
reindex migration chunk id mismatch
index rebuilt but old refs broken
eval rag precision recall for chunking
cannot prove better chunking
live monitoring rag chunk health
sudden drift after deploy
context flips with same corpus

metrics and contracts:
delta s question retrieved <= 0.45
coverage target section >= 0.70
lambda observe convergent 3 paraphrases 2 seeds
traceability contract snippet_id section_id source_url offsets tokens
snippet contract cite then explain
chunk boundaries align semantic windows
chunk size tokens window length overlap
hash based chunk id
versioned chunk schema

formats and pipelines:
pdf ocr html markdown word docs
code files notebooks tables logs
monolithic vs semantic chunks
sliding window chunking
title based segmentation
section anchors toc
header detection underlines numbering
hybrid retrievers fail due to chunking
vector db looks fine but chunks bad
store independent chunking guardrails

common incidents:
important section never retrieved
only meaningless sub section retrieved
citations collapse after parsing
reindex changes chunk ids breaks bookmarks
deployment changes chunking strategy
roll back but index not aligned
monitoring catches sudden chunk collapse
-->

<!--
Primary pages in this folder:
ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md
ProblemMap/GlobalFixMap/Chunking/chunking-checklist.md
ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md
ProblemMap/GlobalFixMap/Chunking/section_detection.md
ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md
ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md
ProblemMap/GlobalFixMap/Chunking/reindex_migration.md
ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md
ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md
-->

<!--
Related routing pages:
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/embedding-vs-semantic.md
ProblemMap/patterns/pattern_vectorstore_fragmentation.md
ProblemMap/chunking-checklist.md
ProblemMap/retrieval-playbook.md
ProblemMap/context-drift.md
ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md

Cross folder jumps:
Retrieval Global Fix Map README
Embeddings Global Fix Map README
VectorDBs_and_Stores Global Fix Map README
-->



# Chunking — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

A compact hub to **stabilize document chunking** across formats, pipelines, and retrieval systems.  
This folder routes chunk-related bugs to structural fixes and provides checklists, schema, and live recipes.  
No infra change required.

---

## Orientation: what each page does

| Page | What it solves | Typical symptom |
|---|---|---|
| [Chunk ID Schema](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md) | Unique ID + schema for each chunk | Duplicate or drifting chunks across runs |
| [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking-checklist.md) | Minimal audit list for validity | Chunks too long, too short, or incomplete |
| [Code / Tables / Blocks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md) | Preserve structure for code, tables, blocks | Retrieval drops formatting or logic |
| [Section Detection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md) | Detect paragraph and section anchors | Anchors missing, snippets cut mid-thought |
| [Title Hierarchy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md) | Maintain document heading hierarchy | Only partial or meaningless sub-sections retrieved |
| [PDF Layouts & OCR](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md) | Repair PDF/OCR-specific chunking | Citations collapse after parsing |
| [Reindex & Migration](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md) | Safe chunk migration during reindex | Index rebuilt but old refs mismatch |
| [Eval RAG Precision & Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md) | Deterministic evaluation recipes | “Better” chunking cannot be proven |
| [Live Monitoring (RAG)](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md) | Online health checks for chunking | Sudden drift or collapse after deploy |

---

## When to use this folder

- Your chunks look fine by eye but retrieval skips important sections.  
- PDF / OCR parsing collapses headers, math, or tables.  
- Hybrid retrievers underperform due to inconsistent chunk boundaries.  
- Reindexing breaks old citations.  
- Context flips between runs with same corpus.

---

## Acceptance targets

- Chunk boundaries align with semantic windows  
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- Traceability contract fields always present: `{snippet_id, section_id, source_url, offsets, tokens}`

---

## 60-second fix checklist

1) **Check chunk IDs**  
   Apply `chunk_id_schema`. Ensure unique + stable across reindex.

2) **Audit with checklist**  
   Run the [chunking-checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking-checklist.md) before ingest.

3) **Preserve structure**  
   Use [code_tables_blocks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md) for code, tables, blocks.

4) **Validate anchors**  
   Confirm section and title detection. Apply [title_hierarchy](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md).

5) **Reindex safely**  
   Use [reindex_migration](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md) with hash/version lock.

6) **Monitor live**  
   Apply [live_monitoring_rag](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md) to catch collapse early.

---

## Minimal probe pack

```txt
Context: I loaded TXT OS and the WFGY pages.

Task:
- Given doc corpus D, log ΔS(question, retrieved) and λ across 3 paraphrases.
- Validate chunk IDs and section anchors.
- If ΔS ≥ 0.60 or λ flips, propose the smallest structural change:
  chunk schema, checklist, or reindex.
- Verify coverage ≥ 0.70 after fix.

Return JSON:
{ "citations": [...], "ΔS": 0.xx, "λ_state": "<>", "coverage": 0.xx, "next_fix": "..." }
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

