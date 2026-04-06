---
name: evolve
description: Run full self-maintenance cycle (insights + lesson + ACP decision + AGENTS integration + optional commit) across Codex and Copilot sessions.
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
- codex adapter: `.agents/skills/custom/evolve/scripts/codex_exec_acp_adapter.py`

## Session Sources
- **Codex sessions**: `~/.codex/sessions/*.jsonl` (default `--sessions-root`)
- **Copilot sessions**: `~/.copilot/session-state/*/` (via `--extra-sessions-root`)

To scan both Codex and Copilot sessions in one cycle:
```bash
python3 scripts/self_evolve_cycle.py \
  --sessions-root ~/.codex/sessions \
  --extra-sessions-root ~/.copilot/session-state
```

## Knowledge Base
- `references/techvault-practices.md` — Agent best practices extracted from TechVault
  (context efficiency, session archetypes, API resilience, SLO patterns, skill design)

## Packaged Helper
- `scripts/git_gate.sh`
- `scripts/self_evolve_cycle.py`
- `scripts/codex_exec_acp_adapter.py`

## Command
```bash
python3 /home/paul_chen/.agents/skills/custom/evolve/scripts/self_evolve_cycle.py \
  --repo-root /home/paul_chen \
  --agents-root /home/paul_chen/.agents \
  --sessions-root /home/paul_chen/.codex/sessions \
  --extra-sessions-root /home/paul_chen/.copilot/session-state \
  --decision-mode acp \
  --acp-provider codex
```

## Optional Flags
- `--auto-commit`: commit guarded changes when repo is clean.
- `--skip-lesson`: skip single-session lesson stage.
- `--acp-provider copilot|gemini`: switch provider.
- `--summary-out <path>`: deterministic output path for CI/manual audit.
- `--extra-sessions-root <path>`: additional session directory to scan (e.g. Copilot sessions).

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

## Skill Deployment
- Source: `~/prj_pri/custom-skills/evolve/`
- `~/.agent` is a symlink → `~/.agents` (same directory)
- Codex custom skills: `~/.codex/skills/`
- Copilot common skills: `~/.agents/skills/`
- This skill is NOT auto-deployed; copy or symlink manually
