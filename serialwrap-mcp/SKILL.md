---
name: serialwrap-mcp
description: Use serialwrap broker + MCP for multi-agent UART access with single-writer arbitration, RAW logging, and session-safe command execution. Trigger when tasks involve UART command execution, UART state collection, multi-agent UART coordination, or UART evidence export.
---

# serialwrap-mcp Agent Skill

## 目的
定義 Agent 在 UART 任務中使用 `serialwrap`/`serialwrap-mcp` 的觸發條件、操作順序與安全邊界，避免直接碰觸實體 UART 造成資料失真或衝突。

## 何時該使用
- 需要多 Agent 共用同一 UART 並保證單寫入仲裁。
- 需要完整 RAW log（含 timestamp/source/cmd_id/seq/crc）做回放或稽核。
- 需要在人類 console 與 Agent 任務同時運作下保持一致視圖。
- 需要以 MCP 工具模式把 UART 操作整合到 Agent workflow。

## 何時不要使用
- 單次、一次性、無需追溯的本機 serial 測試。
- target 不經 UART 而經 SSH/ADB 等其他通道，且不需 UART 證據鏈。

## 前置條件
- `serialwrapd` 必須啟動。
- 目標 session 必須是 `READY`。
- profile 與 target 已綁定（`session bind` + `session attach` 至少完成一次）。

## 標準執行順序
1. 健康檢查：`serialwrap_get_health` 或 CLI `serialwrap daemon status`。
2. 探測資源：`serialwrap_list_sessions`、`serialwrap_list_devices`，或 CLI `session list` / `device list`。
3. 鎖定目標：`serialwrap_get_session_state(selector)`，必要時先做 `serialwrap_self_test`。
4. 若 session 未 READY、tty 已變更、或 bridge stale，可用 `serialwrap_bind_session` / `serialwrap_attach_session` / `serialwrap_recover_session`。
5. 提交命令：`serialwrap_submit_command`，必填 `source` 與 `selector`。
6. `line` 前景命令：用 `serialwrap_get_command` 或 CLI `cmd status --cmd-id ...` 直接讀 `stdout`。
7. `background` 命令：用 `serialwrap_tail_command_result` 或 CLI `cmd result-tail --cmd-id ...` 增量取回 chunk。
8. `interactive` 任務：用 `interactive-open/send/status/close`，不要拿 `cmd submit` 硬跑全螢幕互動程式。
9. 需要完整證據時，再拉 CLI `log tail-raw` / `wal export`。

## MCP Tool 對應
- `serialwrap_get_health` -> `health.status`
- `serialwrap_list_devices` -> `device.list`
- `serialwrap_list_sessions` -> `session.list`
- `serialwrap_get_session_state` -> `session.get_state`
- `serialwrap_bind_session` -> `session.bind`
- `serialwrap_attach_session` -> `session.attach`
- `serialwrap_self_test` -> `session.self_test`
- `serialwrap_recover_session` -> `session.recover`
- `serialwrap_submit_command` -> `command.submit`
- `serialwrap_get_command` -> `command.get`
- `serialwrap_tail_command_result` -> `command.result_tail`
- `serialwrap_clear_session` -> `session.clear`
- `serialwrap_attach_console` -> `session.console_attach`
- `serialwrap_detach_console` -> `session.console_detach`
- `serialwrap_list_consoles` -> `session.console_list`
- `serialwrap_open_interactive` -> `session.interactive_open`
- `serialwrap_send_interactive_keys` -> `session.interactive_send`
- `serialwrap_get_interactive_status` -> `session.interactive_status`
- `serialwrap_close_interactive` -> `session.interactive_close`
- `serialwrap_tail_results` -> `result.tail`（deprecated alias）

## MCP 參數規範
- `serialwrap_submit_command`
  - 必填：`selector`, `cmd`
  - 建議：`source="agent:<name>"`, `mode="line|background|interactive"`, `timeout_s`, `priority`
- `serialwrap_get_command`
  - 必填：`cmd_id`
- `serialwrap_tail_command_result`
  - 必填：`cmd_id`
  - 建議：`from_chunk`, `limit`
- `serialwrap_get_session_state`
  - 必填：`selector`（`session_id | COMx | alias`）

## CLI 快速對照
- `serialwrap list` 已移除，現在改用：
  - `serialwrap daemon status`
  - `serialwrap device list`
  - `serialwrap session list`
  - `serialwrap session self-test --selector COM2`
  - `serialwrap cmd submit --selector COM2 --cmd 'pwd' --source agent:diag --mode line --cmd-timeout 10`
  - `serialwrap cmd status --cmd-id <cmd_id>`
  - `serialwrap cmd result-tail --cmd-id <cmd_id> --from-chunk 0 --limit 100`

## 實務注意事項
- `line` 命令不要用 `cmd result-tail` 讀結果；它是給 `background` capture 用的。`line` 請直接看 `cmd status` / `command.get.stdout`。
- 長命令或有狀態副作用的命令（例如 `ob sync`, 套件升級, 韌體操作）要給足 `cmd-timeout`。timeout 太短時 broker 可能以 `CTRL_C` 回收，target 端會留下半完成狀態。
- 若 target 報 `Another ... already running`，先檢查 target 端是否真的還有活著的 process；若沒有，再做最小清理，例如移除空的 stale lock 目錄。
- `cmd status` 若仍是 `running`，不要盲目重送相同命令，先確認 target 端是否仍在執行。
- 每筆自動化命令必填 `source`，不可省略，確保追蹤性。

## 安全規則
- 禁止 Agent 直接寫 `/dev/ttyUSB*` 或 `/dev/ttyACM*`。
- 禁止繞過 broker 自行開多個 serial writer。
- 長流命令（`logread -f`, `tcpdump`, kernel debug）優先用 `mode=background`；若必須前景執行，必須明確設定較長 timeout。
- 卡住時先 `serialwrap_self_test`，再決定是否 `serialwrap_recover_session`。

## 最小可用範例
```bash
/home/paul_chen/.paul_tools/serialwrap daemon status
/home/paul_chen/.paul_tools/serialwrap session self-test --selector COM2
/home/paul_chen/.paul_tools/serialwrap cmd submit --selector COM2 --cmd 'ob sync --path ~/notes' --source agent:diag --mode line --cmd-timeout 300
/home/paul_chen/.paul_tools/serialwrap cmd status --cmd-id <cmd_id>
```

## 參考檔案
- `/home/paul_chen/prj_pri/ser-dep/skills.md`
- `/home/paul_chen/prj_pri/ser-dep/docs/serialwrap-spec.md`
