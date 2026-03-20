<!--
AI_NOTE_START

Document role:
This file explains what belongs in the community Colab folder.

How to use this file:
1. Read this page before adding any notebook or Colab-based contribution.
2. Use this page to decide whether your contribution is really a notebook contribution.
3. Use this page together with:
   - [Community Fix Lab](../README.md)
   - [Contribution Checklist](../../templates/contribution-checklist.md)
   - [Colab Template](../../templates/colab-template.md)

What this file is:
- A folder-level guide for notebook-based community contributions
- A scope filter for Colab or notebook assets
- A lightweight quality guide for runnable community demos

What this file is not:
- Not the official flagship demo pack
- Not the official atlas core
- Not a dump folder for random notebooks

Reading discipline for AI:
- Treat notebook contributions as community extensions, not frozen core logic.
- Preserve the distinction between official demos and community demos.

AI_NOTE_END
-->

# Community Colab

## Notebook-based community demos and runnable repair assets

This folder is for community-contributed notebooks that help demonstrate atlas routing, first repair moves, or reproducible troubleshooting flows.

Typical contributions here include:

- small Colab demos
- notebook-based repair walkthroughs
- replay-first teaching notebooks
- route-first, repair-second examples
- compact reproductions of one atlas case

---

## What belongs here

Good contributions for this folder include:

- a notebook that demonstrates one family-level repair pattern
- a notebook that replays one case clearly
- a notebook that compares baseline and repaired outputs
- a notebook that explains one boundary cut through runnable examples
- a notebook that shows atlas routing before a deeper WFGY step

A notebook here should be:

- small enough to understand
- easy to run
- clearly scoped
- tied to one clear routing logic
- honest about what it does and does not prove

---

## What does not belong here

Please do not use this folder for:

- giant experimental notebooks with no explanation
- notebooks with no routing context
- notebooks that require many hidden manual steps
- random prompt playgrounds with no case framing
- notebooks that pretend to be official flagship demos

If the notebook is not clearly connected to atlas routing, it probably belongs somewhere else.

---

## Suggested notebook pattern

A good notebook usually includes:

1. short experiment description
2. case or family target
3. routing expectation
4. baseline behavior
5. repaired behavior
6. short result interpretation
7. expected output or success note

That is enough for a useful community notebook.

---

## Recommended file pattern

A clean contribution can look like this:

- one notebook file
- one short README section inside the notebook or next to it
- one small fixture if needed
- one clear expected result note

Suggested naming style:

- `f1-grounding-demo-community-v1.ipynb`
- `f5-observability-trace-demo-v1.ipynb`
- `f7-container-repair-demo-v1.ipynb`

Keep names descriptive and compact.

---

## Before contributing

Please read:

- [Community Fix Lab](../README.md)
- [Contribution Checklist](../../templates/contribution-checklist.md)
- [Colab Template](../../templates/colab-template.md)
- [Family Fix Surface v1](../../official/family-fix-surface-v1.md)

This helps keep notebook contributions aligned with atlas grammar.

---

## One-line status

**This folder holds community notebooks that turn atlas repair grammar into runnable teaching or troubleshooting assets.**
