from __future__ import annotations

from typing import Any, List, Tuple

from ..base import Game


class Hex(Game):
    """Connection game on an N x N hex board."""

    def __init__(self, size: int = 3):
        self.size = size
        self.dirs: List[Tuple[int, int]] = [
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
        ]

    def reset(self) -> List[List[str]]:
        return [[" "] * self.size for _ in range(self.size)]

    def valid_actions(self, state: List[List[str]]) -> List[str]:
        actions = []
        for r in range(self.size):
            for c in range(self.size):
                if state[r][c] == " ":
                    actions.append(f"{r},{c}")
        return actions

    def apply_action(self, state: List[List[str]], action: str) -> List[List[str]]:
        r_s, c_s = action.split(",")
        r, c = int(r_s), int(c_s)
        if r < 0 or r >= self.size or c < 0 or c >= self.size:
            raise ValueError("Invalid move")
        if state[r][c] != " ":
            raise ValueError("Invalid move")
        piece = self._current_player(state)
        new_state = [row.copy() for row in state]
        new_state[r][c] = piece
        return new_state

    def is_terminal(self, state: List[List[str]]) -> bool:
        if self.get_winner(state) is not None:
            return True
        return all(cell != " " for row in state for cell in row)

    def get_winner(self, state: List[List[str]]) -> int | None:
        if self._has_path(state, "X"):
            return 0
        if self._has_path(state, "O"):
            return 1
        return None

    def render(self, state: List[List[str]]) -> str:
        rows = []
        indent = ""
        for r in range(self.size):
            rows.append(indent + " ".join(state[r]))
            indent += " "
        board = "\n".join(rows)
        return f"```\n{board}\n```"

    def _current_player(self, state: List[List[str]]) -> str:
        flat = [cell for row in state for cell in row]
        x_count = flat.count("X")
        o_count = flat.count("O")
        return "X" if x_count == o_count else "O"

    def _has_path(self, state: List[List[str]], piece: str) -> bool:
        from collections import deque

        n = self.size
        visited = set()
        queue = deque()
        if piece == "X":
            for r in range(n):
                if state[r][0] == piece:
                    queue.append((r, 0))
                    visited.add((r, 0))
            goal = lambda r, c: c == n - 1
        else:
            for c in range(n):
                if state[0][c] == piece:
                    queue.append((0, c))
                    visited.add((0, c))
            goal = lambda r, c: r == n - 1
        while queue:
            r, c = queue.popleft()
            if goal(r, c):
                return True
            for dr, dc in self.dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in visited and state[nr][nc] == piece:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return False
