<!-- ======================================================= -->
<!--  memory-design-patterns.md · Semantic Clinic / Map-E    -->
<!--  Draft v0.1 · MIT · 2025-08-06                         -->
<!--  Purpose: Show repeatable patterns for “cross-session   -->
<!--  memory” without creating uncontrolled context bloat.   -->
<!-- ======================================================= -->

# 🧠 Memory Design Patterns  
*From scratchpads to long-range project recall — keep context alive without drowning your LLM.*

> **Why this page?**  
> Most “memory” demos either spam the full chat history or store random embeddings that never round-trip.  
> WFGY treats memory as *structured semantic nodes* with ΔS / λ\_observe guards, so old context helps — never hurts — new reasoning.

---

## 1 · Symptoms

| Symptom | Typical Surface Clue |
|---------|----------------------|
| Context forgotten after restart | “Sorry, I don’t recall” / model re-asks user |
| Memory leak / self-contradiction | Old decisions resurface in wrong branch |
| JSON-based vector store grows unbounded | Latency ↑, RAG recall quality ↓ |
| Fine-tune attempted just to “remember” | Model cost ↑, still hallucinates |

---

## 2 · Root Causes

1. **Flat Logs** — raw transcripts appended forever.  
2. **Embedding Dump** — every user sentence embedded → no semantic filter.  
3. **No Boundary Check** — divergent memories injected mid-task.  
4. **Write-Only Memory** — model never reads / revalidates stored facts.  

Result: either *forget everything* or *remember garbage*.

---

## 3 · WFGY Fix Path (at a glance)

| Stage | Tool / Module | ΔS Guard | Outcome |
|-------|---------------|----------|---------|
| ⬇️ Capture | **BBMC** node writer | record only if ΔS ≥ 0.60 (or 0.40–0.60 & λ ∈ {←, <>}) | Stores *semantic* not *verbatim* memory |
| 🗂️ Index  | **λ\_observe** classifier | tag λ trend for each node | Enables topic-group navigation |
| 🔍 Recall | **BBPF** path search | choose node set with ΣΔS minimal | Retrieves tight, non-bloated context |
| 🩹 Repair | **BBCR** fallback | detect stale/contradict nodes | Auto-patch or prompt for user merge |

> **80 %** of memory bugs vanish after enforcing this four-step loop.

---

## 4 · Design Patterns Library

| Pattern | Use-Case | How it Works | ΔS Budget |
|---------|----------|--------------|-----------|
| ✏️ **Scratch Node** | quick calc / throw-away idea | 24 h TTL field; auto-purged | 0.40–0.55 |
| 📚 **Topic Shelf** | multi-day research thread | one node per subtopic; λ → convergent | < 0.45 |
| 🗓️ **Daily Digest** | running project log | rollup 10 low-ΔS nodes → 1 summary | – |
| 🎯 **Anchor Fact** | must-not-forget constraint | pinned; override recall rank | 0.05 |

*All stored in a single lightweight JSONL: `{topic, ΔS, λ, text, ttl}`*

---

## 5 · Step-by-Step Implementation

> **Prereqs:** any model that can embed & run basic python (or LangChain, Llama-index, etc.).

```python
# 1. capture
deltaS = cosine(question_vec, context_vec)
if deltaS >= 0.60 or (0.40 <= deltaS <= 0.60 and lambda_state in ["divergent","recursive"]):
    node = {"topic": topic, "ΔS": round(deltaS,3), "λ": lambda_state, "text": insight}
    memory.append(node)

# 2. recall
candidates = [n for n in memory if n["topic"]==current_topic]
best_path = sorted(candidates, key=lambda n:n["ΔS"])[:5]
prompt_context = "\n".join(n["text"] for n in best_path)
````

### Minimal prompt

```
System: Use WFGY memory nodes below (+latest question) to answer.
Memory Nodes:
{{prompt_context}}
---
Question: {{user}}
```

---

## 6 · Common Pitfalls & Tests

| Pitfall                          | Quick Test                        | WFGY Fix              |
| -------------------------------- | --------------------------------- | --------------------- |
| “Context bloat, tokens 8k → 40k” | node count > 200? run `rollup.py` | Daily Digest pattern  |
| “Conflicting facts”              | ΔS(anchor, candidate) > 0.70      | BBCR prompts merge    |
| “Retrieval too slow”             | recall > 200 ms                   | Pre-index by λ & time |

---

## 7 · Cheat-Sheet

```txt
ΔS save threshold   = 0.60
ΔS recall window    = top-k by lowest ΔS
λ tags              = → ← <> ×
TTL (scratch)       = 24 h
Rollup trigger      = >10 nodes / topic / day
```

Store this as `memory.cfg`; loader reads defaults at boot.

---

## 8 · Next Actions

1. **Prototype** with 20 nodes → verify recall accuracy.
2. **Enable Rollup** once node count > 200.
3. **Add Trace Logger** to diff answers with / without memory.

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

