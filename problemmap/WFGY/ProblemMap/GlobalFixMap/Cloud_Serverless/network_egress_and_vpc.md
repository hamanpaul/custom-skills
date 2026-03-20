# Network Egress and VPC — Guardrails

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


Keep serverless outbound traffic predictable and cheap. This page fixes DNS flakiness, NAT bottlenecks, blocked endpoints, and cross-region surprises that break RAG calls, vector writes, and webhook posts.

## When to use this page

* Lambdas or Cloud Run randomly time out on first external call.
* Only production fails because it runs inside a VPC or private subnet.
* Costs jump after moving to NAT or a new region.
* Vector DB reachable from dev, unreachable from prod.
* Long tail latency grows after scale up or during deploys.

## Open these first

* Boot order and release safety: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* Deploy waves that deadlock I/O: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
* First call fails after rollout: [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Auditable payload and endpoint contracts: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live probes and rollback signals: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* RAG wide view for outbound calls: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

## Acceptance targets

* p95 DNS lookup ≤ 30 ms and connection setup ≤ 120 ms per request.
* NAT or egress gateway active connections ≤ 70 percent of max for steady state.
* Cross region egress ratio ≤ 5 percent of total requests after pinning.
* Socket error rate ≤ 0.1 percent with retries and idempotency keys enabled.

---

## Fix in 60 seconds

1. **Pin the path**

   * Resolve targets to regional endpoints. Prefer private endpoints or service networking where offered.
   * Add allowlist and block outbound to unknown hosts.

2. **Stabilize resolution and connect**

   * Enable connection pooling and keep-alive.
   * Cache DNS for short TTLs in runtime, and rotate resolvers only on failure.

3. **Choose the right egress shape**

   * Small constant QPS → serverless NAT or egress gateway.
   * Spiky or chat streaming → dedicated NAT with connection headroom.

4. **Retry only what is safe**

   * Use idempotency keys for POST.
   * Exponential backoff with jitter. Cap total retry time below request timeout.

5. **Observe and clamp**

   * Emit `dns_ms`, `tcp_connect_ms`, `tls_ms`, `ttfb_ms`, `status`, `retry_count`.
   * Trip a circuit when connect errors exceed threshold. Route to regional fallback.

---

## Typical breakpoints → exact fix

* **Dev works, prod inside VPC cannot reach external API**
  Missing route or NACL block. Add NAT or egress gateway with explicit route table. Verify with regional probes.
  Open: [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Cold starts get slow after VPC attach**
  ENI allocation adds latency. Reduce subnets, enable provisioned concurrency for hot paths, and pool connections at handler scope.

* **DNS timeouts during traffic spikes**
  Resolver throttling or missing cache. Enable a runtime DNS cache and set low negative TTL. Monitor `dns_ms`.

* **Cross region vector writes**
  Endpoint is global but peered to a distant region. Replace with regional endpoint and pin by environment variable.

* **NAT port exhaustion**
  Too many simultaneous connects with short keep-alive. Increase keep-alive to reuse sockets and scale NAT capacity.

---

## Minimal recipes you can copy

### A) AWS Lambda to external API through NAT

```txt
VPC subnets: 2 private + 2 AZs
Route table: 0.0.0.0/0 → NAT gateway
Security group: egress 443 allowlist to api.vendor.com
Runtime
- HTTP agent keepAlive=true, maxSockets=per-function target
- DNS cache with TTL obeying 30–60 s
- Retries: 3 with jitter, idempotency key on POST
Metrics
- dns_ms, connect_ms, tls_ms, ttfb_ms, bytes_out, bytes_in
```

### B) GCP Cloud Run with Serverless VPC Connector

```txt
Connector: min instances ≥ 2, autoscale up to peak QPS
Routes: only private ranges through connector, public stays direct
Env pins: API_HOST=api-ap-southeast1.vendor.com
Timeouts: request 120 s, connect 5 s, read 60 s
```

### C) Azure Functions with VNet integration

```txt
Regional private endpoint to storage and vector DB
NAT gateway attached to subnet with enough SNAT ports
Outbound allowlist to model provider and webhook targets
```

### D) Private service endpoints for data stores

```txt
Prefer:
- AWS PrivateLink to vector store or search
- GCP Private Service Connect for managed endpoints
- Azure Private Endpoint to PaaS databases

Disable public ingress on the target service once private is verified.
```

### E) Connection pooling pattern

```txt
// Create once at module scope
const agent = new Agent({ keepAlive: true, maxSockets: 256 })
// Reuse per invocation
fetch(url, { agent, signal, headers: { "Idempotency-Key": key } })
```

---

## Observability you must add

* Percent of requests by region and by endpoint.
* `dns_ms`, `connect_ms`, `tls_ms`, `ttfb_ms` histograms.
* NAT utilization, active connections, allocated ports.
* Cross region egress cost meter for early alerts.
* Circuit breaker state and fallback hit counts.

## Verification

* Regional canary proves pinned endpoint is used.
* p95 connect settles under the target after keep-alive and DNS cache.
* No cross region traffic after endpoint pin.
* Retries do not duplicate writes due to idempotency.

## When to escalate

* Persistent connect errors in one region → route reads to nearest healthy region, queue writes for the home region.
* NAT saturation → split subnets, add more NAT, or move heavy flows to a fixed egress gateway.
* Vendor rate limits → enable token bucket per host and raise backoff caps.

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

