# Planner Review Checklist v1

## 0. Document status

This document defines the first compact review checklist for the Atlas Auto Repair planner layer.

Its purpose is simple:

> provide a short, reusable review sheet
> for checking whether a repair planner output is disciplined enough
> for first-stage Atlas-based repair planning.

This file does **not** define a benchmark.
It defines a practical review checklist.

It should be read together with:

- `repair-planner-spec-v1.md`
- `repair-planner-prompt-v1.md`
- `repair-plan-schema-v1.json`
- `planner-test-note-v1.md`
- `repair-validation-loop-v1.md`
- `rollback-policy-v1.md`

---

## 1. What this checklist is for

This checklist is used to review whether a planner output is behaving correctly in v1.

It is meant for:

- manual planner review
- prompt iteration
- small internal tests
- demo review
- future planner quality control

It is **not** meant to judge whether the whole case is already solved.

It is only meant to judge whether the planner produced a good **first repair plan**.

---

## 2. Core review principle

A good planner output should be:

- family-aligned
- conservative
- local
- validation-aware
- misrepair-aware
- escalation-capable

A bad planner output usually becomes:

- too broad
- too confident
- too vague
- too action-heavy
- too weak on validation
- too weak on rollback awareness

This checklist is designed to catch those failures early.

---

## 3. How to use this checklist

Review the planner output item by item.

For each row, use one of these verdicts:

- `pass`
- `partial`
- `fail`

If a planner output has multiple `fail` items in core areas, it should not be treated as strong planner behavior.

Core areas include:

- family alignment
- action quality
- validation target
- misrepair awareness
- scope discipline

---

## 4. Checklist

| No. | Review Item | What to check | Verdict |
|---|---|---|---|
| 1 | Family alignment | Does the selected repair family stay aligned with the routed case? | pass / partial / fail |
| 2 | Neighbor discipline | Does the planner avoid jumping too early into a neighboring repair family? | pass / partial / fail |
| 3 | Action count discipline | Does the planner propose only 1 to 3 candidate actions? | pass / partial / fail |
| 4 | Action locality | Are the actions small enough to validate locally? | pass / partial / fail |
| 5 | Action plausibility | Do the actions make sense for the routed family and fix surface? | pass / partial / fail |
| 6 | Scope discipline | Is the chosen `plan_scope` appropriate for the case risk level? | pass / partial / fail |
| 7 | Validation target clarity | Does the planner name a real first validation target? | pass / partial / fail |
| 8 | Misrepair awareness | Does the planner name a realistic main misrepair risk? | pass / partial / fail |
| 9 | Escalation discipline | Does the planner escalate or narrow scope when evidence is weak? | pass / partial / fail |
| 10 | Confidence discipline | Is planner confidence consistent with routing quality and evidence sufficiency? | pass / partial / fail |
| 11 | Anti-fantasy discipline | Does the planner avoid pretending to solve the whole case at once? | pass / partial / fail |
| 12 | Operational usefulness | Does the output provide a usable next step such as validate, revise, rollback, or escalate? | pass / partial / fail |

---

## 5. Review item notes

### 1. Family alignment

A good planner should remain anchored to the routed family unless there is explicit routing uncertainty.

Common failure:

- planner drifts into a neighboring family without sufficient reason

---

### 2. Neighbor discipline

A good planner should understand neighboring pressure without letting that pressure hijack the first repair move.

Common failure:

- F1 case turns into F7-first repair too early
- F4 case turns into F3-first repair too early
- F5 case turns into F6 intervention too early

---

### 3. Action count discipline

A good v1 planner should not spray many actions.

Expected range:

- 1 to 3 actions

Common failure:

- 5 or more actions
- mixed action bag with no real first move

---

### 4. Action locality

A good planner should choose actions that are local and inspectable.

Common failure:

- broad system mutation
- vague “improve everything” repair language
- multi-step chain without checkpoints

---

### 5. Action plausibility

