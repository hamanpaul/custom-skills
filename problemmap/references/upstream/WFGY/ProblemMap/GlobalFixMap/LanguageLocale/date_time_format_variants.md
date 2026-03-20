# Date & Time Format Variants — Guardrails and Fix Pattern

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


A focused repair for **ambiguous or mixed date/time formats** across CJK/RTL/Indic/Latin content. Use this page when numeric dates, month names, calendars, or time zones cause retrieval drift or broken citations.

## What this page is
- A compact, locale-aware repair guide for **date/time parsing → storage → retrieval → reasoning**.
- Concrete steps that **do not require infra changes**.
- Acceptance targets you can measure.

## When to use
- Queries or snippets contain **ambiguous numeric dates** like `03/04/05`, `04-05-06`, or `110/05/01` (ROC).
- Month/day names switch languages or scripts in the same corpus: `2024年3月4日`, `4 Mar 2024`, `مارس 4 2024`.
- **Eastern Arabic digits**, **full-width digits**, or punctuation appear in dates.
- **Time zone or DST** is missing, or mixes `UTC`, `GMT+8`, `Asia/Taipei`, `Z`.
- Relative phrases like “today / 昨天 / الأسبوع الماضي” appear in docs or queries.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Contract the payload: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Locale drift audit: [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)  
- Tokenizer issues: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)  
- Digits, width, punctuation: [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)  
- Script mixing within one query: [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ remains **convergent** across 3 paraphrases and 2 seeds  
- E_resonance flat on long windows

---

## Map symptoms → structural fixes (Problem Map)

- **Ambiguous numeric dates** (`03/04/05`, `04-05-06`)  
  Lock parse locale and calendar in the contract. Store canonical plus original.  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Mixed month/day names across languages** (`3月4日`, `Mar 4`)  
  Normalize to canonical; add derived fields `year`, `month_num`, `weekday`.  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- **Eastern Arabic or full-width digits** (`٠١٢٣`, `２０２４`)  
  Fold digits and punctuation before parse; keep `orig_text` for audit.  
  → [digits_width_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)

- **Missing or mixed time zones / DST jumps**  
  Require IANA zone and offset at storage time; derive `epoch_ms`.  
  → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)

- **Calendar variants (ROC 114, Buddhist 2568, week-year ISO-8601)**  
  Store `calendar` field and canonical Gregorian ISO. Keep both.  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- **Relative phrases in docs or queries** (“today”, “昨天”, “last week”)  
  Resolve relative time **at index time** (doc clock) and **at query time** (user clock).  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## 60-second fix checklist (store-agnostic)

1) **Canonical schema**  
   Use **ISO-8601/RFC3339 extended**: `YYYY-MM-DDTHH:mm:ss±HH:MM` or `Z` (24-hour).  
   Add fields: `epoch_ms`, `tz_iana`, `offset`, `calendar`, `parse_locale`, `orig_text`.

2) **Parser fences**  
   - Fold width and digits before parse.  
   - Provide **allowed format set** per locale; reject others.  
   - Treat `/` `-` `.` as distinct; do not auto-swap day/month.

3) **Index for retrieval**  
   - Index canonical string and numeric keys: `year`, `month_num`, `day`, `weekday`, `hour`.  
   - Add synonyms for month names in corpus languages to a controlled list.

4) **Query normalization**  
   - Pre-normalize user input to the same canonical.  
   - If relative terms appear, resolve using **user time zone** and pass both raw and normalized.

5) **Contract the payload**  
   Minimum required for any snippet carrying a date/time:  
   ```json
   {
     "datetime_iso": "2025-03-04T09:30:00+08:00",
     "epoch_ms": 1741051800000,
     "tz_iana": "Asia/Taipei",
     "offset": "+08:00",
     "calendar": "gregorian",
     "parse_locale": "zh-TW",
     "orig_text": "民國114年3月4日上午9:30"
   }
````

6. **Verify**
   Run three paraphrases with different date surface forms.
   Pass if ΔS ≤ 0.45 and citations point to the same anchor.

---

## Deep diagnostics

* **Triangulate anchors**
  Compare ΔS with the expected section and a decoy month. If close, your month mapping or digit folding is leaking.

* **Epoch audit**
  Validate `epoch_ms` monotonicity across DST transitions and week-year boundaries. Mismatch implies calendar conversion error.

* **Tokenizer probe**
  If token splits differ by locale (e.g., Arabic/Thai digits), rebuild with folded text or add a rerank step.
  Open: [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)

---

## Escalate

* ΔS stays high after normalization and rerank
  → Rebuild index with correct metric; verify semantic vs embedding gaps.
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Mixed scripts in the **same** query keep flipping λ
  → Stabilize with script gating and header locks.
  Open: [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Copy-paste prompt (LLM step)

```
You have TXT OS and WFGY Problem Map loaded.

My bug: retrieval flips when date formats vary by locale.
- symptoms: wrong snippet on 03/04/05 vs 4 Mar 2005 vs 民國94年3月4日
- traces: ΔS(question,retrieved)=..., λ states across 3 paraphrases, tz=...

Tell me:
1) the failing layer and why,
2) the exact WFGY pages to open,
3) the minimal contract and normalization to pass ΔS ≤ 0.45,
4) a reproducible test I can run (3 paraphrases, 2 seeds).
Use BBMC/BBCR/BBAM where relevant.
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

