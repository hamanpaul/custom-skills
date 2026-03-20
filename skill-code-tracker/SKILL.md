---
name: skill-code-tracker
description: Trace code paths across files using LSP/ctags/cscope. Use when user asks to trace, find callers/callees, go to definition, find references, build call graph, or navigate code relationships across files.
---

# Code Tracker Skill

Trace code paths (definition → references → call hierarchy → type hierarchy) using semantic tools.

## Scope

觸發條件（任一）：
- `trace`/`追 code`/`呼叫鏈`/`call graph`
- `callers`/`callees`/`找誰呼叫`
- `go to definition`/`找定義`/`find references`/`找引用`
- `type hierarchy`/`implementation`
- `LSP + trace`、`cscope/ctags 導航`、`跨檔追蹤`

## Workflow

1. **確認 seed**：從使用者輸入取得起點
   - `seed.position`：`{ file, line, col }`
   - `seed.symbol`：`{ name }`
   - `seed.file`：`{ file }`（file-level outline）
   - 若使用者未提供明確 symbol：先用 `rg` 以模糊關鍵字定位候選檔案/片段，轉成 `seed.file` 或 `seed.position`

2. **由模糊 seed 映射到 symbol**（僅在缺少明確 symbol 時）
   - 以 `ctags`/`cscope` 從 `seed.file` 或 `seed.position` 找到候選 symbol
   - 選出最相關的 symbol 作為正式 trace 起點（例如：`wpa_driver_do_broadcom_acs`）

3. **選擇工具**（降級路由）：
   - 優先：`lsp` MCP（axivo/mcp-lsp）
   - 次選：`ctags` MCP（ctags-mcp-server）
   - 備選：`cscope` MCP（cscope-mcp）
   - 最後：`rg`/`ast-grep`（小範圍驗證）

4. **執行 trace**：
   - `trace definition`：找定義（含 typeDefinition/implementation）
   - `trace callers`：找 incoming calls
   - `trace callees`：找 outgoing calls
   - `trace slice`：深度 N 的 call graph

5. **套用限制**（hard limits）：
   - `maxDepth`：預設 3
   - `maxFanout`：預設 10
   - `maxNodes`：預設 200
   - `timeoutMs`：預設 30000

6. **輸出**：
   - `trace.md`：人讀報告（含 Mermaid 圖）
   - `trace.json`：機器可用（nodes/edges/meta）
   - 輸出至：`~/obsidian_vault/root-note/arc-notes/lsp-mcp/`
   - 檔名：`<project>+<feature>+<timestamp>.trace.{md,json}`
   - `trace.md` 以繁體中文撰寫

## Output Format

### trace.md 規格
- 頂部標示 `trace_mode`：`lsp`/`ctags`/`cscope`/`rg`/`mixed`
- 路徑顯示：`basename:line:col`（撞名才補齊 `dir/file`）
- 每節點標示：`[via=... conf=...]`
- 必須包含 Mermaid 圖（`flowchart TD`）
 - `conf` 不可省略

### 信心分數（conf）
| via | conf |
|-----|------|
| lsp | 0.9~1.0 |
| cscope/ctags | 0.4~0.8 |
| rg/ast-grep | 0.1~0.4 |
| cscope+rg | 加分後提升 |

### stale 處理
- `stale` 節點：`conf = conf * 0.8`
- `stale` 且 `via=ctags/cscope`：再乘 `0.8`

## MCP Tools Available

### cscope-mcp
- `find_file`（find f）
- `find_global_definition`（find g）
- `find_callers`（find c）
- `find_callees`（find d）
- `find_symbol`（find s）
- `find_egrep`（find e）
- `health`

### ctags-mcp-server
- `generate_tags`
- `find_symbol`
- `go_to_definition`
- `list_symbols_in_file`
- `get_file_outline`

### axivo/mcp-lsp
- `definitions`
- `references`
- `callHierarchy/incomingCalls`
- `callHierarchy/outgoingCalls`
- `typeHierarchy`
- `workspaceSymbol`
- `documentSymbol`

## References

- `references/lsp-mcp-skill-spec.md`
- `references/lsp-mcp-skill-note.md`
