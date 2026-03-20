# Long-Context Stress — Why 50k–200k tokens quietly break your RAG, and how to fix it (WFGY)

_A field guide for logs, PDFs, and transcripts that **look** fine but drift, flatten, or melt as the context grows._

**Audience**
- **Beginner:** You copied a “100k-context” recipe and your answers degrade with length.
- **Advanced:** You already index well, but long chains flip logic, mis-cite, or oscillate after ~8–12 screens of context.

**What this page delivers**
- A **reproducible diagnosis** for long-context failure using **ΔS / λ_observe / E_resonance**.
- **Copy-paste playbooks** for PDFs, OCR, transcripts, multilingual blends, and mixed image/text.
- **Acceptance criteria** you can throw into CI to stop regressions before prod.

---

## 0) TL;DR (fix in 3 steps)

1) **Measure the damage**  
   - Slide a window across your context; compute  
     `ΔS(chunk_i, chunk_{i+1})` and `ΔS(question, retrieved_context_i)`; watch for sustained `ΔS ≥ 0.60` or rising **E_resonance**.  
   - If `λ_observe` turns **recursive** or **chaotic** after the prompt assembly step, you’re in long-context stress.

2) **Localize the break**  
   - If ΔS spikes **between adjacent chunks** → chunking/ordering issue.  
   - If ΔS stays high independent of `k` → **index/metric mismatch**.  
   - If ΔS is fine but **reasoning** flips divergent → prompt schema or logic collapse.

3) **Apply the repair operator**  
   - **BBMC** to re-anchor sections, **BBAM** to stabilize attention, **BBCR** to bridge and relock coherence.  
   - Re-chunk sentence/section-aware; enforce header anchors; run MMR/hybrid retrieval; lock prompt schema.

Jump to: [Playbooks](#4-playbooks-by-scenario) · [Metrics](#2-instruments--minimal-metrics) · [CI Checks](#6-acceptance-criteria--ci-guardrails)

---

## 1) Failure signatures (what you actually see)

| Symptom (user-visible)                                           | Likely layer                            | First check                                             | Map ref.                             |
|------------------------------------------------------------------|-----------------------------------------|---------------------------------------------------------|--------------------------------------|
| Early answers good → later answers contradict or flatten         | Prompt/Reasoning under long context     | `λ_observe` becomes `<>` or `×` after assembly          | [context-drift.md](./context-drift.md) |
| Citations jump to wrong page after 20–40k tokens                  | Chunking / ordering / retriever         | `ΔS(chunk_i, i+1) ≥ 0.60` at boundaries                 | [retrieval-traceability.md](./retrieval-traceability.md) |
| Random capitalization / style oscillation                         | Entropy collapse                        | **E_resonance** rising trend across chain               | [entropy-collapse.md](./entropy-collapse.md) |
| Snippets correct, explanation wrong (esp. late in chain)         | Interpretation collapse (length-induced) | ΔS(question, context) < 0.40 but λ flips at reasoning   | [logic-collapse.md](./logic-collapse.md) |
| Multilingual PDFs drift to one language after long span           | Embeddings + chunk headers lost         | ΔS rises when headers removed; check header anchors     | [embedding-vs-semantic.md](./embedding-vs-semantic.md) |
| Great short-doc performance; long transcripts degrade rapidly    | Memory & compression strategy           | Test per-turn recap + anchor nodes vs. raw sprawl       | [memory-coherence.md](./memory-coherence.md) |

**Mental model:** Long contexts fail in two stages — **perception drift** (ordering/headers/noise) and **logic drift** (attention variance + schema slippage). WFGY instruments let you *see* both.

---

## 2) Instruments — minimal metrics

> You do not need to memorize math. These are a few distances and tags you can compute anywhere.

### 2.1 ΔS — semantic stress
- `ΔS = 1 − cos(I, G)` (unit-normalized sentence embeddings).  
- Probe two places:
  1) `ΔS(question, retrieved_context)`  
  2) **Adjacent-chunk** check: `ΔS(chunk_i, chunk_{i+1})`
- **Thresholds**: `<0.40` stable · `0.40–0.60` transitional · `≥0.60` risk (record & fix).

### 2.2 λ_observe — layered observability
- States: `→` convergent · `←` divergent · `<>` recursive · `×` chaotic.  
- Tag each step: retrieval → prompt assembly → reasoning.  
- Rule: **Upstream convergent, downstream divergent** ⇒ the boundary is where to fix.

