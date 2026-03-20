# Example 04 — Multi-Agent Coordination Boundary (No.6 Logic Collapse)

**Goal**  
Prevent agents from polluting each other’s context. A “Scholar” drafts an answer from evidence; an “Auditor” validates it against the same evidence using a strict **handoff contract**. If validation fails, we do not ship text—we ask for more evidence or retry retrieval. No SDKs, single-file runs.

**Problem Map link**  
Targets **No.6 Logic Collapse & Recovery** (state consistency during hand-offs). Secondary reductions in **No.1** (hallucination) and **No.2** (intent split) because each agent operates inside a hard boundary.

**Outcome**  
- Clean hand-off JSON with explicit **scope**, **evidence ids**, **claims**, and **verdict**  
- Deterministic accept/reject logic; no “looks right” guesses  
- Machine-readable agent traces for audits and regressions

---

## 1) Inputs

Use the same tiny corpus as earlier examples:

```json
// data/chunks.json
[
  {"id":"p1#1","page":1,"text":"X is a constrained mapping."},
  {"id":"p2#1","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
````

Two test questions:

* **Q1**: “What is X?” → should pass with citation `[p1#1]`
* **Q2**: “Explain Z.” → should refuse as `not in context`

---

## 2) Handoff Contract (JSON)

This is the **only** way agents talk. Anything outside the contract is ignored.

```json
// contract.schema (conceptual)
{
  "handoff_id": "string",             // unique
  "question": "string",
  "scope": { "allowed_ids": ["..."] },// strict evidence boundary
  "scholar": {
    "claim": "string",                 // one-sentence claim
    "citations": ["..."],              // ids subset of allowed_ids
    "notes": "string"                  // optional, not binding
  },
  "auditor": {
    "verdict": "VALID | INVALID | NOT_IN_CONTEXT",
    "reason": "string",
    "citations": ["..."],              // subset of allowed_ids
    "corrected_claim": "string|null"   // for INVALID when fix is trivial
  }
}
```

**Rules**

1. `citations ⊆ scope.allowed_ids` for both agents
2. If `verdict != VALID`, the pipeline must **not** emit an answer
3. If `verdict = NOT_IN_CONTEXT`, retrieval retries are allowed; otherwise surface a refusal
4. Trace every hand-off as JSONL

---

## 3) Path A — Python (single file, no extra deps)

Create `agents.py`.

```python
# agents.py -- two-agent boundary with strict JSON handoff
import json, os, time, uuid, urllib.request, sys

CHUNKS = json.load(open("data/chunks.json", encoding="utf8"))

def retrieve(question, k=2):
    qs = set(question.lower().split())
    scored = []
    for c in CHUNKS:
        score = sum(1 for w in c["text"].lower().split() if w in qs)
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    picks = [c for _, c in scored[:k]]
    return picks

def build_scholar_prompt(q, chunks):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    return (
        "Role: Scholar.\n"
        "Use only the evidence. If not provable, reply exactly: not in context.\n"
        "Return JSON with fields: claim, citations (array of ids). No extra keys.\n\n"
        f"Question: {q}\n\nEvidence:\n{ctx}\n"
    )

def build_auditor_prompt(q, chunks, scholar_json):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    return (
        "Role: Auditor.\n"
        "Validate the Scholar strictly against the same evidence.\n"
        "Return JSON with fields: verdict (VALID|INVALID|NOT_IN_CONTEXT), reason, citations (array), corrected_claim (or null).\n"
        "Rules:\n"
        "- If the claim is outside evidence, verdict=INVALID.\n"
        "- If the question cannot be answered from evidence, verdict=NOT_IN_CONTEXT.\n"
        "- citations must only reference provided evidence ids.\n\n"
        f"Question: {q}\nEvidence:\n{ctx}\n\nScholar:\n{scholar_json}\n"
    )

def call_openai(prompt, model=os.getenv("OPENAI_MODEL","gpt-4o-mini")):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key: raise RuntimeError("Set OPENAI_API_KEY")
    body = json.dumps({
        "model": model,
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req) as r:
        j = json.loads(r.read().decode("utf-8"))
        return j["choices"][0]["message"]["content"].strip()

def parse_json_block(txt):
    # best-effort extract first JSON object in the text
    start = txt.find("{")
    end = txt.rfind("}")
    if start == -1 or end == -1 or end <= start: return {}
    try:
        return json.loads(txt[start:end+1])
    except Exception:
        return {}

def enforce(handoff):
    allowed = set(handoff["scope"]["allowed_ids"])
    def subset(cites): return set(cites).issubset(allowed)

    s = handoff["scholar"]
    a = handoff["auditor"]

    # basic checks
    if not subset(s.get("citations", [])):
        return "REJECT", "scholar cites outside scope"
    if not subset(a.get("citations", [])):
        return "REJECT", "auditor cites outside scope"

    verdict = a.get("verdict", "INVALID")
    if verdict == "VALID":
        return "ACCEPT", "auditor validated"
    if verdict == "NOT_IN_CONTEXT":
        return "RETRY", "needs more/different evidence"
    return "REJECT", "auditor invalidated claim"

def run(question):
    handoff_id = str(uuid.uuid4())
    chunks = retrieve(question, k=2)
    scope_ids = [c["id"] for c in chunks]

    scholar_prompt = build_scholar_prompt(question, chunks)
    scholar_raw = call_openai(scholar_prompt)
    scholar = parse_json_block(scholar_raw) or {"claim":"not in context","citations":[]}

    auditor_prompt = build_auditor_prompt(question, chunks, json.dumps(scholar))
    auditor_raw = call_openai(auditor_prompt)
    auditor = parse_json_block(auditor_raw) or {"verdict":"NOT_IN_CONTEXT","reason":"parse failed","citations":[],"corrected_claim":None}

    handoff = {
        "handoff_id": handoff_id,
        "question": question,
        "scope": {"allowed_ids": scope_ids},
        "scholar": scholar,
        "auditor": auditor
    }

    decision, reason = enforce(handoff)

    os.makedirs("runs", exist_ok=True)
    with open("runs/agent_trace.jsonl","a",encoding="utf8") as f:
        f.write(json.dumps({
            "ts": int(time.time()),
            "handoff": handoff,
            "decision": decision,
            "reason": reason
        }, ensure_ascii=False) + "\n")

    return decision, reason, handoff

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: OPENAI_API_KEY=sk-xxx python agents.py \"your question\"")
        sys.exit(1)
    print(run(sys.argv[1]))
```

Run:

```bash
OPENAI_API_KEY=sk-xxx python agents.py "What is X?"
OPENAI_API_KEY=sk-xxx python agents.py "Explain Z."
```

**Pass criteria**

* Q1 prints `('ACCEPT', 'auditor validated', …)` and both agents cite only `[p1#1]`
* Q2 prints `('RETRY' or 'REJECT', …)` with `NOT_IN_CONTEXT` verdict; no free-text answer emitted
* Two lines appended to `runs/agent_trace.jsonl`

---

## 4) Path B — Node (single file, no deps)

Create `agents.mjs`.

```js
// agents.mjs -- two-agent boundary in Node, strict JSON handoff
import fs from "node:fs";
import https from "node:https";
import crypto from "node:crypto";

const CHUNKS = JSON.parse(fs.readFileSync("data/chunks.json","utf8"));

function retrieve(q, k=2){
  const qs = new Set(q.toLowerCase().split(/\s+/));
  return [...CHUNKS]
    .map(c => [c.text.toLowerCase().split(/\s+/).filter(w=>qs.has(w)).length, c])
    .sort((a,b)=>b[0]-a[0]).slice(0,k).map(([_,c])=>c);
}
function buildScholarPrompt(q, chunks){
  const ctx = chunks.map(c => `[${c.id}] ${c.text}`).join("\n\n");
  return `Role: Scholar.
Use only the evidence. If not provable, reply exactly: not in context.
Return JSON with fields: claim, citations (array of ids). No extra keys.

Question: ${q}

Evidence:
${ctx}
`;
}
function buildAuditorPrompt(q, chunks, scholarJson){
  const ctx = chunks.map(c => `[${c.id}] ${c.text}`).join("\n\n");
  return `Role: Auditor.
Validate the Scholar strictly against the same evidence.
Return JSON with fields: verdict (VALID|INVALID|NOT_IN_CONTEXT), reason, citations (array), corrected_claim (or null).
Rules:
- If the claim is outside evidence, verdict=INVALID.
- If the question cannot be answered from evidence, verdict=NOT_IN_CONTEXT.
- citations must only reference provided evidence ids.

Question: ${q}
Evidence:
${ctx}

Scholar:
${scholarJson}
`;
}
async function callOpenAI(prompt, model=process.env.OPENAI_MODEL || "gpt-4o-mini"){
  const apiKey = process.env.OPENAI_API_KEY;
  if(!apiKey) throw new Error("Set OPENAI_API_KEY");
  const body = JSON.stringify({ model, messages:[{role:"user",content:prompt}], temperature:0 });
  const resp = await new Promise((resolve,reject)=>{
    const req = https.request("https://api.openai.com/v1/chat/completions",{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "Authorization":`Bearer ${apiKey}`,
        "Content-Length":Buffer.byteLength(body)
      }
    }, r=>{
      let data=""; r.on("data",d=>data+=d); r.on("end",()=>resolve(JSON.parse(data)));
    });
    req.on("error",reject); req.write(body); req.end();
  });
  return resp.choices[0].message.content.trim();
}
function parseJsonBlock(txt){
  const s = txt.indexOf("{"), e = txt.lastIndexOf("}");
  if(s<0 || e<=s) return {};
  try { return JSON.parse(txt.slice(s,e+1)); } catch { return {}; }
}
function enforce(handoff){
  const allowed = new Set(handoff.scope.allowed_ids);
  const subset = cites => cites.every(x => allowed.has(x));
  const s = handoff.scholar, a = handoff.auditor;

  if(!subset(s.citations || [])) return ["REJECT","scholar cites outside scope"];
  if(!subset(a.citations || [])) return ["REJECT","auditor cites outside scope"];
  if(a.verdict === "VALID") return ["ACCEPT","auditor validated"];
  if(a.verdict === "NOT_IN_CONTEXT") return ["RETRY","needs more/different evidence"];
  return ["REJECT","auditor invalidated claim"];
}
async function run(q){
  const chunks = retrieve(q,2);
  const scopeIds = chunks.map(c=>c.id);
  const scholarRaw = await callOpenAI(buildScholarPrompt(q, chunks));
  const scholar = parseJsonBlock(scholarRaw) || {claim:"not in context", citations:[]};
  const auditorRaw = await callOpenAI(buildAuditorPrompt(q, chunks, JSON.stringify(scholar)));
  const auditor = parseJsonBlock(auditorRaw) || {verdict:"NOT_IN_CONTEXT", reason:"parse failed", citations:[], corrected_claim:null};
  const handoff = {
    handoff_id: crypto.randomUUID(),
    question: q,
    scope: { allowed_ids: scopeIds },
    scholar, auditor
  };
  const [decision, reason] = enforce(handoff);
  fs.mkdirSync("runs",{recursive:true});
  fs.appendFileSync("runs/agent_trace.jsonl", JSON.stringify({ ts: Date.now(), handoff, decision, reason })+"\n");
  return { decision, reason, handoff };
}
if (import.meta.url === `file://${process.argv[1]}`) {
  const q = process.argv.slice(2).join(" ");
  if(!q){ console.error("usage: OPENAI_API_KEY=sk-xxx node agents.mjs \"your question\""); process.exit(1); }
  console.log(await run(q));
}
```

Run:

```bash
OPENAI_API_KEY=sk-xxx node agents.mjs "What is X?"
OPENAI_API_KEY=sk-xxx node agents.mjs "Explain Z."
```

**Pass criteria** are identical to Python.

---

## 5) Acceptance logic (deterministic)

A request only emits a final answer if:

1. `auditor.verdict == VALID`
2. `scholar.citations ⊆ scope.allowed_ids` **and** `auditor.citations ⊆ scope.allowed_ids`
3. (Optional) The answer passes your template compliance checks from Example 02

If any check fails, you **do not** print text. You retry retrieval or respond with `not in context`.

---

## 6) Failure shapes & quick fixes

* **Boundary leak**: citations include an id not in `scope.allowed_ids` → fix retrieval scope or chunk ids
* **Over-refusal**: `NOT_IN_CONTEXT` but query tokens exist in evidence → increase top-k pre-rerank (see Example 03)
* **Agreeing wrong**: both agents agree on an incorrect statement → your evidence is wrong; fix chunking or data quality
* **Parsing noise**: models add prose around JSON → `parse_json_block` already strips; keep temperature at 0

---

## 7) Production tips

* Log `handoff` objects to a dedicated topic or file for audits
* Add a **cooldown**: if 2 consecutive `NOT_IN_CONTEXT` happen for the same user intent, escalate to fallback UX instead of re-query loops
* Surface `reason` to operators; it is much faster than re-reading raw answers

---

## 8) Where to go next

* Combine with **Example 03** (intersection + rerank) for better evidence
* Add a third agent **Policy** that blocks answers containing restricted terms, still within the same `scope` ids
* Wire this acceptance gate into your API so UI can never bypass it

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

