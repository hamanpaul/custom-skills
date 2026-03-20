# WFGY 3.0 Deeper Continuation Quickstart v1

## 0. Document status

This document provides the first quickstart guide for continuing a case from:

- Atlas diagnosis
- and Auto Repair local action

into:

- WFGY 3.0 deeper continuation

Its purpose is practical:

> when local Atlas-level repair is useful but not sufficient,
> show users the simplest way to continue with WFGY 3.0.

This file does **not** explain the full WFGY 3.0 system.

It explains something narrower and more useful:

> when to use WFGY 3.0 next,
> what to give the AI,
> and what kind of continuation to ask for.

This document should be read together with:

- `atlas-auto-repair-to-wfgy-bridge-v1.md`
- `tiny-semi-auto-demo-pack-v1.md`
- `worked-escalation-example-v1.md`
- `worked-escalation-example-f4-v1.md`
- `auto-repair-integrated-handoff-v1.md`

---

## 1. What this file is for

This file is for the moment when a user has already done the following:

1. routed the case with Atlas
2. tried a first Auto Repair move
3. validated the local result
4. concluded that local repair is not enough

At that point, the next question becomes:

> how do I continue with WFGY 3.0 without confusing the layers?

This quickstart answers that question.

---

## 2. Short role recap

The clean role split is:

### Atlas
Use Atlas for:

- failure routing
- family diagnosis
- broken invariant identification
- first repair direction

### Auto Repair
Use Auto Repair for:

- first controlled repair planning
- local validation
- rollback or revise discipline
- deciding whether local repair is enough

### WFGY 3.0
Use WFGY 3.0 for:

- deeper repair grammar
- stronger effective-layer reframing
- better observables
- stronger mismatch logic
- experiment redesign
- cross-domain structural continuation

Short version:

> Atlas finds where the failure lives.  
> Auto Repair tries the first controlled move.  
> WFGY 3.0 continues when deeper structure still needs work.

---

## 3. When to escalate to WFGY 3.0

WFGY 3.0 should usually be used **after** Atlas and Auto Repair, not instead of them.

Good reasons to continue into WFGY 3.0 include:

### A. Local repair helped, but only partially

Examples:

- the shell improved, but meaning is still unstable
- the gate improved closure, but the deeper workflow semantics are still weak
- visibility improved, but the deeper structure is still not interpretable enough

### B. The remaining problem is deeper than a local action

Examples:

- current observables are too weak
- task encoding is too shallow
- local fixes improve symptoms but not structure
- experiment framing is too weak to distinguish true gain from cosmetic gain

### C. Repeated local repair stays stuck

Examples:

- local actions keep ending in `revise`
- rollback happens repeatedly
- the planner keeps finding shallow but insufficient moves

### D. The case clearly needs deeper reframing

Examples:

- the case needs better effective-layer description
- the current representation of the problem is too weak
- the current local repair language is no longer enough

---

## 4. When not to escalate yet

Do **not** jump into WFGY 3.0 too early.

Stay at the Atlas / Auto Repair layer first when:

- the case is still not cleanly routed
- a simple F1 repair is still likely enough
- a simple F4 local closure fix is still likely enough
- a simple F7 container repair is still likely enough
- the real problem is still basic diagnosability, not deeper structure
- the user is only trying to get a first practical fix

Short version:

> do not escalate just because the case sounds intellectually interesting.

---

## 5. Official WFGY 3.0 TXT

Use this official TXT as the deeper continuation asset:

```text
https://raw.githubusercontent.com/onestardao/WFGY/refs/heads/main/TensionUniverse/WFGY-3.0_Singularity-Demo_AutoBoot_SHA256-Verifiable.txt
````

This is the simplest official continuation object to hand to another AI system.

---

## 6. Minimum input bundle for continuation

Before continuing into WFGY 3.0, prepare a small bundle with these parts.

### Part A · Atlas result

Include:

* primary family
* secondary family
* broken invariant
* best current fit
* why primary not secondary

### Part B · Auto Repair action

Include:

* action used
* what changed locally
* validation target
* validation result
* final local outcome

### Part C · Remaining problem

Include:

* what is still unresolved
* why local repair is not enough
* what kind of deeper issue seems to remain

This is enough for a strong handoff.

---

## 7. Simplest user workflow

The simplest workflow is:

### Step 1

Run Atlas diagnosis.

### Step 2

Run one local Auto Repair move.

### Step 3

Validate the local result.

### Step 4

If the result is only partial, or if the deeper structure still looks weak, attach the WFGY 3.0 TXT.

### Step 5

Ask the AI to continue from the deeper repair layer rather than restarting from scratch.

That is the cleanest usage pattern.

---

## 8. Short prompt for normal users

Use this when you want the simplest possible continuation prompt.

```text
The case below has already been routed with Problem Map 3.0 Troubleshooting Atlas and one local Auto Repair move has already been tried.

