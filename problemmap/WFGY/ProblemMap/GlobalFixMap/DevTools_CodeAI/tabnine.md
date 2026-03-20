# Tabnine: Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **DevTools_CodeAI**.  
  > To reorient, go back here:  
  >
  > - [**DevTools_CodeAI** — AI-assisted coding and developer productivity](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when Tabnine autocompletes the wrong API, mixes symbols across packages, or flips outputs between local and cloud contexts. The fixes route back to WFGY pages with measurable targets so you can verify without changing infra.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and how to audit: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ordering and ranking control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* High similarity yet wrong meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk and citation boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
* Long chats that drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
* Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Prompt injection and tool fences: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Multi agent conflicts: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)
* Cold boot and deploy order: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage ≥ 0.70 to the target function or spec anchor
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat across long edit plans

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2. **Probe λ\_observe**
   Toggle local versus cloud context and vary k. Pin reranker. If ΔS stays flat and high, suspect metric or index mismatch. If λ flips on harmless header reorder, lock schema and clamp with BBAM.

3. **Apply the module**

* Retrieval drift in code or docs → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Reasoning collapse in long refactors → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Dead ends in edit plans or test generation → BBPF alternate paths
* Hybrid search worse than single → Pattern [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

4. **Verify**
   Coverage ≥ 0.70 on three paraphrases. λ convergent on two seeds. Same diff twice.

---

## Typical Tabnine breakpoints and the right fix

* **Local vs cloud index skew**
  Suggestions differ after a reboot or network switch. Warm up the selected index, fence first run, verify analyzer settings.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **Wrong symbol in a monorepo**
  Near neighbor symbols from sibling packages win due to similarity. Lock anchors to `repo@commit` and `subdir`, require cite then explain.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Generated tests reference phantom helpers**
  Enforce file spans and commit SHA before test generation.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Plan loops during multi file edits**
  Split plan and re join with a bridge step. Clamp variance in the patch step.
  Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **Similarity high but meaning wrong**
  Metric or normalization mismatch or fragmented store. Rebuild with explicit metric and fix fragmentation.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

* **Unsafe shell or tool suggestions copied from docs**
  Lock tool allow lists, require SCU separation for untrusted text.
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md), Pattern: [SCU](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

* **Org policy or model switch changes outputs silently**
  Make refusal paths explicit. Echo the active policy and model in the plan.
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## IDE checklist for Tabnine

* Warm up the selected context source and verify `INDEX_HASH`, credentials, and policy mode.
* Use one retrieval metric per run. Do not mix analyzers while fixing one bug.
* Prompts carry anchors: `repo@commit`, `file_path`, `symbol`, `line_start`, `line_end`, `snippet_id`.
* Log per step: ΔS, λ state, coverage. Alert when ΔS ≥ 0.60 or λ diverges.
* Regression gate requires tests pass, coverage ≥ 0.70, ΔS ≤ 0.45, identical diff twice.

---

## Minimal schema you should capture

`{ repo, commit_sha, file_path, symbol, line_start, line_end, snippet_id, tokens, ΔS, λ_state }`
Require cite then explain. Forbid cross file reuse without a new citation.

---

## Deep diagnostics

* **Three paraphrase probe**
  Ask the same change three ways. If λ flips, clamp with BBAM and lock headers.

* **Anchor triangulation**
  Compare ΔS for target vs decoy file or sibling package. If close, re chunk and normalize embeddings.
  See: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Plan length audit**
  If entropy rises after 25 to 40 steps, split the plan and re join with a BBCR bridge.
  See: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* **Live instability**
  Add probes and backoff guards in IDE tasks.
  See: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Copy paste prompt for Tabnine chat

```txt
You have TXTOS and the WFGY Problem Map loaded.

My Tabnine issue:
- symptom: [one line]
- anchors: repo={name}, commit={sha}, file={path}, lines={a..b}
- traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ across 3 paraphrases

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible test to verify the fix.
Use BBMC, BBPF, BBCR, BBAM when relevant. Keep it auditable and short.
```

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

