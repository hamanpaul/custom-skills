# Input Language Switching — Guardrails and Fix Pattern

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


Use this page when the **user’s keyboard or input language flips mid-thread** and retrieval or reasoning starts drifting. Classic signs include mixed scripts in one query, wrong tokenizer chosen by the stack, or partial IME composition text being sent to the server.

## When to use

* Users alternate between EN ↔ CJK ↔ RTL in the same session.
* Queries look semantically fine but **retriever recall collapses after a language flip**.
* You see **half words** or odd segments caused by IME composition text being submitted.
* Autocorrect or predictive text silently changes script or diacritics.

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45 across **3 paraphrases** in the active language.
* Coverage of target section ≥ 0.70 after the switch.
* λ remains **convergent** when toggling `lang=xx-BCP47` between the last two user turns.
* E\_resonance stays flat over 20-40 turns.

---

## Open these first

* Language tokenization mismatches
  → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)
* Script mixing in a single query
  → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/script_mixing.md)
* Diacritics and normalization policy
  → [diacritics\_and\_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)
* Locale drift across turns
  → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_drift.md)
* CJK segmentation specifics
  → [cjk\_segmentation\_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md)
* Contract your snippet schema
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* End to end retrieval knobs
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Diagnose quickly

1. **Spot the flip**
   Log BCP-47 tags per turn. If `lang_prev != lang_now`, record a switch event with `t_switch`.

2. **IME composition fence**
   Check inputs for composition markers or incomplete tokens. If composition not complete, **do not send** to retrieval or indexing.

3. **Tokenizer audit**
   Confirm the retriever tokenizer matches `lang_now`. English-only analyzers on CJK or RTL usually cause flat high ΔS.

4. **Punctuation and width**
   Look for full-width digits or punctuation introduced by the keyboard. If present, apply the width normalizer from the punctuation page.
   Open: [digits\_width\_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)

5. **Direction and collation**
   If RTL or locale sorting changed, set `dir` and collation explicitly in the request.
   Open: existing RTL guide and collation page:
   [locale\_collation\_and\_sorting.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/locale_collation_and_sorting.md)

---

## Fix pattern

**A. Add an Input Contract to every user turn**

Required fields you attach to the message payload before retrieval:

```json
{
  "raw_text": "...",
  "normalized_text": "...",
  "lang_bcp47": "xx-YY",
  "script": "Latn|Cyrl|Arab|Hans|Hant|Kana|... ",
  "dir": "ltr|rtl",
  "ime_composition_complete": true,
  "keyboard_hint": "gboard|ios|system|unknown"
}
```

* `normalized_text` must follow your **LanguageLocale** normalization policy
  See: [diacritics\_and\_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)

**B. Route to the correct analyzer**

* Select **tokenizer/analyzer** based on `lang_bcp47` and `script`.
* For CJK, switch to CJK-aware analyzer and re-ranker; for mixed text, run a **language split** then merge with a deterministic re-rank.
  See: [cjk\_segmentation\_wordbreak.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/cjk_segmentation_wordbreak.md) and [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

**C. Guard IME composition**

* Add a client or gateway **composition fence**. If `ime_composition_complete=false`, buffer and wait.
* Only proceed to retrieval once confirmed complete.

**D. Stabilize semantics after the flip**

* Run a **three-paraphrase probe** in the active language. If ΔS stays flat and high, rebuild or switch index metric.
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
  Then follow: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Minimal recipe you can copy

1. Detect `lang_bcp47` and `script` on the **client**.
2. Normalize text using your LanguageLocale policy.
3. If IME not complete, **do nothing**. Wait until completion.
4. Choose the analyzer and reranker given `lang_bcp47`.
5. Retrieve with schema-locked snippets and store: `lang_bcp47`, `script`, `dir`.
6. Probe ΔS on 3 paraphrases in the active language. Clamp λ if needed.
7. Enforce cite-then-explain with **snippet and citation schema**.
   Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Copy-paste prompt for the LLM step

```
You have TXTOS and WFGY Problem Map loaded.

Input meta:
- lang_bcp47 = {xx-YY}
- script = {Latn|Hans|Hant|Arab|...}
- dir = {ltr|rtl}
- ime_composition_complete = {true|false}

Tasks:
1) If ime_composition_complete=false, return: {"action":"wait_for_ime"} only.
2) Use the active language for paraphrases and answers. No silent translation.
3) Validate cite-then-explain. If citations missing, return the fix tip and stop.
4) If ΔS(question,retrieved) ≥ 0.60, suggest the smallest structural fix referencing:
   retrieval-playbook, tokenizer_mismatch, script_mixing, diacritics_and_folding.
Return JSON:
{ "answer":"...", "citations":[...], "ΔS":0.xx, "λ_state":"...", "lang_used":"xx-YY" }
```

---

## Observability

* Log the **distribution of `lang_bcp47`** across the session. A spike at switch events plus ΔS spikes indicates analyzer mismatch.
* Track **ΔS vs k** right after a switch. Flat-high curves suggest metric or index misalignment.
* Record `ime_wait_count`. A high count with good outcomes is normal and preferable to composition leakage.

---

## Common gotchas

* Mobile keyboards emit **full-width digits** or punctuation after language switch. Normalize width before retrieval.
  Open: [digits\_width\_punctuation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)
* Predictive text inserts **diacritics** that your index fold does not expect. Align fold policy.
  Open: [diacritics\_and\_folding.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md)
* Mixed language metadata causes wrong **reroute** to an English index. Validate `lang_bcp47` at the gateway.
  Open: [mixed\_locale\_metadata.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/mixed_locale_metadata.md)

---

## Escalate

* If ΔS remains ≥ 0.60 after analyzer and normalization fixes, **split the index by language** or switch to a **multilingual embedding** and rebuild with correct metric.
  Open: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

**Next suggested page to generate**
`ProblemMap/GlobalFixMap/LanguageLocale/nonstandard_whitespace.md`
Focus on NBSP, NNBSP, thin-space, zero-width joiner/non-joiner, and their impact on retrieval.

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
