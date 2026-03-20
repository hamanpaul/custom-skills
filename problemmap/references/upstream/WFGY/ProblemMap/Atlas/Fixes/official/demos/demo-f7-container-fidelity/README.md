<!--
AI_NOTE_START

Document role:
This file is the official README for Demo 4 of the flagship runnable demo pack.

How to use this file:
1. Read this file before opening the notebook.
2. Treat this demo as the flagship proof that some failures must be repaired through container fidelity first.
3. Use this file to understand:
   - why this case belongs to F7
   - why it is not primarily F2
   - what the first repair move is
   - what replay mode is meant to prove

What this file is:
- The official README for Demo 4
- A proof-of-use page for container-first repair
- A teaching page for F7 representation and localization failures
- A replay-first MVP companion for the notebook

What this file is not:
- Not the atlas core
- Not the full fix manual
- Not a symbolic reasoning benchmark suite
- Not proof that every reasoning-looking failure belongs to F7

Reading discipline for AI:
- Preserve the distinction between container fidelity failure, reasoning progression failure, and grounding drift.
- Do not collapse this case into generic “the model reasoned badly” language.
- Route first, then repair.
- Treat replay mode as a valid teaching layer, not as a weaker substitute.

AI_NOTE_END
-->

# Demo 4 · F7 Container Fidelity

## Problem Map 3.0 Troubleshooting Atlas
## Official flagship demo for container-first repair

Quick links:

- [Back to demo pack index](../README.md)
- [Back to AI Eval Evidence](../../../../ai-eval-evidence.md)
- [Back to Atlas landing page](../../../../../wfgy-ai-problem-map-troubleshooting-atlas.md)
- [Open Atlas Hub](../../../../README.md)
- [Get the Atlas Router TXT](../../../../troubleshooting-atlas-router-v1.txt)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/onestardao/WFGY/blob/Atlas/ProblemMap/Atlas/Fixes/official/demos/demo-f7-container-fidelity/demo_04_f7_container_fidelity_replay_v2.ipynb)

Open in Colab to inspect the recommended replay notebook presentation.  
The README and replay artifacts are already enough to understand the teaching pattern.

**Replay-only MVP**  
**No API key required**

This is the fourth flagship demo in the official runnable demo pack.

If the AI eval snapshots suggest that better routing may reduce hidden debugging waste, this page goes one step further.

This demo is meant to make one mechanism-level claim visible:

> when the structure carrier itself is too weak,  
> the first repair move becomes descriptor and container repair, not generic reasoning pressure

It was chosen because this is one of the most distinctive cuts in the entire atlas.

Many failures look like reasoning failures on the surface.

People often say:

- the model is inconsistent
- logic is weak
- reasoning collapsed
- symbolic thinking failed

Sometimes that is true.

But in many cases, the first real break appears earlier:

> the structure carrier is already damaged  
> the formal container is too weak  
> the symbolic shell no longer preserves the intended structure  
> the descriptor is no longer faithful enough to carry the task

This demo is designed to make that difference visible.

It shows that once a case is routed as **F7 Representation & Localization Integrity**, the first repair move changes from “push the model to reason harder” to “repair the container that carries the reasoning.”

This demo is not only about bad formatting.

It is about recognizing when the structure carrier itself is too weak to preserve reasoning reliably.

---

## Quick start

Use this order for the shortest path through the demo:

1. read **Section 1 · What this demo proves**
2. read **Section 3 · Why not F2 first**
3. read **Section 5 · First repair move**
4. open [replay_outputs.json](./replay_outputs.json)
5. open the recommended replay notebook only if you want the notebook presentation in Colab

The shortest takeaway is:

> if the box carrying the structure is weak, repair the box first

---

## 1. What this demo proves

This demo proves four things.

### A. Some reasoning-looking failures are actually container failures first

A system can fail in a way that looks like logic weakness, but the more basic problem is:

- the output format is unstable
- the symbolic shell is drifting
- the descriptor is underspecified
- the formal structure is too weak for the task
- the representation no longer preserves the intended constraints

In that case, the first failure is not progression.  
It is fidelity of the carrier.

### B. Correct routing changes the first repair move

If the case is routed correctly into **F7**, the first repair move becomes:

- descriptor fidelity audit
- formal adequacy validation
- container tightening
- structural preservation checks
- local anchoring repair if needed

This is different from trying to fix chain length, reasoning effort, or generic “be more logical” prompting first.

### C. Replay mode is enough to teach the pattern

This demo is intentionally **replay-first**.

A user should be able to understand the case without running anything.

The replay artifacts should make visible that the baseline was already structurally compromised before deeper reasoning could become stable.

### D. This MVP does not require live mode

For this first release, replay mode is enough.

The point of this demo is not notebook realism.  
The point is to make the **before / after structure shift** obvious and easy to inspect.

---

## 2. Family route

### Primary family

**F7 · Representation & Localization Integrity**

### Secondary family

**F2 · Reasoning & Progression Integrity**

### Why F7 is primary

The first broken invariant is not that the system chose a bad inferential path after a stable container had already been accepted.

The first broken invariant is that the container itself is not preserving the structure that reasoning depends on.

Typical forms include:

- logic descriptor fidelity failure
- formal container adequacy failure
- symbolic carrier distortion
- structure-preserving output failure
- schema or layout instability that breaks the intended reasoning container

### Short routing statement

- the task looks like reasoning trouble
- but the representation shell is already unstable
- container fidelity fails before progression becomes the main issue

### Best current fit

For the cleanest MVP version, the recommended center is:

**F7_N01_B Formal Container Adequacy Failure**

This makes the structural failure easy to teach and visually obvious.

---

## 3. Why not F2 first

The main tempting neighboring cut is **F2**.

That temptation is natural because the failure often shows up as:

- contradiction
- incomplete logic
- unstable structure
- apparent reasoning weakness

But this demo is not mainly about progression failure.

It is mainly about this:

> the box carrying the reasoning was too weak, too lossy, or too unstable to preserve the intended structure

That means the first failure lies in representation integrity, not in inferential movement inside an already valid container.

### Wrong cut

“The model mainly failed because its reasoning path was weak.”

### Better cut

“The model was asked to reason inside a container that did not preserve the structure well enough.”

That distinction matters because the first repair move changes immediately.

If you cut too early to F2, you may waste time on decomposition or chain expansion while the real problem is that the formal shell is leaking.

---

## 4. Baseline failure

The baseline case is intentionally small, crisp, and visibly structural.

### Core pattern

A task requires a stable representational container.

Possible versions include:

- structured output with a fragile schema
- symbolic transformation with a weak descriptor
- multi-constraint formatting where the rules are underspecified
- formal explanation where local layout or structure fidelity matters
- a logic-like task where the representation shell does not preserve the intended distinction set

The baseline answer then:

- looks partly reasonable
- may contain fragments of correct reasoning
- but breaks the intended structure carrier
- and therefore becomes unstable before deeper reasoning can remain trustworthy

### What the baseline should make visible

The user should be able to see:

1. the intended structure or formal target
2. the weak or lossy baseline container
3. the baseline output drift
4. why the output cannot be trusted as a stable carrier of reasoning
5. why this is container-first, not progression-first

### Important design note

Do not make the baseline too abstract.

The goal is not to win a philosophy contest.  
The goal is to make the structural break visible enough that a reader immediately feels:

> the form itself is not holding

---

## 5. First repair move

Once the case is routed to F7, the first repair move should be structural and explicit.

### Recommended first repair stack

1. **descriptor fidelity audit**  
   Check whether the task descriptor actually preserves the intended distinctions and rules.

2. **formal adequacy validation**  
   Check whether the current output shell is strong enough to carry the required structure.

