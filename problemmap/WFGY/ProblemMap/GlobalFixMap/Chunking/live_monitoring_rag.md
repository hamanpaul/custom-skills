# RAG live monitoring

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Chunking**.  
  > To reorient, go back here:  
  >
  > - [**Chunking** — text segmentation and context window management](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Operational probes, alerts, and dashboards to keep retrieval stable after you change chunking, OCR, or indexing. This page defines the minimal signals you must log and the exact gates to alert on.

## Open these first
- Chunk ids and stability: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)  
- Title tree numbering: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)  
- Section boundary rules: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)  
- Typed blocks (code, tables, figures): [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)  
- PDF layout and OCR normalization: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)  
- Rebuild without breaking citations: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)  
- Eval harness and gates: [eval_rag_precision_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md)  
- Traceable retrieval schema: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload contracts for RAG: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Visual recovery map: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Prompt injection defenses: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)  
- Triage runbook: [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## What to monitor in real time

Log per query and aggregate into one minute windows.

- **Coverage**: share of answers that cite at least one valid snippet.  
- **ΔS(question, retrieved)**: semantic distance for the chosen citation. Stable ≤ 0.45. Risk ≥ 0.60.  
- **λ_observe**: convergence state across paraphrases. Track flip rate between adjacent steps.  
- **Citation accuracy**: cited `section_id` and offsets match a valid block within a 30 byte window.  
- **Anchor proximity**: title tree distance between cited section and expected anchor when known.  
- **Index integrity**: `index_hash`, `metric`, `analyzer`, and `embed_model` fingerprint. Alert on drift.  
- **Rerank stability**: Kendall tau between top ten on consecutive runs for the same query template.  
- **Latency SLOs**: p50, p95 for retrieve and reason stages.  
- **Error budget**: rolling one hour budget for coverage and citation accuracy.

## Logging schema to enable the probes

Emit one record per question. Follow the fields from the traceability spec and chunking pages.

```json
{
  "qid": "live-2025-08-27T12:30:22Z-000134",
  "question": "When to use SCU",
  "retrieval": {
    "topk": [
      {"id":"S.4.2.p.Bk011a", "score":0.83, "type":"prose", "offsets":[204611,205279]},
      {"id":"S.4.1.p.Bk010",  "score":0.79, "type":"prose", "offsets":[198002,199112]}
    ],
    "metric": "cos",
    "analyzer": "porter-en",
    "index_hash": "faiss:v3:hnsw:cos",
    "embed_model": "text-embedding-3-large",
    "ΔS_list": [0.31, 0.59],
    "λ_states": ["→","→"]
  },
  "answer": {
    "citations": [{"id":"S.4.2.p.Bk011a", "offsets":[204611,205279]}],
    "coverage": true,
    "ΔS": 0.31,
    "λ_final": "→"
  },
  "perf": {"t_retrieve_ms": 120, "t_reason_ms": 480},
  "context": {"client":"prod", "build":"2025.08.27.2", "region":"ap-sg"},
  "ts":"2025-08-27T12:30:22Z"
}
````

## Alert rules and thresholds

Use rolling windows with at least 200 samples or five minutes, whichever is larger.

* **Coverage drop**: coverage < 0.70 for five minutes. Page on call.
* **ΔS spike**: p90 ΔS ≥ 0.60 or median ΔS ≥ 0.45 for three minutes.
* **λ flip rate**: fraction of paraphrase triplets with divergent λ ≥ 0.10.
* **Citation mismatch**: citation accuracy < 0.95 for five minutes.
* **Index drift**: any change in `index_hash` while build id is constant.
* **Rerank instability**: average top ten Kendall tau < 0.6 over five minutes.
* **Latency regression**: p95 retrieve or reason above baseline by 30 percent.

## Dashboards to build

* **SLO board**: coverage, citation accuracy, ΔS median, ΔS p90, λ flip rate.
* **Title tree health**: anchor proximity histogram and top failing sections.
* **Content type panel**: split metrics for prose, table, code, figure.
* **Index integrity**: time series of `index_hash`, metric, analyzer, embed model.
* **Rerank panel**: tau vs recall proxy and error bars.
* **Latency panel**: p50, p95 by stage.

## Canary and rollback policy

* Ship a shadow index behind a flag. Verify gates from [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md).
* Start at five percent traffic with hourly comparison to the live index.
* **Promote** only if coverage improves or is equal, citation accuracy ≥ 0.95, median ΔS ≤ 0.40, recall proxy unchanged, and λ flip rate ≤ baseline.
* **Rollback** immediately on two consecutive alert windows or any index drift event.

## Sampling and gold refresh

* Mirror one percent of production queries to a frozen gold set run each day.
* Regenerate three paraphrases per question monthly.
* Mark hard negatives near anchors after layout changes from [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

## Copy rules you can paste into your monitor

**Coverage gate**

```
window_5m_coverage = sum(answer.coverage) / count()
alert if window_5m_coverage < 0.70 for 5m
```

**ΔS gate**

```
window_3m_ds_p90 = percentile(answer.ΔS, 90)
alert if window_3m_ds_p90 >= 0.60 for 3m
```

**λ flip rate**

```
lambda_flips = count(lambda_triplet_state == "divergent") / count(lambda_triplet_state)
alert if lambda_flips >= 0.10 for 5m
```

**Citation accuracy**

```
cite_ok = count(citation.within_30_bytes == true) / count()
alert if cite_ok < 0.95 for 5m
```

**Index drift**

```
alert if distinct(index_hash) > 1 and distinct(build) == 1 over 5m
```

## LLM assisted triage prompt

```
You have TXT OS and the WFGY Problem Map.

Given a five minute slice of live logs with:
- ΔS per retrieved item and for the chosen citation,
- λ states across three paraphrases,
- coverage and citation accuracy,
- index_hash, metric, analyzer, embed_model,
- top sections and their title tree ids.

Do:
1) Identify the failing layer: chunk boundary, rerank, index metric, OCR normalization, or prompt schema.
2) Return the exact WFGY pages to open next from:
   retrieval-traceability, data-contracts, section_detection, code_tables_blocks,
   pdf_layouts_and_ocr, reindex_migration, rerankers, embedding-vs-semantic.
3) Propose a minimal reversible fix and a verification test.
Return compact JSON {layer, pages[], fix, test}.
```

## Common pitfalls

* Shipping a new index without freezing normalizers. Offsets will not align. See [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).
* Measuring answers without cite-first. Coverage becomes meaningless. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
* Ignoring content types. Averages hide failures in tables and code.
* Comparing different rerankers in the same chart. Pin rerank during canary.
* Missing guard on `index_hash`. Small rebuilds can cause silent drift.
* Treating high similarity as correctness. Check [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

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

