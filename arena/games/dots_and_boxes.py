from __future__ import annotations

from typing import Any, Dict, List, Set

from ..base import Game


class DotsAndBoxes(Game):
    """Simplified Dots and Boxes on an n x n grid."""

    def __init__(self, size: int = 2):
        self.size = size
        self.h_edges = (size + 1) * size
        self.total_edges = 2 * size * (size + 1)
        # Precompute edge sets for each box
        self.box_to_edges: List[Set[int]] = []
        for r in range(size):
            for c in range(size):
                top = self._h_edge_index(r, c)
                bottom = self._h_edge_index(r + 1, c)
                left = self._v_edge_index(r, c)
                right = self._v_edge_index(r, c + 1)
                self.box_to_edges.append({top, bottom, left, right})

    def reset(self) -> Dict[str, Any]:
        return {"edges": set(), "boxes": [None] * (self.size * self.size)}

    def valid_actions(self, state: Dict[str, Any]) -> List[str]:
        return [str(i) for i in range(self.total_edges) if i not in state["edges"]]

    def apply_action(self, state: Dict[str, Any], action: str) -> Dict[str, Any]:
        edge = int(action)
        if edge < 0 or edge >= self.total_edges or edge in state["edges"]:
            raise ValueError("Invalid move")
        new_state = {"edges": set(state["edges"]), "boxes": state["boxes"].copy()}
        new_state["edges"].add(edge)
        player = self._current_player(state)
        for idx, edges in enumerate(self.box_to_edges):
            if new_state["boxes"][idx] is None and edges.issubset(new_state["edges"]):
                new_state["boxes"][idx] = player
        return new_state

    def is_terminal(self, state: Dict[str, Any]) -> bool:
        return len(state["edges"]) == self.total_edges

    def get_winner(self, state: Dict[str, Any]) -> int | None:
        if not self.is_terminal(state):
            return None
        p0 = state["boxes"].count(0)
        p1 = state["boxes"].count(1)
        if p0 > p1:
            return 0
        if p1 > p0:
            return 1
        return None

    def render(self, state: Dict[str, Any]) -> str:
        lines: List[str] = []
        for r in range(self.size + 1):
            # Dots and horizontal edges
            line = ""
            for c in range(self.size):
                line += "*"
                edge_idx = self._h_edge_index(r, c)
                line += "---" if edge_idx in state["edges"] else "   "
            line += "*"
            lines.append(line)
            if r < self.size:
                # Vertical edges and boxes row
                line = ""
                for c in range(self.size):
                    edge_idx = self._v_edge_index(r, c)
                    line += "|" if edge_idx in state["edges"] else " "
                    owner = state["boxes"][r * self.size + c]
                    token = "X" if owner == 0 else "O" if owner == 1 else " "
                    line += f" {token} "
                edge_idx = self._v_edge_index(r, self.size)
                line += "|" if edge_idx in state["edges"] else " "
                lines.append(line)
        board = "\n".join(lines)
        return f"```\n{board}\n```"

    def _current_player(self, state: Dict[str, Any]) -> int:
        return len(state["edges"]) % 2

    def _h_edge_index(self, r: int, c: int) -> int:
        return r * self.size + c

    def _v_edge_index(self, r: int, c: int) -> int:
        return self.h_edges + r * (self.size + 1) + c
