# FAISS: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **VectorDBs_and_Stores**.  
  > To reorient, go back here:  
  >
  > - [**VectorDBs_and_Stores** — vector indexes and storage backends](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A compact repair guide for FAISS retrieval stacks. Use this when recall looks fine but meaning drifts, or when IVF/HNSW tuning flips answers across seeds. The checks below route you to the exact WFGY fix pages and give a minimal recipe you can paste into a runbook.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Embedding ≠ meaning: [Embedding vs Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Vectorstore health: [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)
- Query split (HyDE vs BM25): [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Evaluating RAG: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)
- FAISS specifics: [Vectorstore Metrics & FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
- Live checks: [Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   - Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   - Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**  
   - Sweep `k ∈ {5, 10, 20}` and for IVF sweep `nprobe ∈ {1, 4, 8, 16}`.  
   - For HNSW, sweep `efSearch ∈ {32, 64, 128}`.  
   - If ΔS flattens high across k, suspect metric/index mismatch.

3) **Apply the module**  
   - Retrieval drift → **BBMC** + [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
   - Reasoning collapse after retrieval → **BBCR** bridge + **BBAM** variance clamp, see [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).  
   - Dead ends in long runs → **BBPF** alternate path + [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md).

4) **Verify**  
   - Coverage to target section ≥ 0.70, ΔS ≤ 0.45 on three paraphrases, λ stays convergent across seeds.

## Typical breakpoints and the right fix

| Symptom | Likely cause | Open this | Minimal fix |
|---|---|---|---|
| High cosine similarity but wrong meaning | IP vs L2 mixup, un-normalized embeddings | [Embedding vs Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) | Normalize vectors; match metric to embedder; re-index |
| Good recall, messy top-k order | Rerank missing or weak | [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) | Add cross-encoder rerank, k=50→top-10 |
| Some facts never show up | Shards or label fragmentation | [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) | Merge shards; rebuild IVF lists; verify dim |
| Answers flip between runs | IVF `nlist/nprobe` underfit, PQ over-aggressive | [FAISS Pitfalls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md) | Raise `nprobe`, enlarge training set, reduce PQ |
| Hybrid gets worse than single retriever | Query split and prompt coupling | [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) | Split semantic vs lexical prompts; fuse post-retrieval |

## FAISS quick checklist
- Confirm **dimension** matches the embedding model output exactly.  
- Confirm **metric**: IP with normalized vectors, or L2 with raw vectors. Do not mix.  
- For IVF, set `nlist` based on corpus size, train with at least `100× nlist` examples.  
- Start with `nprobe ≈ sqrt(nlist)` and tune upward until ΔS stabilizes.  
- For HNSW, raise `efConstruction` and `efSearch` until ΔS stops improving.  
- Rebuild the index after changing normalization or metric.  
- Lock the snippet schema and citations using [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

## Copy-paste repair prompt
```

audit FAISS retrieval with ΔS and λ\_observe.
report: metric choice (IP/L2), normalization, dim, index type, nlist/nprobe or HNSW ef.
run three paraphrases, k in {5,10,20}. if ΔS stays >0.45, switch to normalized IP and rebuild.
apply BBMC + Data Contracts; add reranker for top-50→10. show before/after ΔS table.

```

## Acceptance targets
- Coverage ≥ 0.70 to the target section.  
- ΔS ≤ 0.45 across three paraphrases.  
- λ remains convergent across seeds.  
- E_resonance flat under long windows.

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

