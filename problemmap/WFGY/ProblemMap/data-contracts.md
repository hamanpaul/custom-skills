# 📑 Data Contracts — Stable Interfaces for RAG & Agents

Everything WFGY touches is JSON-first and versioned. These “contracts” make pipelines observable, reproducible, and easy to debug.

> **Quick Nav**  
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Traceability](./retrieval-traceability.md) ·
> [Eval](./eval/README.md) ·
> [Ops](./ops/README.md) ·
> Patterns: [SCU](./patterns/pattern_symbolic_constraint_unlock.md) ·
> [Memory Desync](./patterns/pattern_memory_desync.md)

---

## 0) Envelope (required for all records)

```json
{
  "schema_version": "1.0.0",
  "event": "ingest.write | retrieve.run | rerank.run | answer.decide",
  "ts": "2025-08-13T10:22:59Z",
  "trace_id": "uuid",
  "agent_id": "scout|medic|engineer|retriever|system",
  "mem_rev": "r42", 
  "mem_hash": "sha256:..."
}
````

* `mem_rev`/`mem_hash` prevent **memory overwrite** and **desync**.
* Use the same envelope for logs and datasets.

---

## 1) Chunk record

**Purpose:** atomic, traceable text unit for retrieval.

```json
{
  "$schema": "https://wfgy.dev/schemas/chunk-1.0.json",
  "chunk_id": "c_00123",
  "doc_id": "d_wfgy_paper",
  "section_id": "s_intro",
  "span": {"line_start": 120, "line_end": 154},
  "lang": "en",
  "text": "Delta-S measures semantic stress ...",
  "hash": "sha256:...",
  "embedding": {
    "model": "sentence-transformers/all-MiniLM-L6-v2",
    "dim": 384,
    "vector": [0.012, -0.044, ...],
    "normalized": true,
    "metric": "cosine"
  },
  "anchors": ["ΔS", "semantic stress"]
}
```

**Rules**

* Keep **original text** + **normalized text** (case/punctuation) if you apply normalization downstream.
* Always store `metric` and `normalized`.

---

## 2) Query record

```json
{
  "$schema": "https://wfgy.dev/schemas/query-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "text": "How does ΔS detect retrieval failure?",
  "lang": "en",
  "hyde": "Generate a canonical query about ... (optional)",
  "tokens": {"count": 12, "analyzer": "icu"},
  "hints": {"doc_id": ["d_wfgy_paper"], "section_id": []}
}
```

---

## 3) Retrieval result (candidate)

```json
{
  "$schema": "https://wfgy.dev/schemas/retrieved-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "ranker": "dense|bm25|hybrid",
  "k": 50,
  "items": [
    {
      "chunk_id": "c_00123",
      "doc_id": "d_wfgy_paper",
      "score": 0.812,           // retriever-native score
      "cosine": 0.91,           // optional explicit cosine
      "ΔS_q_ctx": 0.36,         // optional, if ground anchor available
      "source": "dense",
      "features": {"bm25": 8.3, "dense": 0.91}
    }
  ]
}
```

---

## 4) Rerank result

```json
{
  "$schema": "https://wfgy.dev/schemas/rerank-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "model": "BAAI/bge-reranker-base",
  "k_in": 60,
  "k_out": 8,
  "items": [
    {
      "chunk_id": "c_00123",
      "pre_score": {"dense": 0.91, "bm25": 8.3},
      "post_score": {"ce": 0.82},
      "reason": "mentions ΔS definition and failure threshold",
      "selected": true
    }
  ]
}
```

---

## 5) Prompt frame (schema-locked)

```json
{
  "$schema": "https://wfgy.dev/schemas/prompt-frame-1.0.json",
  "system": "You are a grounded assistant. Cite before you explain.",
  "task": "Answer the user's question using ONLY the cited snippets.",
  "constraints": ["No cross-source merging", "Cite line spans"],
  "citations": [
    {"id": "c_00123", "doc_id": "d_wfgy_paper", "section_id": "s_intro", "span": [120,154]}
  ],
  "question": "How does ΔS detect retrieval failure?"
}
```

---

## 6) Answer + trace

```json
{
  "$schema": "https://wfgy.dev/schemas/answer-1.0.json",
  "q_id": "q_2025_08_13_0001",
  "answer_text": "ΔS measures the semantic gap ...",
  "cited_chunks": ["c_00123", "c_00987"],
  "λ_observe": "→",
  "metrics": {"ΔS_q_ctx": 0.38, "latency_ms": 922}
}
```

---

## 7) Metrics pack (for CI)

```json
{
  "$schema": "https://wfgy.dev/schemas/metrics-1.0.json",
  "dataset": "goldset_v1",
  "recall@50": 0.91,
  "nDCG@10": 0.62,
  "ΔS_mean": 0.41,
  "ΔS_p95": 0.58,
  "λ_convergent_rate": 0.82
}
```

---

## Acceptance checklist

* ✅ All records include **envelope** (schema\_version, event, ts, trace\_id, mem\_rev/hash).
* ✅ Chunks persist **metric** and **normalized** flags.
* ✅ Prompts are **schema-locked** (cite → explain).
* ✅ Answers store **cited chunk IDs** and **λ state**.
* ✅ Metrics committed per PR (goldset.jsonl).

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

