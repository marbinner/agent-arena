from __future__ import annotations

from typing import Any, List

from ..base import Game


class ConnectFour(Game):
    """Classic Connect Four on a 7x6 board."""

    def __init__(self, rows: int = 6, cols: int = 7, connect: int = 4):
        self.rows = rows
        self.cols = cols
        self.connect = connect

    def reset(self) -> List[List[str]]:
        return [[" "] * self.cols for _ in range(self.rows)]

    def valid_actions(self, state: List[List[str]]) -> List[str]:
        return [str(c) for c in range(self.cols) if state[0][c] == " "]

    def apply_action(self, state: List[List[str]], action: str) -> List[List[str]]:
        col = int(action)
        if state[0][col] != " ":
            raise ValueError("Invalid move")
        piece = self._current_player(state)
        new_state = [row.copy() for row in state]
        for r in range(self.rows - 1, -1, -1):
            if new_state[r][col] == " ":
                new_state[r][col] = piece
                break
        return new_state

    def is_terminal(self, state: List[List[str]]) -> bool:
        return self.get_winner(state) is not None or all(state[0][c] != " " for c in range(self.cols))

    def get_winner(self, state: List[List[str]]) -> int | None:
        for r in range(self.rows):
            for c in range(self.cols):
                piece = state[r][c]
                if piece == " ":
                    continue
                if self._check_direction(state, r, c, 1, 0, piece):
                    return 0 if piece == "X" else 1
                if self._check_direction(state, r, c, 0, 1, piece):
                    return 0 if piece == "X" else 1
                if self._check_direction(state, r, c, 1, 1, piece):
                    return 0 if piece == "X" else 1
                if self._check_direction(state, r, c, 1, -1, piece):
                    return 0 if piece == "X" else 1
        return None

    def render(self, state: List[List[str]]) -> str:
        rows = ["|".join(row) for row in state]
        board = "\n".join(rows)
        return f"```\n{board}\n```"

    def _check_direction(self, state: List[List[str]], r: int, c: int, dr: int, dc: int, piece: str) -> bool:
        for i in range(1, self.connect):
            nr, nc = r + dr * i, c + dc * i
            if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
                return False
            if state[nr][nc] != piece:
                return False
        return True

    def _current_player(self, state: List[List[str]]) -> str:
        flat = sum(state, [])
        x_count = flat.count("X")
        o_count = flat.count("O")
        return "X" if x_count == o_count else "O"
