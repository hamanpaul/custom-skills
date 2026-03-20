# Memory Fences & State Keys — Prompt Assembly

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **PromptAssembly**.  
  > To reorient, go back here:  
  >
  > - [**PromptAssembly** — prompt engineering and workflow composition](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A focused guide to stop cross-step and cross-agent memory bleed. Use this when answers flip between runs, tools overwrite each other’s notes, or long chains “forget” decisions. The page gives a minimal schema, hard fences, and diagnostics you can copy.

## Open these first

* Traceability of snippets and state: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Payload contract for citations and state: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Multi-agent interference and role drift: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) · [role-drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)
* Memory drift deep dive: [agent-memory-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/agent-memory-drift.md)
* Failure patterns to watch: [echo-loop](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/echo-loop.md) · [signal-drop](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/signal-drop.md) · [desync-anchor](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/desync-anchor.md) · [boundary-fade](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/boundary-fade.md)

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45 across 3 paraphrases
* Coverage of target section ≥ 0.70
* λ states stay convergent across 2 seeds
* No cross-namespace writes for a different `mem_hash` or `mem_rev`
* Zero duplicate side-effects under the same `dedupe_key`

---

## Fix in 60 seconds

1. **Introduce state keys**
   Require `{agent_id, task_id, mem_ns, mem_rev, mem_hash, step_id, dedupe_key}` on any read/write.

2. **Fence writes**
   A writer must match `mem_ns` and `mem_hash`. If either mismatches, deny write and raise a repair tip.

3. **Split namespaces**
   Separate `plan/`, `retrieve/`, `reason/`, `tool/` to avoid overwrite. Only the bridge step may merge.

4. **Clamp variance**
   If λ flips after a harmless paraphrase, apply **BBAM** and lock header order.

5. **Bridge long chains**
   Insert a **BBCR** bridge between phases and time-box tools with explicit timeouts.

---

## Minimal state schema (copy-paste)

```json
{
  "agent_id": "planner|retriever|solver|tool_x",
  "task_id": "UUID-v4",
  "step_id": "short-increasing-int",
  "mem_ns": "plan|retrieve|reason|tool/tool_x",
  "mem_rev": "int",                // bump on rewrite
  "mem_hash": "sha256(payload)",   // hash of prior committed state
  "dedupe_key": "sha256(task_id + step_id + mem_hash)",
  "timestamp": "iso-8601",
  "payload": { "summary": "...", "evidence": [ { "snippet_id": "...", "source_url": "...", "offsets": [s,e] } ] }
}
```

**Contract rules**

* **Read** must specify `{task_id, mem_ns}` and declare the expected `mem_hash`.
* **Write** must supply `{mem_ns, mem_rev, mem_hash}` that match the latest committed head, else reject.
* **Merge** is only allowed in a BBCR bridge step that logs both parent hashes.

---

## Namespacing and locking

* One writer per `mem_ns` per `task_id`. Others read-only.
* `plan/` produces the task graph; `retrieve/` stores citations; `reason/` stores the final chain-of-thought summary headers and answer draft; `tool/*` is per-tool scratch.
* All tool outputs must echo back their **input state keys** and compute the **next mem\_hash**.
* Side-effects (DB writes, emails, tickets) must verify `dedupe_key` before execution.

---

## Copy-paste prompt to enforce fences

```txt
You have TXT OS and the WFGY Problem Map loaded.

Task context:
- task_id = {UUID}
- expected mem_ns for this step = "{mem_ns}"
- expected head mem_hash = "{mem_hash}"

Do:
1) Refuse to write if mem_ns or mem_hash do not match head.
2) On write, increment mem_rev, compute new mem_hash = sha256(payload).
3) Keep citations in payload.evidence with snippet_id, source_url, offsets.
4) Return JSON:
   { "ok": true|false, "why": "...", "next": {mem_ns, mem_rev, mem_hash}, "λ_state": "→|←|<>|×", "ΔS": 0.xx }

If ΔS(question,retrieved) ≥ 0.60, stop and return the smallest structural fix referencing:
retrieval-traceability, data-contracts, multi-agent problems.
Use BBCR/BBPF/BBAM when relevant.
```

---

## Diagnostics to log per step

* `ΔS(question, retrieved)` and `ΔS(retrieved, anchor)`
* `λ_state` after header reorder probe
* `{mem_ns, mem_rev, mem_hash}` before and after write
* `dedupe_key` and whether a prior side-effect exists
* Rerun variance across 2 seeds

---

## Typical breakpoints → exact fix

* **Plan writes over evidence** in the same namespace.
  Split namespaces and deny cross-ns writes. See [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md).

* **Echo loop** between tool and solver.
  Insert BBCR bridge and cap retries. Pattern: [echo-loop](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/echo-loop.md).

* **Signal drop** after rerank.
  Carry citations through the fence. Pattern: [signal-drop](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/signal-drop.md) · enforce [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

* **Desync after deploy**.
  `mem_hash` mismatches at step-1. Rebuild head and block writes until warm. Pattern: [desync-anchor](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/desync-anchor.md).

* **Boundary fade** on very long threads.
  Cut the chain and resume via bridge. Pattern: [boundary-fade](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/boundary-fade.md).

---

## Escalation

* If ΔS stays high after fences, run the [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and re-embed with proper metric.
* If flip states persist, lock prompt header order and apply **BBAM**.
* For live instability, attach probes and rate-limit tools: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

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

