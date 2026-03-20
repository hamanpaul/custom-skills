---
name: coordinator
description: Orchestrate multi-agent short-lived jobs with run/jobs/stat/stop/kill/cron-run plus relay send/replay.
---

# coordinator

## Trigger
Use when user requests:
- 多 agent 協作
- 單專案多線開發
- coordinator run/jobs/stat/stop/kill
- cron-run 排程協作
- relay 訊息轉發或 replay

## Goal
Route to the right multi-agent mechanism with provider-aware defaults:
- If provider/runtime is `codex` and user did not explicitly ask for coordinator-specific flows, use Codex native multi-agent.
- Otherwise, use one coordinator job to run bounded collaboration with observable state and replayable relay logs.

## Routing Decision (provider-aware)
1) Prefer Codex native multi-agent when all are true:
- current runtime/provider is `codex`
- request is generic multi-agent collaboration (no explicit coordinator command requirement)

2) Use coordinator job flow when any are true:
- user explicitly asks for `coordinator.sh` / `run|jobs|stat|stop|kill`
- user explicitly asks for `relay-send` / `relay-replay`
- user explicitly asks for `cron-run` lock-aware non-reentrant behavior
- cross-provider orchestration is required (`codex` / `copilot` / `gemini`)

## Codex Native Multi-agent Path
- Do not create coordinator job in this path.
- Use Codex built-in sub-agent flow (`spawn_agent` / `send_input` / `wait` / `close_agent`).
- Use `/agent` for thread switching and `/ps` `/clean` for background terminal management as needed.
- Verify feature status when needed:
```bash
codex features list | rg '^multi_agent'
# if disabled:
codex features enable multi_agent
```

## Runtime Defaults
- state root: `~/.agents/state/coordinator`
- provider: `codex`（可切 `copilot` / `gemini`）
- provider default model/reasoning：
  - `codex`: `gpt-5.3-codex` / `xhigh`
  - `copilot`: `gpt-5-mini` / `high`
  - `gemini`: `gemini-3-pro-preview` / `""`
- default write scope: `.agents/**`

## Commands
```bash
# run job
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh \
  run --topic "mesh-design" --to-agents "agentA,agentB" --hold-open

# inspect jobs
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh jobs --limit 20

# inspect one job
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh stat <job-id>

# stop / kill
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh stop <job-id>
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh kill <job-id>

# relay send + replay
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh relay-send <job-id> \
  --from-agent agentA --to-agent agentB --intent ask --payload-text "question"
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh relay-replay <job-id>

# cron mode (lock-aware, non-reentrant)
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh \
  cron-run --topic nightly --to-agents "agentA,agentB"

# sdk worker mode (codex delegate)
/home/paul_chen/.agents/skills/custom/coordinator/scripts/coordinator.sh \
  run --topic "mesh-design" --to-agents "agentA,agentB" --provider codex --worker-mode sdk \
  --sdk-script /home/paul_chen/.agents/tools/agent-core/scripts/copilot_sdk_orchestrator.mjs \
  --sdk-delegate-template "codex exec -c model={model_q} -c model_reasoning_effort={reasoning_q} {prompt_q}"
```

`--sdk-delegate-template` 建議優先使用 shell-safe placeholders：
- `{provider_q}` `{model_q}` `{reasoning_q}` `{cwd_q}` `{prompt_q}`

## Safety Rules
- Mailbox 僅存 metadata，不存全文對話。
- Relay 僅允許 job 內已宣告 agent（含 `coordinator`）。
- job 非 `running` 時拒絕 relay-send。
- write scope 與現有 running job 重疊時拒絕新 job（`blocked_by_scope_conflict`）。

## Output Contract
Always report:
- command status
- `job_id` / `trace_id`（若有）
- state/log file path
- blocked reason（若失敗）

For Codex native path, report instead:
- routed path (`codex-native-multi-agent`)
- feature status (`multi_agent` enabled/disabled)
- whether coordinator job creation was skipped
