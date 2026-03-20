---
name: ebpf-ftrace
description: eBPF/ftrace troubleshooting and evidence workflow for kernel/runtime tracing tasks.
related:
  - ebpf-baseline
  - ftrace-capture
  - ebpf-verify
depends_on:
  - ebpf-baseline
used_with:
  - ftrace-capture
  - ebpf-verify
anti_patterns:
  - long-running-capture
---

# ebpf-ftrace

## Trigger
Use when task involves:
- eBPF program attach/load/verify issues
- `ftrace` / `trace_pipe` / tracefs evidence collection
- kernel path timing or call-path tracing
- `bpftool`-based state inspection

## Scope
- Build a repeatable workflow for eBPF + ftrace diagnostics.
- Collect verifiable artifacts and commands.
- Keep changes non-destructive and minimal.

## Workflow
1. Baseline readiness（`[[ebpf-baseline]]`）
   - Ensure tracefs/debugfs mounted and readable.
2. Trace capture（`[[ftrace-capture]]`）
   - Record trace events with explicit filters and bounded duration.
3. Verification（`[[ebpf-verify]]`）
   - Validate that output matches expected path/function/event.
4. Evidence export
   - Save command output and trace logs with timestamped paths.

## Command Reference
```bash
# tracefs / debugfs
mount | rg "tracefs|debugfs"
sudo mount -t tracefs tracefs /sys/kernel/tracing 2>/dev/null || true
sudo mount -t debugfs debugfs /sys/kernel/debug 2>/dev/null || true

# bpftool baseline
sudo bpftool prog show
sudo bpftool map show
sudo bpftool net show

# ftrace baseline
cat /sys/kernel/tracing/current_tracer
cat /sys/kernel/tracing/available_tracers

# example: function tracer
echo function | sudo tee /sys/kernel/tracing/current_tracer >/dev/null
echo 1 | sudo tee /sys/kernel/tracing/tracing_on >/dev/null
sleep 2
echo 0 | sudo tee /sys/kernel/tracing/tracing_on >/dev/null
sudo cat /sys/kernel/tracing/trace | tail -n 200

# live stream
sudo timeout 5 cat /sys/kernel/tracing/trace_pipe
```

## Verification Checklist
- `bpftool` output contains expected program/map/link.
- trace output contains expected function/event keyword.
- trace duration and filter are bounded (avoid unbounded capture).
- command + output paths are recorded for replay.

## Output Contract
Always report:
- `commands_run`
- `artifacts` (trace file / command output path)
- `key_findings`
- `next_actions`

## 自主維護知識（agent-managed）
<!-- self-evolve-managed-knowledge:start -->
- [ebpf_ftrace] 整理 `ebpf_ftrace` 主題的專業流程、關鍵指令與驗證步驟。
<!-- self-evolve-managed-knowledge:end -->
