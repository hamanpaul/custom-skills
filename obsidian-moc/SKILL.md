---
name: obsidian-moc
description: "Obsidian MOC（Map of Content）自動生成與更新。掃描三個 Vault 產生三層階層索引。"
triggers:
  - "MOC"
  - "更新索引"
  - "目錄"
  - "map of content"
  - "筆記索引"
---

# Obsidian MOC Skill

## 用途
自動生成/更新 `~/notes/MOC.md`，提供三層階層索引：
1. **第一層**：Vault（TechVault / WorkVault / PersonalVault）
2. **第二層**：Tags（依筆記數量降冪排序）
3. **第三層**：母子關係（`atomized_from:` 欄位）

## 工具
`ObsToolsVault/tools/moc-generator.py`

## 指令

```bash
# 生成/更新 MOC.md
python3 ObsToolsVault/tools/moc-generator.py

# 預覽（不寫入）
python3 ObsToolsVault/tools/moc-generator.py --dry-run

# 顯示統計
python3 ObsToolsVault/tools/moc-generator.py --stats
```

## 觸發時機
1. **手動**：使用者要求「更新 MOC」時執行
2. **Pre-commit hook**：每次 git commit 前自動執行
3. **Crontab**：定期由 `copilot -m gpt-5-mini` 觸發

## 工作流程
1. 執行 `python3 ObsToolsVault/tools/moc-generator.py`
2. 確認輸出的筆記數量是否合理
3. 如有新增的 tag 未在 `role-tags-Regulator.md` 定義 → 提醒使用者
4. 完成後回報統計摘要

## 注意事項
- MOC.md 放在 repo 根目錄，不屬於任何 Vault
- MOC.md 是自動產生的，**請勿手動編輯**
- 同一筆記有多個 tag 時，會出現在多個 tag 群組下（屬正常行為）
- Vault 層級的計數是不重複的
