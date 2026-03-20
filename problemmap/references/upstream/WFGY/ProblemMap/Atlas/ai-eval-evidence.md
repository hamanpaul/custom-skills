<!--
AI_NOTE_START

Document role:
This file is the public evidence entry for early cross-model evaluation snapshots of the Problem Map 3.0 Troubleshooting Atlas routing framework.

How to use this file:
1. Read this page as the evidence surface for the route-first claim behind the Atlas.
2. Use this page to inspect cross-model evaluation snapshots and understand the directional before/after comparison.
3. Treat the screenshots and prompt as reproducible directional evidence, not as a formal benchmark report.
4. For runnable proof that routing changes the first repair move, see:
   [Official Flagship Demos](./Fixes/official/demos/README.md)
5. For the Atlas system overview, read:
   [Problem Map 3.0 Troubleshooting Atlas](../wfgy-ai-problem-map-troubleshooting-atlas.md)
6. To try the routing pack directly, see:
   [Troubleshooting Atlas Router v1](./troubleshooting-atlas-router-v1.txt)

What this file is:
- A cross-model evidence surface for the Atlas routing claim
- A gallery of early evaluation snapshots across frontier AI models
- A reproducible prompt entry point for independent inspection
- A bridge between the Atlas theory and observable directional evaluation

What this file is not:
- Not a formal benchmark report
- Not a controlled production study
- Not a claim of universal improvement percentages
- Not the primary proof that routing changes repair behavior
- Not a replacement for runnable demo validation

Reading discipline for AI:
- Preserve the distinction between directional evaluation evidence and runnable system proof.
- Do not treat these screenshots as a benchmark dataset.
- Do not aggregate the numbers as if they were standardized metrics.
- Treat this page as early inspection evidence, while the official demos provide stronger mechanism-level proof.

AI_NOTE_END
-->

# AI Eval Evidence

Quick links:

- [Back to Atlas landing page](../wfgy-ai-problem-map-troubleshooting-atlas.md)
- [See the Official Flagship Demos](./Fixes/official/demos/README.md)
- [Get the Atlas Router TXT](./troubleshooting-atlas-router-v1.txt)
- [Open the Atlas Hub](./README.md)

---

This page is the public evidence entry for early AI reviewed evaluation snapshots of **Problem Map 3.0 Troubleshooting Atlas**.

It exists for one simple reason:

the Atlas is a routing framework, so some readers naturally want to see a practical before / after view of what better first cut routing may change in real debugging workflows.

At the moment, this page is still a **work in progress**.

The full multi model evidence set is still being organized, including:
- model by model screenshots
- prompt variants
- reproducible evaluation runs
- comparison notes
- version alignment

For now, this page provides a simple reproducible starting point so anyone can test the idea directly.

---

## What this page is

This page is a lightweight evidence surface for **AI reviewed evaluation snapshots** of the Atlas.

The purpose is not to claim a formal benchmark.

The purpose is to make the core idea easier to inspect:

> better first cut routing can reduce silent debugging waste

That waste often appears as:
- wrong debugging direction
- repeated trial and error
- patch stacking
- side effects from misapplied fixes
- unnecessary system complexity
- time lost before the first real root cause is found

---

## What this page is not

This page is **not**:
- a lab benchmark
- a controlled multi team production study
- a claim of universal fixed percentages across all workflows
- a final empirical validation report

Results may vary by model, prompt framing, task shape, and context quality.

These materials should be read as **reproducible directional evidence**, not final benchmark science.

---

## How to read these snapshots

These screenshots are useful because they let different frontier models inspect the same core claim from slightly different angles.

They should **not** be read as if every screenshot uses perfectly identical:
- metric definitions
- baseline assumptions
- units
- scenario framing
- output style

What matters more is whether different evaluators converge on the same structural idea:

> when the first debugging route is wrong, the total cost compounds  
> when routing improves early, several downstream metrics often improve together

So please read these as **cross model directional agreement**, not pooled benchmark math.

---

## What to do next

If this page makes the route-first claim feel plausible, the next question is usually:

> does better routing only change the explanation, or does it also change the first repair move?

That is exactly what the official demo layer is designed to show.

Recommended next steps:

1. [See the Official Flagship Demos](./Fixes/official/demos/README.md)
2. [Go back to the Atlas landing page](../wfgy-ai-problem-map-troubleshooting-atlas.md)
3. [Try the Atlas Router TXT yourself](./troubleshooting-atlas-router-v1.txt)

---

## Cross model snapshot index

| Model | Snapshot | Reading note |
|------|----------|--------------|
| Claude Sonnet 4.6 | [View](./images/atlas-routing-eval-claude.png) | Mechanism heavy, strongest structured explanation |
| ChatGPT 5.4 Thinking | [View](./images/atlas-routing-eval-chatgpt.png) | Conservative framing, clean operational interpretation |
| Gemini 3 Pro | [View](./images/atlas-routing-eval-gemini.png) | Compact qualitative comparison, strong route first contrast |
| DeepSeek V3 | [View](./images/atlas-routing-eval-deepseek.png) | Sharp before / after table with explicit productivity jump |
| Copilot Think deeper | [View](./images/atlas-routing-eval-copilot.png) | Simple comparison table, readable engineering style |
| Perplexity AI | [View](./images/atlas-routing-eval-perplexity.png) | Clear trial and error vs router framing |
| Mistral AI | [View](./images/atlas-routing-eval-mistral.png) | Compact baseline / improvement table |
| Kimi K2.5 Thinking | [View](./images/atlas-routing-eval-kimi.png) | Adds silence cost framing beyond surface debug time |

