# Embeddings — Normalization and Scaling

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Embeddings**.  
  > To reorient, go back here:  
  >
  > - [**Embeddings** — vector representations and semantic search](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A repair page for scale and metric mismatches in embedding pipelines. Use this when retrieval quality looks good by similarity numbers but the meaning is wrong, or when different stores or models disagree after a migration.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and how to verify: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Schema and payload locks: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning root cause: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Store specific notes, FAISS example: [faiss.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md)

## When to use this page

* Similarity scores look high but answers cite the wrong section.
* Cosine in docs, dot in code, or the reverse.
* One environment normalizes vectors while another does not.
* Upgrades introduce new dimensions or multilingual models and recall drops.
* PQ or HNSW behaves differently after a rebuild.

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows

---

## Map symptoms → structural fixes

* Wrong meaning despite high similarity
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Metric or analyzer mismatch across write and read paths
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* Fragmented store after mixed normalization or mixed models
  → Pattern: [pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

* Index type changes that silently change scale behavior
  → FAISS guardrails: [faiss.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md)

---

## 60-second checklist

1. Decide the semantic metric
   Use cosine for unit vectors. Use dot only when magnitude carries meaning. Record the choice in your data contract.

2. Enforce one normalization policy
   Either store all vectors L2-normalized or normalize at query time on both write and read paths. Never mix.

3. Lock dimensions and model id
   Record `embed_model`, `dim`, `metric`, `normalize=true|false`, and `EMB_HASH` in every payload. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

4. Rebuild when the policy changes
   If the previous index mixed policies, re-embed and rebuild. Validate with a small gold set and the acceptance targets above.

---

## Minimal probes you can paste into a notebook

```txt
Probe A — norm distribution
1. Sample 10k vectors before index.
2. Compute median ||v||2 and IQR.
3. If median ≈ 1.0 with tiny IQR, corpus looks normalized. If not, policy is mixed.

Probe B — metric toggle
1. Run the same top-k with and without L2 normalization on queries.
2. If the winner set flips and ΔS improves only under one policy, lock that policy.

Probe C — k-sweep stability
1. For k in {5, 10, 20}, chart ΔS(question, retrieved).
2. Flat and high values suggest metric or analyzer mismatch.

Probe D — multilingual scale check
1. Split queries by language tag.
2. If one language has systematically higher norms or ΔS, normalize and consider per-language centering.
```

---

## Common failure patterns and the fix

* Mixed policies across services
  Write path stores raw vectors while the retriever normalizes only queries. Fix with one policy. Rebuild or pre-normalize on write.

* Cosine in code, dot in index
  Check the store configuration and the client. Align both ends and re-verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

* Dimensionality drift after model swap
  Store `dim` inside the contract and refuse ingestion when `dim` mismatches. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

* Anisotropy or cluster collapse
  Try mean-centering and unit-norm. If recall remains low, re-embed with a model that was trained for cosine and re-chunk per the playbook. See [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

* PQ or HNSW surprises
  Confirm that training data for PQ used the same normalization policy as the live corpus. Store-specific notes in [faiss.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/VectorDBs_and_Stores/faiss.md).

---

## Verification protocol

1. Build a ten question gold set with exact anchors.
2. Run three paraphrases and two seeds.
3. Require coverage ≥ 0.70 and ΔS ≤ 0.45 before and after the change.
4. Keep traces with `metric`, `normalize_flag`, `dim`, `EMB_HASH`, and index type.
   Eval references: [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Hand-off checklist for teams

* Contract fields present in every write
  `embed_model`, `dim`, `metric`, `normalize`, `EMB_HASH`, `INDEX_HASH`.
* One policy in code and infra
  Normalization on both ends or on neither.
* Store and client agree on metric
  Unit tests assert the setting at startup.
* Monitoring
  Log ΔS and λ by policy. Alert when ΔS ≥ 0.60 or λ flips.
  Ops references: [live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

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

