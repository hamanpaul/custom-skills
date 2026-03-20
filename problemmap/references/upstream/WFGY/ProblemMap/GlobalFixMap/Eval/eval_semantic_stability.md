# Eval — Semantic Stability (Seed & Prompt Jitter, stdlib-only)

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval**.  
  > To reorient, go back here:  
  >
  > - [**Eval** — model evaluation and benchmarking](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

> **Evaluation disclaimer (semantic stability)**  
> Stability scores in this page are heuristic signals about how outputs move under small changes.  
> They do not prove global robustness or safety and should be combined with other checks.

---

**Goal**  
Quantify how **stable** your pipeline is under small, *non-semantic* perturbations: different seeds, low temperature noise, and benign **prompt jitters** (punctuation/whitespace/synonym swaps). A robust system should keep claims, citations, refusals, and constraint echos **invariant** (or nearly so).

**What you get**
- Clear invariants: **Claim**, **Citation**, **Refusal**, **Constraint Echo (SCU)**
- Deterministic metrics: **I-AA** (intra-answer agreement), **NED** (normalized edit distance), **CSS** (citation-set stability), **RCR** (refusal consistency rate)
- A stdlib-only **runner** that repeats each QID under seeds & jitters, and a strict **CI gate**

---

## 1) Stability Invariants & Metrics

Let a question `q` be executed **N** times with seed set `S` and jitter set `J`. Each run `r` produces:
- `claim` (string) or exact refusal token `not in context`
- `citations` (list of ids, scoped to retrieved ids)
- Optional: `constraints_echo` (list of locked constraints)

**Normalization**
- `canon(claim)` = lowercase → strip punctuation/extra spaces.
- `C` (containment): at least one `gold_claim_substr` ∈ `canon(claim)` (≥5 chars, case-insensitive).
- `H` (citation hit): `(citations ∩ gold_citations) ≠ ∅` and `citations ⊆ retrieved_ids`.

**Per-QID metrics**
- **RCR** (Refusal Consistency Rate) = max class frequency of `is_refusal` over N runs.
- **ACR** (All-run Containment Rate) = |{runs with C=true}| / N.
- **CGHC** (Citation Gold Hit Consistency) = |{runs with H=true}| / N.
- **CSS** (Citation Set Stability) = `|∩_runs citations| / |∪_runs citations|` (IoU of citation sets).
- **NED₅₀** (Median Normalized Edit Distance) = median over all run pairs `ned(claim_i, claim_j)` where
  \[
  \text{ned}(a,b) = \frac{\text{lev}(a,b)}{\max(|a|,|b|,1)}
  \]
- **SCU-Cons** (Constraint Echo Consistency) = 1 if every run’s `constraints_echo` equals the locked set; else 0.

> We prefer **semantic invariants** (ACR, CGHC, CSS) over surface-similarity alone (NED), but we track both.

**Default stability gates (suggested)**
- For `answerable=true` items:
  - **ACR ≥ 0.95**, **CGHC ≥ 0.95**, **CSS ≥ 0.70**, **NED₅₀ ≤ 0.20**
  - If constraints provided: **SCU-Cons = 1**
- For `answerable=false` items:
  - **RCR ≥ 0.98** (refusal nearly always preserved)

---

## 2) Experiment Design (Seeds × Jitters)

**Seeds:** e.g., S = {0,1,2,3,4} with `temperature ∈ {0.0, 0.2}` (model-side)  
**Prompt jitters (question-side; deterministic & benign):**
- `ws` — normalize/densify whitespace (adds/removes single spaces)
- `punct` — swap `?`↔`—`, add commas where harmless
- `syn` — swap common verbs: *explain→describe, list→enumerate, compare→contrast*
- `order` — reorder a pair of non-semantic clauses (“with citations, in one sentence”)

Each run picks `(seed, jitter)` from a small grid. No external libs; all jitters are **pure string transforms**.

---

## 3) Data Contracts (recap)

- **Gold** (`ProblemMap/eval/gold.jsonl`)  
  Same as other evals: `qid`, `question`, `answerable`, `gold_claim_substr`, `gold_citations`, optional `constraints`.

- **Traces (per-run)** appended to `runs/stability.jsonl` by this runner:
```json
{
  "qid":"A0001","run_id":"A0001#seed=2;j=punct",
  "seed":2,"jitter":"punct",
  "answer_json":{"claim":"X rejects null keys.","citations":["p1#2"],"constraints_echo":["X rejects null keys."]},
  "retrieved_ids":["p1#1","p1#2","p2#1"]
}
````

---

## 4) Reference Runner (stdlib-only)

Save as `ProblemMap/eval/semantic_stability.py`:

```python
#!/usr/bin/env python3
import json, argparse, random, time, re, urllib.request, itertools, math, string, sys, os

REFUSAL = "not in context"

# --------- prompt jitters (benign, deterministic) ----------------------------
SYN_MAP = {
    r"\bexplain\b": "describe",
    r"\blist\b": "enumerate",
    r"\bcompare\b": "contrast",
    r"\bshow\b": "display",
}

def jitter_ws(q):  # add/remove single spaces around commas/colons
    q = re.sub(r"\s+,", ",", q)
    q = re.sub(r",\s*", ", ", q)
    q = re.sub(r"\s+:", ": ", q)
    q = re.sub(r"\s{2,}", " ", q)
    return q.strip()

def jitter_punct(q):
    q = q.replace("?", " ?").replace("  ", " ")
    q = q.replace("—", "-").replace("–", "-")
    if not q.endswith("?") and q[-1] not in ".!?":
        q += "?"
    return q

def jitter_syn(q):
    s = q
    for pat, repl in SYN_MAP.items():
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    return s

def jitter_order(q):
    # swap order of two benign optional clauses if present
    parts = re.split(r"\s+with\s+citations\s*,?\s*|\s*,?\s*in\s+one\s+sentence\s*", q, flags=re.IGNORECASE)
    if len(parts) >= 2 and "with citations" in q.lower() and "in one sentence" in q.lower():
        # rebuild in swapped order
        base = parts[0].strip()
        return f"{base} in one sentence, with citations"
    return q

JITTERS = {"none": lambda x:x, "ws": jitter_ws, "punct": jitter_punct, "syn": jitter_syn, "order": jitter_order}

# --------- helpers -----------------------------------------------------------
def canon(s):
    s = s.lower().strip()
    s = s.translate(str.maketrans("", "", string.punctuation))
    s = re.sub(r"\s+", " ", s)
    return s

def contains_substr(claim, subs):
    c = canon(claim or "")
    if not subs: return True
    subs = [canon(x) for x in subs if x and len(x)>=5]
    return any(s in c for s in subs)

def citation_hit(citations, gold, retrieved):
    if not isinstance(citations, list): return False
    if not set(citations).issubset(set(retrieved or [])): return False
    return bool(set(citations or []) & set(gold or [])) if gold else (citations == [])

def levenshtein(a, b):
    a, b = a or "", b or ""
    if a == b: return 0
    la, lb = len(a), len(b)
    if la == 0: return lb
    if lb == 0: return la
    dp = list(range(lb+1))
    for i in range(1, la+1):
        prev, dp[0] = dp[0], i
        for j in range(1, lb+1):
            cur = dp[j]
            cost = 0 if a[i-1]==b[j-1] else 1
            dp[j] = min(dp[j]+1, dp[j-1]+1, prev+cost)
            prev = cur
    return dp[lb]

def ned(a, b):
    m = max(len(a or ""), len(b or ""), 1)
    return levenshtein(a or "", b or "") / m

def percentiles(xs, ps=(50,)):
    if not xs: return {p:0 for p in ps}
    xs = sorted(xs)
    out={}
    for p in ps:
        k=(p/100)*(len(xs)-1)
        f=int(k); c=min(f+1,len(xs)-1); d=k-f
        out[p]=xs[f]*(1-d)+xs[c]*d
    return out

# --------- pipeline hook -----------------------------------------------------
def call_pipeline_http(url, question, seed, jitter_name, knobs=None):
    body = json.dumps({"q": question, "seed": seed, "jitter": jitter_name, "knobs": knobs or {}}).encode("utf-8")
    req  = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))
    # Expected:
    # {
    #   "answer_json": {"claim": str, "citations":[id,...], "constraints_echo":[...]?},
    #   "retrieved_ids":[id,...]
    # }

