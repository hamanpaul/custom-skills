# Vespa: Guardrails and Fix Patterns

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


Use this page when your retrieval stack runs on Vespa with vector or hybrid ranking. It routes common store-level failures to the right structural fixes in the Problem Map and gives a minimal checklist you can apply fast.

## When to open this page

- High vector similarity yet wrong meaning  
- Hybrid keyword + vector flips order between runs  
- Citations land on the wrong section or offsets do not match  
- Tensor dimensions or distance functions differ across write and read  
- Coverage stays low on the intended section even though recall looks fine

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe remains convergent across 3 paraphrases  
- E_resonance flat on long windows

---

## Map symptoms → structural fixes

- Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Snippet or citation does not match the retrieved section.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid collapse or query split between BM25 and vector.  
  → [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Version skew after deploy or wrong rank profile in use.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Long chains smear topics or capitalization across sessions.  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal Vespa setup checklist

1) **Pin tensor schema and metric**  
   Use one embedding model per vector field. Keep a single tensor dimension and a single distance function for the rank profile. Reject documents that do not match the expected dimension.

2) **Contract the snippet**  
   Every hit must carry `{snippet_id, section_id, source_url, offsets, tokens}`. Enforce cite-then-explain in the answer layer.  
   Spec: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Hybrid ordering and reranking**  
   Combine keyword recall with `nearestNeighbor` recall, then run a deterministic rerank pass. Log both candidate lists to detect query split.  
   Guide: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

4) **Analyzer and casing parity**  
   Freeze tokenization, stemming, and casing rules for all text fields used in BM25 or filters. Keep the same rules at write and read.

5) **Observability probes**  
   Log ΔS(question, retrieved) and λ per step: retrieve → rerank → reason. Alert when ΔS ≥ 0.60 or λ diverges.

6) **Cold start and deploy fences**  
   Block traffic until the new application package, schema hash, and rank profile version are active.  
   See: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## 60-second diagnosis

1) Run a 10-question smoke set on one target section.  
2) Compute ΔS(question, retrieved) for each question.  
3) If median ΔS ≥ 0.60, apply one structural fix in this order:  
   a) normalize embeddings and pin one distance function  
   b) enforce data contracts and traceability  
   c) add deterministic reranking and align analyzers  
4) Require coverage ≥ 0.70 before you publish.

---

## Copy-paste audit prompt

```

I uploaded TXT OS and the WFGY Problem Map pages.
Store: Vespa. Retrieval: BM25 + nearestNeighbor with rerank.

Audit this query and return:

* ΔS(question, retrieved) and λ across retrieve → rerank → reason.
* If ΔS ≥ 0.60, choose exactly one minimal structural fix and name the page:
  embedding-vs-semantic, retrieval-traceability, data-contracts, rerankers.
* JSON only:
  { "citations":\[...], "ΔS":0.xx, "λ":"→|←|<>|×", "next\_fix":"..." }

```

---

## Common Vespa gotchas

- Mixed embedding dimensions or distance functions across rank profiles  
  Standardize on one and validate on write.

- Summary fields do not include offsets or token spans  
  Add fields to the summary and verify the contract.

- Match-phase or targetHits tuned too low for the collection size  
  Recall collapses and rerank cannot recover. Increase recall or shard-level limits.

- Filter mismatches due to analyzer differences  
  Keep analyzer and casing identical across environments.

- Application package deployed but old profile still served  
  Fence the cutover and verify the active profile hash before enabling traffic.

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

