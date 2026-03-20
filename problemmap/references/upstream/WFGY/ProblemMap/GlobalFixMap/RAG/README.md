
<!--
Search Anchor:
rag global fix map
retrieval augmented generation failures
rag retrieval drift
rag hallucination with citations
citation break rag
cite then explain schema
hybrid retriever failure
bm25 ann reranker disagreement
index skew stale index
index healthy recall low
context drift rag
prompt header reorder rag
entropy collapse long chain rag
eval drift rag deterministic
rag eval variance replay
rag acceptance targets
delta s question retrieved
coverage target section
lambda observe convergent
three paraphrases two seeds
eval variance 5 replays

Core pages in this folder:
retrieval_drift -> GlobalFixMap/RAG/retrieval_drift.md
hallucination_rag -> GlobalFixMap/RAG/hallucination_rag.md
citation_break -> GlobalFixMap/RAG/citation_break.md
hybrid_failure -> GlobalFixMap/RAG/hybrid_failure.md
index_skew -> GlobalFixMap/RAG/index_skew.md
context_drift -> GlobalFixMap/RAG/context_drift.md
entropy_collapse -> GlobalFixMap/RAG/entropy_collapse.md
eval_drift -> GlobalFixMap/RAG/eval_drift.md

Symptom routing:
correct facts exist but not retrieved -> retrieval_drift + citation_break
citations unstable missing wrong snippet -> citation_break + ProblemMap/retrieval-traceability.md + ProblemMap/data-contracts.md
citations look right but answer invents -> hallucination_rag + prompt-injection defenses
hybrid worse than single -> hybrid_failure + query parsing split + reranker weights
high similarity wrong meaning -> embedding vs semantic + vectorstore fragmentation + metric mismatch
answers flip between runs -> context_drift + lambda variance clamp
chain grows never lands -> entropy_collapse + logic collapse guards
index healthy but recall low -> index_skew + build order + analyzer mismatch
eval scores noisy across replays -> eval_drift + deterministic eval path

Jump pages outside this folder:
ProblemMap/embedding-vs-semantic.md
ProblemMap/patterns/pattern_vectorstore_fragmentation.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/context-drift.md
ProblemMap/entropy-collapse.md
ProblemMap/retrieval-playbook.md
GlobalFixMap/VectorDBs_and_Stores/README.md
GlobalFixMap/VectorDBs_and_Stores/faiss.md
GlobalFixMap/VectorDBs_and_Stores/chroma.md
GlobalFixMap/VectorDBs_and_Stores/qdrant.md
GlobalFixMap/VectorDBs_and_Stores/weaviate.md
GlobalFixMap/VectorDBs_and_Stores/milvus.md
GlobalFixMap/VectorDBs_and_Stores/pgvector.md
GlobalFixMap/VectorDBs_and_Stores/redis.md
GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md
GlobalFixMap/VectorDBs_and_Stores/pinecone.md
GlobalFixMap/VectorDBs_and_Stores/typesense.md
GlobalFixMap/VectorDBs_and_Stores/vespa.md

Incident keywords:
rag incident
retrieval incident
reranker incident
hybrid incident
citation incident
hallucination incident
index rebuild incident
analyzer mismatch
metric mismatch cosine ip l2
top k recall low
coverage below threshold
delta s above 0.60
lambda flips across paraphrases
deterministic replay
gold set regression
-->


# RAG — Global Fix Map

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

A focused hub for **Retrieval Augmented Generation** failures.  
Use this folder when answers exist in the corpus but retrieval or evaluation drifts.  
Each page gives guardrails, measurable targets, and direct links to structural fixes. No infra change required.

---

## Orientation: what each page solves

| Page | What it fixes | Typical symptom |
|---|---|---|
| [retrieval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/retrieval_drift.md) | Keeps retrieve → rerank → reason aligned | Correct facts exist but never show up in the top k |
| [hallucination_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/hallucination_rag.md) | Blocks free text invention inside RAG | Citations look right but answer adds content not in source |
| [citation_break.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/citation_break.md) | Enforces cite then explain schema | Links point to the wrong snippet or disappear on retry |
| [hybrid_failure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/hybrid_failure.md) | Makes BM25 + ANN + reranker agree | Hybrid worse than a single retriever |
| [index_skew.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/index_skew.md) | Recovers broken or stale indexes | Index looks healthy yet recall is low |
| [context_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/context_drift.md) | Stabilizes header order and prompt state | Answers flip between runs with only header changes |
| [entropy_collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/entropy_collapse.md) | Caps chain growth and noise in long flows | Steps balloon, chain never lands |
| [eval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/eval_drift.md) | Makes eval runs deterministic | Metrics vary across identical replays |

---

## When to use this folder

- Correct facts exist in the corpus but never appear in answers  
- Citations break, hallucinations creep in, or snippets drift  
- Hybrid retrievers perform worse than single retrievers  
- Index looks healthy but coverage remains low  
- Evaluation metrics vary across identical runs

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- Eval variance ≤ 0.05 across 5 replays

---

## Symptoms → exact fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| High similarity yet wrong meaning | metric or analyzer mismatch | [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) · [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Correct section never retrieved | fragmented store or missing anchors | [retrieval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/retrieval_drift.md) · [citation_break.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/citation_break.md) |
| Hybrid worse than single | query split or mis weighted rerank | [hybrid_failure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/hybrid_failure.md) |
| Citations unstable or missing | schema not enforced | [citation_break.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/citation_break.md) |
| Answers flip between runs | prompt header reordering or λ variance | [context_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/context_drift.md) |
| Index “healthy” but recall low | stale build, analyzer mismatch | [index_skew.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/index_skew.md) |
| Eval scores noisy across replays | non deterministic eval path | [eval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/eval_drift.md) |

---

## 60 second fix checklist

1) **Lock metrics and analyzers**  
   One embedding family per field. One distance metric. Same analyzer on write and read.  
   Use: [Vector DBs & Stores](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md)

2) **Enforce the snippet contract**  
   Required: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Use: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Measure ΔS and λ**  
   Three paraphrases, two seeds. Alert when ΔS ≥ 0.60 or λ flips.  
   Use: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

4) **Add a deterministic reranker**  
   Keep BM25 and ANN candidate lists. Detect query split and resolve.  
   Use: [hybrid_failure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG/hybrid_failure.md)

5) **Rebuild where needed**  
   Follow the rebuild order with a small gold set.  
   Use: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

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
Context: TXT OS and WFGY pages are loaded.

Task:
- For question Q, log ΔS(Q, retrieved) and λ across 3 paraphrases and 2 seeds.
- Enforce cite-then-explain with the traceability schema.
- If ΔS ≥ 0.60 or λ flips, return the smallest structural change that
  pushes ΔS ≤ 0.45 and coverage ≥ 0.70.
- Use BBMC, BBCR, BBPF, BBAM when relevant.

Return JSON only:
{ "citations": [...], "ΔS": 0.xx, "λ_state": "<>", "coverage": 0.xx, "next_fix": "..." }
```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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

