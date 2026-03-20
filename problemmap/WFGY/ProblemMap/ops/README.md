# Ops — Deploy & Runbook (Problem Map)

**Purpose:** this folder contains operational runbooks, checklists and playbooks for deploying, observing, debugging and failing-over RAG pipelines and their surrounding infra.  
Target audience: SREs and engineers responsible for production RAG services. Newbie friendly — each section has a checklist and exact commands.

---

## Quick nav
- **Deployment checklist** → [deployment_checklist.md](./deployment_checklist.md)  
- **Live monitoring & alerts (RAG)** → [live_monitoring_rag.md](./live_monitoring_rag.md)  
- **Debug playbook (step-by-step)** → [debug_playbook.md](./debug_playbook.md)  
- **Failover & recovery** → [failover_and_recovery.md](./failover_and_recovery.md)

---

## Scope & assumptions
- Production topology: API gateway → RAG service (retriever + generator + guard) → Vector DB + Source storage.  
- Infra: Kubernetes (Helm) or docker-compose for small envs. Prometheus + Grafana for metrics; centralized logs (ELK/Fluentd/Vector).  
- Safety-first: ops steps favor **read-only** diagnostic commands until root cause is clear.

---

## How to use these runbooks
1. Read the **deployment checklist** before you deploy.  
2. Use **live monitoring** to ensure SLOs after deploy.  
3. If incident happens, follow **debug_playbook** (triage → isolate → mitigate → fix).  
4. If controller/broker or core services fail, follow **failover_and_recovery**.

---

## Quick operator checks (first 60s)
- Is service responding? `curl -fsS http://$SERVICE/healthz || true`  
- Are pods healthy? `kubectl get pods -n $NS`  
- Any obvious error spikes in logs (last 1 minute): `kubectl logs -n $NS -l app=$APP --since=1m | tail -n 200`  
- Check key metrics in Prometheus (latency/p95, error rate, retriever QPS).

---

## Where patterns & examples map here
- If retrieval bad → see `ProblemMap/retrieval-collapse.md` and [examples for vector-store repair](../examples/example_05_vectorstore_repair.md).  
- If bootstrap ordering failures on start → see `ProblemMap/bootstrap-ordering.md` & [pattern_bootstrap_deadlock.md](../patterns/pattern_bootstrap_deadlock.md).  
- For memory/state issues → `ProblemMap/patterns/pattern_memory_desync.md`.

---

> If you want me to also generate ready-to-apply Kubernetes manifests or Prometheus alerts for your environment (Helm values), I can produce them next — tell me cluster flavor (k8s / k3s / kind / docker-compose) and I’ll adapt.

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

