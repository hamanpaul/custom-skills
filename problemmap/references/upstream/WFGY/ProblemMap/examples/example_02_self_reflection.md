# Example 02 — Self-Reflection Trace and Triage (No.1 Hallucination & No.2 Query Parsing)

> **Evaluation disclaimer (self reflection)**  
> This example shows how a model can reflect on its own answers under a specific prompt and setup.  
> The reflections and scores are illustrative and do not prove that the model is generally self aware or reliable.

---

**Goal**  
Turn raw traces into a **decision report** that tells you where the failure started: retrieval or generation.  
No SDKs, no extra dependencies. Works with the trace produced in Example 01.

**Problem Map link**  
Targets **No.1 Hallucination & Chunk Drift** and **No.2 Query Parsing / Intent Split**.  
Second-order benefits for No.4 (Tail Noise) once you cut low-value evidence.

**Outcome**  
- A per-question **triage label**: `retrieval_drift`, `generation_drift`, or `ok`  
- A short **why** field pointing to the exact symptom  
- A machine-readable JSONL report you can diff over time

---

## 1) Inputs

- `runs/trace.jsonl` from Example 01 (each line: `{"q": "...", "chunks":[{"id":"..."},...], "answer":"...", "ok": true/false }`)
- `data/chunks.json` (chunk id → text)

> If you skipped Example 01, create the same two files now. Keep chunk ids stable.

---

## 2) Reflection rubric (simple and reproducible)

We use deterministic checks, not another LLM, to avoid circular reasoning.

**Signals**
- **Template compliance**: either contains `not in context` or a `citations:` line  
- **Citation overlap**: ids mentioned in the answer must be a subset of retrieved ids  
- **Evidence containment**: ≥ 1 non-trivial phrase (≥ 5 chars, letters/digits) from the answer appears verbatim in evidence  
- **Question-evidence alignment**: ≥ 1 query token appears in evidence; if not, likely retrieval drift

**Labels**
- `generation_drift`: template violated **or** citation overlap = 0 **or** evidence containment = 0 while evidence contains relevant terms  
- `retrieval_drift`: evidence lacks query terms (poor alignment), even if the answer looks “reasonable”  
- `ok`: citations present **and** evidence containment > 0 **and** some query terms found in evidence  
- `refusal_ok`: answer is exactly `not in context` and evidence truly lacks query terms  
- `refusal_suspect`: `not in context` but evidence actually contains query terms (over-refusal)

---

## 3) Path A — Python reflection (single file)

Create `reflect.py`.

