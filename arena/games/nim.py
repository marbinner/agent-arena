from __future__ import annotations

from typing import List

from ..base import Game


class Nim(Game):
    """Simple impartial game of Nim with a single heap."""

    def __init__(self, total: int = 12, max_take: int = 3):
        self.total = total
        self.max_take = max_take

    def reset(self) -> int:
        return self.total

    def valid_actions(self, state: int) -> List[str]:
        return [str(i) for i in range(1, min(self.max_take, state) + 1)]

    def apply_action(self, state: int, action: str) -> int:
        take = int(action)
        if take < 1 or take > self.max_take or take > state:
            raise ValueError("Invalid move")
        return state - take

    def is_terminal(self, state: int) -> bool:
        return state == 0

    def get_winner(self, state: int) -> int | None:
        if state != 0:
            return None
        moves_made = self.total - state
        return (moves_made - 1) % 2

    def render(self, state: int) -> str:
        sticks = "|" * state
        return f"Remaining: {state}\n```\n{sticks}\n```"
