# Semi-Auto Repair Scope v1

## 0. Document status

This document defines the first formal scope boundary for **semi-auto repair** inside the Atlas Auto Repair layer.

Its purpose is to answer one practical question:

> which repair actions are safe enough to be partially automated in early phases,
> and which repair actions should remain planner-only, review-bound, or explicitly delayed?

This document does **not** claim that broad autonomous repair is already available.

It defines something narrower and safer:

> the first controlled scope for limited, auditable, reversible semi-auto repair.

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

---

## 1. What semi-auto repair means here

Semi-auto repair does **not** mean unrestricted self-directed repair.

It means:

> the system may generate, apply, or suggest a narrowly bounded repair action
> when the action is local, inspectable, reversible, and validation-ready.

This is an intentionally limited concept.

The system is allowed to help with a repair action only when:

- the case has already been routed
- the repair family is clear enough
- the action is small enough to validate
- the rollback path is explicit
- the risk is low enough for controlled trial

So semi-auto repair sits between:

- repair planning only

and

- fully autonomous repair execution

It is a middle layer.

---

## 2. Why this scope document is needed

Without a scope boundary, Auto Repair would drift too quickly into unsafe territory.

Some repair actions are naturally suited to early semi-auto use.

Others are not.

For example:

- replacing an evidence subset may be reasonable
- inserting a readiness gate suggestion may be reasonable
- tightening a broken output schema may be reasonable

But:

- making high-impact boundary interventions
- mutating broad workflow logic under uncertainty
- applying strong legitimacy or policy changes
- performing deep repair on ambiguous multi-family cases

should not be treated as early semi-auto operations.

So this document exists to keep growth disciplined.

---

## 3. Core scope principle

The scope rule is simple:

> only actions that are local, inspectable, reversible, and validation-ready
> may enter early semi-auto repair.

If an action fails one or more of those tests, it should remain:

- planner-only
- review-bound
- escalation-only
- or future-stage work

This is the main protective rule for v1.

---

## 4. Semi-auto repair tiers

Semi-auto repair should be understood in three operational tiers.

### Tier 1 · Suggest-only

The system proposes a repair action, but does not apply it automatically.

This is the safest tier.

Typical use:

- high-risk family pressure
- ambiguous cases
- human-in-the-loop workflows
- early repair demos

### Tier 2 · Controlled apply-and-check

The system applies a small local action in a tightly bounded context and immediately checks the result.

This is the main target tier for early semi-auto repair.

Typical use:

- swap evidence set
- add a readiness gate in a toy workflow
- tighten a schema in a replayable output shell

### Tier 3 · Bounded iterative repair

The system may try a small action, validate, and either keep, revise, or rollback under strict local limits.

This tier is possible later, but should not be rushed.

It requires stronger validation and rollback discipline.

---

## 5. What qualifies as in-scope for v1

A repair action is in scope for early semi-auto use when all of the following are true.

### Condition 1 · Routed case exists

The case must already have:

- primary family
- broken invariant
- best current fit
- fix surface direction
- usable confidence and evidence status

No semi-auto repair should happen on an unrouted or weakly defined case.

### Condition 2 · Action is local

The action must target a narrow region.

Examples:

- evidence set
- output schema
- readiness gate
- trace insertion point
- descriptor shell

The action must not require broad undefined system mutation.

### Condition 3 · Action is inspectable

The before/after difference must be understandable.

If nobody can tell what changed, the action is too loose for early semi-auto use.

### Condition 4 · Action is reversible

A restore point or rollback path must be available.

If the system cannot explain how to back out, the action is not ready.

### Condition 5 · Validation target is explicit

The planner must be able to name the first validation target.

Examples:

- anchor alignment
- readiness state
- schema validity
- trace usefulness

If the validation target is vague, the action is too immature.

---

## 6. Best early family targets

Not all families are equally suitable for early semi-auto work.

### F1 · Grounding & Evidence Integrity

This is one of the best early targets.

Why:

- actions are often concrete
- validation is easier
- rollback is usually manageable
- local scope is often clear

Good early examples:

- replace wrong evidence subset with a corrected evidence subset
- filter semantically adjacent but misleading anchors
- force re-check against a declared source target
- narrow retrieval candidates for a replayable case

