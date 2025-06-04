from __future__ import annotations

from typing import List, Tuple

from ..base import Game


class Mancala(Game):
    """Simplified Mancala (Kalah) without extra turns."""

    def reset(self) -> Tuple[List[int], int]:
        board = [4] * 6 + [0] + [4] * 6 + [0]
        return board, 0

    def valid_actions(self, state: Tuple[List[int], int]) -> List[str]:
        board, player = state
        offset = 0 if player == 0 else 7
        return [str(i) for i in range(6) if board[offset + i] > 0]

    def apply_action(self, state: Tuple[List[int], int], action: str) -> Tuple[List[int], int]:
        board, player = state
        pit = int(action)
        if pit < 0 or pit >= 6:
            raise ValueError("Invalid pit index")
        idx = pit if player == 0 else 7 + pit
        seeds = board[idx]
        if seeds == 0:
            raise ValueError("Invalid move")
        new_board = board.copy()
        new_board[idx] = 0
        i = idx
        while seeds:
            i = (i + 1) % 14
            if player == 0 and i == 13:
                continue
            if player == 1 and i == 6:
                continue
            new_board[i] += 1
            seeds -= 1
        # capture
        if player == 0 and 0 <= i <= 5 and new_board[i] == 1 and new_board[12 - i] > 0:
            new_board[6] += new_board[12 - i] + 1
            new_board[i] = 0
            new_board[12 - i] = 0
        elif player == 1 and 7 <= i <= 12 and new_board[i] == 1 and new_board[12 - i] > 0:
            new_board[13] += new_board[12 - i] + 1
            new_board[i] = 0
            new_board[12 - i] = 0
        # check game end
        if all(n == 0 for n in new_board[0:6]) or all(n == 0 for n in new_board[7:13]):
            new_board[6] += sum(new_board[0:6])
            new_board[13] += sum(new_board[7:13])
            for j in range(0, 6):
                new_board[j] = 0
            for j in range(7, 13):
                new_board[j] = 0
        next_player = 1 - player
        return new_board, next_player

    def is_terminal(self, state: Tuple[List[int], int]) -> bool:
        board, _ = state
        return all(n == 0 for n in board[0:6]) or all(n == 0 for n in board[7:13])

    def get_winner(self, state: Tuple[List[int], int]) -> int | None:
        board, _ = state
        if not self.is_terminal(state):
            return None
        if board[6] > board[13]:
            return 0
        if board[13] > board[6]:
            return 1
        return None

    def render(self, state: Tuple[List[int], int]) -> str:
        board, _ = state
        top = " ".join(str(board[i]) for i in range(12, 6, -1))
        bottom = " ".join(str(board[i]) for i in range(0, 6))
        board_str = f" {board[13]} | {top}\n{bottom} | {board[6]}"
        return f"```\n{board_str}\n```"
