---
name: terminology-enforcer
description: Normalize terminology consistently and produce explicit replacement artifacts.
---

# terminology-enforcer

## Trigger
Use when user asks for terminology consistency, wording normalization, or documentation cleanup.

## Workflow
1. Load source text.
2. Apply terminology mapping rules.
3. Produce three artifacts:
   - 替換清單 (`old -> new`)
   - 套用後文本
   - 未決清單 (ambiguous terms)
4. Keep original meaning unchanged while normalizing vocabulary.

## Output Contract
- `replacement-map.md` (替換清單)
- `normalized-text.md`
- `pending-terms.md` (未決)

