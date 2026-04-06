---
name: codex-project-insights
description: Cross-session audit using weighted scoring to generate ranked rule integrations.
---

# codex-project-insights

## Trigger
Use for periodic project-level audits (manual or cron).

## Inputs
- `~/.codex/sessions/*.jsonl` (default `--sessions-root`)
- `~/.copilot/session-state/*/` (via `--extra-sessions-root`)
- `~/.codex/history.jsonl`

## Scoring
- `half_life_days = 21`
- `score = 0.55*short_window + 0.30*long_window + 0.15*severity`
- `short_window = 14 days`
- `long_window = 90 days`
- `add threshold = 0.65` (2 consecutive cycles)
- `remove threshold = 0.25` (4 consecutive cycles)

## Workflow
1. Aggregate event signals across sessions.
2. Apply time decay and scoring model.
3. Rank signals by score.
4. Generate integration candidates with threshold decisions.
5. Respect cooldown and max rules per cycle.
6. Integrate accepted rules directly into `.agents/AGENTS.md`.
7. If running full cycle, enforce commit guard before auto-commit.

## Tooling
- Standalone scoring:
  - `.agents/skills/custom/codex-project-insights/scripts/project_insights.py`
- Full cycle orchestration:
  - `.agents/skills/custom/codex-project-insights/scripts/self_evolve_cycle.py`

## Output
- `insights-<timestamp>.json`
- `integration-<timestamp>.json`
- `cycle-<timestamp>.json` (if full cycle)
- ranked rows with `score`
- add/remove candidate sets and integration results
