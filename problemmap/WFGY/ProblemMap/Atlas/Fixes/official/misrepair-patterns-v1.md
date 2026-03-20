<!--
AI_NOTE_START

Document role:
This file is the first official misrepair guide for Atlas v1.

How to use this file:
1. Read this file after:
   - [Family Fix Surface v1](./family-fix-surface-v1.md)
   - [Atlas to WFGY Bridge v1](./atlas-to-wfgy-bridge-v1.md)
   - [Canonical Casebook v1](../../canonical-casebook-v1.md)
2. Treat this document as the official guide to common wrong first moves after routing.
3. Use this file to understand:
   - which repair mistakes are common by family
   - why those mistakes are tempting
   - how to avoid wasting the first repair move
4. Use this file for teaching, demo design, contributor guidance, and AI-facing repair warnings.

What this file is:
- The first official misrepair pattern guide
- A repair-discipline companion to the family fix surface
- A route-first warning layer

What this file is not:
- Not the atlas core
- Not the full deep repair manual
- Not the full WFGY 3.0 exploration pack
- Not a list of every possible implementation error
- Not a replacement for correct routing

Reading discipline for AI:
- Always preserve route-first discipline.
- Do not use this file to infer family routing by itself.
- Use misrepair warnings only after the case has been routed.
- Treat these patterns as common failure modes of the first repair move, not as full case classifications.

AI_NOTE_END
-->

# Misrepair Patterns v1 ⚠️

## Problem Map 3.0 Troubleshooting Atlas  
## Official guide to wrong first repair moves

## 0. Document Status 🚦

This document is the **first official misrepair guide** for the atlas fix layer.

It exists to answer a very practical question:

> After correct routing, what are the most common wrong first repair moves?

This matters because many debugging failures do not come only from bad classification.

They also come from:

- repairing the wrong layer first
- choosing a repair move that sounds sensible but is structurally misaligned
- patching a downstream symptom before restoring the upstream invariant

This document is frozen as **Misrepair Patterns v1**.

It is frozen not because all repair mistakes are known forever, but because the first stable public set of family-level misrepair warnings is now strong enough to support teaching, demos, and real troubleshooting.

---

## 1. Why misrepair deserves its own document 🧠

Correct routing is necessary, but not sufficient.

A team can correctly identify:

- the family
- the broken invariant
- the best current fit

and still lose time if the first repair move is wrong.

Misrepair matters because the wrong first move often does one of three things:

1. wastes time on a downstream symptom
2. makes the case look more stable while leaving the real failure untouched
3. pushes the team into a more confusing second-order mess

Short version:

> **wrong first repair moves are one of the fastest ways to turn a solvable case into a messy one**

---

## 2. What this document covers 🎯

This document focuses on **family-level misrepair patterns**.

That means it identifies:

- the most common wrong first move for each family
- why that wrong move is tempting
- what structural mistake it reflects
- what the correct repair posture should be instead

This document does **not** try to list every possible implementation error.
That belongs later to:

- community fix packs
- runnable examples
- Colab workflows
- benchmark reruns
- deeper WFGY exploration

This document stays at the official public grammar layer.

---

## 3. Core misrepair discipline 🔒

The official misrepair discipline is simple:

### Rule 1

Do not repair before routing.

### Rule 2

Do not patch downstream polish before restoring the broken invariant.

### Rule 3

Do not mistake the easiest visible symptom for the first repair target.

### Rule 4

Do not skip from first repair directly to grand theory when the family-level first move has not yet been tried.

### Rule 5

Do not confuse deeper WFGY exploration with the first repair move.

Short version:

> **route first  
> repair the right layer first  
> then escalate if needed**

---

## 4. Family-level misrepair patterns 🧩

---

# F1 · Grounding & Evidence Integrity 🌍

## Common misrepair

The most common wrong first move is:

- polishing the answer
- rephrasing the response
- improving style or fluency
- increasing reasoning verbosity
- adding semantic decoration without re-checking the anchor

## Why this is tempting

It is tempting because a grounding error often looks like a weak answer.

So people try to make the answer “better” instead of making it **truer**.

## Why this is structurally wrong

The broken invariant in F1 is not fluency first.
It is anchor alignment.

If the answer is detached from:

- evidence
- world reference
- target semantics
- real deployment context

then style work simply produces a more elegant detachment.

## Correct repair posture

Do this instead:

- re-check the anchor
- trace source-to-claim linkage
- separate proxy from target
- verify evidence alignment before improving presentation

## One-line misrepair summary

**Do not polish an ungrounded answer.**

---

# F2 · Reasoning & Progression Integrity 🧠

## Common misrepair

The most common wrong first move is:

