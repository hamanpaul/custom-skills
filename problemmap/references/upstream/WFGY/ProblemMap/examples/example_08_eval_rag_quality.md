# Example 08 — Evaluate RAG Quality (Precision, Refusal, Citations)

> **Evaluation disclaimer (example RAG quality)**  
> The scores in this example come from one concrete RAG setup and prompt design.  
> They are meant to show how to run an evaluation, not to claim that any model or stack is globally better.

---

**Goal**  
Measure RAG quality with **deterministic, SDK-free** metrics so you stop guessing. We score **answer precision**, **refusal behavior** (over/under-refusal), and **citation hit rate** from traces you already generate in Examples 01–03.

**Problem Map link**  
Improves observability for **No.1 Hallucination & Chunk Drift**, **No.2 Query Parsing**, **No.4 Tail Noise**, and **No.3 Index Schema Drift** (by catching quality drops after rebuilds).

**Outcome**  
- One command produces a **Markdown report** of key metrics  
- Metrics come from your **own traces** (`runs/trace.jsonl`) — no extra SDKs  
- Safe to wire into CI/CD as quality gates

---

## 1) Inputs

1) **Gold QA set** — tiny, reproducible file you can expand any time:

```json
// eval/qaset.json
[
  { "qid": "q1", "q": "What is X?", "answerable": true,  "gold_ids": ["p1#1"], "gold_claim": "X is a constrained mapping." },
  { "qid": "q2", "q": "Explain Y.", "answerable": true,  "gold_ids": ["p2#1"], "gold_claim": "Y is unrelated to X." },
  { "qid": "q3", "q": "What is Z?", "answerable": false, "gold_ids": [] },
  { "qid": "q4", "q": "Summarize the external link.", "answerable": false, "gold_ids": [] }
]
````

2. **Prediction traces** — produced by your guarded pipeline (Example 01 or 03).
   Each line in `runs/trace.jsonl` should look like:

```json
{"ts": 1699999999, "q": "What is X?", "chunks": [{"id":"p1#1"}], "answer":"- claim\n- citations: [p1#1]", "ok": true}
```

> If your system logs a different shape, the scorer below handles both `citations: [id,...]` embedded in text **and** a JSON field `citations` if you already emit one.

---

## 2) Metrics (deterministic definitions)

* **Answered?** `answered = !refusal`, where `refusal` means answer text equals (case-insensitive) `not in context`.
* **Citation Hit (per Q)** `hit = overlaps(predicted_citations, gold_ids)`
* **Answer Precision (over answered)** `precision = correct / answered`, where:

  * For `answerable=true`: **correct** if `hit==true` and not refusal
  * For `answerable=false`: any answered output counts as **incorrect** (hallucination)
* **Over-Refusal Rate**: fraction of `answerable=true` questions that were refused
* **Under-Refusal (Hallucination) Rate**: fraction of `answerable=false` questions that were answered
* **Citation Hit Rate (CHR)** (answerable only): mean of `hit`
* **Schema/Template Compliance**: % of predictions that either include a `citations` list or return refusal token

> Optional: If you maintain `gold_claim`, we also compute **Claim Containment** (any ≥5-char phrase from gold appears in answer). It’s a weak but useful extra signal.

---

## 3) Path A — Python scorer (stdlib only)

Create `eval/score.md.py` (yes, a `.py` file that writes **Markdown** to stdout).

```python
# eval/score.md.py -- score precision/refusal/citation from traces; emits Markdown
import json, re, sys
from typing import Dict, List

REFUSAL_TOKEN = "not in context"
CIT_RE = re.compile(r"citations\s*:\s*\[([^\]]*)\]", re.IGNORECASE)

def parse_citations(answer: str, parsed_field=None):
    if isinstance(parsed_field, list):  # if you already stored as JSON list
        return [str(x).strip() for x in parsed_field]
    m = CIT_RE.search(answer or "")
    if not m: return []
    raw = m.group(1).strip()
    if not raw: return []
    return [t.strip() for t in re.split(r"[,\s]+", raw) if t.strip()]

