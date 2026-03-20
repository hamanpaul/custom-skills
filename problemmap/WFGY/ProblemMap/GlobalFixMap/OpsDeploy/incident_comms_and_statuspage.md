# Incident Communications and Status Page: OpsDeploy Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OpsDeploy**.  
  > To reorient, go back here:  
  >
  > - [**OpsDeploy** — operations automation and deployment pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Clear comms reduce panic and shorten incidents. Use this page to script your updates, pick the right status, and keep owners and users aligned while you fix the root cause.

---

## Open these first
- Live telemetry and runbook: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
- Rollback tools: [rollback_and_fast_recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollback_and_fast_recovery.md)
- Rollout controls: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md), [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md), [feature_flags_safe_launch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md)
- Pins and caches: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md), [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Load and retries: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)
- After action: [postmortem_and_regression_tests.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/postmortem_and_regression_tests.md)

---

## When to use
- Error rate passes 0.5 percent for more than five minutes.  
- p99 latency doubles for read paths.  
- 429 storms or provider 5xx that persist after backoff.  
- Mixed answers across versions or bad citations appear.  
- Any rollback lever is considered or pulled.

---

## Severity ladder
| Sev | User impact | Default status page state |
|---|---|---|
| S1 | Major outage, most users blocked | Major outage |
| S2 | Partial outage, degraded answers or timeouts | Degraded performance |
| S3 | Narrow scope, one region or one feature | Partial outage |
| S4 | Advisory only, no user breakage | Monitoring or Informational |

Pick the lowest sev that still describes actual user pain.

---

## Acceptance targets for comms
- First external update in 10 minutes or less after trigger.  
- Update cadence every 15 to 20 minutes until stable, then every 30 minutes.  
- Status page always matches the in product banner.  
- Each update carries owner, scope, current user effect, next checkpoint time.  
- After resolve, publish a short cause and a link to the postmortem ticket.

---

## 60 second comms plan
1) Assign roles fast. Incident lead, Comms lead, Support lead, SRE on call.  
2) Set the initial state on the status page. Choose S1 to S4.  
3) Post the first update. Acknowledge impact. Say what users can expect next.  
4) Pin an in product banner on affected surfaces.  
5) Keep a 15 minute timer. Post deltas not fluff.  
6) When quality targets are green, move state to monitoring.  
7) On resolve, post the user visible fix and next steps. Link the postmortem page when ready.

---

## Status page states and triggers
| State | What users see | Typical trigger |
|---|---|---|
| Degraded performance | slow answers or sometimes wrong citations | ΔS p95 drift rising yet under rollback bar, p95 latency up 20 percent |
| Partial outage | some features fail, retries help | one region down, one tool chain failing |
| Major outage | most requests fail or unusable answers | rollback in progress, provider wide failure |
| Maintenance | planned or emergency work | change freeze exception, hotfix rollout |

ΔS and coverage are internal gates. Do not expose raw numbers to users.

---

## Message templates

### Initial acknowledgement
```text
We are investigating an incident affecting AI answers. Users may see slow responses or missing citations. The team has engaged rollback options and is validating recovery steps now. Next update in 15 minutes.
````

### Ongoing update

```text
Mitigation is in progress. We reduced traffic to the new model and restored the previous index for two regions. Errors are trending down and response time is improving. Next checkpoint at hh:mm UTC.
```

### Identified cause

```text
We identified a mismatch between cache keys and the new index pointer. This caused mixed answers. We rotated the cache namespace and warmed hot paths. Monitoring continues.
```

### Resolved

```text
This incident is resolved. Answers and citations are stable. We will publish a brief write up and the prevention steps. Thank you for your patience.
```

### Postmortem scheduled

```text
A postmortem is scheduled. We will share the timeline, the root cause, and changes that prevent recurrence. Target publish within 48 hours.
```

---

## In product banner copy

Short. Actionable. Example:

```text
Some AI answers may be slow or incomplete right now. We are restoring normal service. No action needed by you.
```

Add a link to the status page entry.

---

## Internal notification matrix

| Audience      | Channel                           | What to include                               |
| ------------- | --------------------------------- | --------------------------------------------- |
| Exec on call  | paging plus chat room             | sev, scope, owner, ETA for next checkpoint    |
| Support       | help center macro and status link | what users experience, safe workaround if any |
| Sales and CSM | email bulletin or room            | who is affected, what to tell customers       |
| Eng org       | incident room topic               | technical progress and rollback lever status  |

Keep one source of truth. Everything else points to it.

---

## Evidence to log for comms

* Timestamps of each public update.
* Status page state changes and who changed them.
* Link to the exact pins in effect during each window.
* ΔS, coverage, λ snapshots that drove decisions.
* Rollback time, cache namespace, region scope.
* Final resolve time and the postmortem ticket id.

---

## Common pitfalls

* Silence while engineers work. Post small deltas on time.
* Status page says green while the banner says yellow. Keep them aligned.
* Promising exact ETAs. Promise the next checkpoint time instead.
* Over sharing internals. Users need effect and recovery, not raw metrics.
* Forgetting to remove the banner after resolve.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

