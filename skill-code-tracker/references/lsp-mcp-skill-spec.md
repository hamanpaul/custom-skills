# lsp-mcp-skill-spec（v0）

## 1. 範圍與目標
### 1.1 目標
- 專為 Agent CLI trace code 使用：定義→引用→呼叫關係→型別/繼承（以 C/C++ 優先）。
- 降低誤判率、提升準確率：語意結果優先；降級結果必須附證據與信心分數。
- 加速分析：限制深度/扇出/節點數、最小化檔案讀取、快取與 stale 標記。
- 易於安裝維護：分層清楚、設定資料化、WSL Ubuntu only、版本不鎖定但需兼容層。

### 1.2 非目標（v0）
- 不做自動重建索引（僅標記 stale 並降信心）。
- 不做 refactor/rename/workspace edit 的自動套用（可列為 future）。
- 不處理跨平台（Windows/macOS）與多 repo 同時工作流。

---

## 2. 前置條件（WSL Ubuntu only）
### 2.1 必要（must）
- Node.js v24（供 `axivo/mcp-lsp`）
- `npx`
- LSP servers（依語言）
  - C/C++：`clangd`（使用 `compile_commands.json`）
  - Lua：`lua-language-server`（若採用）
  - Python：`pylsp` 或同等（若採用）
  - Bash/Zsh：`bash-language-server`（若採用）
  - ODL：有支援的 LSP/工具鏈才納入
- `ctags`（universal-ctags）
- `cscope`

### 2.2 可選（optional）
- `rg`
- `fd`
- `ast-grep`

---

## 3. 依賴元件（固定組合）
### 3.1 MCP servers
- `axivo/mcp-lsp`（LSP MCP）
- `ctags-mcp-server`（Index MCP：ctags）
- `cscope-mcp`（Index MCP：自建；參考 `~/.paul_tools/mcp_server/liu-mcp/` 的結構與慣例）

### 3.2 Skill
- `skill-code-tracker`（trace orchestrator）

### 3.3 安裝位置規範
- 所有 MCP servers 安裝於：`~/.paul_tools/mcp_server/`
- 版本策略：`axivo/mcp-lsp` 與 `ctags-mcp-server` 不鎖版本；skill 必須有 normalize/compat 層吸收輸出差異。

---

## 4. Workspace 與索引檔規格
### 4.1 workspace_root
- `workspace_root` 由 skill trigger 當下指定的專案路徑決定。
- `workspace_root` 不寫死（可能在 `arc_prj` 或 `build-home` 下）。

### 4.2 `compile_commands.json`（僅 clangd）
- 僅用於 `clangd`（C/C++），假設單一檔案、固定檔名：`compile_commands.json`
- 由使用者自行生成，並以 symlink 方式存在於專案根目錄。

### 4.3 cscope/ctags 索引檔（使用者自行生成）
以下檔案以 **symlink** 方式存在於專案根目錄，供 CLI（含互動式 cscope）直接使用：
- `cscope.files`
- `cscope.out`
- `cscope.out.in`
- `cscope.out.po`
- `tags`（固定檔名；若另有命名需求需另補 spec）

---

## 5. 工具分工與降級策略（固定規格）
### 5.1 定位
- LSP：語意導航（definition/references/call hierarchy/type hierarchy/symbols）
- ctags：`definition/outline`（seed、檔案結構、快速定位）
- cscope：`callers/callees/refs`（關係候選）
- rg/fd/ast-grep：最後防線 + 低信心時取證據提升信心（小範圍）

### 5.2 降級路由（v0）
1. LSP MCP（優先）
2. Index MCP（ctags/cscope）
3. Text 工具（rg/fd/ast-grep）僅用於：
   - 所有 MCP 失效時的手動追蹤輔助
   - 或 `conf` 過低時在候選附近取證據，提升 `conf`

---

## 6. `cscope-mcp` Tool 映射（必做）
對齊 `cscope find <key>`：
- `find f` → `cscope.find_file`：`{ file }`
- `find g` → `cscope.find_global_definition`：`{ symbol }`
- `find c` → `cscope.find_callers`：`{ function }`
- `find d` → `cscope.find_callees`：`{ function }`
- `find s` → `cscope.find_symbol`：`{ symbol }`
- `find e` → `cscope.find_egrep`：`{ pattern }`