```python
# reflect.py -- classify traces as retrieval_drift / generation_drift / ok
import json, re, sys
from typing import Dict, List

PHRASE_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9\-\s]{4,}")  # >=5 chars

def load_chunks(path: str) -> Dict[str, str]:
    items = json.load(open(path, encoding="utf8"))
    return {c["id"]: c["text"] for c in items}

def extract_citation_ids(ans: str) -> List[str]:
    # naive parser for: citations: [p1#1, p2#3]
    m = re.search(r"citations\s*:\s*\[([^\]]*)\]", ans, re.IGNORECASE)
    if not m: return []
    raw = m.group(1)
    return [t.strip() for t in re.split(r"[,\s]+", raw) if t.strip()]

def phrases(s: str) -> List[str]:
    return [p.strip() for p in PHRASE_RE.findall(s)]

def any_phrase_in_evidence(ans: str, ev: str) -> bool:
    ev_low = ev.lower()
    for p in phrases(ans):
        if len(p) >= 5 and p.lower() in ev_low:
            return True
    return False

def any_query_token_in_evidence(q: str, ev: str) -> bool:
    qtok = {w for w in re.split(r"\W+", q.lower()) if len(w) >= 3}
    if not qtok: return False
    evtok = set(re.split(r"\W+", ev.lower()))
    return len(qtok & evtok) > 0

def reflect_one(rec: Dict, chunk_map: Dict[str, str]) -> Dict:
    q, ans = rec["q"], rec.get("answer","")
    ids = [c["id"] for c in rec.get("chunks", []) if "id" in c]
    ev = "\n\n".join(chunk_map.get(i, "") for i in ids)

    tmpl_ok = ("not in context" in ans.lower()) or ("citations:" in ans.lower())
    cit_ids = extract_citation_ids(ans)
    cit_overlap = all(cid in ids for cid in cit_ids) if cit_ids else False
    ev_contains_answer = any_phrase_in_evidence(ans, ev)
    q_align = any_query_token_in_evidence(q, ev)

    if "not in context" in ans.lower():
        if q_align:
            label, why = "refusal_suspect", "evidence contains query terms but model refused"
        else:
            label, why = "refusal_ok", "no query terms found in evidence; refusal acceptable"
    else:
        if not tmpl_ok or (cit_ids and not cit_overlap):
            label, why = "generation_drift", "template/citations violated"
        elif not ev_contains_answer and q_align:
            label, why = "generation_drift", "answer text not grounded in evidence"
        elif not q_align:
            label, why = "retrieval_drift", "evidence lacks query terms"
        else:
            label, why = "ok", "citations present and answer grounded"

    return {
        "q": q, "label": label, "why": why,
        "chunks": ids, "citations_in_answer": cit_ids
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python reflect.py runs/trace.jsonl data/chunks.json")
        sys.exit(1)
    trace_path, chunk_path = sys.argv[1], sys.argv[2]
    chunks = load_chunks(chunk_path)
    out = []
    with open(trace_path, encoding="utf8") as f:
        for line in f:
            if not line.strip(): continue
            rec = json.loads(line)
            out.append(reflect_one(rec, chunks))
    for r in out:
        print(json.dumps(r, ensure_ascii=False))
````

Run:

```bash
python reflect.py runs/trace.jsonl data/chunks.json > runs/report.jsonl
```

**Pass criteria**

* For “What is X?” you should see `label: ok`
* For “What is Z?” you should see `label: refusal_ok`
* If you deliberately break the template or citations, you should get `generation_drift`
* If you swap chunks to unrelated text, you should get `retrieval_drift`

---

## 4) Path B — Node reflection (single file, no deps)

Create `reflect.mjs`.

```js
// reflect.mjs -- classify traces as retrieval_drift / generation_drift / ok
import fs from "node:fs";

function loadChunks(path) {
  const arr = JSON.parse(fs.readFileSync(path, "utf8"));
  const m = {};
  for (const c of arr) m[c.id] = c.text;
  return m;
}

function extractCitationIds(ans) {
  const m = ans.match(/citations\s*:\s*\[([^\]]*)\]/i);
  if (!m) return [];
  return m[1].split(/[, \t\r\n]+/).map(s => s.trim()).filter(Boolean);
}

function phrases(s) {
  return (s.match(/[A-Za-z0-9][A-Za-z0-9-\s]{4,}/g) || []).map(x => x.trim());
}

function anyPhraseInEvidence(ans, ev) {
  const evLow = ev.toLowerCase();
  return phrases(ans).some(p => p.length >= 5 && evLow.includes(p.toLowerCase()));
}

function anyQueryTokenInEvidence(q, ev) {
  const qtok = new Set(q.toLowerCase().split(/\W+/).filter(w => w.length >= 3));
  if (!qtok.size) return false;
  const evtok = new Set(ev.toLowerCase().split(/\W+/));
  for (const w of qtok) if (evtok.has(w)) return true;
  return false;
}

