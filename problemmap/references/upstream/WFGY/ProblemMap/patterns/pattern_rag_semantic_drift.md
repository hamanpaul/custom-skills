# Pattern — RAG Semantic Drift (No.1)

**Scope**  
Answers **sound plausible** but are **not grounded** in retrieved evidence, or they thread together semantically related but **non-authoritative** chunks. Common in long, generic corpora and when chunk borders split **entity** from its **constraints**.

**Why it matters**  
Semantic drift is the primary source of silent hallucinations. It evades naive keyword checks and only shows up when you enforce grounding, citations, and refusal behavior.

> Quick nav: [Patterns Index](./README.md) · Examples: 
> [Example 01](../examples/example_01_basic_fix.md) · 
> [Example 03](../examples/example_03_pipeline_patch.md) · 
> [Eval: Precision & CHR](../eval/eval_rag_precision_recall.md)

---

## 1) Signals & fast triage

**You likely have this if:**
- The model answers without `citations` **or** cites chunks that don’t contain the claim.
- Changing chunk size flips answers from correct → plausible-but-wrong.
- Retrieving more chunks **degrades** precision (tail noise stitching).
- Reports from Example 02 label many cases as `generation_drift`.

**Deterministic checks (no LLM needed):**
- **Template compliance:** output has `citations: [id,...]` **or** equals `not in context`.
- **Citation overlap:** cited ids ⊆ retrieved ids.
- **Containment:** any ≥5-char phrase from answer appears verbatim in evidence.

> Use `reflect.py` / `reflect.mjs` from **Example 02**; the label `generation_drift` is your smoking gun.

---

## 2) Minimal reproducible case

Create `data/chunks.json`:

```json
[
  {"id":"p1#1","text":"X is a constrained mapping used in the alpha protocol."},
  {"id":"p1#2","text":"Constraints: X must preserve ordering and reject null keys."},
  {"id":"p2#1","text":"Y is a generalized mapping often compared to X in blogs."}
]
````

Two questions:

* **Q1**: “What is X?” → correct chunk is `p1#1`, optionally `p1#2` for constraints.
* **Q2**: “List X’s constraints.” → correct chunk is `p1#2`.

**Repro:**
Run **Example 01** but increase top-k to 12 without rerank or knee cut. You’ll see the model stitch `p2#1` into the answer when it shouldn’t.

---

## 3) Root causes

* **Chunk boundary split**: entity in one chunk, constraints in another; retrieval returns only one half.
* **Tail noise**: irrelevant but semantically nearby chunks flood the prompt.
* **Index/schema drift**: embedding model or normalization mismatch yields incomparable scores (see Example 05).
* **Prompt freedom**: no evidence-only contract; model “fills gaps” from prior knowledge.
* **Query parsing**: multi-intent queries aren’t decomposed; the pipeline answers the wrong sub-intent first.

---

## 4) Standard fix (ordered, minimal, measurable)

**Step 1 — Enforce guard** (Example 01)

* Template: evidence-only + refusal token.
* Require `citations: [id,...]`. Treat missing citations as **failure**.

**Step 2 — Stabilize retrieval** (Example 03)

* Candidate pools: BM25 **and** embeddings → **intersection**, union fallback only if needed.
* Rerank by cosine; **knee cutoff**; keep **top-8**.
* Shrink chunk size so **entity + constraints** co-locate.

**Step 3 — Validate index** (Example 05)

* Refuse queries when manifest mismatches runtime.
* Rebuild and re-baseline recall\@k.

**Step 4 — Add acceptance gate** (Example 04)

* Scholar emits claim+citations inside **scope.allowed\_ids**; Auditor validates.
* If `INVALID` or `NOT_IN_CONTEXT` → do **not** emit text.

**Step 5 — Evaluate** (Example 08)

* Track Precision (answered), Over/Under-refusal, Citation Hit Rate.
* Compare before/after; lock gates in CI.

---

## 5) “Good” vs “Bad” outputs (deterministic examples)

**Good (answerable):**

```
- claim: X is a constrained mapping used in the alpha protocol.
- citations: [p1#1]
```

**Good (answerable with constraints):**

```
- claim: X preserves ordering and rejects null keys.
- citations: [p1#2]
```

**Good (unanswerable):**

```
not in context
```

**Bad (semantic drift):**

```
- claim: X is similar to Y and generally used in blogs.
- citations: [p2#1]     # off-topic; no constraints; not authoritative
```

---

## 6) Acceptance criteria (ship/no-ship)

A response **may ship** only if **all** hold:

1. Output equals refusal token **or** includes `citations` list.
2. `citations ⊆ retrieved_ids` and **containment** passes.
3. If multi-agent is used, **Auditor** verdict is `VALID`.
4. **Eval gates**:

   * Precision (answered) ≥ 0.80
   * Under-refusal ≤ 0.05
   * Citation Hit Rate ≥ 0.75

Otherwise → refuse, retry retrieval, or escalate UX.

---

## 7) Prevention (contracts & defaults)

* **Chunking contract**

  * Target **250–400 tokens**; never exceed 512 without reason.
  * Prefer **semantic paragraph + header** over fixed windows when regulations/constraints exist.
  * Include stable `id`, `source`, `page`, `version`.

* **Retrieval defaults**

  * Pools: `TOPK_LEX=40`, `TOPK_SEM=40` → **intersection**, fallback to union if `|∩| < 8`.
  * Rerank: cosine vs query; keep **top-8**; apply **knee cut**.

* **Prompt contract**

  * Evidence sandbox; forbid links/tools; **JSON-only** schema.
  * Refusal token: `not in context` (exact string).

* **Index manifest**

  * Pin `embedding.model`, `dimension`, `normalized`, `metric`, `chunker.version`.
  * Validator must **abort** requests on mismatch.

---

## 8) Debug workflow (10 minutes)

1. Run **Example 02** and export `runs/report.jsonl`.
2. Filter `generation_drift` cases.
3. Inspect retrieved ids vs cited ids; if mismatch → go to Example 03.
4. If retrieval is fine but answer still floats → tighten guard (Example 01) and gate with Auditor (Example 04).
5. Re-score with **Example 08**; commit the `eval/report.md` diff.

---

## 9) Common traps & fixes

* **Raising top-k “to be safe”** → increases tail noise → worse drift. Fix with **intersection + knee cut**.
* **Large chunks to “add context”** → model stops citing; answers look right but are ungrounded. **Shrink** and **co-locate** constraints.
* **Mixing indices** (different models/dims) across environments → incomparable scores. **Validate manifest**; rebuild.
* **Treating refusal as failure** → trains teams to prefer bad answers. Count correct refusals as **success**.

---

## 10) Minimal checklist (copy into PR)

* [ ] Guarded template enforced; refusal token exact match.
* [ ] Intersection+r̲e̲r̲a̲n̲k̲ with knee cut; top-8.
* [ ] Manifest validated at boot; readiness flips only after sentinel passes.
* [ ] Auditor gate in place (if multi-agent).
* [ ] Eval gates pass: Precision / Under-refusal / CHR thresholds.

---

## References to hands-on examples

* **Example 01** — Guarded template + trace
* **Example 02** — Reflection triage (`generation_drift`)
* **Example 03** — Intersection + Rerank + Knee
* **Example 04** — Multi-agent acceptance gate
* **Example 05** — Manifest & index repair
* **Example 08** — Quality scoring & CI gates

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

