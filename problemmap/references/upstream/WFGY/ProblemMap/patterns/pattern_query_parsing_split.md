# Pattern — Query Parsing Split (Multi-Intent / Wrong Sub-Intent First)

**Scope**  
A single user query actually contains **multiple intents** (lookup + policy + transformation + generation), but the pipeline treats it as **one** retrieval/generation ask. The system answers the **easiest/earliest** sub-intent and ignores the rest, or mixes intents, causing off-topic retrieval and wrong acceptance decisions.

**Why it matters**  
Multi-intent queries are common (“compare A vs B and give a summary with citations”). If you don’t split, retrieval pools and prompts blur constraints, you get **false grounding**, and audit trails become meaningless (“which intent did this citation serve?”).

> Quick nav: [Patterns Index](./README.md) · Examples: 
> [Example 01](../examples/example_01_basic_fix.md) · 
> [Example 03](../examples/example_03_pipeline_patch.md) · 
> [Eval: Precision & CHR](../eval/eval_rag_precision_recall.md)

---

## 1) Signals & Fast Triage

**Likely symptoms**
- The answer handles **only part** of the question (e.g., explains A but not B or the comparison).
- Retrieved chunks mix unrelated facets (policy + tutorial + changelog) → noisy context, low CHR.
- Auditor (Example 04) flips `VALID` ↔ `NOT_IN_CONTEXT` depending on which fragment the model latched onto.
- Example 02 labels skew to `query_parse_error`.

**Deterministic checks (no LLM)**
- **Separator heuristics**: query contains `and`, `vs`, `;`, `,`, numbered lists `1) 2)`, or colon-scoped asks (“X: do Y, then Z”).  
- **Verb phase count**: ≥2 finite verbs across different objects (`compare`, `explain`, `implement`, `deploy`).  
- **Constraint tokens**: presence of at least one **data** intent (`find`, `lookup`, `cite`) and one **action** intent (`summarize`, `generate`, `rewrite`).  
If ≥2 signals → treat as **multi-intent** and split.

---

## 2) Minimal Reproducible Case

`data/chunks.json`:

```json
[
  {"id":"pA#1","text":"Policy A: Only domain example.com is allowed."},
  {"id":"pB#1","text":"Policy B: Allow *.company.com and partner domains."},
  {"id":"pC#1","text":"How to edit email settings in the dashboard."}
]
````

User query:
**“Compare Policy A vs B with citations, then draft an email asking IT to switch our domain.”**

Naive pipelines either:

1. Summarize A **or** B only, **or**
2. Draft the email **without** grounded comparison.

---

## 3) Root Causes

* **Single-turn monolith**: retrieval runs once on the whole sentence; constraints collide.
* **No intent schema**: pipeline can’t represent “first compare (grounded), then draft (un-grounded).”
* **Prompt overloading**: one template tries to do comparison + generation + policy proof.
* **Acceptance gate blind**: Auditor validates a claim that mixes two intents.

---

## 4) Standard Fix (Ordered, Minimal, Measurable)

**Step 1 — Detect & Split**

* Run deterministic heuristics (Section 1) to produce **sub-intents** with **roles**: `COMPARE`, `LOOKUP`, `DRAFT`, `REWRITE`, etc.
* Each sub-intent gets its **own** retrieval pool and acceptance rule.

**Step 2 — Bind Contracts per Sub-Intent**

* Evidence-only template for **grounded** intents (`COMPARE`, `LOOKUP`) → requires `citations: [id,...]`.
* Free-form template for **creative** intents (`DRAFT`) → must **echo** the grounded summary id (handoff contract) but does **not** add new citations.

**Step 3 — Sequence with Handoffs**

* Output of grounded step → `summary.claim`, `citations`.
* Draft step **may** rephrase but cannot introduce new factual claims; it references the **handoff id**.

**Step 4 — Accept or Refuse**

* Accept only if **grounded** step is `VALID` (Example 04) **and** draft step references the correct handoff id.
* If grounded step is `NOT_IN_CONTEXT`, overall request returns refusal with explanation.

**Step 5 — Evaluate**

* Example 08: score **per-intent** precision and CHR; drafts are graded on **schema compliance**, not truth.

---

## 5) Reference Implementation — Python (stdlib only)

Create `tools/intent_split.py`.

```python
# tools/intent_split.py -- rule-based multi-intent splitter + per-intent contracts
import re, json, os, time, urllib.request, uuid

