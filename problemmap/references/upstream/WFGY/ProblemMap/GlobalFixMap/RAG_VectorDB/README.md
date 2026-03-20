<!--
Search Anchor:
rag vector database failures
rag vectordb global fix map
rag embedding bugs
vector db retrieval drift
embedding metric mismatch cosine l2 dot
embedding normalization scaling issues
tokenization casing embedding drift
chunking embedding contract mismatch
vectorstore fragmentation rag
dimension mismatch embedding index
index skew stale vector index
hybrid retriever weighting bm25 ann
near duplicate embedding collapse
embedding poisoning contamination
rag semantic boundary failure
high similarity wrong meaning
citations wrong section vectordb
hybrid retriever underperform
index healthy but recall low
delta s question retrieved
lambda observe convergent
e_resonance flat
rag acceptance targets

Fix pages in this folder:
metric_mismatch.md
normalization_and_scaling.md
tokenization_and_casing.md
chunking_to_embedding_contract.md
vectorstore_fragmentation.md
dimension_mismatch_and_projection.md
update_and_index_skew.md
hybrid_retriever_weights.md
duplication_and_near_duplicate_collapse.md
poisoning_and_contamination.md

Related WFGY pages:
ProblemMap/data-contracts.md
ProblemMap/retrieval-traceability.md
ProblemMap/rerankers.md
ProblemMap/bootstrap-ordering.md
ProblemMap/context-drift.md
ProblemMap/entropy-collapse.md

Vector DB vendors:
faiss
milvus
qdrant
weaviate
pinecone
chroma
pgvector
redis vector
elasticsearch dense vector
typesense
vespa

Incident keywords:
rag vectordb incident
embedding mismatch incident
vector index rebuild
semantic drift retrieval
citation mismatch vectordb
hybrid retriever bug
embedding poisoning attack
-->


# RAG + VectorDB — Global Fix Map

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

This hub covers **typical retrieval bugs caused by vector databases and embeddings**.  
Use this page if your RAG pipeline looks fine but answers keep drifting, citations don’t match, or hybrid retrievers underperform.  
Every page here is a guardrail with copy-paste recipes and acceptance targets.  

---

## Orientation: what each page means

| Fix Page | What it solves | Typical symptom |
|----------|----------------|-----------------|
| [metric_mismatch.md](./metric_mismatch.md) | Distance metric mismatch (cosine vs L2 vs dot) | High similarity numbers but wrong meaning |
| [normalization_and_scaling.md](./normalization_and_scaling.md) | Missing normalization or scaling issues | Embeddings with larger norms dominate |
| [tokenization_and_casing.md](./tokenization_and_casing.md) | Tokenizer or casing drift | Same text embeds differently across runs |
| [chunking_to_embedding_contract.md](./chunking_to_embedding_contract.md) | Chunking not aligned with embedding model | Citations cut mid-sentence or incoherent snippets |
| [vectorstore_fragmentation.md](./vectorstore_fragmentation.md) | Over-fragmented stores | Retrieval pulls incomplete, scattered sections |
| [dimension_mismatch_and_projection.md](./dimension_mismatch_and_projection.md) | Embedding and index dimension mismatch | Runtime errors or silent drop of vectors |
| [update_and_index_skew.md](./update_and_index_skew.md) | Index not refreshed after updates | Old sections keep showing up |
| [hybrid_retriever_weights.md](./hybrid_retriever_weights.md) | Hybrid weighting not tuned | BM25+ANN underperforms single retriever |
| [duplication_and_near_duplicate_collapse.md](./duplication_and_near_duplicate_collapse.md) | Redundant entries collapse signal | Top-k filled with near-identical chunks |
| [poisoning_and_contamination.md](./poisoning_and_contamination.md) | Malicious or noisy vectors | Hallucinations, unsafe content retrieval |

---

## When to use this folder

- Your answers look **semantically wrong** even though top-k similarity looks high.  
- Citations point to the wrong section or cannot be verified.  
- Hybrid retrieval underperforms vs single retriever.  
- Index seems “healthy” but recall/coverage stays low.  

---

## Core acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across 3 paraphrases  
- E_resonance flat on long windows  

---

## FAQ for newcomers

**Why do we need these fixes if VectorDBs are mature?**  
Because RAG pipelines often break not at the infra level but at the **semantic boundary**. Even if FAISS, Milvus, or Pinecone run fine, the *contracts* between embedding, chunking, and retrieval are fragile.

**What is metric mismatch and why is it deadly?**  
If your index uses `L2` but embeddings were trained for `cosine`, the “closest” neighbors are meaningless. This is the single most common RAG failure.

**Why do duplicates matter so much?**  
If your corpus has many repeated sentences, the retriever fills top-k with clones. The LLM sees no diversity and hallucinates.

**Is poisoning really a real-world issue?**  
Yes. Even a single malicious doc can bias retrieval. This page shows how to detect and quarantine them without retraining the whole pipeline.

---

## 60-Second Fix Checklist

1. **Lock metrics and analyzers**  
   One embedding model per field. One distance metric. Same analyzer for read/write.

2. **Enforce snippet contracts**  
   Require `{snippet_id, section_id, source_url, offsets, tokens}`.  
   → See [data-contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3. **Tune hybrid retrievers**  
   Keep candidate lists from BM25 and ANN. Detect query splits.  
   → See [rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

4. **Cold-start fences**  
   Block traffic until index hash and embedding version match.  
   → See [bootstrap-ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

5. **Observability**  
   Log ΔS and λ. Alert if ΔS ≥ 0.60.  

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

