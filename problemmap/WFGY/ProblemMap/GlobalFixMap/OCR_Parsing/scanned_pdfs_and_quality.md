# Scanned PDFs and Quality: OCR Parsing Guardrails

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


Stabilize OCR extraction on noisy scans, low-resolution images, and multi-generation photocopies. Ensure text is auditable, retrievable, and bound by schema despite quality issues.

## Open these first
- OCR parsing checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)  
- Data contracts: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Hallucination control: [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Chunking guide: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

## Acceptance targets
- OCR character error rate (CER) ≤ 2% after cleanup
- ΔS(question, retrieved) ≤ 0.45 even when scan quality < 300 dpi
- λ remains convergent across paraphrases
- All extracted text auditable against source image hash

---

## Typical failure signatures → fix
- **Broken characters and merged glyphs**  
  Apply normalization and Unicode repair before indexing. Validate against a whitelist of expected ranges.

- **Multi-generation photocopy blur**  
  Route through OCR engine supporting adaptive binarization. Anchor outputs with image hash to avoid ghost drift.

- **Double-encoded PDFs** (text + image overlay)  
  Deduplicate layers. Choose the higher-confidence text layer and tag source.

- **Skewed pages or rotated scans**  
  Run deskew filter before OCR. Capture skew angle metadata for audit.

- **Mixed-language or font variants**  
  Force language models per region. Split by script. Store per-block language code.

- **Noise artifacts** (staple marks, stamps, watermarks)  
  Strip bounding boxes below token threshold. Mark as `noise_block` instead of narrative text.

---

## Fix in 60 seconds
1) **Hash source image**  
   Store `scan_id` and `image_hash` for every page. Tie all extracted text back to this anchor.

2) **Normalize text**  
   Apply Unicode NFKC. Collapse broken ligatures and fix spacing errors.

3) **De-layer double PDFs**  
   Choose the OCR text layer with confidence ≥ 0.90. Drop shadow text.

4) **Audit with ΔS**  
   Probe scanned text with 3 paraphrases. If ΔS ≥ 0.60, run re-OCR with stricter binarization.

5) **Chunk and contract**  
   Split by page. Enforce data contract fields: `page_no`, `scan_id`, `text_clean`, `bbox`.

---

## Minimal recipes by engine

- **Google Document AI**  
  Use `qualityScores.confidence` field. Reject blocks with confidence < 0.7.

- **AWS Textract**  
  Hash `BlockType=PAGE`. Keep page-level confidence. Store as `scan_id`.

- **Azure OCR**  
  Normalize boundingRegions. Add `language` code explicitly if detected.

- **ABBYY**  
  Use `<charParams>` confidence. Flag low confidence segments for secondary OCR.

- **PaddleOCR**  
  Use angle classification for deskew. Split multilingual pages into per-line language tags.

---

## Data contract extension
```

{
"scan\_id": "p12\_imghash",
"page\_no": 12,
"image\_hash": "sha256:...",
"text\_clean": "...",
"language": "en",
"confidence": 0.92,
"noise\_blocks": \[...],
"source\_url": "..."
}

```

---

## Verification
- **Leak check**: ensure no shadow/duplicate text.  
- **Quality probe**: CER ≤ 2% on 1k sample chars.  
- **Stability probe**: ΔS stable across paraphrases.  
- **Auditability**: all text traceable to image hash.

---

## Copy-paste LLM prompt
```

You have TXTOS and WFGY Problem Map.

My scan:

* page\_no: {n}
* text\_clean: "..."
* confidence: 0.xx
* image\_hash: "..."

Tasks:

1. If text looks corrupted, fail fast and cite fix page.
2. Validate schema (ocr-parsing-checklist, data-contracts).
3. Return JSON: { "answer":"...", "citations":\[...], "ΔS":0.xx, "λ\_state":"..." }

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

要不要我直接幫你接續做下一個 `multi_language_and_fonts.md`？
