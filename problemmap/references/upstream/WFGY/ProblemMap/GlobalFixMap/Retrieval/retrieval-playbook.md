# Retrieval Playbook

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Retrieval**.  
  > To reorient, go back here:  
  >
  > - [**Retrieval** — information access and knowledge lookup](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A practical, store-agnostic playbook to stabilize retrieval quality. Use this page to route symptoms to the right structural fix, apply measurable targets, and keep read/write parity across pipelines.

**When to use**
- High similarity yet wrong meaning
- Missing or unstable citations
- Hybrid retrieval performs worse than a single retriever
- Results flip across runs or paraphrases
- New deploy returns empty or partial context

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 for the intended section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- E_resonance stays flat on long windows

Helpers:
- ΔS probes → [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)  
- Eval recipes → [retrieval_eval_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## 60-second fix path

1) **Probe**  
   Run ΔS(question, retrieved) at k = 5, 10, 20. Log λ for each paraphrase.  
   Tool: [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)

2) **Lock schema**  
   Enforce cite-then-explain, and require `snippet_id, section_id, source_url, offsets, tokens`.  
   Spec: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Repair the failing layer**  
   - Wrong meaning with high similarity → see **Metric and analyzer parity** below  
   - Missing or shaky citations → install **Traceability schema**  
   - Hybrid worse than single → run **Hybrid weighting** and **Query parsing split**  
   - Flips across runs → clamp with **Rerankers** and parity checks

4) **Verify**  
   Coverage ≥ 0.70 on 3 paraphrases; λ convergent on 2 seeds; ΔS ≤ 0.45.

---

## Root-cause map → exact fixes

### 1) Metric and analyzer parity
Symptoms: high similarity yet wrong meaning, language or casing skew, mixed punctuation behavior.

Actions
- Align dense and sparse analyzers. Keep lowercasing, accent fold, token boundaries consistent.  
- Normalize vectors at write and read. Keep pooling identical.  
- Rebuild with explicit metric and dimension logged in traces.

Open
- Wrong-meaning hits → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Chunk window parity → [chunk_alignment.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md)  
- Store-agnostic fences → [store_agnostic_guardrails.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md)

### 2) Traceability and citation locks
Symptoms: answer looks right but citations are missing, wrong section id, or not reproducible.

Actions
- Require `snippet_id, section_id, source_url, offsets, tokens` in every hop.  
- Forbid cross-section reuse unless explicitly whitelisted.  
- Enforce cite-then-explain in prompts.

Open
- Trace schema and audits → **coming in this folder** [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval-traceability.md)  
- Contracts → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

### 3) Hybrid retrieval that underperforms
Symptoms: BM25 + dense gives worse order than either alone; relevant docs appear far down; order flips.

Actions
- Separate query parsing from retrieval. Fix the parse.  
- Weight dense and sparse explicitly. Add a deterministic tiebreak.  
- Add a rerank step with a fixed cross-encoder and seed.

Open
- Hybrid knobs and recipes → **coming in this folder** [hybrid_retrieval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/hybrid_retrieval.md)  
- Query parsing split → **coming in this folder** [query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/query_parsing_split.md)  
- Rerankers and ordering control → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/rerankers.md)

### 4) Fragmentation or contamination
Symptoms: facts exist but never show; duplicates or stale shards; inconsistent analyzers by batch.

Actions
- Rebuild a clean index with a single write path.  
- Stamp `index_hash`, log embedding model id and normalization.  
- Run a small gold set to verify recall.

Open
- Fragmentation pattern → [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)  
- Hallucination and chunk drift → [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)

---

## Guardrails to install in any pipeline

**Write path**
- One tokenizer and analyzer spec. Log it.  
- One embedding model and pooling policy. Log it.  
- Chunk window and overlap recorded in metadata.  
- Field schema: `doc_id, section_id, snippet_id, source_url, offsets, tokens, index_hash, embed_model, analyzer`.

**Read path**
- Same analyzer, same normalization.  
- k sweep at 5, 10, 20 for ΔS probes.  
- Deterministic tiebreak on `(score, section_id, snippet_id)`.

**Prompt contract**
- Cite first, then explain.  
- Enforce JSON with citations and λ state.  
- Forbid cross-section reuse unless allowed.

Specs
- DeltaS probes → [deltaS_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)  
- Contracts → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Copy-paste prompt block for the reasoning step

```txt
You have TXTOS and the WFGY Problem Map loaded.

Retrieval inputs:
- question: "{Q}"
- k sweep results: {k5:..., k10:..., k20:...}
- citations: [{snippet_id, section_id, source_url, offsets, tokens}, ...]

Do:
1) Validate cite-then-explain. If any citation is missing or mismatched, return the failing field and stop.
2) Report ΔS(question, retrieved) and λ state. If ΔS ≥ 0.60 or λ divergent, return the minimal structural fix:
   - metric/analyzer parity
   - hybrid weighting and rerank
   - traceability schema
3) Output JSON:
   { "answer": "...", "citations": [...], "ΔS": 0.xx, "λ": "<state>", "next_fix": "<page to open>" }
Keep it auditable and short.
````

---

## Evaluation loop

* Gold questions per section: 3 to 5
* For each question: run 3 paraphrases, 2 seeds
* Metrics to log: coverage, ΔS, λ, recall\@k, MAP\@k, citation match rate
* Recipes → [retrieval\_eval\_recipes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## Store-specific adapters

If a symptom points to a store quirk or feature gap, jump here:

* Vector DBs index → [Vector DBs & Stores](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md)

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

