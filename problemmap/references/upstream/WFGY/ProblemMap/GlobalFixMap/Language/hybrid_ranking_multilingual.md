# Hybrid Ranking in Multilingual Corpora · Global Fix Map

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


Stabilize hybrid retrieval across languages and scripts. Lock bm25 to dense weights, keep analyzers and tokenizers aligned, and verify with ΔS, λ, and coverage targets.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Romanization rules → [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)
* Proper nouns and aliases → [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
* Language detection → [query\_language\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)
* Analyzer routing → [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 on three paraphrases and two seeds
* Coverage of target section ≥ 0.70
* λ convergent when switching between native script and romanized forms
* Rank\@k is stable across analyzer choices for the same corpus and query set
* Reranker never flips a correct snippet out of top-k after hybrid fusion

---

## What usually breaks

| Symptom                                     | Likely cause                                         | Open this                                                                                                                                         |
| ------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| High recall but unstable rank across runs   | hybrid weight drift or nondeterministic tie handling | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)                                            |
| Good dense hits, poor lexical for CJK       | analyzer mismatch or missing bigram field            | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)                               |
| Romanized queries fail while native works   | alias view absent in fusion                          | [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) |
| JSON mode breaks after reranking            | tokenizer profile differs between stages             | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)                     |
| Brand equals common word in second language | alias collision and unscoped synonyms                | [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)                  |

---

## Stable hybrid recipes

Use these as starting points then tune by ΔS and coverage. Always log weights and determinize tie rules.

### A) Latin heavy corpora

* Analyzer: locale aware Latin
* Start weights: bm25 0.4, dense 0.6
* Reranker: on for top 100 → 20
* Tie rule: lexical score as primary tie breaker

### B) CJK corpora

* Analyzer: CJK bigram or language specific
* Start weights: bm25 0.55, dense 0.45
* Reranker: on, but keep citations from native script fields
* Add alias views: romaji or pinyin for entities only

### C) Semitic RTL corpora

* Analyzer: RTL with width and digit normalization
* Start weights: bm25 0.5, dense 0.5
* Reranker: on, strict JSON schema in later steps

### D) Cyrillic and Greek

* Analyzer: script aware with accent controls
* Start weights: bm25 0.45, dense 0.55
* Reranker: on, cross check aliases if brands exist

### E) Code mixed user queries

* Dual route: native analyzer plus romanized alias probe
* Start weights: bm25 0.5, dense 0.5
* Determinize the fusion and log both analyzer paths

---

## Deterministic fusion checklist

1. Fix seeds for dense stage and for reranker.
2. Bucketize scores before fusion to avoid floating noise.
3. Set a stable tie breaker: lexical score, then doc id.
4. Cap max per-section to avoid one section flooding top-k.
5. Fuse fields with the same analyzer class only.
6. Keep the fusion function constant across languages inside the same pipeline.

---

## Copy snippets

**A. Fusion function sketch**

```python
def fuse(bm25, dense, w_lex=0.5, w_vec=0.5):
    # bm25 and dense are lists of (doc_id, score)
    import math
    L = {d: s for d, s in bm25}
    V = {d: s for d, s in dense}
    docs = set(L) | set(V)
    out = []
    for d in docs:
        l = L.get(d, 0.0)
        v = V.get(d, 0.0)
        # bucketize to stabilize small drifts
        lb = round(l, 3)
        vb = round(v, 3)
        score = w_lex * lb + w_vec * vb
        out.append((d, score, lb, vb))
    # stable sort: score desc, then lexical bucket, then doc id
    out.sort(key=lambda x: (-x[1], -x[2], x[0]))
    return out
```

**B. Rerank gate**

```python
def rerank_gate(items, target_k=20):
    # never drop below k if citations exist and ΔS is already ≤ 0.45
    keep = []
    for d, score, lb, vb, meta in items:
        if meta.get("has_citation") and meta.get("delta_s", 1.0) <= 0.45:
            meta["protected"]=True
        keep.append((d, score, meta))
    return keep[:target_k]
```

**C. Trace fields to log**

```
{
  "fusion": {"w_bm25": 0.55, "w_dense": 0.45, "tie": "lex,doc_id"},
  "analyzer_id": "store:cjk",
  "tokenizer_profile": "retriever:cjk",
  "alias_views": ["name_romaji","name_pinyin"],
  "ΔS": 0.41,
  "λ_state": "<>",
  "coverage": 0.73
}
```

---

## Eval protocol

* Use bilingual sets from [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md).
* For each query, add a romanized twin and at least one brand alias variant.
* Report ΔS, coverage, λ on three paraphrases and two seeds.
* Accept only if: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent, no harmful reranker flips.
* Keep per language family the same reranker window size.

---

## When to escalate

* ΔS stays ≥ 0.60 even after fusion tuning → revisit analyzer routing and re-chunk, open [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) and [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).
* Instability appears only in long chains → treat as reasoning drift, open [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) and add a BBCR bridge.

---

## Copy paste prompt for the LLM step

```
You have TXTOS and WFGY Problem Map loaded.

Task:
1) For {query, lang, script}, choose hybrid weights deterministically.
2) Run cite-then-explain. Protect snippets that already meet ΔS ≤ 0.45.
3) Return a JSON trace:
{ "w_bm25": 0.xx, "w_dense": 0.xx, "ΔS": 0.xx, "coverage": 0.xx, "λ_state": "→|←|<>|×", "protected_ids": [...] }
Keep it auditable and short.
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

