---
name: broadcom-prpl-patch
description: 將 Broadcom prplWare patch bundle 套用到 BGW720 worktree 的流程。用於比較新舊 patch drop、比對目前 repo 差異、判斷哪些檔案可直接覆蓋，以及依 `notes.txt` 或 release note 決定 impl107 helper driver patch 要套進 source 還是只保留為 repo artifact。
---

當使用者要求把 Broadcom prplWare patch bundle 例如 `CS00012439197_6.3.0_prplware4.0.3_YYYYMMDD.tgz` 套用到 BGW720 worktree，或要求你檢查/審閱 patch 是否正確整合時，使用此 skill。

## Patch bundle 結構

Broadcom patch bundle 可能包含：

- `altsdk/openwrt/patches/prpl/v23.05.3_prplware-v4.0.3/feeds/`
  - `feed_prplmesh/services/pwhm/files/etc/amx/wld/wld_defaults/`
  - `feed_prplmesh/services/pwhm/patches/`
  - `feed_prplos/.../prpl-webui-bcm/`
- `userspace/public/libs/prpl_brcm/mods/mod-whm-brcm/`
  - `Makefile.fullsrc`
  - `include_priv/`
  - `src/`
- `bcmdrivers/broadcom/net/wl/impl107/*.patch`
- `build/` — build system 檔案（如 `Bcmwrt.mk`）
- `notes.txt`

## 🚫 三階段強制流程（BLOCKING GATES）

Patch bundle 的套用分為三個階段，每個階段都是 BLOCKING GATE——
**未通過前一階段，禁止進入下一階段。禁止跳過任何階段。**

---

### GATE 1：清點（Inventory）— 套用前必須完成

**目的：建立 bundle 的完整檔案清單，確保每一個檔案都被辨識與分類。**

執行清點腳本：

```bash
~/.copilot/skills/broadcom-prpl-patch/patch-inventory.sh ~/brcm-patchs/<MMDD>
```

輸出每行格式：`<category>\t<path>`，category 為 IPATCH / COPY / REF / OTHER。

**GATE 1 通過條件：**
- 腳本成功執行（exit 0）
- OTHER = 0（若有 OTHER 需人工分類）
- 向用戶展示完整清單，確認分類無誤後才開始套用

---

### GATE 2：套用（Apply）— 逐檔處理

**按分類處理每一個檔案，處理後立即更新 status：**

| category | 處理方式 | 驗證方式 |
|----------|---------|---------|
| `IPATCH` | 依 notes.txt 指示（通常 `patch -p1`），先 dry-run | dry-run + apply + reverse dry-run |
| `COPY`   | `diff` 比對後 `cp` 覆蓋 | `cmp -s` 確認一致 |
| `REF`    | 不進 repo，僅參考 | 標記 `skipped` |
| `OTHER`  | 停下來問用戶 | 用戶指示 |

每處理完一個檔案，立即：
```sql
UPDATE patch_files SET status = 'applied', reason = '<how>' WHERE path = '<file>';
```

**COPY 類檔案特別注意：**
- `notes.txt` 不會提及 COPY 類檔案。不要因為 notes.txt 沒提到就跳過。
- COPY 檔可能在任何目錄：`build/`、`userspace/`、`altsdk/`、`targets/` 等。
- 歷史教訓：0315 bundle 的 `build/Bcmwrt.mk`（COPY 類）被漏掉三次，
  因為只看 notes.txt 的 IPATCH 指示。

**GATE 2 通過條件：**
- `SELECT count(*) FROM patch_files WHERE status = 'pending'` = 0
- 每一行都是 `applied` 或 `skipped`（附 reason）

---

### GATE 3：驗證（Verify）— 套用後必須通過

**目的：用腳本逐檔比對 bundle vs worktree，產出機器可讀結果。**

執行驗證腳本：

```bash
~/.copilot/skills/broadcom-prpl-patch/patch-verify.sh ~/brcm-patchs/<MMDD> <worktree>
```

Exit codes：
- `0` = ALL PASSED — 可進入 build
- `1` = HAS FAILURES（MISSING 或無法解析）— **BLOCKED，禁止 build/commit**
- `2` = HAS DIFFS（檔案存在但內容不同）— 每個 DIFF 必須由人工判定：
  - 若為 worktree 有意的本地修正 → 標記為已知差異，可繼續
  - 若為漏掉的更新 → 修復後重跑腳本

**GATE 3 通過條件：**
- Exit code = 0，或 exit code = 2 且所有 DIFF 已由用戶確認
- 零個 FAIL 行
- 向用戶展示驗證結果

**若 GATE 3 未通過：**
- 禁止宣稱 patch 已完成
- 禁止進入 build
- 禁止 git commit
- 必須修復所有 FAIL 項目後重跑驗證腳本

