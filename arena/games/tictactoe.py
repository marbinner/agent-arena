from __future__ import annotations

from typing import Any, List

from ..base import Game


class TicTacToe(Game):
    """Simple 3x3 tic-tac-toe implementation."""

    def reset(self) -> List[str]:
        return [" "] * 9

    def valid_actions(self, state: List[str]) -> List[str]:
        return [str(i) for i, cell in enumerate(state) if cell == " "]

    def apply_action(self, state: List[str], action: str) -> List[str]:
        idx = int(action)
        if state[idx] != " ":
            raise ValueError("Invalid move")
        new_state = state.copy()
        new_state[idx] = self._current_player(state)
        return new_state

    def is_terminal(self, state: List[str]) -> bool:
        return self.get_winner(state) is not None or all(cell != " " for cell in state)

    def get_winner(self, state: List[str]) -> int | None:
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if state[a] != " " and state[a] == state[b] == state[c]:
                return 0 if state[a] == "X" else 1
        return None

    def render(self, state: List[str]) -> str:
        rows = ["|".join(state[i : i + 3]) for i in range(0, 9, 3)]
        board = "\n-----\n".join(rows)
        return f"```\n{board}\n```"

    def _current_player(self, state: List[str]) -> str:
        x_count = state.count("X")
        o_count = state.count("O")
        return "X" if x_count == o_count else "O"