A good planner should propose actions that actually match the routed family and fix surface.

Common failure:

- schema tightening on a grounding-first case
- reasoning pressure on an execution-first case
- visibility uplift presented as if it were full repair

---

### 6. Scope discipline

A good planner should choose a plan scope that matches case risk.

Examples:

- `minimal` for simple F1 grounding repair
- `constrained` for local F4 or F7 repair
- `planner-only` or `requires-review` for risky F6-heavy cases

Common failure:

- broad scope under weak evidence

---

### 7. Validation target clarity

A good planner must name the first thing that should be checked after the first action.

Examples:

- anchor alignment
- readiness state
- schema validity
- failure-path visibility

Common failure:

- no validation target
- vague validation like “check if better”

---

### 8. Misrepair awareness

A good planner should identify the most likely wrong repair path.

Common failure:

- no misrepair note at all
- generic warning that teaches nothing
- missing obvious neighbor-family trap

---

### 9. Escalation discipline

A good planner should know when not to force a repair plan.

Common failure:

- planner keeps proposing aggressive actions under high ambiguity
- planner avoids escalation even when the case is weakly defined

---

### 10. Confidence discipline

A good planner should not sound more certain than the evidence allows.

Common failure:

- `high` planner confidence on weak routing
- strong claims in boundary-heavy cases

---

### 11. Anti-fantasy discipline

A good planner should plan the first move, not a heroic total cure.

Common failure:

- repair story instead of repair plan
- pretending full closure from one local action

---

### 12. Operational usefulness

A good planner output should help the next layer act.

Common failure:

- output is conceptually interesting but operationally useless
- no clear next step

---

## 6. Quick scoring suggestion

A lightweight scoring approach for internal review:

- `pass` = 2
- `partial` = 1
- `fail` = 0

Suggested rough reading:

- `20 to 24` = strong v1 planner output
- `14 to 19` = usable but needs refinement
- `0 to 13` = weak planner output

This is only a rough internal guide.
It is not a public benchmark claim.

---

## 7. High-priority fail conditions

Even if the total score is not terrible, the planner should still be treated as weak if it fails in one or more of these core areas:

- family alignment
- action plausibility
- validation target clarity
- misrepair awareness
- escalation discipline

These are the most important v1 planner review items.

---

## 8. Short review template

Use this compact template for fast review:

```text
Planner Review Summary

Case ID:
Primary family:
Planner verdict:

1. Family alignment:
2. Action count discipline:
3. Action plausibility:
4. Scope discipline:
5. Validation target clarity:
6. Misrepair awareness:
7. Escalation discipline:
8. Overall usability:

Final reading:
- strong
- usable with revision
- weak
````

---

## 9. Example quick review

### Example

Case type:
F4 premature execution case

Planner output summary:

* selected repair family = F4
* 2 actions
* readiness gate first
* validation target = readiness state
* misrepair risk = blocking valid downstream progress
* next step = validate-first-action

Review:

* family alignment = pass
* action count discipline = pass
* action plausibility = pass
* scope discipline = pass
* validation target clarity = pass
* misrepair awareness = pass
* escalation discipline = partial
* overall usability = strong

This is the kind of compact review the checklist is meant to support.

---

## 10. What this checklist does not yet include

Planner Review Checklist v1 does **not** yet include:

* automated grader logic
* model-to-model planner comparison
* weighted benchmark scoring
* family-specific scoring matrices
* longitudinal planner tracking

Those can come later.

For now, the point is to make planner review fast, structured, and reusable.

---

## 11. Recommended next step

Once this checklist exists, the next useful follow-up is probably:

* `tiny-planner-output-examples-pack-v1.md`

That would pair well with:

* planner test note
* planner review checklist

and give the planner layer a stronger small evidence set.

---

## 12. One-line summary

**Planner Review Checklist v1 provides a compact way to judge whether the Atlas Auto Repair planner is family-aligned, conservative, validation-aware, and operationally useful.**
