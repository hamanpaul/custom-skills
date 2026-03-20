# Safe Early Action Catalog v1

## 0. Document status

This document defines the first small catalog of **safe early repair actions** for Atlas-based Auto Repair.

Its purpose is practical:

> before building broader semi-auto repair behavior,
> define a small set of actions that are local, inspectable, reversible, and validation-friendly.

This document does **not** claim that the full repair library already exists.

It claims something narrower and more useful:

> the project now has a first controlled catalog of early repair actions
> that are suitable for planning, validation, demos, and later constrained semi-auto use.

This file should be read together with:

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

---

## 1. Why this catalog exists

The current Auto Repair layer already has:

- architecture
- repair action schema
- validation logic
- rollback logic
- planner logic
- semi-auto scope discipline

But without a small action catalog, the system still lacks a practical middle layer between:

- abstract repair planning
and
- actual candidate repair moves

This catalog fills that gap.

It gives the system a first set of repair actions that are:

- simple enough to inspect
- small enough to validate
- narrow enough to rollback
- stable enough for demos and future constrained execution

In short:

> this is the first usable action shelf for Auto Repair.

---

## 2. Design rule for v1 catalog

This catalog only includes actions that satisfy the early safety rule:

> local, inspectable, reversible, and validation-ready

That means the catalog intentionally prioritizes:

- F1
- F4
- F7

These are the best early families for safe, auditable repair action design.

This catalog does **not** yet aim to cover all families equally.

That is intentional.

---

## 3. Catalog structure

Each action entry in this file follows the same compact structure:

1. Action ID
2. Action Title
3. Target Family
4. Target Region
5. Repair Type
6. Intended Effect
7. Allowed Scope
8. Validation Target
9. Rollback Hint
10. Typical Use Case
11. Main Misrepair Risk
12. When Not To Use

This is a practical catalog format, not a full schema file.

The full schema contract still lives in:

- `repair-action-schema-v1.md`
- `repair-plan-schema-v1.json`

---

# Part I

# F1 Safe Early Actions

These actions target **Grounding & Evidence Integrity**.

They are usually good early candidates because they are concrete and comparatively easy to inspect.

---

## F1 Action 1

### Action ID
`F1_RG_001`

### Action Title
Re-ground evidence set

### Target Family
F1

### Target Region
F1_N01 Retrieval Anchor Drift

### Repair Type
re-grounding

### Intended Effect
Restore evidence-anchor alignment by replacing the current evidence set with a better-aligned one.

### Allowed Scope
minimal

### Validation Target
anchor alignment

### Rollback Hint
restore prior evidence set

### Typical Use Case
The current answer appears to rely on semantically adjacent but incorrect source chunks.

### Main Misrepair Risk
The repair may hide a deeper representation issue if the real problem is not anchor drift.

### When Not To Use
Do not use as the first move if the main problem is clearly malformed structure or broken container fidelity.

---

## F1 Action 2

### Action ID
`F1_AF_001`

### Action Title
Filter misleading adjacent anchors

### Target Family
F1

### Target Region
F1_N02 Semantic Grounding Mismatch

### Repair Type
anchor filtering

### Intended Effect
Remove candidate evidence that is semantically close but misaligned with the true task target.

### Allowed Scope
minimal

### Validation Target
semantic target fit

### Rollback Hint
restore prior candidate evidence pool

### Typical Use Case
The system keeps choosing near-match references that sound plausible but are not actually target-correct.

### Main Misrepair Risk
The repair may over-prune and remove useful evidence.

### When Not To Use
Do not use when the real issue is missing evidence rather than misleading evidence.

---

## F1 Action 3

### Action ID
`F1_SR_001`

### Action Title
Force source-target recheck

### Target Family
F1

### Target Region
F1_E02 OOD World Grounding Failure

### Repair Type
anchor re-check

### Intended Effect
Require an explicit source-to-target verification step before accepting the current grounding.

### Allowed Scope
constrained

### Validation Target
source match

### Rollback Hint
remove added recheck step

