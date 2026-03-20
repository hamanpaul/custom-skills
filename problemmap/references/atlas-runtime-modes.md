# Atlas runtime modes

## Source of truth
- Upstream repo: `WFGY/ProblemMap/Atlas/adapter-runtime-modes-v1.md`

## Modes
- `strict`
  - default mode
  - best for triage, routing discipline, stable classification
- `teaching`
  - use when the operator asks for explanation or boundary teaching
- `repair_preview`
  - use only after the route is stable and a first move preview is requested
- `compact`
  - use in token-constrained or batch settings

## Cross-mode invariants
- route first, then explain, then preview repair
- keep `why_primary_not_secondary`
- keep `broken_invariant`
- keep honest `confidence` and `evidence_sufficiency`
- do not let compact mode silently remove required fields
