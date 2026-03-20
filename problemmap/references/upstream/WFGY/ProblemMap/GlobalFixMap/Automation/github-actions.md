# GitHub Actions — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Automation Platforms**.  
  > To reorient, go back here:  
  >
  > - [**Automation Platforms** — stabilize no-code workflows and integrations](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

Use this when your automation runs in **GitHub Actions** and you see race conditions, duplicate runs, stale artifacts, secret mismatch, or retrieval steps that look fine but answers drift.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Workflow jobs start before embeddings or the index are ready  
  Fix No.14: **Bootstrap Ordering** →  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First run after deploy uses wrong secret or old model version  
  Fix No.16: **Pre-Deploy Collapse** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Circular waits between indexing and retrieval jobs or external runners  
  Fix No.15: **Deployment Deadlock** →  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High vector similarity but wrong meaning in answers  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Logs cannot explain “why this snippet” was chosen  
  Fix No.8: **Retrieval Traceability** →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Standardize with **Data Contracts** →  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval underperforms single retriever when mixing sources or rerankers  
  Pattern: **Query Parsing Split** →  
  [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Review **Rerankers** →  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts exist in the store but are never retrieved  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Minimal GitHub Actions workflow with WFGY gates

```yaml
name: rag-pipeline

on:
  workflow_dispatch:
  push:
    paths:
      - "rag/**"
      - ".github/workflows/rag-pipeline.yml"

env:
  VECTOR_READY_FLAG: vector_ready.txt
  INDEX_HASH_FILE: index_hash.txt
  SECRET_REV: ${{ secrets.SECRET_REV }}

jobs:
  build-index:
    runs-on: ubuntu-latest
    outputs:
      index_hash: ${{ steps.hash.outputs.index_hash }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        run: |
          pip install -r rag/requirements.txt

      - name: Build index
        run: |
          python rag/build_index.py --out artifacts/index.faiss --metric cosine
          echo "ok" > $VECTOR_READY_FLAG

      - name: Compute INDEX_HASH
        id: hash
        run: |
          python - << 'PY'
import hashlib, sys
with open("artifacts/index.faiss","rb") as f:
    h = hashlib.sha256(f.read()).hexdigest()
open("${{ env.INDEX_HASH_FILE }}","w").write(h)
print(f"index_hash={h}")
PY
          echo "index_hash=$(cat $INDEX_HASH_FILE)" >> $GITHUB_OUTPUT

      - name: Upload index artifacts
        uses: actions/upload-artifact@v4
        with:
          name: rag-index
          path: |
            artifacts/index.faiss
            ${{ env.VECTOR_READY_FLAG }}
            ${{ env.INDEX_HASH_FILE }}

  run-llm:
    runs-on: ubuntu-latest
    needs: build-index
    steps:
      - uses: actions/checkout@v4

      - name: Download index artifacts
        uses: actions/download-artifact@v4
        with:
          name: rag-index
          path: artifacts

      - name: Warm-up fence
        run: |
          test -f artifacts/${{ env.VECTOR_READY_FLAG }} || { echo "Vector not ready"; exit 1; }
          test -f artifacts/${{ env.INDEX_HASH_FILE }} || { echo "Missing INDEX_HASH"; exit 1; }
          echo "wf_rev=${{ github.run_id }}"
          echo "secret_rev=${{ env.SECRET_REV }}"
          echo "index_hash=$(cat artifacts/${{ env.INDEX_HASH_FILE }})"

      - name: Run guarded RAG
        env:
          WF_REV: ${{ github.run_id }}
          SECRET_REV: ${{ env.SECRET_REV }}
          INDEX_HASH: ${{ needs.build-index.outputs.index_hash }}
        run: |
          python rag/run_guarded.py \
            --wf-rev "$WF_REV" \
            --secret-rev "$SECRET_REV" \
            --index-hash "$INDEX_HASH" \
            --trace out/trace.json \
            --emit out/answer.json

      - name: ΔS and λ checks
        run: |
          python rag/check_metrics.py --trace out/trace.json --fail-threshold 0.60

      - name: Upload outputs
        uses: actions/upload-artifact@v4
        with:
          name: rag-output
          path: out/
````

**What this enforces**

* Build and retrieval use the same metric and a single `INDEX_HASH`.
* LLM job hard-fails if the vector layer is not ready.
* A separate metrics step rejects runs with ΔS ≥ 0.60 or divergent λ.
* Artifacts give you traceability for “why this snippet”.

Specs and recipes
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Common GitHub Actions gotchas

* **Workflow re-runs** mutate state
  Compute a server-side `dedupe_key = sha256(run_id + wf_rev + index_hash)`. Reject duplicates.

* **Matrix jobs** double write to the same index or store
  Serialize writes or gate on a single producer job. Use `needs:` fan-in.

* **Secrets rotate during a long build**
  Stamp `secret_rev` into artifacts and validate in the consumer job. Abort on mismatch.
  See [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Artifact retention** truncates traces that you need for audits
  Set longer retention or sync traces to durable storage with rev-stamped paths.

* **Cosine vs inner product mismatch** between write and read codepaths
  Rebuild with explicit metric and normalization.
  See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## When to escalate

* ΔS stays ≥ 0.60 after chunk and retrieval fixes
  Work through the playbook to rebuild and verify.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Same inputs flip answers between runs or branches
  Check version skew and session state.
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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