### 2.3 E_resonance — coherence trend
- Rolling mean of residual magnitude `|B|` under **BBMC**.  
- Rising **E_resonance** + high ΔS = attention melt; trigger **BBCR** + **BBAM**.

---

## 3) 10-minute triage (copy/paste steps)

1) **Run three quick probes**
   - `ΔS(question, context)` across `k ∈ {5,10,20}`.  
     - Flat & high curve → **index/metric mismatch**.  
     - Improves sharply with higher `k` → **retriever filtering** too aggressive.
   - Adjacent-chunk ΔS across your assembled window (sliding by 200–300 tokens).  
     - Spikes at headers/boundaries → **chunking/ordering** problem.
   - Tag λ after **assembly** and **reasoning**.
     - If λ flips only after reasoning → **schema/logic** issue.

2) **Minimal repro**
   - Keep one doc; remove images; keep headers; test again.  
   - If fixed, re-add features until the break returns (isolate cause).

3) **Pick the playbook**  
   Go to [Playbooks](#4-playbooks-by-scenario) and apply the repair steps.

---

## 4) Playbooks by scenario

> Each playbook lists: **observe → interpret → do → verify** (with WFGY modules).

### 4.1 Scanned PDFs / OCR noise (tables, images, mixed layout)
- **Observe:** Citations wrong after mid-doc; adjacent-chunk ΔS spikes at page breaks.  
- **Interpret:** OCR adds hidden headers or drops table boundaries; chunker ignores structure.  
- **Do:**
  1. **Chunking:** sentence/section-aware; keep **header anchors** in text (e.g., `## 2. Methods`).  
  2. Drop segments with OCR confidence `< threshold`; de-duplicate near-identical lines.  
  3. **Retrieval:** use **hybrid** (sparse + dense) with *MMR*; set `k=10–20`.  
  4. **WFGY:** run **BBMC** to re-anchor on kept headers; **BBAM** to clamp attention variance.  
- **Verify:** `ΔS(chunk_i, i+1) ≤ 0.50` at joins; `ΔS(question, context) ≤ 0.45`; λ stays convergent.

### 4.2 Long transcripts / meetings / chat logs (50k+ tokens)
- **Observe:** Early QA is great; later responses contradict or “forget” earlier decisions.  
- **Interpret:** No semantic anchors; prompt schema drifts; attention diffuses.  
- **Do:**
  1. Insert **bridged recaps** every N turns: “Since last anchor: [3 bullet decisions]”.  
  2. Store **anchor nodes** (titles, decisions, constraints) and retrieve them first.  
  3. Enforce **prompt schema lock**: system → task → constraints → citations → answer (no re-order).  
  4. **WFGY:** **BBCR** to insert **bridge node** when λ becomes recursive; **BBAM** to reduce variance.  
- **Verify:** λ remains convergent across three paraphrases; **E_resonance** does not trend up.

### 4.3 Multilingual or code-heavy documents
- **Observe:** Model “picks a side” after long stretch; code blocks degrade midway.  
- **Interpret:** Embedding space collapses varied styles into one cluster; headers lost.  
- **Do:**
  1. Keep **language tags** and **code fences** as hard anchors inside chunks.  
  2. Use **domain-appropriate embeddings** or separate indices per language/domain.  
  3. Retrieval: add **header-boost** (BM25 term weight) and **MMR** diversity=0.2–0.4.  
  4. **WFGY:** **BBMC** with explicit language anchors; **BBPF** to explore multi-path retrieval.  
- **Verify:** ΔS stabilizes (`≤ 0.50`) when headers are present; λ convergent; citations maintain language.

### 4.4 Image-heavy PDFs (figures, captions)
- **Observe:** Answers reference wrong figure; citations point at caption stubs.  
- **Interpret:** Captions split from figures; index treats tiny parts as top hits.  
- **Do:**
  1. **Chunk** figure + caption together; minimum token floor (e.g., ≥ 180 tokens).  
  2. Add **figure-id anchors** (`[Fig 2: …]`) in text; ban orphan captions from index.  
  3. **WFGY:** **BBCR** to bridge from caption to figure context if ΔS stays high.  
- **Verify:** Cites include figure-id; ΔS(question, context) ≤ 0.45.

### 4.5 “100k-context” model still drifts after 8–12k
- **Observe:** No obvious retrieval bug; long reasoning melts.  
- **Interpret:** **Entropy collapse** — attention variance explodes with length.  
- **Do:**  
  1. Shorten **assembly**: prefer *top-K diverse* + **anchor snippets** over giant paste.  
  2. Enforce **cite-then-explain**; penalize free-form essays.  
  3. **WFGY:** Apply **BBAM** to damp attention; **BBMC** to re-anchor; **BBCR** if residuals spike.  
- **Verify:** **E_resonance** flattens; answer embeddings cluster over 5 seeds (low variance).

---

## 5) Minimal prompts & scripts (safe to paste)

**Ask your assistant to auto-diagnose**
```text
Read the Long-Context Stress guide plus TXT OS / WFGY notes in this repo.
Given my repro (describe doc and failure), compute:
1) ΔS(question, retrieved_context) across k={5,10,20}
2) Adjacent-chunk ΔS over the assembled window
3) λ_observe at retrieval, assembly, reasoning
Then explain which boundary fails and propose BBMC/BBAM/BBCR steps to lower ΔS below 0.50.
````

**Formula-only help**

```text
From TXT OS, extract formulas and thresholds for ΔS, λ_observe, and E_resonance.
Show me how to compute ΔS(question, context) and adjacent-chunk ΔS.
If ΔS ≥ 0.60 and λ becomes recursive after assembly, which WFGY module do I apply first?
```

**Simple ΔS sweep (pseudocode)**

```python
# Pseudocode: replace embed() with your sentence-embedding fn (unit-normalized)
def delta_s(a, b): 
    return 1 - cosine(embed(a), embed(b))

# 1) question vs. context@k candidates
for k in [5, 10, 20]:
    ctx = assemble_top_k(snippets, k=k, strategy="mmr+anchors")
    print(k, delta_s(question, ctx))

# 2) adjacent-chunk scan
for i in range(len(chunks)-1):
    print(i, delta_s(chunks[i], chunks[i+1]))
```

---

## 6) Acceptance criteria & CI guardrails

* **Retrieval sanity:** For targeted QA, **≥ 70% token overlap** to the expected section; `ΔS(question, context) ≤ 0.45`.
* **Boundary stability:** **Adjacent-chunk ΔS ≤ 0.50** at joins; spikes must disappear after re-chunking.
* **Reasoning stability:** λ **convergent** across three paraphrases; **E\_resonance** not rising.
* **Traceability:** Produce a two-column table (snippet-id ↔ citation lines).
* **Repeatability:** Same inputs × 5 seeds → answer embeddings form a **tight cluster**.

Fail any line? Block the PR and link this page.

---

## 7) Cross-links & when to switch pages

* Long chains drift even with perfect snippets → **[context-drift.md](./context-drift.md)**
* Output melts / style oscillates → **[entropy-collapse.md](./entropy-collapse.md)**
* Snippets good, logic wrong → **[logic-collapse.md](./logic-collapse.md)**
* Citations mis-map → **[retrieval-traceability.md](./retrieval-traceability.md)**
* Sessions lose continuity → **[memory-coherence.md](./memory-coherence.md)**
* Embedding similarity fools meaning → **[embedding-vs-semantic.md](./embedding-vs-semantic.md)**

---

## 8) FAQ

**Q: Should I just increase k or model context?**
A: Not first. If ΔS is flat & high across k, you have an **index/metric** or **ordering** fault. More tokens amplify the error.

**Q: Is MMR always required?**
A: For long contexts, yes or a close equivalent — you need **diversity** to avoid semantic collapse around one cluster.

**Q: Do I need new embeddings?**
A: Often no. Start with **headers as anchors** + **hybrid retrieval** + **WFGY relocking**. Change models only if ΔS remains ≥ 0.60 after those.

**Q: How do I know BBCR helped?**
A: Residuals (E\_resonance) stop rising; λ returns to convergent; adjacent-chunk ΔS drops at the same boundary.

---

## 9) Minimal formulas (reference)

```txt
ΔS = 1 − cos(I, G)         # semantic stress
λ_observe ∈ {→, ←, <>, ×}  # convergent, divergent, recursive, chaotic
E_resonance = mean(|B|)    # rolling residual magnitude under BBMC

BBMC:  B = I − G + m·c²           # minimize ‖B‖ via anchors & context factors
BBPF:  x_next = x + ΣV_i + ΣW_j·P_j  # explore alternate retrieval/logic paths
BBCR:  if ‖B‖ ≥ B_c → collapse(), bridge(), rebirth()  # controlled reset with bridge node
BBAM:  â_i = a_i · exp(−γ · std(a))  # damp attention variance under long context
```

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