---

### 🔴 問題發生時的強制回查規則

**當 build 後發現功能未啟用或行為異常時：**

1. **第一步永遠是回查 bundle**，不是自行修改 source/build system：
```bash
# 搜尋 bundle 中是否有相關修復
grep -rn '<keyword>' ~/brcm-patchs/<MMDD>/
# 重跑 GATE 3 驗證腳本，看是否有 FAIL
```

2. 只有在確認 bundle 中沒有對應修復後，才可以自行修改。
3. 自行修改前必須告知用戶：「bundle 中未包含此修復，我需要自行修改 X 檔案」。

**違反此規則 = 重複 0315 事件四的錯誤。**

---

常見路徑：

- patch drop：`~/brcm-patchs/MMDD/`
- 原始 tarball：`~/brcm-patchs/CS00012439197_6.3.0_prplware4.0.3_YYYYMMDD.tgz`
- 已知問題筆記：`~/brcm-patchs/patch-exp.md`
- 目標 worktree：目前的 BGW720 repo

## 比對策略

永遠分兩個維度比對：

1. **新 bundle vs 前一版 bundle**
   - 目的：找出 Broadcom 相對於上一版 patch release 新增了什麼。
   - 不要把流程寫死成特定的 `0227` vs `0306`；永遠拿「這次 patch」去比「它的前一版 patch」。
   - 已驗證過的一個例子：bundle `0306` 對上一版 `0227` 的差異只有：
     - `bcmdrivers/.../impl107/0002-rb224211.patch`
     - `bcmdrivers/.../impl107/0003-rb223772_rb224292_rb225045.patch`
     - `bcmdrivers/.../impl107/0004-rb224802.patch`
     - `notes.txt` 增加描述這三個 patch 的文字

2. **新 bundle vs 目標 repo**
   - 目的：找出目前 codebase 還缺哪些內容。
   - 不要假設「新舊 bundle 差異」就等於「repo 與 bundle 差異」。
   - 例子：`9025` 與 `9026` 雖然在 `0227` bundle 就已存在，但後續某個 repo baseline 仍然缺正確的 `9025` 內容，也仍然缺 `9026`。

常用指令：

```bash
diff -rq ~/brcm-patchs/0227 ~/brcm-patchs/0306

PATCH=~/brcm-patchs/0306
DST=~/BGW720-B0-403
cd "$PATCH"
find altsdk userspace bcmdrivers -type f | sort | while read -r rel; do
  if [ -e "$DST/$rel" ]; then
    cmp -s "$PATCH/$rel" "$DST/$rel" || echo "DIFF $rel"
  else
    echo "NEW  $rel"
  fi
done
```

## 來源一致性檢查

如果你同時有原始 tarball 與解開後的目錄，先比對一次，確認解開後的樹可信。
以下組合曾經驗證過：

- `~/brcm-patchs/CS00012439197_6.3.0_prplware4.0.3_20260305.tgz`
- `~/brcm-patchs/0306`

## 檔案處理規則

1. **OpenWrt feed patch 檔**
   - `altsdk/.../feed_prplmesh/.../patches/*.patch` 是 OpenWrt patch queue 的輸入。
   - 當 repo 內容不同時，直接 verbatim 覆蓋。
   - 用 `cmp -s` 驗證。

2. **userspace source 檔**
   - `whm_brcm_api_ext.c` 與 `whm_brcm_api_ext_vndr.c` 屬於高風險檔案。
   - 如果 bundle 內容會覆蓋掉 worktree 既有修正，必須保留本地修正。

3. **impl107 driver helper patch 檔**
   - `bcmdrivers/broadcom/net/wl/impl107/*.patch` 不能只靠路徑名稱解讀。
   - 先讀 patch bundle 的 release note，通常是 `notes.txt`，判定它們要如何整合進 repo。
   - 不要假設每個 impl107 patch 都固定使用 `patch -p1`。
   - 若 release note 明確寫要套進 source，先 dry-run，再實際套用，最後做 reverse dry-run 驗證。
   - 除非 repo 本來就把這類 helper patch 當正式輸入 artifact 追蹤，且 release note 也明確要求保留 raw patch，否則不要只 commit raw helper patch 檔。

4. **impl107 helper patch 強制決策**
   - 每個 `impl107/*.patch` 都必須先被判定為以下其中一種模式，不能跳過：
     - `apply_to_source`：release note 要求把 patch 真正套進 `impl107/main/...` source tree。
     - `track_helper_patch_only`：repo 明確把此類 patch 視為正式輸入 artifact，且本次 release note 沒要求實際套進 source。
   - 只要 `notes.txt` 出現類似 `impl107/# patch -p1 < xxx.patch`、`apply patch`、`patch -p1` 之類指示，預設必須判定為 `apply_to_source`。
   - 若無法明確判定模式，視為阻斷條件，停止提交並向使用者回報。