def is_refusal(answer: str) -> bool:
    return (answer or "").strip().lower() == REFUSAL_TOKEN

def load_jsonl(path):
    with open(path, encoding="utf8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            yield json.loads(line)

def phrase_containment(gold_claim: str, answer: str) -> bool:
    if not gold_claim: return False
    gold = gold_claim.lower()
    ans = (answer or "").lower()
    # find ≥5 char alnum phrases from gold and check if any appears in ans
    for m in re.finditer(r"[a-z0-9][a-z0-9\-\s]{4,}", gold):
        p = m.group(0).strip()
        if len(p) >= 5 and p in ans:
            return True
    return False

def main(qaset_path, traces_path):
    gold = {x["q"]: x for x in json.load(open(qaset_path, encoding="utf8"))}
    preds = list(load_jsonl(traces_path))

    # map predictions to gold by exact string match on q (simple and robust)
    rows = []
    for p in preds:
        q = p.get("q") or p.get("question") or ""
        if q not in gold: 
            # skip unknown questions; you can optionally warn
            continue
        g = gold[q]
        ans = p.get("answer","")
        cits = parse_citations(ans, p.get("citations"))
        refusal = is_refusal(ans)
        hit = bool(set(cits) & set(g.get("gold_ids", [])))
        contain = phrase_containment(g.get("gold_claim",""), ans)
        rows.append({
            "qid": g["qid"], "q": q, "answerable": g["answerable"],
            "refusal": refusal, "hit": hit, "contain": contain,
            "answered": not refusal
        })

    # aggregate
    total = len([r for r in rows if r["qid"]])
    pos = [r for r in rows if r["answerable"]]
    neg = [r for r in rows if not r["answerable"]]
    answered = [r for r in rows if r["answered"]]
    answered_pos = [r for r in answered if r["answerable"]]

    # precision over answered
    correct_over_answered = sum(1 for r in answered if (r["answerable"] and r["hit"]))
    precision = (correct_over_answered / max(len(answered),1)) if answered else 0.0

    over_refusal = sum(1 for r in pos if r["refusal"]) / max(len(pos),1) if pos else 0.0
    under_refusal = sum(1 for r in neg if not r["refusal"]) / max(len(neg),1) if neg else 0.0
    chr_rate = sum(1 for r in pos if (not r["refusal"] and r["hit"])) / max(len(pos),1) if pos else 0.0
    contain_rate = sum(1 for r in pos if (not r["refusal"] and r["contain"])) / max(len(pos),1) if pos else 0.0

    # emit Markdown
    def pct(x): return f"{100*x:.1f}%"
    print("# RAG Quality Report\n")
    print(f"- Questions scored: **{total}**")
    print(f"- Answer precision (over answered): **{pct(precision)}**")
    print(f"- Over-refusal (answerable but refused): **{pct(over_refusal)}**")
    print(f"- Under-refusal / Hallucination (unanswerable but answered): **{pct(under_refusal)}**")
    print(f"- Citation hit rate (answerable): **{pct(chr_rate)}**")
    print(f"- Claim containment (answerable): **{pct(contain_rate)}**")
    print("\n## Per-question\n")
    print("| qid | answered | hit | refusal | label |")
    print("|-----|----------|-----|---------|-------|")
    for r in rows:
        label = ("OK" if (r["answerable"] and not r["refusal"] and r["hit"]) else
                 ("REFUSAL_OK" if (not r["answerable"] and r["refusal"]) else
                  ("OVER_REFUSAL" if (r["answerable"] and r["refusal"]) else
                   ("HALLUCINATION" if (not r["answerable"] and not r["refusal"]) else
                    "ANS_NO_HIT"))))
        print(f"| {r['qid']} | {str(r['answered']).lower()} | {str(r['hit']).lower()} | {str(r['refusal']).lower()} | **{label}** |")
```

Run (and generate a Markdown report):

```bash
python eval/score.md.py eval/qaset.json runs/trace.jsonl > eval/report.md
```

**Pass criteria**

* `report.md` renders with overall metrics and a per-question table
* For a pipeline resembling Examples 01–03, you should see:

  * Low **under-refusal** (few hallucinations on unanswerable)
  * Moderate **over-refusal** initially (can be tuned via retrieval)
  * **Citation hit rate** improving after Example 03 intersection+rerank

---

## 4) Path B — Node scorer (stdlib only, writes Markdown)

Create `eval/score.md.mjs`.

```js
// eval/score.md.mjs -- score precision/refusal/citation from traces; emits Markdown
import fs from "node:fs";

const REFUSAL = "not in context";
function parseJSONL(path){
  return fs.readFileSync(path,"utf8").split(/\r?\n/).filter(Boolean).map(JSON.parse);
}
function parseCitations(answer, parsedField){
  if (Array.isArray(parsedField)) return parsedField.map(x=>String(x).trim());
  const m = (answer||"").match(/citations\s*:\s*\[([^\]]*)\]/i);
  if(!m) return [];
  return m[1].split(/[, \t\r\n]+/).map(s=>s.trim()).filter(Boolean);
}
function isRefusal(answer){ return (answer||"").trim().toLowerCase() === REFUSAL; }
function phraseContain(gold, ans){
  if(!gold) return false;
  const g = gold.toLowerCase(), a = (ans||"").toLowerCase();
  const matches = g.match(/[a-z0-9][a-z0-9-\s]{4,}/g) || [];
  return matches.some(p => p.trim().length>=5 && a.includes(p.trim()));
}

