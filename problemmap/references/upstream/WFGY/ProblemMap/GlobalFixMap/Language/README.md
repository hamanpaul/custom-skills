<!--
Search Anchor:
language and multilingual global fix map
cross lingual retrieval
cross language retrieval
multilingual rag problems
bilingual corpus retrieval issues
mixed script corpus
mixed language query
code switching queries
code switched prompt
cjk thai indic languages
rtl languages arabic hebrew
cyrillic search issues
accented latin letters
non latin script recall low
high similarity but wrong meaning multilingual
multilingual hybrid retrieval worse than single
index healthy but low coverage for cjk
zh hans and zh hant never co retrieve
thai recall suddenly drops
korean jamo or particles missing
japanese segmentation problems
wordpiece bpe tokenizer mismatch

Typical multilingual bugs:
query in english answer in wrong local language
question translated but citations jump section
answer quotes wrong paragraph after translation
mixed latin plus cjk query under recall
proper noun aliases flip between local and english
romanization vs transliteration mismatch
brand names oscillate between scripts
language detection flips per run
search analyzer and index analyzer not aligned
reranker mono lingual on multi lingual corpus
negations removed by stopwords
particles or unit words dropped by morphology
accent stripping changes meaning
width normalization not applied
half width full width inconsistent
unicode normalization inconsistent
diacritics dropped or duplicated
locale drift in logs vs index

When to use this folder:
bilingual faq site
global product docs
support center in many languages
developer docs in english plus local language
cjk manual plus english index
arabic or hebrew rtl knowledge base
indic language content with mixed scripts
logs or tickets mixing english and local language
user queries with frequent code switching
chatbot that must answer in user language but cite english docs

Languages covered (examples):
english en
simplified chinese zh hans
traditional chinese zh hant
japanese ja
korean ko
thai th
vietnamese vi
hindi hi
bengali bn
arabic ar
hebrew he
russian ru
ukrainian uk
turkish tr
polish pl
spanish es
portuguese pt
french fr
german de
italian it
indonesian id
malay ms
tagalog tl

Key metrics:
delta s question retrieved <= 0.45 across languages
coverage of intended section >= 0.70 after repair
lambda observe convergent across 3 paraphrases and 2 seeds
e_resonance flat on long mixed script windows
citation fields complete and stable
alias noise does not leak into evidence
language detection contract stable
query routing and analyzers deterministic

Core pages in this folder:
ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md
ProblemMap/GlobalFixMap/Language/script_mixing.md
ProblemMap/GlobalFixMap/Language/locale_drift.md
ProblemMap/GlobalFixMap/Language/multilingual_guide.md
ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md
ProblemMap/GlobalFixMap/Language/romanization_transliteration.md
ProblemMap/GlobalFixMap/Language/query_language_detection.md
ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md
ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md
ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md
ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md
ProblemMap/GlobalFixMap/Language/code_switching_eval.md
-->

<!--
Related structural fixes:
ProblemMap/embedding-vs-semantic.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/context-drift.md
ProblemMap/patterns/pattern_query_parsing_split.md
ProblemMap/GlobalFixMap/Retrieval/README.md
ProblemMap/GlobalFixMap/Embeddings/README.md
ProblemMap/GlobalFixMap/Chunking/README.md
ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md
-->

<!--
Language patterns and scenarios:
query: chinese question english docs
query: english question chinese docs
query: japanese question english and japanese docs
query: thai ui labels with english logs
query: spanish product name english manual
query: arabic faq english knowledge base
query: cjk code switching with english error message
query: local name plus english acronym
pattern: user asks in local language wants local answer
pattern: user asks in english wants citations in local docs
pattern: product or brand has many spellings
pattern: same entity across scripts and romanization
pattern: eval set for bilingual and code switching
-->

<!--
Cross folder jumps:
ProblemMap/GlobalFixMap/Language/README.md
ProblemMap/GlobalFixMap/Retrieval/README.md
ProblemMap/GlobalFixMap/Embeddings/README.md
ProblemMap/GlobalFixMap/Chunking/README.md
ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md
ProblemMap/SemanticClinicIndex.md
-->


# Language & Multilingual · Global Fix Map

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

A compact hub to **stabilize cross-lingual retrieval and reasoning**.  
Use this folder when your corpus or queries include CJK, RTL, Indic, Cyrillic, accented Latin, or frequent code-switching. No infra change required.

