# Deep Dive — Cross-Agent Memory Overwrite (Multi-Agent Chaos)

> **Status:** Production-ready guidance with reproducible steps and guardrails.
> If you have real traces, please share anonymized logs — they help harden thresholds & adapters.

---

## Quick nav

* Back to multi-agent map → [Multi-Agent Problems](../Multi-Agent_Problems.md)
* Related patterns → Memory Desync ([pattern\_memory\_desync](../patterns/pattern_memory_desync.md)), SCU ([pattern\_symbolic\_constraint\_unlock](../patterns/pattern_symbolic_constraint_unlock.md)), Vectorstore Fragmentation ([pattern\_vectorstore\_fragmentation](../patterns/pattern_vectorstore_fragmentation.md))
* Examples → [Example 04 · Multi-Agent Coordination](../examples/example_04_multi_agent_coordination.md), [Example 03 · Pipeline Patch](../examples/example_03_pipeline_patch.md)
* Eval → [Cross-Agent Consistency (κ)](../eval/eval_cross_agent_consistency.md)

---

## 1) Problem definition

Two or more agents write to a **shared memory** (vector store, KV store, doc DB). Without versioning & conflict control, a later write silently **overwrites** a more recent or semantically different state (“last-writer-wins”). Downstream agents read stale or missing facts → contradictions, hallucinations, or wrong tool calls.

**Typical symptoms**

* “We agreed on Plan v3 yesterday… why are we back to v0?”
* Auditor validates **deleted** or **older** evidence.
* Turn logs show **non-monotonic** version jumps: `… 7 → 3 → 8`.

---

## 2) Threat model (why it happens)

* **Stale write**: Agent B writes with an old `mem_rev` it fetched minutes ago.
* **Concurrent write**: Agents A & B write simultaneously; store picks one arbitrarily.
* **Namespace collision**: Different flows use the same `entity_id` or index namespace.
* **Schema drift**: A writes `{plan,deadline}`, B writes `{deadline,notes}` and drops `plan`.
* **Fragmented store**: Partitions disagree on latest revision (see vectorstore fragmentation).

---

## 3) Data model & invariants (copy/paste)

Every write envelope **must** include:

```json
{
  "entity_id": "project:alpha",
  "agent_id": "planner",
  "role_id": "planner@v3",
  "role_hash": "sha256:78c2…",      // persona digest (see role-drift.md)
  "op_id": "op-2025-08-13T12:34:56Z#1234",
  "timestamp": "2025-08-13T12:34:56Z",
  "mem_rev": 8,                     // intended new revision (monotonic int)
  "prev_rev": 7,                    // what writer claims to extend
  "mem_hash": "sha256:abcd1234",    // hash(content)
  "parents": [7],                   // for merges, can be [7,7a] (three-way)
  "content": {
    "plan": "Deliverable X by EOD",
    "dependencies": ["doc-123"]
  }
}
```

**Store invariants**

1. **Monotonicity**: `mem_rev` strictly increases per `entity_id`.
2. **CAS on prev\_rev**: write only applies if store’s `head_rev == prev_rev`.
3. **Audit trail**: every write stored append-only in `mem_log`.
4. **Branch-safe** (optional): allow **branches** on conflict; reconcile later.

---

## 4) Reproduce the bug (minimal & deterministic)

**Goal:** make Agent B overwrite Agent A with a stale revision.

### 4.1 Curl (HTTP debug endpoints, stdlib-only server assumed)

```bash
# 1) A reads, sees head_rev=7
curl -s http://localhost:8080/mem/head?entity_id=project:alpha | jq

# 2) A writes rev=8 (ok)
curl -s -X POST http://localhost:8080/mem/write -H 'Content-Type: application/json' -d '{
  "entity_id":"project:alpha","agent_id":"planner","role_id":"planner@v3",
  "role_hash":"sha256:78c2","op_id":"op-A","timestamp":"2025-08-13T01:00:00Z",
  "mem_rev":8,"prev_rev":7,"mem_hash":"sha256:aa","content":{"plan":"v8"}
}' | jq

# 3) B (stale) still thinks head=7 and tries to write another “rev=8”
curl -s -X POST http://localhost:8080/mem/write -H 'Content-Type: application/json' -d '{
  "entity_id":"project:alpha","agent_id":"executor","role_id":"executor@v1",
  "role_hash":"sha256:91ff","op_id":"op-B","timestamp":"2025-08-13T01:00:02Z",
  "mem_rev":8,"prev_rev":7,"mem_hash":"sha256:bb","content":{"plan":"v0 (stale)"}
}' | jq
```

**Expected (correct)**: second call gets `409 Conflict` (CAS failed).
**Buggy (overwrite)**: second call `200 OK`, head becomes stale content.

### 4.2 Minimal Python test (single file)

* Simulate two concurrent writes; assert the second is rejected **or** creates a **branch**.

---

## 5) Detection & fast triage (no LLM)

**Reject on arrival** if any of:

* `prev_rev < head_rev` at write time (**stale write**).
* `prev_rev == head_rev` but `mem_hash` differs (**concurrent write**, collision).
* `role_hash` mismatches bound persona for the writer (possible role-drift).
* `entity_id` not in writer’s allowed scope (tool/ACL violation).

**Emit metrics/logs** for each rejection and keep an **append-only** record.

---

## 6) Guardrails (choose one or combine)

### 6.1 Optimistic CAS (compare-and-swap) — simplest & strong

