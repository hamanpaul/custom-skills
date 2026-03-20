---
name: codex-lesson
description: Single-session retrospective that generates rule integration candidates with evidence.
---

# codex-lesson

## Trigger
Use after a task/session ends to capture immediate lessons.

## Inputs
- Target session JSONL (or latest session)
- Current AGENTS/skill rules

## Workflow
1. Parse session events and identify friction signals.
2. Extract evidence from concrete event counts and traces.
3. Produce rule integration candidates:
   - rule addition
   - rule clarification
   - rule removal candidate
4. If approved by decision gate, integrate directly into `.agents/AGENTS.md`.
5. Emit a structured report with references.

## Output
- `lesson-<timestamp>.json`
- `lesson-<timestamp>.md`
- section: `rule integration`
- section: `evidence`
- section: `session metadata`
