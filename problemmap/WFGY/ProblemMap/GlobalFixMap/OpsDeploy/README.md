<!--
Search Anchor:
ops and deploy global fix map
rag ops deployment playbook
llm rollout readiness gate
blue green switchover guardrails
vector index build and swap safety
cache warmup and invalidation rag
rate limit backpressure llm api
feature flags safe launch guardrails
idempotency and retry storms
rollback and fast recovery plan
release calendar and change freeze
incident comms and statuspage
shadow traffic mirroring rag
read only mode and maintenance window
db migration guardrails for rag

When to use this folder:
first calls after deploy crash or return stale content
delta s and citations looked fine yesterday but flip today
rate limits cascade queues spike and latency climbs
canary looks fine then full rollout breaks retrieval
index swap succeeds but answers cite old snippets
retries cause duplicate side effects or extra charges
feature flags bleed traffic into unfinished paths
maintenance windows corrupt embeddings or anchors
p95 latency leaves budget during rollout
model id or prompt rev changes silently
vector index and cache disagree on which corpus is live

Core pages in this folder:
ProblemMap/GlobalFixMap/OpsDeploy/README.md
ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md
ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md
ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md
ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md
ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md
ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md
ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md
ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md
ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md
ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md
ProblemMap/GlobalFixMap/OpsDeploy/rollback_and_fast_recovery.md
ProblemMap/GlobalFixMap/OpsDeploy/postmortem_and_regression_tests.md
ProblemMap/GlobalFixMap/OpsDeploy/release_calendar_and_change_freeze.md
ProblemMap/GlobalFixMap/OpsDeploy/incident_comms_and_statuspage.md
ProblemMap/GlobalFixMap/OpsDeploy/shadow_traffic_mirroring.md
ProblemMap/GlobalFixMap/OpsDeploy/read_only_mode_and_maintenance_window.md
ProblemMap/GlobalFixMap/OpsDeploy/db_migration_guardrails.md

Related structural fixes:
ProblemMap/rag-architecture-and-recovery.md
ProblemMap/retrieval-playbook.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/bootstrap-ordering.md
ProblemMap/deployment-deadlock.md
ProblemMap/predeploy-collapse.md
ProblemMap/ops/live_monitoring_rag.md
ProblemMap/ops/debug_playbook.md
ProblemMap/GlobalFixMap/EvalObservability/README.md
ProblemMap/GlobalFixMap/EvaluationGuardrails/README.md

Deployment scenarios:
rollout readiness for new rag pipeline
blue green cutover for retrievers or models
vector index swap with zero stale answers
cache warmup and invalidation at cutover
rate limit and backpressure under traffic spikes
feature flags and partial rollouts
idempotent write or billing paths under retry storms
retry backoff design to avoid thundering herd
fast rollback and recovery when metrics break
postmortem and regression tests after incidents
change freeze around launch windows
incident comms and statuspage updates
shadow traffic mirroring before going live
read only mode during maintenance windows
db migrations without breaking anchors
-->


# Ops & Deploy — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

A compact hub to **ship safely and keep RAG/LLM systems stable after release**.  
Use this folder to pick the right guardrail, verify with measurable targets, and recover fast when things wobble. No infra change required.

---



## Open these first
- Visual recovery map → [RAG Architecture & Recovery](../../rag-architecture-and-recovery.md)  
- Retrieval knobs end-to-end → [Retrieval Playbook](../../retrieval-playbook.md)  
- Traceability and snippet schema → [Retrieval Traceability](../../retrieval-traceability.md) · [Data Contracts](../../data-contracts.md)  
- Boot order and deploy traps → [Bootstrap Ordering](../../bootstrap-ordering.md) · [Deployment Deadlock](../../deployment-deadlock.md) · [Pre-Deploy Collapse](../../predeploy-collapse.md)  
- Live ops tools → [Live Monitoring for RAG](../../ops/live_monitoring_rag.md) · [Debug Playbook](../../ops/debug_playbook.md)  