function reflectOne(rec, chunkMap) {
  const q = rec.q, ans = rec.answer || "";
  const ids = (rec.chunks || []).map(c => c.id).filter(Boolean);
  const ev = ids.map(i => chunkMap[i] || "").join("\n\n");

  const tmplOk = ans.toLowerCase().includes("not in context") || /citations\s*:/i.test(ans);
  const citIds = extractCitationIds(ans);
  const citOverlap = citIds.length ? citIds.every(id => ids.includes(id)) : false;
  const evContainsAnswer = anyPhraseInEvidence(ans, ev);
  const qAlign = anyQueryTokenInEvidence(q, ev);

  let label, why;
  if (ans.toLowerCase().includes("not in context")) {
    if (qAlign) { label = "refusal_suspect"; why = "evidence contains query terms but model refused"; }
    else        { label = "refusal_ok";      why = "no query terms found in evidence; refusal acceptable"; }
  } else {
    if (!tmplOk || (citIds.length && !citOverlap)) {
      label = "generation_drift"; why = "template/citations violated";
    } else if (!evContainsAnswer && qAlign) {
      label = "generation_drift"; why = "answer text not grounded in evidence";
    } else if (!qAlign) {
      label = "retrieval_drift";  why = "evidence lacks query terms";
    } else {
      label = "ok";               why = "citations present and answer grounded";
    }
  }
  return { q, label, why, chunks: ids, citations_in_answer: citIds };
}

if (process.argv.length < 4) {
  console.error("usage: node reflect.mjs runs/trace.jsonl data/chunks.json");
  process.exit(1);
}
const [tracePath, chunkPath] = process.argv.slice(2);
const chunkMap = loadChunks(chunkPath);

const lines = fs.readFileSync(tracePath, "utf8").split(/\r?\n/).filter(Boolean);
for (const line of lines) {
  const rec = JSON.parse(line);
  console.log(JSON.stringify(reflectOne(rec, chunkMap)));
}
```

Run:

```bash
node reflect.mjs runs/trace.jsonl data/chunks.json > runs/report.jsonl
```

Pass criteria are the same as Python.

---

## 5) Read the report as a triage table

Turn `runs/report.jsonl` into a quick view:

```bash
echo -e "| q | label | why |\n|---|---|---|" > runs/report.md
cat runs/report.jsonl | python - <<'PY'
import sys, json
for line in sys.stdin:
    r = json.loads(line)
    q = (r["q"][:60] + "…") if len(r["q"])>60 else r["q"]
    print(f"| {q} | **{r['label']}** | {r['why']} |")
PY >> runs/report.md
```

You’ll get a Markdown table you can paste into an issue or PR.

---

## 6) What to do for each label

* `retrieval_drift`
  Move to **Example 03 (Intersection + Rerank)**; reduce chunk size so entity + constraints live together; drop tail after the score knee.

* `generation_drift`
  Keep the evidence-only template at the end of the system prompt; set temperature to 0 for evaluation; if needed, require exact `citations: [id,...]`.

* `refusal_ok`
  This is good. It means the model did not fabricate beyond evidence.

* `refusal_suspect`
  Increase top-k before rerank. If query is truly absent from your corpus, consider a fallback answer or a different data source.

* `ok`
  Baseline reached. Move to Eval examples to measure precision/recall and stability.

---

## 7) Optional: LLM-assisted reflection (still deterministic output)

If you prefer a short natural-language summary per case, you can add a second pass that prompts an LLM to **summarize** the deterministic checks into 1–2 sentences.
Keep the JSON decision from the scripts above as source-of-truth, and store the LLM summary as an auxiliary field.

---

## 8) Common mistakes

* Mixing traces from different chunking pipelines → chunk ids do not resolve. Keep a single chunker per index build.
* Relying only on citation strings → models can fabricate ids. Always check overlap with retrieved ids.
* Treating refusal as a failure → under constrained evidence, refusal is the correct output.

---

## 9) Next steps

* Run **Example 03** to harden retrieval
* Use **Eval** docs to compare before/after on precision, refusal, and citation overlap
* Wire this reflection into CI: fail a build if `generation_drift` exceeds your threshold

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

