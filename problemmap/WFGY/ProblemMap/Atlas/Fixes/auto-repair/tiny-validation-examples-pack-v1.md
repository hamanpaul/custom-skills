# Tiny Validation Examples Pack v1

## 0. Document status

This document defines the first tiny validation example pack for Atlas-based Auto Repair.

Its purpose is simple:

> show a few minimal before/after validation examples
> so the Auto Repair layer can move from abstract rules
> to concrete, inspectable validation behavior.

This file does **not** claim to be a full benchmark set.

It claims something smaller and more useful:

> the project now has a first set of tiny validation examples
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

---

## 1. Why this pack exists

The current Auto Repair layer already has:

- architecture
- action schema
- planner logic
- validation logic
- rollback logic
- scope discipline
- safe early action catalog

But without concrete examples, those layers can still feel too abstract.

This pack fills that gap.

It provides a few small examples that show:

- what action was selected
- what was validated
- what changed before and after
- what verdict was reached
- why the verdict makes sense

In short:

> this pack is the first small evidence layer for Auto Repair validation.

---

## 2. What these examples are meant to prove

These examples are intentionally small.

They are not meant to prove:

- full autonomous repair
- full benchmark performance
- universal repair correctness

They are meant to prove something narrower:

1. a small repair action can be selected cleanly
2. a clear validation target can be named
3. before/after states can be compared
4. the system can produce a usable verdict
5. the repair logic can be explained without ambiguity

That is already very valuable.

---

## 3. Pack scope

This v1 pack includes three tiny examples:

- one F1 example
- one F4 example
- one F7 example

These were chosen because they are the best early families for:

- local actions
- visible changes
- simple validation targets
- reversible repair moves

This pack intentionally does **not** include F6-heavy examples.
Those remain too risky for early tiny validation samples.

---

## 4. Standard tiny example format

Each tiny validation example uses the following structure:

1. Example ID
2. Family
3. Target action
4. Validation target
5. Before state
6. After state
7. Validation verdict
8. Why this verdict is correct
9. Main teaching point

This format is intentionally small and reusable.

---

# Example 1

# F1 Tiny Validation Example

## Example ID

`TVE_F1_001`

## Family

F1 · Grounding & Evidence Integrity

## Target action

`F1_RG_001`  
Re-ground evidence set

## Validation target

anchor alignment

## Before state

The answer is fluent and plausible, but it is grounded in a semantically adjacent source chunk rather than the intended source.

The local failure looks like:

- evidence is nearby
- wording looks reasonable
- source alignment is wrong

## After state

The evidence set is replaced with a better-aligned source group.

The answer is now tied to the intended source target.

The local state now looks like:

- evidence anchor is corrected
- source alignment improves
- answer is more tightly attached to the right support

## Validation verdict

`accept`

## Why this verdict is correct

The target invariant improved:

- evidence-anchor integrity is stronger
- no meaningful collateral damage is visible
- the action remained local and reversible

## Main teaching point

A grounding repair should be judged by **anchor alignment**, not by style or fluency alone.

---

# Example 2

# F4 Tiny Validation Example

## Example ID

`TVE_F4_001`

## Family

F4 · Execution & Contract Integrity

## Target action

`F4_GT_001`  
Insert readiness gate

## Validation target

readiness state

## Before state

A downstream action is available and is executed before upstream readiness is complete.

The local failure looks like:

- a draft exists
- approval is incomplete
- execution still moves forward

## After state

A local readiness gate is inserted.

The downstream step is now blocked until upstream readiness is satisfied.

The local state now looks like:

- execution no longer starts too early
- the workflow respects readiness order
- closure becomes more stable

## Validation verdict

`accept`

## Why this verdict is correct

The target invariant improved:

- closure integrity is stronger
- premature execution is prevented
- rollback remains clear because the gate can be removed if needed

## Main teaching point

Execution repair should be judged by **closure correctness**, not by whether the system appears more active.

---

# Example 3

# F7 Tiny Validation Example

## Example ID

`TVE_F7_001`

## Family

F7 · Representation & Localization Integrity

## Target action

`F7_SC_001`  
Tighten output schema

## Validation target

schema validity

## Before state

The content is partly correct, but the structured shell is broken.

The local failure looks like:

- field boundaries leak
- object shape is invalid
- output cannot be reliably consumed downstream

## After state

The schema shell is tightened and the output boundary is restored.

The local state now looks like:

- structure is valid
- field boundaries hold
- downstream consumption becomes possible

## Validation verdict

`accept`

## Why this verdict is correct

The target invariant improved:

- container fidelity is stronger
- the repaired structure is clearly more usable
- the change is inspectable and reversible

## Main teaching point

A container repair should be judged by **structural validity**, not by content plausibility alone.

---

## 5. Optional partial or revise-style example

The pack should also show that not every repair becomes an immediate accept.

This small example is useful for teaching cautious validation.

---

# Example 4

# F7 Partial Validation Example

## Example ID

`TVE_F7_002`

## Family

F7 · Representation & Localization Integrity

## Target action

`F7_DR_001`  
Repair descriptor shell

## Validation target

descriptor fidelity

## Before state

The output task descriptor is weak and under-specified.

This causes unstable structured output.

## After state

The descriptor becomes stricter and the structure becomes cleaner.

However, the semantic fit to the original task appears weaker.

## Validation verdict

`revise`

## Why this verdict is correct

The repair improved one dimension:

- descriptor structure became cleaner

But it also introduced possible collateral damage:

- semantic fit may have weakened

So the right early verdict is not full accept.

It is revise.

## Main teaching point

A cleaner container is not always a fully successful repair if semantic fit drops.

---

## 6. What these examples teach

Taken together, these tiny examples teach four important lessons.

### Lesson 1

A repair should be judged against its declared validation target.

### Lesson 2

A local improvement can be strong enough for `accept`.

### Lesson 3

A mixed result should often become `revise`, not forced success.

### Lesson 4

Validation is what turns repair from intuition into disciplined workflow.

---

## 7. Why these examples are useful

These tiny examples are useful for at least four reasons.

### A. Planner support

They help test whether a repair planner is choosing actions that can actually be validated.

### B. Validation support

They show what before/after validation is supposed to look like.

### C. Demo support

They are small enough to reuse in future repair demos.

### D. Future semi-auto support

They provide the first tiny evidence base for safe early semi-auto repair behavior.

---

## 8. What this pack does not yet include

Tiny Validation Examples Pack v1 does **not** yet include:

- large validation datasets
- cross-family repair chains
- F6-heavy intervention examples
- benchmark-scale scoring
- automated validator code
- rollback case examples as a separate pack

Those can come later.

This pack is intentionally minimal.

---

## 9. Recommended next step

Once this pack exists, the next useful follow-up is one of these:

1. create a tiny rollback examples pack
2. create a planner test note using these examples
3. create one tiny semi-auto demo spec that consumes these examples

The strongest immediate next step is probably:

> create a tiny rollback examples pack

because validation and rollback naturally belong close together.

---

## 10. One-line summary

**Tiny Validation Examples Pack v1 provides the first small before/after validation examples for safe early Atlas-based repair actions in F1, F4, and F7.**