---

## Orientation — pages and what they solve

| Page | What it solves | Typical symptom |
|------|----------------|-----------------|
| [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) | Locks tokenization and segmentation for CJK/Thai/Indic | High sim but low recall on CJK/Thai; broken tokens |
| [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) | One query carries mixed scripts and analyzers split | Mixed Latin+CJK queries under-recall or flip |
| [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) | Normalization for width/accents/variants (Hans↔Hant) | zh-Hans/zh-Hant never co-retrieve; accent variants miss |
| [multilingual_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md) | End-to-end recipes and acceptance targets | Unsure where drift comes from across languages |
| [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) | Alias shield for names, brands, products | Proper nouns oscillate across spellings |
| [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) | Romanization pairs and transliteration consistency | Inconsistent transliteration causes misses |
| [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md) | Stable language detection contract | Detection flips per run; routing becomes random |
| [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) | Route analyzers per language + parity w/ index | Search vs index behave differently |
| [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md) | Deterministic hybrid rerank across languages | Multilingual ranking unstable, hybrid < single |
| [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md) | Clamp stopwords/lemmatizers to protect meaning | Negations/particles vanish; unit words lost |
| [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md) | Controlled translation bridge with glossary | Local path ΔS stays high; glossary needed |
| [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md) | Bilingual & code-switch eval sets + checks | Cannot prove multilingual stability before ship |

---

## When to use this folder

- High similarity yet wrong meaning on bilingual or mixed-script corpora  
- Citations point to the wrong section after translating the question  
- Hybrid retrievers underperform a single retriever across languages  
- Index looks healthy while coverage stays low for non-Latin scripts  
- Names flip between native, transliteration, and English aliases  
- zh-Hans and zh-Hant never co-retrieve; Thai recall drops for no reason  

---

## Acceptance targets

- **ΔS(question, retrieved) ≤ 0.45** across language variants  
- **Coverage ≥ 0.70** to the intended section after repair  
- **λ_observe convergent** across 3 paraphrases and 2 seeds  
- **E_resonance flat** on long windows that mix scripts  
- Citation fields complete; alias noise does not leak into evidence  

---

## Map symptoms → structural fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| High similarity yet wrong meaning | Embedding not multilingual or pre-normalization mismatch | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Citations jump sections after translation | Snippet schema too loose | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| zh-Hans and zh-Hant never co-retrieve | Variant mapping and width rules missing | [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) |
| Thai or CJK recall collapses | Tokenizer mismatch or missing segmenter | [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) |
| Mixed Latin + CJK query under-recalls | Analyzer split across scripts | [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) |
| Hybrid worse than single | Query parsing split or mis-weighted rerank | [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Proper nouns oscillate | Missing alias fields and entity shield | [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) |
| Transliteration inconsistency | Romanization rules not aligned | [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) |
| Language detection drifts | Detection contract weak or unlocked | [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md) |
| Search vs index disagree | Analyzer routing error | [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md) |
| Ranking unstable across languages | Mono-lingual reranker or unaligned features | [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md) |
| Negations/particles vanish | Stopword or morphology too aggressive | [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md) |
| Persistent high ΔS on local path | Need glossary-backed translation bridge | [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md) |

---

## Fix in 60 seconds

1) **Detect language**  
   Emit stable language + confidence. If unstable, fix detection first.  
   → [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)

2) **Lock normalization and analyzers**  
   Keep locale, width, accents, and segmentation identical on write/read.  
   → [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) · [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)

3) **Protect entities and syntax**  
   Alias fields and romanization pairs; clamp stopwords/morphology for negations and units.  
   → [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) · [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) · [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)

4) **Stabilize ranking**  
   Use multilingual or dual-track rerank with deterministic ordering.  
   → [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)

5) **Translation bridge only if needed**  
   Pair with a glossary and keep native path as default.  
   → [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md)

6) **Verify**  
   With bilingual & code-switch sets confirm ΔS ≤ 0.45, Coverage ≥ 0.70, λ convergent.  
   → [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)

---

## Store-agnostic quick recipes

- Normalize the same way for corpus and queries before storing vectors  
- CJK/Thai require segmentation or bigrams; keep entity fields as keyword  
- If no multilingual embeddings, add a lexical sidecar and align features with a deterministic rerank