const [qasetPath, tracePath] = process.argv.slice(2);
if(!qasetPath || !tracePath){
  console.error("usage: node eval/score.md.mjs eval/qaset.json runs/trace.jsonl > eval/report.md");
  process.exit(1);
}
const goldArr = JSON.parse(fs.readFileSync(qasetPath,"utf8"));
const gold = Object.fromEntries(goldArr.map(x => [x.q, x]));
const preds = parseJSONL(tracePath);

const rows = [];
for(const p of preds){
  const q = p.q || p.question || "";
  if(!gold[q]) continue;
  const g = gold[q];
  const ans = p.answer || "";
  const cits = parseCitations(ans, p.citations);
  const refusal = isRefusal(ans);
  const hit = cits.some(id => g.gold_ids.includes(id));
  const contain = phraseContain(g.gold_claim || "", ans);
  rows.push({ qid: g.qid, q, answerable: g.answerable, refusal, hit, contain, answered: !refusal });
}

// aggregates
const total = rows.length;
const pos = rows.filter(r => r.answerable);
const neg = rows.filter(r => !r.answerable);
const answered = rows.filter(r => r.answered);
const correctOverAnswered = answered.filter(r => r.answerable && r.hit).length;

function pct(x){ return `${(100*x).toFixed(1)}%`; }
const precision = answered.length ? correctOverAnswered / answered.length : 0;
const overRefusal = pos.length ? pos.filter(r => r.refusal).length / pos.length : 0;
const underRefusal = neg.length ? neg.filter(r => !r.refusal).length / neg.length : 0;
const chr = pos.length ? pos.filter(r => !r.refusal && r.hit).length / pos.length : 0;
const containRate = pos.length ? pos.filter(r => !r.refusal && r.contain).length / pos.length : 0;

