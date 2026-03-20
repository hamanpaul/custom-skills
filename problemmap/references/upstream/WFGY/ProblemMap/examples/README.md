# Problem Map — Examples Index (hands-on, SDK-free)

This folder gives you **copy-paste runnable walkthroughs** that fix real failure modes from the Problem Map.  
Everything is **SDK-free**. You can use Ollama, LangChain, vanilla OpenAI, or anything else.  
Each example follows a strict format so you can reproduce, verify, and ship.

## What you will get from each example

- **Problem:** the exact failure it targets and its Problem Map number  
- **Inputs:** tiny reproducible corpus + the prompt template  
- **Steps:** minimal commands you can paste into a terminal  
- **Checks:** how to verify the fix worked, with clear pass/fail signals  
- **Why it works:** one short paragraph, no fluff

> If you have not run a guarded RAG pipeline yet, start here:  
> **[Getting Started → `ProblemMap/getting-started.md`](../getting-started.md)**

---

## Example list

### 01) Basic Guarded Answer (No.1 Hallucination & Chunk Drift)
- File: [`example_01_basic_fix.md`](./example_01_basic_fix.md)  
- Goal: force the model to answer only from evidence or say `not in context`.  
- Outcome: fewer fabrications, stable citations.

### 02) Self-Reflection Trace (No.1, No.2)
- File: [`example_02_self_reflection.md`](./example_02_self_reflection.md)  
- Goal: log query → retrieved chunks → answer, then reflect where drift starts.  
- Outcome: fast pinpointing of retrieval vs generation faults.

### 03) Pipeline Patch: Intersection + Rerank (No.1, No.4)
- File: [`example_03_pipeline_patch.md`](./example_03_pipeline_patch.md)  
- Goal: combine BM25 ∩ embedding, then rerank by cosine to remove tail noise.  
- Outcome: higher citation hit rate with the same token budget.

### 04) Multi-Agent Coordination Boundary (No.6 Logic Collapse)
- File: [`example_04_multi_agent_coordination.md`](./example_04_multi_agent_coordination.md)  
- Goal: keep sub-agents from merging incompatible contexts.  
- Outcome: fewer cross-topic blends and cleaner handoffs.

### 05) Vector Store Repair and Metrics (No.3 Index Schema Drift)
- File: [`example_05_vectorstore_repair.md`](./example_05_vectorstore_repair.md)  
- Goal: align chunker version, tokenizer, and index metadata.  
- Outcome: comparable scores across rebuilds, stable recall.

### 06) Prompt-Injection Block (Clinic: Injection)
- File: [`example_06_prompt_injection_block.md`](./example_06_prompt_injection_block.md)  
- Goal: sandbox evidence and neutralize instruction pollution.  
- Outcome: controlled outputs that ignore adversarial text.

### 07) Bootstrap Ordering (No.14)
- File: [`example_07_bootstrap_ordering.md`](./example_07_bootstrap_ordering.md)  
- Goal: warm models and indexes before the first query hits.  
- Outcome: no cold-start nulls, fewer first-minute errors.

### 08) Evaluate RAG Quality (Precision, Refusal, Citations)
- File: [`example_08_eval_rag_quality.md`](./example_08_eval_rag_quality.md)  
- Goal: run a tiny benchmark on precision, refusal rate, and citation overlap.  
- Outcome: a repeatable baseline you can compare after every change.

---

## Conventions used by all examples

**1) Evidence-only answer template**

```text
Use only the evidence. If not provable, reply exactly: not in context.
Answer format:
- claim
- citations: [id,...]
````

**2) Minimal hybrid retrieval**

* Retrieve by BM25 and embeddings
* Intersect, then rerank by cosine
* Keep top 8 after rerank, drop the tail

**3) Trace everything**

Each run appends one JSON line to `runs/trace.jsonl`:

```json
{"ts": 1699999999, "q": "question", "chunks": [{"id":"p12#2","score":0.83}], "answer":"...", "ok": true}
```

**4) Verification rules**

* If the answer contains facts outside evidence, it fails
* If evidence is insufficient, the correct output is `not in context`
* Citation ids in the answer must exist in the retrieved set

---

## Quick smoke test before any example

This is a lightweight end-to-end test you can paste now.

```bash
# 1) Prepare a tiny corpus (two short pages as plain text)
mkdir -p data
cat > data/pages.json <<'JSON'
[
  {"id":"p1","page":1,"text":"The library defines X. X is a constrained mapping. See also Y."},
  {"id":"p2","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
JSON

# 2) Create two small chunks (one per page)
cat > data/chunks.json <<'JSON'
[
  {"id":"p1#1","page":1,"text":"X is a constrained mapping."},
  {"id":"p2#1","page":2,"text":"Y is unrelated to X. It describes a separate protocol."}
]
JSON
```

Now choose **Python** or **Node**. Both use the same conventions.

**Python prompt builder** (paste into a REPL and adapt to your LLM client):

```python
def build_prompt(q, chunks):
    ctx = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    return (
        "Use only the evidence. If not provable, reply exactly: not in context.\n"
        "Answer format:\n"
        "- claim\n- citations: [id,...]\n\n"
        f"Question: {q}\n\nEvidence:\n{ctx}\n"
    )

q = "What is X?"
chunks = [
  {"id":"p1#1","text":"X is a constrained mapping."},
  {"id":"p2#1","text":"Y is unrelated to X. It describes a separate protocol."}
]
print(build_prompt(q, chunks))
```

**Node prompt builder**:

```js
function buildPrompt(q, chunks) {
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

console.log(buildPrompt("What is X?", [
  { id:"p1#1", text:"X is a constrained mapping." },
  { id:"p2#1", text:"Y is unrelated to X. It describes a separate protocol." }
]));
```

**Pass criteria**

* A correct answer for “What is X?” must say “X is a constrained mapping.” and cite `[p1#1]`
* If you ask “What is Z?”, the only valid answer is `not in context`

---

## How to use these examples in a real repo

1. Create a branch named `pm-examples`
2. Copy any `example_*.md` you need into your project’s docs folder
3. Replace the tiny corpus with your own `pages.json` and `chunks.json`
4. Keep the template and the verification rules
5. Commit traces for future debugging and audits

If you discover a better parameter or a corner case, open a PR to improve the example.
Clear diffs beat long explanations.

---

## Troubleshooting

* **Model refuses too often**
  Increase top-k to 12 before rerank, but keep only top 8 after rerank.
* **Citations look wrong**
  Check that chunk ids are preserved all the way into the prompt.
* **Different runs give different answers**
  Fix your seed where possible and avoid mixing corpora built by different chunkers.

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

