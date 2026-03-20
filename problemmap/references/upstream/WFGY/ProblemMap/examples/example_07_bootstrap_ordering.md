# Example 07 — Bootstrap Ordering & Readiness Gate (No.14)

**Goal**  
Eliminate “starts but not ready” failures. We introduce a **deterministic bootstrap sequence** and a **readiness gate** that only flips to `READY` after models, indices, and policies are warmed and verified. Queries routed before that point are rejected fast with `503 Service Unavailable`.

**Problem Map link**  
Targets **No.14 — Bootstrap Ordering**. Secondary reductions in **No.11 (Symbolic Collapse)** by ensuring commits and caches are only exposed post-warmup.

**Outcome**  
- Predictable start-up: no first-minute 500s or null answers  
- A single, observable `READY` flag guarded by verifiable checks  
- Reproducible warm-up that runs the **same path** as production queries (no special backdoor)

---

## 1) Typical failure shapes we will kill

- **Cold model**: first call triggers model download/compile; timeouts or partial prompts  
- **Index not loaded**: FAISS/ANN handle exists but vectors are empty; retrieval returns nothing  
- **Manifest mismatch**: runtime embeds with settings incompatible with index (drift)  
- **Guard missing**: early requests bypass guard/template while warm-up initializes it  
- **Racey caches**: concurrent warm-ups rebuild the same index/embeddings; last writer wins  
- **Probe inversion**: liveness probe green, readiness probe also green, but the service is still warming

---

## 2) Bootstrap plan (phased)

We require each phase to **prove** completion before moving on.

0. **Config load** → read runtime config; fail fast if missing  
1. **Manifest validation** → compare `index_out/manifest.json` with runtime (Example 05 validator)  
2. **Model warm-up** → load the embedding/generation models; run a 1-token dry call  
3. **Index warm-up** → load vector index into memory; fetch `ids.json`; touch a sentinel vector  
4. **Sentinel query** → run a realistic retrieval+guarded template end-to-end; verify refusal/answer semantics  
5. **Flip `READY`** → atomically set readiness; export `/readyz` endpoint

If any phase fails: keep `/livez` green, **/readyz red**, and retry phase with backoff. Do **not** accept traffic.

---

## 3) Path A — Python (stdlib HTTP, single file)

Create `server.py`.

