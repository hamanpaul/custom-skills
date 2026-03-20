# Playbook: Agents Triage in 15 Minutes

A fast path to isolate failure layers and route to the right fix.

## Minute 0–3  Measure and log
- Compute ΔS(question, retrieved) and ΔS(retrieved, anchor)
- Record λ on the last three steps
- If ΔS ≥ 0.60 stop and jump to chunking and metric checks

## Minute 3–7  Retrieval checks
- Verify analyzer and metric across write and read
- Sweep k values 5, 10, 20
- If hybrid, enable deterministic rerank
- Open: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

## Minute 7–10  Schema and tools
- Enforce snippet contract and cite-first
- Tighten tool JSON schemas
- Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Minute 10–13  Long chain stability
- Insert BBCR bridge and cap step depth
- Watch λ for flips on paraphrase
- Open: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

## Minute 13–15  Decide and verify
- If metrics improved, rerun with three paraphrases
- If not, rebuild index parameters and re-run gold tests
- Escalate when live flips persist  
  Open: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
