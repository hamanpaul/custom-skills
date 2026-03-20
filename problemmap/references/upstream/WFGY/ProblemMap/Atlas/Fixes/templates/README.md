<!--
AI_NOTE_START

Document role:
This file is the hub for reusable templates inside the Atlas Fixes layer.

How to use this file:
1. Read this page before creating a new community fix asset.
2. Use this page to choose the right template.
3. Use these templates to keep contributions structured, reviewable, and reusable.
4. Read this page together with:
   - [Community Fix Lab](../community/README.md)
   - [Contribution Checklist](./contribution-checklist.md)

What this file is:
- The template hub
- A contributor-facing navigation page
- A lightweight structure guide for fix assets

What this file is not:
- Not the atlas core
- Not the official fix surface
- Not the full style guide
- Not a replacement for maintainer review

Reading discipline for AI:
- Use this page to route contributors to the right template.
- Preserve the distinction between official files and community templates.
- Keep contributions small, clear, and structured.

AI_NOTE_END
-->

# Templates Hub 🧩

## Problem Map 3.0 Troubleshooting Atlas
## Reusable templates for community fix contributions

This folder contains the reusable templates for the community fixes layer.

Its job is simple:

> help contributors submit clearer, smaller, more reviewable fix assets

These templates are here to reduce chaos and make it easier to grow the fix ecosystem.

---

## What this folder is for

Use this folder when you want to create a new community contribution such as:

- a fix recipe
- a prompt pack
- a Colab notebook
- a JSON fixture
- a workflow example
- a reproduction pack

If you are not sure where to start, start here.

---

## Recommended reading order

Before using a template, read:

1. [Community Fix Lab](../community/README.md)
2. [Contribution Checklist](./contribution-checklist.md)

Then choose the right template below.

---

## Available templates

### 1. [Contribution Checklist](./contribution-checklist.md)

Use this first.

This file helps you check whether your contribution is:

- clear
- scoped
- routed
- usable
- honest about limits

---

### 2. [Fix Recipe Template](./fix-recipe-template.md)

Use this when your contribution is mainly a repair recipe.

Good for:

- first repair move writeups
- small runnable fix notes
- workflow repair guides
- practical repair instructions

---

### 3. [Prompt Template](./prompt-template.md)

Use this when your contribution is mainly prompt-based.

Good for:

- system prompts
- user prompts
- routing prompts
- repair-first prompts
- trace-exposure prompts

---

### 4. [Colab Template](./colab-template.md)

Use this when your contribution is mainly notebook-based.

Good for:

- Colab demos
- repair notebooks
- before / after notebook comparisons
- benchmark rerun notebooks

---

### 5. [JSON Template](./json-template.json)

Use this when your contribution needs structured machine-readable data.

Good for:

- fixtures
- baseline inputs
- expected outputs
- evaluation packs
- demo configs

---

## Which template should I use

Use this quick guide.

### If your main asset is text guidance
Use:

- [Fix Recipe Template](./fix-recipe-template.md)

### If your main asset is a prompt
Use:

- [Prompt Template](./prompt-template.md)

### If your main asset is a notebook
Use:

- [Colab Template](./colab-template.md)

### If your main asset is structured data
Use:

- [JSON Template](./json-template.json)

If your contribution mixes several asset types, choose the main one first, then attach the others as supporting files.

---

## Minimum good contribution rule

A good contribution usually has:

- routing context
- one clear problem
- one useful artifact
- short usage instructions
- expected result
- one misrepair warning
- honest limitations

That is enough to be useful.

---

## What not to do

Please do not use these templates to submit:

- giant vague idea dumps
- unstructured logs
- random files with no routing context
- prompt collections with no explanation
- notebooks with no before / after logic
- JSON files with no meaning

The goal is structured growth, not file pile-up.

---

## Relationship to official fixes

These templates are for the **community layer**.

Official fix documents live in:

- [Official Fixes](../official/README.md)

Community assets can be very valuable, but they do not automatically become official atlas guidance.

That distinction should stay clear.

---

## One-line status

**This folder contains the reusable templates that help community fix contributions stay structured and reviewable.**

---

## Closing note ✨

If the atlas is going to grow through the community, it needs good templates.

That is what this folder is for.