```python
# server.py -- readiness-gated RAG microservice (stdlib only)
import json, os, threading, time, socketserver, http.server, urllib.request

READY = False
READY_LOCK = threading.Lock()
STATE = {"phase": "init", "errors": []}

# --- utilities ---------------------------------------------------------------
def log(msg): print(time.strftime("%H:%M:%S"), msg, flush=True)

def http_post_json(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))

def call_openai(prompt, model=os.getenv("OPENAI_MODEL","gpt-4o-mini")):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key: raise RuntimeError("Set OPENAI_API_KEY")
    body = {
        "model": model,
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0
    }
    j = http_post_json("https://api.openai.com/v1/chat/completions", body, {
        "Content-Type":"application/json", "Authorization": f"Bearer {api_key}"
    })
    return j["choices"][0]["message"]["content"].strip()

def build_prompt(q, chunks):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    return (
        "Use only the evidence. If not provable, reply exactly: not in context.\n"
        "Answer format:\n- claim\n- citations: [id,...]\n\n"
        f"Question: {q}\n\nEvidence:\n{ctx}\n"
    )

# --- phases ------------------------------------------------------------------
def phase_config():
    STATE["phase"] = "config"
    # minimal runtime config in env or file
    required = ["OPENAI_API_KEY"]
    for k in required:
        if not os.getenv(k):
            raise RuntimeError(f"missing {k}")
    log("config OK")

def phase_manifest():
    STATE["phase"] = "manifest"
    # compare manifest vs runtime; reuse your Example 05 fields
    manifest = json.load(open("index_out/manifest.json", encoding="utf8"))
    runtime = {
        "index_type": "faiss.IndexFlatIP",
        "metric": "inner_product",
        "embedding": { "model": manifest["embedding"]["model"],
                       "dimension": manifest["embedding"]["dimension"],
                       "normalized": True },
        "chunker_version": manifest["chunker"]["version"],
        "text_preproc": manifest["text_preproc"]
    }
    # simple equality check
    mismatches = []
    if manifest["index_type"] != runtime["index_type"]:
        mismatches.append("index_type")
    if manifest["metric"] != runtime["metric"]:
        mismatches.append("metric")
    if manifest["embedding"]["dimension"] != runtime["embedding"]["dimension"]:
        mismatches.append("embedding.dimension")
    if manifest["embedding"]["model"] != runtime["embedding"]["model"]:
        mismatches.append("embedding.model")
    if manifest["chunker"]["version"] != runtime["chunker_version"]:
        mismatches.append("chunker.version")
    if mismatches:
        raise RuntimeError("manifest mismatch: " + ", ".join(mismatches))
    log("manifest OK")

def phase_model():
    STATE["phase"] = "model"
    # 1-token dry pass to ensure the model is reachable
    _ = call_openai("Reply with: ok", model=os.getenv("OPENAI_MODEL","gpt-4o-mini"))
    log("model warm OK")

def phase_index():
    STATE["phase"] = "index"
    # lightweight: just ensure ids.json and chunks.json are readable
    ids = json.load(open("index_out/ids.json"))
    chunks = json.load(open("data/chunks.json", encoding="utf8"))
    if not ids or not chunks:
        raise RuntimeError("index or chunks missing")
    STATE["ids"] = ids
    STATE["chunks"] = {c["id"]: c for c in chunks}
    log("index warm OK")

def phase_sentinel():
    STATE["phase"] = "sentinel"
    # end-to-end smoke: take first two chunks; ask a question that should refuse or answer
    ids = STATE["ids"][:2]
    chunks = [STATE["chunks"][i] for i in ids if i in STATE["chunks"]]
    q = "What is X?"
    prompt = build_prompt(q, chunks)
    ans = call_openai(prompt)
    if not (("citations" in ans.lower()) or ("not in context" in ans.lower())):
        raise RuntimeError("sentinel failed template")
    log("sentinel OK")

def warmup():
    global READY
    try:
        for step in (phase_config, phase_manifest, phase_model, phase_index, phase_sentinel):
            try:
                step()
            except Exception as e:
                STATE["errors"].append({"phase": STATE["phase"], "error": str(e)})
                log(f"[retry in 3s] {STATE['phase']} failed: {e}")
                time.sleep(3)
                return warmup()  # restart phases from the beginning
        with READY_LOCK:
            READY = True
            STATE["phase"] = "ready"
        log("READY=TRUE")
    except Exception as e:
        STATE["errors"].append({"phase": "fatal", "error": str(e)})
        log("fatal warmup error: " + str(e))

# --- HTTP server -------------------------------------------------------------
class Handler(http.server.BaseHTTPRequestHandler):
    def _write(self, code, payload):
        self.send_response(code); self.send_header("Content-Type","application/json"); self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        if self.path == "/livez":
            return self._write(200, {"live": True, "phase": STATE["phase"]})
        if self.path == "/readyz":
            return self._write(200 if READY else 503, {"ready": READY, "phase": STATE["phase"], "errors": STATE["errors"][-5:]})
        if self.path.startswith("/answer"):
            if not READY: return self._write(503, {"error":"not ready"})
            # minimal demo answer using first two chunks
            q = self.path.split("q=",1)[1] if "q=" in self.path else "What is X?"
            ids = STATE["ids"][:2]
            chunks = [STATE["chunks"][i] for i in ids if i in STATE["chunks"]]
            ans = call_openai(build_prompt(q, chunks))
            return self._write(200, {"q": q, "answer": ans, "chunks": ids})
        return self._write(404, {"error":"not found"})

def main():
    threading.Thread(target=warmup, daemon=True).start()
    with socketserver.TCPServer(("", 8080), Handler) as httpd:
        log("listening on :8080")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
````

Run:

```bash
# preconditions: index_out/{manifest.json,ids.json} and data/chunks.json exist
OPENAI_API_KEY=sk-xxx python server.py
# in another shell
curl -s localhost:8080/livez
curl -s localhost:8080/readyz   # expect 503 until warm-up ends, then 200
curl -s "localhost:8080/answer?q=What%20is%20X?"
```

**Pass criteria**

* `/livez` is **always** 200 after process starts
* `/readyz` returns 503 **until** sentinel passes; then flips to 200 and stays green
* `/answer` rejects with 503 before ready; serves after ready

---

## 4) Path B — Node (http stdlib, single file)

Create `server.mjs`.

```js
// server.mjs -- readiness-gated RAG microservice (Node stdlib)
import http from "node:http";
import fs from "node:fs";
import https from "node:https";

let READY = false;
const STATE = { phase: "init", errors: [], ids: [], chunks: {} };

function log(...a){ console.log(new Date().toISOString(), ...a); }

function callOpenAI(prompt, model=process.env.OPENAI_MODEL || "gpt-4o-mini"){
  const key = process.env.OPENAI_API_KEY; if(!key) throw new Error("Set OPENAI_API_KEY");
  const body = JSON.stringify({ model, messages:[{role:"user", content: prompt}], temperature: 0 });
  return new Promise((resolve,reject)=>{
    const req = https.request("https://api.openai.com/v1/chat/completions", {
      method:"POST",
      headers:{ "Content-Type":"application/json", "Authorization":`Bearer ${key}`, "Content-Length": Buffer.byteLength(body) }
    }, res => { let d=""; res.on("data",x=>d+=x); res.on("end",()=>resolve(JSON.parse(d).choices[0].message.content.trim())); });
    req.on("error", reject); req.write(body); req.end();
  });
}