回傳格式（v0 最小）：`Location[]`
- `file`（basename）
- `path`（workspace 相對路徑；用於去重/避免撞名）
- `line`（1-based；若 cscope 原生輸出為 1-based，直接採用；若為 0-based，需在 mcp 層或 skill 層轉換，但 `trace.md` 必須 1-based）
- `col`（可選；未知則省略或設 1）
- `text`（可選：命中行摘要；`find e` 建議提供）

執行模式：直接跑 `cscope` 指令查詢（對齊互動式使用習慣），不設計長駐 daemon。

---

## 7. Skill：`skill-code-tracker`（v0 行為規格）
### 7.1 觸發條件（SKILL.md）
description 需夠窄，觸發意圖包含任一類：
- `trace/追 code/呼叫鏈/call graph/callers/callees/找誰呼叫`
- `找定義(go to definition)/找引用(find references)/type hierarchy/implementation`
- `LSP + trace`、`cscope/ctags 導航`、`跨檔追蹤`

### 7.2 輸入（最小介面）
skill 需支援下列 seed 型態（至少其一）：
- `seed.position`：`{ file, line, col }`（報告層 1-based；內部可轉換）
- `seed.symbol`：`{ name }`
- `seed.file`：`{ file }`（用於 file-level outline/符號列舉）

### 7.3 hard limits（必做）
- `maxDepth`
- `maxFanout`
- `maxNodes`
- `timeoutMs`
超限時必須裁切並在報告標註「被裁切」與原因。

---

## 8. 輸出規格（固定）
### 8.1 報告路徑顯示
- `trace.md`：只顯示 `basename:line:col`；撞名才最小化補齊 `dir/file:line:col`
- `trace.json`：保留 `path`（相對路徑）+ `file`（basename）

### 8.2 trace 方式標示
- `trace.md` 頂部必須輸出 `trace_mode`：`lsp` / `ctags` / `cscope` / `rg` / `mixed`
- 每個節點行尾必須輸出：`[via=... conf=...]`

### 8.3 信心分數（conf）
- 範圍：0~1
- 用途：排序/裁切/告警；不作語意保證
- v0 基準（可調整但要固化規則）
  - `via=lsp`：0.9~1.0
  - `via=cscope/ctags`：0.4~0.8
  - `via=rg/fd/ast-grep`：0.1~0.4
  - `via=cscope+rg` / `ctags+rg`：在候選附近取到明確證據時可加分

### 8.4 Mermaid 圖（人讀報告必須包含）
- `trace.md` 必須包含至少一張 `mermaid` 圖（建議 `flowchart TD`）表達本次 trace 的 nodes/edges（或深度=1 的子圖）。
- 產生 Mermaid 圖時，需自主套用 `mermaid-agent` skill 的規範（語法正確、短標籤、必要時加雙引號、避免括號/長字串、使用 `style` 同時指定 `fill`/`stroke`）。

---

## 9. 快取與 stale（v0：不重建）
### 9.1 定義
- `stale`：結果「可能失效」（workspace 狀態已變更或索引可能落後），v0 不重建，只標記並下修 `conf`。

### 9.2 依據（repo signature）
- git 專案：`repo_signature = HEAD_SHA + dirty_flag`
- 非 git：以關鍵檔 mtime/hash 近似（至少 `compile_commands.json`）

### 9.3 下修規則（需固化）
- `stale` 節點/邊：`conf = conf * 0.8`（固定規則）
- `stale` 且 `via=ctags/cscope`：再額外下修（例如再乘 `0.8`）

---

## 10. Trace 輸出落點與命名（保留歷史）
- 產出目錄：`~/obsidian_vault/root-note/arc-notes/lsp-mcp/`
- 檔名：`<project>+<feature>+<timestamp>.trace.md`、`<project>+<feature>+<timestamp>.trace.json`
- 必須保留歷史 trace（不覆寫）。

---

## 11. 測試規格（v0）
### 11.1 Unit（skill 層）
- normalize：path/basename、去重 key 穩定性
- merge+dedup：跨 provider 合併規則
- conf/stale：固定規則輸入→輸出一致
- bound：maxDepth/maxFanout/maxNodes 生效，且裁切標註存在

### 11.2 Integration
- LSP MCP：至少 C/C++（clangd）definition/references/call hierarchy
- ctags MCP：definition/outline 可用
- cscope MCP：`find c/d/s/g/f/e` 可用（索引檔存在情境）
- optional 工具：`rg/ast-grep` 取證據提升信心（有裝才跑）

### 11.3 Regression
- 固定 seed + 固定 repo_signature：比對 `trace.json` 的 nodes/edges 結構（排序需穩定）