def call_pipeline_local(question, seed, jitter_name, knobs=None):
    # Replace with your local guarded call (Example 01/03). Stub here:
    random.seed(seed)
    return {"answer_json":{"claim": REFUSAL, "citations":[]}, "retrieved_ids":[]}

# --------- experiment runner -------------------------------------------------
def run_stability(gold_path, url=None, seeds="0,1,2,3,4", jitters="none,ws,punct,syn", out="runs/stability.jsonl"):
    seeds = [int(x) for x in seeds.split(",") if x!=""]
    jitters = [j for j in jitters.split(",") if j in JITTERS]
    gold = [json.loads(l) for l in open(gold_path,encoding="utf8") if l.strip()]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    f = open(out,"a",encoding="utf8")
    for g in gold:
        qid, q = g["qid"], g["question"]
        for s, j in itertools.product(seeds, jitters):
            qjit = JITTERS[j](q)
            res = call_pipeline_http(url, qjit, s, j) if url else call_pipeline_local(qjit, s, j)
            rec = {
                "qid": qid,
                "run_id": f"{qid}#seed={s};j={j}",
                "seed": s,
                "jitter": j,
                "answer_json": res.get("answer_json",{}),
                "retrieved_ids": res.get("retrieved_ids",[])
            }
            f.write(json.dumps(rec, ensure_ascii=False)+"\n")
    f.close()

