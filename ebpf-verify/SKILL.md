---
name: ebpf-verify
description: Verify eBPF/ftrace capture artifacts against expected event/function outcomes.
depends_on:
  - ebpf-baseline
used_with:
  - ftrace-capture
related:
  - ebpf-ftrace
anti_patterns:
  - no-evidence-summary
---

# ebpf-verify

## Trigger
- 當任務需要驗證 eBPF/ftrace 結果是否符合預期時。

## Input
- baseline/capture 產生的 artifacts。
- 預期函式、事件或關鍵字。

## Flow
1. 比對 `bpftool` 輸出是否含預期 program/map/link。
2. 比對 trace 是否含預期函式/事件關鍵字。
3. 輸出可追溯結論與下一步建議。

## Output
- `verification_result`
- `evidence_refs`
- `next_actions`

## Quick Commands
```bash
sudo bpftool prog show | rg "<expected-prog>"
sudo bpftool map show | rg "<expected-map>"
rg "<expected-event-or-func>" /sys/kernel/tracing/trace
```

## Links
- 前置依賴 `[[ebpf-baseline]]`。
- 常與 `[[ftrace-capture]]` 串接。
