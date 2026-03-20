# Blue-Green Switchovers for Serverless and Edge

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


A safe pattern to shift 100 percent of live traffic from **blue** to **green** without downtime, cache poison, or state skew. Works for API Gateway + Lambda, Cloudflare Workers, Vercel Edge, Fastly Compute, and similar stacks.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Snippet trace and contracts: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Meaning vs distance: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Collapse diagnostics: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) · [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Cloud companions:
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
  [Observability and SLO](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md) ·
  [Canary Release](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/canary_release_serverless.md)

---

## Core acceptance to flip colors

* ΔS(question, retrieved) median ≤ 0.45 on gold probes.
* Coverage ≥ 0.70 to correct section.
* λ convergent across three paraphrases and two seeds.
* p95 warm latency within 25 percent of blue.
* Zero new error class at headers or body read.
* Cache hit rate within five points once namespaces are split.
* `INDEX_HASH`, metric, analyzer match between blue and green or are intentionally versioned.

---

## Topologies that work

**Edge weight switch**

* One CDN route, two origins. Blue and green behind a weight.
* Keep **sticky hashing** by `stable_user_id` so dialogs do not jump during ramp.

**Header based switch**

* Default to blue. Send `x-exp: green` for selected cohorts.
* Propagate header to core services and logs.

**DNS label switch**

* `api-blue.example.com` and `api-green.example.com`.
* Edge forwards based on label. Use short TTL only after green passes probes.

---

## Pre-flight checklist

* **Env parity** proved with the parity sheet. Open: [Runtime Env Parity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/runtime_env_parity.md)
* **Secret bundles** rotated with overlap. Open: [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md)
* **Index family** built and labeled: `docs-v3-green`, analyzer and metric recorded.
* **Cache namespaces** isolated: `blue:` vs `green:` prefixes at edge and core.
* **Queue topics** duplicated: `jobs.blue` and `jobs.green`. Producers switch at flip time with idempotent keys. Open: [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md)
* **Probe set** ready: 50 to 200 questions, three paraphrases, two seeds.

---

## Switch playbook

1. **Shadow validate**
   Replay a sample to green. Block promotion if ΔS ≥ 0.60, coverage < 0.70, or JSON schema violations.

2. **Canary ramp**
   Move one percent of sticky users to green at the edge. Keep cache namespaces split.
   Open: [Canary Release](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/canary_release_serverless.md)

3. **Green warmup**
   Ensure cold start panels are flat. If p95 warm is worse only due to cold, fix memory or reserve concurrency.
   Open: [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)

4. **Cutover window**

   * Freeze new blue writes that create cross request state.
   * Drain blue job queues with a backfill guard.
   * Switch producers to `jobs.green`.
   * Flip traffic weight to green. Keep blue read only for a short fence window.

5. **Cache migration**

   * Invalidate user facing keys on the blue prefix.
   * Prime green with popular keys.
     Open: [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

6. **Post cutover audit**

   * Compare ΔS, coverage, λ, p95 warm to pre-flip baselines.
   * Verify `INDEX_HASH` and analyzer match.
   * Confirm egress success rate and dedupe guard.
     Open: [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

7. **Decommission blue**

   * Stop accepting writes.
   * Keep blue for rollback until probe board stays green for one peak hour.

---

## Data and state guidance

* **Databases**
  Prefer live backward compatible migrations. If you need forward only, pause blue writes to the affected tables during the flip.

* **Vector indexes**
  Version by family. Never point green to blue vectors by accident. Verify metric and analyzer, not only the hash.

* **Queues and schedulers**
  Idempotent keys: `sha256(source_id + revision + index_hash)`.
  Keep retry policies aligned across colors.

* **Caches**
  Always split prefixes. Never reuse the blue prefix for green.

---

## Observability fields to join on

```json
{
  "ts": "2025-08-28T04:00:00Z",
  "route": "chat.rag.answer",
  "color": "green",
  "sticky": "h21",
  "region": "eu-west",
  "edge_pop": "cdg",
  "INDEX_HASH": "0x9a77",
  "retrieval": { "metric": "cosine", "analyzer": "bilstem", "ΔS_q_r": 0.36, "coverage": 0.74, "λ_state": "<>" },
  "cache": { "prefix": "green:", "hit": true },
  "status": 200,
  "latency_ms": { "tffb": 140, "tusable": 320, "tfinal": 1180 }
}
```

---

## Rollback cookbook

* ΔS rises or coverage drops
  Repoint traffic to blue, keep green read only. Rebuild index with the chunking checklist.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) · [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking_checklist.md)

* Latency spike at body read
  Increase memory or reserve concurrency. Adjust stream chunk sizes.
  Open: [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)

* First call after switch fails
  Check boot order and version skew.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* Tool loops start
  Lock tool schemas and timeouts, split memory namespaces.
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Common traps

* Mixing cache prefixes so users see stale blue answers after the flip.
* DNS TTL set short before green is warm.
* Single region green while blue is multi region.
* Reranker versions differ between colors.
* Secrets rotated on edge but not core.

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