# --------- scorer over stability.jsonl --------------------------------------
def score_stability(gold_path, stability_path, gates=None):
    gates = gates or {"acr":0.95,"cghc":0.95,"css":0.70,"ned50":0.20,"rcr":0.98}
    gold = {g["qid"]: g for g in (json.loads(l) for l in open(gold_path,encoding="utf8") if l.strip())}
    rows = [json.loads(l) for l in open(stability_path,encoding="utf8") if l.strip()]
    by_q = {}
    for r in rows:
        by_q.setdefault(r["qid"], []).append(r)

    agg = {"answerable":0,"unanswerable":0,"fail":0,"pass":0}
    details = {}

    for qid, runs in by_q.items():
        g = gold.get(qid, {})
        answ = bool(g.get("answerable"))
        if answ: agg["answerable"]+=1
        else: agg["unanswerable"]+=1

        claims = [r.get("answer_json",{}).get("claim","") for r in runs]
        cits   = [tuple(r.get("answer_json",{}).get("citations",[]) or []) for r in runs]
        ret_ids= [set(r.get("retrieved_ids",[]) or []) for r in runs]
        is_ref = [ (c or "").strip().lower()==REFUSAL for c in claims ]
        # ACR/CGHC
        C = [contains_substr(c, g.get("gold_claim_substr")) for c in claims]
        H = [citation_hit(list(cits[i]), g.get("gold_citations"), list(ret_ids[i])) for i in range(len(runs))]
        acr  = sum(1 for x in C if x)/max(len(runs),1)
        cghc = sum(1 for x in H if x)/max(len(runs),1)
        # CSS
        inter = set(cits[0])
        union = set(cits[0])
        for s in cits[1:]:
            inter &= set(s); union |= set(s)
        css = (len(inter)/len(union)) if union else 1.0
        # NED50 (pairwise)
        claim_norm = [canon(c) for c in claims if c and (c.strip().lower()!=REFUSAL)]
        dists = []
        for i in range(len(claim_norm)):
            for j in range(i+1, len(claim_norm)):
                dists.append(ned(claim_norm[i], claim_norm[j]))
        ned50 = percentiles(dists, (50,)).get(50, 0.0) if dists else 0.0
        # RCR
        maj = max(sum(1 for x in is_ref if x), sum(1 for x in is_ref if not x))
        rcr = maj/max(len(is_ref),1)
        # SCU
        if g.get("constraints"):
            ech = [tuple((r.get("answer_json",{}).get("constraints_echo") or [])) for r in runs]
            scu_cons = 1 if all(set(e)==set(g["constraints"]) for e in ech) else 0
        else:
            scu_cons = None

        # decide per QID
        if answ:
            ok = (acr>=gates["acr"] and cghc>=gates["cghc"] and css>=gates["css"] and ned50<=gates["ned50"] and (scu_cons in (None,1)))
        else:
            ok = (rcr>=gates["rcr"])
        details[qid] = {"acr":round(acr,4),"cghc":round(cghc,4),"css":round(css,4),"ned50":round(ned50,4),"rcr":round(rcr,4),"scu_cons":scu_cons}
        agg["pass" if ok else "fail"] += 1

    # overall decision: must have zero fails
    report = {"totals": agg, "gates": gates, "pass": agg["fail"]==0, "details": details}
    return report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["run","score"], required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--stability", default="runs/stability.jsonl")
    ap.add_argument("--http", default=None, help="http://localhost:8080/qa (optional)")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--jitters", default="none,ws,punct,syn")
    ap.add_argument("--gates", default="acr=0.95,cghc=0.95,css=0.70,ned50=0.20,rcr=0.98")
    args = ap.parse_args()

    if args.mode=="run":
        run_stability(args.gold, url=args.http, seeds=args.seeds, jitters=args.jitters, out=args.stability)
        print(json.dumps({"ok":True,"wrote":args.stability}, indent=2))
    else:
        gates = dict((k,float(v)) for k,v in (kv.split("=") for kv in args.gates.split(",")))
        print(json.dumps(score_stability(args.gold, args.stability, gates), indent=2))

