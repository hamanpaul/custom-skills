---
name: obsidian-atomize
description: "Obsidian 筆記原子化拆分工具：將大型多主題筆記拆分為 Zettelkasten 風格的原子筆記，保留母子關聯並擴展連結網。"
triggers:
  - "原子化"
  - "拆分筆記"
  - "atomize"
  - "split note"
  - "zettelkasten"
---

# Obsidian Atomize Skill

## 用途
將大型多主題筆記拆分為單一概念的原子筆記，同時：
- 保留原始檔作為母筆記（不刪除、不修改內容）
- 子筆記透過 `atomized_from:` 連結母筆記
- 擴展 `related:` 連結網（兄弟連結 + 跨 vault 關聯）

## 六階段工作流

### 1. CANDIDATE_SCAN
掃描 Vault 找出拆分候選：
- 行數 > 200
- H2（##）段落 > 3
- 包含多個獨立概念

```bash
# 快速找候選
wc -l TechVault/*.md | sort -rn | head -20
```

### 2. CONTENT_ANALYSIS
對候選檔案：
- 解析 markdown 結構（H1/H2/H3 段落）
- 識別每個段落的核心概念
- 判斷哪些 tag 是全域的、哪些是段落特定的
- 標記共用前言/背景段落

### 3. SPLIT_PLAN
產出拆分方案（**必須使用者確認才執行**）：

| 原子筆記名 | 來源段落 | Tags | Related |
|-----------|---------|------|---------|
| `pwhm-fsm-states.md` | §2-3 | #pWHM, #wiki | 母+兄弟+外部 |

方案需包含：
- 新檔名（kebab-case）
- 來源行範圍
- 繼承的 tags + 段落特定 tags
- related 連結清單

### 4. EXECUTE
為每個原子筆記建立 .md 於 Vault 根目錄（扁平化規則）：

```yaml
---
title: "子筆記標題"
created: 2026-02-26        # 用母筆記的原始日期
source: "原子化拆分"
atomized_from: "[[母筆記名]]"
tags:
  - 繼承的tag
  - 段落特定tag
related:
  - "[[母筆記名]]"
  - "[[兄弟筆記1]]"
  - "[[兄弟筆記2]]"
---
```

同時更新母筆記的 `related:`，加入所有子筆記連結。

### 5. LINK_EXPANSION
擴展連結網：
- 掃描全 vault，找內容相似的現有筆記
- 雙向補上 `related:` 連結
- 更新其他引用母筆記的筆記 → 加入相關子筆記連結
- 建議新的跨 vault 關聯

### 6. VALIDATE
驗證：
- [ ] 所有新 .md 有完整 frontmatter（title/created/source/atomized_from/tags/related）
- [ ] 所有 `[[wikilink]]` 對應的檔案存在
- [ ] 所有 tags 在 `role-tags-Regulator.md` 有定義
- [ ] 扁平化規則：.md 只在 Vault 根目錄
- [ ] 母筆記 `related:` 已更新
- 觸發 MOC 更新：`python3 ObsToolsVault/tools/moc-generator.py`
- 更新 `processed_files.json`

## 規則

### Frontmatter 新增欄位
```yaml
atomized_from: "[[母筆記名]]"   # 必填，指向母筆記
```

### Tag 繼承策略
- **全域 tag**（如 `#WIFI`、`#公司`）→ 所有子筆記繼承
- **段落 tag**（如 `#debug`、`#code`）→ 只給對應的子筆記
- 如發現新 tag 需求 → 先在 `role-tags-Regulator.md` 定義

### 最小原子大小
- 建議 ≥ 30 行（太短的段落不值得獨立成筆記）
- 共用前言/背景 < 20 行時直接複製到每個子筆記
- 共用前言/背景 ≥ 20 行時獨立成一個 `-overview.md` 子筆記

### 命名慣例
母筆記：`pwhm-broadcom-analysis.md`
子筆記：`pwhm-broadcom-fsm-states.md`、`pwhm-broadcom-vendor-hooks.md`
（前綴保持與母筆記一致，加上段落主題後綴）

## 注意事項
- **永遠不要刪除或修改母筆記的內容**（只更新其 `related:` 欄位）
- 每次最多處理 1 個母筆記（避免批次錯誤）
- 拆分完成後必須觸發 MOC 更新
- 所有 .md 遵循扁平化規則（只放 Vault 根目錄）
