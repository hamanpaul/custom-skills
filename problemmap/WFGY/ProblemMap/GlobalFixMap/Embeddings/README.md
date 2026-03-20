<!--
Search Anchor:
embeddings global fix map
embedding layer guardrails
embedding stability before retrieval
embedding drift causes retrieval drift
vectors look fine but retrieval wrong
coverage low despite healthy index
store queries fail silently
silent failure vector db
high similarity wrong neighbors
nearest neighbors wrong meaning
metric mismatch cosine l2 dot
distance metric mismatch embedding model assumption
faiss l2 default cosine expected
pinecone cosine redis dot
normalization scaling embeddings
l2 normalize on write and query
embedding norms dominate results
magnitude drift unstable retrieval
tokenization mismatch embedding
tokenizer mismatch ingestion query
casing drift apple vs Apple embeddings differ
lowercase mismatch
chunking to embedding contract
chunk alignment semantic window
snippets cut mid thought anchors lost
mid sentence split citations incoherent
vectorstore fragmentation
index fragmented recall low even high k
sharded store drift
missing anchors scattered sections
dimension mismatch embedding dimension index dimension
projection mismatch truncation silent
runtime errors or silent drop vectors
update and index skew
stale vectors remain in index
old embeddings show up after updates
rebuild index correct dimension
hybrid retriever weights bm25 ann unbalanced
hybrid worse than single retriever
weights mis tuned reranker overlap low
duplication near duplicate collapse
top k filled with near identical chunks
same doc retrieved repeatedly lack diversity
poisoning contamination adversarial vectors
noisy vectors randomized retrieval
malicious doc biases retrieval
quarantine poisoned embeddings
embedding version drift
embedding model family mismatch per field
analyzer mismatch read write
observability embeddings
delta s question retrieved
lambda observe convergent paraphrases seeds
e resonance flat long windows
acceptance targets embeddings
delta s <= 0.45
coverage >= 0.70
lambda convergent 3 paraphrases 2 seeds
no index skew between write read

Primary pages in this folder:
ProblemMap/GlobalFixMap/Embeddings/metric_mismatch.md
ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md
ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md
ProblemMap/GlobalFixMap/Embeddings/chunking_to_embedding_contract.md
ProblemMap/GlobalFixMap/Embeddings/vectorstore_fragmentation.md
ProblemMap/GlobalFixMap/Embeddings/dimension_mismatch_and_projection.md
ProblemMap/GlobalFixMap/Embeddings/update_and_index_skew.md
ProblemMap/GlobalFixMap/Embeddings/hybrid_retriever_weights.md
ProblemMap/GlobalFixMap/Embeddings/duplication_and_near_duplicate_collapse.md
ProblemMap/GlobalFixMap/Embeddings/poisoning_and_contamination.md

Related routing pages:
ProblemMap/GlobalFixMap/Retrieval/README.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/embedding-vs-semantic.md
ProblemMap/chunking-checklist.md
ProblemMap/patterns/pattern_vectorstore_fragmentation.md
ProblemMap/rerankers.md
ProblemMap/bootstrap-ordering.md
ProblemMap/rag-architecture-and-recovery.md

Vector DB store jump index:
ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md
faiss chroma qdrant weaviate milvus pgvector redis elasticsearch pinecone typesense vespa

Common incidents:
embedding recall collapse
embedding mismatch after deploy
embedding normalization missing
tokenizer version drift
casing mismatch ingestion query
dimension mismatch silent truncation
index skew stale results
duplicate chunks fill top k
poisoned vectors retrieval unsafe
hybrid retrieval collapse noise
-->


# Embeddings — Global Fix Map

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

A hub to stabilize the **embedding layer** before retrieval begins.  
Use this folder if your vectors look fine at a glance but retrieval keeps drifting, coverage stays low, or store queries fail silently. No infra change needed.

---

## Orientation: what each page covers

| Page | What it solves | Typical symptom |
|---|---|---|
| [Metric Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/metric_mismatch.md) | Store metric (L2, cosine, dot) differs from model assumption | High similarity but wrong neighbors |
| [Normalization & Scaling](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md) | Embeddings not normalized or scaled | Results unstable across runs |
| [Tokenization & Casing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md) | Tokenizer mismatch, casing differences | Same text gives different vectors |
| [Chunking → Embedding Contract](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/chunking_to_embedding_contract.md) | Chunk cuts misaligned with semantic windows | Snippets cut mid-thought, anchors lost |
| [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/vectorstore_fragmentation.md) | Index silently fragmented | Recall too low even with large k |
| [Dimension Mismatch & Projection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/dimension_mismatch_and_projection.md) | Store dimension vs embedding dimension mismatch | Index errors or silent truncation |
| [Update & Index Skew](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/update_and_index_skew.md) | Old vectors remain in index | Results point to stale data |
| [Hybrid Retriever Weights](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/hybrid_retriever_weights.md) | BM25 + ANN weights unbalanced | Hybrid worse than single retriever |
| [Duplication & Near-Duplicate Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/duplication_and_near_duplicate_collapse.md) | Duplicate data overwhelms recall | Same doc retrieved repeatedly |
| [Poisoning & Contamination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/poisoning_and_contamination.md) | Embeddings polluted by adversarial/noisy vectors | Retrieval looks “randomized” |

---

## When to use this folder

- Retrieval looks **fine by eye** but metrics drift across runs.  
- Coverage stays low despite healthy-looking indexes.  
- Citations pull from **stale** or duplicated data.  
- Same query yields different answers depending on casing or seed.  
- Hybrid retrievers collapse into noise.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 for target section  
- λ_observe convergent across 3 paraphrases and 2 seeds  
- No index skew between write/read

---

## 60-second fix checklist

1. **Lock metrics**  
   One model family, one distance metric.  
   Guide: [Metric Mismatch](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/metric_mismatch.md)

2. **Normalize**  
   Apply L2 norm to embeddings at both write and query.  
   Guide: [Normalization & Scaling](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/normalization_and_scaling.md)

3. **Unify tokenization**  
   Same tokenizer + casing across ingestion and query.  
   Guide: [Tokenization & Casing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/tokenization_and_casing.md)

4. **Audit chunking**  
   Verify semantic alignment, no mid-thought splits.  
   Guide: [Chunking → Embedding Contract](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/chunking_to_embedding_contract.md)

5. **Rebuild index if skewed**  
   Drop old embeddings, rebuild with correct dimension.  
   Guide: [Update & Index Skew](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/update_and_index_skew.md)

---

## FAQ for newcomers

**Why is metric mismatch so common?**  
Because vector DBs default differently: FAISS often L2, Pinecone cosine, Redis dot. If your embedding model expects cosine, L2 will silently break recall.

**Why normalize embeddings?**  
Without normalization, embeddings vary in magnitude. Distance stops reflecting meaning.

**Why do tokenizers matter?**  
“Apple” vs “apple” may yield different vectors if one side lowercases, the other doesn’t.

**What if coverage stays low after all fixes?**  
Check for fragmentation and duplication collapse. The issue may not be the embedding model itself, but how the index is populated.

---

- [Retrieval (Global Fix Map)](https://github.com/onestardao/WFGY/tree/main/ProblemMap/GlobalFixMap/Retrieval/README.md)  
- [Vector DBs & Stores](https://github.com/onestardao/WFGY/tree/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/README.md)

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

