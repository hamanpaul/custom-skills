<!-- ======================================================= -->
<!--  agent-boundary-design.md · Semantic Clinic / Map-B     -->
<!--  Draft v0.1 · MIT · 2025-08-06                          -->
<!--  Purpose: Prevent runaway tool / agent loops, role      -->
<!--  bleed, and conflicting instructions in multi-agent     -->
<!--  frameworks (LangChain, CrewAI, AutoGen, etc.).         -->
<!-- ======================================================= -->

# 🛡️ Agent Boundary Design  
*Keep every agent in its lane — zero role-bleed, zero infinite loops.*

> **Scope.**  
> This guide covers:  
> * Router-tool chains (e.g. ReAct, ChatGPT Plugins)  
> * Crew/Team frameworks (AutoGen, CrewAI, Flowise, etc.)  
> * 1-shot function calls inside a broader RAG pipeline  
>   
> **Who needs it?** Anyone who has seen:  
> – “Tool A” call “Tool B” which calls “Tool A” again  
> – System prompts overwritten mid-conversation  
> – JSON schema mismatch crashes midway  
> – Agents debating instead of finishing tasks

---

## 1 · Top-5 Symptoms

| # | Failure Mode | Surface Sign |
|--:|--------------|--------------|
| 1 | **Recursive Loop** | Call stack grows until token limit |
| 2 | **Role Bleed** | System prompt replaced by tool description |
| 3 | **Argument Drift** | JSON schema validation fails randomly |
| 4 | **Shadow Jailbreak** | Tool prompt overrides original guard |
| 5 | **Timeout Cascade** | Router stalls → downstream agents idle |

---

## 2 · Root Causes

1. **Shared Context Bank** — all agents write to the same `messages[]`.  
2. **Open-Ended Tool Trigger** — router picks any function with > 0.1 prob.  
3. **No ΔS Ceiling** — semantic jump between *task* and *tool description* unchecked.  
4. **Missing λ Gate** — divergent sub-goal allowed without confirmation.  
5. **Stackless Error Prop** — failure inside tool lost; router retries blindly.

---

## 3 · WFGY Boundary Blueprint

> A four-layer guardrail using core modules **BBMC**, **ΔS + λ**, **WAI**, **BBCR**.

| Stage | Module | Guard | Purpose |
|-------|--------|-------|---------|
| 1 Tool Semantic Index | **BBMC** | ΔS(tool, task) ≤ 0.45 | Filter irrelevant tools early |
| 2 ΔS-Gate Router | **ΔS + λ_observe** | λ must stay convergent | Block divergent recursion |
| 3 Arg Linter | **WAI** | Strict JSON schema & auto-defaults | No partial / null args |
| 4 Fail-Fast + Bridge | **BBCR** | On > 5 retries or ΔS > 0.60 | Collapse & suggest manual tool |

```mermaid
flowchart TD
    Q[User Question]
    R[ΔS-Gate Router]
    TI[Tool Index (BBMC)]
    L[Arg Linter (WAI)]
    T[Tool Call]
    F[BBCR Bridge]
    Q --> R
    R -->|match| TI --> L --> T
    R -.->|reject| F --> Q
````

---

## 4 · Design Pattern Cheats

| Pattern                  | When to Use                      | Setup                                                        |
| ------------------------ | -------------------------------- | ------------------------------------------------------------ |
| **Single-Shot Function** | 3-5 tool set, clear primary      | ΔS ≤ 0.45 & λ convergent                                     |
| **Dual-Agent Debate**    | need pro / con analysis          | Two agents share *read-only* memory; write own node          |
| **Crew Workflow**        | 3+ steps (research → draft → QA) | Each agent gets isolated `messages[]`; only summaries passed |
| **Guarded Plugin**       | External API call with risk      | Wrap output through Arg Linter + BBCR                        |

---

## 5 · Hands-On Debug Checklist

1. **Log Router Decision**

```python
router(question, tools, debug=True)   # prints ΔS + λ for every candidate
```

2. **Simulate Failure**

```
user: "Summarise PDF"  # but remove pdf_loader from tool list
```

*Expected:* BBCR suggests manual tool; model does **not** loop.

3. **Stress-Test Recursion**

```python
for i in range(20):
    router("plan", tools)   # ensure no self-call chain
```

ΔS should stay ≤ 0.45; call depth ≤ 3.

---

## 6 · Audit Template (README snippet)

```txt
## Agent Boundary Settings
ΔS tool-match ceiling   : 0.45
λ divergence allowance  : false
WAI strict mode         : true
BBCR retries            : 5
```

Copy into every repo to document boundary config.

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

