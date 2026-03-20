# Example 05 — Vector Store Repair & Metrics (No.3 Index Schema Drift)

**Goal**  
Detect and repair **index schema drift** before you query. We standardize a manifest, validate compatibility at runtime, and—if needed—rebuild the index deterministically. Compatible with FAISS (CPU), SQLite VSS, or any store as long as you emit the manifest.

**Problem Map link**  
Targets **No.3 Index Schema Drift**. Also reduces **No.1** (hallucination) and **No.4** (tail noise) by making scores comparable across rebuilds.

**Outcome**  
- A versioned **manifest.json** that fingerprints your index build (chunker, model, metric, dims, normalization, locale, etc.)  
- A **validator** that fails fast if runtime config mismatches the index  
- A **repair path** that rebuilds the store and proves score comparability  
- A small **metrics panel** (recall@k, citation overlap, score correlation)

---

## 1) Inputs

- `data/chunks.json` — array of `{id, page, text}` (from earlier examples)  
- You choose the backend (this example uses FAISS FlatIP on CPU)

---

## 2) Manifest schema (store with every index)

Create `index_out/manifest.json` at build time:

```json
{
  "schema_version": "1.0",
  "index_type": "faiss.IndexFlatIP",
  "metric": "inner_product",
  "embedding": {
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "dimension": 384,
    "normalized": true
  },
  "chunker": {
    "name": "wfgy-chunker",
    "version": "2025.08.12",
    "rules": {
      "max_tokens": 350,
      "boundary_markers": ["abstract","introduction","conclusion","references"]
    }
  },
  "text_preproc": {
    "unicode_norm": "NFC",
    "lowercase": true,
    "strip_punct": false,
    "language": "en"
  },
  "build": {
    "chunks": 1274,
    "checksum_chunks_json_sha256": "…",
    "created_at_utc": "2025-08-12T12:34:56Z",
    "tool_versions": {
      "sentence_transformers": "2.7.0",
      "faiss": "1.8.0",
      "python": "3.11.9"
    }
  }
}
````

**Compatibility rule (must all match unless a declared converter exists):**
`index_type` • `metric` • `embedding.model` • `embedding.dimension` • `embedding.normalized` • `chunker.version` • `text_preproc.unicode_norm/lowercase/language`.

---

## 3) Path A — Python: build + manifest (CPU only)

Install:

```bash
pip install pyyaml numpy sentence-transformers faiss-cpu
```

Build script `tools/build_index.py`:

```python
# tools/build_index.py -- build FAISS + manifest
import json, os, sys, hashlib, time
import numpy as np, faiss
from sentence_transformers import SentenceTransformer

