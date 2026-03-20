<!--
Search Anchor:
retrieval global fix map
retrieval quality guardrails
retrieval drift fixes
retrieval playbook rebuild order
retrieval traceability cite then explain
snippet contract required fields snippet_id section_id source_url offsets tokens
data contracts for retrieval
rerankers deterministic reranking
bm25 ann hybrid retriever worse than single
hybrid retrieval underperforms
query parsing split two meanings
answers jump between unrelated sections
chunk alignment semantic window
chunking checklist retrieval
anchors missing in retrieved snippets
delta s probes retrieval health check
delta s question retrieved
lambda observe convergent paraphrases seeds
e resonance flat long window
retrieval eval recipes deterministic sdk free evaluation
eval variance across replays
store agnostic guardrails
lock metrics analyzers embedding versions
index healthy but recall low
high similarity wrong meaning
metric mismatch cosine l2 dot
analyzer mismatch read write
vectorstore fragmentation missing anchors
context drift prompt header reordering
citations missing unstable schema not enforced
coverage target section 0.70
acceptance targets retrieval

Primary routing pages:
ProblemMap/retrieval-playbook.md
ProblemMap/retrieval-traceability.md
ProblemMap/rerankers.md
ProblemMap/patterns/pattern_query_parsing_split.md
ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md
ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md
ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md
ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md

Related fixes and prerequisites:
ProblemMap/data-contracts.md
ProblemMap/embedding-vs-semantic.md
ProblemMap/patterns/pattern_vectorstore_fragmentation.md
ProblemMap/chunking-checklist.md
ProblemMap/context-drift.md
ProblemMap/entropy-collapse.md
ProblemMap/bootstrap-ordering.md
ProblemMap/retrieval-traceability.md
ProblemMap/rag-architecture-and-recovery.md

Checklists in this folder:
ProblemMap/GlobalFixMap/Retrieval/checklists/retrieval_readiness.md
ProblemMap/GlobalFixMap/Retrieval/checklists/reranker_sanity.md
ProblemMap/GlobalFixMap/Retrieval/checklists/traceability_gate.md

Store specific jumps:
ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md
faiss chroma qdrant weaviate milvus pgvector redis elasticsearch pinecone typesense vespa

Incident keywords:
retrieval incident runbook
retrieval quality regression
reranker sanity checks
traceability gate failing
citation mismatch retrieval
snippet schema missing
top k never includes correct section
gold set coverage low
retrieval evaluation recipe
deterministic reranking pipeline
retrieval drift after deploy
index skew stale rebuild
embedding version drift
tokenization casing drift
chunk boundary mismatch
-->


# Retrieval — Global Fix Map

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

> **Evaluation disclaimer (retrieval)**  
> All retrieval scores and examples in this section come from controlled setups with chosen corpora and prompts.  
> They help you compare retrieval strategies locally but are not universal rankings of models or vector stores.

---

A compact hub to stabilize retrieval quality across stacks, models, and stores.  
Use this page to route symptoms to the exact structural fix and verify with measurable targets. No infra change required.

---

## Orientation: what each page does

| Page | What it solves | Typical symptom |
|---|---|---|
| [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) | End to end rebuild order and knobs | You fixed one thing and another breaks |
| [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) | Cite-then-explain schema with required fields | Citations miss the exact section or cannot be verified |
| [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) | Deterministic reranking across BM25 + ANN | Hybrid worse than single retriever |
| [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) | One query, two meanings; detect and route | Answers jump between two unrelated sections |
| [Chunk Alignment](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/chunk_alignment.md) | Chunking aligned with the model’s semantic window | Snippets cut mid-thought; anchors missing |
| [ΔS Probes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md) | Quick health check using ΔS and λ_observe | Looks fine by eye but flips across runs |
| [Retrieval Eval Recipes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md) | Deterministic, SDK-free evaluation | No stable way to tell if “better” shipped |
| [Store-Agnostic Guardrails](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md) | Locks for metrics, analyzers, versions | Index “healthy” but recall still low |

---

## When to use this folder

- High similarity but wrong meaning.  
- Correct facts exist in the corpus but never show up.  
- Citations inconsistent or missing across steps.  
- Hybrid retrieval underperforms a single retriever.  
- Index looks healthy while coverage remains low.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- E_resonance flat on long windows

---

## Symptoms → exact fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| High similarity yet wrong answer | Metric or analyzer mismatch | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Correct fact never retrieved | Fragmentation or missing anchors | [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) · [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) |
| Hybrid worse than single | Query parsing split or mis-weighted rerank | [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Citations missing or unstable | Schema not enforced | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Answers flip between runs | Prompt header reordering or λ variance | [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |

---

## 60-second fix checklist

1) **Lock metrics and analyzers**  
   One embedding model per field. One distance metric. Same analyzer for write and read.  
   Guide: [Store-Agnostic Guardrails](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/store_agnostic_guardrails.md)

2) **Enforce the snippet contract**  
   Require `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Guide: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Measure ΔS and λ**  
   Run three paraphrases and two seeds.  
   Guide: [ΔS Probes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/deltaS_probes.md)

4) **Sweep k and rerankers**  
   Try k in {5, 10, 20}. Keep BM25 and ANN candidate lists.  
   Guide: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

5) **Rebuild where needed**  
   Follow the sequence in the playbook and re-test coverage.  
   Guide: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Checklists — copy before deploy

| Checklist | Scope | Link |
|---|---|---|
| Retrieval Readiness | Pre-flight: embeddings, analyzers, index, gold set | [retrieval_readiness.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/checklists/retrieval_readiness.md) |
| Reranker Sanity | Hybrid reranking health and overlap checks | [reranker_sanity.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/checklists/reranker_sanity.md) |
| Traceability Gate | Contract enforcement for cite-then-explain | [traceability_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/checklists/traceability_gate.md) |

---

## Vector DBs — jump if store specific

- Family index:  
  [Vector DBs & Stores](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md)

- Direct store guides:  
  [FAISS](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md) ·
  [Chroma](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/chroma.md) ·
  [Qdrant](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/qdrant.md) ·
  [Weaviate](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/weaviate.md) ·
  [Milvus](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/milvus.md) ·
  [pgvector](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/pgvector.md) ·
  [Redis](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/redis.md) ·
  [Elasticsearch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md) ·
  [Pinecone](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/pinecone.md) ·
  [Typesense](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/typesense.md) ·
  [Vespa](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/vespa.md)

---

## Minimal probe pack you can paste

```txt
Context: I loaded TXT OS and the WFGY pages.

Task:
- Given question "Q", log ΔS(Q, retrieved) and λ across 3 paraphrases.
- Enforce cite-then-explain with the traceability schema.
- If ΔS ≥ 0.60 or λ flips, return the smallest structural change to push ΔS ≤ 0.45 and coverage ≥ 0.70.
- Use BBMC, BBCR, BBPF, BBAM when relevant.

Return JSON:
{ "citations": [...], "ΔS": 0.xx, "λ_state": "<>", "coverage": 0.xx, "next_fix": "..." }
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