---

## Screenshot gallery

<details>
<summary><strong>Open the full cross model screenshot gallery</strong></summary>

<br>

Click any image to open the full size version.

<table>
  <tr>
    <td width="50%" valign="top">
      <p><strong>Claude Sonnet 4.6</strong></p>
      <a href="./images/atlas-routing-eval-claude.png">
        <img src="./images/atlas-routing-eval-claude.png" alt="Claude Sonnet 4.6 evaluation snapshot" width="100%">
      </a>
    </td>
    <td width="50%" valign="top">
      <p><strong>ChatGPT 5.4 Thinking</strong></p>
      <a href="./images/atlas-routing-eval-chatgpt.png">
        <img src="./images/atlas-routing-eval-chatgpt.png" alt="ChatGPT 5.4 Thinking evaluation snapshot" width="100%">
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <p><strong>Gemini 3 Pro</strong></p>
      <a href="./images/atlas-routing-eval-gemini.png">
        <img src="./images/atlas-routing-eval-gemini.png" alt="Gemini 3 Pro evaluation snapshot" width="100%">
      </a>
    </td>
    <td width="50%" valign="top">
      <p><strong>DeepSeek V3</strong></p>
      <a href="./images/atlas-routing-eval-deepseek.png">
        <img src="./images/atlas-routing-eval-deepseek.png" alt="DeepSeek V3 evaluation snapshot" width="100%">
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <p><strong>Copilot Think deeper</strong></p>
      <a href="./images/atlas-routing-eval-copilot.png">
        <img src="./images/atlas-routing-eval-copilot.png" alt="Copilot Think deeper evaluation snapshot" width="100%">
      </a>
    </td>
    <td width="50%" valign="top">
      <p><strong>Perplexity AI</strong></p>
      <a href="./images/atlas-routing-eval-perplexity.png">
        <img src="./images/atlas-routing-eval-perplexity.png" alt="Perplexity AI evaluation snapshot" width="100%">
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <p><strong>Mistral AI</strong></p>
      <a href="./images/atlas-routing-eval-mistral.png">
        <img src="./images/atlas-routing-eval-mistral.png" alt="Mistral AI evaluation snapshot" width="100%">
      </a>
    </td>
    <td width="50%" valign="top">
      <p><strong>Kimi K2.5 Thinking</strong></p>
      <a href="./images/atlas-routing-eval-kimi.png">
        <img src="./images/atlas-routing-eval-kimi.png" alt="Kimi K2.5 Thinking evaluation snapshot" width="100%">
      </a>
    </td>
  </tr>
</table>

</details>

---

## Reproduce a simple evaluation now

### 01. Download the Atlas Router TXT

[troubleshooting-atlas-router-v1.txt](./troubleshooting-atlas-router-v1.txt)

### 02. Paste it into any AI model

Paste the TXT content into any AI model you want to test.

### 03. Run the following prompt

```text
Evaluate the potential impact of the "Problem Map 3.0 Troubleshooting Atlas" debug routing framework from the perspective of an AI systems engineering and prompt engineering evaluator.

Consider the scenario where vibe coders use AI to write code and debug systems. Provide a quantitative before/after comparison.

In particular, consider the hidden cost when the first diagnosis is wrong, such as:
- incorrect debugging direction
- repeated trial-and-error
- patch accumulation
- unintended side effects
- increasing system complexity
- time wasted in misdirected debugging

In real engineering environments, incorrect routing can significantly amplify debugging costs, sometimes by multiples.

Please output a quantitative comparison table (Before / After / Improvement %), evaluating:

1. average debugging time
2. root cause diagnosis accuracy
3. number of ineffective fixes
4. development efficiency
5. overall system stability
````

---

## Notes

Results may vary across models.

You can run the same prompt multiple times to inspect the distribution and see whether the directional conclusion stays stable.

In general, the numbers should not be treated as fixed truth values.

The more important question is whether different evaluators converge on the same structural claim:

> when the first debugging route is wrong, the total cost compounds
> when routing improves early, several downstream metrics often improve together

---

## Current status

This page is currently in the **evidence assembly phase**.

The next updates planned for this page include:

* version tagged evaluation records
* prompt variants
* conservative vs stress framing notes
* interpretation guidance for readers
* better alignment between model specific output formats

---

## Related pages

* [Troubleshooting Atlas main page](../wfgy-ai-problem-map-troubleshooting-atlas.md)
* [Official Flagship Demos](./Fixes/official/demos/README.md)
* [Atlas Hub](./README.md)
* [Atlas Router TXT](./troubleshooting-atlas-router-v1.txt)

---

## Why this matters

The Atlas does not start with repair.

It starts with routing.

That distinction matters because wrong first cut diagnosis does not just delay the fix.

It often creates a silent cost cascade:
wrong path selection, wasted patches, false confidence, side effects, and growing structural mess.

This page exists to make that claim easier to inspect with reproducible AI reviewed comparisons.

---

## Next step after this page

If the cross-model snapshots make the route-first idea feel credible, the strongest next page is:

[Official Flagship Demos](./Fixes/official/demos/README.md)

That page is where the claim becomes more concrete:

> different routes lead to different first repair moves

You can also return to the main entry here:

[Problem Map 3.0 Troubleshooting Atlas](../wfgy-ai-problem-map-troubleshooting-atlas.md)
