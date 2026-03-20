---
name: agent-broswer
description: Search and verify web information with source attribution and recency checks. Use when tasks require internet lookup, latest/current data, official documentation, product specs/prices, regulations, news, or when users ask to browse/verify and provide links.
---

# Agent Broswer

## Goal

Deliver web research results with verifiable sources, concrete dates, and clear uncertainty handling.

## Trigger Phrases

Trigger this skill when requests contain phrases like:
- 幫我上網查
- 幫我找資料
- 幫我確認最新資訊
- 請附來源 / 請給連結
- 幫我 verify / lookup / browse

## Workflow

1. Define scope before searching.
- Extract topic, locale, time range, and expected output format.
- For requests with `最新`/`今天`/`current`, force explicit date validation.

2. Search and collect candidate sources.
- Start with broad queries, then narrow by official domain or primary source.
- For technical topics, prioritize official documentation first.
- For high-risk topics (medical/legal/financial/security), prioritize official institutions and standards docs.

3. Verify and reconcile.
- Cross-check unstable facts with at least two independent sources when possible.
- Mark conflicting results explicitly instead of guessing.
- If no reliable source exists, state inability to verify.

4. Produce evidence-based response.
- Provide direct answer first.
- Provide key findings with absolute dates.
- Provide source links.
- Provide uncertainty/limitations when needed.

## Hard Rules

- Never fabricate citations.
- Never output claims from web search without source links.
- Always include absolute dates when discussing time-sensitive facts.
- Always distinguish `fact from source` vs `inference`.

## Output Contract

Use this response shape:

- `結論`：一句話答案
- `依據`：2-5 條重點（含日期）
- `來源`：可點擊連結清單
- `限制`：資料缺口、來源衝突、或無法驗證項目
