# Metric Mismatch — Guardrails and Fix Pattern

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


Use this page when **nearest neighbors look similar in cosine space but your VectorDB runs L2 or dot**, or the reverse.  
This failure appears often in FAISS, Milvus, pgvector, Weaviate, Redis, Vespa, and similar stores.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  

---

## Core acceptance

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 for the target section  
- λ remains convergent across three paraphrases and two seeds  
- Store metric matches embedding training metric (cosine ↔ cosine, L2 ↔ L2, dot ↔ dot)

---

## Typical breakpoints and the right fix

- **High cosine similarity in logs but wrong meaning**  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  

- **Top-k neighbors inconsistent across runs** (vector drift between L2 and cosine)  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  

- **Switching embedding models breaks index** (new default metric not aligned with store)  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)  

- **Hybrid dense+BM25 loses semantic signal** (wrong weighting due to metric scaling)  
  → [hybrid_failure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/RAG/hybrid_failure.md)  

---

## Store defaults reference

| Store         | Default metric       | Notes                                  |
|---------------|----------------------|----------------------------------------|
| FAISS         | L2 (can set IP or cosine) | Normalize vectors before cosine search |
| Milvus        | L2 / IP              | Cosine requires explicit normalization |
| pgvector      | L2 / cosine / IP     | Must choose at index creation          |
| Weaviate      | cosine               | Dot/IP optional                        |
| Redis-Vector  | cosine               | Normalize mandatory                    |
| Vespa         | dot                  | Needs scaling to emulate cosine        |

---

## Fix in 60 seconds

1. **Log current metric**  
   Run a probe query (`SELECT metric FROM index_metadata`). Verify it matches embedding doc.

2. **Check normalization**  
   If metric=cosine but vectors are raw, ΔS will inflate. Normalize to unit length.

3. **Re-index with explicit metric**  
   Drop and rebuild index with the same metric as embedding training.  

4. **Hybrid sanity check**  
   If using BM25+dense, reweight so ΔS ≤ 0.45 and coverage ≥ 0.70.  

---

## Copy-paste test query

```sql
-- Example: pgvector
SELECT id, embedding <=> query_embedding
FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 5;
````

Ensure `<=>` operator matches the chosen metric (`cosine`, `L2`, or `IP`).

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

