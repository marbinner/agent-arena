from __future__ import annotations

from typing import Any

from .base import Game, Player


class GameEngine:
    """Run a match between two players."""

    def __init__(self, game: Game, player0: Player, player1: Player):
        self.game = game
        self.players = [player0, player1]

    def play(self) -> int:
        """Run the game and return the winning player (0 or 1)."""
        state = self.game.reset()
        current = 0
        while not self.game.is_terminal(state):
            player = self.players[current]
            action = player.select_action(self.game, state)
            state = self.game.apply_action(state, action)
            current = 1 - current
        winner = self.game.get_winner(state)
        assert winner is not None
        return winner