---

## When to use this folder
- First calls after deploy crash or return stale content.  
- ΔS and citations look fine yesterday but flip today.  
- Rate limits cascade, queues spike, latency climbs.  
- Canary looks good then full rollout breaks retrieval.  
- Index swap succeeds but answers cite old snippets.  
- Retries cause duplicate side effects or charges.  
- Feature flags bleed traffic into unfinished paths.  
- Maintenance windows corrupt embeddings or anchors.  

---

## Acceptance targets for a safe rollout
- **ΔS(question, retrieved) ≤ 0.45** across three paraphrases.  
- **Coverage ≥ 0.70** on the expected new section.  
- **λ remains convergent** on 2 seeds during rollout.  
- **Idempotency ≥ 99.9%** on retry storms.  
- **Zero silent index mismatches** (hash + counts match).  
- **P95 latency stays in budget** with backpressure active.  

---

<!--
Anchor Menu:
open: ops and deploy readme ProblemMap/GlobalFixMap/OpsDeploy/README.md
open: rollout readiness gate page ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md
open: staged rollout canary page ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md
open: blue green switchovers page ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md
open: version pinning and model lock page ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md
open: vector index build and swap page ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md
open: cache warmup and invalidation page ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md
open: rate limit backpressure page ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md
open: feature flags safe launch page ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md
open: idempotency and dedupe page ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md
open: retry backoff page ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md
open: rollback and fast recovery page ProblemMap/GlobalFixMap/OpsDeploy/rollback_and_fast_recovery.md
open: postmortem and regression tests page ProblemMap/GlobalFixMap/OpsDeploy/postmortem_and_regression_tests.md
open: release calendar and change freeze page ProblemMap/GlobalFixMap/OpsDeploy/release_calendar_and_change_freeze.md
open: incident comms and statuspage page ProblemMap/GlobalFixMap/OpsDeploy/incident_comms_and_statuspage.md
open: shadow traffic mirroring page ProblemMap/GlobalFixMap/OpsDeploy/shadow_traffic_mirroring.md
open: read only mode and maintenance window page ProblemMap/GlobalFixMap/OpsDeploy/read_only_mode_and_maintenance_window.md
open: db migration guardrails page ProblemMap/GlobalFixMap/OpsDeploy/db_migration_guardrails.md

jump: rag architecture and recovery ProblemMap/rag-architecture-and-recovery.md
jump: retrieval playbook ProblemMap/retrieval-playbook.md
jump: retrieval traceability schema ProblemMap/retrieval-traceability.md
jump: data contracts snippet schema ProblemMap/data-contracts.md
jump: bootstrap ordering page ProblemMap/bootstrap-ordering.md
jump: deployment deadlock page ProblemMap/deployment-deadlock.md
jump: pre deploy collapse page ProblemMap/predeploy-collapse.md
jump: live monitoring for rag page ProblemMap/ops/live_monitoring_rag.md
jump: debug playbook page ProblemMap/ops/debug_playbook.md

jump: eval observability readme ProblemMap/GlobalFixMap/EvalObservability/README.md
jump: evaluation and guardrails readme ProblemMap/GlobalFixMap/EvaluationGuardrails/README.md
-->


## Quick routes — per-page guides

