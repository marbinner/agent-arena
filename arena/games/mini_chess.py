from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..base import Game


class MiniChess(Game):
    """6x6 chess variant based on Los Alamos chess."""

    def __init__(self):
        self.rows = 6
        self.cols = 6

    def reset(self) -> Dict[str, Any]:
        board = [
            ["r", "n", "q", "k", "n", "r"],
            ["p"] * self.cols,
            [" "] * self.cols,
            [" "] * self.cols,
            ["P"] * self.cols,
            ["R", "N", "Q", "K", "N", "R"],
        ]
        return {"board": board, "turn": "white"}

    def valid_actions(self, state: Dict[str, Any]) -> List[str]:
        board = state["board"]
        turn = state["turn"]
        actions: List[str] = []
        for r in range(self.rows):
            for c in range(self.cols):
                piece = board[r][c]
                if piece == " ":
                    continue
                if turn == "white" and piece.isupper():
                    actions.extend(self._piece_moves(board, r, c, piece, True))
                elif turn == "black" and piece.islower():
                    actions.extend(self._piece_moves(board, r, c, piece, False))
        return actions

    def apply_action(self, state: Dict[str, Any], action: str) -> Dict[str, Any]:
        if action not in self.valid_actions(state):
            raise ValueError("Invalid move")
        board = [row.copy() for row in state["board"]]
        sr, sc = self._parse_coord(action[:2])
        dr, dc = self._parse_coord(action[2:])
        piece = board[sr][sc]
        board[sr][sc] = " "
        board[dr][dc] = piece
        turn = "black" if state["turn"] == "white" else "white"
        return {"board": board, "turn": turn}

    def is_terminal(self, state: Dict[str, Any]) -> bool:
        return self.get_winner(state) is not None or not self.valid_actions(state)

    def get_winner(self, state: Dict[str, Any]) -> int | None:
        flat = sum(state["board"], [])
        if "K" not in flat:
            return 1
        if "k" not in flat:
            return 0
        return None

    def render(self, state: Dict[str, Any]) -> str:
        board = state["board"]
        rows = []
        for r in range(self.rows - 1, -1, -1):
            rows.append("|".join(board[r]))
        board_str = "\n".join(rows)
        return f"Turn: {state['turn']}\n```\n{board_str}\n```"

    # internal helpers -------------------------------------------------

    def _parse_coord(self, coord: str) -> Tuple[int, int]:
        col = ord(coord[0]) - ord("a")
        row = self.rows - int(coord[1])
        return row, col

    def _format_coord(self, r: int, c: int) -> str:
        return f"{chr(ord('a') + c)}{self.rows - r}"

    def _piece_moves(
        self, board: List[List[str]], r: int, c: int, piece: str, white: bool
    ) -> List[str]:
        moves: List[str] = []
        if piece.upper() == "P":
            moves.extend(self._pawn_moves(board, r, c, white))
        elif piece.upper() == "R":
            moves.extend(self._linear_moves(board, r, c, white, directions=[(1,0),(-1,0),(0,1),(0,-1)]))
        elif piece.upper() == "N":
            moves.extend(self._knight_moves(board, r, c, white))
        elif piece.upper() == "Q":
            moves.extend(self._linear_moves(board, r, c, white, directions=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]))
        elif piece.upper() == "K":
            moves.extend(self._king_moves(board, r, c, white))
        return [self._format_coord(r, c) + self._format_coord(dr, dc) for dr, dc in moves]

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def _is_enemy(self, board: List[List[str]], r: int, c: int, white: bool) -> bool:
        piece = board[r][c]
        if piece == " ":
            return False
        return piece.islower() if white else piece.isupper()

    def _is_empty(self, board: List[List[str]], r: int, c: int) -> bool:
        return board[r][c] == " "

    def _pawn_moves(self, board: List[List[str]], r: int, c: int, white: bool) -> List[Tuple[int, int]]:
        moves = []
        dr = -1 if white else 1
        nr = r + dr
        if self._in_bounds(nr, c) and self._is_empty(board, nr, c):
            moves.append((nr, c))
        for dc in (-1, 1):
            nc = c + dc
            if self._in_bounds(nr, nc) and self._is_enemy(board, nr, nc, white):
                moves.append((nr, nc))
        return moves

    def _linear_moves(
        self,
        board: List[List[str]],
        r: int,
        c: int,
        white: bool,
        directions: List[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        moves = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while self._in_bounds(nr, nc):
                if self._is_empty(board, nr, nc):
                    moves.append((nr, nc))
                elif self._is_enemy(board, nr, nc, white):
                    moves.append((nr, nc))
                    break
                else:
                    break
                nr += dr
                nc += dc
        return moves

    def _knight_moves(self, board: List[List[str]], r: int, c: int, white: bool) -> List[Tuple[int, int]]:
        deltas = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]
        moves = []
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if self._in_bounds(nr, nc) and (
                self._is_empty(board, nr, nc) or self._is_enemy(board, nr, nc, white)
            ):
                moves.append((nr, nc))
        return moves

    def _king_moves(self, board: List[List[str]], r: int, c: int, white: bool) -> List[Tuple[int, int]]:
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if not self._in_bounds(nr, nc):
                    continue
                if self._is_empty(board, nr, nc) or self._is_enemy(board, nr, nc, white):
                    moves.append((nr, nc))
        return moves
