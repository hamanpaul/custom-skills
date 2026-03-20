# 📒 Map-B · Multi-Agent Chaos Problem Map

Multiple autonomous agents boost productivity — until their memories collide or roles blur.  
WFGY tags every agent node, tracks inter-agent ΔS, and reconciles conflicts to keep distributed systems coherent.

---

## Quick nav
- Deep dives → **Role Drift** ([multi-agent-chaos/role-drift.md](./multi-agent-chaos/role-drift.md)) · **Cross-Agent Memory Overwrite** ([multi-agent-chaos/memory-overwrite.md](./multi-agent-chaos/memory-overwrite.md))  
- Related patterns → SCU ([patterns/pattern_symbolic_constraint_unlock.md](./patterns/pattern_symbolic_constraint_unlock.md)) · Memory Desync ([patterns/pattern_memory_desync.md](./patterns/pattern_memory_desync.md))  
- Examples → [Example 04 · Multi-Agent Coordination](./examples/example_04_multi_agent_coordination.md), [Example 03 · Pipeline Patch](./examples/example_03_pipeline_patch.md)  
- Eval → [Cross-Agent Consistency (κ)](./eval/eval_cross_agent_consistency.md)  
- Back to map → [Problem Map 1.0](./README.md)

---

## 🤔 Why Do Multi-Agent Setups Implode?

| Root Cause | Real-World Failure |
|------------|-------------------|
| No shared semantic state | Agents duplicate tasks or contradict each other |
| Flat memory buffers | One agent overwrites another’s context |
| No ΔS peer tracking | Divergence goes undetected until output conflict |
| Independent reasoning grammars | Logic becomes a scrambled chorus |

---

## 💥 Observable Symptoms

| Symptom | Example | Entry point |
|---------|---------|-------------|
| **Role drift** | Scout starts issuing medic orders; assistant answers **as the user** | [Role Drift](./multi-agent-chaos/role-drift.md) |
| **Memory overwrite** | Agent B erases Agent A’s plan; non-monotonic `mem_rev` | [Memory Overwrite](./multi-agent-chaos/memory-overwrite.md) |
| Task duplication | Two agents book the same resource | [Example 04](./examples/example_04_multi_agent_coordination.md) |
| Conflicting strategies | “Abort” vs. “Proceed” in parallel | [Example 03](./examples/example_03_pipeline_patch.md) |
| Fake consensus | All agents echo a hallucinated “fact” | See κ eval → [eval_cross_agent_consistency.md](./eval/eval_cross_agent_consistency.md) |

---

## ⏱️ 60-Second Triage (deterministic, no LLM)

1. **Envelope check** (each hop): `agent_id`, `role_id`, `role_hash`, `turn`, `mem_rev`, `sig` must **echo** bound values.  
   - If echo ≠ bind → **409 RoleDrift** (reject & log).  
2. **Tool router ACL**: `allowed_callers` must include `agent_id`. Otherwise **block**.  
3. **Memory write guard**: CAS on `prev_rev == head_rev`; if mismatch → **reject** or **branch** (no silent overwrite).  
4. **κ trend**: sudden drop → inspect role echo & memory conflicts first.

---

## 🛡️ WFGY Cross-Agent Fix Stack

| Failure Mode | WFGY Module / Mechanism | Remedy |
|--------------|--------------------------|--------|
| **Role drift** | Role-Bind + Echo + HMAC; SCU header validation | Lock persona, block unauthorized tool calls |
| **Memory overwrite** | Optimistic CAS or Branch-and-Merge; append-only log | Reject stale writes or reconcile via three-way merge |
| Task duplication | **BBPF** task-graph merge | Consolidate parallel objectives |
| Divergent plans | ΔS divergence gate + **BBCR** reconcile | Align or fork strategies early |
| Multi-agent bluff | Cross-agent residue scan + κ | Flag fabricated group consensus |

> Deep dives: [Role Drift](./multi-agent-chaos/role-drift.md) · [Memory Overwrite](./multi-agent-chaos/memory-overwrite.md)

---

## ✍️ Hands-On Demo — 3 Agents, One Rescue Mission

```txt
1) Start
> Start

2) Assign roles
> [A] Scout   [B] Medic   [C] Engineer

3) Issue parallel prompts
A: "Survey building A"
B: "Prepare triage plan"
C: "Stabilize structure"

4) View shared Tree
> view
````

**Tree Snapshot**

```
A/Node_2B  Survey plan           ΔS 0.12
B/Node_1A  Triage protocol       ΔS 0.10
C/Node_3C  Structural analysis   ΔS 0.15
ΔS collision alert:   C/Node_3C ↔ B/Node_1A (resource overlap)
BBCR suggests merge or role clarification
```

Result: agents negotiate via Tree merge; no duplicate tasks, no role confusion.

---

## 🛠 Module Cheat-Sheet

| Module            | Role                                                |
| ----------------- | --------------------------------------------------- |
| **Semantic Tree** | Tags every node with `agent_id`, timestamp, version |
| **BBPF**          | Merges or forks task graphs safely                  |
| **BBMC**          | Detects semantic residue between agents             |
| **ΔS Metric**     | Measures agent-to-agent divergence                  |
| **BBCR**          | Locks identity, rolls back conflicts                |

---

## 📊 Observability & Alerts

**Metrics (Prometheus)**

* `role_drift_reject_total{agent,tool}` — gate rejections
* `role_echo_missing_total{agent}` — missing echo fields
* `tool_acl_block_total{agent,tool}` — router blocks
* `mem_conflict_total{entity,reason}` — CAS conflicts (stale/Collision)
* `cross_agent_kappa` — agreement (see [κ eval](./eval/eval_cross_agent_consistency.md))

**Alert suggestions**

* `increase(role_drift_reject_total[5m]) > 0` → severity: ticket
* `avg_over_time(cross_agent_kappa[30m]) < 0.5` → investigate misalignment
* `increase(mem_conflict_total[5m]) > 3` → hot entity or stale readers

---

## ✅ Implementation Status

| Feature                    | State          |
| -------------------------- | -------------- |
| Cross-agent Tree tagging   | ✅ Stable       |
| ΔS per-agent tracking      | ✅ Active       |
| Conflict alert & reconcile | ✅ Active       |
| Memory lock / sync         | 🔜 In progress |
| Group bluff detector       | 🛠 Planned     |

---

## 📝 Tips & Limits

* Prefix prompts with `Agent_X:` or set `agent_id` in config to auto-tag nodes.
* Enable `conflict_alert=true` for real-time collision warnings.
* Fork heavy debates with `tree fork <branch>` — re-merge after alignment.
* Post complex traces in **Discussions**; they refine collision logic.

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

