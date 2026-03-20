# Numbering & Sort Orders — Language-aware Collation

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


Stabilize ranking, citations, and UI lists when locale collation and numbering systems differ from ASCII order. This page fixes “looks sorted but retrieval flips” and “citations jump rows between runs”.

---

## When to use this page
- Lists look sorted to users but change order across runs.
- Numerics sort as text (“2” after “10”), or different digit sets mix (ASCII, Arabic-Indic, Devanagari).
- CJK collation groups by codepoint not by radicals/pinyin/custom.
- Accents or folded forms collide (“résumé” vs “resume”) and break stable keys.
- Search results rerank differently after deploy on another OS or locale.

---

## Open these first
- Visual map and recovery → [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Why this snippet and citation schema → [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema and stable keys → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Wrong-meaning near neighbors → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Query split that reshuffles order → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

Related LanguageLocale pages
- Tokenizer mismatch → [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Digits, width, punctuation → [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)  
- Diacritics and folding → [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)  
- CJK word-breaks → [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)  
- Locale drift between nodes → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases  
- Coverage of target section ≥ 0.70  
- λ stays convergent across two seeds  
- Collation stable across platforms for the same `locale`, `numeric`, `case`, and `sensitivity` settings

---

## Map symptoms → structural fixes (Problem Map)
- **“2, 10, 3” sort order** or mixed digit systems  
  → Normalize digits and enable numeric collation.  
  Spec: [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Accent collides or reorders after deploy**  
  → Fix ICU collator options and fold consistently.  
  Spec: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md) · [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

- **CJK “sorted” by codepoint not by language expectation**  
  → Use locale collation (zh, ja, ko) or custom key.  
  Spec: [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)

- **Hybrid retrievers underperform after “sorting fix”**  
  → Query split or reranker blind spots.  
  Spec: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## 60-second fix checklist
1) **Normalize and tag**
- Convert all digits to a canonical set before indexing.  
  Recommended: NFKC, then digit map to ASCII.  
- Persist `locale`, `script`, `collator_options` on every list, key, and snippet.

2) **Use a real collator**
- Enable ICU/Locale collation with explicit options:  
  `numeric=true`, `caseLevel=false`, `sensitivity=base|accent`, `ignorePunctuation=true` where appropriate.  
- Keep the same options in both indexing and query time. Record them in logs.

3) **Stable keys for citations**
- Derive `sort_key = collator(key_text)` and store alongside raw text.  
- Use `sort_key` to order snippets and to generate stable page anchors.

4) **CJK specifics**
- If users expect pinyin/reading order, precompute a language-specific `sort_key_pinyin` or `kana_key`.  
- For ideograph radicals or stroke count, store explicit numeric keys and sort numerically.

5) **Verify**
- Run three paraphrases and two seeds.  
- Pass thresholds: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent.  
- Cross-platform check: Linux vs Windows vs Mac produce identical order for the same settings.

---

## Minimal schema (Data Contracts)
Add these fields to any list, index, or snippet payload:
```json
{
  "locale": "zh-Hans-CN",
  "script": "Hans",
  "number_system": "latn",
  "collator": {
    "numeric": true,
    "sensitivity": "base",
    "caseLevel": false,
    "ignorePunctuation": true
  },
  "sort_key": "<opaque-stable-key>",
  "norm": {
    "unicode": "NFKC",
    "digits_mapped": true
  }
}
````

Contract guide → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Copy-paste prompt for your LLM step

```
You have TXT OS and the WFGY Problem Map loaded.

My issue is unstable order under mixed locales.
Inputs:
- locale = {locale}, script = {script}, number_system = {num}
- collator = {numeric, sensitivity, caseLevel, ignorePunctuation}
- traces: ΔS(question,retrieved)=..., λ states across 3 paraphrases

Do:
1) Tell me if instability comes from collation vs retrieval.
2) Point me to the exact WFGY page to open next.
3) Give the minimal steps to reach ΔS ≤ 0.45 with stable order across platforms.
Return a short JSON plan with fields {fix_layer, next_page, steps[], verify}.
```

---

## Next planned file

`mixed_locale_metadata.md` — contract for storing locale/script/number system/tokenizer and cross-node validation rules.

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

**下一個要做：** `mixed_locale_metadata.md`（LanguageLocale 契約欄位與驗證規則）。