| Scenario | Fix Page |
|----------|----------|
| Rollout readiness | [rollout_readiness_gate.md](./rollout_readiness_gate.md) |
| Canary strategy | [staged_rollout_canary.md](./staged_rollout_canary.md) |
| Blue/green cutover | [blue_green_switchovers.md](./blue_green_switchovers.md) |
| Version pin & freeze | [version_pinning_and_model_lock.md](./version_pinning_and_model_lock.md) |
| Vector index swap | [vector_index_build_and_swap.md](./vector_index_build_and_swap.md) |
| Cache warmup | [cache_warmup_invalidation.md](./cache_warmup_invalidation.md) |
| Rate limits | [rate_limit_backpressure.md](./rate_limit_backpressure.md) |
| Feature flags | [feature_flags_safe_launch.md](./feature_flags_safe_launch.md) |
| Idempotency | [idempotency_dedupe.md](./idempotency_dedupe.md) |
| Retry logic | [retry_backoff.md](./retry_backoff.md) |
| Rollback plan | [rollback_and_fast_recovery.md](./rollback_and_fast_recovery.md) |
| Postmortems | [postmortem_and_regression_tests.md](./postmortem_and_regression_tests.md) |
| Change freeze | [release_calendar_and_change_freeze.md](./release_calendar_and_change_freeze.md) |
| Incident comms | [incident_comms_and_statuspage.md](./incident_comms_and_statuspage.md) |
| Shadow traffic | [shadow_traffic_mirroring.md](./shadow_traffic_mirroring.md) |
| Maintenance window | [read_only_mode_and_maintenance_window.md](./read_only_mode_and_maintenance_window.md) |
| DB migrations | [db_migration_guardrails.md](./db_migration_guardrails.md) |

---

## 60-second ship checklist

1. **Freeze the world** → Pin model IDs, prompt revs, index hashes.  
2. **Warm up safely** → Build index off-path, preload caches with canary.  
3. **Shadow then canary** → Mirror prod queries, step rollout 5% → 25% → 100%.  
4. **Guard the edge** → Enable backpressure, retries with jitter, idempotency keys.  
5. **Know your exit** → Keep rollback switch and comms draft ready.  

---

## Symptoms → exact fix

| What you see | Open this |
|--------------|-----------|
| Deploy points to old snippets | [vector_index_build_and_swap.md](./vector_index_build_and_swap.md) · [cache_warmup_invalidation.md](./cache_warmup_invalidation.md) |
| Canary fine, full rollout breaks | [staged_rollout_canary.md](./staged_rollout_canary.md) · [feature_flags_safe_launch.md](./feature_flags_safe_launch.md) |
| Wrong model after failover | [version_pinning_and_model_lock.md](./version_pinning_and_model_lock.md) |
| Retries duplicate charges | [idempotency_dedupe.md](./idempotency_dedupe.md) · [retry_backoff.md](./retry_backoff.md) |
| RL storms, timeouts | [rate_limit_backpressure.md](./rate_limit_backpressure.md) |
| Need rollback now | [rollback_and_fast_recovery.md](./rollback_and_fast_recovery.md) · [blue_green_switchovers.md](./blue_green_switchovers.md) |
| Maintenance corrupts anchors | [read_only_mode_and_maintenance_window.md](./read_only_mode_and_maintenance_window.md) · [db_migration_guardrails.md](./db_migration_guardrails.md) |
| Unsure if safe to ship | [rollout_readiness_gate.md](./rollout_readiness_gate.md) |

---

## FAQ

**Q: What does ΔS mean here?**  
A: ΔS is a stability score. It measures how much the retrieved content drifts from the expected anchor when you change the query slightly. Lower is better (≤ 0.45 is safe).  

**Q: What is λ convergence?**  
A: λ tracks whether retrieval order flips unpredictably. If λ is stable across seeds, your rollout is consistent.  

**Q: Why do I need idempotency keys?**  
A: Without them, retries can double-charge a user or run the same side-effect twice. Keys make every request “safe to retry.”  

**Q: How do I know if my index swap worked?**  
A: Check doc counts and hashes before cutover. If they mismatch, you’re pointing at an incomplete index.  

**Q: Canary looked fine but production broke — why?**  
A: Canary often hides tail-latency, cache misses, or load-based rate limits. Always test at increasing % of live traffic.  

**Q: Why do you mention rollback comms?**  
A: Technical rollback is only half. Users and stakeholders need fast updates, so pre-draft Statuspage or Slack messages are essential.  

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