### Typical Use Case
The system appears to answer with decent fluency, but the output is not reliably tied to the correct source target.

### Main Misrepair Risk
The repair may create extra checking without improving true grounding.

### When Not To Use
Do not use if the case has no inspectable source target.

---

# Part II

# F4 Safe Early Actions

These actions target **Execution & Contract Integrity**.

They are strong early candidates because the repair region is often workflow-visible.

---

## F4 Action 1

### Action ID
`F4_GT_001`

### Action Title
Insert readiness gate

### Target Family
F4

### Target Region
F4_N03 Pre-Readiness Execution Failure

### Repair Type
gate insertion

### Intended Effect
Prevent downstream execution from starting before upstream readiness conditions are satisfied.

### Allowed Scope
constrained

### Validation Target
readiness state

### Rollback Hint
remove inserted gate

### Typical Use Case
A step is executing too early because the system treats draft availability as if it were true readiness.

### Main Misrepair Risk
The repair may block valid flow if the gate condition is too broad.

### When Not To Use
Do not use if the real problem is continuity drift rather than closure breakdown.

---

## F4 Action 2

### Action ID
`F4_OC_001`

### Action Title
Correct downstream ordering

### Target Family
F4

### Target Region
F4_N01 Bootstrap Ordering Failure

### Repair Type
ordering correction

### Intended Effect
Restore the correct order of operations so later steps only run after prerequisite steps finish.

### Allowed Scope
constrained

### Validation Target
ordering correctness

### Rollback Hint
restore previous step ordering

### Typical Use Case
A pipeline is failing because one module is consuming incomplete or not-yet-approved upstream outputs.

### Main Misrepair Risk
The repair may reorder visible steps while leaving hidden dependency problems untouched.

### When Not To Use
Do not use if the problem is actually missing observability rather than wrong ordering.

---

## F4 Action 3

### Action ID
`F4_CL_001`

### Action Title
Harden local closure rule

### Target Family
F4

### Target Region
F4_E01 Institutional Enforcement Drift

### Repair Type
closure hardening

### Intended Effect
Strengthen a local closure condition so rule-to-action execution cannot bypass required checks.

### Allowed Scope
requires-review

### Validation Target
closure path stability

### Rollback Hint
restore prior closure rule

### Typical Use Case
A process nominally has a policy or rule, but execution keeps slipping through incomplete enforcement paths.

### Main Misrepair Risk
The repair may produce a stricter-looking closure rule that reduces usability without fixing the underlying enforcement gap.

### When Not To Use
Do not use as an automatic first move in high-ambiguity institutional or boundary-heavy cases.

---

# Part III

# F7 Safe Early Actions

These actions target **Representation & Localization Integrity**.

They are good early targets because the repaired region is often visible in the output container itself.

---

## F7 Action 1

### Action ID
`F7_SC_001`

### Action Title
Tighten output schema

### Target Family
F7

### Target Region
F7_N01 Symbolic Representation Fidelity Failure

### Repair Type
schema tightening

### Intended Effect
Restore valid container structure by explicitly enforcing a tighter schema shell.

### Allowed Scope
constrained

### Validation Target
schema validity

### Rollback Hint
revert schema constraint

### Typical Use Case
The content is partially right, but the output breaks the required structured format.

### Main Misrepair Risk
The repair may improve container validity while silently reducing semantic fit.

### When Not To Use
Do not use before checking whether the real issue is grounding rather than container structure.

---

## F7 Action 2

### Action ID
`F7_DR_001`

### Action Title
Repair descriptor shell

### Target Family
F7

### Target Region
F7_N01_A Logic Descriptor Fidelity Failure

### Repair Type
descriptor correction

### Intended Effect
Make the formal or symbolic descriptor more faithful to the intended reasoning structure.

### Allowed Scope
constrained

### Validation Target
descriptor fidelity

### Rollback Hint
restore prior descriptor wording

### Typical Use Case
The system output keeps drifting because the formal container describing the task is underspecified or structurally weak.

