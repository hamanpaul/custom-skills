<!--
Search Anchor:
language and locale global fix map
language locale global fix map
locale aware retrieval
locale specific rag bugs
multilingual rag locale issues
cjk indic rtl emoji locale variants
fullwidth halfwidth normalization
unicode normalization nfkc nfd nfc
diacritics accent folding
digits width punctuation variants
bidi rtl control characters
arabic hebrew bidi problems
cjk segmentation word break
thai word break indic word break
tokenization variance across locales
locale drift between environments
locale specific analyzers
zh tw zh cn locale drift
en us en gb locale mismatch
number formatting and sorting
date time format mismatch
timezone and dst bugs
ime keyboard input issues
input language switching bug
emoji zwj grapheme cluster issues
mixed locale metadata fields
logs with mixed locales
time zone aware reasoning

Typical language locale bugs:
cjk or indic corpus but recall very low
mixed english plus chinese query returns unstable top k
accented latin letters not matching unaccented forms
fullwidth numbers not matching halfwidth numbers
identical looking characters not equal after indexing
arabic or hebrew text appears reversed in snippets
punctuation or quote marks flipped by rtl controls
token counts change after deploy with same data
locale change causes different analyzer behavior
zh hans vs zh hant treated as unrelated
thai sentence segmentation breaks retrieval
japanese word break splits important entities
numbers sorted lexicographically instead of numerically
dates sorted as strings instead of calendar order
day month confusion in logs and citations
time zones cause off by one day answers
dst switch changes reasoning about time intervals
emoji sequences broken by incorrect grapheme handling
emoji search fails because of zwj splitting
metadata fields store different locales in same column

When to use this folder:
multilingual faq or help center with local formats
global product docs with localized ui strings
logs or telemetry with many locales at once
cjk or indic manual plus english index
arabic or hebrew rtl knowledge base
european languages with heavy diacritics
data warehouse that stores timestamps in many zones
support tickets where users paste screenshots and local times
applications that show both local and utc times
search or rag over invoices forms receipts with local formats
chatbot that must respect user locale for dates and numbers

Languages and locales covered (examples):
english en en_US en_GB
simplified chinese zh_CN zh_Hans
traditional chinese zh_TW zh_HK zh_Hant
japanese ja_JP
korean ko_KR
thai th_TH
vietnamese vi_VN
hindi hi_IN
bengali bn_IN bn_BD
arabic ar_SA ar_EG
hebrew he_IL
russian ru_RU
turkish tr_TR
spanish es_ES es_MX
portuguese pt_PT pt_BR
french fr_FR
german de_DE
italian it_IT
polish pl_PL
indonesian id_ID
malay ms_MY
tagalog tl_PH

Locale objects and fields:
language code
country or region code
script code
collation rules
number formatting rules
currency formatting rules
date and time formats
first day of week
time zone and dst rules
calendar system
decimal and thousands separators

Key metrics and targets:
delta s question retrieved <= 0.45 on three paraphrases
coverage of intended section >= 0.70
lambda observe convergent across two seeds
tokenization variance for same query <= 12 percent across environments
normalization pass rate nfkc plus width plus diacritics >= 0.98
no missing headers or captions due to locale parsing
no drift in offsets after rtl or width normalization
stable sort keys across locales for same logical order