- adding more context blindly
- extending the chain
- asking for “more detailed reasoning” without stabilizing the path
- increasing recursion before the progression is viable

## Why this is tempting

It is tempting because a reasoning failure often looks like not-enough-thinking.

So people try to add:

- more steps
- more context
- more explanation

without checking whether the progression itself is broken.

## Why this is structurally wrong

If the path is already unstable, making it longer usually amplifies the instability.

This turns:

- local confusion
into
- larger collapse

## Correct repair posture

Do this instead:

- reduce the path
- insert checkpoints
- test alternate parses
- find the first unstable transition
- restore viable progression before adding depth

## One-line misrepair summary

**Do not make a broken reasoning path longer before making it viable.**

---

# F3 · State & Continuity Integrity 🧵

## Common misrepair

The most common wrong first move is:

- adding more instructions
- stuffing in more memory context
- writing stronger role prompts without repairing the thread
- treating continuity drift as mere formatting confusion

## Why this is tempting

It is tempting because continuity problems often look like weak discipline.

So people try to “remind the system harder” instead of restoring:

- persistence
- role boundaries
- ownership lines
- continuity structure

## Why this is structurally wrong

A broken thread is not fixed by shouting more instructions at it.

If memory, ownership, or role continuity is already drifting, extra instruction text can even increase confusion.

## Correct repair posture

Do this instead:

- restore continuity checkpoints
- re-fence roles
- trace ownership
- identify where the thread broke
- rebuild persistence before adding new behavioral instructions

## One-line misrepair summary

**Do not use stronger instructions to replace broken continuity.**

---

# F4 · Execution & Contract Integrity ⚙️

## Common misrepair

The most common wrong first move is:

- tuning prompts before checking closure
- asking the model to reason better when the workflow cannot close
- treating deadlock as a language problem
- polishing policy language while the bridge remains broken

## Why this is tempting

It is tempting because execution problems often show up as bad outcomes.

So people attack the visible output instead of the hidden skeleton.

## Why this is structurally wrong

If readiness, ordering, bridge integrity, liveness, or closure are broken, the system may never have had a valid execution path in the first place.

That means output-level optimization is often wasted.

## Correct repair posture

Do this instead:

- check readiness
- verify ordering
- inspect bridge closure
- test liveness
- confirm that the rule-to-action path actually closes

## One-line misrepair summary

**Do not ask the workflow to think better before it can close.**

---

# F5 · Observability & Diagnosability Integrity 🔎

## Common misrepair

The most common wrong first move is:

- jumping into high-level intervention before visibility exists
- making strong structural claims with weak trace support
- treating opacity as if the hidden cause were already known
- escalating into boundary repair before diagnosability is restored

## Why this is tempting

It is tempting because people feel pressure to act quickly.

When the failure is opaque, there is a strong urge to guess the deep cause and move immediately.

## Why this is structurally wrong

If the system still lacks:

- trace visibility
- coherence visibility
- auditability
- warning structure

then early intervention often targets the wrong layer.

This creates misrepair that feels bold, but is poorly grounded.

## Correct repair posture

Do this instead:

- expose the trace
- insert observability
- inspect coherence visibility
- strengthen warning structure
- improve diagnosability before deeper intervention

## One-line misrepair summary

**Do not intervene at the highest level while the failure is still structurally opaque.**

---

# F6 · Boundary & Safety Integrity 🛡️

## Common misrepair

The most common wrong first move is:

- treating a real boundary failure as a pure observability issue
- assuming more explanation alone will restore control
- writing nicer goals without checking incentive and control paths
- delaying stabilization while waiting for perfect interpretability

## Why this is tempting

It is tempting because many F6 cases are surrounded by uncertainty, visibility issues, or complex theory language.

So people stay too long in analysis mode when the boundary is already breaking.

## Why this is structurally wrong

If the system is already drifting outside a viable boundary, repair must include stabilization of:

- control
- incentive
- corridor viability
- target alignment
- collective boundary integrity

More visibility may help, but visibility alone is not enough.

## Correct repair posture

Do this instead:

- inspect the active boundary breach
- check control-path integrity
- identify incentive distortion
- stabilize safe corridor behavior
- separate proxy from target

## One-line misrepair summary

**Do not treat a real boundary breach as only a visibility problem.**

---

# F7 · Representation & Localization Integrity 🧱

## Common misrepair

The most common wrong first move is:

- extending reasoning on top of a broken carrier
- adding explanation text instead of repairing structure
- assuming the issue is only semantic or grounding
- treating symbolic or layout distortion as superficial

## Why this is tempting

It is tempting because representation failures can look like confusion, hallucination, or weak explanation.

