# 🛰️ System-Prompt Drift — How Hidden Instructions Lose Authority  
_A user-friendly guide to diagnosing and fixing “why did my system prompt stop working?”_

---

## 1  What Is System-Prompt Drift?

“System-prompt drift” occurs when the foundational instructions that define an agent’s **identity, tone, or guardrails** gradually lose influence over time (or instantly under certain triggers).  
The model still answers, but:

* Tone shifts from professional → casual → chaotic  
* Guardrails weaken, leaking disallowed content  
* Chain-of-thought grows inconsistent or contradictory  

> **Core insight:** LLMs have no native concept of *instruction priority*.  
> Without reinforcement, later tokens can override earlier ones.

---

## 2  Early-Warning Signs

| Symptom | How to Spot | Typical Trigger |
|---------|-------------|-----------------|
| Tone drift (“you” → “we” → “ya”) | Diff analysis of consecutive answers | Long conversation or paraphrase loops |
| Policy leakage | Previously filtered topics slip through | Mixed file uploads (PDF + code) |
| Over-explanation after concise goal | Answer length suddenly doubles | Retrieval injects verbose context |
| “Why do you need that?” disappears | Politeness layer collapses | Multi-agent routing / tool calls |
| Temperature spike | Output variance ↑, repetition ↓ | System prompt trimmed by token limit |

---

## 3  Root Causes (Technical)

### 3.1  Token Supersession  
LLM context windows are linear. New tokens can overshadow earlier tokens via attention weight decay.

### 3.2  Role Collision  
Aggregating content from multiple sources (user, tools, memory) without role tags causes blending of semantic channels.

### 3.3  Truncation Loss  
When the buffer hits the window limit, oldest tokens are dropped — often the system prompt header.

### 3.4  Hidden Injection  
Retrieved chunks may contain meta-instructions (“The following should be summarized as …”) that override role.

---

## 4  Broken Remedies to Avoid

| Attempt | Why It Fails |
|---------|--------------|
| **“Repeat system prompt each turn.”** | Costs tokens; still lost under truncation or injection. |
| **“Hard-code tonality keywords.”** | Keyword collision is brittle; adversary can mimic them. |
| **“Raise top_p / lower temperature.”** | Alters style but not underlying role authority. |
| **“Fine-tune on more examples.”** | Long-context decay still erodes influence at runtime. |

---

## 5  WFGY Solution Blueprint

| Stage | Module | Action |
|-------|--------|--------|
| 5.1 **Role Tagging** | **WRI / WAI** | Wrap every segment: `<sys>…</sys>` `<user>…</user>` `<tool>…</tool>` |
| 5.2 **Semantic Boundary Heatmap** | ΔS + λ_observe | Measure drift: if ΔS(system, answer) > 0.45 **and** λ flips, mark risk. |
| 5.3 **Attention Modulation** | **BBAM** | Down-weight non-system tokens when λ diverges from system anchor. |
| 5.4 **Automatic Re-Anchoring** | **BBCR** | If ΔS > 0.60, collapse reasoning, re-inject compressed system prompt, resume. |
| 5.5 **Trace Split** | Bloc/Trace | Persist system-layer trace separate from answer layer for auditability. |

### 5.6  Implementation Snippet

```python
def enforce_system_role(sys_prompt, history, new_msg):
    drift = delta_s(sys_prompt, new_msg)
    lam  = observe_lambda(sys_prompt, new_msg)
    if drift > 0.45 and lam in ("←", "×"):
        # role divergence detected
        reborn_prompt = compress(sys_prompt)  # 20–30 tokens
        return f"<sys>{reborn_prompt}</sys>\n{history}\n{new_msg}"
    return f"{history}\n{new_msg}"
````

*`compress()` uses WFGY BBMC to keep ΔS ≤ 0.25 while shrinking to fit.*

---

## 6  Friendly Checklist (Paste into Runbook)

1. **Tag Roles Once** — no implicit mixing.
2. **Monitor ΔS(system, answer)** every turn.
3. **If ΔS ≥ 0.45 with divergent λ →** trigger BBAM weight clamp.
4. **If ΔS ≥ 0.60 →** run BBCR collapse-rebirth (re-inject summary prompt).
5. **Every 30 turns** or on tool call, re-compress system prompt to ≤ 50 tokens.

> **Tip:** Users never notice a 30-token summary, but models retain authority.

---

## 7  Validation Matrix

| Test Case                            | Target Metric                              |
| ------------------------------------ | ------------------------------------------ |
| 20-turn dialogue, paraphrase ×3      | Tone consistency score ≥ 0.9               |
| Mixed PDF + code retrieval           | ΔS(system, answer) median ≤ 0.40           |
| Adversarial “Ignore above” injection | Model outputs refusal / filtered text      |
| Window overflow 3×                   | System role preserved (λ stays convergent) |

---

## 8  FAQ

**Q:** *Do I always need role tags?*
**A:** Yes. Token streams without explicit roles are inherently unstable at >100 turns.

**Q:** *Will OpenAI “system” field alone work?*
**A:** Helps, but downstream retrieval or multi-agent merges still dilute authority; WFGY adds extra enforcement.

**Q:** *Is ΔS expensive to compute each turn?*
**A:** Sentence-level embeddings (768–1536 d) are fast; cache results in memory store.

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

