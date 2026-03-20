---
name: pwhm-trace-classifier
description: 分類 pWHM HLAPI→LLAPI→Vendor 追蹤路徑為 19 種模式之一。用於分析 pWHM API call chain、辨識 ODL handler 類型、判斷 FTA/SWLA/Vendor 路徑。觸發關鍵字：pWHM trace、HLAPI path、追蹤分類、trace type、ODL handler。
---

# pWHM Trace Type Classifier

## 觸發條件
- 使用者要求分析 pWHM 的 API 呼叫路徑
- 需要判斷某個 TR-181 參數走哪種 trace pattern
- 遇到 HLAPI↔LLAPI↔Vendor 映射問題
- 關鍵字：trace type、追蹤分類、HLAPI path、ODL handler、SWLA dispatch

## 三大追蹤類型

### Type A — ODL Handler（資料模型層）
起點在 ODL 定義的 `on action read/write` 或 `read with/write with`。
特徵：直接在 `.odl` 中綁定 C 函式。

### Type B — SWLA Dispatch（服務工作層）
起點在 SWLA（Service Worker Layer Agent）分派邏輯。
特徵：透過 `amx_swla_dispatch()` 進入，再由參數名比對路由到特定 handler。

### Type C — LLAPI / Vendor Direct（底層直通）
起點在 LLAPI 或 Vendor 函式指標直接呼叫。
特徵：跳過 SWLA，直接走 `mfn_*`、`wifiGen_*`、或 vendor callback。

## 19 種追蹤模式速查

| # | 模式名稱 | 類型 | 關鍵特徵 |
|---|---------|------|---------|
| 1 | ODL on action read | A | `_action_read` 在 .odl |
| 2 | ODL Direct Write Handler | A | `_action_write` 在 .odl |
| 3 | ODL read with Handler | A | `_read_with` 函式 |
| 4 | ODL write with Handler | A | `_write_with` 函式 |
| 5 | Parent Object Event Handler | A | `_event_handler` 監聽父物件 |
| 6 | SWLA Generic Dispatch | B | `amx_swla_dispatch` → 通用路由 |
| 7 | SWLA Specific Param Handler | B | SWLA → 特定參數 handler |
| 8 | SWLA Object Changed Callback | B | `_object_changed` 回調 |
| 9 | Sync Logic | B | 同步函式連鎖 |
| 10 | Direct mfn_ Call | C | `mfn_*` 指標直呼 |
| 11 | wifiGen_ Call | C | `wifiGen_*` 封裝 |
| 12 | Recursive wld_ Call | C | `wld_*` 遞迴呼叫 |
| 13 | Vendor Pointer Assignment | C | `vendor_ops->fn = ...` |
| 14 | Vendor Naming Convention | C | 命名規則對應 |
| 15 | Method/Action Call | B | `.method` 呼叫模式 |
| 16 | Parent Object Read Handler | A | 父物件讀取 |
| 17 | Indirect LLAPI via Mgmt | C | 管理函式間接呼叫 |
| 18 | wifiGen_ep_stats Read-only | C | 唯讀統計路徑 |
| 19 | Parent Indirect Sync Chain | B | 父物件間接同步連鎖 |
| 20 | C-Code Setter Update | C | C code setter / Read-Only ODL |
| 21 | Vendor Param Pass-through | C | 參數透傳 |
| 22 | Event-Based Update Sequence | B | 事件驅動更新序列 |

## 分類工作流程

1. **辨識進入點**：從 `.odl` 檔的 `on action` / `read with` / `write with` 找起
2. **判斷有無 SWLA**：若走 `amx_swla_dispatch` → Type B；否則繼續
3. **判斷是否直接 ODL handler**：若 `.odl` 直接綁定 C 函式 → Type A
4. **剩餘為 Type C**：直接走 `mfn_*` / `wifiGen_*` / vendor callback
5. **細分模式**：依關鍵特徵對照上表，標註模式編號
6. **輸出格式**：

```
參數路徑: Device.WiFi.Radio.{i}.Channel
追蹤類型: Type B — SWLA Dispatch
模式: #7 (SWLA Specific Parameter Handler)
進入點: amx_swla_dispatch → whm_wifi_radio_channel_handler
LLAPI: mfn_setRadioChannel → wl_ioctl
```

## 參考文件
- `[[pWHM-trace-type-classification]]` — 19 種模式完整說明與程式碼範例
- `[[trace-type-overview]]` — 概覽與基礎 Handler（模式 1-4）
- `[[trace-type-swla-dispatch]]` — SWLA 分派（模式 5-9）
- `[[trace-type-llapi-vendor]]` — LLAPI/Vendor（模式 10-14）
- `[[trace-type-advanced-patterns]]` — 進階模式（15-22）
- `[[trace-type-reference]]` — 環境與 hlapi_tracer.py 工具
