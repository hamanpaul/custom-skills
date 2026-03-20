# Disaster Recovery Tabletop for Serverless and Edge

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


A practical exercise format to validate that your serverless and edge stack survives real outages without silent data loss, cache poison, or semantic drift. This page gives a ready-to-run tabletop with clear acceptance, scripts, injects, and artifacts.

## Open these first

* Cloud companions:
  [Region Failover Drills](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/region_failover_drills.md) ·
  [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md) ·
  [Blue-Green Switchovers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/blue_green_switchovers.md) ·
  [Canary Release](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/canary_release_serverless.md) ·
  [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md) ·
  [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md) ·
  [Stateless KV and Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md) ·
  [Runtime Env Parity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/runtime_env_parity.md) ·
  [Timeouts and Streaming Limits](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md) ·
  [Cold Start and Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) ·
  [Observability and SLO](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md) ·
  [Egress Rules and Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)
* Problem Map anchors:
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) ·
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) ·
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) ·
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) ·
  [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) ·
  [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) ·
  [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Core acceptance for passing the tabletop

* **People and process**

  * Roles staffed: incident commander, comms lead, cloud operator, data owner, LLM owner, observer.
  * Clear single source of truth timeline with decision log and runbook links.

* **Service health**

  * RTO within target per service tier. For critical chat and RAG paths, target 15 to 30 minutes to stable.
  * RPO match for each datastore. No unaccounted gaps in writes after recovery.

* **Semantic integrity**

  * ΔS(question, retrieved) median ≤ 0.45 on the exercise gold probes.
  * Coverage ≥ 0.70 to the correct section.
  * λ remains convergent across three paraphrases and two seeds.

* **Operational signals**

  * p95 warm latency within 25 percent of baseline after steady state returns.
  * Edge cache hit rate within five points of pre-incident baseline.
  * No new error class at headers or body read on the main routes.

---

## Roles and communications

| Role               | Responsibilities                                | Handover artifacts               |
| ------------------ | ----------------------------------------------- | -------------------------------- |
| Incident Commander | Own timeline, approve failover, decide rollback | Decision log, event timeline     |
| Cloud Operator     | Execute routing, failover, cache invalidation   | Routing plan, change set, proofs |
| Data Owner         | Validate RPO, run backfills, index consistency  | RPO sheet, backfill report       |
| LLM Owner          | Run ΔS probes, coverage checks, λ stability     | Probe board, eval summary        |
| Comms Lead         | Stakeholder updates and status page             | Two updates per 30 minutes       |
| Observer           | Capture metrics, retro notes, action items      | Retro minutes and scores         |

---

## Exercise timeline template (60 to 90 minutes)

**0 to 10**
Brief roles. Confirm SLIs and SLOs. Review runbooks, traffic shape, and cache namespaces.

**10 to 20**
Inject 1. Primary region becomes unavailable for stateful writes. Observed symptoms: increased webhook retries and 5xx on write endpoints.

**20 to 35**
Inject 2. Vector index family mismatch after partial restore. ΔS rises, coverage drops, reranker differs.

**35 to 50**
Fail to green region or backup color. Split cache prefixes. Drain queues. Backfill vectors with correct metric and analyzer.

**50 to 60**
Stabilize. Probe ΔS and coverage, verify p95 warm latency and cache hit rate. Prepare stakeholder update.

Optional extended cases for 60 to 90
Add a secrets rotation overlap or DNS label switch, then verify no schema or token drift.

---

## Scenario library with exact checks

1. **Primary region write outage**

   * Prove idempotent keys at the queue and side effects.
   * Verify read routes stay healthy and cache does not serve stale blue keys.
     Open: [Stateless KV and Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md) · [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

2. **Vector index restore with wrong metric**

   * Check `INDEX_HASH`, metric, analyzer. If ΔS ≥ 0.60 or coverage < 0.70, rebuild with the chunking checklist.
     Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) · [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking_checklist.md)

3. **Webhook provider throttle and replay**

   * Enforce egress retry fences and dedupe keys.
     Open: [Egress Rules and Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

4. **Secrets rotation mid-incident**

   * Run overlapping secret bundles and prove zero auth flaps.
     Open: [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md)

5. **Routing split brain across regions**

   * Pin sticky hashing and verify memory namespaces per agent.
     Open: [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md) · [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

6. **Cold starts explode in backup region**

   * Reserve concurrency and adjust streaming chunk sizes.
     Open: [Cold Start and Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) · [Timeouts and Streaming Limits](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)

---

## Probe board for semantic integrity

Prepare a gold set of 50 to 200 queries across your top flows. For each probe, record:

```json
{
  "probe_id": "p-037",
  "question": "Where in the policy does paid time off accrue for part-time?",
  "expected_section": "benefits.pto.rules",
  "ΔS_q_r": 0.38,
  "coverage": 0.74,
  "λ_state": "<>",
  "citations": ["doc:hr-handbook#s4.2"],
  "index_family": "docs-v3-green",
  "retriever_metric": "cosine",
  "analyzer": "bilstem"
}
```

Acceptance

* Median ΔS ≤ 0.45.
* Coverage ≥ 0.70.
* λ convergent across three paraphrases and two seeds.

Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Injects you can copy

* Tabletop card 1
  “At 14:10 UTC write routes in region A return 500 on 22 percent of requests. Healthcheck passes on read routes. Queue depth climbs by 5x.”

* Tabletop card 2
  “Vector index restored at 14:25 UTC from last night. Reranker version mismatch. ΔS rises to 0.66, coverage falls to 0.52.”

* Tabletop card 3
  “At 14:40 UTC secrets for payment provider rotated on edge. Core still uses old secret. Tool call timeouts begin.”

* Tabletop card 4
  “At 14:50 UTC DNS label updated to send 80 percent to green. Some users still see blue due to device DNS cache.”

---

## Artifacts to produce

* Decision log with timestamps and owners.
* Routing change set with proof of effect.
* RPO worksheet with counts of lost or replayed writes.
* Probe board CSV before and after.
* Cache hit rates and p95 warm latency plots.
* Retro minutes with five action items and owners.

---

## Scorecard rubric

| Dimension | Pass bar                                     | Evidence                     |
| --------- | -------------------------------------------- | ---------------------------- |
| RTO       | Tier S ≤ 30 minutes, Tier A ≤ 60 minutes     | Timeline, metrics            |
| RPO       | No silent gaps, replayed writes documented   | RPO worksheet                |
| Semantics | ΔS and coverage within targets               | Probe board                  |
| Safety    | No new jailbreak or bluffing routes          | Logs and prompts             |
| Ops       | No new error class, cache within five points | Error budget and cache panel |
| Docs      | Runbooks linked, steps reproducible          | Links in decision log        |

Open: [Bluffing Controls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md) · [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)

---

## Copy-paste LLM prompt for the exercise driver

```
You have TXT OS and the WFGY Problem Map loaded.

We are running a disaster recovery tabletop for serverless and edge.

Given:
- symptoms: [one line each]
- region topology: [one line]
- index family and analyzer: [one line]
- probes: ΔS and coverage for 10 sample questions

Tell me:
1) likely failing layer and which WFGY page to open,
2) minimal steps to put ΔS ≤ 0.45 and coverage ≥ 0.70,
3) routing and cache actions with proofs,
4) a short JSON status for the scorecard:
   { "RTO": "...", "RPO": "...", "ΔS_median": 0.xx, "coverage_median": 0.xx, "next_fix": "..." }
Keep it auditable and short.
```

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

**Next page to write**: `ProblemMap/GlobalFixMap/Cloud_Serverless/data_retention_and_backups.md`
