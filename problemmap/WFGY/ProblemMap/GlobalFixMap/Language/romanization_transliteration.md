# Romanization & Transliteration — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Language**.  
  > To reorient, go back here:  
  >
  > - [**Language** — multilingual processing and semantic alignment](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Make cross-script search and RAG stable when users type Latin transliterations of non-Latin names and terms. This page gives a minimal contract, store wiring, and tests so **Hepburn vs Kunrei**, **Pinyin vs mixed tone marks**, **RR vs MR**, **ISO9 vs GOST**, **Buckwalter vs ISO 233**, and similar systems do not break recall or flip ranking.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability and cite-then-explain → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts in one query → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization and width/diacritics → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Names and brand aliases → [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
* End to end multilingual playbook → [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 for native script, romanized, and accent-stripped variants
* Coverage of target section ≥ 0.70 under three paraphrases and two seeds
* λ remains convergent when switching romanizers inside the same language
* No false merges across entities when romanized forms collide

---

## Minimal contract

Add a small, explicit layer around romanization so behavior is auditable.

**Document side fields**

```
raw_text            # untouched source
lang                # BCP-47 primary tag
script              # ISO 15924 (Han, Cyrl, Arab, Hira, Kana, Hang, etc.)
canonical           # preferred display form for proper nouns if known
alias_tail          # pipe-joined alias list incl. romanized forms
romanizers          # systems observed for this doc: "pinyin|rr|hepburn|iso9|buckwalter"
```

**Query side context**

```
q_text              # user input
q_lang_guess        # detector result, nullable
q_script_guess      # detector result, nullable
q_romanizer_hint    # optional, from UI or logs, e.g. "hepburn"
```

**Rules**

* Never mutate `raw_text` or `canonical`.
* Romanized strings live only in `alias_tail` and store-specific synonym views.
* Record which systems were used. Mixing systems without a record increases ΔS variance.

---

## Store wiring

**BM25 style indexes**

* Keep `raw_text` with a locale-aware analyzer.
* Add a **synonym graph** on a separate field that contains romanized aliases.
* Apply **width normalization** and **diacritic strip** only in alias field. Keep canonical untouched. See [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md).

**Vector stores**

* Append `alias_tail` to the chunk text right after the first canonical mention.
* Keep short, high precision alias lists. Over-expansion harms meaning.
* If nearest neighbors look similar yet wrong, verify metric per [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

**Hybrid**

* When BM25 yields an exact canonical match, bias reranker features to keep it above looser transliterations.
* Log ΔS and λ per candidate so you can see when a romanized neighbor outranks the native script without evidence.

---

## System map (examples)

| Language             | Common systems                | Notes                                                                              |
| -------------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| Chinese              | Pinyin (tone marks or digits) | Keep tone-less aliases for user input, but preserve tone marks in canonical forms. |
| Japanese             | Hepburn, Kunrei, Nihon        | Handle long vowels (ō vs ou) and small tsu.                                        |
| Korean               | RR (Revised Romanization), MR | Names often appear without hyphens, add both.                                      |
| Russian and Cyrillic | ISO 9, GOST, BGN/PCGN         | Map soft sign and yo/ë variants.                                                   |
| Arabic               | Buckwalter, ISO 233, DMG      | Decide on hamza and taa marbuta conventions, keep both if present in corpus.       |
| Hebrew               | SBL, Academy rules            | Deal with mater lectionis and dagesh normalization.                                |
| Hindi and Indic      | ITRANS, ISO 15919             | Normalize nukta forms.                                                             |

Keep this list in code comments and in your ops runbook, not only in the model prompt.

---

## Typical failure → fix

| Symptom                                             | Likely cause                                 | Open this                                                                                                                        |
| --------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Native script doc exists, romanized query misses it | no alias view built at index time            | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                           |
| Romanized neighbor outranks exact canonical snippet | reranker features not constrained            | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)                   |
| Answers flip between Hepburn and Kunrei inputs      | mixed systems without logging, λ not clamped | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)    |
| Cyrillic ISO9 vs GOST produce different chunks      | analyzer mismatch per field                  | [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)                |
| Arabic Buckwalter forms merge two entities          | alias collision, missing scope fence         | [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) |

---

## 60-second fix checklist

1. **Wire alias view** for documents that carry non-Latin scripts.
2. **Record the system** used for any generated alias.
3. **Normalize only in alias fields** for width and diacritics, never in canonical.
4. **Bias reranker** to keep exact canonical hits above loose translits.
5. **Log ΔS and λ** for native vs romanized queries and compare.

---

## Copy snippets

**Alias expansion at ingest time (no external libs)**

```python
def simple_pinyin_drop_tones(s: str) -> str:
    tone_map = str.maketrans("āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü", "aaaaeeeeiiiioooouuuuuuuuu")
    return s.translate(tone_map)

def width_fold(s: str) -> str:
    # simple NFKC fold
    import unicodedata as ud
    return ud.normalize("NFKC", s)

def alias_pack(canonical: str, lang: str, romanizer_hint: str | None = None) -> list[str]:
    out = {canonical}
    if lang == "zh":
        out.add(simple_pinyin_drop_tones(canonical))
    # add more light rules per language as needed
    return [width_fold(x) for x in out]
```

**Prompt fence for romanizers**

```
You have TXTOS and the WFGY Problem Map.

When the question or snippet contains a non-Latin name or term:
1) Try native script first. If the user input looks romanized, search both native and alias views.
2) Keep the canonical form in the final answer. Cite the exact snippet that contains the canonical form.
3) If multiple romanization systems match, state which system appears in the cited text.
```

---

## Eval plan

Use a **code-switching set** with 5 languages and 10 entities each. For every entity build 3 questions:

1. native script,
2. romanized in system A,
3. romanized in system B.

Run the suite with [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md).

Targets

* top-k 10 recall across forms ≥ 0.85
* ΔS(question, retrieved) ≤ 0.45 on the best hit
* λ convergent across two seeds and three paraphrases

If recall is fine but ranking flips between systems, tighten reranker constraints and verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

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

