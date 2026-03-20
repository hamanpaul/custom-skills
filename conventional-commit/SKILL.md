---
name: conventional-commit
description: Create standard commit messages using Conventional Commits with safe multiline shell quoting.
---

# conventional-commit

## Trigger
Use when user asks to prepare commit messages or commit staged changes.

## Commit Format
- Header: `type(scope): subject`
- Optional body: context, rationale, impact
- Optional footer: issue links or metadata
- Breaking change note: `BREAKING CHANGE: <description>`

## Language Policy
- Detect GitHub repo owner from `git remote get-url origin` when possible.
- If owner is `hamanpaul`, write commit content in Traditional Chinese (`zh-TW`):
  - `subject` in `type(scope): subject`
  - optional body
  - optional footer text (except reserved tokens like `BREAKING CHANGE`)
- For non-`hamanpaul` repos, follow user/project preference.
- If owner cannot be determined, ask user before finalizing the message language.

## Allowed Types
- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`
- `perf`

## Workflow
1. Inspect staged diff and summarize intent.
2. Resolve repo owner and apply language policy (`hamanpaul/*` => `zh-TW`).
3. Choose `type(scope)` and concise subject.
4. Add body bullets for key changes.
5. Add footer if needed.
6. If incompatible behavior changes exist, include `BREAKING CHANGE`.
7. Emit shell-safe command form for multiline commit messages.

## Output Example
```bash
git commit -m 'feat(agents): add weighted insights pipeline
- add project_insights script
- add git gate fallback handling
BREAKING CHANGE: switches docs root to .agents
'
```
