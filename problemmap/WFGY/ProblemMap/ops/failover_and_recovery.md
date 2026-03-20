# Failover & recovery — deterministic recovery steps

**Purpose:** deterministic operator steps to failover or recover critical components (vectorstore, retriever, generator, indexer, controller). Aim to reduce data loss and return to safe state quickly.

---

## Basic principles
1. **Fail fast to a safe mode** — prefer read-only answers or cached responses over uncontrolled writes or risky LLM calls.  
2. **Preserve evidence** — do not truncate logs or delete index segments until investigation complete.  
3. **Prefer scoped recovery** — restart single pod/shard before cluster-wide actions.

---

## Scenario A: Vectorstore shard down / index corrupt

**Symptoms**
- Retriever returns empty sets or inconsistent scores for golden queries.  
- Vectorstore pod logs show IO / index errors.

**Steps**
1. Mark the shard unhealthy in the service registry (so retriever avoids it).  
2. If replica exists, route traffic to other replica.  
3. Attempt graceful re-open:
   ```bash
   kubectl -n $NS exec deploy/vectorstore -- /bin/sh -c "ctl index reopen shard-5"


4. If reopen fails, restore from latest snapshot (S3) to a new shard:

   * Create new PV and restore snapshot.
   * Start fresh pod pointed to restored PV.
5. Re-run small validation suite (10–50 golden qids) before reintroducing shard.

**Post recovery**

* Re-index missing docs if necessary; track reindex job progress.
* Add a postmortem entry and schedule a permanent fix.

---

## Scenario B: Generator (LLM) provider outage

**Symptoms**

* LLM errors (5xx), rate-limit responses, or auth failures.

**Steps**

1. Switch to backup LLM provider (if configured) via config flag:

   ```bash
   # toggle provider in config map or feature flag
   kubectl -n $NS set env deploy/rag-api PROVIDER=backup-provider
   ```
2. If no backup, enable local fallback:

   * Return cached answers for known qids.
   * Return safe refusal for unknown qids.
3. Throttle traffic and backlog long-running requests to a worker queue.
4. Once provider restored, slowly ramp traffic and compare CHR/precision to baseline.

---

## Scenario C: Bootstrap deadlock at startup

**Symptoms**

* Pods stuck in CrashLoopBackOff or `Ready` never true; logs show circular dependency or missing migration.

**Steps**

1. Inspect init containers & migration jobs:

   ```bash
   kubectl -n $NS get jobs
   kubectl -n $NS logs job/migrations
   ```
2. Run migrations manually in controlled pod:

   ```bash
   kubectl -n $NS run --rm -it migration-runner --image=myimage -- bash -c "python migrate.py"
   ```
3. Ensure controller component (if any) is up before starting retriever/generator. Use Helm hooks or manual `kubectl apply` ordering.
4. If necessary, scale down and start components one-by-one.

---

## Safety nets & best practices

* Keep automated snapshots of vectorstore daily; keep 7–14 days retention.
* Maintain a tested restore playbook and a “mini-cluster” restore test monthly.
* Automate warm-failover for LLMs: pre-warm API tokens for backup providers.

---

## Post-incident

* Triage root cause, assign fixes.
* Add automated test that would have caught this.
* Update runbooks and notify stakeholders.

---

### Links

* Deployment checklist → [deployment\_checklist.md](./deployment_checklist.md)
* Debug playbook → [debug\_playbook.md](./debug_playbook.md)
* Live monitoring → [live\_monitoring\_rag.md](./live_monitoring_rag.md)

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

