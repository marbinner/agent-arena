from __future__ import annotations

from typing import List

from ..base import Game


class MultiHeapNim(Game):
    """Nim variant with multiple heaps."""

    def __init__(self, heaps: List[int] | None = None, max_take: int | None = 3):
        if heaps is None:
            heaps = [3, 4, 5]
        self.initial_heaps = list(heaps)
        self.max_take = max_take
        self.total = sum(heaps)

    def reset(self) -> List[int]:
        return self.initial_heaps.copy()

    def valid_actions(self, state: List[int]) -> List[str]:
        actions: List[str] = []
        for i, heap in enumerate(state):
            if heap == 0:
                continue
            limit = heap if self.max_take is None else min(self.max_take, heap)
            for t in range(1, limit + 1):
                actions.append(f"{i},{t}")
        return actions

    def apply_action(self, state: List[int], action: str) -> List[int]:
        try:
            heap_idx_str, take_str = action.split(",")
            heap_idx = int(heap_idx_str)
            take = int(take_str)
        except ValueError as exc:
            raise ValueError("Invalid action format") from exc
        if heap_idx < 0 or heap_idx >= len(state):
            raise ValueError("Invalid heap index")
        heap = state[heap_idx]
        if take < 1 or take > heap:
            raise ValueError("Invalid number to take")
        if self.max_take is not None and take > self.max_take:
            raise ValueError("Invalid number to take")
        new_state = state.copy()
        new_state[heap_idx] -= take
        return new_state

    def is_terminal(self, state: List[int]) -> bool:
        return all(h == 0 for h in state)

    def get_winner(self, state: List[int]) -> int | None:
        if not self.is_terminal(state):
            return None
        moves_made = self.total - sum(state)
        return (moves_made - 1) % 2

    def render(self, state: List[int]) -> str:
        lines = [f"{i}: {'|' * heap}" for i, heap in enumerate(state)]
        board = "\n".join(lines)
        return f"```\n{board}\n```"
