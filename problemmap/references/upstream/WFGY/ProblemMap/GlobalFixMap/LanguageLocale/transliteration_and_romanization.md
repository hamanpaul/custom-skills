# Transliteration & Romanization — Global Fix Map

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


Stabilize queries when users type **Pinyin/Romaji/IAST/RTGS/Buckwalter** variants instead of native scripts.  
Use this page to bridge **native-script ↔ romanized** forms for retrieval, ranking, and reasoning without changing infra.

---

## What this page is
- A compact repair guide for **script-to-roman** mismatches in RAG and search.
- Concrete schema rules and query tactics that unify **multiple romanization systems** per language.
- Exact jump links to structural fixes so you can verify with measurable targets.

## When to use
- Users type **Pinyin with tone marks vs numbers** or ad-hoc English spellings.
- Japanese **Hepburn vs Kunrei** differences (“shi/si”, “tsu/tu”; macron “ō” vs “ou”).
- Korean **Revised RR vs McCune-Reischauer** (“Busan/Pusan”, “Jeju/Cheju”).
- Arabic/Persian **DIN/Buckwalter/ad-hoc** (“Muhammad/Mohamed/Mohammad”).
- Cyrillic names produce **Čajkovskij/Chaikovsky/Tchaikovsky** style drift.
- Greek/Indic/Vietnamese diacritics collapse or fold in unpredictable ways.
- Native pages index fine, yet **romanized queries miss or rank poorly**.

---

## Open these first
- Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Tokenizer fit: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Diacritic folding: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)  
- Locale drift: [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)  
- CJK wordbreaks: [cjk_segmentation_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)  
- Mixed scripts in one query: [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)

---

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.  
- Coverage of target section ≥ 0.70.  
- λ remains convergent across two seeds.  
- **Cross-script parity**: romanized query recall ≥ 0.90 of native-script recall on your gold set.

---

## Common failure patterns → exact fix

- **Romanization system mismatch** (e.g., Hepburn vs Kunrei, RR vs MR, DIN vs ad-hoc).  
  Lock a canonical key and index both forms.  
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Tone marks vs numbers in Pinyin** (“lǐ/lĭ/li3”).  
  Add a tone-stripped key and a numeric-tone key, dedupe at index time.  
  Open: [diacritics_and_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)

- **Macrons and long vowels in Romaji** (“ō/oo/ou”).  
  Normalize to a canonical long-vowel key and store alternates.  
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Arabic definite article or spacing drift** (“al Riyadh/Ar-Riyāḍ/Riyadh”).  
  Strip articles into a side key; keep original for display.  
  Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Query parsing split** under hybrid retrievers when romanized variants explode terms.  
  Pin two-stage queries and rerank deterministically.  
  Open: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## 60-second fix checklist

1) **Measure ΔS and λ**  
   Compute ΔS(question, retrieved). If ΔS ≥ 0.60 and λ flips on small romanization edits, treat as schema/index mismatch.

2) **Add a Romanization Bridge** (store-agnostic)
- For each document and title, compute and store:
  - `key_native` = original script  
  - `key_roman_primary` = your chosen canonical system per language  
  - `key_roman_alt[]` = enumerated alternates (e.g., Hepburn/Kunrei, RR/MR, DIN/ad-hoc, Pinyin tone/number)  
- Index `key_native` and `key_roman_*` in the same record; **dedupe** by stable `doc_id`.
- At query time, expand to canonical plus alternates, then **rerank**.

3) **Lock the contract**  
   Require fields in the snippet payload:  
   `lang`, `script`, `roman_system`, `key_roman_primary`, `key_roman_alt`, `source_url`, `offsets`.  
   See: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Probe robustness**  
   Run a three-paraphrase test: native script, canonical romanization, alternate romanization.  
   Targets must meet **Acceptance**.

---

## Minimal per-language mapping hints

- **Chinese**: tone marks ↔ numeric tones; collapse `ü` ↔ `v` in legacy inputs.  
- **Japanese**: macron `ō/ū` ↔ `ou/oo/uu`; “shi/si”, “ji/zi”, “chi/ti”, “tsu/tu”; small “っ/tsu” doubling.  
- **Korean**: RR ↔ MR pairs (“Busan/Pusan”, “Jeju/Cheju”, “Gyeong/ Kyŏng”).  
- **Arabic/Persian**: articles `al-/el-` optional; hamza/ta marbuta variants; DIN ↔ Buckwalter map.  
- **Indic (IAST/ISO/Harvard-Kyoto)**: `ś/ṣ/ñ/ṭ/ḍ` ↔ `sh/sh/ny/t/d`.  
- **Cyrillic**: `Ч/ч` ↔ `Ch/Č`, `Ю/ю` ↔ `Yu/Iu`, etc., preserve soft sign loss with an alternate key.  
- **Greek**: `Μιχάλης` ↔ `Michalis/Michales`; handle `mp/nt` digraphs.

Document your choices inside `roman_system` so audits are reproducible.

---

## Copy-paste prompt (LLM step)

```

You have TXT OS and the WFGY Problem Map loaded.

My multilingual issue:

* symptom: romanized queries miss or rank poorly vs native script
* traces: ΔS(question,retrieved)=..., λ states across native/roman/alternate

Tell me:

1. which layer is failing and why,
2. the exact WFGY page to open,
3. the minimal Romanization Bridge to add (keys + query expansion),
4. how to verify with coverage ≥ 0.70 and ΔS ≤ 0.45 across three paraphrases.
   Reference: retrieval-playbook, retrieval-traceability, data-contracts, diacritics\_and\_folding.

```

---

## Next planned file in `LanguageLocale/`
- **mixed_numeric_systems.md**  ← numbers written in native digits vs ASCII, year/era systems, and counters.

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

