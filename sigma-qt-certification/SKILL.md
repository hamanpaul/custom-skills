---
name: sigma-qt-certification
description: Sigma Agent / QuickTrack WiFi 認證測試完整流程，涵蓋環境建置、Docker 設定、Device 檔客製化、HE/VHT/EHT 測試執行、報告判讀與常見問題排除。用於 Broadcom 平台 WiFi 6/6E/7 認證。觸發關鍵字：Sigma、QuickTrack、WiFi 認證、CAPI、device file、HE test、EHT、Wi-Fi Test Suite。
---

# Sigma/QT WiFi 認證 Skill

## 觸發條件
- 建置或維護 Sigma/QT 測試環境
- 客製化 Device 檔案適配新 DUT/平台
- 執行 WiFi 6/6E/7 認證測試
- 判讀 QuickTrack 報告或排除測試失敗
- 關鍵字：Sigma、QuickTrack、WiFi 認證、CAPI、device file、HE/VHT/EHT test

## 架構概覽

### Sigma vs QuickTrack
| | Sigma Agent | QuickTrack |
|---|---|---|
| 角色 | 外部測試機控制 APUT | DUT 內建服務 |
| 架構 | UCC → Sigma Agent → APUT | UCC → app-dut (on APUT) |
| 轉接層 | 多一層 Sigma Agent | 直連，少一道轉接 |
| 報告路徑 | agent_log_extract | Cloud-Reports / Test-Logs |

### 網路拓樸
```
控制網 (out-of-band): 192.168.250.x/24  ← UCC/控制器
測試網 (in-band):     192.165.1.x/16    ← AP LAN/BSS
```
- 兩張乙太網卡（內建 + USB），控制網與測試網**必須隔離**

## Phase 1：環境建置

### 作業系統需求
- Fedora Core 37 或 Ubuntu 22.04
- 停用 SELinux：`/etc/sysconfig/selinux` → `SELINUX=disabled`
- 停用 firewalld：`systemctl disable firewalld`
- 必要套件：`tcllib expect lftp telnet`

### Docker 環境（建議方式）
```bash
# WSL2 Ubuntu → Docker Container 架構
# NIC1: 控制網 192.168.250.x
# NIC2: 測試網 192.165.1.x
# Container 內執行 agent_start，開放 agentport (15000/TCP)
```

### 網路介面設定
```bash
# USB NIC（控制網）
ip addr add 192.168.250.100/24 dev enp1s0f0
# 內建 NIC（測試網）
ip addr add 192.165.1.100/16 dev enp4s0
```

## Phase 2：Device 檔客製化

### 建立新裝置 Profile
1. 複製基礎檔：`cp sigma/main/device/brcm-cms.tcl sigma/main/device/<new-device>.tcl`
2. 更新 namespace：`namespace eval HE::<device>` 必須與封包名稱一致
3. 調整硬體參數：射頻介面、功率、通道、MLO 編排

### MLO 映射要點
- `mlo_list` 以 MAP/AAP 順序列舉
- 對應 2G/5G/6G 介面：確保索引與 `wl#` 吻合
- Wi-Fi 7 多頻同時需額外確認索引對應

### Wi-Fi Test Suite 範本
- 目錄：`sigma/main/others/Wi-FiTestSuite/`
- AllInitCommand (`cmds/WTS-HE/AllInitCommand_HE.txt`)：
  - 固定啟動宏呼叫 `InitEnv.txt`、`CommonDefs.txt`、`HE-testbed-reset.txt`
  - 須保留 `wfa_test_commands!RadioOff.txt!` Radio Reset 步驟
- PreCorrection 開關：`$PreCorrection_TC_Flag` 控制版本資訊蒐集

## Phase 3：測試執行

### Sigma Agent 啟動
```bash
cd sigma/main
./agent_start --program HE --device <device-name>
# agentport 預設 15000/TCP
```

### 支援的認證 Program（15 項）
| Program | 標準 | 說明 |
|---------|------|------|
| HE | 802.11ax | Wi-Fi 6 主要認證 |
| VHT | 802.11ac | Wi-Fi 5 |
| EHT | 802.11be | Wi-Fi 7 |
| WPA3 | — | 安全性認證 |
| MBO | — | Multi-Band Operation |
| ... | — | 見 `[[sigma-qt-setup]]` 完整清單 |

### 半手動驗證（無 UCC 時）
```bash
# 在 Wi-FiTestSuite 目錄下透過 cmds/config 手動執行
# 另開終端觀察 CAPI
./agent_log_extract.tcl
```

## Phase 4：報告判讀

### QuickTrack 報告位置
- 報告：`/usr/local/bin/WFA-QuickTrack-Tool/Cloud-Reports`
- 日誌：`/usr/local/bin/WFA-QuickTrack-Tool/Test-Logs`

### 常見判讀要點
- PASS/FAIL 直接標註於報告
- 注意 conditional PASS（需人工確認）
- 比對日誌中的 CAPI 序列以定位失敗步驟

## Phase 5：常見問題

| 問題 | 可能原因 | 解法 |
|------|---------|------|
| Test Suite 找不到 AP | 控制網/測試網未隔離 | 確認兩張 NIC 分屬不同網段 |
| Device 檔載入失敗 | namespace 不匹配 | 確認 `package provide` 與 `namespace eval` 一致 |
| MLO 測試失敗 | `wl#` 索引對應錯誤 | 檢查 `mlo_list` 與實際介面映射 |
| CAPI timeout | agent 未啟動或 port 不通 | 確認 `agent_start` 執行中、firewall 開放 15000/TCP |
| Wi-Fi 7 lftp 上傳失敗 | 缺少 lftp 套件 | `dnf install lftp` |

## 參考文件
- `[[sigma-qt-test-framework-details]]` — 測試框架完整細節（母筆記）
- `[[sigma-qt-setup]]` — 架構設定與 Program 總覽
- `[[sigma-qt-he-tests]]` — Wi-Fi 6 HE 測試項目
- `[[sigma-qt-other-tests]]` — VHT/EHT 測試與報告
- `[[sigma-qt-local-setup-guide]]` — 本機測試環境建置
- `[[sigma-qt-build-setup]]` — 建置環境
- `[[Sigma-Agent-device-file-guide]]` — Device 檔指南
- `[[Sigma-QT工具建置與測試流程]]` — 工具建置流程
- `[[wifi-certification-summary]]` — WiFi 認證流程總結
