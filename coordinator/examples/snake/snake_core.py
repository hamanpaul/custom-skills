#!/usr/bin/env python3
"""Terminal snake core engine for auto-play and multi-agent experiments."""

from __future__ import annotations

from dataclasses import dataclass
import random


DIRECTIONS: dict[str, tuple[int, int]] = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
}
DIRECTION_ORDER = ["up", "right", "down", "left"]
OPPOSITE = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


Point = tuple[int, int]


@dataclass(frozen=True)
class Snapshot:
    width: int
    height: int
    step: int
    score: int
    direction: str
    head: Point
    body: tuple[Point, ...]
    food: Point


class SnakeEngine:
    def __init__(self, width: int = 20, height: int = 12, seed: int = 0) -> None:
        if width < 6 or height < 6:
            raise ValueError("width/height must be >= 6")
        self.width = width
        self.height = height
        self._rnd = random.Random(seed)
        cx = width // 2
        cy = height // 2
        self.body: list[Point] = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = "right"
        self.step = 0
        self.score = 0
        self.food = self._spawn_food()

    @property
    def head(self) -> Point:
        return self.body[0]

    def snapshot(self) -> Snapshot:
        return Snapshot(
            width=self.width,
            height=self.height,
            step=self.step,
            score=self.score,
            direction=self.direction,
            head=self.head,
            body=tuple(self.body),
            food=self.food,
        )

    def _next_head(self, direction: str) -> Point:
        dx, dy = DIRECTIONS[direction]
        x, y = self.head
        return (x + dx, y + dy)

    def _in_bounds(self, pos: Point) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def _spawn_food(self) -> Point:
        occupied = set(self.body)
        cells = [(x, y) for y in range(self.height) for x in range(self.width) if (x, y) not in occupied]
        if not cells:
            return self.head
        return self._rnd.choice(cells)

    def _normalize_direction(self, direction: str) -> str:
        text = direction.strip().lower()
        if text not in DIRECTIONS:
            return self.direction
        if len(self.body) > 1 and OPPOSITE[text] == self.direction:
            return self.direction
        return text

    def is_safe(self, direction: str) -> bool:
        d = self._normalize_direction(direction)
        nxt = self._next_head(d)
        if not self._in_bounds(nxt):
            return False
        will_eat = nxt == self.food
        occupied = set(self.body if will_eat else self.body[:-1])
        return nxt not in occupied

    def available_directions(self) -> list[str]:
        return [d for d in DIRECTION_ORDER if self.is_safe(d)]

    def apply(self, direction: str) -> bool:
        d = self._normalize_direction(direction)
        if not self.is_safe(d):
            self.step += 1
            return False
        nxt = self._next_head(d)
        self.body.insert(0, nxt)
        if nxt == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.body.pop()
        self.direction = d
        self.step += 1
        return True

    def render(self) -> str:
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        fx, fy = self.food
        if self._in_bounds(self.food):
            grid[fy][fx] = "*"
        for x, y in self.body[1:]:
            if self._in_bounds((x, y)):
                grid[y][x] = "o"
        hx, hy = self.head
        if self._in_bounds(self.head):
            grid[hy][hx] = "@"

        border = "+" + ("-" * self.width) + "+"
        lines = [border]
        for row in grid:
            lines.append("|" + "".join(row) + "|")
        lines.append(border)
        lines.append(f"step={self.step} score={self.score} len={len(self.body)} dir={self.direction}")
        return "\n".join(lines)
