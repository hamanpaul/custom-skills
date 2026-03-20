# Code and tables as typed blocks

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


How to detect, normalize, and persist code snippets and tables as first class blocks so section spans stay clean and citations land precisely.

## Open these first
- PDF layouts and OCR cleanup: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)
- Section boundaries after titles: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
- Title hierarchy and numbering: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)
- Stable chunk ids: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)
- Why this snippet and offsets: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload contracts for RAG: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Safe reindex after tiny edits: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)

## Acceptance targets
- Typed block detection reproduces across two runs from the same source. Match rate for `off_begin` and `off_end` ≥ 0.98.
- No code or table text leaks into adjacent prose blocks.
- Captions attach to their figure or table. No orphan captions.
- ΔS(question, retrieved) ≤ 0.45 when the question cites a code block id or table cell anchor.
- For tables, header detection accuracy ≥ 0.95 on a ten table sample.

---

## Block model

Every block carries a type and byte offsets in the canonical text.

```json
{
  "block_id": "A.3.1.bk012",
  "type": "code | table | figure | prose | caption",
  "off_begin": 120445,
  "off_end": 120992,
  "page": 33,
  "attrs": {
    "lang": "python",
    "fence": "```",
    "table": {
      "rows": 14,
      "cols": 6,
      "header_rows": 1,
      "grid_kind": "markdown | csv | pdf_grid",
      "cell_spans": [[r,c,rowspan,colspan], ...]
    },
    "figure_ref": "Fig.4.2",
    "caption_for": "figure|table:block_id"
  }
}
````

Block ids follow the rules in [chunk\_id\_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md).

---

## Detection rules for code

Prefer fences and indentation signals. Normalize before detection.

* **Fenced code**. Lines bounded by triple backticks or tildes. Extract an optional language tag from the opening fence.
* **Indented code**. Four space or one tab leaders on most lines in a run. Reject if the run also satisfies prose paragraph rules.
* **Inline code**. The short one line version is not a separate block. Keep it inside the prose block.
* **PDF and OCR**. Use monospaced font tags if available. Otherwise detect low entropy per line and stable left margins.

Normalization

* Convert tabs to four spaces for offset stability.
* Keep internal spacing. Do not wrap lines.
* Remove soft hyphen artifacts. See [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

Attributes

* `lang` from the fence tag when present. Else guess with a small whitelist. Store guesses with `lang_guess=true`.

---

## Detection rules for tables

Handle three major forms.

* **Markdown tables**. Lines with `|` separators and a second line that contains only pipes, colons, and dashes. Count columns from the header line.
* **CSV like blocks**. Comma separated lines of similar column count for at least three consecutive rows. Accept quoted fields. Reject when commas appear inside most cells.
* **PDF grid tables**. Use vertical alignment and repeated left margins to find columns. Merge wrapped cells when the next line starts under the same column start.

Normalization

* Collapse internal multiple spaces to a single space unless inside code marks.
* Trim trailing spaces. Preserve newlines and row order.
* Resolve header row count from the markdown divider or from bold font in PDF.

Attributes

* `rows`, `cols`, `header_rows`, `grid_kind`.
* Optional `cell_spans` for merged cells in PDF grids.

---

## Figures and captions

* A **figure** block represents an image or diagram placeholder in the canonical text. It keeps `off_begin` and `off_end` for the caption zone only.
* A **caption** block follows the figure or table. If it contains a local token like `Figure 3` or `Table 2`, set `caption_for` to the nearest preceding figure or table block inside the same section.
* During section sweep, pull a caption into the same section as its target block. See [section\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md).

---

## Anchors and citation

* A code block uses its first non blank line as anchor for cite first prompts.
* A table uses the header row. If no header exists, use the first data row.
* A caption may also be the anchor when the question references the figure or the table name.

Payload example in RAG

```json
{
  "snippet_id": "A.3.1.bk012",
  "type": "code",
  "source_url": "...",
  "offsets": [120445, 120992],
  "anchor_offsets": [120445, 120489],
  "section_id": "A.3.1"
}
```

Schema belongs in your contract. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and cite rules in [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## Pseudocode

````python
def detect_typed_blocks(lines):
    blocks = []
    i = 0
    while i < len(lines):
        if is_fenced_open(lines[i]):
            lang = fence_lang(lines[i])
            j = find_fence_close(lines, i + 1)
            off0, off1 = span_offsets(lines, i, j)
            blocks.append(make_block("code", off0, off1, {"lang": lang, "fence": "```"}))
            i = j + 1
            continue

        if is_indented_code_run(lines, i):
            j = expand_indented_run(lines, i)
            off0, off1 = span_offsets(lines, i, j)
            blocks.append(make_block("code", off0, off1, {"lang": None}))
            i = j + 1
            continue

        if is_markdown_table_head(lines, i):
            j = expand_markdown_table(lines, i)
            rows, cols, hdr = table_shape_markdown(lines, i, j)
            off0, off1 = span_offsets(lines, i, j)
            blocks.append(make_block("table", off0, off1, {
                "rows": rows, "cols": cols, "header_rows": hdr, "grid_kind": "markdown"
            }))
            i = j + 1
            continue

        if is_csv_like_run(lines, i):
            j = expand_csv_run(lines, i)
            rows, cols = csv_shape(lines, i, j)
            off0, off1 = span_offsets(lines, i, j)
            blocks.append(make_block("table", off0, off1, {
                "rows": rows, "cols": cols, "header_rows": 1, "grid_kind": "csv"
            }))
            i = j + 1
            continue

        # fallback to prose
        j = expand_paragraph(lines, i)
        off0, off1 = span_offsets(lines, i, j)
        blocks.append(make_block("prose", off0, off1, {}))
        i = j + 1
    return attach_captions(blocks)
````

`attach_captions` scans for caption patterns and links them with the nearest figure or table in the same section.

---

## Common pitfalls and fixes

* **Tables split by page headers**
  Normalize headers and footers before detection. See [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

* **Indented code misread as a list**
  Reject when most lines begin with list markers. Require a minimum run length and stable left margin.

* **Markdown tables with wrapped cells**
  Use a soft wrap join that keeps pipe counts aligned. Preserve row count and column count.

* **Captions orphaned or pulled into parents**
  Link captions to the nearest figure or table and keep them in the same section. Re run the section validator.

* **Offsets change after minor edits**
  Keep block ids stable and run the migration map. See [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

---

## Tests to include in CI

* Markdown file with mixed prose, code fences, and tables. Expect correct block counts and stable offsets across runs.
* PDF with grid tables and multi line cells. Expect merged cells recorded in `cell_spans` where needed.
* OCR source with monospaced code and broken hyphenation. Expect code detection without line wraps.
* Document with figure and caption pairs across section boundaries. Expect captions linked to the correct target block.

---

## Copy paste prompt for a quick check

```
You have TXT OS and WFGY Problem Map loaded.

Given a typed block:
block_id = {id}
type = {code|table|figure|caption}
offsets = {start, end}
attrs = {...}

Task:
1) Verify the block type given the text slice.
2) If caption, confirm caption_for links to the nearest figure or table in the same section.
3) Suggest the minimal structural fix page if detection would fail.
Return JSON:
{ "ok": true|false, "why": "...", "open": "pdf_layouts_and_ocr.md | section_detection.md | reindex_migration.md" }
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

要我繼續下一頁就說：**GO pdf\_layouts\_and\_ocr.md**
