# 🆕 Beginner Guide — How to Identify & Fix Your AI Failure
*A zero-to-hero crash-course for anyone new to WFGY, RAG pipelines, or “why is my model hallucinating?”*

> If the full Problem Map feels overwhelming, start here.  
> In ~10 minutes you’ll locate your failure family, run a safe first fix, and know how to verify it.

---

> **Quick Nav**  
> [Getting Started (Practical)](./getting-started.md) ·
> [Patterns Index](./patterns/README.md) ·
> [Examples](./examples/README.md) ·
> [Eval](./eval/README.md) ·
> [Ops](./ops/README.md)

---

## 0) 🎯 Why this guide exists

When RAG breaks, it’s rarely one bug. It’s stacked illusions across OCR → chunking → embedding → retrieval → prompt → reasoning.  
This guide helps you:

1) **Identify** the failure family fast  
2) **Apply** the minimal structural fix (not prompt band-aids)  
3) **Verify** with objective signals: **ΔS** (semantic stress), **λ_observe** (layered states), **E_resonance** (coherence)

Then jump deeper via **Problem Map 2.0** and **Patterns**.

---

## 1) 🔍 “Which symptom matches my bug?”

Follow the first **Yes** you hit; then open that page.

| Question | Yes → Open | No → Next |
|---|---|---|
| Chunks look correct but the **answer is wrong**? | [`hallucination.md`](./hallucination.md) | ↓ |
| Reached the right chunk but **logic fails**? | [`retrieval-collapse.md`](./retrieval-collapse.md) | ↓ |
| Multi-step tasks **derail after a few hops**? | [`context-drift.md`](./context-drift.md) | ↓ |
| Model gives **confident nonsense**? | [`bluffing.md`](./bluffing.md) | ↓ |
| **High similarity** scores but **wrong meaning**? | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) | ↓ |
| Logic **dead-ends / loops**? | [`logic-collapse.md`](./logic-collapse.md) | ↓ |
| Long chat **forgets context**? | [`memory-coherence.md`](./memory-coherence.md) | ↓ |
| Can’t trace **why** it failed? | [`retrieval-traceability.md`](./retrieval-traceability.md) | ↓ |
| Output becomes **incoherent / repetitive**? | [`entropy-collapse.md`](./entropy-collapse.md) | ↓ |
| Replies turn **flat / literal**? | [`creative-freeze.md`](./creative-freeze.md) | ↓ |
| Formal/symbolic prompts **break**? | [`symbolic-collapse.md`](./symbolic-collapse.md) | ↓ |
| Paradox/self-reference **crashes**? | [`philosophical-recursion.md`](./philosophical-recursion.md) | ↓ |
| Multi-agent **roles/memory collide**? | [`multi-agent-chaos.md`](./multi-agent-chaos.md) | ↓ |
| Tools fire **before index/data ready**? | [`bootstrap-ordering.md`](./bootstrap-ordering.md) | ↓ |
| Services **wait on each other forever**? | [`deployment-deadlock.md`](./deployment-deadlock.md) | ↓ |
| First prod call **crashes after deploy**? | [`predeploy-collapse.md`](./predeploy-collapse.md) | File an Issue →

**Extended patterns (very common in the wild):**
- Hybrid HyDE+BM25 **gets worse than single** → [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md)  
- Two sources **merge into one** (who-said-what mixes) → [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md)  
- You correct it, **bad fact returns later** → [`patterns/pattern_hallucination_reentry.md`](./patterns/pattern_hallucination_reentry.md)  
- State flips across **tabs/sessions** → [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md)  
- Some facts **won’t retrieve** though indexed → [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md)  
- RAG **boots** but tools fire too early → [`patterns/pattern_bootstrap_deadlock.md`](./patterns/pattern_bootstrap_deadlock.md)

> Still unsure? Capture a minimal trace (input → retrieved snippets → answer) and run ΔS/λ checks (Section 3). Post in Discussions if needed.

