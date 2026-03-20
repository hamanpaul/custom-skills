---
name: evolve
description: Run full self-maintenance cycle (insights + lesson + ACP decision + AGENTS integration + optional commit) in one trigger.
---

# evolve

## Trigger
Use when user requests:
- 自主維護
- 自我進化
- evolve
- full self-evolve cycle
- 一鍵更新 AGENTS 規則

## Goal
Execute one complete self-maintenance cycle and return verifiable artifacts.

## Default Runtime
- decision mode: `acp`
- ACP provider: `codex`
- codex model: `gpt-5.3-codex`
- codex reasoning: `xhigh`
- codex adapter: `.agents/tools/codex-insights/scripts/codex_exec_acp_adapter.py`

## Packaged Helper
- `scripts/git_gate.sh`

## Command
```bash
python3 /home/paul_chen/.agents/tools/codex-insights/scripts/self_evolve_cycle.py \
  --repo-root /home/paul_chen \
  --agents-root /home/paul_chen/.agents \
  --sessions-root /home/paul_chen/.codex/sessions \
  --decision-mode acp \
  --acp-provider codex
```

## Optional Flags
- `--auto-commit`: commit guarded changes when repo is clean.
- `--skip-lesson`: skip single-session lesson stage.
- `--acp-provider copilot|gemini`: switch provider.
- `--summary-out <path>`: deterministic output path for CI/manual audit.

## Verification
After execution, check:
- summary JSON exists and `status=ok`
- decision report exists
- integration report exists
- `.agents/AGENTS.md` managed block changed only when accepted rules > 0

## Output Contract
Always report:
- summary file path
- decision mode and backend
- accepted/rejected proposal counts
- whether `.agents/AGENTS.md` was updated
- commit result (`performed/reason`)