function buildPrompt(q, chunks){
  const ctx = chunks.map(c => `[${c.id}] ${c.text}`).join("\n\n");
  return `Use only the evidence. If not provable, reply exactly: not in context.
Answer format:
- claim
- citations: [id,...]

Question: ${q}

Evidence:
${ctx}
`;
}

async function warmup(){
  try {
    STATE.phase = "config";
    if(!process.env.OPENAI_API_KEY) throw new Error("missing OPENAI_API_KEY");

    STATE.phase = "manifest";
    const m = JSON.parse(fs.readFileSync("index_out/manifest.json","utf8"));
    if(m.index_type !== "faiss.IndexFlatIP" || m.metric !== "inner_product") throw new Error("manifest mismatch");

    STATE.phase = "model";
    await callOpenAI("Reply with: ok");

    STATE.phase = "index";
    STATE.ids = JSON.parse(fs.readFileSync("index_out/ids.json","utf8"));
    const chunksArr = JSON.parse(fs.readFileSync("data/chunks.json","utf8"));
    STATE.chunks = Object.fromEntries(chunksArr.map(c => [c.id, c]));

    STATE.phase = "sentinel";
    const ids = STATE.ids.slice(0,2);
    const chunks = ids.map(i => STATE.chunks[i]).filter(Boolean);
    const ans = await callOpenAI(buildPrompt("What is X?", chunks));
    if(!(ans.toLowerCase().includes("citations") || ans.toLowerCase().includes("not in context")))
      throw new Error("sentinel failed template");

    READY = true; STATE.phase = "ready"; log("READY=TRUE");
  } catch (e){
    STATE.errors.push({ phase: STATE.phase, error: String(e) });
    log("[retry in 3s]", STATE.phase, e);
    setTimeout(warmup, 3000);
  }
}

const server = http.createServer(async (req,res)=>{
  const json = (code,obj)=>{ res.writeHead(code,{"Content-Type":"application/json"}); res.end(JSON.stringify(obj)); };
  if(req.url === "/livez") return json(200, {live:true, phase:STATE.phase});
  if(req.url === "/readyz") return json(READY?200:503, {ready:READY, phase:STATE.phase, errors:STATE.errors.slice(-5)});
  if(req.url.startsWith("/answer")){
    if(!READY) return json(503, {error:"not ready"});
    const q = (req.url.split("q=")[1]||"What is X?").replace(/\+/g," ");
    const ids = STATE.ids.slice(0,2);
    const chunks = ids.map(i => STATE.chunks[i]).filter(Boolean);
    const ans = await callOpenAI(buildPrompt(q, chunks));
    return json(200, {q, answer: ans, chunks: ids});
  }
  return json(404, {error:"not found"});
});

server.listen(8080, ()=>{ log("listening on :8080"); warmup(); });
```

Run:

```bash
OPENAI_API_KEY=sk-xxx node server.mjs
curl -s localhost:8080/readyz
```

**Pass criteria** mirror the Python version.

---

## 5) K8s / container probes (production hints)

**Key principle:** **liveness** means “process is alive”, **readiness** means “pipeline is provably usable.”

```yaml
# deployment snippet (k8s)
livenessProbe:
  httpGet: { path: /livez, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 5
readinessProbe:
  httpGet: { path: /readyz, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 3
```

**Order of dependencies at boot**

1. Config & secrets
2. Storage mounts (index files)
3. Network (LLM endpoint)
4. Service warm-up → `/readyz` flips
5. Gate ingress/traffic

---

## 6) Anti-race guarantees

* **Single warm-up owner**: a background thread/task holds a lock; other threads read `READY` only
* **Idempotent warm-up**: re-running warm-up does not corrupt state; it re-verifies and flips `READY` if all checks pass
* **Atomic flag**: only set `READY=True` **after** all phases succeed; do not stream partial readiness

---

## 7) Common mistakes & quick fixes

* **Probe copy-paste**: exposing `/readyz` that always returns 200 → defeats the point; wire it to the real checks
* **Warm-up path ≠ prod path**: using a special “test prompt” that skips the guard/template → sentinel passes but prod fails; run the **same template**
* **Index drift post-deploy**: replacing `index_out` files on disk without flipping readiness to red → serve stale ids; add a file watcher to invalidate readiness and re-warm

---

## 8) What to log

Append a line to `runs/boot.jsonl` at each phase:

```json
{"ts":1699999999,"phase":"manifest","ok":true}
{"ts":1699999999,"phase":"ready","ok":true}
```

Alert on repeated retries or prolonged `ready=false` after deploy.

---

## 9) Next steps

* Combine with **Example 03** and **05** so readiness includes retrieval quality (knee cut present) and schema validation
* Add **Ops** dashboards (see `ops/live_monitoring_rag.md`): track `readyz` duration, first-token latency, refusal and citation rates
* For multi-instance rollouts, use a rolling update policy that drains traffic from old pods only after new pods report `ready=true` for N seconds

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

