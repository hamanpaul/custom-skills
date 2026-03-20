---
name: pwhm-debug
description: pWHM 系統化除錯流程，涵蓋 sahtrace/ba-cli 日誌操作、GDB remote debug、除錯資料蒐集與分析。用於 pWHM 元件（mod-whm、mod-whm-brcm、hostapd）的問題排查。觸發關鍵字：pWHM debug、sahtrace、ba-cli、GDB、pWHM 除錯、trace zone。
---

# pWHM Debug Skill

## 觸發條件
- 使用者遇到 pWHM 相關問題需要除錯
- 需要設定 trace level、收集日誌
- 需要 GDB remote debug pWHM 元件
- 關鍵字：pWHM debug、sahtrace、ba-cli trace、gdbserver、除錯

## Phase 1：日誌架構快速定位

### Trace 等級（低→高）
| Level | 用途 |
|-------|------|
| error | 僅錯誤 |
| warning | 警告+錯誤 |
| info | 一般資訊（預設） |
| debug | 詳細除錯 |
| trace | 最詳細追蹤 |

### pWHM 主要 Zone
| Zone | 說明 |
|------|------|
| mod-whm | 核心模組 |
| mod-whm-brcm | Broadcom vendor 模組 |
| mod-whm-ext | Extension 模組 |
| hostapd | hostapd 整合 |
| amx-swla | SWLA 層 |

### Runtime 操作（ba-cli）
```bash
# 查看目前 trace 設定
ba-cli 'sah-trace.Zone.?' | grep -E 'Name|Level'

# 設定特定 zone 為 debug
ba-cli 'sah-trace.Zone.mod-whm.Level=debug'

# 設定所有 zone 為 trace（最詳細）
for z in mod-whm mod-whm-brcm mod-whm-ext hostapd; do
  ba-cli "sah-trace.Zone.${z}.Level=trace"
done
```

## Phase 2：切換輸出管道
```bash
# 輸出到 syslog（預設）
ba-cli 'sah-trace.OutputType=syslog'

# 輸出到 stdout（即時觀看）
ba-cli 'sah-trace.OutputType=stdout'

# 輸出到檔案
ba-cli 'sah-trace.OutputType=file'
ba-cli 'sah-trace.OutputFile=/tmp/whm-trace.log'
```

## Phase 3：除錯資料蒐集
```bash
# 完整蒐集腳本
logread > /tmp/syslog.txt
ba-cli 'sah-trace.Zone.?' > /tmp/trace-zones.txt
ubus-cli 'Device.WiFi.Radio.?' > /tmp/radio-status.txt
ubus-cli 'Device.WiFi.SSID.?' > /tmp/ssid-status.txt
wl -i wl0 status > /tmp/wl0-status.txt
```

## Phase 4：GDB Remote Debug

### 在目標設備上
```bash
# 找到 pWHM PID
pidof mod-whm

# 啟動 gdbserver
gdbserver :9999 --attach $(pidof mod-whm)
```

### 在開發主機上
```bash
# 使用 cross-compiled gdb
arm-linux-gnueabihf-gdb mod-whm

# 連線
(gdb) target remote <device-ip>:9999
(gdb) bt          # backtrace
(gdb) info threads # 檢視執行緒
(gdb) thread apply all bt  # 所有執行緒 backtrace
```

## Phase 5：建議操作流程

```
問題報告 → Phase 1（設定 trace level）
         → Phase 2（選擇輸出管道）
         → 重現問題
         → Phase 3（蒐集資料）
         → 分析日誌 → 定位問題
         → 若需深入 → Phase 4（GDB）
```

## 現有除錯工具
| 工具 | 用途 |
|------|------|
| `ba-cli` | Bus-Agnostic CLI，查詢/設定 TR-181 資料模型 |
| `ubus-cli` | uBus 直接查詢 |
| `pcb-cli` | PCB (Process Communication Bus) 查詢 |
| `sahtrace` | SAH trace 控制 |
| `wl` | Broadcom WiFi driver 控制 |
| `hostapd_cli` | hostapd 控制介面 |

## 參考文件
- `[[pwhm-debug-howto]]` — 完整除錯指南
- `[[pwhm-debug-logging]]` — 日誌追蹤操作細節
- `[[pwhm-debug-gdb-tools]]` — GDB 與工具參考
- `[[pwhm-broadcom-analysis]]` — Broadcom 整合分析
