# ProblemMap drift guard

The ProblemMap drift guard is a **manager-side check** for keeping worker agents on track without guessing at the repair.

## Why it exists

When a worker goes sideways, the first visible symptom is often noisy:

- repeated clarification questions
- stalled progress updates
- a failure that looks like "tool broke" but is really continuity loss
- a result that is technically polished but targets the wrong thing

Blindly retrying with a louder prompt can make this worse. The guard turns the current task trail into a small ProblemMap case, then diagnoses the route before the manager intervenes.

## Inputs

`scripts/problemmap-guard.py` reads:

- `runtime/context/context.jsonl`
- a target `task_id`
- a target `worker_id`
- an optional manager-side expected goal override

## Output files

By default the helper writes under:

```text
runtime/artifacts/problemmap/<task-id>/<worker-id>/
  case.json
  diagnosis.json
  event.json
```

## Suggested trigger rules

Run the guard when:

1. the same worker sends 2+ `ASK` messages on one task
2. the worker sends 3+ `STATUS` messages without converging
3. the worker emits `FAIL`
4. the worker returns a `RESULT` with weak overlap against the manager's expected goal

## Heuristic signals

The helper derives ProblemMap-friendly signals from the context trail, including:

- `event:misunderstood_request`
- `event:wrong_approach`
- `event:context_compacted`
- `event:turn_aborted`
- `event:buggy_code`
- `event:excessive_changes`
- `nonzero-exit-code`

## How the manager should use the diagnosis

Do **not** treat the output as a worker-visible scolding note. It is a manager control aid.

Typical reactions:

- **F2 Reasoning & Progression**: narrow the goal, reduce decomposition width, checkpoint the next step.
- **F3 State & Continuity**: replay the sanitized context, restore task boundaries, reset ownership assumptions.
- **F4 Execution & Contract**: check runtime/tool readiness, protocol closure, and pane transport before changing prompts.
- **F6 Boundary & Safety**: tighten scope, forbid unrelated edits, and re-ground on artifacts or paths.

## Example

```bash
python3 smux-manager-skill/scripts/problemmap-guard.py \
  /tmp/smux-manager-demo task-123 codex \
  --expected "Investigate failing auth tests under tests/ and src/auth.ts"
```

After reading `diagnosis.json`, mirror only the **manager decision** back into the shared context, not the worker's hidden reasoning.
