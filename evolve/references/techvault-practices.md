# TechVault-sourced Agent Best Practices

Extracted from `~/notes/TechVault/` to strengthen evolve's session analysis,
pattern extraction, and rule generation.

## Context Efficiency (Manus團隊)

- **KV-Cache hit rate** is the most important production metric — 10x cost
  difference between cache hit and miss.
- Use **logits masking** (tool availability state machines) instead of
  dynamically changing tool schemas, which breaks prompt caching.
- Treat the **filesystem as infinite external memory** — write large results
  to files and let agents read via tools, keeping context lean.
- Keep **error paths in context** to prevent repeated mistakes.
- **Few-shot examples** must have diversity; uniform examples cause overfitting.

## Session Archetypes (session-behavior-report)

- **Bimodal distribution**: 57.93% micro-sessions (≤20 lines, <5 min) and
  11.96% deep sessions (≥500 lines).
- **Task completion rate**: 91.33% — abort/restart is per-turn, not failure.
- **Turn-abort rate**: 62.24% (but task-abort only 15.59%) — agents prefer
  short iterations with restarts over long single attempts.
- **Context compression**: Rare (2.55%) — most tasks fit in single context.
- Implication: evolve should classify sessions as micro/deep and weight
  insights accordingly.

## API Resilience (5 個坑)

- **Rate limits**: Exponential backoff mandatory for external APIs; observed
  ban after 15 calls with 30-min timeout.
- **Token budget bloat**: 10 tools × 600 tokens/schema = 6000 token base
  cost. At step 50, history consumes 80% of context window.
- **Memory manager pattern**: Compress old turns to summary +
  checkpoint files for resume, instead of growing context forever.
- **Structured output instability**: ~2% failure rate (every 50 calls).
  Always add JSON validation + retry logic.

## SLO-driven Operations (copilot-sdk discussion)

- Implement **observability before optimization** (not after).
- Track **p95/p99 latency + error rate** as regression signals.
- Use **canary/traffic mirroring** before full rollout of rule changes.
- Build **performance fingerprints** to detect regressions automatically.

## Skill Design (Agent Skills 深度指南)

- Skills use **progressive disclosure**: YAML frontmatter always loaded →
  SKILL.md on relevance → linked files on demand.
- Keep SKILL.md ≤5,000 words; ≤20-50 active skills per session.
- **Evals**: define success criteria → record runs → check rules → score →
  track regressions.
- The **description field** drives skill trigger decisions — it's the single
  most important quality lever.

## Trust Escalation (公司內導入 AI Agent)

- Three-phase adoption: personal exploration → read-only trusted services →
  graduated write access.
- **Data quality + documentation depth** determines agent capability.
- Long tasks need **pre-flight decomposition + milestone checks**.
- Security is **foundational, not afterthought**.

## Actionable Rules for Evolve

These patterns should inform evolve's rule generation:

1. When session history >70% of context window → suggest filesystem offload
2. For micro-sessions (<20 lines): prioritize latency; for deep (>500):
   enable memory compression + checkpointing
3. Per-session tool definition budget: ≤3000 tokens. Warn if >10 tools active
4. API rate-limit recovery: exponential backoff mandatory
5. Track p95 lesson extraction latency; regression gate at >15% increase
6. Read-only → write access must pass 2 approval cycles
