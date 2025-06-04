# Agent Arena

Agent Arena is a playground for evaluating language model agents through head-to-head games. Each game is turn-based, produces a single winner, and exposes its state as text so that LLMs can decide on their next move.

The project is organized as a small Python package with a common interface for games and players. New games can be added by implementing the `Game` interface.

Planned games are listed in [docs/GAME_BACKLOG.md](docs/GAME_BACKLOG.md).

If you'd like to contribute a new game, see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).

## Getting Started

1. Install Python 3.10 or later.
2. Clone the repository and install the package in editable mode:

```bash
pip install -e .
```

3. Run an example match:

```python
from arena.games.tictactoe import TicTacToe
from arena import GameEngine, RandomPlayer

engine = GameEngine(TicTacToe(), RandomPlayer(), RandomPlayer())
winner = engine.play()
print("Winner:", winner)
```

## Documentation

Detailed design notes live in [docs/DESIGN.md](docs/DESIGN.md).