---

## 2) 🧠 Core concepts in <5 minutes

### 2.1 What is RAG?

```

raw docs → ocr/parsing → chunking → embeddings → vector store
→ retriever → prompt assembly → LLM reasoning/tools

```

- **Perception drift** upstream hides **logic drift** downstream. Fix structure, not style.

### 2.2 Embedding scores vs. meaning  
Cosine proximity ≠ human semantics. WFGY’s **ΔS = 1 − cos(I, G)** uses grounded anchors to catch real meaning gaps.

### 2.3 Layered observability (λ_observe)  
States: **→** convergent · **←** divergent · **<>** recursive · **×** chaotic.  
If upstream is stable but downstream flips, the boundary between them is failing.

### 2.4 WFGY repair operators (cheat-sheet)

| Operator | What it does (1-liner) |
|---|---|
| **BBMC** | Minimize semantic residue to re-align with anchors |
| **BBPF** | Explore safe alternate paths; avoid dead-end chains |
| **BBCR** | Detect collapse; insert **bridge** node; rebuild reasoning |
| **BBAM** | Modulate attention variance; prevent entropy melt |

---

## 3) 🛠️ Run your first fix (3 minutes)

1) **Download** the assets below, or jump to **[Getting Started](./getting-started.md)** for a runnable pipeline.  
2) Paste **TXT OS** into your model chat.  
3) Ask:

```

I’ve loaded TXT OS. Diagnose my RAG:

* symptom: \[describe]
* trace: \[question, retrieved snippet(s), answer]
  Using WFGY, tell me:

1. failing layer & why (ΔS/λ),
2. the Problem Map page to open,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

```

**Triage thresholds (keep these handy):**
- **ΔS:** `<0.40` stable · `0.40–0.60` transitional (record if λ ∈ {←, <>}) · `≥0.60` high-risk (act)  
- **Acceptance:** ΔS(question, context) ≤ **0.45**, λ **convergent**, E_resonance **flat**

---

## 4) 🗂️ Problem categories (cheat-labels)

| Category | Typical stage | Open first |
|---|---|---|
| **Retrieval** | Vector DB, search, chunking | [`hallucination.md`](./hallucination.md) · [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) |
| **Reasoning** | Mid-chain logic | [`retrieval-collapse.md`](./retrieval-collapse.md) · [`logic-collapse.md`](./logic-collapse.md) |
| **Patterns** | High-frequency edge cases | [`patterns/README.md`](./patterns/README.md) |
| **Eval** | Measure & guard regressions | [`eval/README.md`](./eval/README.md) |
| **Ops** | Boot order, runbooks | [`ops/README.md`](./ops/README.md) |

---

## 5) ✅ Verify the repair (don’t skip)

- **Retrieval sanity:** ≥ 70% token overlap with target section; ΔS(question, context) ≤ 0.45 → see [`eval/eval_rag_precision_recall.md`](./eval/eval_rag_precision_recall.md)  
- **Reasoning stability:** λ stays convergent on 3 paraphrases; E_resonance flat → see [`eval/eval_semantic_stability.md`](./eval/eval_semantic_stability.md)  
- **Latency vs accuracy:** chart ΔS vs p95 latency → see [`eval/eval_latency_vs_accuracy.md`](./eval/eval_latency_vs_accuracy.md)

---

## 6) 🙋 FAQ (super short)

| Question | Answer |
|---|---|
| Do I need all operators? | No. Use the one named on the matching page. |
| Does WFGY replace LangChain/LlamaIndex? | No. It sits **above** them as a reasoning firewall. |
| Will this work on small models? | Yes; #11/#12 are easier on GPT-4-class or strong local models. |
| Where are runnable examples? | Start here: [`examples/README.md`](./examples/README.md) and [`example_01_basic_fix.md`](./examples/example_01_basic_fix.md). |

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