EMB_MODEL = os.getenv("EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OUT_DIR   = sys.argv[2] if len(sys.argv) > 2 else "index_out"

def sha256(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def main(chunks_path, out_dir=OUT_DIR):
    os.makedirs(out_dir, exist_ok=True)
    chunks = json.load(open(chunks_path, encoding="utf8"))
    texts  = [c["text"] for c in chunks]
    ids    = [c["id"] for c in chunks]

    model  = SentenceTransformer(EMB_MODEL)
    embs   = model.encode(texts, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    d = embs.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embs.astype(np.float32))

    faiss.write_index(index, f"{out_dir}/faiss.index")
    np.save(f"{out_dir}/embs.npy", embs)
    json.dump(ids, open(f"{out_dir}/ids.json","w"))

    manifest = {
        "schema_version": "1.0",
        "index_type": "faiss.IndexFlatIP",
        "metric": "inner_product",
        "embedding": { "model": EMB_MODEL, "dimension": int(d), "normalized": True },
        "chunker":   { "name": "wfgy-chunker", "version": "2025.08.12",
                       "rules": { "max_tokens": 350,
                                  "boundary_markers": ["abstract","introduction","conclusion","references"] } },
        "text_preproc": { "unicode_norm":"NFC","lowercase":True,"strip_punct":False,"language":"en" },
        "build": {
            "chunks": len(chunks),
            "checksum_chunks_json_sha256": sha256(chunks_path),
            "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tool_versions": {
                "sentence_transformers": getattr(model, "__version__", "unknown"),
                "faiss": faiss.__version__,
                "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            }
        }
    }
    json.dump(manifest, open(f"{out_dir}/manifest.json","w"), indent=2)
    print(f"Wrote {out_dir}/faiss.index and manifest.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python tools/build_index.py data/chunks.json [index_out]")
        sys.exit(1)
    main(sys.argv[1], OUT_DIR)
```

Build:

```bash
python tools/build_index.py data/chunks.json index_out
```

---

## 4) Validator — fail fast if drift is detected

Runtime config `tools/runtime_config.json`:

```json
{
  "embedding": { "model": "sentence-transformers/all-MiniLM-L6-v2", "normalized": true, "dimension": 384 },
  "index_type": "faiss.IndexFlatIP",
  "metric": "inner_product",
  "chunker_version": "2025.08.12",
  "text_preproc": { "unicode_norm": "NFC", "lowercase": true, "language": "en" }
}
```

Validator `tools/validate_index.py`:

```python
# tools/validate_index.py -- compare manifest vs runtime config; exit non-zero on FAIL
import json, sys

REQUIRED = [
    ("index_type",), ("metric",),
    ("embedding","model"), ("embedding","dimension"), ("embedding","normalized"),
    ("chunker","version"),
    ("text_preproc","unicode_norm"), ("text_preproc","lowercase"), ("text_preproc","language")
]

def get(d, *keys):
    for k in keys:
        d = d.get(k, {})
    return d if d else None

def main(manifest_path, runtime_cfg_path):
    m = json.load(open(manifest_path, encoding="utf8"))
    r = json.load(open(runtime_cfg_path, encoding="utf8"))

    failures = []
    for path in REQUIRED:
        mv = get(m, *path) if len(path)>1 else m.get(path[0])
        if path == ("chunker","version"):
            rv = r.get("chunker_version")
        else:
            rv = get(r, *path) if len(path)>1 else r.get(path[0])
        if mv != rv:
            failures.append({"field":".".join(path), "manifest": mv, "runtime": rv})

    if failures:
        print("FAIL: incompatible index/runtime configuration")
        for f in failures:
            print(f"- {f['field']}: manifest={f['manifest']} vs runtime={f['runtime']}")
        sys.exit(2)
    print("PASS: index compatible with runtime")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python tools/validate_index.py index_out/manifest.json tools/runtime_config.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
```

Validate:

```bash
python tools/validate_index.py index_out/manifest.json tools/runtime_config.json
```

**Pass criteria**

* On exact match → `PASS`
* On mismatch → `FAIL` with the differing fields listed; your app should abort querying and trigger repair

---

## 5) Repair plan — deterministic rebuild

When validation fails:

1. **Abort queries** to the old index
2. **Rebuild** with the expected runtime config (Section 3)
3. **Verify** with the metrics below before serving traffic

Optionally keep a **migration note** in `index_out/REPAIR.md`:

```markdown
# REPAIR 2025-08-12
- cause: embedding model changed from MiniLM-L6-v2 → all-mpnet-base-v2 (dim 768)
- action: rebuilt embeddings + FAISS index; normalized=True
- verification: recall@5 + citation overlap improved; score corr not comparable due to model change
```

---

## 6) Metrics — prove comparability and quality

### 6.1 Recall\@k and citation overlap (on a tiny QA set)

`eval/qa.json`:

```json
[
  { "qid": "q1", "q": "Define X.", "gold_ids": ["p1#1"] },
  { "qid": "q2", "q": "Explain Y.", "gold_ids": ["p2#1"] }
]
```

Scorer `tools/eval_recall.py`:

```python
# tools/eval_recall.py -- recall@k and gold-id overlap using the built index
import json, sys, numpy as np, faiss
from sentence_transformers import SentenceTransformer

def load(idx_dir, chunks_path):
    ids = json.load(open(f"{idx_dir}/ids.json"))
    index = faiss.read_index(f"{idx_dir}/faiss.index")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    chunks = {c["id"]: c["text"] for c in json.load(open(chunks_path, encoding="utf8"))}
    return model, index, ids, chunks

def retrieve(model, index, ids, q, topk=8):
    v = model.encode([q], normalize_embeddings=True)
    sim, ix = index.search(v.astype(np.float32), topk)
    return [ids[i] for i in ix[0]]

def main(idx_dir, chunks_path, qa_path, k=5):
    model, index, ids, chunks = load(idx_dir, chunks_path)
    qa = json.load(open(qa_path, encoding="utf8"))
    hits = 0
    for item in qa:
        top = retrieve(model, index, ids, item["q"], k)
        if set(item["gold_ids"]) & set(top): hits += 1
        print({"qid": item["qid"], "top": top})
    print(f"recall@{k} = {hits}/{len(qa)} = {hits/len(qa):.2f}")

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("usage: python tools/eval_recall.py index_out data/chunks.json eval/qa.json [k]")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv)>4 else 5)
```

Run:

```bash
python tools/eval_recall.py index_out data/chunks.json eval/qa.json 5
```

**Pass criteria**

* Recall\@5 ≥ your baseline on the same QA set (store the number in your repo)

### 6.2 Score comparability across two indices

When only **non-semantic** parameters changed (e.g., FAISS IVF nlist), scores should correlate.

`tools/score_corr.py`:

```python
# tools/score_corr.py -- compare cosine scores across indexes for a query list
import json, sys, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from scipy.stats import spearmanr  # optional, or implement rank corr manually

def load(idx_dir):
    ids = json.load(open(f"{idx_dir}/ids.json"))
    index = faiss.read_index(f"{idx_dir}/faiss.index")
    return ids, index

def qvec(model, q): return model.encode([q], normalize_embeddings=True).astype(np.float32)

def scores(model, index, q, ids, topk=50):
    sim, ix = index.search(qvec(model,q), topk)
    return { ids[i]: float(s) for i,s in zip(ix[0], sim[0]) }

def main(idx_a, idx_b, queries):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    ids_a, A = load(idx_a); ids_b, B = load(idx_b)
    assert ids_a == ids_b, "compare on same corpus"
    with open(queries, encoding="utf8") as f: Q = [l.strip() for l in f if l.strip()]
    for q in Q:
        sa, sb = scores(model, A, q, ids_a), scores(model, B, q, ids_b)
        # align keys
        common = [k for k in sa.keys() if k in sb]
        xa = np.array([sa[k] for k in common]); xb = np.array([sb[k] for k in common])
        rho = spearmanr(xa, xb).correlation
        print({"q": q, "spearman": float(rho), "n": len(common)})

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("usage: python tools/score_corr.py index_a index_b queries.txt")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
```

Interpretation:

* **High correlation (ρ ≥ 0.9)** → indices are comparable; safe to swap
* **Low correlation** with **different embedding model/dimension/normalization** → expected; treat as a semantic change, re-baseline your eval

---

## 7) Node quick checks (manifest only, no heavy deps)

`tools/manifest_check.mjs`:

```js
// tools/manifest_check.mjs -- fail fast on drift (Node, no deps)
import fs from "node:fs";

const required = [
  ["index_type"], ["metric"],
  ["embedding","model"], ["embedding","dimension"], ["embedding","normalized"],
  ["chunker","version"],
  ["text_preproc","unicode_norm"], ["text_preproc","lowercase"], ["text_preproc","language"]
];

function get(obj, path) {
  return path.reduce((o,k)=> (o && typeof o==='object') ? o[k] : undefined, obj);
}

const [manifestPath, runtimePath] = process.argv.slice(2);
if(!manifestPath || !runtimePath){
  console.error("usage: node tools/manifest_check.mjs index_out/manifest.json tools/runtime_config.json");
  process.exit(1);
}
const m = JSON.parse(fs.readFileSync(manifestPath,"utf8"));
const r = JSON.parse(fs.readFileSync(runtimePath,"utf8"));

let fails = [];
for(const path of required){
  const mv = get(m, path);
  const rv = path.join(".")==="chunker.version" ? r["chunker_version"] : get(r, path);
  if(mv !== rv){
    fails.push({ field: path.join("."), manifest: mv, runtime: rv });
  }
}
if(fails.length){
  console.error("FAIL: incompatible index/runtime configuration");
  for(const f of fails) console.error(`- ${f.field}: manifest=${f.manifest} vs runtime=${f.runtime}`);
  process.exit(2);
}
console.log("PASS: index compatible with runtime");
```

Run:

```bash
node tools/manifest_check.mjs index_out/manifest.json tools/runtime_config.json
```

---

## 8) Common mistakes & quick fixes

* **Mixed chunkers**: building the index from `chunks.json` created with different rules than runtime expects → bump `chunker.version`; rebuild and re-evaluate.
* **Normalization mismatch**: manifest says `normalized=true` but runtime feeds unnormalized query vectors → your scores won’t be comparable; normalize at both build and query.
* **Dimension drift**: switching models without clearing old artifacts → validator will fail on `dimension`. Rebuild fully.
* **Locale drift**: indexing English text but querying in another language without multilingual embeddings → recall collapses; use a multilingual model or translate queries.

---

## 9) Pass/Fail gate you can wire into CI

* **Gate 1 (Schema)**: `validate_index.py` / `manifest_check.mjs` must PASS
* **Gate 2 (Quality)**: recall\@5 vs last baseline must be ≥ baseline − ε (e.g., ε=0.02)
* **Gate 3 (Comparability)**: score correlation ρ ≥ 0.9 for non-semantic changes

If any gate fails → block deploy, open a “REPAIR” note, and rebuild.

---

## 10) Next steps

* Combine with **Example 03** to stabilize candidate sets before rerank
* Use **Example 08** to run a fuller evaluation (precision, refusal, citation overlap)
* Add a small **dashboard** (see `ops/live_monitoring_rag.md`) to watch recall\@k and refusal in prod

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