Good early validation targets:

- anchor alignment
- source match
- semantic target fit

Good early rollback targets:

- restore previous evidence selection
- restore previous candidate set

---

### F4 · Execution & Contract Integrity

This is also a strong early target.

Why:

- workflow errors are often structurally visible
- gates and ordering logic can often be stated clearly
- before/after comparison is practical

Good early examples:

- insert a readiness gate in a toy workflow
- block downstream execution until upstream state is satisfied
- reorder a local workflow step in a replayable demonstration
- harden a closure rule in a constrained example

Good early validation targets:

- readiness state
- gate behavior
- ordering correctness
- closure path stability

Good early rollback targets:

- remove inserted gate
- restore previous ordering rule

---

### F7 · Representation & Localization Integrity

This is another excellent early target.

Why:

- structure is visible
- repairs are often local
- many actions are schema-like and easy to inspect
- replay demos work very well here

Good early examples:

- tighten JSON schema
- correct field shell shape
- restore array/object boundary
- strengthen formal descriptor wording

Good early validation targets:

- schema validity
- shell integrity
- descriptor fidelity

Good early rollback targets:

- restore prior schema
- remove tightened descriptor
- revert shell correction

---

## 7. Medium-scope families

Some families can support semi-auto work, but only carefully.

### F5 · Observability & Diagnosability Integrity

Possible early actions:

- suggest trace insertion
- add logging layer in replayable or synthetic workflows
- expose candidate path visibility
- add coherence probe markers

Why medium-risk:

- better visibility is useful
- but visibility improvement is not the same as true repair
- noise can increase quickly
- over-instrumentation can reduce clarity

Good use mode:

- suggest-only
- limited apply-and-check in small replay settings

Bad use mode:

- broad instrumentation without a narrow probe target

---

### F3 · State & Continuity Integrity

Possible early actions:

- continuity scaffold suggestion
- ownership trace suggestion
- role fence suggestion
- local persistence marker proposal

Why medium-risk:

- continuity problems often look simple but become complex quickly
- state and ownership can drift in subtle ways
- rollback may be harder than it first appears

Good use mode:

- planner-heavy
- toy examples
- constrained replay use

Bad use mode:

- aggressive live mutation of broad state behavior

---

## 8. Out of scope for early semi-auto use

The following areas should remain out of scope for v1 semi-auto execution.

### F6-heavy intervention

Boundary and safety cases should not become early semi-auto execution targets.

Why:

- the risk of wrong intervention is high
- the evidence is often incomplete
- planner-only or review-bound handling is safer
- the cost of false confidence is too high

Allowed early use:

- planner-only
- stabilization suggestion
- review recommendation
- escalation marker

Not allowed early use:

- aggressive automatic intervention
- strong policy-like changes
- legitimacy or incentive restructuring
- unsafe autonomous boundary action

---

### Multi-family ambiguity under weak evidence

If the case is sitting in strong ambiguity, semi-auto execution should not proceed.

Examples:

- F1/F7 ambiguity under synthetic structure pressure
- F3/F4 ambiguity under workflow-memory interaction
- F5/F6 ambiguity under abstract governance pressure

In such cases, the correct move is:

- revise routing
- reduce scope
- escalate
- stop and wait

---

### Broad system mutation

Actions that touch too much system surface at once are out of scope.

Examples:

- broad prompt system rewrites
- large multi-step repair sequences
- cross-module mutation without a local restore point
- unrestricted configuration rewrites

These are too large for early semi-auto discipline.

---

## 9. Allowed early action categories

The following action categories are good early semi-auto candidates.

### Category A · Evidence-local actions
Examples:

- re-ground evidence set
- filter anchors
- restore correct evidence source
- narrow candidate evidence range

### Category B · Gate-local actions
Examples:

- insert readiness gate
- block downstream step until upstream ready
- enforce minimal closure rule
- restore local ordering check

### Category C · Schema-local actions
Examples:

- tighten schema shell
- restore missing object boundary
- correct descriptor format
- constrain a field structure

### Category D · Probe-local actions
Examples:

- add a local trace probe
- expose one hidden workflow stage
- add one candidate trace line
- insert one visibility checkpoint

This category should remain more cautious than A, B, and C.

---

