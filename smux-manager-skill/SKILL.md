---
name: smux-manager-skill
description: Run a smux-native manager/worker workflow over tmux panes with task envelopes, sanitized context mirrors, and optional thin helper scripts.
compatibility: Designed for GitHub Copilot CLI workflows.
metadata:
  author: sw2-skills-collection
  version: "0.1.0"
---

# Smux Manager Skill

Use this skill when one pane should act as a **manager agent** and coordinate one or more **worker agent panes** through `tmux-bridge`, without first building a separate orchestration runtime.

This version also supports a **ProblemMap drift guard**: the manager can diagnose suspicious worker behavior from the shared context mirror before blindly retrying, widening scope, or rewriting prompts.

## When to use

- You already have tmux panes running agents such as Copilot CLI or Codex.
- You want **1-to-many task dispatch** from one manager pane to multiple worker panes.
- You want worker panes to see a **shared, sanitized manager context**.
- You want to stay **smux-native first** and add helpers only if pain appears.

## When not to use

- You need unattended execution, durable replay, or restart recovery.
- You need queue semantics that survive process or tmux restarts.
- You need device/UART brokering or policy enforcement beyond pane orchestration.

## Core model

1. **Manager is just another pane**
   - The first version should not assume a daemon or server.
   - The manager agent uses `tmux-bridge` directly.

2. **Pane transport is for control signals**
   - Use pane messages for task assignment and short status.
   - Put long outputs in artifact files and send paths back.

3. **Workers should read a context mirror, not scrape the manager pane**
   - Keep a sanitized `context.jsonl` / `context.md` / `live.log`.
   - Workers consume snapshot + delta using `context_seq`.

4. **Manager is the only task authority**
   - Only the manager may assign, requeue, cancel, or rotate leases.
   - Workers may ask for context, report progress, succeed, or fail.

## Roles

### Manager pane

- Discovers worker panes
- Writes the shared context mirror
- Sends `TASK_ASSIGN`
- Collects `TASK_ACCEPT`, `STATUS`, `RESULT`, `FAIL`
- Runs ProblemMap drift checks when a worker looks off-task, confused, or stalled
- Decides requeue / retry / cancel

### Worker panes

- Receive `TASK_ASSIGN`
- Read the current context snapshot and deltas
- Reply through `tmux-bridge` using protocol verbs
- Write long outputs to artifact files

### Optional bus pane

- Runs `tail -f runtime/context/live.log`
- Gives humans and agents a passive shared view of manager↔worker traffic

## Recommended workflow

1. Initialize a runtime directory:

   ```bash
   smux-manager-skill/scripts/init-runtime.sh /tmp/smux-manager-demo
   ```

2. Label panes early:

   ```bash
   tmux-bridge name "$(tmux-bridge id)" manager
   tmux-bridge name %1 codex
   ```

3. Append sanitized context entries as the manager clarifies or narrows work:

   ```bash
   smux-manager-skill/scripts/append-context.sh \
     /tmp/smux-manager-demo 110 manager codex CONTEXT task-123 \
     "Investigate failing auth tests under tests/ and src/auth.ts"
   ```

4. Dispatch a task:

   ```bash
   smux-manager-skill/scripts/send-task.sh \
     codex task-123 codex 45 110 lease-task-123 \
     "Investigate failing auth tests" "tests/ src/auth.ts" \
     "/tmp/smux-manager-demo/artifacts"
   ```

5. Track short replies in the manager pane and mirror meaningful ones back into `context.jsonl` / `context.md` / `live.log`.

6. When a worker starts to drift, diagnose before you re-prompt. For example:

   ```bash
   python3 smux-manager-skill/scripts/problemmap-guard.py \
     /tmp/smux-manager-demo task-123 codex \
     --expected "Investigate failing auth tests under tests/ and src/auth.ts"
   ```

   This writes a ProblemMap case, diagnosis, and gated event artifact under:

   ```text
   /tmp/smux-manager-demo/artifacts/problemmap/task-123/codex/
   ```

   Use the diagnosis to decide whether to re-ground the task, restore continuity, tighten boundaries, or reassign the worker.

7. Let workers send protocol replies with the helper when PATH or read-guard friction appears:

   ```bash
   TMUX_BRIDGE_BIN="$HOME/.smux/bin/tmux-bridge" \
   smux-manager-skill/scripts/send-reply.sh \
     manager TASK_ACCEPT task-123 codex 46 110 lease-task-123 \
     "Accepted and starting inspection"
   ```

## Protocol summary

Required verbs:

- `HELLO`
- `TASK_ASSIGN`
- `TASK_ACCEPT`
- `HEARTBEAT`
- `STATUS`
- `ASK`
- `RESULT`
- `FAIL`

Required fields on every task-bound message:

- `task`
- `worker`
- `seq`
- `lease_token`
- `context_seq`

See `references/PROTOCOL.md` for the wire format and examples.

## Context mirror policy

- Mirror **only manager↔worker sanitized context**
- Do **not** mirror user↔manager conversation by default
- Use `context_seq` so workers can read snapshot + delta instead of scraping manager scrollback

See `references/CONTEXT_MIRROR.md` for file layout and update rules.

## ProblemMap drift guard

Use the ProblemMap guard when a worker shows signs such as:

- repeated `ASK` messages on the same task
- multiple `STATUS` updates with little forward motion
- a `FAIL` that suggests confusion, loss of continuity, or runtime closure issues
- a `RESULT` that does not line up with the manager's stated goal

The guard reads `runtime/context/context.jsonl`, builds a compact failure-bearing case, routes it through the sibling `problemmap` skill, and emits:

- `case.json`
- `diagnosis.json`
- `event.json`

The diagnosis is manager-facing. It helps the manager choose the next control move instead of improvising generic prompt changes.

See `references/PROBLEMMAP_GUARD.md` for trigger patterns and intervention guidance.

## Thin helper scripts

- `scripts/init-runtime.sh` — create runtime folders and mirror files
- `scripts/append-context.sh` — append a sanitized context event to JSONL / Markdown / live log
- `scripts/send-task.sh` — send a `TASK_ASSIGN` envelope using the required read-act-read cycle
- `scripts/send-reply.sh` — send worker replies with tmux-bridge path fallback and read-act-read handling
- `scripts/problemmap-guard.py` — build a ProblemMap case from context events and emit a route-first drift diagnosis

## Observed thin-helper thresholds

The smux-native MVP worked, but the first live validations exposed two real sources of friction:

1. **Pane-local PATH drift**
   - Fresh worker panes did not always have `tmux-bridge` on `PATH`.
   - The pragmatic fix is to support `TMUX_BRIDGE_BIN` or fall back to `~/.smux/bin/tmux-bridge`.

2. **Read guard recovery**
   - Workers can accidentally `type` a reply and then forget the extra `read` required before `keys Enter`.
   - A helper script is worth keeping once more than one worker pane is active.

3. **Worker drift is often continuity or boundary failure, not just a bad prompt**
   - Repeated `ASK`, stalled `STATUS`, and off-target `RESULT` messages can mean F2/F3/F4/F6-class problems.
   - Run the ProblemMap guard before expanding task scope or retrying with noisier instructions.

## Escalate beyond smux when

- You need durable queues or replay after restart
- Many worker panes make manual status tracking too noisy
- Lease / retry / artifact tracking becomes too tedious by hand
- The manager needs to run unattended

At that point, keep the same protocol and context mirror, then add a thin helper layer or a real runtime on top.
