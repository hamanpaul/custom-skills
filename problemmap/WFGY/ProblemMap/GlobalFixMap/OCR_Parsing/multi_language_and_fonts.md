# Multi-language and Fonts: OCR Parsing Guardrails

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


Stabilize OCR when documents mix scripts, uncommon fonts, or character sets. Prevent silent corruption when engines guess wrong language or merge glyphs across font families.

## Open these first
- OCR parsing checklist: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)  
- Data contracts: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Tokenization and casing: [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OCR_Parsing/tokenization_and_casing.md)  
- Unicode normalization: [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md)

## Acceptance targets
- Language detection accuracy ≥ 0.95 per block
- Font mis-read rate < 1% per 1,000 chars
- No cross-script merges (CJK vs Latin, RTL vs LTR)
- ΔS(question, retrieved) ≤ 0.45 after language split

---

## Typical failure signatures → fix
- **CJK vs Latin collisions**  
  OCR merges Latin letters inside Chinese/Japanese text. Split into script-specific blocks, then re-OCR with correct language model.

- **Right-to-left scripts** (Arabic, Hebrew) misaligned  
  Store `direction=rtl` metadata. Reverse tokens if engine defaults to LTR.

- **Uncommon fonts or stylized typefaces**  
  Preprocess with font normalization (convert to system fonts). Use OCR engine with adaptive recognition.

- **Mixed languages in same paragraph**  
  Detect language per line or span. Store `lang_code` for each.

- **Math vs text confusion**  
  Superscripts, subscripts, and symbols misinterpreted as language characters. Route math zones separately. Tag as `math_block`.

---

## Fix in 60 seconds
1) **Detect language per block**  
   Run script detection. Assign `lang_code` and `direction`. Reject ambiguous blocks.

2) **Normalize Unicode**  
   Apply NFKC, collapse ligatures, unify spacing.

3) **Re-OCR with correct model**  
   For each block, call OCR with explicit `lang_code`. Prefer specialized models (e.g., PaddleOCR multilingual, ABBYY).

4) **Attach metadata**  
   Store `lang_code`, `direction`, `font_name` if available.

5) **Audit with ΔS**  
   Probe retrieval stability with three paraphrases. If ΔS ≥ 0.60, recheck font normalization.

---

## Data contract extension
```

{
"block\_id": "scan12\_line4",
"lang\_code": "zh",
"direction": "ltr",
"font\_name": "SimSun",
"text\_clean": "...",
"confidence": 0.93,
"source\_url": "..."
}

```

---

## Minimal recipes by engine

- **Google Document AI**  
  Use `detectedLanguages.languageCode` per block. Reject if confidence < 0.8.

- **AWS Textract**  
  No native multi-lang. Wrap with external script detection. Add `lang_code` manually.

- **Azure OCR**  
  `language` field auto-detected. Cross-check with Unicode ranges.

- **ABBYY**  
  Supports per-block language tags. Ensure config has all needed languages.

- **PaddleOCR**  
  Use multilingual model. Explicitly set `--lang` flag to avoid mis-guess.

---

## Verification
- **Script coverage**: verify all scripts recognized.  
- **Direction check**: RTL blocks labeled correctly.  
- **Font audit**: ensure no decorative font corruption.  
- **Retrieval stability**: ΔS stable across paraphrases.  

---

## Copy-paste LLM prompt
```

You have TXTOS and WFGY Problem Map loaded.

My OCR block:

* text\_clean: "..."
* lang\_code: "ar"
* direction: "rtl"
* font\_name: "Courier"

Check:

1. If characters look corrupted, fail fast and cite fix page.
2. Enforce schema with lang\_code and direction.
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

