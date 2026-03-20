# Pattern: Memory Namespace Split

**Problem**  
Agents overwrite or re-assert stale facts after refresh. Different tools write to the same memory without fences.

**When to use**  
Any multi-agent or tool-rich pipeline where memories persist across runs or threads.

**Recipe**
1) Create namespaces per role or tool: `agent/<name>`, `tool/<name>`, `session/<id>`.
2) Stamp every write with `mem_rev` and `mem_hash`.
3) Read policy: prefer `session` then `agent` then `tool`.
4) Write policy: do not merge across namespaces without a reducer function.
5) Gate responses when `mem_rev` is older than the current `index_hash` snapshot.

**Acceptance**
- No stale fact re-entry in three paraphrase tests.
- λ stays convergent before and after memory refresh.

**Related fixes**
- [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)  
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
