#!/usr/bin/env python3
"""Extensible auto-play policy agents for snake demo."""

from __future__ import annotations

from dataclasses import dataclass

from snake_core import DIRECTION_ORDER, SnakeEngine, Snapshot


@dataclass(frozen=True)
class AgentMessage:
    from_agent: str
    to_agent: str
    intent: str
    payload_text: str


class FoodHunterAgent:
    agent_id = "food-hunter"

    def propose(self, engine: SnakeEngine, snap: Snapshot) -> tuple[str, str]:
        candidates = engine.available_directions()
        if not candidates:
            return snap.direction, "no_safe_candidates"

        def score(direction: str) -> tuple[int, int]:
            nx, ny = self._next_point(snap.head, direction)
            fx, fy = snap.food
            dist = abs(nx - fx) + abs(ny - fy)
            turn_penalty = 0 if direction == snap.direction else 1
            return (dist, turn_penalty)

        chosen = min(candidates, key=score)
        return chosen, f"prefer_food dist={score(chosen)[0]}"

    @staticmethod
    def _next_point(head: tuple[int, int], direction: str) -> tuple[int, int]:
        x, y = head
        if direction == "up":
            return (x, y - 1)
        if direction == "right":
            return (x + 1, y)
        if direction == "down":
            return (x, y + 1)
        return (x - 1, y)


class SafetyGuardAgent:
    agent_id = "safety-guard"

    def review(self, engine: SnakeEngine, snap: Snapshot, proposed: str) -> tuple[str, str]:
        if engine.is_safe(proposed):
            return proposed, "proposed_safe"

        candidates = engine.available_directions()
        if not candidates:
            return proposed, "no_safe_move"

        chosen = max(candidates, key=lambda direction: self._mobility_score(engine, direction))
        return chosen, f"override_unsafe mobility={self._mobility_score(engine, chosen)}"

    def _mobility_score(self, engine: SnakeEngine, direction: str) -> int:
        nx, ny = FoodHunterAgent._next_point(engine.head, direction)
        score = 0
        for d in DIRECTION_ORDER:
            tx, ty = FoodHunterAgent._next_point((nx, ny), d)
            if 0 <= tx < engine.width and 0 <= ty < engine.height:
                score += 1
        return score


class FallbackAgent:
    agent_id = "fallback-agent"

    def finalize(self, engine: SnakeEngine, snap: Snapshot, proposed: str) -> tuple[str, str]:
        if engine.is_safe(proposed):
            return proposed, "keep_reviewed"
        candidates = engine.available_directions()
        if not candidates:
            return proposed, "terminal_no_move"
        return candidates[0], "fallback_first_safe"


class MultiAgentPolicy:
    def __init__(self) -> None:
        self.food_hunter = FoodHunterAgent()
        self.safety_guard = SafetyGuardAgent()
        self.fallback = FallbackAgent()

    @property
    def agent_ids(self) -> list[str]:
        return [self.food_hunter.agent_id, self.safety_guard.agent_id, self.fallback.agent_id]

    def decide(self, engine: SnakeEngine) -> tuple[str, list[AgentMessage]]:
        snap = engine.snapshot()
        proposed, reason1 = self.food_hunter.propose(engine, snap)
        reviewed, reason2 = self.safety_guard.review(engine, snap, proposed)
        final_move, reason3 = self.fallback.finalize(engine, snap, reviewed)

        messages = [
            AgentMessage(
                from_agent=self.food_hunter.agent_id,
                to_agent=self.safety_guard.agent_id,
                intent="propose",
                payload_text=f"step={snap.step} proposed={proposed} reason={reason1}",
            ),
            AgentMessage(
                from_agent=self.safety_guard.agent_id,
                to_agent=self.fallback.agent_id,
                intent="review",
                payload_text=f"step={snap.step} reviewed={reviewed} reason={reason2}",
            ),
            AgentMessage(
                from_agent=self.fallback.agent_id,
                to_agent="coordinator",
                intent="answer",
                payload_text=f"step={snap.step} final={final_move} reason={reason3}",
            ),
        ]
        return final_move, messages
