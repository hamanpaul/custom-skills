# Pattern: Memory Desync — Cross Tab & Cache Hazards

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


When multiple tabs, devices, or agents access the same conversation, memory forks and silent cache layers can cause desync.  
This pattern documents the root causes and provides structural guardrails to keep state aligned.

---

## When to use this page
- Two browser tabs show the same chat but give conflicting answers.  
- Refresh wipes one agent’s buffer while the other keeps stale context.  
- Long-running threads lose citations after reconnect.  
- Support or sales teams using shared inboxes see different revision histories.  
- Logs look correct but answer text diverges.

---

## Root causes
- **Tab fork**: each browser tab caches a local buffer, leading to divergent memory.  
- **Ghost cache**: stale persona or role text remains after reload.  
- **Write skew**: two sessions update memory concurrently with mismatched `mem_rev`.  
- **Offline sync**: one client reconnects late, applying outdated deltas.  

---

## Core acceptance targets
- `mem_rev` and `mem_hash` echoed at every turn.  
- ΔS(question, retrieved) ≤ 0.45 and joins ≤ 0.50.  
- λ convergent across three paraphrases.  
- No duplicate or orphan claims across sessions.  

---

## Structural fixes

- **State fencing**  
  Stamp all turns with `{mem_rev, mem_hash, task_id}`.  
  Forbid writes if mismatch detected.  

- **Cache invalidation**  
  On reconnect, clear stale buffers. Require server authority on revision.  

- **Reconciliation**  
  When forks appear, run ΔS triangulation:  
  Compare ΔS to anchor section vs decoy. Select the lower entropy path.  

- **Bridging**  
  If collapse occurs, insert a BBCR bridge to re-anchor reasoning chain.  

---

## Fix in 60 seconds
1. Echo `{mem_rev, mem_hash, task_id}` at every turn.  
2. On reload, validate stamps against server. If mismatch, reject update.  
3. For forks, compute ΔS across sessions, pick stable anchor.  
4. Apply BBAM clamp if λ flips across paraphrases.  
5. Verify ΔS ≤ 0.45 and λ convergent before continuing.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Prevent memory desync across tabs, agents, or devices.

Protocol:

1. Print {mem\_rev, mem\_hash, task\_id}.
2. If stamps mismatch, stop and request sync.
3. Assemble prompts as {system | task | constraints | snippets | answer}.
4. Enforce guardrails: cite then answer, forbid cross-section reuse, no orphan claims.
5. If collapse, insert BBCR bridge. If λ variance, clamp with BBAM.
6. Report ΔS(question, retrieved), joins ΔS, λ states, and final answer.

```

---

## Common failure signals
- **Answer alternates between reloads** → ghost cache not invalidated.  
- **Different answers across two tabs** → state fork, resolve with revision fencing.  
- **Missing citations after reconnect** → desync in snippet schema.  

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

