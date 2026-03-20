# Tiny Rollback Examples Pack v1

## 0. Document status

This document defines the first tiny rollback example pack for Atlas-based Auto Repair.

Its purpose is simple:

> show a few minimal rollback cases
> so the Auto Repair layer can move from rollback policy rules
> to concrete, inspectable rollback behavior.

This file does **not** claim to be a full rollback benchmark set.

It claims something smaller and more useful:

> the project now has a first set of tiny rollback examples
> for safe early repair actions in F1, F4, and F7.

This document should be read together with:

- `README.md`
- `auto-repair-architecture-v1.md`
- `repair-action-schema-v1.md`
- `repair-validation-loop-v1.md`
- `rollback-policy-v1.md`
- `auto-repair-roadmap-v1.md`
- `repair-planner-spec-v1.md`
- `repair-planner-prompt-v1.md`
- `repair-plan-schema-v1.json`
- `semi-auto-repair-scope-v1.md`
- `safe-early-action-catalog-v1.md`
- `tiny-validation-examples-pack-v1.md`

---

## 1. Why this pack exists

The current Auto Repair layer already defines:

- when rollback should happen
- what rollback should restore
- how rollback relates to validation
- how rollback should connect to revision and escalation

But rules alone are not enough.

Without examples, rollback can still feel abstract.

This pack fills that gap.

It provides a few small examples that show:

- what repair action failed or caused harm
- what rollback target was chosen
- what restore point was used
- what the post-rollback state should look like
- what next step becomes reasonable

In short:

> this pack is the first small evidence layer for rollback behavior.

---

## 2. What these examples are meant to prove

These examples are intentionally small.

They are not meant to prove:

- full rollback automation
- deployment-grade state restoration
- universal rollback correctness across all families

They are meant to prove something narrower:

1. a harmful or misleading repair can be identified
2. a restore point can be named clearly
3. rollback can be described locally and concretely
4. post-rollback state can be summarized
5. the workflow can continue safely after rollback

That is already very valuable.

---

## 3. Pack scope

This v1 pack includes three tiny rollback examples:

- one F1 example
- one F4 example
- one F7 example

These were chosen because they are the best early families for:

- local repair actions
- visible local harm
- clear restore points
- simple rollback explanations

This pack intentionally does **not** include F6-heavy rollback cases.
Those remain too risky and too abstract for early tiny rollback samples.

---

## 4. Standard tiny rollback format

Each tiny rollback example uses the following structure:

1. Example ID
2. Family
3. Failed or harmful repair action
4. Rollback target
5. Rollback reason
6. Restore point
7. Post-rollback state
8. Next step
9. Why rollback is correct
10. Main teaching point

This format is intentionally small and reusable.

---

# Example 1

# F1 Tiny Rollback Example

## Example ID

`TRE_F1_001`

## Family

F1 · Grounding & Evidence Integrity

## Failed or harmful repair action

`F1_AF_001`  
Filter misleading adjacent anchors

## Rollback target

`F1_AF_001`

## Rollback reason

The filtering step removed misleading anchors, but also removed the truly relevant source chunk.

The repair made the evidence set look cleaner, but semantic alignment with the real source became worse.

## Restore point

prior candidate evidence pool

## Post-rollback state

The earlier evidence pool is restored so the system no longer remains trapped in the over-pruned evidence state.

The grounding problem is still unresolved, but the case is no longer worse than before.

## Next step

`retry-with-alternate-action`

## Why rollback is correct

Rollback is correct because the repair damaged the target layer more than it improved it.

The local repair goal was grounding improvement, but the real outcome was harmful over-pruning.

## Main teaching point

A grounding repair should be rolled back if it creates a cleaner-looking but less truthful evidence set.

---

# Example 2

# F4 Tiny Rollback Example

## Example ID

`TRE_F4_001`

## Family

F4 · Execution & Contract Integrity

## Failed or harmful repair action

`F4_GT_001`  
Insert readiness gate

## Rollback target

`F4_GT_001`

## Rollback reason

The new readiness gate blocked the original premature execution, but it also blocked a valid downstream path that should have remained available.

The repair improved closure locally, but overshot the intended scope.

## Restore point

previous workflow gate configuration

