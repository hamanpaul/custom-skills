# Patterns — Failure Catalog (Problem Map 2.0)

This folder is a **field guide** to recurring failures in RAG and multi-stage LLM pipelines.  
Each pattern is **actionable**: fast signals, root causes, a minimal repro, a deterministic fix, and links to hands-on examples (SDK-free, stdlib-only).

**How to use this folder**

1) Start with the **symptom** you’re seeing.  
2) Open the matching **pattern** and run the *Minimal Repro* + *Standard Fix*.  
3) Wire the **acceptance criteria** into CI (see Example 08) so the fix stays fixed.

---

## Quick Index

| Pattern | Problem Map No. | Symptoms you’ll see | Fix entrypoint |
|---|---:|---|---|
| **RAG Semantic Drift** ([pattern_rag_semantic_drift.md](./pattern_rag_semantic_drift.md)) | **No.1** | Plausible but ungrounded answers; citations don’t contain the claim | [Example 01](../examples/example_01_basic_fix.md), [Example 03](../examples/example_03_pipeline_patch.md) |
| **Memory Desync** ([pattern_memory_desync.md](./pattern_memory_desync.md)) | — (State/Context) | Old names/IDs reappear; agents disagree across turns | [Example 04](../examples/example_04_multi_agent_coordination.md) |
| **Vector Store Fragmentation** ([pattern_vectorstore_fragmentation.md](./pattern_vectorstore_fragmentation.md)) | **No.3** | Recall flips across envs; score scales change; rank inversions | [Example 05](../examples/example_05_vectorstore_repair.md) |
| **Hallucination Re-Entry** ([pattern_hallucination_reentry.md](./pattern_hallucination_reentry.md)) | — (Provenance) | Model’s prior text shows up as “evidence”; non-corpus sources cited | [Example 06](../examples/example_06_prompt_injection_block.md) |
| **Bootstrap Deadlock** ([pattern_bootstrap_deadlock.md](./pattern_bootstrap_deadlock.md)) | **No.14** | `/readyz` stuck/flapping; circular waits at startup | [Example 07](../examples/example_07_bootstrap_ordering.md) |
| **Query Parsing Split** ([pattern_query_parsing_split.md](./pattern_query_parsing_split.md)) | — (Parsing) | Multi-intent prompts answered partially or mixed | [Example 03](../examples/example_03_pipeline_patch.md), [Example 04](../examples/example_04_multi_agent_coordination.md) |
| **Symbolic Constraint Unlock (SCU)** ([pattern_symbolic_constraint_unlock.md](./pattern_symbolic_constraint_unlock.md)) | **No.11** (Symbolic collapse) | “Must/Only/Never” rules vanish mid-pipeline; impossible states | [Example 03](../examples/example_03_pipeline_patch.md), [Example 04](../examples/example_04_multi_agent_coordination.md), [Example 08](../examples/example_08_eval_rag_quality.md) |


> **Legend:** Problem Map numbers refer to root categories used across the repo. “—” means cross-cutting (not a single number).

---

## Pick-a-Pattern in 30 Seconds (Triage Flow)

1. **Grounding first** — Run Example 01 on a few failing questions.  
   - If refusal behavior or citations fail ⇒ go to **Semantic Drift**.  
2. **Context/state sanity** — Check `context_id` / `mem_rev/hash`.  
   - Mismatch ⇒ **Memory Desync**.  
3. **Index parity** — Validate `index_out/manifest.json` vs runtime.  
   - Drift or score scale shift ⇒ **Vector Store Fragmentation**.  
4. **Provenance** — Inspect `source` for cited ids.  
   - Any `model|chat|tmp:` ⇒ **Hallucination Re-Entry**.  
5. **Startup** — If the first minute after deploy is flaky ⇒ **Bootstrap Deadlock**.  
6. **Query shape** — If the prompt mixes “compare… then draft…” ⇒ **Query Parsing Split**.  
7. **Logic rules** — If answers cross “must/only/never” boundaries ⇒ **SCU**.

---

## Standard Acceptance Gates (copy to CI)

- **Guarded Output:** either exact refusal token `not in context` **or** JSON with `claim` + `citations:[id,…]` scoped to retrieved ids.  
- **Provenance:** all citations pass the corpus-only filter (no `chat:/draft:/tmp:`).  
- **Context Consistency:** if used, `context_id.mem_rev/hash` echoes the turn snapshot.  
- **Constraint Integrity (SCU):** `constraints_echo` ≡ locked set; no contradiction patterns matched.  
- **Quality Gates (Ex.08):** precision≥0.80, under-refusal≤0.05, citation hit rate≥0.75.

---

## File Layout

- [pattern_rag_semantic_drift.md](./pattern_rag_semantic_drift.md) — How to stop plausible-but-wrong answers with hard grounding.  
- [pattern_memory_desync.md](./pattern_memory_desync.md) — One snapshot per turn; bind and echo across agents.  
- [pattern_vectorstore_fragmentation.md](./pattern_vectorstore_fragmentation.md) — Keep embeddings/metrics/chunkers aligned.  
- [pattern_hallucination_reentry.md](./pattern_hallucination_reentry.md) — Keep model/session text out of evidence.  
- [pattern_bootstrap_deadlock.md](./pattern_bootstrap_deadlock.md) — Deterministic startup ordering and readiness.  
- [pattern_query_parsing_split.md](./pattern_query_parsing_split.md) — Deterministically split multi-intent prompts.  
- [pattern_symbolic_constraint_unlock.md](./pattern_symbolic_constraint_unlock.md) — Lock+echo constraints; gate contradictions.

See [../examples/](../examples/README.md) for runnable, stdlib-only code referenced in each pattern.


---

## Contributing (tight process)

1. **Propose** a new pattern via issue labels: `pattern-proposal`, with minimal repro + acceptance gate.  
2. **Stabilize** with an example (Python or Node, stdlib-only).  
3. **Add** to this README only after approval.  
4. **Guard** with Example 08 metrics before shipping a pattern-driven fix.

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

