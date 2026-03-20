---
name: ambiorix-cli
description: Ambiorix 框架 CLI 工具操作與資料模型查詢，涵蓋 ba-cli/ubus-cli/pcb-cli 用法、ODL 初始化流程、資料模型註冊驗證、偵錯技巧。用於 prplOS 平台上操作 TR-181 資料模型。觸發關鍵字：Ambiorix、ba-cli、ubus-cli、pcb-cli、ODL、資料模型、TR-181 查詢。
---

# Ambiorix CLI Skill

## 觸發條件
- 使用者需要查詢或操作 TR-181 資料模型
- 需要使用 ba-cli / ubus-cli / pcb-cli
- 需要理解 Ambiorix 元件關係或初始化流程
- 需要偵錯 Ambiorix 服務問題
- 關鍵字：Ambiorix、ba-cli、ubus-cli、pcb-cli、ODL、TR-181、資料模型

## 核心概念

### 三大匯流排
| Bus | 工具 | 場景 |
|-----|------|------|
| uBus | `ubus-cli` | OpenWrt 原生，最常用 |
| PCB | `pcb-cli` | Process Communication Bus |
| Bus-Agnostic | `ba-cli` | 跨匯流排統一操作（建議優先使用） |

### 元件關係
```
ODL 定義 (.odl) → amxd 載入 → amxb 註冊到 bus → CLI 查詢
```

## 常用操作

### 查詢資料模型
```bash
# 列出所有 WiFi Radio
ba-cli 'Device.WiFi.Radio.?'

# 查詢特定參數
ba-cli 'Device.WiFi.Radio.1.Channel'

# 搜尋特定路徑（支援萬用字元）
ba-cli 'Device.WiFi.SSID.*.SSID'

# 列出物件的所有參數
ubus-cli 'Device.WiFi.Radio.1.?'
```

### 設定參數
```bash
# 設定值
ba-cli 'Device.WiFi.Radio.1.Channel=6'

# 呼叫方法
ba-cli 'Device.WiFi.Radio.1._exec("reload")'
```

### 監聽事件
```bash
# 訂閱物件變更事件
ubus-cli 'subscribe Device.WiFi.Radio.*'

# 監聽特定事件
ba-cli 'Device.WiFi.Radio.1.?&listen=true'
```

## 初始化流程驗證
```bash
# 1. 確認服務已啟動
ps | grep mod-whm

# 2. 確認 ODL 載入成功
ba-cli 'Device.WiFi.?' | head -5

# 3. 確認 bus 註冊
ubus list | grep -i wifi

# 4. 檢查服務狀態
ba-cli 'Device.Services.?' | grep -i whm
```

## 偵錯技巧

### 常見問題排查
```bash
# 物件不存在
ba-cli 'Device.WiFi.Radio.?' 
# → 若空：檢查 mod-whm 是否啟動、ODL 是否正確

# 參數設定失敗
ba-cli 'Device.WiFi.Radio.1.Channel=149'
# → 確認參數是否 read-only、值是否合法

# Bus 連線問題
ubus list 2>&1 | head
# → 若 timeout：確認 ubusd 是否執行中
```

### 日誌查看
```bash
# Ambiorix 框架日誌
logread | grep -i amx

# 特定模組日誌
logread | grep -E 'mod-whm|amxd|amxb'
```

## libamx 函式庫對照
| 函式庫 | 用途 |
|--------|------|
| libamxd | 資料模型定義與管理 |
| libamxb | Bus 後端抽象層 |
| libamxo | ODL 解析器 |
| libamxc | 通用容器（list/htable/variant） |
| libamxp | 訊號與 slot 機制 |
| libamxs | 同步（sync）模組 |

## 參考文件
- `[[ambiorix-analysis]]` — Ambiorix 完整分析
- `[[ambiorix-foundation]]` — 基礎概念
- `[[ambiorix-architecture]]` — 系統架構
- `[[ambiorix-cli-tools]]` — CLI 工具與程式片段
- `[[ambiorix-startup]]` — 初始化與資料模型註冊
- `[[ambiorix-debug]]` — 驗證與偵錯技巧