GROUND_REFUSAL = "not in context"

def split_intents(q: str):
    text = q.strip()
    # crude separators
    parts = re.split(r"\bthen\b|;| and then | && | -> ", text, flags=re.IGNORECASE)
    intents = []
    for p in parts:
        role = "LOOKUP"
        if re.search(r"\bcompare|vs\b", p, re.IGNORECASE): role = "COMPARE"
        if re.search(r"\bdraft|email|write|generate|compose\b", p, re.IGNORECASE): role = "DRAFT"
        intents.append({"id": str(uuid.uuid4())[:8], "role": role, "text": p.strip()})
    # if single fragment but has both compare + draft keywords, split into two logical intents
    if len(intents)==1 and re.search(r"\bcompare|vs\b", text, re.IGNORECASE) and re.search(r"\bdraft|email|write|generate\b", text, re.IGNORECASE):
        intents = [
            {"id": str(uuid.uuid4())[:8], "role":"COMPARE", "text": text},
            {"id": str(uuid.uuid4())[:8], "role":"DRAFT",   "text": text}
        ]
    return intents

def retrieve(chunks, q, k=6):
    qs = set(w for w in re.split(r"\W+", q.lower()) if len(w)>=3)
    scored = []
    for c in chunks:
        toks = re.split(r"\W+", c["text"].lower())
        overlap = sum(1 for t in toks if t in qs)
        scored.append((overlap, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s,c in scored[:k]]

def build_compare_prompt(q, ctx, allowed):
    ctxs = "\n\n".join(f"[{c['id']}] {c['text']}" for c in ctx)
    return (
        "Task: Compare the two policies strictly from EVIDENCE.\n"
        "Output JSON ONLY: { claim: string, citations: [id,...] }\n"
        f"If not provable, reply exactly '{GROUND_REFUSAL}'.\n\n"
        f"Question: {q}\nEVIDENCE:\n{ctxs}\n"
    )

def build_draft_prompt(summary_json):
    return (
        "Task: Draft a short email referencing the grounded comparison.\n"
        "You MUST echo {handoff_id} exactly and MUST NOT add new policy facts.\n"
        "Output JSON ONLY: { email: string, handoff_id: string }\n\n"
        f"Grounded summary:\n{json.dumps(summary_json)}\n"
    )

def call_openai(prompt, model=os.getenv("OPENAI_MODEL","gpt-4o-mini")):
    key=os.getenv("OPENAI_API_KEY"); assert key, "OPENAI_API_KEY"
    body = json.dumps({"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0}).encode()
    req  = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body, headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    with urllib.request.urlopen(req) as r:
        j=json.loads(r.read().decode()); return j["choices"][0]["message"]["content"].strip()

def parse_json(text):
    s=text.find("{"); e=text.rfind("}")
    if s<0 or e<=s: return None
    try: return json.loads(text[s:e+1])
    except: return None

def run(q, chunks):
    turns=[]
    intents = split_intents(q)
    handoff=None
    for it in intents:
        if it["role"] in ("LOOKUP","COMPARE"):
            ctx = retrieve(chunks, it["text"], k=6)
            allowed = [c["id"] for c in ctx]
            out = parse_json(call_openai(build_compare_prompt(it["text"], ctx, allowed)))
            if not out or (isinstance(out, dict) and out.get("claim","").strip().lower()==GROUND_REFUSAL):
                return {"status":"REFUSAL", "reason":"grounding_failed"}
            # schema & scope checks
            if not set(out.get("citations",[])).issubset(set(allowed)):
                return {"status":"REJECT", "reason":"citation_out_of_scope"}
            handoff = {"handoff_id": str(uuid.uuid4())[:8], "summary": out}
            turns.append({"intent": it, "ctx_ids": allowed, "out": out, "handoff_id": handoff["handoff_id"]})
        elif it["role"]=="DRAFT":
            if not handoff: return {"status":"REJECT", "reason":"draft_without_grounding"}
            draft = parse_json(call_openai(build_draft_prompt({"handoff_id": handoff["handoff_id"], **handoff["summary"]})))
            if not draft or draft.get("handoff_id") != handoff["handoff_id"]:
                return {"status":"REJECT", "reason":"handoff_mismatch"}
            turns.append({"intent": it, "out": draft, "handoff_id": handoff["handoff_id"]})
    return {"status":"OK", "turns": turns}

if __name__=="__main__":
    chunks = json.load(open("data/chunks.json",encoding="utf8"))
    print(json.dumps(run("Compare Policy A vs B with citations, then draft an email asking IT to switch our domain.", chunks), indent=2))
```

**Pass criteria**

* For the sample query, the first turn is a **grounded** `COMPARE` with citations to `pA#1`/`pB#1`.
* The `DRAFT` turn echoes the **handoff\_id** and contains no new policy facts.
* If comparison is `not in context`, overall **REFUSAL** (no email is drafted).

---

## 6) Node Quick Variant (split only, no LLM call)

Create `tools/intent_split.mjs`.

```js
// tools/intent_split.mjs -- detect multi-intent; emit a small plan
export function splitIntents(q){
  const text = q.trim();
  const cuts = text.split(/(?:\bthen\b|;| and then | && | -> )/i).map(s=>s.trim()).filter(Boolean);
  const parts = cuts.length ? cuts : [text];
  return parts.map(p=>{
    let role = "LOOKUP";
    if (/\bcompare|vs\b/i.test(p)) role = "COMPARE";
    if (/\bdraft|email|write|generate|compose\b/i.test(p)) role = "DRAFT";
    return { role, text: p };
  });
}

// CLI
if (import.meta.url === `file://${process.argv[1]}`) {
  const q = process.argv.slice(2).join(" ");
  console.log(JSON.stringify(splitIntents(q), null, 2));
}
```

---

## 7) Acceptance Criteria (ship/no-ship)

A multi-intent response **may ship** only if:

1. Each **grounded** sub-intent has `citations ⊆ retrieved_ids` and passes Auditor `VALID`.
2. **Creative** sub-intents (draft/rewrite) echo a valid `handoff_id` from a `VALID` grounded step.
3. If any grounded sub-intent returns `not in context`, the overall request refuses (no partial answers).
4. Example 08 per-intent gates pass (CHR for grounded, compliance for drafts).

---

## 8) Prevention (contracts & defaults)

* **Query schema**: `role: {COMPARE|LOOKUP|DRAFT|REWRITE}`, `text`, optional `constraints`.
* **Router default**: split when ≥2 deterministic signals fire; otherwise single-intent.
* **Template isolation**: distinct prompts per role; never mix compare + draft in the same prompt.
* **UI hinting**: suggest quick toggles (“Compare” / “Draft”) for power users; cut ambiguity at the source.

---

## 9) Debug Workflow (10 minutes)

1. Run the splitter; print the plan.
2. Execute grounded step(s) first and log citations.
3. Ensure draft step references a real `handoff_id`.
4. If grounded fails → return refusal; do **not** proceed.
5. Re-score with Example 08; CHR should improve while over-refusal stays controlled.

---

## 10) Common Traps & Fixes

* **Draft first** temptation → ungrounded emails. Always ground **before** drafting.
* **One big retrieval** for all roles → tail noise. Retrieve **per role**.
* **Auditor on drafts** → meaningless. Audit only **grounded** claims; drafts check **schema** and **handoff**.
* **Partial shipping** (“we answered the easy half”) → inconsistent UX. Refuse on missing grounded parts.

---

## 11) Minimal Checklist (copy into PR)

* [ ] Split multi-intent queries deterministically into roles.
* [ ] Grounded steps use evidence-only template + citations.
* [ ] Drafts echo `handoff_id`; no new facts.
* [ ] Acceptance gate enforces per-role rules; no partial ship.
* [ ] Example 08 gates pass per intent.

---

## References to hands-on examples

* **Example 01** — Guarded baseline (evidence-only + refusal)
* **Example 02** — Reflection triage (`query_parse_error`)
* **Example 03** — Retrieval stabilization for each sub-intent
* **Example 04** — Acceptance gate (Scholar/Auditor + handoff)
* **Example 08** — Eval per intent (CHR for grounded, compliance for drafts)

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

