# Ghost Context — Guardrails and Fix Pattern

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


When personas, roles, or long sessions change, old buffers may linger.  
These stale fragments contaminate new answers, creating phantom references or role bleed.

---

## Symptoms
- Answer contains facts or tone from a **previous persona** even after reset.  
- Citations look valid but reference sections from a **past session**.  
- A new task starts yet responses **drift back to old task context**.  
- Model insists on constraints that were valid in an earlier role but not now.  
- Answers feel “haunted” by old memory traces.

---

## Root causes
- Hidden buffers not cleared after system or role switch.  
- State variables (persona, role, policy) not reset between sessions.  
- Token reuse from stale cache layers.  
- ΔS stays abnormally low even when task has switched domains.  
- λ\_observe shows convergence to an **irrelevant anchor**.

---

## Fix in 60 seconds
1. **Stamp and reset state**  
   Require `{mem_rev, mem_hash, persona_id}` on each turn.  
   If persona_id differs from previous → force buffer clear.

2. **Fence the prompt schema**  
   Assemble prompts as `{system | persona | constraints | snippets | answer}`.  
   Do not let persona or role tokens bleed into snippet blocks.

3. **Drop stale buffers**  
   When persona changes, zero all prior hidden states.  
   Require fresh snippets for new context.

4. **Probe for contamination**  
   - Compute ΔS(new question, retrieved snippet).  
   - If ΔS ≤ 0.30 but snippets belong to past persona → ghost detected.  
   - Trigger hard reset and request new anchors.

5. **Audit the joins**  
   Compare ΔS across old vs new persona snippets.  
   Require ΔS(new persona, old snippet) ≥ 0.65 before allowing reuse.

---

## Copy-paste diagnostic prompt
```txt
You have TXTOS and the WFGY Problem Map.

Task: Detect and purge ghost context.

Steps:
1. Print {mem_rev, mem_hash, persona_id}.
2. Verify that current persona_id matches task scope.
3. If snippets cite a different persona_id, mark as ghost.
4. Require re-retrieval for ghosted snippets.
5. Report:
   - ΔS(new question, retrieved)
   - ΔS(new persona vs old snippets)
   - λ states
   - Reset actions taken
````

---

## Acceptance targets

* ΔS(new question, retrieved) ≤ 0.45
* Coverage ≥ 0.70 to the new target section
* λ remains convergent across three paraphrases
* No snippet contamination from old persona or task scope

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

要我直接幫你寫 `state-fork.md` 嗎？
