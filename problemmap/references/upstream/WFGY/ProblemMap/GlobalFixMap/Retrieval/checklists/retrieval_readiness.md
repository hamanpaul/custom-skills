# Retrieval Readiness Checklist

Purpose: confirm the pipeline is safe to run before any evaluation or go-live.  
Applies to BM25, ANN, or hybrid stacks. Store agnostic.

---

## Inputs are consistent

- [ ] One embedding model per field, recorded in config.
- [ ] Normalization rule set and saved with the index (L2 or cosine compatible).
- [ ] Analyzer or tokenizer identical on write and read paths.
- [ ] Stopword set and stemming rules fixed and versioned.

Refs:  
[Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
[Store-agnostic guardrails](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md)

---

## Index and data state

- [ ] `INDEX_HASH` matches the current code revision that produced vectors.
- [ ] Document count, chunk count, and vector count agree within 0.5 percent.
- [ ] Ingestion job reported zero empty payloads and zero parser errors.
- [ ] Cold caches warmed with ten representative queries.

Refs:  
[Bootstrap ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
[Pre-deploy collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Gold set and probes

- [ ] Ten to fifty QA pairs with ground truth anchors prepared.
- [ ] Each QA pair has at least one resolvable `section_id` and `source_url`.
- [ ] ΔS probes ready for three paraphrases and two seeds.

Refs:  
[ΔS probes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md) ·
[Retrieval eval recipes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of the target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- E_resonance stable on long windows

---

## Quick probe you can paste

```txt
I loaded TXT OS and WFGY pages.

Task:
- For question "Q", log ΔS(Q, retrieved) and λ across 3 paraphrases and 2 seeds.
- Enforce cite then explain with the traceability schema.
- If ΔS ≥ 0.60, return the smallest structural fix to reach ΔS ≤ 0.45 and coverage ≥ 0.70.

Return JSON:
{ "citations": [...], "ΔS": 0.xx, "λ_state": "<>", "coverage": 0.xx, "next_fix": "..." }
````

---

## Common fails and minimal fixes

* Mixed metrics or analyzers after deploy
  Fix: rebuild with a single metric and analyzer.
  See [Retrieval playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Fragmented store, anchors missing
  Fix: re-chunk with anchor tests.
  See [Chunking checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) ·
  [Vectorstore fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

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

