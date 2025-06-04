from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..base import Game


class Othello(Game):
    """Othello/Reversi implementation for two players."""

    def __init__(self, size: int = 8):
        self.size = size

    def reset(self) -> Dict[str, Any]:
        board = [[" "] * self.size for _ in range(self.size)]
        mid = self.size // 2 - 1
        board[mid][mid] = "O"
        board[mid + 1][mid + 1] = "O"
        board[mid][mid + 1] = "X"
        board[mid + 1][mid] = "X"
        return {"board": board, "player": "X"}

    def valid_actions(self, state: Dict[str, Any]) -> List[str]:
        board = state["board"]
        player = state["player"]
        actions = self._valid_actions_for_player(board, player)
        if actions:
            return [f"{r},{c}" for r, c in actions]
        return ["pass"]

    def apply_action(self, state: Dict[str, Any], action: str) -> Dict[str, Any]:
        board = state["board"]
        player = state["player"]
        opponent = "O" if player == "X" else "X"
        new_board = [row.copy() for row in board]

        if action == "pass":
            return {"board": new_board, "player": opponent}

        r, c = map(int, action.split(","))
        if (r, c) not in self._valid_actions_for_player(board, player):
            raise ValueError("Invalid move")

        new_board[r][c] = player
        for dr, dc in self._directions():
            flips: List[Tuple[int, int]] = []
            rr, cc = r + dr, c + dc
            while 0 <= rr < self.size and 0 <= cc < self.size and new_board[rr][cc] == opponent:
                flips.append((rr, cc))
                rr += dr
                cc += dc
            if flips and 0 <= rr < self.size and 0 <= cc < self.size and new_board[rr][cc] == player:
                for fr, fc in flips:
                    new_board[fr][fc] = player
        return {"board": new_board, "player": opponent}

    def is_terminal(self, state: Dict[str, Any]) -> bool:
        board = state["board"]
        current = state["player"]
        opponent = "O" if current == "X" else "X"
        full = all(cell != " " for row in board for cell in row)
        no_moves = not self._valid_actions_for_player(board, current) and not self._valid_actions_for_player(board, opponent)
        return full or no_moves

    def get_winner(self, state: Dict[str, Any]) -> int | None:
        board = state["board"]
        x_count = sum(row.count("X") for row in board)
        o_count = sum(row.count("O") for row in board)
        if x_count == o_count:
            return None
        return 0 if x_count > o_count else 1

    def render(self, state: Dict[str, Any]) -> str:
        board = state["board"]
        rows = ["|".join(row) for row in board]
        board_str = "\n".join(rows)
        return f"```\n{board_str}\n```"

    def _valid_actions_for_player(self, board: List[List[str]], player: str) -> List[Tuple[int, int]]:
        opponent = "O" if player == "X" else "X"
        actions: List[Tuple[int, int]] = []
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] != " ":
                    continue
                if self._would_flip(board, r, c, player, opponent):
                    actions.append((r, c))
        return actions

    def _would_flip(self, board: List[List[str]], r: int, c: int, player: str, opponent: str) -> bool:
        for dr, dc in self._directions():
            rr, cc = r + dr, c + dc
            found_opponent = False
            while 0 <= rr < self.size and 0 <= cc < self.size and board[rr][cc] == opponent:
                rr += dr
                cc += dc
                found_opponent = True
            if found_opponent and 0 <= rr < self.size and 0 <= cc < self.size and board[rr][cc] == player:
                return True
        return False

    def _directions(self) -> List[Tuple[int, int]]:
        return [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
