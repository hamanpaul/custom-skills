# Images and Figures: OCR Parsing Guardrails

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


Stabilize text extraction around inline images, charts, and figures. Prevent figure captions or axis labels from bleeding into body text, and preserve semantic anchors for later retrieval.

## Open these first
- OCR end to end checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Retrieval traceability: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on captioned answers
- Coverage ≥ 0.70 for questions tied to figure anchors
- λ remains convergent across three paraphrases
- Captions and labels stored separately from body text

---

## Typical failure signatures → fix
- **Figure captions merged with paragraphs**  
  Split by bbox banding and assign `figure_caption`. Keep paragraph tokens clean.

- **Axis labels or legend entries treated as running text**  
  Extract into `figure_metadata.axis_labels` and `figure_metadata.legend`. Never merge into narrative.

- **Scanned figure with embedded text**  
  Route figure OCR separately. Keep `figure_id`, `text_extracted`, and bounding box. Tie back to figure image reference.

- **Multi-column figure bleed**  
  If caption spans columns, capture as caption block, not as content. Anchor to `figure_id`.

- **Images with no OCR text**  
  Provide stub with `figure_id`, `bbox`, and `alt_text` if known. Maintain traceability.

---

## Fix in 60 seconds
1) **Detect figure zones**  
   Identify bounding boxes flagged as images or graphics. Assign `figure_id`.

2) **Isolate captions**  
   If text appears immediately above/below the figure and repeats formatting (italic, smaller font), tag as caption.

3) **Route labels**  
   Apply heuristic rules for x-axis, y-axis, legend. Store under `figure_metadata`.

4) **Clean narrative**  
   Remove all figure-related text from `text_clean`. Retain only in figure structures.

5) **Probe retrieval**  
   Ask a figure-specific question. If ΔS ≤ 0.45 and λ stable, cleanup succeeded.

---

## Minimal recipes by engine

- **Google Document AI**  
  Use `layout.figure` and boundingPoly. Capture associated `paragraph` blocks as captions when within ±10% of figure bbox.

- **AWS Textract**  
  Detect `BlockType=KEY_VALUE_SET` around figure images. Treat them as labels, route into `figure_metadata`.

- **Azure OCR**  
  Use boundingRegions and detect blocks adjacent to figures. Anchor captions if directly above/below polygon.

- **ABBYY**  
  In XML, `<block type="Picture">` + following `<par>` → caption. Inline text with picture coordinates goes to figure metadata.

- **PaddleOCR**  
  Split text lines overlapping with figure bbox. Store separately as figure text, not narrative.

---

## Data contract additions for figures
```

{
"figure\_id": "fig3",
"bbox": \[x0,y0,x1,y1],
"caption": "Figure 3: Error rate across embedding sizes.",
"figure\_metadata": {
"axis\_labels": \["tokens","ΔS"],
"legend": \["baseline","with WFGY"],
"text\_extracted": "0.45, 0.30..."
},
"section\_id": "4.2",
"page": 12,
"source\_url": "..."
}

```

Mandatory: all figure text lives in `figure_metadata` or `caption`, never in `text_clean`.

---

## Verification
- **Leak check**: ensure no caption/axis strings appear in `text_clean`.
- **Figure QA**: ask "what does fig3 show?" — answer must cite `figure_id`.
- **ΔS probe**: figure-specific questions yield ΔS ≤ 0.45.
- **λ probe**: paraphrases about same figure converge.

---

## Copy-paste LLM prompt
```

You have TXT OS and WFGY Problem Map.

For figure-linked snippets:

* use text\_clean for reasoning,
* use caption and figure\_metadata for figure answers,
* cite figure\_id.

Tasks:

1. If figure text leaks into body, fail fast and return fix reference (ocr-parsing-checklist, data-contracts, retrieval-traceability).
2. Return JSON:
   { "citations":\["fig3"], "answer":"...", "λ\_state":"...", "ΔS":0.xx, "next\_fix":"..." }

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

