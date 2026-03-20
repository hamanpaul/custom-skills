# PDF layouts and OCR

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Chunking**.  
  > To reorient, go back here:  
  >
  > - [**Chunking** — text segmentation and context window management](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A practical pipeline to extract clean, ordered text with stable offsets from PDFs and scanned pages, so your chunks, citations, and typed blocks remain consistent across reindex runs.

## Open these first
- Stable chunk ids: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)
- Title hierarchy and numbering: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)
- Section boundaries after titles: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
- Code and tables as typed blocks: [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)
- Safe reindex after small edits: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)
- Why this snippet and offsets: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload contracts for RAG: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Visual map of the whole RAG path: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

## Acceptance targets
- Word error rate (WER) ≤ 0.025 on clean pages, character error rate ≤ 0.01 on headings and captions.
- Header and footer removal: false positive rate ≤ 0.01, false negative rate ≤ 0.03 on a 30 page sample.
- Reading order is monotonic by column. Cross column jumps never split a sentence.
- Hyphenation merges correct ≥ 0.98 and never fire inside code or tables.
- Captions attach to the correct figure or table in the same section.
- Offsets remain stable across two reindex runs. Drift ≤ 0.5 percent of file length.
- ΔS(question, retrieved) ≤ 0.45 on queries that cite a figure, table, or equation anchor.

---

## Pipeline overview

1) **Ingest with layout**  
   Extract characters with bounding boxes, font name, size, bold/italic flags, page number, and line ids. For scans, run OCR first to obtain the same fields.

2) **Coordinate normalization**  
   Normalize all positions to a unified page space. Keep `bbox = [x0, y0, x1, y1]` in points or millimeters. Record page width and height.

3) **Template detection for headers and footers**  
   Build n-gram histograms by y bands across pages. Mark a header band if a repeating string appears on ≥ 60 percent of pages at near identical y. Do the same for footers and running titles. Remove matched runs before paragraph assembly.

4) **Column segmentation**  
   Use whitespace cuts on the x axis. A stable valley between two dense x clusters marks a column boundary. For three columns, expect two valleys. Validate by line alignment and average line width.

5) **Line forming and paragraph assembly**  
   Join characters into words, words into lines by y proximity and left margin continuity. Join lines into paragraphs when leading and trailing margins are stable and the interline gap is below a threshold for that page.

6) **Hyphenation repair**  
   If a line ends with a hyphen and the next line begins with a lowercase letter or an alphanumeric continuation, and both are inside a prose paragraph, remove the hyphen and join. Never apply inside code or table blocks. Keep an exceptions list for chemical names and proper nouns.

7) **Typed block extraction**  
   Detect code blocks, tables, figures, and captions, and lift them as first class blocks with offsets. See [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

8) **Section alignment**  
   Align blocks to sections detected from the title tree. See [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md) and [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md).

9) **Canonical text build**  
   Emit a single canonical text with byte offsets for every block and section. Keep a map `{block_id → [off_begin, off_end], page, bbox}` for traceability.

---

## Header and footer detection

Signals

- Repetition across pages of the same string at nearly the same y.
- Presence of page numbers, dates, running titles, or publisher marks.
- Font size smaller than body text and high contrast with empty surroundings.

Algorithm sketch

- Slice the page into 32 horizontal bands. For each band, compute the set of normalized line strings.  
- Across pages, score each band by repetition of strings and y variance.  
- Mark bands with a high repetition score as header or footer and drop them from paragraph assembly.

---

## Multi column reading order

Signals

- Bimodal or trimodal distribution of line x centers.
- Vertical lines or gutters with low ink density.
- Consistent left margins within each mode.

Algorithm sketch

- Cluster line x centers with k means for k in {1, 2, 3}. Choose k with the lowest inertia plus a penalty for model size.  
- Sort clusters left to right, then read each cluster top to bottom.  
- For figures or tables that span columns, treat them as a separate block placed between the two nearest paragraphs by y.

