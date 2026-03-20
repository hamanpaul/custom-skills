# Azure OpenAI — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LLM_Providers**.  
  > To reorient, go back here:  
  >
  > - [**LLM_Providers** — model vendors and deployment options](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when failures look provider-specific on **Azure OpenAI**. Examples include wrong model alias vs deployment name, missing `api-version`, tool call payload shape drift, content safety blocks, or region throttling. Each fix maps back to WFGY pages with measurable targets.

**Core acceptance**

- ΔS(question, retrieved) ≤ 0.45  
- coverage ≥ 0.70 for the target section  
- λ remains convergent across 3 paraphrases

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- First call after deploy fails: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Fix in 60 seconds

1) **Measure ΔS**

- Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
- Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe with λ_observe**

- Vary k (5, 10, 20). If ΔS stays high while recall is fine, suspect index or metric mismatch.  
- Reorder prompt headers. If ΔS spikes, lock the schema.

3) **Apply the module**

- Retrieval drift → **BBMC** + **Data Contracts**.  
- Reasoning collapse → **BBCR** bridge + **BBAM** variance clamp.  
- Dead ends in long runs → **BBPF** alternate path.

---

## Azure-specific failure signatures and the right fix

| Symptom | Likely cause on Azure | Open this fix |
|---|---|---|
| 200 OK but empty or tool call ignored | Missing or wrong `api-version` for that model family | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| “Deployment not found”, even though the model exists | Using **model name** instead of **deployment name**, or wrong resource/region | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Output blocked, vague “content filtered” | Azure content safety layer different from OpenAI default | [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md), then clamp with **BBAM** |
| Tool call schema mismatch vs OpenAI | Response keys or enum names differ across `api-version` | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Works in one region, fails in another | Model availability and quotas are regional | [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) |
| Latency spikes or 429 under load | Per-resource rate limits, private link, or vnet egress | [Ops Live Monitoring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) |
| Function calls drop arguments | Old `api-version` truncates or renames fields | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Fine-tuned or staged deployment not picked | Wrong `deployment` alias bound in prod slot | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Minimal provider checklist

1) **Endpoint correctness**  
Resource url, region, and deployment name are consistent. Avoid mixing model name with deployment name in the same client.

2) **Version pinning**  
Pin an `api-version` known to support your features (tools, JSON mode, response format). Treat version bumps as schema migrations.

3) **Schema lock**  
Adopt the Problem Map **Data Contracts** snippet for tool payloads and citations. Reject partial responses. Require structured `finish_reason`.

4) **Safety behavior**  
Expect an extra content-safety layer. When blocked, route to **BBPF** alternate path and down-shift temperature, then retry with narrowed scope.

5) **Observability**  
Log λ state per step, ΔS per hop, and the exact deployment id used. Carry region and version in traces.

---

## Copy-paste prompt (safe to hand the AI)

```

I am using Azure OpenAI. Audit my run as follows:

* Check ΔS(question, retrieved) and ΔS(retrieved, anchor). Show the numbers.
* Confirm endpoint tuple: {resource, region, deployment}. Confirm `api-version` and tool schema.
* If tool/schema mismatch: apply the WFGY Data Contracts checklist and propose the exact fields to lock.
* If blocked by content safety: switch to a narrower prompt schema, reduce temperature, and route via BBPF.
* Keep λ convergent across 3 paraphrases. If it flips, apply BBCR + BBAM and show the before/after traces.

Link me to the exact Problem Map pages I should read next.

```

---

## Escalation

- **Still unstable after schema lock** → re-index and re-embed, verify with [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).  
- **Consistent provider errors** → freeze `api-version`, roll back deployment alias, rerun with fixed seed, attach λ traces, then open [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).  
- **First call after deploy fails** → rebuild boot fence with [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).

---

## Acceptance targets

- coverage to target section ≥ 0.70  
- ΔS(question, retrieved) ≤ 0.45  
- λ convergent across seeds and paraphrases  
- repeatable traces and identical schema across regions

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

