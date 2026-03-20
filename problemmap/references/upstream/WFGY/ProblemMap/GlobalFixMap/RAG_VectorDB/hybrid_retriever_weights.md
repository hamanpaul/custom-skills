# Hybrid Retriever Weights — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **RAG_VectorDB**.  
  > To reorient, go back here:  
  >
  > - [**RAG_VectorDB** — vector databases for retrieval and grounding](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when **hybrid retrieval underperforms a single retriever** or when results look noisy after fusing BM25, dense vectors, HyDE, or filters. Failures usually come from **score scale mismatch**, **duplicate dominance**, or **query-type priors** not reflected in weights.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Ordering control: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Query parsing split (HyDE, BM25): [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Vector store fragmentation: [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)  
- Metric mismatch: [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/metric_mismatch.md)  
- Normalization and scaling: [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md)  
- Tokenization and casing: [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md)

---

## Core acceptance

- ΔS(question, retrieved) ≤ 0.45 on 3 paraphrases and 2 seeds.  
- Coverage ≥ 0.70 to the target section after fusion and rerank.  
- λ remains convergent when weights are perturbed within ±10 percent.  
- Jaccard overlap against the best single retriever’s top-k ≥ 0.60.  
- No single source type or domain exceeds 40 percent of the final top-k unless configured.

---

## Symptoms → likely cause → open this

- Hybrid is worse than dense alone  
  → raw scores on different scales or rank fusion mis-tuned  
  → [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- BM25 dominates multilingual queries  
  → tokenizer or casing divergence for CJK or mixed scripts  
  → [tokenization_and_casing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md)

- HyDE helps recall yet increases wrong-meaning hits  
  → HyDE prompts off-domain, no rerank clamp  
  → [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Same snippet appears many times and crowds others  
  → duplicate and near-duplicate collapse missing  
  → (next page) `duplication_and_near_duplicate_collapse.md`

- Fusion order unstable across shards  
  → partial index rollout or fragmented store  
  → [vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md)

---

## Fix in 60 seconds

1) **Normalize each retriever’s scores inside the candidate pool**  
   Use one of: min-max to 0–1 per retriever, z-score per retriever, or pure rank-based RRF.

2) **De-duplicate by snippet identity**  
   Collapse near-duplicates using stable keys: `{doc_id, section_id, hash_64}`.

3) **Fuse with a simple, auditable rule**  
   Start with RRF: `score = Σ 1 / (rank_i + k)` with `k ∈ [50, 100]`.  
   Then try weighted sum on normalized scores: `S = wdense*sdense + wbm25*sbm25 + whyde*shyde`.

4) **Rerank with a cross-encoder**  
   Rerank top 50–100 to top 10–20. Enforce cite-then-explain in the prompt.

5) **Measure ΔS and λ**  
   If λ flips when weights move by ±10 percent, clamp with BBAM and lock schema headers.

---

## Minimal reference recipe

```

retrievers:

* name: dense
  k: 60
  norm: z
  weight: 0.55
* name: bm25
  k: 200
  norm: rank   # convert to ranks 1..k
  weight: 0.35
* name: hyde
  k: 60
  norm: z
  weight: 0.10

fusion:
method: RRF
rrf\_k: 60
dedupe: snippet\_id  # or doc\_id+section\_id+hash64

rerank:
model: cross-encoder-v2
take\_top: 15

accept:
deltaS\_max: 0.45
coverage\_min: 0.70
jitter\_weight: 0.10   # weights +/- 10 percent must keep λ convergent

```

---

## Weighting heuristics that actually work

- **Short factual queries**  
  Increase dense weight to 0.6–0.7. Keep BM25 at 0.3–0.4. HyDE optional.

- **Long verbose queries or code**  
  Push BM25 to 0.5. Keep dense at 0.4. Use reranker to clean length bias.

- **Multilingual or mixed-script**  
  Reduce BM25 weight if tokenizer mismatch is suspected. Verify casing and analyzer.

- **Highly structured data**  
  Use BM25 boost on fielded terms. Keep dense for semantic recall.

- **Safety or policy queries**  
  HyDE at most 0.15. Prefer deterministic BM25 plus strict reranker.

---

## Observability probes you must log

- Per retriever: raw score mean and stdev before normalization.  
- After fusion: source mix histogram and duplicate collapse count.  
- ΔS(question, retrieved) and λ states at steps: retrieve, fuse, rerank, answer.  
- A/B against best single retriever and report ΔS improvement or regression.

---

## Common gotchas

- Mixing **cosine** dense scores with **BM25 raw scores** without normalization.  
- HyDE prompts built with a different tokenizer than the dense model.  
- Reranker trained on passages while you fuse at document level.  
- Language-specific analyzers differ across shards and you fuse their outputs.  
- Latency cutoffs truncate candidate lists unevenly and bias the fusion.

---

## Verification

- Gold set of 100 queries with 3 paraphrases.  
- Require ΔS ≤ 0.45 and coverage ≥ 0.70 after fusion plus rerank.  
- Jaccard with best single retriever ≥ 0.60.  
- Weight jitter ±10 percent must keep λ convergent and citations stable.

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