Got it — here’s the **English FAQ version** for the *Language & Multilingual · Global Fix Map* README. It follows the same style and clarity as the Chinese one, but rewritten in English for new users.

---

## FAQ — Common Questions (Language & Multilingual)

**Q1. Why does a bilingual or mixed query look similar but hit the wrong section?**  
A1. Most often the index and query use different analyzers or normalization steps, or CJK/Thai segmentation was never applied. Always lock the same normalization (width, accents, casing, segmentation) for both sides, then rebuild the index.  
Open: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) · [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)

**Q2. Why do zh-Hans and zh-Hant never co-retrieve?**  
A2. Variant and width rules are missing. Apply Unicode normalization, full/half-width mapping, and variant mapping before indexing.  
Open: [locale_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)

**Q3. After translating the question into English, citations jump to the wrong section.**  
A3. The citation schema is too loose, missing fields like `section_id` and `offsets`. Enforce snippet contracts and cite-then-explain.  
Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

**Q4. Why does Thai or Japanese recall fluctuate a lot?**  
A4. Classic tokenizer mismatch. Ensure index and query share the same segmenter; if not, use bigram or hybrid segmentation.  
Open: [tokenizer_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)

**Q5. Why do mixed Latin + CJK queries under-recall?**  
A5. The analyzer splits into two routes and weights unevenly. Script-aware splitting or fixed routing is needed.  
Open: [script_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md) · [query_routing_and_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)

**Q6. Why do proper nouns oscillate between native, romanized, and English aliases?**  
A6. Alias fields and romanization tables are missing. Add aliases and protect them with keyword fields.  
Open: [proper_noun_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) · [romanization_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)

**Q7. Why does multilingual reranking give different orderings each run?**  
A7. You are using a monolingual reranker or unaligned features. Switch to a multilingual reranker or dual-track (lexical+vector) with deterministic tie-breaks.  
Open: [hybrid_ranking_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)

**Q8. Should I enable translation bridging from the start?**  
A8. No. Always try the native language path first. Only enable when ΔS stays above 0.45 over time, and always with glossaries.  
Open: [fallback_translation_and_glossary_bridge.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/fallback_translation_and_glossary_bridge.md)

**Q9. Why do negations or particles disappear, flipping the meaning?**  
A9. Stopword or morphology rules are too aggressive. Protect negations, units, and structural particles.  
Open: [stopword_and_morphology_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)

**Q10. Why does language detection keep flipping and causing misrouting?**  
A10. The detection contract isn’t locked, or samples are too short. Set stable model, sample length, confidence threshold, and fallback paths.  
Open: [query_language_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)

**Q11. Metrics look fine but recall for non-Latin languages stays low.**  
A11. First check normalization and segmentation, then verify aliases/romanization and multilingual rerank alignment. Add code-switch eval sets for validation.  
Open: [multilingual_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md) · [code_switching_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)

**Q12. What is the minimum acceptance test?**  
A12. Run bilingual and code-switch eval sets. Confirm all:  
1) ΔS(question, retrieved) ≤ 0.45  
2) Coverage ≥ 0.70  
3) λ convergent.  
If not, debug in order: detection → normalization → entity protection → rerank → translation bridge.

**Q13. Is there a ready-to-paste diagnostic prompt?**  
A13. Yes. Use the following inside your LLM:  
```txt
You have TXTOS and the WFGY Problem Map loaded.

Task:  
- Given a bilingual question Q, measure ΔS(Q, retrieved) and λ across 3 paraphrases.  
- Verify index/query normalization (width, accents, casing, segmentation).  
- Enforce cite-then-explain. Protect entities with alias/romanization.  
- If ΔS ≥ 0.60 or λ flips, output minimal structural fix until ΔS ≤ 0.45, Coverage ≥ 0.70.

Return JSON:  
{ "citations":[...], "ΔS":0.xx, "λ_state":"<>|→|←|×", "coverage":0.xx, "next_fix":"..." }
````

**Q14. If I want to change the least, what’s the fix priority?**
A14. 1) Lock language detection contract  2) Lock normalization and analyzers  3) Add aliases/romanization  4) Multilingual rerank  5) Only then enable translation bridge.

**Q15. Accuracy improved, but rankings across languages still flip occasionally.**
A15. Add stable sort keys and fixed weight tables. Inject language features into rerankers and set deterministic tie-break rules.
Open: [hybrid\_ranking\_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)


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

