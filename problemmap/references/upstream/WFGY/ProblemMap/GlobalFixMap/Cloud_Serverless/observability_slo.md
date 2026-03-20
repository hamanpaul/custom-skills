# Observability and SLO — Serverless and Edge

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Cloud_Serverless**.  
  > To reorient, go back here:  
  >
  > - [**Cloud_Serverless** — scalable functions and event-driven pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Make failures visible before users feel them. This page defines the SLIs, SLOs, probes, and alerts you need for serverless and edge stacks that run RAG, agents, and tool calls.

## When to use this page

* Latency or error patterns vary by region or edge POP.
* Cold starts and concurrency caps spike at random times.
* RAG answers flip on harmless paraphrases and you cannot see why.
* Webhooks and egress succeed sometimes and duplicate other times.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval knobs and ordering: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Trace and prove snippets: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · Contract payloads: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Meaning vs distance: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Boot and deploy hazards: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Cloud and edge companions:
  [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) ·
  [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md) ·
  [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md) ·
  [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md) ·
  [Runtime Env Parity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/runtime_env_parity.md) ·
  [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md) ·
  [Pricing vs Latency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/pricing_latency_tradeoffs.md) ·
  [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md) ·
  [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md) ·
  [Region Failover Drills](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/region_failover_drills.md) ·
  Live ops guides: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Core SLIs

**Availability**

* Request success rate per region and per edge POP.
* Distinguish user cancellations, timeouts at connect, TLS, headers, body, tool call.

**Latency**

* End to end p50 p95 p99 by verb and route. Separate cold vs warm.
* Streaming time to first byte, and time to usable first chunk.

**RAG quality**

* ΔS(question, retrieved) and ΔS(retrieved, anchor section).
* Coverage to the target section.
* λ state across three paraphrases and two seeds.

**Cold start pressure**

* Cold start rate per minute. Concurrency utilization per function.

**Queues and webhooks**

* Backlog length, backlog age p50 p95.
* Outbound webhook success, retries, dedupe drops.

**Edge and cache**

* Cache hit ratio for hot prefixes. Invalidation lag.

**Index integrity**

* {INDEX\_HASH, METRIC, ANALYZER, BUILD\_TS} parity across regions.

---

## SLO examples you can adopt

* Availability SLO 99.5 percent monthly per region.
  Two burn windows: 2 hours and 30 days.

* Latency SLO p95 within 25 percent of baseline for served geography.
  Track separate SLOs for cold and warm.

* RAG SLO ΔS ≤ 0.45 and coverage ≥ 0.70 on a fixed probe set against production indices.
  λ convergent across three paraphrases.

* Webhook SLO 99 percent delivery within 90 seconds with no duplicates for a given `dedupe_key`.

* Queue SLO backlog age p95 ≤ 60 seconds during peak.

---

## Event schema to log on every request

```json
{
  "ts": "2025-08-27T06:21:45Z",
  "region": "eu-west",
  "edge_pop": "cdg",
  "route": "chat.rag.answer",
  "cold_start": false,
  "concurrency_util": 0.62,
  "latency_ms": { "tffb": 180, "tusable": 400, "tfinal": 1450 },
  "status": 200,
  "timeout_stage": null,
  "retrieval": {
    "k": 10,
    "metric": "cosine",
    "analyzer": "bilstem",
    "INDEX_HASH": "a9c1…",
    "ΔS_q_r": 0.31,
    "ΔS_r_anchor": 0.28,
    "coverage": 0.78,
    "λ_state": "<>"
  },
  "webhook": { "emitted": true, "tries": 1, "dedupe_key": "sha256(...)" },
  "queue": { "enq": 12, "deq": 12, "backlog": 3, "age_p95_ms": 4200 }
}
```

Keep PII out. Redact secrets at source.

---

## Dashboards that catch real incidents

* Availability and error breakdown by stage: connect, TLS, headers, body read, tool call.
* p50 p95 p99 latency split by cold and warm.
* Cold start rate and concurrency utilization.
* RAG probe board: ΔS histogram, coverage violin, λ flip count.
* Queue backlog and age percentiles with alarm lines.
* Webhook success and dedupe drops.
* Edge cache hit and purge counts per prefix.
* Index parity table per region showing `INDEX_HASH`.

---

## Burn rate alerts you can paste

**Availability budget**

* Error budget over 30 days: `EB = 1 - 0.995 = 0.005`
* High burn alert: 2 hour window where `burn = errors / requests > 14 * EB / 720`
* Slow burn alert: 24 hour window where `burn > 6 * EB / 720`

**Latency budget**

* Define baseline `p95_ref`. Alert when `p95_now > 1.25 * p95_ref` for 10 minutes and cold rate not the cause.

**RAG quality**

* Alert when ΔS median on probe set ≥ 0.60 or λ flips on more than 1 of 3 paraphrases.
* Gate deploy if coverage on probes < 0.70.

---

## Probes to run continuously

* **Three paraphrases per gold question**. Log ΔS, coverage, λ.
* **Two-seed repeat** for the same inputs. If answers flip, clamp variance using BBAM and lock snippet schema.
* **Anchor triangulation** against a decoy section to detect bad chunking.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Instrumentation tips per layer

* **Cold vs warm separation**
  Tag every invocation with `cold_start`. Keep distinct latency panels.
  Open: [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)

* **Timeout anatomy**
  Record stage where it failed. Add separate counters for connect, TLS, headers, body, tool.
  Open: [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)

* **Queues**
  Always report backlog and age percentiles. Alert on age, not only length.
  Open: [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md)

* **Edge caches**
  Expose purge counts and hit ratio by prefix and tenant.
  Open: [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

* **Region and routing**
  Add stickiness headers and show which region served. Log weights and hysteresis values.
  Open: [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md)

* **Egress and webhooks**
  Include `dedupe_key`, tries, final status, and emitter region.
  Open: [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

---

## Release gates that prevent regressions

* Block deploy if probe set fails any of: ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent.
* Block if p95 increased more than 25 percent at warm for 10 minutes.
* Block if cold start rate doubles against last week baseline.
* Block if `INDEX_HASH` changed but analyzer or metric changed silently.

---

## Escalate with the right fix

* Answers drift across regions → verify `INDEX_HASH`, rebuild, purge caches.
  Open: [Region Failover Drills](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/region_failover_drills.md)

* High similarity but wrong meaning → fix chunking and metrics.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Flip states on long chains → clamp with BBAM and shorten plans.
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) · [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

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

**Next page to write**: `ProblemMap/GlobalFixMap/Cloud_Serverless/canary_release_serverless.md`