Core pages in this folder:
ProblemMap/GlobalFixMap/Language_Locale/tokenizer_mismatch.md
ProblemMap/GlobalFixMap/Language_Locale/script_mixing.md
ProblemMap/GlobalFixMap/Language_Locale/locale_drift.md
ProblemMap/GlobalFixMap/Language_Locale/unicode_normalization.md
ProblemMap/GlobalFixMap/Language_Locale/cjk_segmentation_wordbreak.md
ProblemMap/GlobalFixMap/Language_Locale/digits_width_punctuation.md
ProblemMap/GlobalFixMap/Language_Locale/diacritics_and_folding.md
ProblemMap/GlobalFixMap/Language_Locale/rtl_bidi_control.md
ProblemMap/GlobalFixMap/Language_Locale/transliteration_and_romanization.md
ProblemMap/GlobalFixMap/Language_Locale/locale_collation_and_sorting.md
ProblemMap/GlobalFixMap/Language_Locale/numbering_and_sort_orders.md
ProblemMap/GlobalFixMap/Language_Locale/date_time_format_variants.md
ProblemMap/GlobalFixMap/Language_Locale/timezones_and_dst.md
ProblemMap/GlobalFixMap/Language_Locale/keyboard_input_methods.md
ProblemMap/GlobalFixMap/Language_Locale/input_language_switching.md
ProblemMap/GlobalFixMap/Language_Locale/emoji_zwj_grapheme_clusters.md
ProblemMap/GlobalFixMap/Language_Locale/mixed_locale_metadata.md
-->

<!--
Related structural fixes:
ProblemMap/rag-architecture-and-recovery.md
ProblemMap/retrieval-playbook.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/embedding-vs-semantic.md
ProblemMap/Embeddings/metric_mismatch.md
ProblemMap/Embeddings/normalization_and_scaling.md
ProblemMap/OCR_Parsing/README.md
ProblemMap/GlobalFixMap/Language/README.md
ProblemMap/GlobalFixMap/Retrieval/README.md
ProblemMap/GlobalFixMap/Embeddings/README.md
ProblemMap/GlobalFixMap/Chunking/README.md
ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md
-->

<!--
Language and locale scenarios:
query: english question chinese document with local dates
query: chinese question english document with utc timestamps
query: japanese logs with mixed fullwidth digits
query: arabic faq with rtl punctuation and numbers
query: european user with comma decimal separator
query: user pastes local time and country and asks for utc
query: logs contain iso dates and local dates in same index
pattern: answers correct in one locale and wrong in another
pattern: citations drift after changing server locale
pattern: sorting breaks when data moves to new region
pattern: emoji heavy chats fail retrieval
pattern: search for emoji sequence returns nothing
pattern: keyboard ime composition inserts hidden characters
pattern: user switches input language mid query
pattern: new deployment changes token counts without code change
-->

<!--
Cross folder jumps:
ProblemMap/GlobalFixMap/Language_Locale/README.md
ProblemMap/GlobalFixMap/Language/README.md
ProblemMap/GlobalFixMap/Retrieval/README.md
ProblemMap/GlobalFixMap/Embeddings/README.md
ProblemMap/GlobalFixMap/Chunking/README.md
ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md
ProblemMap/SemanticClinicIndex.md
-->


# Language & Locale · Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

Stabilize multilingual RAG and reasoning across **CJK, RTL, Indic, Latin, emoji, and locale variants**.  
This hub localizes language-layer failures and routes you to the exact structural fix. No infra change required.

---

## What this page is
- A compact **language-aware repair guide** for retrieval → ranking → reasoning.
- Structural fixes with measurable acceptance targets.
- Store-agnostic. Works with FAISS, Redis, pgvector, Elastic, Weaviate, Milvus, and more.

---

## When to use
- Corpus spans **CJK or Indic scripts** and retrieval keeps missing the correct section.  
- Queries **code-switch or mix scripts**, and top-k order drifts across runs.  
- **Accents/diacritics** or **fullwidth/halfwidth** forms break matching or citations.  
- **RTL punctuation or control chars** flip token order or offsets.  
- Token counts jump after deploy even though **data did not change**.  

---