## 10. Disallowed early action categories

The following should remain outside early semi-auto scope.

### Category X · Full workflow redesign
Too broad.

### Category Y · High-abstraction policy intervention
Too risky.

### Category Z · Multi-step repair chains without checkpoints
Too hard to validate and rollback.

### Category W · Boundary-heavy autonomous intervention
Too dangerous for early phases.

---

## 11. Required safety checks before semi-auto apply

Before any in-scope action is applied, the system should confirm:

1. the case has a valid routed basis
2. the selected repair family is not weakly guessed
3. the action is in an allowed category
4. the plan scope is compatible with semi-auto use
5. the first validation target is explicit
6. the rollback target is explicit
7. no major stop condition is present

If these checks fail, the system should not auto-apply.

It should revert to:

- planner-only
- review-bound
- escalation
- or stop-and-wait

---

## 12. Required stop conditions

Semi-auto repair should stop immediately when:

- `no_fit = true`
- family confidence is too weak
- evidence sufficiency is too weak
- the restore point is unclear
- the first validation target is unclear
- the action would enter F6-heavy intervention space
- the action would affect multiple major layers at once
- the planner cannot distinguish between local gain and likely collateral damage

These conditions are not edge cases.
They are core protections.

---

## 13. Example in-scope actions

### Example A · F1 local semi-auto action

Case:
retrieval anchor drift in a replayable benchmark case

Action:
replace evidence subset with a better-aligned subset

Why in scope:

- local
- easy to compare
- rollback possible
- validation target is explicit

Recommended tier:

- Tier 2

---

### Example B · F4 local semi-auto action

Case:
downstream send step executes before upstream readiness is complete

Action:
insert a local readiness gate in the replay workflow

Why in scope:

- narrow workflow change
- visible before/after
- rollback is clear
- validation target is explicit

Recommended tier:

- Tier 2

---

### Example C · F7 local semi-auto action

Case:
output content is partially correct but the JSON shell is invalid

Action:
tighten schema shell and restore object boundary

Why in scope:

- strongly local
- highly inspectable
- validation is straightforward
- rollback is simple

Recommended tier:

- Tier 2

---

## 14. Example out-of-scope actions

### Example A · F6 boundary intervention

Case:
high-pressure alignment and legitimacy ambiguity

Action:
apply a strong autonomous stabilization rule

Why out of scope:

- high-risk boundary region
- low tolerance for false confidence
- review and escalation are safer

---

### Example B · broad workflow rewrite

Case:
multi-step workflow occasionally fails under mixed memory and closure pressure

Action:
rewrite the whole workflow plan automatically

Why out of scope:

- too broad
- too hard to validate locally
- rollback would be unstable

---

### Example C · abstract coherence intervention

Case:
value / knowledge / probability coherence case under F5/F6 boundary pressure

Action:
apply a strong abstract corrective rewrite

Why out of scope:

- high abstraction
- hard to validate locally
- planner-only or escalation is safer

---

## 15. Semi-auto success condition

Early semi-auto repair should be considered successful only when:

- the action stays in scope
- the local target improves
- collateral damage is absent or clearly acceptable
- rollback remains available
- the action does not silently widen into a larger mutation

This is the right early success standard.

Not:

- impressive-looking output
- aggressive intervention
- speculative repair story
- broad but untestable change

---

## 16. Relationship to future phases

This scope document is mainly for the transition between:

- Stage 1 · Repair planner
and
- Stage 2 · Constrained semi-auto repair

It should remain conservative until:

- validation examples become stronger
- rollback discipline is more battle-tested
- action libraries become cleaner
- family-specific patterns are better understood

So this document is not the end state.

It is the safe doorway into the next phase.

---

## 17. Recommended immediate next step

Once this file exists, the next useful step is likely one of these:

- create a small action catalog for F1 / F4 / F7
- create one minimal semi-auto demo spec
- create one validator example pack for semi-auto cases

The best immediate move is probably:

> start with a tiny catalog of safe early actions

That would make the semi-auto layer much more concrete.

---

## 18. One-line scope summary

**Semi-Auto Repair Scope v1 defines which Atlas-based repair actions are safe enough for early constrained semi-auto use, and which actions must remain planner-only, review-bound, or delayed.**
