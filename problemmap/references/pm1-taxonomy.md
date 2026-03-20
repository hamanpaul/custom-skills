# PM1 taxonomy

## Source of truth
- Upstream repo: `WFGY/ProblemMap/README.md`
- Stable table: the 16-row Problem Map 1.0 failure catalog

## Non-loss rules
- Keep exactly 16 stable identifiers.
- Do not renumber, merge, or invent `17+` categories.
- Map a bug to 1-3 PM1 candidates before widening the diagnosis.
- Preserve `symptom -> PM1 number -> source path` traceability.

## PM1 stable identifiers
1. `[IN]` hallucination & chunk drift
2. `[RE]` interpretation collapse
3. `[RE]` long reasoning chains
4. `[RE]` bluffing / overconfidence
5. `[IN]` semantic != embedding
6. `[RE]` logic collapse & recovery
7. `[ST]` memory breaks across sessions
8. `[IN]` debugging black box
9. `[ST]` entropy collapse
10. `[RE]` creative freeze
11. `[RE]` symbolic collapse
12. `[RE]` philosophical recursion
13. `[ST]` multi-agent chaos
14. `[OP]` bootstrap ordering
15. `[OP]` deployment deadlock
16. `[OP]` pre-deploy collapse

## Practical use
- Use PM1 as the stable public vocabulary layer.
- Return PM1 candidates even when Atlas routing is still partial.
- If PM1 evidence is weak, say so explicitly instead of forcing a false-hard mapping.