### Main Misrepair Risk
The repair may over-specify the descriptor and force unnatural output behavior.

### When Not To Use
Do not use if the container is already stable and the true problem is progression-first.

---

## F7 Action 3

### Action ID
`F7_SH_001`

### Action Title
Restore shell boundary

### Target Family
F7

### Target Region
F7_E01 Explanation Fidelity Distortion

### Repair Type
shell correction

### Intended Effect
Repair broken object / array / field boundary so the output shell can hold the intended content correctly.

### Allowed Scope
minimal

### Validation Target
shell integrity

### Rollback Hint
restore prior shell version

### Typical Use Case
The answer content exists, but the structure leaks across fields or breaks object boundaries.

### Main Misrepair Risk
The repair may produce a cleaner shell that still carries the wrong content.

### When Not To Use
Do not use if the shell is valid and the deeper issue is evidence or logic drift.

---

# Part IV

# F5 Limited Early Actions

These actions are included with extra caution.

They are useful, but should mostly remain in suggest-only or narrow apply-and-check mode.

---

## F5 Action 1

### Action ID
`F5_TE_001`

### Action Title
Insert trace exposure point

### Target Family
F5

### Target Region
F5_N01 Failure Path Opacity

### Repair Type
trace exposure

### Intended Effect
Expose one previously hidden step or path so the failure becomes more diagnosable.

### Allowed Scope
minimal

### Validation Target
failure-path visibility

### Rollback Hint
remove added trace point

### Typical Use Case
A workflow is failing, but the hidden transition point cannot currently be inspected.

### Main Misrepair Risk
The repair may add more visible output without making the true bottleneck easier to identify.

### When Not To Use
Do not use if the workflow already has enough visibility and the real problem is execution or boundary failure.

---

## F5 Action 2

### Action ID
`F5_LU_001`

### Action Title
Add local logging uplift

### Target Family
F5

### Target Region
F5_E02 Early Warning Deficit

### Repair Type
logging uplift

### Intended Effect
Increase the observability of a narrow failure region by adding a focused local logging layer.

### Allowed Scope
constrained

### Validation Target
probe usefulness

### Rollback Hint
remove noisy logging layer

### Typical Use Case
The system needs one additional logging or probe layer to identify a pre-failure transition.

### Main Misrepair Risk
The repair may increase noise and reduce practical diagnosability.

### When Not To Use
Do not use as a blanket instrumentation move across the whole system.

---

# Part V

# Catalog use rules

This catalog should be used under the following rules.

## Rule 1
Prefer one action first.

Do not start by throwing multiple categories of repair at the case.

## Rule 2
Validate after each local action.

Do not assume that a seemingly reasonable repair already helped.

## Rule 3
Rollback must stay possible.

If rollback is unclear, the action should not be treated as safe early action.

## Rule 4
Do not treat this catalog as a full repair library.

This is an **early action catalog**, not the final repair universe.

## Rule 5
Use caution near family boundaries.

Especially:

- F1 / F7
- F3 / F4
- F5 / F6

The planner should remain conservative in these regions.

---

# Part VI

# What this catalog does not yet include

Safe Early Action Catalog v1 does **not** yet include:

- large multi-step repair chains
- high-risk F6 intervention actions
- deep continuity mutation actions
- broad workflow redesign actions
- autonomous cross-family repair bundles
- optimizer scoring over action sets

Those belong to later phases, not this v1 catalog.

---

# Part VII

# Recommended next step

Once this catalog exists, the next logical move is one of these:

1. create a small validator example pack for these actions
2. create a small demo spec for one F1, one F4, and one F7 semi-auto action
3. create a planner test note showing how these actions are selected

The strongest immediate next step is probably:

> turn 2 or 3 of these actions into tiny repair planner examples and tiny validation examples.

That would make the catalog feel operational very quickly.

---

## One-line summary

**Safe Early Action Catalog v1 defines the first controlled set of local, inspectable, reversible, and validation-ready repair actions for Atlas-based Auto Repair.**