* Require `prev_rev == head_rev` at write.
* On mismatch → **reject** or **auto-branch**.

**Python-like pseudo (stdlib-only)**

```python
def safe_write(store, w):  # w: envelope dict (see schema)
    head = store.head_meta(w["entity_id"])      # {"rev":int,"hash":str}
    if head["rev"] != w["prev_rev"]:
        return {"status":"conflict", "reason":"stale_prev", "head": head}
    # Atomically swap (rev must advance by 1)
    ok = store.compare_and_swap(
        entity_id=w["entity_id"],
        expected_rev=head["rev"],
        new_rev=w["mem_rev"],
        new_hash=w["mem_hash"],
        content=w["content"],
        op_meta={k:w[k] for k in ("agent_id","role_id","role_hash","op_id","timestamp")}
    )
    return {"status":"ok"} if ok else {"status":"retry","reason":"cas_failed"}
```

**Node/TS HMAC signature (optional)**

```ts
import crypto from "crypto";
function signWrite(agentId: string, roleHash: string, prevRev: number, memRev: number, key: Buffer){
  const payload = `${agentId}|${roleHash}|${prevRev}|${memRev}`;
  return crypto.createHmac("sha256", key).update(payload).digest("hex");
}
```

### 6.2 Branch-and-Merge (BBCR-style)

* On conflict, create a **branch** (`mem_rev=8a`) instead of rejecting; later run a **three-way merge**.

**Three-way merge outline**

```
base = rev 7
A    = rev 8 (agent A)
B    = rev 8a (agent B)
ΔA = diff(base, A);  ΔB = diff(base, B)
if ΔA ∩ ΔB == Ø → merge = base ⊕ ΔA ⊕ ΔB
else → manual decision or rule-based precedence (e.g., auditor > planner)
```

*No external libs needed*: represent `content` as JSON and define a minimal **diff** (added/removed keys; for strings, use normalized edit distance ≤ threshold to auto-merge).

### 6.3 ΔS semantic collision alert (nice-to-have)

* Compute a **cheap semantic distance** between the new `content` and head content:

  * Normalize (lowercase, strip punctuation), tokenize, Jaccard overlap on tokens.
  * If overlap `< 0.6` **and** same `prev_rev` → raise collision alert, require manual confirm.

---

## 7) Observability (Prometheus) & alerts

**Metrics**

* `mem_write_total{entity,agent,outcome="ok|conflict|retry"}`
* `mem_conflict_total{entity,reason="stale_prev|hash_collision"}`
* `mem_branch_total{entity}` (if branch mode)
* `mem_head_rev{entity}` (gauge)
* `mem_write_latency_seconds` (histogram)

**Alert rules (examples)**

```yaml
# Frequent conflicts (possible hot entity or stale readers)
alert: MemConflictsSpike
expr: increase(mem_conflict_total[5m]) > 3
for: 5m
labels: { severity: ticket }

# Head revision oscillation (rollback/flip-flop)
alert: MemHeadOscillation
expr: changes(mem_head_rev[10m]) > 5
for: 10m
labels: { severity: ticket }
```

> Also track **cross-agent κ**; sudden drops often co-occur with memory corruption. See [cross-agent eval](../eval/eval_cross_agent_consistency.md).

---

## 8) Tests & acceptance criteria

**Unit**

* **Stale write** rejected (`prev_rev < head_rev`).
* **Concurrent write**: either **reject** or **create branch**; never silent overwrite.
* **Schema merge**: non-overlapping keys merge automatically.

**E2E**

* Two agents race on the same `entity_id`: final head must be **v8** or (**v8 + v8a** if branching), never **v0**.
* κ remains ≥ baseline after enabling guards.

**Acceptance (ship)**

* `mem_conflict_total` steady and low; no silent overwrites in 1k writes.
* No data loss in replay tests (log → rebuild yields identical head).

---

## 9) Rollout plan (safe)

1. **Shadow mode**: turn on CAS checks, **warn-only**; measure conflict rate.
2. **Canary**: reject stale writes for 10% entities; branch on collision (optional).
3. **Full**: enforce CAS for all; keep feature flag for emergency bypass.
4. **Post-rollout**: schedule merge jobs for any branches; add dashboards.

---

## 10) Sample logs (anonymized JSONL)

```json
{"ts":"2025-08-13T01:00:00Z","entity_id":"project:alpha","op":"write","agent":"planner","prev_rev":7,"mem_rev":8,"status":"ok"}
{"ts":"2025-08-13T01:00:02Z","entity_id":"project:alpha","op":"write","agent":"executor","prev_rev":7,"mem_rev":8,"status":"conflict","reason":"stale_prev","head_rev":8}
{"ts":"2025-08-13T01:00:03Z","entity_id":"project:alpha","op":"write","agent":"executor","prev_rev":8,"mem_rev":9,"status":"ok"}
```

---

> Have a reproducible overwrite trace? Please share; even 5–10 turns help us tune adapters and defaults.

### ↩︎ Back & See also

- **Back to Map-B:** [Multi-Agent Chaos Problem Map](../Multi-Agent_Problems.md)  
- **Related deep dives:**  
  - [Cross-Agent Memory Overwrite](./memory-overwrite.md)  
  - [Agent Role Drift](./role-drift.md)  
- **Upstream patterns:**  
  - [Symbolic Constraint Unlock (SCU)](../patterns/pattern_symbolic_constraint_unlock.md)  
  - [Memory Desync](../patterns/pattern_memory_desync.md)

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

