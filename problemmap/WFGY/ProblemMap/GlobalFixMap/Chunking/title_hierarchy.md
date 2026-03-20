# Title Hierarchy: robust heading tree for chunking and citations

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


A field guide to build a stable section tree from PDFs, HTML, and mixed sources. The output drives `section_id` paths like `1.2.3`, anchors for cite-then-explain, and deterministic `chunk_id` assembly.

## Open these first
- Why-this-snippet and trace schema: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload and citation locks: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Chunk identifiers and redirects: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)
- Next stage after headings: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
- Layout and OCR normalizing: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)
- Reindex and id migration: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)

## Acceptance targets
- Reproducible section tree on two runs of the same source: identical `section_id` paths for ≥ 0.98 of headings.
- Coverage ≥ 0.95 of human visible headings, with at most 1 spurious heading per 20 pages.
- ΔS(question, retrieved) ≤ 0.45 on cite-first prompts that target a section anchor.
- No depth jumps. The path never skips a level. For example `1 → 1.1 → 1.1.1` is valid, `1 → 1.0.1` is not.

---

## Pipeline overview

1) **Normalize text and blocks**  
   Build a canonical text layer and a block sequence. Repair OCR line breaks, remove running headers and footers. See [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

2) **Collect heading candidates**  
   - HTML: tags `h1..h6` plus role attributes and ARIA landmarks.  
   - PDF: typography cues from font size quantiles, boldness, line spacing, indentation deltas.  
   - Regex cues for numbering and prefixes: `^\d+(\.\d+){0,5}[.)]?`, `^[A-Z][.)]`, `^Appendix [A-Z]\b`, `^Chapter \d+\b`.

3) **Score and classify**  
   For each candidate, compute a heading score from four families: typography, numbering pattern, lexical shape, and context breaks. Keep candidates whose score passes a tuned threshold. Reject lines that end in periods or contain dense punctuation.

4) **Assign levels**  
   Prefer explicit dot numbering when present. Else infer level by relative size bin and indentation quantiles. Clamp level movements to step size one. If the previous level is `L`, a new heading can be `L`, `L+1`, or any ancestor close, chosen by context windows.

5) **Emit section nodes**  
   Create nodes with `section_id`, `title`, `slug`, `page_start`, and lazy `page_end` filled when the next sibling begins. Snap the first body block after a heading as the anchor sentence.

6) **Validate the outline**  
   Run monotonicity checks, parent presence, and unique path constraints. If a violation appears, repair locally by demoting or promoting a small set of nodes.

---

## Section node schema

```json
{
  "section_id": "2.4.1",
  "title": "Evaluation protocol and metrics",
  "slug": "evaluation-protocol-and-metrics",
  "depth": 3,
  "page_start": 12,
  "page_end": 15,
  "offsets": [23871, 44122],
  "title_hash": "sha1:2c7d9c…",
  "children": []
}
````

* `slug` is a lowercase kebab form of the title for readable anchors.
* `offsets` bracket the full section span in the canonical text.

---

## Heuristics that make it stable

* **Dot patterns beat typography**
  If both exist, use numbering like `3.1.2` to set depth and use typography only as a tie breaker.

* **Uppercase ratio and token count**
  Flags like `UPPERCASE_RATIO ≥ 0.60` and `token_count ≤ 80` help catch style headings. Titles rarely end with a period or colon unless they are figure titles.

* **Indent and size bins**
  Build quantiles for font size per document. Use a two dimension decision: `bin(size)` and `delta_indent`. Map to depth using a learned or rule table.

* **Appendix and roman numerals**
  Accept `Appendix A`, `Appendix B.2`, and roman sequences `I, II, III`. Normalize to a numeric level while keeping the original string in `title`.

* **Table and code shields**
  Do not mistake figure captions, table titles, or code comments for headings. Reserve them as block types. See [code\_tables\_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

---

## Copy-paste outline builder (pseudocode)

```python
def build_title_hierarchy(blocks):
    stack = []  # list of nodes by depth
    nodes = []
    for blk in blocks:
        if not is_heading_candidate(blk):
            continue
        depth = estimate_depth(blk)  # number or inferred
        title = normalize_title(blk.text)
        node = make_node(depth, title, blk.page, blk.offsets)
        # attach into tree
        while len(stack) >= depth:
            stack.pop()
        if stack:
            parent = stack[-1]
            parent.children.append(node)
        else:
            nodes.append(node)
        stack.append(node)
    # fill page_end by looking at next sibling or end of doc
    nodes = fill_section_ranges(nodes, blocks)
    return nodes
```

`estimate_depth` prefers dot numbering. If absent, infer by size and indent bins. Clamp jumps larger than one level.

---

## 60-second validator

Sample ten headings uniformly across the document.

* Each has a unique `section_id` path with depth ≤ 6.
* Reading order of titles equals lexicographic order of `section_id`.
* The first sentence under each title exists and becomes an anchor.
* On re-run from the same source, all ten `section_id` paths match exactly.

---

## Edge cases and repairs

* **Repeated titles in different parts**
  If the same string repeats, disambiguate by parent path. The `section_id` remains unique.

* **Multi column PDFs**
  Break candidates by columns before heading scoring. Merged lines inflate score falsely.

* **Heading wrapped across pages**
  Merge lines within a vertical window. If a heading breaks across pages, keep `page_start` at the first page.

* **Front matter and ToC**
  Exclude lines inside the table of contents and reference lists. Use anchors like “Contents” and page number columns to skip.

* **Aggressive demotion**
  When two consecutive headings both look like `H2` by size, allow demoting the second to `H3` if a dot pattern suggests child relation.

---

## Tests to include in CI

* PDF set with known outlines: expect exact `section_id` paths.
* HTML set with mixed tag and style headings: expect depth tolerances within one level.
* OCR set with noisy fonts: expect no more than one false heading per ten pages.
* Migration test: small edits do not change parent paths for unaffected sections. See [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

---

## When it fails and what to open

* Headings look right but citations land off target
  → Verify block boundaries and anchor selection. Open: [section\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

* Many paths change after minor text edits
  → Check size binning and clamp rules. Open: [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

* Numbered sections rank incorrectly in search
  → Lock the anchor and rerank deterministically. Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

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