5. **impl107 helper patch fail-fast 規則**
   - 若本次提交新增或更新了 `bcmdrivers/broadcom/net/wl/impl107/*.patch`，但 `impl107/main/...` 底下沒有任何對應 source diff，預設視為失敗，不可提交。
   - 若宣稱已採用 `apply_to_source`，必須同時滿足：
     - `patch --dry-run` 成功
     - 實際 `patch` 成功
     - `patch --dry-run -R` 成功
     - `git diff --name-only` 可見 `impl107/main/...` 的實際 source 變更
   - 若上述任一條件不成立，不得以「新增 helper patch 檔」取代真正整合。

6. **提交前驗證關卡**
   - 對每個 `apply_to_source` 的 impl107 patch，提交前至少做一次：
     - `git diff --name-only -- bcmdrivers/broadcom/net/wl/impl107/main`
     - 關鍵符號搜尋，確認 source 真有吸收 patch 內容
   - 若 userspace 已新增對新 driver 能力的 consume 邏輯，但 driver source 沒有對應 producer 變更，必須明確標記為半套整合，禁止當成完成態提交。

範例：

```bash
# 0306 notes.txt 寫的是: ** impl107/# patch -p1 < xxx.patch
cd ~/BGW720-B0-403/bcmdrivers/broadcom/net/wl/impl107
patch --dry-run -p1 < ~/brcm-patchs/0306/bcmdrivers/broadcom/net/wl/impl107/0002-rb224211.patch
patch -p1 < ~/brcm-patchs/0306/bcmdrivers/broadcom/net/wl/impl107/0002-rb224211.patch
patch --dry-run -R -p1 < ~/brcm-patchs/0306/bcmdrivers/broadcom/net/wl/impl107/0002-rb224211.patch
git diff --name-only -- main
```

7. **notes.txt**
   - 複製或提交前先檢查 `git ls-files -- notes.txt`。
   - 若 repo 沒有追蹤 `notes.txt`，把它當參考資料即可，不要提交。

## 每次 patch 都要檢查的已知重複問題

1. `WL_STA_ANT_MAX` 不可保持未定義。
   - 在 `whm_brcm_api_ext.c` 與 `whm_brcm_api_ext_vndr.c` 中，必要時優先改用 `MAX_NR_ANTENNA`。
2. eht/he band guard 必須存在。
   - eht 邏輯應只在 6 GHz 啟用。
   - he 邏輯應只在非 2.4 GHz 啟用。
3. `Makefile.fullsrc` 可能缺少 `cchk` fallback。
   - 如果 worktree 已有需要的 `whm_brcm.c` 處理，避免回歸。

常用檢查：

```bash
grep -n "WL_STA_ANT_MAX" <patch>/userspace/.../src/whm_brcm_api_ext*.c
grep -n "operatingFrequencyBand" <patch>/userspace/.../src/whm_brcm_api_ext.c | grep -c "eht\|he"
```

## 實作規則

- 把「目前 patch 對前一版 patch」與「目前 patch 對 repo」分開比較。
- worktree 特有修正優先於舊 patch 內容。
- 可以提交 repo 追蹤的 source change 與 feed patch 檔，但不能用 raw helper artifact 取代真正整合。
- 若 `notes.txt` 未被追蹤，就不要提交。
- helper driver patch 的處理方式由 release note 決定；例如 0306 的 `notes.txt` 就明確要求 `patch -p1`。
- patch 完成後，必須通過 GATE 3 驗證腳本，再進入 build。
- **最終提交前，明確回答這五個問題（缺一不可）：**
  1. bundle 中共有幾個檔案？
  2. 哪些是 COPY 直接覆蓋？（含路徑）
  3. 哪些是 IPATCH 已套入 source？（含路徑）
  4. 哪些被 skip？（附原因）
  5. GATE 3 驗證腳本是否全部 PASSED？

## 歷史事故記錄

### 0315 事件：build/Bcmwrt.mk 遺漏（三次重複）

- **Bundle 內容**：`build/Bcmwrt.mk` 新增 `export BUILD_BRCM_OPENWRT`
- **分類**：COPY（直接替換檔）
- **notes.txt 是否提及**：否
- **後果**：WMM per-BSS counter 功能的 source code 已套用，但 build system 未啟用 `-DWL_WMM_BSS_STATS`，裝置上看不到 WMM counters
- **錯誤應對**：追蹤問題後自行修改 `make.common`，而非回查 bundle
- **被漏掉次數**：3 次
- **Root cause**：沒有執行 GATE 1 清點，只看 notes.txt 就開始套用
- **修正措施**：本 skill 的三階段強制流程
