# State Fork — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **MemoryLongContext**.  
  > To reorient, go back here:  
  >
  > - [**MemoryLongContext** — extended context windows and memory retention](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


When the same `task_id` is held in multiple tabs, agents, or sessions, their memories may diverge.  
This creates **two or more competing state branches**, producing unstable or contradictory answers.

---

## Symptoms
- Two browser tabs answer the same task differently.  
- Multi-agent orchestration produces **conflicting citations**.  
- Session resumes but history appears **rewritten or selectively dropped**.  
- Answers alternate between two incompatible interpretations.  
- Logs show inconsistent `mem_rev` or `mem_hash` values for the same `task_id`.

---

## Root causes
- Concurrent writes to the same memory namespace.  
- Missing checks for `mem_rev` version control.  
- Agents refreshing at different times and overwriting buffers.  
- Weak schema: task identity not fenced by `{task_id, mem_rev, mem_hash}`.  
- No conflict resolution logic when branches emerge.

---

## Fix in 60 seconds
1. **Version control memory**
   - Every write stamped with `{task_id, mem_rev, mem_hash}`.  
   - Reject writes if `mem_rev` < server `mem_rev`.  
   - Require conflict resolution if two branches exist.

2. **Isolate namespaces**
   - Each agent/tab gets unique memory slot.  
   - If collaboration required, merge through a **coordinator agent**.  

3. **Detect divergence early**
   - Measure ΔS(answerA, answerB) across tabs.  
   - If ΔS ≤ 0.40 but snippets differ, state fork detected.  

4. **Resolve fork**
   - Run reconciliation: pick majority snippet set, or force human confirm.  
   - Hash merged state and issue new `{mem_rev, mem_hash}`.  

5. **Trace schema**
   - Require all claims to cite snippet ids.  
   - Reject orphan claims without snippet anchors.

---

## Copy-paste diagnostic prompt
```txt
You have TXTOS and the WFGY Problem Map.

Task: Detect and repair state forks across tabs or agents.

Protocol:
1. Print {task_id, mem_rev, mem_hash}.
2. If two active branches share task_id with different mem_rev → flag fork.
3. Compare ΔS(answerA, answerB).
   - If ΔS ≤ 0.40 but snippets differ → fork confirmed.
4. Apply resolution:
   - Choose majority snippet set or request human input.
   - Issue new {mem_rev, mem_hash}.
5. Report ΔS, λ states, and resolution path.
````

---

## Acceptance targets

* No conflicting branches for the same `task_id`.
* All writes validated against server-side `mem_rev`.
* ΔS(answerA, answerB) ≥ 0.60 after resolution.
* λ remains convergent across three paraphrases.
* Audit log records merge or reject actions explicitly.

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

