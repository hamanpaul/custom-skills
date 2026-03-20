---
name: ebpf-baseline
description: Baseline checks for eBPF/ftrace readiness and tracefs environment.
related:
  - ebpf-verify
used_with:
  - ftrace-capture
anti_patterns:
  - unbounded-trace
---

# ebpf-baseline

## Trigger
- 當任務需要確認 eBPF/ftrace 是否可用時。

## Input
- 目標系統 shell 存取權限。
- 可用的 `bpftool` 與 tracefs/debugfs 路徑。

## Flow
1. 檢查 tracefs/debugfs 掛載狀態。
2. 檢查 `bpftool prog/map/net show` 是否可執行。
3. 確認 `current_tracer`/`available_tracers` 可讀。

## Output
- `commands_run`
- `baseline_artifacts`
- `baseline_findings`

## Quick Commands
```bash
mount | rg "tracefs|debugfs"
sudo bpftool prog show
sudo bpftool map show
cat /sys/kernel/tracing/current_tracer
cat /sys/kernel/tracing/available_tracers
```

## Links
- 下一步通常接 `[[ftrace-capture]]`。
- 結果驗證可交給 `[[ebpf-verify]]`。
