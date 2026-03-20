# Global fix routing

## Source of truth
- Upstream repo: `WFGY/ProblemMap/GlobalFixMap/README.md`

## Role
GlobalFixMap is the downstream repair router. It is not the primary diagnosis layer.

## Handoff contract
Once the route is stable, return:
- `family`
- `page`
- `minimal_fix`
- `link` or source path

## Routing rule
- Prefer one family and one page.
- Do not dump the entire fix corpus into the main skill prompt.
- Use vendor or tool-specific pages only when the diagnosis justifies it.
