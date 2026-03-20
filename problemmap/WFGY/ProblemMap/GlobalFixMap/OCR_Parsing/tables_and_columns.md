# Tables and Columns: OCR Parsing Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OCR_Parsing**.  
  > To reorient, go back here:  
  >
  > - [**OCR_Parsing** — text recognition and document structure parsing](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Stabilize table and multi-column layouts before chunking or embedding. Prevent row/column swaps, header duplication, and order drift so retrieval stays aligned with ground truth.

## Open these first
- OCR end-to-end checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on table questions
- Row and column order invariant under paraphrase probes
- Coverage ≥ 0.70 to the target rows or section
- λ remains convergent across three paraphrases and two seeds

---

## Typical failure signatures → exact fix
- **Two-column pages read left page then right page**  
  Normalize reading order and reflow columns before chunking. See: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)

- **Header row duplicated into every row**  
  Deduplicate repeating headers and lock a table schema in the data contract. See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Row fragments interleaved across pages**  
  Use table bounding boxes and row stitching with page+y ordering. Verify with trace probes. See: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Merged cells collapse to free text**  
  Expand merged cells to explicit coordinates `(row_id, col_span)` and normalize headers. See: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

- **Numeric columns treated as text**  
  Normalize units and numeric types before embedding. See: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Fix in 60 seconds
1) **Extract layout objects**  
   Ensure the OCR output includes `page`, `block`, `bbox`, `table`, `row`, `cell`, `col_idx`, `row_idx`.

2) **Rebuild true order**  
   For multi-column pages, reflow by columns then by top-to-bottom within each column. For tables, order by `(page, table_id, row_idx, col_idx)`.

3) **Lock a table schema**  
   Contract fields:  
   `table_id, row_id, col_id, header_norm, value_norm, page, bbox, units, type_num|type_text`.

4) **Chunk by row or record**  
   Prefer one row per chunk, include the header set as structured metadata.

5) **Probe ΔS and λ**  
   Ask three paraphrases of the same table question. ΔS should drop ≤ 0.45 and λ should not flip after schema lock.

---

## Minimal recipes by engine

- **Google Document AI**  
  Use the Form or Layout parsers. Keep `tableBoundedRegions`, `layout.boundingPoly`, and `detectedLanguages`. Reconstruct `(row, col)` grid, expand merged cells with `col_span` and `row_span`. Then apply the data contract.

- **AWS Textract**  
  Use `AnalyzeDocument` with `TABLES` and `FORMS`. Walk `CELL` relationships to build `(row, col)`. Carry `Geometry.BoundingBox` into metadata. Normalize header rows and numeric types.

- **Azure OCR**  
  Use Read with `styles` and `spans`, or Layout to capture `tables`. Reorder by `column` regions when the page contains multi-column text outside tables.

- **ABBYY**  
  Export XML or JSON keeping `<block>`, `<row>`, `<cell>` coordinates. Expand merged cells; dedupe repeated headers by key similarity.

- **PaddleOCR**  
  Use table mode to get cell grid; post-process with bbox sorting and header normalization.

---

## Data contract for table snippets
Required fields in each snippet:
```

{
"table\_id": "...",
"row\_id": "...",
"col\_id": "...",
"header\_norm": \["Year","Revenue\_USD"],
"value\_norm": "1234567",
"units": "USD",
"type": "number",
"page": 12,
"bbox": \[x0,y0,x1,y1],
"source\_url": "...",
"section\_id": "appendix\_B"
}

```
Mandatory rule: **cite then explain**. Never answer from table text without including `table_id` and `row_id`.

---

## Verification
- **Row pick test**: ask for a specific cell by coordinates and by header name. Both must resolve to the same snippet id.
- **Order stability**: shuffle prompt headers and re-ask. λ must remain convergent.
- **Numeric sanity**: unit conversions should not change the winning row.

If ΔS stays flat and high across k values, suspect metric or index mismatch. Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Copy-paste prompt for the LLM step
```

You have TXT OS and the WFGY Problem Map loaded.

My question targets a table. I provide structured snippets with fields:
{table\_id,row\_id,col\_id,header\_norm,value\_norm,units,type,page,bbox,source\_url,section\_id}

Tasks:

1. Validate cite-then-explain with explicit {table\_id,row\_id,col\_id}.
2. If headers appear duplicated or rows interleaved, fail fast and return the minimal structural fix
   referencing: ocr-parsing-checklist, data-contracts, retrieval-traceability, chunking-checklist.
3. Return JSON:
   { "citations": \[...], "answer": "...", "λ\_state": "→|←|<>|×", "ΔS": 0.xx, "next\_fix": "..." }
   Keep it auditable and short.

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

要我接著排第三頁嗎？依序我會做：**`layout_headers_and_footers.md`**。