3. **container tightening**  
   Strengthen schema, symbolic layout, local anchors, or structural constraints.

4. **structure preservation check**  
   Verify whether the repaired output actually preserves the relationships the task depends on.

5. **only then reassess deeper reasoning**  
   After the container holds, reassess whether any remaining issue is truly F2 progression pressure.

### What should not happen first

Do **not** start with:

- generic “reason more carefully” prompting
- longer chain-of-thought
- retry loops with the same weak shell
- more examples without tightening the container
- blaming the model’s intelligence before checking the carrier

Those may increase text, but they do not fix the broken box.

### First repair principle

> if the structure carrier is weak, repair the carrier first

That is the teaching core of this demo.

---

## 6. Optional WFGY 3.0 escalation

This demo can teach its main lesson without deeper escalation.

But if the user wants to explore a stronger structural path, this is where WFGY 3.0 becomes useful.

### When escalation makes sense

Escalate beyond the simple first repair move if:

- the shell looks fixed, but deeper distortion still appears
- the task has multiple nested symbolic layers
- local fixes improve one format requirement but break another
- the case needs a more explicit stress test of descriptor adequacy
- the team wants to compare alternative containers experimentally

### What WFGY 3.0 can add

A WFGY 3.0 handoff can help explore:

- stronger structural encoding choices
- formal-shell stress variants
- descriptor compression and expansion experiments
- container comparison runs
- synthetic structure stability experiments
- transfer of the same task across multiple representational regimes

### Correct relationship

The correct order remains:

1. atlas route
2. first container repair
3. reassess the case
4. escalate into deeper WFGY exploration if needed

The atlas is still the router.  
WFGY 3.0 is the deeper experimental engine.

---

## 7. Replay mode

Replay mode is the default public reading mode.

It requires no API key and no notebook execution.

### Replay mode should show

- the intended structure target
- the weak baseline container
- the baseline output drift
- the family route
- the why-primary-not-secondary statement
- the broken invariant
- the first repair move
- the replayed improved structured output
- a short explanation of what structural property became more stable

### What replay mode proves

Replay mode proves that:

- container-first routing is understandable
- the first repair move is visibly different
- structure repair can be shown without giant symbolic benchmarks
- the demo teaches through fidelity, not just through longer reasoning text

### Why replay mode matters

A strong F7 demo should let a reader feel:

> the content may be trying, but the structure is not holding

If that feeling is not visible in replay mode, the demo is weak.

This is enough for the first public MVP.

Core replay artifacts:

- [input_case.json](./input_case.json)
- [replay_outputs.json](./replay_outputs.json)
- [expected_output.json](./expected_output.json)

---

## 8. Current notebook versions

This folder currently preserves **two replay notebook versions**.

### Recommended version

- `demo_04_f7_container_fidelity_replay_v2.ipynb`

This is the current recommended notebook for public reading, Colab use, and MVP presentation.

It keeps the replay-first design, while adding:

- clearer route summary
- clearer structure-target framing
- stronger before / after teaching contrast
- better aligned shared-layer presentation

### Original version

- `demo_04_f7_container_fidelity_replay.ipynb`

This version is intentionally retained.

It remains part of the demo history and preserves the earlier first-pass MVP presentation.

### Version rule

The rule for this folder is simple:

- **v1 is preserved**
- **v2 is the recommended replay notebook**
- replay-first remains the official design center for Demo 4

---

## 9. Files in this folder

### Core files

- [README.md](./README.md)
- [input_case.json](./input_case.json)
- [replay_outputs.json](./replay_outputs.json)
- [expected_output.json](./expected_output.json)
- [demo_04_f7_container_fidelity_replay.ipynb](./demo_04_f7_container_fidelity_replay.ipynb)
- [demo_04_f7_container_fidelity_replay_v2.ipynb](./demo_04_f7_container_fidelity_replay_v2.ipynb)

