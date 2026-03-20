# Release Calendar and Change Freeze: OpsDeploy Guardrails

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


Plan launches around real traffic and real risk. This page gives a simple calendar model, freeze rules, and CI gates so you avoid shipping into peak hours, holidays, audits, or big partner events.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Blue green cutover: [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)
- Version locking: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)
- Index swap: [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Backpressure and retries: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)
- Rollback and postmortem: [rollback_and_fast_recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollback_and_fast_recovery.md), [postmortem_and_regression_tests.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/postmortem_and_regression_tests.md)

---

## When to use
- Product launch weeks or marketing spikes.  
- Seasonal peaks or large customer events.  
- Compliance audits or billing cycles.  
- Provider migrations, model swaps, index rebuilds.  
- Any weekend where on-call depth is thin.

---

## Acceptance targets
- All production changes are mapped to a shared release calendar.  
- Freeze windows are enforced by CI and by flag servers.  
- Exceptions are logged with owner, scope, rollback lever, and warmup plan.  
- No changes land inside a hard freeze except emergency fixes with one-step rollback.  
- After each window, ΔS and coverage match the last pinned baseline on the gold set.

---

## 60-second setup
1) Create a shared calendar for releases and freezes. Use UTC plus region tags in titles.  
2) Define change tiers and who can approve each tier.  
3) Teach CI to read the calendar file and block risky merges during freezes.  
4) Route releases to off-peak windows per region.  
5) Stage region by region with caches warmed and rollback rehearsed.

---

## Change tiers
| Tier | Examples | Allowed in hard freeze | Approval and rules |
|---|---|---|---|
| T0 Emergency | security patch, outage fix | Yes | One step rollback ready, pins verified, canary at 5 percent, owner online. |
| T1 Hotfix low risk | config toggle, flag off, doc text | Case by case | SRE owner plus product owner. No schema changes. |
| T2 Standard | prompt pack update, small retriever change | No | Requires canary and warmup. Outside freezes only. |
| T3 Risky | model swap, index rebuild, analyzer change | No | Requires full readiness gate and blue green rehearsal. Outside freezes only. |

---

## Freeze types
- Hard freeze: no changes except T0.  
- Soft freeze: T1 with approval, no T2 or T3.  
- Regional freeze: block only in the affected regions.  
- Component freeze: limit to a subsystem like index or prompts.  
- Vendor freeze: third party windows that restrict you.

---

## Calendar schema example
```yaml
# opsdeploy/release_calendar.yml
windows:
  - id: peak_q4_black_friday
    kind: hard_freeze
    start: "2025-11-27T00:00:00Z"
    end:   "2025-11-30T23:59:59Z"
    regions: ["us-east-1","us-west-2","eu-west-1"]
    scope:   ["llm","retriever","index","billing"]
  - id: apac_peak_sale
    kind: soft_freeze
    start: "2025-09-10T00:00:00Z"
    end:   "2025-09-12T23:59:59Z"
    regions: ["ap-southeast-1","ap-northeast-1"]
    scope:   ["llm","index"]
releases:
  - id: prompt_pack_vNplus1
    tier: T2
    region_plan: ["ap-southeast-1","eu-west-1","us-east-1"]
    owner: "oncall@company"
````

---

## CI policy to enforce

```yaml
# opsdeploy/change_freeze_gate.yml
inputs:
  calendar_file: "opsdeploy/release_calendar.yml"
  now_utc: "{{ env.NOW }}"
  region: "{{ env.REGION }}"
  tier: "{{ env.CHANGE_TIER }}"        # T0..T3 from the PR label
checks:
  forbid_when:
    - kind: "hard_freeze_active"
    - kind: "soft_freeze_active_and_tier_in"  # blocks T2,T3
      tiers: ["T2","T3"]
  require:
    - readiness_gate_passed: true
    - rollback_lever_defined: true
decision:
  on_fail: block_merge
  on_pass: allow
artifacts:
  - logs/change_freeze_decision.json
```

---

## Exception flow for T0 emergency

1. Confirm the incident page and owner are live.
2. Verify pins and prepare single pointer rollback.
3. Warm the cache for the fix and run a short gold set.
4. Ship canary at 5 percent for ten to fifteen minutes.
5. If green, complete rollout. If not, rollback and file postmortem.

---

## Observability to log

* Window id, region, scope, tier, approver, release id.
* Start and end timestamps and whether the gate blocked any merges.
* Canary metrics during the window, ΔS, coverage, λ, latency, errors.
* Rollback events tied to the release id.

---

## Common pitfalls

* Time zones not normalized so releases miss the window.
* Client only freezes that servers ignore. Always enforce on the server.
* Third party changes during your freeze. Track vendor freezes too.
* Quiet pin drift during a soft freeze. Verify pins in logs for each request.

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

