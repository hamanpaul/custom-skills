---
name: liu-code-decoder
description: Decode Liu/Boshiamy codes before task reasoning using packaged skill-local tools.
---

# liu-code-decoder

## Trigger
Use when input may contain Liu roots/codes or user explicitly asks for decode first.

## Principle
- 先解碼再回答。
- If both decoded and raw tokens exist, preserve raw tokens in output details.

## Tooling
- Preferred MCP commands:
  - `health`
  - `lookup`
  - `decode`
- Packaged fallback tool:
  - `scripts/liu_decode.py`

## Workflow
1. Run `health` to confirm decoder readiness.
2. Run `decode` for full line input.
3. For unresolved segments, run `lookup` for candidate codes.
4. Output:
   - decoded text
   - unresolved segments and candidates
   - confidence note

## Output Contract
- `decoded_text`
- `segments`
- `unresolved_candidates`
