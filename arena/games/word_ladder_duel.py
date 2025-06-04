from __future__ import annotations

from typing import Any, List, Tuple, Iterable

from ..base import Game


class WordLadderDuel(Game):
    """Two-player word ladder race from start to goal."""

    def __init__(self, start: str, goal: str, dictionary: Iterable[str] | None = None):
        if len(start) != len(goal):
            raise ValueError("start and goal must be the same length")
        self.start = start.lower()
        self.goal = goal.lower()
        self.dictionary = set(w.lower() for w in dictionary) if dictionary else None
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"

    def reset(self) -> Tuple[str, int]:
        return (self.start, 0)

    def valid_actions(self, state: Tuple[str, int]) -> List[str]:
        word, _ = state
        actions: List[str] = []
        for i, ch in enumerate(word):
            for new_ch in self.alphabet:
                if new_ch == ch:
                    continue
                candidate = word[:i] + new_ch + word[i + 1 :]
                if self.dictionary is None or candidate in self.dictionary:
                    actions.append(candidate)
        return actions

    def apply_action(self, state: Tuple[str, int], action: str) -> Tuple[str, int]:
        word, count = state
        action = action.lower()
        if len(action) != len(word):
            raise ValueError("Invalid word length")
        diff = sum(a != b for a, b in zip(word, action))
        if diff != 1:
            raise ValueError("Action must change exactly one letter")
        if self.dictionary is not None and action not in self.dictionary:
            raise ValueError("Word not in dictionary")
        return (action, count + 1)

    def is_terminal(self, state: Tuple[str, int]) -> bool:
        return state[0] == self.goal

    def get_winner(self, state: Tuple[str, int]) -> int | None:
        word, count = state
        if word != self.goal:
            return None
        return (count - 1) % 2

    def render(self, state: Tuple[str, int]) -> str:
        word, _ = state
        return f"Current: {word} -> Goal: {self.goal}"
