# Deployment checklist — RAG pipeline (pre-deploy & post-deploy)

**Purpose:** a short, rigorous checklist to verify your environment and reduce bootstrap/dependency issues during deployment.

---

## Before you deploy (pre-flight)

### 1) Environment & prerequisites
- Kubernetes cluster accessible; `kubectl` points to correct context.  
  ```bash
  kubectl config current-context
  kubectl get nodes


* Ensure cluster resources: CPU / memory / ephemeral storage for vectorstore. Confirm quotas.
* Secrets: API keys (LLM), db credentials, vectorstore creds in k8s Secret or vault.
* Helm chart / manifests: reviewed and values set for production (replicas, resources, liveness/readiness).

### 2) Configuration sanity

* `values.yaml` contains:

  * `resources.requests` and `limits` for retriever/generator.
  * `replicaCount >= 2` for critical services (if expected load > small).
  * `readinessProbe` and `livenessProbe` configured.
* Vector store sizing: `index_shards`, disk IOPS, memory (embedding index memory).
* Network egress rules for model API (if external LLM).

### 3) Observability & alarms

* Prometheus scraping configured for app metrics endpoints (`/metrics`).
* Default dashboards in Grafana (latency, error-rate, retriever QPS, CHR).
* Alerts configured (see `live_monitoring_rag.md` for suggested alerts).

---

## Deploy steps

1. Create namespace & secrets:

   ```bash
   kubectl create ns rag-prod || true
   kubectl -n rag-prod apply -f k8s/secrets.yaml
   ```
2. Install/upgrade Helm chart:

   ```bash
   helm upgrade --install rag . -n rag-prod -f values.prod.yaml
   ```
3. Wait for pods to be ready (watch):

   ```bash
   kubectl -n rag-prod rollout status deploy/rag-api -w
   kubectl -n rag-prod get pods -o wide
   ```
4. Smoke tests (simple requests):

   ```bash
   curl -fsS http://<ingress>/healthz
   curl -fsS -X POST http://<ingress>/api/qa -d '{"qid":"smoke-1","q":"Who is the CEO of WFGY?" }' | jq
   ```

---

## Post-deploy checks (first 15 minutes)

* Confirm retriever returns docs for 10 sample queries:

  * Use your `retrieval` debug endpoint to inspect `retrieved_ids`.
* Confirm p95 E2E latency ≤ target (by env). Collect from Grafana or `kubectl logs`.
* Confirm CHR on 10 smoke items ≥ expected baseline (manually assert correctness).
* Check for error spikes in logs:

  ```bash
  kubectl -n rag-prod logs -l app=rag --since=10m | egrep "ERROR|WARN" | head -n 200
  ```

---

## Common config gotchas (double-check)

* Vectorstore read-only mode accidentally set? (affects writes)
* LLM rate-limiting / auth errors (wrong key or quota).
* Wrong index/namespace names between chunker and retriever (off-by-one).
* Probes misconfigured — containers get restarted continuously.

---

## Rollback criteria

Rollback if any of:

* P95 > target and sustained for 10m.
* Error rate > 3× baseline and not transient.
* Retrieval failures (empty pool) > 1% of requests.

Rollback command example:

```bash
helm rollback rag <previous_revision> -n rag-prod
```

---

### Quick checklist (copy/paste)

* [ ] Namespace created, secrets applied
* [ ] Helm values validated (resources, probes)
* [ ] Prometheus/Grafana dashboards in place
* [ ] Smoke tests passed (health & basic QA)
* [ ] Alerts deployed
* [ ] Canary traffic small → monitor 10–30 min

---

### Links

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

