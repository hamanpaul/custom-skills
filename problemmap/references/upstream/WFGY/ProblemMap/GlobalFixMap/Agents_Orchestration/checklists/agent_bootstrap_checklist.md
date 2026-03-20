# Agent Bootstrap Checklist

Print this before the first live run. Fail fast if any item is missing.

## Readiness
- `INDEX_HASH` stored and matches the live store
- `VECTOR_READY == true` and analyzer name recorded
- All secrets present and scoped
- Tool registry frozen and versioned
- `assistant_id` or framework agent id pinned

## Schema and safety
- Snippet contract required: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`
- Cite first then explain enforced in prompts
- Tool JSON schemas strict and echoed on each call
- Redaction prefilter enabled for uploads and captures

## Observability
- Log ΔS(question, retrieved), ΔS(retrieved, anchor), λ state
- Store `mem_rev`, `mem_hash`, `dedupe_key`
- Alerts when ΔS ≥ 0.60 or λ divergent

## Idempotency and order
- Idempotency key defined for side effects
- Single writer or queue selected for shared stores
- Deploy order verified per [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

## Exit gates
- Coverage ≥ 0.70 on three paraphrases
- λ convergent on two seeds
- Rollback path documented with BBCR bridge
