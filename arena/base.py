from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class Game(ABC):
    """Abstract base class for turn-based two-player games."""

    @abstractmethod
    def reset(self) -> Any:
        """Return the initial game state."""

    @abstractmethod
    def valid_actions(self, state: Any) -> List[str]:
        """Return a list of valid actions for the given state."""

    @abstractmethod
    def apply_action(self, state: Any, action: str) -> Any:
        """Return a new state after applying `action` to `state`."""

    @abstractmethod
    def is_terminal(self, state: Any) -> bool:
        """Return True if the game is over."""

    @abstractmethod
    def get_winner(self, state: Any) -> int | None:
        """Return 0 or 1 for the winning player, or None if undecided."""

    @abstractmethod
    def render(self, state: Any) -> str:
        """Return a text representation of `state` for LLM consumption."""


class Player(ABC):
    """Base class for players."""

    @abstractmethod
    def select_action(self, game: Game, state: Any) -> str:
        """Return the action to take given the current state."""


class RandomPlayer(Player):
    """Baseline player that selects a random valid action."""

    def select_action(self, game: Game, state: Any) -> str:
        import random

        actions = game.valid_actions(state)
        return random.choice(actions)
