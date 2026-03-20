# Keyboard Input Methods — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LanguageLocale**.  
  > To reorient, go back here:  
  >
  > - [**LanguageLocale** — localization, regional settings, and context adaptation](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A focused guide for bugs that originate from IME composition on Windows, macOS, Linux, iOS, and Android. Scope includes CJK IMEs (Pinyin, Wubi, Kana/Kanji, 2-set/3-set), Indic transliteration, RTL keyboards, and mixed fullwidth/halfwidth states. Use this when text looks fine to the eye but retrieval or validation behaves inconsistently across devices.

## When to use this page

* Reports say “works on Mac, fails on Windows IME” or “mobile input breaks search.”
* Fields contain invisible marks after copy or composition (ZWJ, ZWNJ, NBSP, RLM/LRM).
* Users toggle fullwidth digits or punctuation and recall suddenly collapses.
* Romanization IMEs produce composed characters that differ from pasted text.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Multilingual overview: [Multilingual Guide](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multilingual-guide.md)
* Tokenizer mismatch: [Tokenizer Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)
* CJK word breaks: [CJK Segmentation & Wordbreak](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)
* RTL markers and controls: [RTL & Bidi Controls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/rtl_bidi_controls.md)
* Script mixing: [Script Mixing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)
* Diacritics: [Diacritics & Folding](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)
* Snippet schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage of target section ≥ 0.70
* λ\_observe remains convergent across 3 paraphrases, 2 seeds, and 2 devices
* E\_resonance stays flat on long input windows

---

## Failure smells

* “Cannot reproduce” until tester types through an IME rather than pasting.
* Same glyphs, different bytes. Equality checks fail, search misses.
* Index recall drops after mobile users enable fullwidth digits.
* Mixed NBSP and normal space in otherwise identical queries.
* Sporadic RTL flip caused by stray RLM/LRM from bidirectional typing.

---

## Fix in 60 seconds

1. **Normalize early**
   On every input boundary apply NFC, width fold, and punctuation fold. Remove ZWJ, ZWNJ, LRM, RLM unless explicitly allowed by schema.

2. **Stabilize tokenization**
   Lock analyzers and tokenizers used for both indexing and querying. If ΔS remains high and flat after IME normalization, revisit metric and analyzer pairing in the store. See [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

3. **Contract the payload**
   For forms and tool calls, require fields that capture canonical and raw strings: `raw`, `normalized`, `locale`, `ime_mode`, `width_state`. Enforce this in your [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

4. **Probe λ**
   Run the same query by paste, by IME typing, and by mobile. If λ flips only for IME-typed paths, you have an input normalization gap.

---

## IME-safe schema (copy block)

Use this contract for any user text that enters retrieval or matching.

```json
{
  "text": {
    "raw": "<exact keystroke result>",
    "normalized": "<NFC + width_fold + punct_fold + bidi_strip>",
    "locale": "zh-TW | zh-CN | ja-JP | ko-KR | hi-IN | ...",
    "ime_mode": "pinyin | wubi | kana | romaji | 2set | 3set | translit | rtl",
    "width_state": "half | full | mixed",
    "bidi_marks": ["RLM","LRM","ZWJ","ZWNJ","NBSP"]
  }
}
```

Store both `raw` and `normalized`. Index `normalized`. Retain `raw` for audits and display.

---

## Normalization and folding rules

| Issue                             | Action                         | Notes                                               |
| --------------------------------- | ------------------------------ | --------------------------------------------------- |
| Composition variance (NFD vs NFC) | Convert to NFC                 | Prevents byte inequality for identical glyphs       |
| Fullwidth digits and Latin        | Width fold to ASCII            | Keep CJK letters untouched                          |
| Smart quotes, ellipsis, dashes    | Punctuation fold to ASCII set  | Avoid tokenizer splits that differ by device        |
| Zero-width characters (ZWJ, ZWNJ) | Strip by default               | Allow only if explicitly required by language rules |
| Bidi controls (LRM, RLM)          | Strip at input for LTR schemas | Keep only in rich text fields, never in keys        |
| NBSP, thin space                  | Map to normal space            | Collapse runs of spaces to a single space           |
| Kana halfwidth/fullwidth          | Fold within script             | Keep semantic marks like voiced sound when needed   |
| Romanization IMEs                 | Canonicalize case and spacing  | For JP/KR/Indic transliteration paths               |

---

## Tests you should run

* **Triplet equality**: paste vs IME vs mobile should produce identical `normalized`.
* **Search parity**: same top-k ordering after normalization across devices.
* **Width flip test**: force fullwidth digits and punctuation, verify recall remains constant.
* **Bidi contamination**: inject RLM/LRM in the middle, verify strip or deterministic handling.
* **ΔS plateaus**: if ΔS remains ≥ 0.60 after normalization, suspect metric mismatch or fragmentation and jump to [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

---

## Escalate with these pages

* Tokenizer and analyzer coupling: [Tokenizer Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)
* Script collisions and mixed runs: [Script Mixing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)
* CJK segmentation: [CJK Segmentation & Wordbreak](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)
* RTL handling: [RTL & Bidi Controls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/rtl_bidi_controls.md)
* Traceable answers: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

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

