# Auto Repair Roadmap v1

## 0. Document status

This document defines the first formal roadmap for the `auto-repair/` layer.

Its purpose is to make three things explicit:

1. what is already established
2. what should come next
3. what is intentionally delayed

Auto Repair Roadmap v1 does **not** claim that Auto Repair is already fully implemented.

It claims something narrower and more useful:

> the first-stage architecture for Atlas-based repair has been defined,
> and the next build sequence is now clear.

---

## 1. What this roadmap is for

This roadmap exists to connect the current Auto Repair foundation with the next practical build stages.

It should help answer:

- what is already done
- what belongs to Phase 1
- what belongs to later phases
- what should not be rushed
- how Auto Repair grows without breaking Atlas discipline

This roadmap should be read together with:

- `README.md`
- `auto-repair-architecture-v1.md`
- `repair-action-schema-v1.md`
- `repair-validation-loop-v1.md`
- `rollback-policy-v1.md`

Together, those documents define the first foundation layer.

This roadmap defines how that foundation should grow.

---

## 2. Current baseline

At the current stage, Auto Repair has a **first formal planning foundation**, not a full repair engine.

The following are already established:

### A. System positioning
Auto Repair has been defined as the bridge between:

- Atlas diagnosis
- Fix Surface
- deeper WFGY repair

### B. Architecture
The core repair workflow has been defined as:

