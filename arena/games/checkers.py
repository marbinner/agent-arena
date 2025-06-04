from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..base import Game


@dataclass
class CheckersState:
    board: List[List[str]]
    turn: int  # 0 for black, 1 for red


class Checkers(Game):
    """Simplified checkers implementation on an 8x8 board."""

    def reset(self) -> CheckersState:
        board = [[" "] * 8 for _ in range(8)]
        for r in range(3):
            for c in range(8):
                if (r + c) % 2 == 1:
                    board[r][c] = "b"
        for r in range(5, 8):
            for c in range(8):
                if (r + c) % 2 == 1:
                    board[r][c] = "r"
        return CheckersState(board, 0)

    def valid_actions(self, state: CheckersState) -> List[str]:
        actions: List[str] = []
        for r in range(8):
            for c in range(8):
                piece = state.board[r][c]
                if not self._belongs_to_player(piece, state.turn):
                    continue
                for dr, dc in self._directions(piece, state.turn):
                    nr, nc = r + dr, c + dc
                    if self._in_bounds(nr, nc) and state.board[nr][nc] == " ":
                        actions.append(f"{r},{c}->{nr},{nc}")
                    elif self._in_bounds(nr, nc) and self._belongs_to_player(state.board[nr][nc], 1 - state.turn):
                        jr, jc = r + 2 * dr, c + 2 * dc
                        if self._in_bounds(jr, jc) and state.board[jr][jc] == " ":
                            actions.append(f"{r},{c}->{jr},{jc}")
        return actions

    def apply_action(self, state: CheckersState, action: str) -> CheckersState:
        src, dst = action.split("->")
        r1, c1 = map(int, src.split(","))
        r2, c2 = map(int, dst.split(","))
        piece = state.board[r1][c1]
        if not self._belongs_to_player(piece, state.turn):
            raise ValueError("Invalid move")
        new_board = [row.copy() for row in state.board]
        new_board[r1][c1] = " "
        if abs(r2 - r1) == 2:
            mr, mc = (r1 + r2) // 2, (c1 + c2) // 2
            new_board[mr][mc] = " "
        if piece == "b" and r2 == 7:
            piece = "B"
        elif piece == "r" and r2 == 0:
            piece = "R"
        new_board[r2][c2] = piece
        return CheckersState(new_board, 1 - state.turn)

    def is_terminal(self, state: CheckersState) -> bool:
        if not self._has_pieces(state, 0) or not self._has_pieces(state, 1):
            return True
        return len(self.valid_actions(state)) == 0

    def get_winner(self, state: CheckersState) -> int | None:
        if not self._has_pieces(state, 0):
            return 1
        if not self._has_pieces(state, 1):
            return 0
        if len(self.valid_actions(state)) == 0:
            return 1 - state.turn
        return None

    def render(self, state: CheckersState) -> str:
        rows = ["|".join(row) for row in state.board]
        board = "\n".join(rows)
        return f"```\n{board}\n```"

    def _belongs_to_player(self, piece: str, player: int) -> bool:
        if player == 0:
            return piece in {"b", "B"}
        return piece in {"r", "R"}

    def _directions(self, piece: str, player: int) -> List[tuple[int, int]]:
        if piece in {"B", "R"}:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return [(1, -1), (1, 1)] if player == 0 else [(-1, -1), (-1, 1)]

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < 8 and 0 <= c < 8

    def _has_pieces(self, state: CheckersState, player: int) -> bool:
        for row in state.board:
            for cell in row:
                if self._belongs_to_player(cell, player):
                    return True
        return False
