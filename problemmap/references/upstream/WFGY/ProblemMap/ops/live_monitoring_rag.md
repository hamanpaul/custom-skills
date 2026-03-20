# Live monitoring & alerting — RAG services

**Goal:** list of recommended metrics, alert rules and dashboard panels to keep RAG pipelines observable and actionable.

---

## Core metrics to collect (recommended names)

**Service-level**
- `rag_e2e_latency_seconds` (histogram) — E2E latency (request in → answer out)  
- `rag_error_count_total` — errors per endpoint  
- `rag_request_count_total` — total requests

**Retrieval-level**
- `retriever_qps_total`  
- `retriever_retrieved_docs_count` (per request)  
- `retriever_empty_result_count_total` — unexpected empty sets

**Vectorstore**
- `vectorstore_index_load_time_seconds`  
- `vectorstore_memory_bytes`  
- `vectorstore_indexed_docs_total`

**Accuracy/provenance**
- `rag_citation_hit_rate` (CHR gauge over sliding window)  
- `rag_precision_shipped` (periodic batch scorer push)  
- `rag_under_refusal_count_total`

**Infrastructure**
- `llm_api_rate_limited_total`  
- `llm_api_error_total`  
- `queue_backlog_count` (if using background queues)

---

## Suggested PromQL alerts (examples)

> Tune thresholds to your workload.

**A) Latency breach (interactive)**
```yaml
alert: RAGHighP95Latency
expr: histogram_quantile(0.95, sum(rate(rag_e2e_latency_seconds_bucket[5m])) by (le,instance)) > 2
for: 5m
labels:
  severity: page
annotations:
  summary: "RAG p95 > 2s ({{ $labels.instance }})"
````

**B) Error spike**

```yaml
alert: RAGErrorSpike
expr: increase(rag_error_count_total[5m]) > 50
for: 2m
labels: { severity: page }
```

**C) Retriever empty results**

```yaml
alert: RetrieverEmptyResults
expr: increase(retriever_empty_result_count_total[5m]) > 1
for: 5m
labels: { severity: ticket }
```

**D) CHR drop**

```yaml
alert: CHRDrop
expr: rag_citation_hit_rate < 0.6
for: 10m
labels: { severity: ticket }
```

**E) LLM auth failure**

```yaml
alert: LLMAuthFail
expr: increase(llm_api_error_total{code="401"}[5m]) > 0
for: 1m
```

---

## Dashboard panels (recommended)

1. E2E latency (p50/p95/p99) trend.
2. Requests per second and error rate.
3. Retriever QPS, avg retrieved docs, empty results.
4. CHR & Precision (batch scorer push).
5. Vectorstore memory & disk IO.
6. LLM provider error & rate-limit metrics.

---

## Incident play (fast actions)

1. If CHR drop → run **diagnostic retrieval** for 10 golden queries (retrieved ids + cosine scores).
2. If retriever empty → check vectorstore health and index partitions. Restart index shard if needed.
3. If E2E latency spike with LLM errors → throttle traffic, put a hard rate limit and rollback deploy if needed.
4. If LLM auth failure → rotate key & redeploy secrets.

---

## How to integrate scoring metrics

* Periodic scorer job should push `rag_citation_hit_rate` and `rag_precision_shipped` as a short-timeseries gauge (per 5–15m window).
* Use batching: run `score_eval.py` (see `ProblemMap/eval/README.md`) nightly and push summary metrics via a small exporter.

---

## Troubleshooting queries (prometheus examples)

* Check p95 per instance:

  ```promql
  histogram_quantile(0.95, sum(rate(rag_e2e_latency_seconds_bucket[5m])) by (le,instance))
  ```
* CHR trend:

  ```promql
  avg_over_time(rag_citation_hit_rate[30m])
  ```

---

### Links

* Deployment checklist → [deployment\_checklist.md](./deployment_checklist.md)
* Debug playbook → [debug\_playbook.md](./debug_playbook.md)
* Eval & scoring → [../eval/README.md](../eval/README.md)

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

