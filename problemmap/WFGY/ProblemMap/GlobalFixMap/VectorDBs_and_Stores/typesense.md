# Typesense: Guardrails and Fix Patterns

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


Use this page when your retrieval stack runs on Typesense with vector or hybrid search. It routes common store-level failures to the exact structural fixes in the Problem Map and gives a minimal checklist you can apply fast.

## When to open this page

- High vector similarity yet wrong meaning
- Hybrid keyword + vector returns unstable rankings between runs
- Citations point to the wrong section or offsets do not line up
- Analyzer or casing differs between write and read
- Index looks healthy but coverage stays low on target sections

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe stays convergent across 3 paraphrases  
- E_resonance flat on long windows

---

## Map symptoms → structural fixes

- Wrong-meaning hits despite high similarity.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Snippet or citation does not match the retrieved section.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid collapse or query split between keyword and vector paths.  
  → [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Version skew after deploy, or wrong analyzer used at runtime.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Long chains smear topics or capitalization across sessions.  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal Typesense setup checklist

1) **Pin metrics and analyzers**  
   Choose one distance metric for vectors and keep normalization identical at write and read. Freeze text analyzer, tokenizer, and casing on all keyword fields used in hybrid queries.

2) **Contract the snippet**  
   Every hit must carry `{snippet_id, section_id, source_url, offsets, tokens}`. Enforce cite-then-explain in the answer layer.  
   Spec: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

3) **Dimension and schema sanity**  
   Use a single embedding dimension per collection. Validate dimension on write. Reject any record whose vector length differs from the schema.

4) **Hybrid ordering and reranking**  
   When combining keyword and vector signals, run a deterministic rerank pass. Log the pre- and post-rerank candidates to catch query split.

5) **Observability probes**  
   Log ΔS(question, retrieved) and λ per step: retrieve → rerank → reason. Alert at ΔS ≥ 0.60 or when λ diverges.

6) **Cold start and deploy fences**  
   Block queries until the collection reports ready and the expected index or analyzer hash matches.  
   See: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## 60-second diagnosis

1) Run a 10-question smoke test on one target section.  
2) Compute ΔS(question, retrieved) for each question.  
3) If median ΔS ≥ 0.60, apply one structural fix in this order:  
   a) normalize embeddings and pin metric  
   b) enforce data contracts and traceability  
   c) add reranking and align analyzers  
4) Require coverage ≥ 0.70 before you publish.

---

## Copy-paste audit prompt

```

I uploaded TXT OS and the WFGY Problem Map pages.
Store: Typesense. Retrieval: vector or hybrid.

Audit this query and return:

* ΔS(question, retrieved) and λ states across retrieve → rerank → reason.
* If ΔS ≥ 0.60, choose exactly one minimal structural fix and name the page:
  embedding-vs-semantic, retrieval-traceability, data-contracts, rerankers.
* JSON only:
  { "citations":\[...], "ΔS":0.xx, "λ":"→|←|<>|×", "next\_fix":"..." }

```

---

## Common Typesense gotchas

- Mixed analyzers across collections or environments  
  Pin analyzer and case rules. Rebuild if the analyzer changed.

- Vector field created with a different dimension than the model now used  
  Validate dimension on write and reject mismatches with a clear error.

- Hybrid search ranks keyword-only hits above relevant vector hits  
  Add a reranking pass and log both candidate lists.

- Batch imports without normalization  
  Normalize embeddings consistently or you will see distance drift.

- Pagination with unstable sort keys during frequent updates  
  Use a stable cursor or snapshot the candidate set before reranking.

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

