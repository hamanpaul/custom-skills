# Staged Rollout & Canary — OpsDeploy Guardrails

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


A practical runbook to ship new models, prompts, retrievers, or pipelines with safety rails. Start with a small, observable canary, compare against a pinned baseline, then graduate traffic only when acceptance targets hold.

## Open these first

* Rollout readiness gate: [rollout\_readiness\_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
* Boot and deploy ordering: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* Deadlocks and first-run failures: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Live probes and ops playbook: [live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* RAG map and schema locks: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Quality evals: [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## When to use this page

* New LLM provider or model version.
* Prompt or tool protocol change.
* Retriever, chunking, or store upgrade.
* Any change that can shift ΔS, λ, coverage, cost, or latency.

## Acceptance targets for graduating a canary

* ΔS drift vs baseline: median ≤ 0.03, p95 ≤ 0.10.
* Coverage to target section ≥ 0.70 on the gold set.
* λ remains convergent across 3 paraphrases and 2 seeds.
* E\_resonance stays flat on long windows.
* p95 latency within +15% of baseline, error rate ≤ 0.5%, tool success ≥ 99%.
* Cost per solved query within +10% unless quality gains are proven.

## Traffic plan

**Phase 0 — Shadow**
Mirror 1% of traffic to canary. Serve baseline answers only. Record ΔS, λ, coverage, latency, cost.

**Phase 1 — Canary live**
Serve 5% users from canary. Compare per-bucket metrics to the same users on baseline where possible.

**Phase 2 — Graduations**
Increase to 25% then 50% then 100% if all gates stay green for a full evaluation window.

## Gates at each step

**G1 Boot and version fences**

* Secrets present. Index and reranker hashes pinned. Model and prompt versions pinned.
* Contracts for snippets and tools in place. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**G2 Quality drift**

* ΔS drift within targets, coverage ≥ 0.70, λ convergent.
* Gold eval regression ≤ 2 points. See [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md).

**G3 Ops SLO**

* Error, latency, and cost within bounds. Live probes healthy. See [live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md).

## Stop and rollback rules

* Hard stop if ΔS p95 drift > 0.15 or coverage < 0.60 or λ flip rate > 0.20.
* Hard stop if 5xx > 1% or tool loop detection fires.
* Soft stop if cost or latency exceed budgets without quality gains.
  If any hard stop triggers, route traffic back to baseline at once and open: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).

## 60-second checklist

1. Pin baseline and canary versions and store their `INDEX_HASH`, `RERANK_HASH`, `PROMPT_VER`, `MODEL_VER`.
2. Attach readiness probes from the gate page.
3. Enable shadow then 5% canary with sampling keys that are stable across sessions.
4. Compare ΔS, coverage, λ, latency, cost against baseline.
5. If green for one full eval window, graduate to the next traffic tier.

## Reference metrics to log per request

* ΔS(question, retrieved), ΔS(retrieved, anchor).
* λ state at retrieve and reason steps.
* Coverage to target section.
* Latency p50 and p95 for retrieve, rerank, and reason.
* Tool call success and retries.
* Cost per solved query.
* Version fields and hashes.

## Canary implementations

### Kubernetes traffic split (Ingress/Nginx example)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: wfgy-api
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-WFGY-Canary"
    nginx.ingress.kubernetes.io/canary-weight: "5"    # 5% canary
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /rag
            pathType: Prefix
            backend:
              service:
                name: wfgy-baseline-svc
                port: { number: 80 }
          - path: /rag
            pathType: Prefix
            backend:
              service:
                name: wfgy-canary-svc
                port: { number: 80 }
```

Use a stable header or hash of `user_id` to keep users on the same arm during the window.

### AWS Lambda weighted alias

```yaml
Type: AWS::Lambda::Alias
Properties:
  FunctionName: !Ref WFGYFunction
  Name: Live
  RoutingConfig:
    AdditionalVersionWeights:
      - FunctionVersion: !GetAtt WFGYFunctionCanary.Version
        FunctionWeight: 0.05
```

Attach CloudWatch alarms that mirror the stop and rollback rules.

## Copy-paste prompt to audit a canary window

```
You have TXT OS and the WFGY Problem Map.

Inputs:
- baseline_metrics: {ΔS_median, ΔS_p95, coverage, λ_flip_rate, p95_latency, cost}
- canary_metrics:   {ΔS_median, ΔS_p95, coverage, λ_flip_rate, p95_latency, cost}

Do:
1) Compare canary vs baseline. Flag any breach of:
   ΔS_median drift > 0.03, ΔS_p95 drift > 0.10,
   coverage < 0.70, λ_flip_rate > 0.20,
   p95_latency > baseline*1.15, error_rate > 0.5%, cost > baseline*1.10.
2) Return PASS or FAIL and list the failing gates. 
3) If FAIL, suggest the smallest structural fix and the exact WFGY page to open next.
```

## What to check if gates fail

* Ordering and secrets at boot. See [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).
* Wrong meaning despite high similarity. See [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).
* Citations not aligned with snippets. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
* Live instability and noisy logs. See [debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

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

