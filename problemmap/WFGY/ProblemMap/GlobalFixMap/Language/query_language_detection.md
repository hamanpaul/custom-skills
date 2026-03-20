# Query Language Detection · Global Fix Map

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


Detect the query language and script correctly, route it to the right analyzer and tokenizer, and keep λ stable across paraphrases. This page gives a small contract, deterministic fallbacks, and tests so short queries, code-switched inputs, and romanized forms do not break retrieval.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts in one query → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization and width/diacritics → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Proper noun aliases → [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
* Romanization and transliteration → [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)
* Multilingual overview → [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 across three paraphrases and two seeds
* Coverage of target section ≥ 0.70
* λ remains convergent when detector confidence is low or when code-switching is present
* Detector outputs BCP-47 `lang` and ISO 15924 `script` with an explicit confidence and rationale
* No false collapse when romanized forms are used instead of native script

---

## Minimal contract

**Inputs**

```
q_text              # user query raw
hints.lang_pref     # optional ui/user preference e.g. "ja"
hints.romanizer     # optional, e.g. "hepburn"
context.domain      # optional product/domain which biases vocabulary
```

**Detector output**

```
lang                # BCP-47 primary tag, null if unknown (e.g., "zh", "ja", "en")
script              # ISO 15924, e.g., "Hans", "Hant", "Latn", "Cyrl", "Arab"
confidence          # 0..1
rationale           # short note, e.g., "CJK bigram ratio 0.82"
variants            # list of plausible alternates, sorted by confidence
romanized_suspect   # bool, true if looks like transliteration of non-Latin
```

**Router decision**

```
analyzer_id         # store-specific analyzer to call
tokenizer_id        # LLM or retriever tokenizer profile
alias_view          # whether to search romanized alias field(s)
```

All five fields must be logged with the retrieval response so you can audit flips.

---

## Typical failure → exact fix

| Symptom                                                                   | Likely cause                                              | Open this                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Short query mis-detected as English, CJK missed                           | length bias without script probe                          | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md), [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)           |
| Romanized Japanese finds wrong page or no hit                             | detector returns `en+Latn` but romanized\_suspect not set | [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)                                                                                                |
| Arabic mixed digits and ASCII flips direction and rank                    | RTL controls and width not normalized                     | [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)                                                                                                                                |
| Brand or person whose alias equals a common word routes to wrong language | alias collision without scope fence                       | [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| High similarity yet wrong meaning across languages                        | analyzer or metric mismatch                               | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)      |

---

## 60-second fix checklist

1. **Two-stage detection**
   Script-first using Unicode ranges, then language model on normalized text. Never rely on language-only detectors for queries shorter than 6 tokens.

2. **Confidence bands**
   If `confidence < 0.65`, run mixed routing: search native analyzer for all `variants.script` plus the romanized alias view.

3. **Romanized suspect path**
   If `romanized_suspect=true`, search native-script alias view and bias reranker to prefer canonical snippets.

4. **Width and diacritics**
   Fold width and diacritics only for the detection step and alias view, not for canonical matching. See [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md).

5. **Log ΔS and λ**
   Keep per-variant logs so you can see which analyzer produced stable evidence.

---

## Copy snippets

**A. Script-first detector skeleton**

```python
import unicodedata as ud
from collections import Counter

def guess_script(s: str) -> tuple[str, float]:
    buckets = Counter()
    total = 0
    for ch in s:
        if ch.isspace() or ch.isdigit():
            continue
        total += 1
        name = ud.name(ch, "")
        # very light bins, expand as needed
        if "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name or "HANGUL" in name:
            buckets["CJK"] += 1
        elif "CYRILLIC" in name:
            buckets["CYRL"] += 1
        elif "ARABIC" in name or "HEBREW" in name:
            buckets["RTL"] += 1
        else:
            buckets["LATN"] += 1
    if total == 0:
        return "UNK", 0.0
    script, cnt = max(buckets.items(), key=lambda x: x[1])
    conf = cnt / total
    # map to ISO 15924 class
    iso = {"CJK":"Han", "CYRL":"Cyrl", "RTL":"Arab", "LATN":"Latn"}.get(script, "Zyyy")
    return iso, conf
```

**B. Romanized suspect heuristic**

```python
def is_romanized_suspect(q: str, script_iso: str) -> bool:
    # e.g., looks like "Tōkyō", "Toukyou", "Zhongguo", "Rossiya"
    if script_iso != "Latn":
        return False
    vowels = sum(ch.lower() in "aeiou" for ch in q)
    tone_marks = any(ch in "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ" for ch in q)
    hyphen = "-" in q
    long_vowel = any(seq in q.lower() for seq in ["ou","aa","ee","oo","uu"])
    return tone_marks or hyphen or long_vowel or vowels >= max(4, len(q)//3)
```

**C. Router decision**

```python
def route(q_text, hints):
    script, s_conf = guess_script(q_text)
    roman_sus = is_romanized_suspect(q_text, script)
    low_conf = s_conf < 0.65 or len(q_text.split()) < 6

    routes = []
    if script in ["Han", "Hira", "Kana", "Hang"]:
        routes.append(("analyzer:cjk", "tokenizer:cjk", False))
    elif script == "Cyrl":
        routes.append(("analyzer:cyrl", "tokenizer:default", False))
    elif script == "Arab":
        routes.append(("analyzer:rtl", "tokenizer:default", False))
    else:
        routes.append(("analyzer:latn", "tokenizer:default", roman_sus))

    if low_conf:
        # add alternates and alias view
        routes.append(("analyzer:latn", "tokenizer:default", True))
        routes.append(("analyzer:cjk", "tokenizer:cjk", True))
    return {
        "script": script,
        "confidence": round(s_conf, 2),
        "romanized_suspect": roman_sus,
        "routes": routes
    }
```

**D. Prompt fence for detectors**

```
You have TXTOS and the WFGY Problem Map.

When a query is short or mixed:
1) Detect script first. If confidence is low, search both native script and romanized alias views.
2) Cite the snippet in the canonical script if available. Use cite-then-explain.
3) Report {lang, script, detector_confidence, romanized_suspect} in the trace.
```

---

## Eval plan

Use the set from [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md). Add 3 extra buckets:

* short queries with 1 to 3 tokens
* romanized vs native for the same entity
* mixed ASCII and RTL digits

Targets

* detector accuracy on script ≥ 0.97 for length ≥ 6 tokens, ≥ 0.90 for length 1–5
* ΔS(question, retrieved) ≤ 0.45 and λ convergent across two seeds
* no rank flip between native and romanized when evidence matches

If recall is fine but ranking flips, clamp reranker and verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

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

