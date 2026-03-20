---
name: ftrace-capture
description: Bounded ftrace capture workflow for kernel path tracing.
depends_on:
  - ebpf-baseline
used_with:
  - ebpf-verify
related:
  - ebpf-ftrace
anti_patterns:
  - long-running-capture
---

# ftrace-capture

## Trigger
- 當任務需要抓取 `trace`/`trace_pipe` 的可重播證據時。

## Input
- 已完成 baseline。
- 目標 tracer 與事件/函式關鍵字。

## Flow
1. 設定 tracer 與必要 filter。
2. 啟動 bounded capture（時間/筆數有上限）。
3. 匯出 trace 檔與命令輸出路徑。

## Output
- `trace_artifacts`
- `capture_window`
- `commands_run`

## Quick Commands
```bash
echo function | sudo tee /sys/kernel/tracing/current_tracer >/dev/null
echo 1 | sudo tee /sys/kernel/tracing/tracing_on >/dev/null
sleep 2
echo 0 | sudo tee /sys/kernel/tracing/tracing_on >/dev/null
sudo cat /sys/kernel/tracing/trace | tail -n 200
sudo timeout 5 cat /sys/kernel/tracing/trace_pipe
```

## Links
- 依賴 `[[ebpf-baseline]]`。
- 完成後交由 `[[ebpf-verify]]` 驗證。