So people often try to make the explanation richer rather than making the carrier faithful.

## Why this is structurally wrong

If the symbolic, formal, local, or structural container is broken, richer content often just fills a distorted shell.

This hides the true problem.

## Correct repair posture

Do this instead:

- audit descriptor fidelity
- inspect formal adequacy
- restore local anchors
- check hierarchy and structure
- repair the carrier before extending reasoning

## One-line misrepair summary

**Do not demand better output from a broken structural carrier.**

---

## 5. Cross-family misrepair traps 🔗

Some wrong first moves happen especially often at family boundaries.

### F1 / F7 trap

Wrong move:
- treating distorted structure as pure grounding
or
- treating broken grounding as only a representation problem

Safe posture:
- ask first whether reality alignment is broken or whether the carrier is broken

---

### F5 / F6 trap

Wrong move:
- escalating immediately into boundary intervention when the system is still too opaque
or
- staying forever in observability uplift when a real boundary breach is already active

Safe posture:
- ask whether the main thing missing is visibility or whether the boundary itself is already failing

---

### F3 / F4 trap

Wrong move:
- treating broken continuity as if it were only workflow closure
or
- treating execution deadlock as if it were only memory confusion

Safe posture:
- ask whether the thread broke first or the loop failed first

---

### F2 / F7 trap

Wrong move:
- patching progression when the carrier is broken
or
- obsessing over the carrier when the progression itself is the unstable element

Safe posture:
- ask whether the structure carrying the reasoning is viable before deepening the path

---

## 6. The official route-first warning pattern 🚨

Whenever a repair attempt fails early, the first question should be:

> Did we repair the wrong layer first?

That question is often more useful than:

> Why did the model still fail?

Because many second-order failures are simply consequences of a wrong first move.

---

## 7. Relationship to Family Fix Surface v1 🛠️

This document is a direct companion to:

- [Family Fix Surface v1](./family-fix-surface-v1.md)

The family fix surface tells you:

- what to try first

This document tells you:

- what **not** to try first

Together, they form the official first repair grammar.

Short version:

> Family Fix Surface = first move  
> Misrepair Patterns = first wrong move to avoid

---

## 8. Relationship to WFGY 3.0 bridge 🌉

This document is also a companion to:

- [Atlas to WFGY Bridge v1](./atlas-to-wfgy-bridge-v1.md)

The bridge tells you:

- when to escalate
- what to pass into WFGY
- what deeper outputs to expect

This document helps you avoid a common mistake before escalation:

- using deeper exploration as a substitute for correct first repair discipline

WFGY escalation becomes much more useful when obvious family-level misrepair has already been avoided.

---

## 9. Relationship to community fixes 🤝

Community-contributed fix packs should learn from this document.

That means community recipes should not only say:

- what to do

They should also say:

- what to avoid doing first

This is especially valuable for:

- Colab demos
- prompt packs
- workflow recipes
- benchmark reruns
- reproduction packs

because runnable material without misrepair discipline often teaches the wrong reflexes.

---

## 10. How to use this file in demos and teaching 🎓

This file is especially useful in three places:

### 1. onboarding

It helps new readers learn that repair is not only about choosing the right move, but also about avoiding the seductive wrong one.

### 2. demos

It makes demos stronger because a “wrong first move” comparison often reveals the atlas value immediately.

### 3. AI-assisted repair

It helps the adapter warn against common repair mistakes before generating the first suggestion.

---

## 11. Patch protocol 🔄

Misrepair Patterns v1 is frozen, but not closed.

### Small patch

Use for:

- clearer wording
- sharper warnings
- stronger family examples
- cleaner cross-family trap explanations

### Medium patch

Use for:

- adding more official misrepair cases
- adding stronger boundary-specific misrepair sections
- integrating more repair-demo comparisons

### Large patch

Only use if:

- the official misrepair grammar becomes structurally misleading
- repeated field use shows that the main wrong-first-move logic is fundamentally incomplete
- the relationship between family-level repair and misrepair needs redesign

### Current status

No large-patch pressure is currently justified.

---

## 12. Official status

The correct formal statement is:

> Misrepair Patterns v1 is the first frozen official guide to common wrong first repair moves in Problem Map 3.0 Troubleshooting Atlas.  
> It helps preserve route-first discipline by showing what not to do first after a case is correctly routed.

---

## 13. One-line version

**Misrepair Patterns v1 tells you the most common wrong first repair move to avoid after atlas routing.**

---

## 14. Closing note ✨

A strong troubleshooting system should not only teach the right move.

It should also teach the most tempting wrong move.

That is what this file is for.

It protects the first repair step from becoming the first big mistake.