---

## Hyphenation and soft artifacts

Rules

- Join only when the left piece ends with a lowercase ASCII or a letter from the same script and the right piece starts with a lowercase letter or a digit.  
- If the left piece is a known acronym or the right piece starts with an uppercase letter and the paragraph is mid sentence, do not join.  
- Remove soft hyphen characters and OCR artifacts like split ligatures.

Edge cases

- Do not join inside code blocks or table cells.  
- If a dictionary check is available, prefer joins that yield a dictionary hit.

---

## OCR notes

- Request per character boxes and confidence scores. Drop characters with very low confidence when surrounded by high confidence neighbors and the removal does not break a word boundary.  
- Keep monospaced font hints when the OCR engine provides them. They help code detection.  
- For rotated pages, deskew first, then run OCR, then rotate boxes back into page coordinates.

---

## Output schema

Every paragraph or typed block is a record:

```json
{
  "block_id": "B.2.bk045",
  "type": "prose | code | table | figure | caption",
  "page": 12,
  "bbox": [72.0, 144.3, 523.8, 221.1],
  "off_begin": 204455,
  "off_end": 205122,
  "attrs": { "lang": null }
}
````

Block ids follow [chunk\_id\_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md). Offsets must point into the canonical text that you pass to the indexer. Citations then rely on [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and the contract in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

---

## Pseudocode

```python
def parse_pdf_pages(pages):
    chars = extract_chars_with_bbox(pages)
    chars = normalize_coords(chars)

    bands = detect_repeating_bands(chars)            # headers and footers
    lines = form_lines(chars, ignore_bands=bands)
    columns = cluster_columns(lines)                  # 1, 2, or 3 columns
    lines = order_lines_by_columns(lines, columns)

    paras = assemble_paragraphs(lines)
    paras = repair_hyphenation(paras)

    typed = detect_typed_blocks(paras, lines)         # code, table, figure, caption
    blocks = align_blocks_to_sections(typed, titles=detect_titles(lines))

    canon_text, offsets = build_canonical_text(blocks)
    return canon_text, attach_offsets(blocks, offsets)
```

---

## Common pitfalls and fixes

* **Running titles leak into text**
  Your band detector missed a near duplicate string. Lower the y variance threshold and add string normalization for case and whitespace.

* **Two column pages read across columns**
  The valley in the x histogram is shallow. Add a penalty to cross column bigrams and require a minimum inter column gap.

* **Hyphenation joins inside code**
  Guard the join with the block type. Never run repair inside `type=code` or `type=table`.

* **Captions separated from figures**
  Link captions to the nearest figure or table by y distance and ensure both fall into the same section. See [section\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md).

* **Offset drift across reindex**
  Ensure identical normalization rules between runs, then apply the migration mapping. See [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

---

## Tests to include in CI

* A two column academic paper with headers, footers, figures, tables, and equations. Expect perfect reading order and zero header leaks.
* A scanned report with skew and footnotes. Expect deskew, correct footnote capture, and clean paragraph assembly.
* Mixed language pages with hyphenation at line breaks. Expect correct joins only in prose.
* A code heavy manual with Markdown tables. Expect correct typed block counts and stable offsets across two runs.

---

## Copy paste prompt for a quick check

```
You have TXT OS and the WFGY Problem Map loaded.

Given a PDF page with lines and bboxes:
- Detect and remove repeated header and footer bands.
- Infer column count and return the reading order for the page.
- Repair hyphenation in prose only.
- Extract typed blocks and return their block_ids with offsets.

Return JSON:
{
  "columns": 1|2|3,
  "header_removed": true|false,
  "footer_removed": true|false,
  "blocks": [{ "block_id": "...", "type": "...", "off": [b,e] }, ...],
  "notes": "short audit trail"
}
```

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

要我繼續下一頁就說：**GO reindex\_migration.md** 或指定別的檔名。