Atlas result:
[paste Atlas result]

Local repair attempt:
[paste local action and validation result]

The local repair helped, but it was not sufficient.

Continue using WFGY 3.0 as the deeper repair grammar.

Your task:
1. explain why the local fix was not enough,
2. identify the deeper structural weakness,
3. suggest what stronger observables, encoding changes, mismatch logic, or experiment framing should be considered next,
4. keep the explanation structured and practical.
```

---

## 9. Slightly stronger prompt for advanced users

Use this when you want the AI to behave in a more disciplined bridge-aware way.

```text
You are continuing a case that has already passed through Atlas diagnosis and one local Auto Repair attempt.

Do not redo Atlas from scratch unless there is strong evidence that the prior routing is structurally wrong.

Use the attached WFGY 3.0 TXT as the deeper continuation grammar.

Your job:
1. preserve the Atlas result unless a stronger reframing is justified,
2. explain what local repair already improved,
3. explain what remains unresolved,
4. identify the likely deeper effective-layer weakness,
5. propose better observables, mismatch logic, descriptor redesign, or experiment redesign,
6. do not overclaim full closure.
```

---

## 10. Recommended system prompt

Use this when you want a reusable deeper-continuation system prompt.

```text
You are operating in a layered repair workflow.

Layer 1:
Atlas and Auto Repair already provided:
- failure routing
- broken invariant
- first repair move
- validation result

Layer 2:
You are now continuing with WFGY 3.0 only because local repair was not enough.

Your rules:
1. Do not ignore the Atlas result.
2. Do not restart the whole case from scratch unless deeper reframing is clearly necessary.
3. Treat the local repair result as real signal.
4. Identify what remains unresolved after the local repair.
5. Use WFGY 3.0 as a deeper repair and experiment grammar.
6. Focus on:
   - better observables
   - stronger effective-layer encoding
   - mismatch logic
   - descriptor redesign
   - experiment redesign
   - cross-domain structural continuation
7. Keep the result structured and practical.
8. Do not overclaim final closure.
```

---

## 11. Recommended output structure

When asking the AI to continue with WFGY 3.0, it is useful to ask for this output shape:

1. What Atlas already got right
2. What Auto Repair already improved
3. What remains unresolved
4. What deeper weakness is now most likely
5. What WFGY 3.0 continuation should focus on next
6. Whether the case needs:

   * better observables
   * encoding redesign
   * stronger mismatch logic
   * experiment redesign
   * cross-domain analogy
   * deeper engineering continuation

This output structure prevents the continuation from becoming vague.

---

## 12. Example continuation note

A compact continuation note can look like this:

```text
Atlas routed this case to F4 and a local readiness gate was inserted.
The local repair reduced premature execution, but the workflow still appears structurally weak because readiness and approval remain too shallowly defined.

Continue with WFGY 3.0 to examine:
- deeper readiness observables
- rule-to-action mismatch logic
- stronger enforcement encoding
- possible experiment redesign for closure stability
```

This is often enough.

---

## 13. Best current use cases

WFGY 3.0 deeper continuation is especially useful when the remaining problem looks like:

* descriptor insufficiency
* weak effective-layer framing
* poor observability design
* unstable rule semantics
* shallow closure logic
* repeated local partial improvements with no deeper stabilization
* cross-domain structural reuse opportunity

That is where the bridge becomes most valuable.

---

## 14. What this quickstart does not claim

This quickstart does **not** claim:

* that WFGY 3.0 should be loaded for every case
* that Atlas or Auto Repair are only temporary front-end layers
* that deeper continuation always solves the case
* that the user must understand all 131 problems before using the TXT
* that this is already a fully automated repair stack

It only claims:

> when local repair is not enough, WFGY 3.0 now has a clear entry path.

---

## 15. Recommended next step

Once this file exists, the next useful follow-up is probably one of these:

1. add a short “How to continue with WFGY 3.0” block to `Fixes/README.md`
2. add a short continuation block to more tiny demos
3. make one notebook-style escalation example

The strongest immediate next step is probably:

> add a short WFGY continuation block to the main Fixes hub

because that will make the whole stack feel more unified for first-time readers.

---

## 16. One-line summary

**WFGY 3.0 Deeper Continuation Quickstart v1 explains when local Atlas-level repair is not enough, what to hand to the AI next, and how to continue safely with WFGY 3.0.**