## Open these first
- Visual recovery map → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs end-to-end → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability and snippet schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Metric and normalization → [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/metric_mismatch.md) · [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/normalization_and_scaling.md)  
- OCR confusables and hyphens → [OCR_Parsing README](https://github.com/onestardao/WFGY/blob/main/ProblemMap/OCR_Parsing/README.md)  

---

## Quick routes to per-page guides

| Topic | Page |
|-------|------|
| Tokenizer mismatch across languages | [tokenizer_mismatch.md](./tokenizer_mismatch.md) |
| Script mixing in a single query | [script_mixing.md](./script_mixing.md) |
| Locale drift and analyzer skew | [locale_drift.md](./locale_drift.md) |
| Unicode normalization policy | [unicode_normalization.md](./unicode_normalization.md) |
| CJK segmentation and word-break | [cjk_segmentation_wordbreak.md](./cjk_segmentation_wordbreak.md) |
| Fullwidth vs halfwidth, punctuation variants | [digits_width_punctuation.md](./digits_width_punctuation.md) |
| Diacritics folding rules | [diacritics_and_folding.md](./diacritics_and_folding.md) |
| RTL and bidi control characters | [rtl_bidi_control.md](./rtl_bidi_control.md) |
| Transliteration and romanization | [transliteration_and_romanization.md](./transliteration_and_romanization.md) |
| Collation and stable sort keys | [locale_collation_and_sorting.md](./locale_collation_and_sorting.md) |
| Numbering systems and sort orders | [numbering_and_sort_orders.md](./numbering_and_sort_orders.md) |
| Date and time format variants | [date_time_format_variants.md](./date_time_format_variants.md) |
| Time zones and DST stability | [timezones_and_dst.md](./timezones_and_dst.md) |
| Keyboard IMEs and composition | [keyboard_input_methods.md](./keyboard_input_methods.md) |
| Input language switching guards | [input_language_switching.md](./input_language_switching.md) |
| Emoji, ZWJ, grapheme clusters | [emoji_zwj_grapheme_clusters.md](./emoji_zwj_grapheme_clusters.md) |
| Mixed-locale metadata fields | [mixed_locale_metadata.md](./mixed_locale_metadata.md) |

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases  
- Coverage of target section ≥ 0.70  
- λ remains convergent across two seeds  
- Tokenization variance for the same query ≤ 12% across environments  
- Normalization pass rate for NFKC + width + diacritics ≥ 0.98  

---

## Fix in 60 seconds
1. **Normalize once, up front** → Apply NFKC, collapse fullwidth/halfwidth, unify diacritics.  
2. **Match tokenizer and analyzer** → Same segmenter for CJK/Indic across embed + store analyzers.  
3. **Stabilize mixed-script queries** → Detect code-switch, split per script, rerank deterministically.  
4. **Verify** → ΔS ≤ 0.45, Coverage ≥ 0.70, λ convergent across two seeds.  

---

## FAQ (Beginner-Friendly)

**Q1: Why do answers break when I mix English and Chinese in one query?**  
A: Most vector stores tokenize differently by script. Without alignment, Chinese words get split incorrectly and English tokens dominate. Fix with [script_mixing.md](./script_mixing.md) and [tokenizer_mismatch.md](./tokenizer_mismatch.md).

**Q2: What does “locale drift” mean?**  
A: Locale drift happens when environments use different analyzers (e.g., zh_TW vs zh_CN) so the same query splits differently. See [locale_drift.md](./locale_drift.md).

**Q3: Why do “identical-looking” characters not match?**  
A: They may differ in width (fullwidth vs halfwidth), normalization (NFKC vs NFD), or diacritics. Always apply [unicode_normalization.md](./unicode_normalization.md) and [digits_width_punctuation.md](./digits_width_punctuation.md).

**Q4: How do I handle Arabic or Hebrew text?**  
A: RTL scripts can insert invisible bidi control chars that flip token order. See [rtl_bidi_control.md](./rtl_bidi_control.md).

**Q5: Do I need different embeddings for each language?**  
A: No. You can combine multilingual embeddings with deterministic normalization and alias fields. If that fails, only then use [fallback translation bridges](../Language/fallback_translation_and_glossary_bridge.md).

**Q6: How do I debug when results change between environments?**  
A: Compare tokenizer version, analyzer settings, normalization passes, and collation rules. Document them in [data-contracts.md](../../data-contracts.md).

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