## Post-rollback state

The over-restrictive gate is removed and the workflow returns to the earlier configuration.

The system regains the previous valid path, while the closure issue remains available for a narrower future repair.

## Next step

`revise`

## Why rollback is correct

Rollback is correct because the inserted gate created stronger collateral damage than the original local gain.

The target problem was premature execution, not total execution shutdown.

## Main teaching point

A closure repair should be rolled back if it blocks more than the failure it was meant to stop.

---

# Example 3

# F7 Tiny Rollback Example

## Example ID

`TRE_F7_001`

## Family

F7 · Representation & Localization Integrity

## Failed or harmful repair action

`F7_SC_001`  
Tighten output schema

## Rollback target

`F7_SC_001`

## Rollback reason

The schema tightening produced a valid structure, but semantic task fit degraded enough that the output became less useful.

The shell improved, but the content quality dropped too much.

## Restore point

prior schema version

## Post-rollback state

The earlier schema shell is restored so the case no longer remains trapped in a structurally valid but semantically degraded state.

The original representation issue is still present, but the system returns to the less harmful baseline.

## Next step

`re-check family fit`

## Why rollback is correct

Rollback is correct because the repair improved one visible dimension while worsening a more important functional dimension.

The action oversolved structure at the cost of task fidelity.

## Main teaching point

A container repair should be rolled back if structural cleanliness comes at too high a semantic cost.

---

## 5. Optional mixed rollback example

This extra example shows that rollback is not always triggered by catastrophic failure.
Sometimes rollback is the right move because the repair attacked the wrong layer first.

---

# Example 4

# F5 Tiny Rollback Example

## Example ID

`TRE_F5_001`

## Family

F5 · Observability & Diagnosability Integrity

## Failed or harmful repair action

`F5_LU_001`  
Add local logging uplift

## Rollback target

`F5_LU_001`

## Rollback reason

The additional logging exposed more detail, but it made the workflow noisier without improving actual diagnosability.

The repair increased visibility volume without improving failure-path clarity.

## Restore point

pre-observability patch state

## Post-rollback state

The added noisy logging layer is removed and the workflow returns to its prior signal level.

The case still needs observability work, but the system is no longer buried under low-value trace noise.

## Next step

`revise`

## Why rollback is correct

Rollback is correct because the repair improved information quantity but degraded practical diagnosability.

The problem was not only missing visibility.
It was missing useful visibility.

## Main teaching point

An observability repair should be rolled back if it adds noise faster than it adds insight.

---

## 6. What these examples teach

Taken together, these tiny rollback examples teach four important lessons.

### Lesson 1

Rollback is not an embarrassment branch.
It is a normal part of repair discipline.

### Lesson 2

A repair can improve one local feature and still deserve rollback.

### Lesson 3

Rollback depends on restore points being clear.

### Lesson 4

Rollback keeps the system from getting trapped in a worse local state.

---

## 7. Why these examples are useful

These tiny rollback examples are useful for at least four reasons.

### A. Validation support

They make rollback logic concrete after validation detects harm.

### B. Planner support

They teach the planner what kinds of actions are likely to overshoot.

### C. Demo support

They provide simple rollback cases for future repair demos.

### D. Future semi-auto support

They create the first tiny evidence base for safe rollback-aware semi-auto behavior.

---

## 8. What this pack does not yet include

Tiny Rollback Examples Pack v1 does **not** yet include:

- large rollback datasets
- benchmark-scale rollback evaluation
- F6-heavy rollback cases
- multi-step repair-chain rollback
- distributed restore behavior
- automated rollback execution code

Those can come later.

This pack is intentionally minimal.

---

## 9. Recommended next step

Once this pack exists, the next useful follow-up is one of these:

1. create a planner test note that uses both validation and rollback examples
2. create one tiny semi-auto repair demo spec using F1 or F4
3. create a small validator-and-rollback paired example sheet

The strongest immediate next step is probably:

> create a planner test note that shows how the planner, validation, and rollback layers connect on the same small cases.

---

## 10. One-line summary

**Tiny Rollback Examples Pack v1 provides the first small rollback examples for safe early Atlas-based repair actions in F1, F4, F7, and limited F5.**
