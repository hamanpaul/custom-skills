# Query Routing and Analyzers · Global Fix Map

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


Bind detected `lang` and `script` to the right analyzer, tokenizer, and alias views. Keep the retriever, reranker, and LLM tokenizer in agreement so ΔS and λ stay stable across paraphrases and seeds.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts in one query → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Proper noun aliases → [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
* Romanization rules → [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)
* Language detection → [query\_language\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 across three paraphrases and two seeds
* Coverage of target section ≥ 0.70
* λ remains convergent when the same question is asked in native script and in romanized form
* Analyzer choice and LLM tokenizer profile are logged and consistent across runs
* No rank flip after switching analyzers on the same corpus

---

## Minimal routing contract

**Detector input and result** from [query\_language\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md) gives:

```
lang, script, confidence, romanized_suspect, variants[]
```

**Routing decision** must produce:

```
analyzer_id          # store analyzer for full-text field
tokenizer_profile    # retriever or LLM tokenizer profile name
alias_views          # which alias fields to probe (romanized, synonyms_local)
hybrid_weights       # bm25:vector ratio, or reranker on/off
notes                # short rationale for audit
```

You must log these five fields in the retrieval trace item along with ΔS and λ.

---

## Store routing matrix

These are stable patterns, not vendor endorsements. Use them to avoid metric and analyzer mismatches.

| Script                | Primary choice                                    | Alias view for romanized      | Notes and links                                                                                                                                                       |
| --------------------- | ------------------------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Latn                  | locale aware analyzer with ICU folding            | none or localized synonyms    | Keep case and diacritics decisions consistent. See [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md). |
| Han, Hira, Kana, Hang | language specific analyzer or CJK bigram analyzer | `title_romaji`, `name_pinyin` | Mix of bigram and dictionary analyzers is fine if logged and deterministic.                                                                                           |
| Cyrl                  | Cyrillic aware analyzer                           | optional translit alias       | Keep transliteration only as alias view. Do not replace canonical text.                                                                                               |
| Arab, Hebr            | RTL analyzer with width and bidi guards           | optional translit alias       | Normalize digits and punctuation for the detector step only.                                                                                                          |
| Mixed scripts         | two analyzers in parallel                         | romanized alias true          | Enforce cite then explain in the answer. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).          |

Store specifics you can cross check:

* Elasticsearch guide → [elasticsearch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md)
* Typesense guide → [typesense.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/typesense.md)
* Vespa guide → [vespa.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/vespa.md)

---

## Typical failure → exact fix

| Symptom                                                     | Likely cause                                                  | Open this                                                                                                                                                                                                            |
| ----------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| High similarity yet wrong meaning after switching analyzers | metric and analyzer mismatch                                  | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Good recall but unstable rank in CJK                        | mixing bigram and dictionary analyzers without a fence        | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)                                                                                                  |
| JSON mode breaks when analyzer changes                      | tokenizer profile not aligned with LLM’s expected JSON tokens | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)                                                                                        |
| Romanized search finds no evidence                          | alias views missing or disabled                               | [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)                                                                    |
| Brand name equals common word in another language           | alias collision and unscoped synonyms                         | [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)                                                                                     |

---

## 60 second routing plan

1. **Script first.** Use the detector output. If `confidence < 0.65`, route both native analyzer and romanized alias.
2. **Lock tokenizer.** Choose a tokenizer profile that matches your retriever model and your LLM. Log it.
3. **Hybrid weights.** Start with bm25\:vector at 0.4:0.6 and move by 0.1 until ΔS ≤ 0.45.
4. **Cite then explain.** Force snippet fields in the native script when possible.
5. **Regression gate.** Require coverage ≥ 0.70 on three paraphrases before deploy.

---

## Copy snippets

**A. Router skeleton**

```python
def choose_route(det):
    routes = []
    if det["script"] in ["Han","Hira","Kana","Hang"]:
        routes.append({
            "analyzer_id": "store:cjk",
            "tokenizer_profile": "retriever:cjk",
            "alias_views": ["name_romaji","name_pinyin"],
            "hybrid_weights": [0.4, 0.6],
            "notes": "cjk primary"
        })
    elif det["script"] == "Cyrl":
        routes.append({
            "analyzer_id": "store:cyrl",
            "tokenizer_profile": "retriever:default",
            "alias_views": ["name_translit"],
            "hybrid_weights": [0.5, 0.5],
            "notes": "cyrillic"
        })
    elif det["script"] == "Arab":
        routes.append({
            "analyzer_id": "store:rtl",
            "tokenizer_profile": "retriever:default",
            "alias_views": ["name_translit"],
            "hybrid_weights": [0.5, 0.5],
            "notes": "rtl"
        })
    else:
        routes.append({
            "analyzer_id": "store:latn",
            "tokenizer_profile": "retriever:default",
            "alias_views": [],
            "hybrid_weights": [0.4, 0.6],
            "notes": "latin"
        })

    if det["confidence"] < 0.65 or det.get("romanized_suspect"):
        # add romanized alias probe for safety
        for r in routes:
            r["alias_views"] = sorted(set(r["alias_views"] + ["aliases_romanized"]))
            r["notes"] += " + alias probe"
    return routes
```

**B. Elasticsearch style mapping sketch**

```json
{
  "mappings": {
    "properties": {
      "body":   { "type": "text", "analyzer": "cjk" },
      "title":  { "type": "text", "analyzer": "cjk" },
      "name_pinyin": { "type": "text", "analyzer": "icu_analyzer" },
      "name_romaji": { "type": "text", "analyzer": "icu_analyzer" },
      "aliases_romanized": { "type": "text", "analyzer": "icu_analyzer" },
      "section_id": { "type": "keyword" }
    }
  }
}
```

**C. Typesense style fields**

```json
{
  "name": "docs",
  "fields": [
    {"name":"body","type":"string","locale":"zh"},
    {"name":"title","type":"string","locale":"zh"},
    {"name":"aliases_romanized","type":"string[]","locale":"en"},
    {"name":"section_id","type":"string","facet":true}
  ]
}
```

**D. Vespa schema sketch**

```
schema docs {
  document docs {
    field body type string { indexing: summary | index }
    field title type string { indexing: summary | index }
    field aliases_romanized type array<string> { indexing: summary | index }
  }
  fieldset default { fields: body, title }
  rank-profile default { first-phase { expression: bm25(body) + bm25(title) } }
}
```

---

## Eval plan

* Use the sets from [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md).
* Add pairs of queries in native script and romanized forms for the same entity.
* Targets: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent on two seeds.
* If rank flips between analyzers, clamp with a deterministic reranker and verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## When to escalate

* ΔS stays ≥ 0.60 after analyzer swap → rebuild index with fixed analyzer and verify metric in [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).
* Instability only in long chains → treat as reasoning issue and apply BBCR bridge, see [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).

---

## Copy paste prompt for the LLM step

```
You have TXTOS and the WFGY Problem Map loaded.

Given detector output {lang, script, confidence, romanized_suspect}:
1) Choose analyzer and tokenizer profile deterministically.
2) If confidence < 0.65 or romanized_suspect=true, search the romanized alias view as well.
3) Cite-then-explain from the native script snippet when possible.
4) Return a JSON trace:
{ "analyzer_id": "...", "tokenizer_profile": "...", "alias_views": [...], "ΔS": 0.xx, "λ_state": "→|←|<>|×" }
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

