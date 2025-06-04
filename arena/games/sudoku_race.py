from __future__ import annotations

from typing import List

from ..base import Game


class SudokuRace(Game):
    """Simple 4x4 Sudoku race where players fill the board."""

    def __init__(self, size: int = 4):
        if size != 4:
            raise ValueError("Only 4x4 Sudoku supported")
        self.size = size
        self.sub = 2  # subgrid size

    def reset(self) -> List[List[int]]:
        # Preset puzzle used for tests
        return [
            [1, 0, 0, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [3, 0, 0, 2],
        ]

    def valid_actions(self, state: List[List[int]]) -> List[str]:
        actions: List[str] = []
        for r in range(self.size):
            for c in range(self.size):
                if state[r][c] != 0:
                    continue
                for v in range(1, self.size + 1):
                    if self._is_valid_move(state, r, c, v):
                        actions.append(f"{r},{c},{v}")
        return actions

    def apply_action(self, state: List[List[int]], action: str) -> List[List[int]]:
        try:
            r, c, v = map(int, action.split(","))
        except Exception as e:
            raise ValueError("Action must be 'row,col,value'") from e
        if not (0 <= r < self.size and 0 <= c < self.size and 1 <= v <= self.size):
            raise ValueError("Action out of bounds")
        if state[r][c] != 0:
            raise ValueError("Cell already filled")
        if not self._is_valid_move(state, r, c, v):
            raise ValueError("Invalid move")
        new_state = [row.copy() for row in state]
        new_state[r][c] = v
        return new_state

    def is_terminal(self, state: List[List[int]]) -> bool:
        return all(cell != 0 for row in state for cell in row)

    def get_winner(self, state: List[List[int]]) -> int | None:
        if not self.is_terminal(state):
            return None
        moves = sum(cell != 0 for row in state for cell in row)
        return (moves - 1) % 2

    def render(self, state: List[List[int]]) -> str:
        lines = [" ".join(str(v) if v != 0 else "." for v in row) for row in state]
        board = "\n".join(lines)
        return f"```\n{board}\n```"

    def _is_valid_move(self, state: List[List[int]], r: int, c: int, v: int) -> bool:
        if any(state[r][i] == v for i in range(self.size)):
            return False
        if any(state[i][c] == v for i in range(self.size)):
            return False
        sr = (r // self.sub) * self.sub
        sc = (c // self.sub) * self.sub
        for i in range(sr, sr + self.sub):
            for j in range(sc, sc + self.sub):
                if state[i][j] == v:
                    return False
        return True