```text
case
→ atlas routing
→ fix surface
→ repair planner
→ candidate repair action
→ validation loop
→ {accept / revise / rollback / escalate}
````

### C. Repair action schema

The minimum structured unit for repair actions now exists.

### D. Validation logic

The first formal validation loop now exists.

### E. Rollback logic

The first rollback policy now exists.

This means the folder is no longer just an idea.

It is now a real first-stage system foundation.

---

## 3. What is complete in v1 foundation

The following should now be treated as complete enough for first-stage use:

### Complete enough now

* purpose and scope definition
* architecture framing
* repair action schema
* validation loop logic
* rollback policy
* family suitability guidance
* phase-based growth model

### Not complete yet

* repair planner implementation
* executable repair action library
* repair demos
* automated validation runners
* autonomous execution loops
* deployment-grade rollback systems

This is the correct maturity reading:

> the architecture layer is established,
> but execution-layer buildout remains future work.

---

## 4. Roadmap overview

The recommended roadmap is divided into four stages.

### Stage 0

Foundation layer

### Stage 1

Repair planner layer

### Stage 2

Constrained semi-auto repair layer

### Stage 3

Validation-driven repair loop layer

These stages are intentionally sequential.

The system should not jump straight to later-stage automation.

---

## 5. Stage 0

## Foundation layer

### Goal

Create a stable conceptual and structural base for all future Auto Repair work.

### Scope

Stage 0 includes:

* README
* architecture
* repair action schema
* validation loop
* rollback policy
* family suitability notes
* folder growth path

### Why Stage 0 matters

Without this stage:

* repair proposals become vague
* validation becomes inconsistent
* rollback becomes ad hoc
* future automation becomes unsafe

### Stage 0 status

**Established**

This stage should now be treated as the completed foundation of Auto Repair v1.

---

## 6. Stage 1

## Repair planner layer

### Goal

Turn routed diagnosis into a structured repair plan.

### Main question

Given:

* a case
* its routed family
* its broken invariant
* its first repair surface

what are the best candidate repair moves to try first?

### Expected outputs

A first planner should be able to produce:

* selected repair family
* 1 to 3 candidate repair actions
* intended effect of each action
* misrepair risk
* validation target
* escalation recommendation if needed

### Deliverables

Recommended files:

* `repair-planner-spec-v1.md`
* `repair-planner-prompt-v1.md`
* `repair-plan-schema-v1.json`

### Why this stage is the next best move

This stage has high value and controlled risk.

It gives the system practical usefulness without forcing unsafe full execution.

### Recommended first family targets

Start with:

* F1
* F4
* F7

These are the best first targets because they are:

* easier to inspect
* easier to validate
* less risky than high-boundary intervention cases

### Stage 1 success condition

Stage 1 can be considered successful when:

* the planner can consume routed cases
* the planner outputs structured repair plans
* the planner uses action-schema language consistently
* the planner includes misrepair warnings
* the planner does not overclaim full repair closure

---

## 7. Stage 2

## Constrained semi-auto repair layer

### Goal

Allow a limited subset of repair actions to be applied in safer regions.

### Important note

This is **not** the stage for broad autonomous system mutation.

It is the stage for constrained, auditable repair application.

### Safe early action examples

#### F1

* evidence set replacement
* anchor re-check
* retrieval candidate filtering

#### F4

* readiness gate insertion suggestion
* ordering correction suggestion
* block-until-ready rule suggestion

#### F7

* schema tightening
* descriptor correction
* shell repair suggestion

### Deliverables

Recommended files:

* `semi-auto-repair-scope-v1.md`
* `repair-executor-prompt-v1.md`
* `repair-result-schema-v1.json`

### Constraints

Stage 2 should remain:

* local
* inspectable
* reversible
* narrow in scope

It should not claim general autonomous repair.

### Stage 2 success condition

Stage 2 can be considered successful when:

* limited repair actions can be generated or applied
* the scope of action is clearly constrained
* every action remains tied to validation
* rollback remains possible
* no unsafe family overreach is allowed

---

## 8. Stage 3

## Validation-driven repair loop layer

### Goal

Create a repeatable loop where repair is judged by before/after outcomes and can lead to:

* accept
* revise
* rollback
* escalate

### Main requirement

At this stage, validation should no longer be just descriptive.

It should become operational enough to guide repair iteration.

### Deliverables

Recommended files:

* `validation-criteria-catalog-v1.md`
* `repair-loop-state-machine-v1.md`
* `rollback-escalation-matrix-v1.md`

### Why this stage is hard

This is the stage where the system must deal with:

* partial improvement
* collateral damage
* family drift
* confidence uncertainty
* repeatable retry logic

This is the first truly difficult Auto Repair stage.

### Stage 3 success condition

Stage 3 can be considered successful when:

* the loop can distinguish good repair from false success
* rollback is triggered cleanly when needed
* escalation is used when the current repair layer is insufficient
* the system remains stable under repeated repair attempts

---

## 9. What is intentionally delayed

The following are intentionally **not** immediate goals.

### Delayed on purpose

* full autonomous repair across all families
* aggressive F6 auto execution
* benchmark-scale repair automation
* distributed repair coordination
* deep code mutation systems
* universal repair policy engines

These are delayed because they would introduce too much instability too early.

This roadmap is designed for disciplined growth, not premature ambition.

---

## 10. Family priority for future work

### Priority 1

Best first build targets:

* F1
* F4
* F7

### Priority 2

Useful but more cautious:

* F5
* F3

### Priority 3

Planner-first, not execution-first:

* F6

This priority ordering should remain stable unless strong evidence suggests otherwise.

---

## 11. Recommended immediate next files

The next practical files should be:

1. `repair-planner-spec-v1.md`
2. `repair-planner-prompt-v1.md`
3. `repair-plan-schema-v1.json`

These three files would move Auto Repair from:

* architecture-only foundation

to:

* architecture plus first operational planning layer

That is the most valuable next step.

---

## 12. Operational interpretation

The correct operational reading of Auto Repair today is:

> Auto Repair is not yet a full execution engine.
> It is now a structured repair-planning system foundation with a clear staged roadmap toward constrained execution and validation-driven loops.

That statement is accurate, useful, and safe.

---

## 13. Recommended growth order

The healthiest order is:

### Step 1

Complete planner files

### Step 2

Create a small repair action catalog for F1 / F4 / F7

### Step 3

Add limited validation examples

### Step 4

Prototype one or two semi-auto repair demos

### Step 5

Only then consider broader loop integration

This order preserves discipline.

---

## 14. One-line roadmap summary

**Auto Repair Roadmap v1 defines the staged path from architecture and repair planning toward constrained execution, validation-driven iteration, and later deeper repair integration.**
