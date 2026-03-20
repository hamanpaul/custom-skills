# Serverless Limits Matrix and Safe Budgets

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


A compact cheat-sheet to keep your RAG and agent flows inside the real limits of each serverless stack. Use this to set safe budgets for time, payload, memory, concurrency, and streaming so you never ship a workflow that silently truncates or times out.

## When to use this page

* “Works locally” but 413/414/431/502 appear in cloud.
* Streams cut around 55–60 seconds even though your function says 300.
* Vector writes fail only under load due to soft concurrency ceilings.
* JSON mode breaks on large tool outputs or long citations.
* Cold starts spike latency after deploy or scale-out.

## Open these first

* End-to-end runtime ceilings: [Timeouts and Streaming Limits](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)
* Cold starts, concurrency, provisioned capacity: [Cold Start and Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)
* Idempotency for retries and queues: [Stateless KV and Queue Patterns](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md)
* Retrieval correctness under truncation: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live probes and rollback: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Acceptance targets

* Effective timeout budget computed and enforced at build time. No 5xx raised by upstream timeouts in synthetic probes.
* p95 response size ≤ 70% of smallest body limit across the path.
* Zero occurrences of 413/414/431 in production after rollout.
* For RAG: no citation truncation, ΔS(question, retrieved) ≤ 0.45 on the probe set.

---

## Compute your real budgets first

**Rule of minimums**
The effective limit is the strictest element across the full path.

```
effective_timeout  = min( client_timeout,
                           edge/LB_timeout,
                           gateway_timeout,
                           function_timeout,
                           upstream_model_timeout )

effective_body_in  = min( client_upload_limit,
                           edge_header_limit + body_limit,
                           gateway_body_limit,
                           function_memory_and_tmp,
                           parser/frame limits )

effective_body_out = min( upstream_chunking,
                           function_response_limit,
                           compression_window,
                           edge/LB_response_limit,
                           client_reader_limit )
```

**Quick mapping tips**

* Headers often cap at 8–16 KB. Large auth payloads or tool schemas can hit 431. Collapse headers and move contracts into the body.
* Many edges proxy WebSocket and SSE differently. Budget for the stricter one when you stream.
* Body limits interact with memory. If your platform ties CPU to memory, raising memory may fix both CPU starvation and output buffering.

---

## The limits you must record per platform

Track these keys for each provider you deploy to. Do not hardcode numbers inside app code. Read from env or a small JSON and ship it with your release.

```
{
  "provider": "cloudflare|vercel|aws_lambda|gcp_cf|cloud_run|azure_f|fly|netlify",
  "region": "ap-southeast-1",
  "timeout_ms": 30000,
  "stream_idle_ms": 120000,
  "concurrency": {
    "soft": 100,
    "burst": 500,
    "account_ceiling_hint": "ticket required to raise beyond soft"
  },
  "memory_mb": 1024,
  "tmp_storage_mb": 512,
  "body_in_mb": 5,
  "body_out_mb": 6,
  "headers_kb": 8,
  "ws_supported": true,
  "sse_supported": true,
  "retry_semantics": "at_least_once|at_most_once",
  "notes": "anycast edge, drains needed for region flips"
}
```

Store per-route overrides. For example, upload routes differ from chat routes.

---

## Copy-paste validator for CI

Add a tiny test that fails builds if you exceed the smallest limit across all active deployments.

```txt
Inputs:
- ROUTES.json with {route, path, needs_stream, max_req_mb, max_resp_mb, target_p95_ms}
- LIMITS.json per environment as in the schema above

Check:
1) For each route, timeout_budget = min(all provider timeout_ms) - drain_safety_ms
   Assert target_p95_ms ≤ 0.7 * timeout_budget
2) Assert route.max_req_mb ≤ min(body_in_mb across providers) * 0.7
3) Assert route.max_resp_mb ≤ min(body_out_mb across providers) * 0.7
4) If needs_stream == true → assert all providers sse_supported == true and stream_idle_ms ≥ target_window
5) If concurrency soft < expected peak → require provisioned capacity plan

Fail with a one-line tip including the smallest limiting provider.
```

---

## Typical failure patterns → exact fix

* **413 Payload Too Large on uploads or tool schemas**
  Shrink request body. Move oversized JSON schemas to a versioned blob, reference by id.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **431 Request Header Fields Too Large**
  Headers grew due to long auth tokens or excessive trace keys. Collapse to a single compact header.
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) to lock tool schema and avoid header bloat.

* **Streams end at a fixed wall clock**
  You hit edge or LB idle timeout. Use heartbeat frames every N seconds and lower per-frame payload to keep buffers small.
  Open: [Timeouts and Streaming Limits](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)

* **JSON mode breaks on long citations**
  Response body exceeded a proxy frame or you buffered the whole stream. Switch to chunked JSON lines with cite-then-explain and a strict schema.
  Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* **Burst traffic returns 429 despite “unlimited” concurrency**
  Account or regional soft limits apply. Pre-warm with provisioned capacity and gate at the queue producer using idempotency keys.
  Open: [Cold Start and Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) · [KV and Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md)

---

## Pattern: budget table you can paste in a repo

Create `infra/limits/<env>.json` and keep it close to code. Example skeleton for a dual-provider rollout:

```json
{
  "env": "prod-2025-08-27",
  "providers": [
    {
      "provider": "aws_lambda",
      "region": "ap-southeast-1",
      "timeout_ms": 30000,
      "stream_idle_ms": 120000,
      "concurrency": { "soft": 150, "burst": 500 },
      "memory_mb": 1024,
      "tmp_storage_mb": 512,
      "body_in_mb": 6,
      "body_out_mb": 6,
      "headers_kb": 8,
      "ws_supported": false,
      "sse_supported": true,
      "retry_semantics": "at_least_once",
      "notes": "ALB behind API GW, drain on deploy"
    },
    {
      "provider": "cloudflare",
      "region": "global-anycast",
      "timeout_ms": 30000,
      "stream_idle_ms": 120000,
      "concurrency": { "soft": 1000, "burst": 5000 },
      "memory_mb": 256,
      "tmp_storage_mb": 0,
      "body_in_mb": 10,
      "body_out_mb": 10,
      "headers_kb": 8,
      "ws_supported": true,
      "sse_supported": true,
      "retry_semantics": "at_most_once",
      "notes": "Edge streams, pin region on long flows"
    }
  ]
}
```

Then let CI compute the minimums and fail fast if your routes exceed them.

---

## Observability you should add

* Per-route histograms for payload in/out.
* Count of 413/414/431 and which hop returned them.
* Stream lifetime distribution and idle gaps.
* Cold start count and warm pool utilization.
* Queue age and rejection rate when concurrency caps.

## Verification

* Synthetic routes produce zero 413/431.
* Stream probes survive at least 2× your target window.
* p95 stays below 70% of the smallest timeout limit after rollout.
* RAG probe set shows no truncation of citations.

## When to escalate

* Repeated 502/504 with flat app CPU. You are hitting proxy timeouts. Lower hop count or raise edge timeout where possible, otherwise split the plan.
* Body out is the wall. Switch to paged responses or chunked JSON lines with a cite index.

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

