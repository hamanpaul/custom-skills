<!--
AI_NOTE_START

Document role:
This file is the reusable template for Colab-based fix contributions inside the Atlas Fixes layer.

How to use this file:
1. Copy this template when creating a new Colab demo or notebook-based fix contribution.
2. Use this file after reading:
   - [Community Fix Lab](../community/README.md)
   - [Contribution Checklist](./contribution-checklist.md)
   - [Fix Recipe Template](./fix-recipe-template.md)
3. Keep the order:
   - atlas routing first
   - first repair move second
   - notebook execution third
   - deeper WFGY escalation fourth if needed

What this file is:
- A standard Colab contribution template
- A lightweight notebook documentation scaffold
- A contributor-facing structure for runnable demo assets

What this file is not:
- Not the atlas core
- Not the official fix surface itself
- Not proof that a notebook is universally good
- Not a replacement for maintainer review

Reading discipline for AI:
- Do not skip routing context.
- Do not present a notebook as a universal solution.
- Keep notebook contributions scoped, reproducible, and easy to inspect.
- Preserve route-first discipline.

AI_NOTE_END
-->

# Colab Template

## Title

Replace this line with a short clear title.

Example:  
`F4 Readiness Gate Demo - Minimal closure repair notebook`

---

## 0. Quick summary

Write 1 to 3 short sentences.

Example:  
This notebook demonstrates a workflow failure caused by missing readiness checks.  
It compares the broken baseline with a repaired version that adds a simple readiness gate.

---

## 1. Notebook type

Choose one or more:

- demo notebook
- benchmark rerun
- repair notebook
- trace notebook
- reproduction notebook
- comparison notebook

---

## 2. Atlas routing context

**Primary family**  
`F?`

**Secondary family**  
`F?` or `None`

**Broken invariant**  
Write one short sentence.

**Best current fit**  
Write the nearest node, family entry, or edge-fit wording.

**Why this notebook belongs here**  
Write 2 to 4 short sentences.

---

## 3. Problem this notebook addresses

Describe the specific problem this notebook demonstrates.

Useful questions:

- what is broken in the baseline
- why a notebook is useful here
- what first repair move is being tested
- what this notebook is not trying to solve

Keep this short and concrete.

---

## 4. Intended use

State clearly how this notebook should be used.

Examples:

- first public demo
- contributor reproduction
- benchmark sanity check
- teaching notebook
- route-first repair demonstration

Optional format:

**Use stage**  
`...`

**Target user**  
`...`

**Expected runtime**  
`...`

---

## 5. Required inputs

List the minimum inputs.

Examples:

- corpus
- query set
- schema file
- workflow config
- notebook parameters
- baseline JSON
- expected JSON

Use a short format like:

```text
Input A:
Input B:
Input C:
````

---

## 6. Notebook sections

A good notebook should usually contain these sections.

### Section A · Setup

What the notebook loads or installs.

### Section B · Case framing

What case is being shown and how it routes in the atlas.

### Section C · Broken baseline

Show the failure first.

### Section D · First repair move

Apply the family-level first repair move.

### Section E · Re-run

Run the repaired version.

### Section F · Comparison

Show before / after differences.

### Section G · Optional WFGY escalation

Show how the same case could be explored more deeply if needed.

---

## 7. Baseline failure

Describe the broken baseline.

Useful questions:

* what is the baseline workflow
* what fails first
* what visible symptom appears
* why is this failure interesting

Optional mini format:

**Baseline setup**
`...`

**Broken behavior**
`...`

**Failure note**
`...`

---

## 8. First repair move

Describe the first repair move being tested.

Useful questions:

* what intervention is being applied
* why it is the correct first move
* what should improve after the intervention

Optional mini format:

**Repair action**
`...`

**Why this is first**
`...`

**Expected improvement**
`...`

---

## 9. Expected outputs

Describe what the notebook should produce.

Examples:

* before / after metrics
* clearer trace output
* better schema pass rate
* fewer wrong anchors
* successful closure
* improved support rate

Optional format:

**Before**
`...`

**After**
`...`

**Success signal**
`...`

---

## 10. Suggested evaluation fields

List only useful fields.

Examples:

* `support_rate`
* `closure_success`
* `schema_pass_rate`
* `trace_completeness`
* `wrong_anchor_rate`
* `field_loss_count`

Optional mini block:

```text
Metric 1:
Metric 2:
Metric 3:
```

---

## 11. Misrepair warning

This section is required.

### Wrong first move

`...`

### Why it is tempting

`...`

### Why this notebook is not meant for that

`...`

This helps prevent notebooks from teaching the wrong reflex.

---

## 12. Optional WFGY escalation

Use this only if deeper WFGY exploration is relevant.

### When to escalate

`...`

### What should be passed into WFGY

* routed family
* broken invariant
* first repair already attempted
* unresolved pressure

### What WFGY is expected to add

`...`

Do not use this section to skip atlas routing.

---

## 13. Files included

List the files included.

Example:

* `demo.ipynb`
* `input.json`
* `expected_output.json`
* `README.md`

---

## 14. Runtime and dependency notes

Be explicit.

Examples:

* Python version
* notebook runtime type
* external packages
* API keys if needed
* GPU not required
* internet required or not required

Short, clear notes are enough.

---

## 15. Limitations

Be honest.

Examples:

* toy dataset only
* small case only
* one model family only
* partial demo, not full system benchmark
* notebook proves first move, not full closure

---

## 16. One-line maintainer note

Write one short line that helps review the contribution.

Example:
Small F4 closure demo notebook with before / after run and simple success metric.

---

## 17. Copy-paste mini skeleton

Use this when you want the fastest possible start.

```md
# Title

## 0. Quick summary
...

## 1. Notebook type
...

## 2. Atlas routing context
Primary family:
Secondary family:
Broken invariant:
Best current fit:
Why this notebook belongs here:

## 3. Problem this notebook addresses
...

## 4. Intended use
Use stage:
Target user:
Expected runtime:

## 5. Required inputs
...

## 6. Notebook sections
A.
B.
C.
D.
E.
F.
G.

## 7. Baseline failure
...

## 8. First repair move
...

## 9. Expected outputs
...

## 10. Suggested evaluation fields
...

## 11. Misrepair warning
Wrong first move:
Why it is tempting:
Why this notebook is not meant for that:

## 12. Optional WFGY escalation
...

## 13. Files included
...

## 14. Runtime and dependency notes
...

## 15. Limitations
...

## 16. One-line maintainer note
...
```

---

## 18. Closing note

A good notebook contribution does not need to be huge.

It only needs to be:

* routed
* runnable
* scoped
* inspectable
* honest about limits