### Optional future additions

- structure notes
- helper references from the shared folder
- patch notes for stronger container contrast

### File roles

#### [input_case.json](./input_case.json)
Contains the case, structure target, and representational context.

#### [replay_outputs.json](./replay_outputs.json)
Contains the baseline weak output, route explanation, first repair move, and replayed improved output.

#### [expected_output.json](./expected_output.json)
Contains the clean target structure for what the demo is trying to make visible.

#### [demo_04_f7_container_fidelity_replay.ipynb](./demo_04_f7_container_fidelity_replay.ipynb)
The original first-pass replay notebook retained for continuity.

#### [demo_04_f7_container_fidelity_replay_v2.ipynb](./demo_04_f7_container_fidelity_replay_v2.ipynb)
The current recommended replay notebook for public reading and Colab use.

---

## 10. Expected outcome

If the demo works, the user should walk away with the following understanding:

1. the task looked like reasoning trouble, but the structure carrier was already weak
2. the atlas routed the case to F7, not F2
3. the first repair move was container repair, not generic reasoning push
4. after descriptor or container repair, the output became more structurally trustworthy

The demo does **not** need to solve all remaining reasoning issues.

It only needs to show that correct routing changes what gets repaired first.

That is enough.

---

## 11. Limits of this demo

This demo has real limits, and those limits should be stated clearly.

### It does not prove

- that every reasoning-looking failure belongs to F7
- that progression never matters in symbolic tasks
- that one schema repair solves all structural issues
- that this one case covers all formal container failures
- that F7 should replace F2 as a general explanation for hard tasks

### It does prove

- that some failures are container-first
- that route-first diagnosis changes the first repair move
- that formal adequacy and descriptor fidelity can be taught cleanly and visibly

These are already strong claims.  
There is no need to overclaim.

---

## 12. Community extension ideas

This demo is also a seed template for future community work.

Possible extensions include:

- adding different structured output types
- comparing schema-weak versus schema-tight runs
- testing symbolic tasks across multiple representational shells
- adding OCR or layout-sensitive variants
- comparing reasoning expansion before and after container repair
- extending the case toward stronger F7 to F2 or F7 to F1 boundary pressure

### Community boundary rule

Contributors should preserve the official logic:

- route first
- explain why primary not secondary
- show the first repair move
- keep replay outputs understandable
- do not turn the demo into an unreadable formalism jungle

For contribution structure, see:

- [Community Fix Lab](../../../community/README.md)
- [Contribution Checklist](../../../templates/contribution-checklist.md)
- [Fix Recipe Template](../../../templates/fix-recipe-template.md)

---

## 13. Why this demo matters

This demo teaches one clean lesson:

> if the box carrying the structure is weak, repair the box first

That is why this is the fourth flagship demo.

It turns F7 from an abstract family label into a practical debugging move.

---

## One-line version

**Demo 4 shows that some reasoning-looking failures are container-first, and that correct routing changes the first repair move from generic reasoning pressure to explicit descriptor and formal container repair.**

---

## Next steps

After this page, most readers continue with:

1. [Back to the demo pack index](../README.md)
2. [Back to AI Eval Evidence](../../../../ai-eval-evidence.md)
3. [Back to the Atlas landing page](../../../../../wfgy-ai-problem-map-troubleshooting-atlas.md)
4. [Open the Atlas Router TXT](../../../../troubleshooting-atlas-router-v1.txt)

If this demo helped you understand the Atlas, consider:

- [starring the WFGY repo](https://github.com/onestardao/WFGY)
- opening an issue
- testing the replay artifacts
- comparing v1 and v2 notebook presentation
- using the demo as a pattern for your own container-first cases

---

## Back to the main page

Read the full product page here:  
[Problem Map 3.0 Troubleshooting Atlas](../../../../../wfgy-ai-problem-map-troubleshooting-atlas.md)
