# Auto Repair Architecture v1

🏗️ **Auto Repair Architecture v1** defines how Atlas-based repair should be structured as a system layer.

This document does **not** claim that a fully autonomous repair engine already exists.

Instead, it defines the intended architecture for moving from:

- diagnosis
- to first repair direction
- to structured repair planning
- to later validation and controlled execution

In short:

> this document explains how Auto Repair should be built,
> not how to pretend it is already finished.

---

## 1. Architectural role

Auto Repair is a **bridge layer** between Atlas diagnosis and deeper repair execution.

Its job is not to replace the Atlas.

Its job is to take a routed case and turn it into a controlled repair workflow.

That means Auto Repair should always sit **after**:

- Atlas routing
- family / node fit judgment
- fix-surface selection

and **before**:

- deeper repair execution
- validation loop
- rollback logic
- escalation into deeper WFGY repair

---

## 2. Full system placement

The current high-level system can be understood like this:

```text
Problem Map 3.0
→ Troubleshooting Atlas
→ Canonical Casebook
→ Atlas-to-AI Adapter
→ Fix Surface
→ Auto Repair
→ WFGY Deep Repair
````

Each layer has a different responsibility:

### Atlas

Defines the failure grammar.

### Casebook

Teaches how to route real cases.

### Adapter

Makes the atlas usable by AI systems.

### Fix Surface

Defines the first repair direction.

### Auto Repair

Turns diagnosis and first repair direction into a repair workflow.

### WFGY Deep Repair

Handles deeper, harder, more abstract, or more recursive repair layers.

---

## 3. Core architectural principle

The architecture should always preserve this order:

1. **Route first**
2. **Select repair family second**
3. **Plan repair third**
4. **Validate fourth**
5. **Execute or escalate fifth**

This order matters.

If repair planning happens before routing is stable, the system will produce shallow, random, or misleading repair proposals.

So the architecture is built on one non-negotiable rule:

> no repair planning without prior routing discipline

---

## 4. Minimal architecture blocks

Auto Repair v1 should be understood as five architecture blocks.

---

## Block A · Case Intake

This block receives the routed case.

Minimum expected inputs:

* case description
* primary family
* secondary family
* broken invariant
* best current fit
* confidence
* evidence sufficiency
* first fix surface direction

This block does not decide the family.
It assumes that Atlas routing has already happened.

Its purpose is to standardize the repair entry point.

---

## Block B · Repair Planner

This is the first truly active Auto Repair block.

Its role is to turn:

* routed diagnosis
* broken invariant
* first fix direction

into:

* candidate repair actions
* action ordering
* validation checkpoints
* misrepair warnings
* escalation recommendations

At this stage, the planner should remain conservative.

It should not claim to solve the whole case.
It should only define a structured first repair plan.

---

## Block C · Repair Action Layer

This block defines the space of allowed repair actions.

A repair action should not be an unstructured sentence.
It should be a typed action unit.

Typical examples:

* re-ground evidence set
* insert readiness gate
* strengthen JSON shell
* expose trace path
* tighten schema contract
* add boundary review checkpoint

This block is where repair action schemas become important.

Without this layer, the planner becomes too loose.

---

## Block D · Validation Loop

This block checks whether the repair improved the case.

Its role is to answer:

* did the broken invariant improve
* did the output become more stable
* did the system become more legible
* did the repair accidentally create a new failure
* should the workflow continue, revise, rollback, or escalate

This block is essential.
Without it, Auto Repair becomes guesswork.

---

## Block E · Rollback and Escalation

This block defines what happens when repair is unsafe, insufficient, or harmful.

Possible outcomes include:

* rollback to prior state
* choose alternate repair action
* switch repair family
* escalate to human review
* escalate to deeper WFGY repair

This is the main safety block of the architecture.

---

## 5. Primary workflow

The intended workflow is:

```text
case
→ atlas routing
→ fix surface
→ repair planner
→ candidate repair actions
→ validation loop
→ {accept / revise / rollback / escalate}
```

This is the smallest clean architecture.

Anything more ambitious should still preserve this core sequence.

---

## 6. What v1 is actually building

Auto Repair v1 is mainly focused on the **planning architecture**, not full autonomous execution.

That means v1 is primarily concerned with:

* architecture
* safety boundary
* repair action schemas
* planner logic
* validation logic
* rollback logic

It is **not** primarily about:

* large repair automation frameworks
* direct code mutation engines
* closed autonomous repair loops across all families
* full benchmark-scale automation

This distinction must remain clear.

---

## 7. Family suitability for early Auto Repair

Not all families should be treated equally in early phases.

### Best early targets

#### F1 · Grounding & Evidence Integrity

Why suitable:

* repair actions are often concrete
* evidence checks are easier to compare
* success can often be inspected clearly

Typical actions:

* re-grounding
* anchor re-check
* evidence filtering
* retrieval correction

#### F4 · Execution & Contract Integrity

Why suitable:

* many failures are workflow-structural
* gates and ordering can often be stated explicitly
* before / after logic is easier to inspect

Typical actions:

* readiness gate insertion
* ordering validation
* closure hardening
* downstream block-until-ready rule

#### F7 · Representation & Localization Integrity

Why suitable:

* many failures are container-visible
* structural correction is easier to verify
* replay demos can show the effect clearly

Typical actions:

* schema tightening
* descriptor repair
* JSON shell correction
* container validation

---

### Medium-risk targets

#### F5 · Observability & Diagnosability Integrity

Useful for:

* trace insertion
* logging uplift
* observability expansion

But caution is needed, because improved visibility is not always the same as repaired failure.

#### F3 · State & Continuity Integrity

Possible for:

* continuity scaffolding
* state trace support
* ownership tracing

But deeper continuity issues can become complicated quickly.

---

### High-risk early targets

#### F6 · Boundary & Safety Integrity

This region should be handled very carefully.

In early architecture phases, F6 should mostly support:

* repair planning
* warning generation
* stabilization suggestions
* escalation discipline

not aggressive automatic execution.

This is because boundary-heavy cases often require:

* stronger judgment
* human review
* intervention restraint
* policy-level caution

---

## 8. Repair planner contract

The planner block should eventually produce outputs like:

* selected repair family
* candidate action 1
* candidate action 2
* candidate action 3
* intended effect of each action
* likely misrepair risk
* what to validate next
* escalation recommendation

This is the practical center of Auto Repair v1.

If the planner is well-designed, later execution work becomes far easier.

If the planner is weak, later execution becomes dangerous.

---

## 9. Validation contract

The validation block should eventually answer at least these questions:

1. Did the targeted broken invariant improve
2. Did the system output become more stable
3. Did the repair reduce ambiguity or just shift it
4. Did the repair create collateral damage
5. Does the case now pass a minimal success contract
6. If not, should the system revise, rollback, or escalate

This means validation is not a cosmetic add-on.

It is part of the architecture.

---

## 10. Rollback contract

Rollback must be part of the design from the beginning.

Early rollback rules should cover at least:

* repair made the case worse
* repair changed the wrong layer
* repair caused new family drift
* repair increased opacity
* repair reduced structural fidelity
* repair crossed a safety boundary

A system that can propose repair but cannot rollback is not ready for trustworthy deployment.

---

## 11. Relationship to WFGY Deep Repair

Auto Repair should not be mistaken for the deepest repair layer.

Its intended role is:

* close to Atlas
* close to first repair direction
* constrained and auditable
* useful for practical first repair planning

WFGY Deep Repair remains the place for:

* higher abstraction
* recursive repair reasoning
* harder latent structure correction
* deeper multi-layer intervention logic

So the relation is:

```text
Atlas diagnosis
→ Auto Repair planning
→ deeper WFGY repair when needed
```

This keeps the system modular.

---

## 12. Recommended growth path

A healthy build path looks like this:

### Stage 1

Architecture and schemas

### Stage 2

Repair planner

### Stage 3

Validation rules

### Stage 4

Limited semi-auto execution in safer families

### Stage 5

Broader repair loop integration

The system should not jump directly to Stage 4 or 5.

That would create unnecessary instability.

---

## 13. Recommended future file set

As the folder grows, the following files make sense:

```text
auto-repair/
├── README.md
├── auto-repair-architecture-v1.md
├── auto-repair-roadmap-v1.md
├── auto-repair-safety-boundary-v1.md
├── repair-action-schema-v1.md
├── repair-validation-loop-v1.md
├── rollback-policy-v1.md
├── recipes/
├── prompts/
├── json/
└── demos/
```

Not all of these are needed immediately.

But this is the intended architecture path.

---

## 14. What v1 should be able to say honestly

The strongest honest statement for v1 is:

> Auto Repair v1 establishes the architecture for Atlas-based repair planning, validation, rollback, and future constrained execution.

That is strong enough to matter and honest enough to trust.

---

## 15. One-line architecture summary

**Auto Repair Architecture v1 defines the bridge from Atlas diagnosis and fix-surface selection to structured repair planning, validation, rollback, and later constrained execution.**
