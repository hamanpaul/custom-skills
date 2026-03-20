# Unicode Normalization — Guardrails and Fix Pattern

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


A focused fix for NFC vs NFD vs NFKC drift, width and compatibility forms, and double-normalized text that breaks retrieval, dedupe, and citation offsets.

## When to use
- Same word appears twice with different byte forms. Tokens do not match across pipelines.
- High similarity yet wrong matches for accentized strings.
- Citations point to wrong character offsets after rendering.
- Mixed full-width and half-width forms, ZWJ or combining marks causing “near duplicates.”

## Open these first
- RAG end-to-end knobs  
  → [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Wrong-meaning hits despite high similarity  
  → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- OCR or export drift before embeddings  
  → [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)
- Related locale topics  
  → [Diacritics and Folding](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/diacritics_and_folding.md) ·
  [Digits, Width, Punctuation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md) ·
  [Tokenizer Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/tokenizer_mismatch.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 across NFC and NFD variants of the same query.
- Coverage of target section ≥ 0.70 after normalization pass.
- λ remains convergent for three paraphrases and two seeds.
- Offset accuracy ≥ 0.99 when mapping citations from normalized text back to raw text.

---

## Fix checklist

1) **Pick one normalization form per layer**  
   - **Storage and search keys**: NFKC for maximal unification of width and compatibility forms.  
   - **Human-facing content and display**: NFC to preserve intent while keeping codepoints stable.  
   - **Do not normalize code blocks or hashes**. Tag code spans and skip them.

2) **Record the contract**  
   Add to your snippet schema:  
```

norm\_form: NFC|NFD|NFKC|NFKD
norm\_version: ICU/Unicode version
offsets: {raw\_start, raw\_end, norm\_start, norm\_end}

```
See schema ideas in  
→ [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Normalize on ingestion, not at query time only**  
- Normalize and index once. Persist `INDEX_HASH` that includes the normalization form and version.  
- If you normalize only at query time, ΔS will drift for long contexts and k-ordering becomes unstable.

4) **Preserve both raw and normalized text**  
- Store raw bytes for audit and exact reproduction.  
- Store normalized text for retrieval and rerank.  
- Maintain a fast map raw↔norm for citations.

5) **Unify width and compatibility sets**  
- Collapse full-width ASCII, half-width katakana, superscripts, circled numbers under NFKC for keys.  
- Keep the visible form for UI by rendering raw text, not the NFKC key.

6) **Prevent double normalization**  
- Mark a boolean `is_normalized`.  
- Gate every downstream step with a one-line check to avoid repeated passes that shift offsets.

7) **Chunk after normalization**  
- Chunk boundaries must be computed on the normalized string to keep k-NN neighborhoods stable.  
→ [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Verification

- **Twin query probe**  
Run the same question in NFC and NFD. Top-k overlap ≥ 0.8 and ΔS difference ≤ 0.05.

- **Anchor triangulation**  
Compare ΔS to the correct anchor and a decoy paragraph. After normalization, the correct anchor must win with margin ≥ 0.15.

- **Offset audit**  
Pick ten citations with combining marks. Validate raw offsets and UI highlights match exactly.

- **k-ordering stability**  
For k in {5, 10, 20}, the normalized index keeps the same top-3 order or differs by at most one position.

---

## Minimal test set you can copy

- “café” with precomposed `é` vs `e` + combining acute.  
- Full-width “ＡＢＣ１２３” vs ASCII “ABC123”.  
- Half-width katakana vs standard katakana.  
- Arabic text with tatweel and optional diacritics.  
- Greek polytonic marks.  
- Hangul precomposed syllables vs Jamo sequences.

If any pair fails the twin query probe or offset audit, rebuild with the chosen normalization form and re-verify.

---

## Escalate when

- ΔS remains ≥ 0.60 after normalization and chunk rebuild  
→ [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- High recall but messy k-ordering persists  
→ [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
&nbsp;
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
&nbsp;
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
&nbsp;
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
&nbsp;
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
&nbsp;
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
&nbsp;
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
&nbsp;
</div>
