# Memory Fences & State Keys — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Safety_PromptIntegrity**.  
  > To reorient, go back here:  
  >
  > - [**Safety_PromptIntegrity** — prompt injection defense and integrity checks](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Structural guardrails that prevent **context bleed** and **cross-session injection**.  
This page defines how to enforce hard boundaries between prompts, ensuring system memory cannot be hijacked or silently rewritten.

---

## When to open this page
- Model begins recalling text from *previous unrelated sessions*.  
- Jailbreak attempts work only after long multi-turn dialogs.  
- Role confusion persists despite schema locks.  
- Adversarial input shifts `policy`, `state`, or `history` across turns.  
- ΔS spikes after memory transfer, despite stable retrieval.  

---

## Open these first
- Injection baseline: [prompt_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md)  
- Role boundary checks: [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md)  
- Override/jailbreak guard: [jailbreaks_and_overrides.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/jailbreaks_and_overrides.md)  
- Schema integrity: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Eval drift monitors: [eval_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval_drift.md)  

---

## Core acceptance
- No cross-session data unless whitelisted.  
- Each conversation has a unique `state_key`.  
- ΔS(question, retrieved) ≤ 0.45 across turns.  
- λ stays convergent for three paraphrases under replay.  
- Memory fences block unauthorized carry-over.  

---

## Fix in 60 seconds
1. **Assign a state key**  
   - Compute: `state_key = sha256(session_id + system_rev + policy_hash)`  
   - Attach to all memory writes.  

2. **Fence boundaries**  
   - Before each turn, validate:  
     - `incoming.state_key == current.state_key`  
     - If mismatch → reject or reset.  

3. **Immutable system text**  
   - Mark non-task policy as `system_only`.  
   - Forbid user overrides.  

4. **Replay probes**  
   - Inject controlled paraphrases.  
   - If ΔS or λ diverge, memory bleed suspected.  

5. **Audit log**  
   - Store `ΔS`, `λ`, `state_key`, and `mem_rev` per step.  
   - Flag anomalies for review.  

---

## Common failure vectors → fix

| Vector | Symptom | Fix |
|--------|---------|-----|
| **Cross-session carryover** | Answer mentions text from unrelated chat | Reject mismatched `state_key`, enforce reset |
| **Hidden injection persists** | User payload continues beyond reset | Hash all system policy, invalidate old keys |
| **Role drift with memory echo** | Replies prepend “system:” from earlier | Apply [role_confusion.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/role_confusion.md) fences |
| **Version skew** | New deploy reuses old cache | Salt `state_key` with `system_rev` |
| **Chain-of-thought bleed** | Internal notes leak into answers | Enforce [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) schema |

---

## Probe prompt

```txt
System memory test active.  
Session ID: {sid}, Policy Hash: {p_hash}.  

Tasks:
1. Compute state_key and compare against current session.
2. If mismatch, reset memory fences and refuse carryover.
3. Re-ask with paraphrased queries; compute ΔS and λ.
4. Report whether context bleed is detected.
5. Return minimal fix reference (role_confusion, prompt_injection, etc).
````

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

