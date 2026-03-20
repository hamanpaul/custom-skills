---
name: obsidian-migration
description: "Obsidian root-note 批次遷移工具：掃描、分類、遷移筆記至 TechVault/WorkVault/PersonalVault，遵循 constitution.md 與 role-tags-Regulator.md 規則。"
triggers:
  - "root-note"
  - "migration"
  - "遷移"
  - "整理筆記"
  - "obsidian vault"
  - "歸檔"
---

# Obsidian Migration Skill

本 Skill 封裝了 root-note 批次遷移的完整流程與經驗。

## 載入方式
完整規格請參閱：`~/notes/ObsToolsVault/obsidian-migration-skill.md`

## 快速規則摘要

1. **扁平化**：.md 只放 Vault 根目錄，非 .md 放 `Assets/`
2. **Frontmatter**：title / created / source / tags / related 全部必填
3. **分類**：技術知識 → TechVault，工作進度 → WorkVault，個人 → PersonalVault
4. **批次 ≤25**：每批提交使用者確認後才執行
5. **related 不可漏**：至少 1 個 `[[wikilink]]`
6. **大量同質 >20**：打包 tarball
7. **語言**：zh-TW（WorkVault 週報例外）

## 狀態追蹤
- SQL: `migration_batch` 表
- JSON: `ObsToolsVault/state/processed_files.json`（MD5 hash key）