// emit Markdown
let out = "";
out += `# RAG Quality Report\n\n`;
out += `- Questions scored: **${total}**\n`;
out += `- Answer precision (over answered): **${pct(precision)}**\n`;
out += `- Over-refusal (answerable but refused): **${pct(overRefusal)}**\n`;
out += `- Under-refusal / Hallucination (unanswerable but answered): **${pct(underRefusal)}**\n`;
out += `- Citation hit rate (answerable): **${pct(chr)}**\n`;
out += `- Claim containment (answerable): **${pct(containRate)}**\n\n`;
out += `## Per-question\n\n| qid | answered | hit | refusal | label |\n|-----|----------|-----|---------|-------|\n`;
for(const r of rows){
  const label = (r.answerable && !r.refusal && r.hit) ? "OK"
               : (!r.answerable && r.refusal) ? "REFUSAL_OK"
               : (r.answerable && r.refusal) ? "OVER_REFUSAL"
               : (!r.answerable && !r.refusal) ? "HALLUCINATION"
               : "ANS_NO_HIT";
  out += `| ${r.qid} | ${String(r.answered).toLowerCase()} | ${String(r.hit).toLowerCase()} | ${String(r.refusal).toLowerCase()} | **${label}** |\n`;
}
process.stdout.write(out);
```

Run:

```bash
node eval/score.md.mjs eval/qaset.json runs/trace.jsonl > eval/report.md
```

---

## 5) Quality gates (copy into CI)

Pick conservative defaults first; tighten over time.

| Gate                         | What it catches                        | Suggested threshold |
| ---------------------------- | -------------------------------------- | ------------------- |
| **G1: Precision (answered)** | wrong answers shipped                  | ≥ 0.80              |
| **G2: Under-refusal**        | hallucinations on negatives            | ≤ 0.05              |
| **G3: Over-refusal**         | too many “not in context” on positives | ≤ 0.25              |
| **G4: Citation Hit Rate**    | off-topic context selection            | ≥ 0.75              |
| **G5: Compliance**           | template drift                         | ≥ 0.98              |

If any gate fails → block deploy and run Example 02/03 to find where drift started.

---

## 6) Typical outcomes & how to improve

* **Low CHR, decent precision** → retrieval is noisy; fix with **intersection + rerank** (Example 03) and smaller chunks.
* **High under-refusal** → your negatives aren’t truly negative, or your intersection is too strict; widen candidate pools before knee-cut.
* **High over-refusal** → evidence exists but template or candidate set is too narrow; increase top-k pre-rerank; ensure ids survive to prompt.
* **Precision fine, CHR low** → model infers from context but cites wrong ids; enforce strict citation schema or shrink chunks to bind entity+constraint.

---

## 7) Extending the QA set (best practices)

* Keep **10–30** mixed questions (answerable/unanswerable) per corpus.
* For answerable items, include **gold\_ids**; optionally add **gold\_claim** to monitor containment.
* When your corpus changes, **clone** the QA set and adjust only the questions affected; never silently mutate old qids.

---

## 8) Wire into your repo

1. Commit `eval/qaset.json`, `eval/score.md.py` (or `.mjs`).
2. Ensure your pipeline writes `runs/trace.jsonl`.
3. Add a CI step:

   ```bash
   python eval/score.md.py eval/qaset.json runs/trace.jsonl > eval/report.md
   grep -E "precision .* [89]\d\.\d%|precision .* 100\.0%" eval/report.md || true # example pattern
   ```
4. Upload `eval/report.md` as a job artifact; link it from your PR template.

---

## 9) Why this works (one paragraph)

We avoid subjective model-judged grading by relying on **observable facts**: refusal tokens, citation overlap, and optional phrase containment. These are deterministic, cheap, and correlate strongly with user-perceived quality. By gating deploys on these signals, you ship fewer hallucinations and catch regressions caused by retrieval tweaks or index rebuilds—without introducing new SDK dependencies.

---

## 10) Next steps

* Track the same metrics in prod (see `ops/live_monitoring_rag.md`)—log a 1% sample to protect privacy.
* If you later add a CPU reranker, re-run this example to quantify the gain vs. the cosine rerank baseline.
* Pair with Example 07’s readiness probe: **don’t** flip ready until the sentinel passes and eval on a smoke set is green.

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