if __name__=="__main__":
    main()
```

**Usage**

```bash
# 1) Run stability (local stub or your HTTP guard)
python ProblemMap/eval/semantic_stability.py --mode run --gold ProblemMap/eval/gold.jsonl --http http://localhost:8080/qa --seeds 0,1,2,3,4 --jitters none,ws,punct,syn

# 2) Score stability
python ProblemMap/eval/semantic_stability.py --mode score --gold ProblemMap/eval/gold.jsonl --stability runs/stability.jsonl \
  --gates acr=0.95,cghc=0.95,css=0.70,ned50=0.20,rcr=0.98 | tee eval/stability.json
```

**Output (example)**

```json
{
  "totals": {"answerable": 20, "unanswerable": 10, "fail": 0, "pass": 30},
  "gates": {"acr":0.95,"cghc":0.95,"css":0.7,"ned50":0.2,"rcr":0.98},
  "pass": true,
  "details": { "A0001": {"acr":1.0,"cghc":1.0,"css":0.75,"ned50":0.08,"rcr":1.0,"scu_cons":1}, "...": "..." }
}
```

---

## 5) CI Wiring (copy/paste)

```bash
# run the sweep once a day or per PR (small seeds/jitters)
python ProblemMap/eval/semantic_stability.py --mode run --gold ProblemMap/eval/gold.jsonl --http http://localhost:8080/qa \
  --seeds 0,1,2 --jitters none,ws,syn

python ProblemMap/eval/semantic_stability.py --mode score --gold ProblemMap/eval/gold.jsonl --stability runs/stability.jsonl \
  --gates acr=0.95,cghc=0.95,css=0.70,ned50=0.20,rcr=0.98 > eval/stability.json

jq -e '.pass == true' eval/stability.json
```

---

## 6) Troubleshooting Map

* **Low ACR/CGHC** (answerable): Retrieval context unstable → use **intersection + knee** and shrink chunks to collocate constraints. See *RAG Semantic Drift* + *Vector Store Fragmentation*.
* **Low CSS**: Multiple near-duplicate evidence ids; stabilize re-ranker and cap rerank depth.
* **High NED** with good ACR/CGHC: Wording variance only; OK if gates passed.
* **Low RCR** (unanswerable): Refusal token drifting → enforce exact token in prompt; tighten acceptance gate.
* **SCU-Cons=0**: Constraint echo not re-injected; apply *Symbolic Constraint Unlock* pattern.

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

