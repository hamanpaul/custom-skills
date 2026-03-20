# Layout, Headers, and Footers: OCR Parsing Guardrails

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


Strip or normalize page furniture before chunking or embedding. Stop headers, footers, page numbers, and watermarks from polluting semantic meaning and wrecking retrieval.

## Open these first
- OCR end to end checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 after layout cleanup
- Coverage ≥ 0.70 for the target section
- λ stays convergent across three paraphrases and two seeds
- Zero header/footer strings inside content tokens of any chunk

---

## Typical failure signatures → exact fix
- **Running headers become part of every chunk**  
  Detect repeating lines at top bands per page. Move them to `page_furniture.header` metadata or drop by rule. See: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)

- **Footers and page numbers leak into answers**  
  Identify bottom band strings and numeric patterns. Attach to metadata `page_furniture.footer` and `page_furniture.page_num`, not the content body. See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Watermarks mix with paragraphs**  
  Use low opacity or diagonal angle cues plus oversized bbox to flag watermark blocks. Remove from body, keep `watermark_text` only in metadata. See: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

- **Section title duplicated on every page**  
  Treat it as header when identical across ≥ 2 consecutive pages. Promote a single canonical section anchor. See: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Footnotes interleaved with paragraph flow**  
  Extract footnote blocks. Keep `footnote_id`, `anchor_offset`, and a separate citation lane. Never mix into paragraph tokens. See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Fix in 60 seconds
1) **Detect bands**  
   For each page, split objects by vertical bands: `top ≤ 12%`, `bottom ≥ 88%`. Flag candidates for headers and footers.

2) **Find repeats**  
   Normalize text (case, whitespace, punctuation), then mark strings that repeat across pages. Anything stable goes to furniture.

3) **Rewrite content**  
   Remove furniture from body tokens. Store originals under `page_furniture`.

4) **Rechunk**  
   Chunk paragraphs without furniture. Carry `section_id`, `page`, and cleaned offsets.

5) **Probe**  
   Re-run three paraphrases. ΔS drops and λ stops flipping if furniture is out of the body.

---

## Minimal recipes by engine

- **Google Document AI**  
  Use `layout.boundingPoly` for band checks. Identify `paragraph` blocks within top/bottom polygons and mark as furniture. Keep `detectedLanguages`. Apply after-parse dedupe across pages.

- **AWS Textract**  
  From `Blocks` with `BlockType=LINE` or `WORD`, inspect `Geometry.BoundingBox.Top/Height`. Route repeated top-band lines to `page_furniture.header`, bottom band to `footer`. Keep `PAGE` relationships for page numbers.

- **Azure OCR**  
  Use `lines` with `boundingRegions`. Sort by `polygon` y positions, isolate bands, then repeat-check across pages. Store page number patterns `^\s*[ivxlcdm]+$|^\s*\d+\s*$` as `page_num`.

- **ABBYY**  
  Export XML, read `<block>` with coordinates. Apply band and repeat filters. Preserve watermarks as `watermark_text` if block has style or angle attributes.

- **PaddleOCR**  
  Use bbox outputs to filter by top/bottom thresholds. De-dup by normalized text across pages. Keep furniture in metadata only.

---

## Data contract additions for layout cleanup
Add these fields to your snippet schema:

```

{
"page": 7,
"section\_id": "2.3",
"bbox": \[x0,y0,x1,y1],
"text\_clean": "...",             // body without furniture
"text\_raw": "...",               // optional, original page text
"page\_furniture": {
"header": "Company Annual Report 2024",
"footer": "Confidential",
"page\_num": "xv",
"watermark\_text": "DRAFT"
},
"footnotes": \[
{"id":"fn12","text":"...","anchor\_offset":325}
],
"source\_url": "..."
}

```

Mandatory rule: model must read `text_clean` for reasoning. `page_furniture` is trace-only.

---

## Verification
- **Furniture leak test**: sample 20 chunks, assert no header/footer strings inside `text_clean`.
- **ΔS drop**: compare ΔS before and after cleaning on the same question. Target ≤ 0.45.
- **λ stability**: shuffle prompt headers, confirm λ stays convergent.
- **Footnote audit**: a question about a footnote must cite `footnotes[*].id`, not guess from body text.

If ΔS remains flat and high, reopen chunking and metric checks. See: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Copy-paste prompt for the LLM step
```

You have TXT OS and the WFGY Problem Map.

For each snippet I provide:

* use text\_clean for reasoning,
* treat page\_furniture as trace only,
* cite then explain.

Tasks:

1. If header/footer strings appear inside text\_clean, fail fast and return the minimal structural fix referencing:
   ocr-parsing-checklist, data-contracts, retrieval-traceability, chunking-checklist.
2. Return JSON:
   { "citations":\[...], "answer":"...", "λ\_state":"→|←|<>|×", "ΔS":0.xx, "next\_fix":"..." }
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

