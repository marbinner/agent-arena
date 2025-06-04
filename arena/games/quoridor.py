from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

from ..base import Game


class Quoridor(Game):
    """Simplified Quoridor implementation on a square board."""

    def __init__(self, size: int = 5, walls_per_player: int = 5):
        self.size = size
        self.walls_per_player = walls_per_player
        self.start_positions = [(0, size // 2), (size - 1, size // 2)]

    def reset(self) -> Dict[str, Any]:
        return {
            "pos": [self.start_positions[0], self.start_positions[1]],
            "h_walls": set(),
            "v_walls": set(),
            "remaining": [self.walls_per_player, self.walls_per_player],
            "current": 0,
        }

    def valid_actions(self, state: Dict[str, Any]) -> List[str]:
        actions: List[str] = []
        player = state["current"]
        r, c = state["pos"][player]
        opponent_pos = state["pos"][1 - player]

        if r > 0 and (r - 1, c) not in state["h_walls"] and opponent_pos != (r - 1, c):
            actions.append("U")
        if r < self.size - 1 and (r, c) not in state["h_walls"] and opponent_pos != (r + 1, c):
            actions.append("D")
        if c > 0 and (r, c - 1) not in state["v_walls"] and opponent_pos != (r, c - 1):
            actions.append("L")
        if c < self.size - 1 and (r, c) not in state["v_walls"] and opponent_pos != (r, c + 1):
            actions.append("R")

        if state["remaining"][player] > 0:
            for rr in range(self.size - 1):
                for cc in range(self.size - 1):
                    if (rr, cc) not in state["h_walls"]:
                        actions.append(f"H {rr} {cc}")
                    if (rr, cc) not in state["v_walls"]:
                        actions.append(f"V {rr} {cc}")
        return actions

    def apply_action(self, state: Dict[str, Any], action: str) -> Dict[str, Any]:
        player = state["current"]
        new_state = {
            "pos": state["pos"].copy(),
            "h_walls": state["h_walls"].copy(),
            "v_walls": state["v_walls"].copy(),
            "remaining": state["remaining"].copy(),
            "current": 1 - player,
        }

        parts = action.split()
        if parts[0] in {"U", "D", "L", "R"}:
            r, c = state["pos"][player]
            if parts[0] == "U":
                nr, nc = r - 1, c
                if nr < 0 or (r - 1, c) in state["h_walls"]:
                    raise ValueError("Invalid move")
            elif parts[0] == "D":
                nr, nc = r + 1, c
                if nr >= self.size or (r, c) in state["h_walls"]:
                    raise ValueError("Invalid move")
            elif parts[0] == "L":
                nr, nc = r, c - 1
                if nc < 0 or (r, c - 1) in state["v_walls"]:
                    raise ValueError("Invalid move")
            else:  # "R"
                nr, nc = r, c + 1
                if nc >= self.size or (r, c) in state["v_walls"]:
                    raise ValueError("Invalid move")
            if (nr, nc) == state["pos"][1 - player]:
                raise ValueError("Cannot move onto opponent")
            new_state["pos"][player] = (nr, nc)
        elif parts[0] in {"H", "V"}:
            if len(parts) != 3:
                raise ValueError("Invalid action format")
            rr, cc = int(parts[1]), int(parts[2])
            if rr < 0 or rr >= self.size - 1 or cc < 0 or cc >= self.size - 1:
                raise ValueError("Wall out of bounds")
            if new_state["remaining"][player] <= 0:
                raise ValueError("No walls remaining")
            if parts[0] == "H":
                if (rr, cc) in state["h_walls"]:
                    raise ValueError("Wall already present")
                new_state["h_walls"].add((rr, cc))
            else:
                if (rr, cc) in state["v_walls"]:
                    raise ValueError("Wall already present")
                new_state["v_walls"].add((rr, cc))
            new_state["remaining"][player] -= 1
        else:
            raise ValueError("Unknown action")

        return new_state

    def is_terminal(self, state: Dict[str, Any]) -> bool:
        if state["pos"][0][0] == self.size - 1:
            return True
        if state["pos"][1][0] == 0:
            return True
        return False

    def get_winner(self, state: Dict[str, Any]) -> int | None:
        if state["pos"][0][0] == self.size - 1:
            return 0
        if state["pos"][1][0] == 0:
            return 1
        return None

    def render(self, state: Dict[str, Any]) -> str:
        board = [["." for _ in range(self.size)] for _ in range(self.size)]
        board[state["pos"][0][0]][state["pos"][0][1]] = "0"
        board[state["pos"][1][0]][state["pos"][1][1]] = "1"
        rows = [" ".join(row) for row in board]
        grid = "\n".join(rows)
        h = sorted(list(state["h_walls"]))
        v = sorted(list(state["v_walls"]))
        return (
            f"```\n{grid}\n```\n"
            f"H walls: {h}\nV walls: {v}\n"
            f"Remaining: {state['remaining']}"
        )

