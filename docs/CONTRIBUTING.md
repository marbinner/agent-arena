# Contributing New Games

To add a new game implementation without stepping on other developers' work, follow these guidelines:

1. **Create a new module** under `arena/games/` with a descriptive file name (e.g. `my_game.py`). Implement a class that subclasses `Game`.
2. **Do not modify** `arena/games/__init__.py`. Game classes are automatically discovered when the package is imported.
3. Add a corresponding test module under `tests/` demonstrating the basic win condition for your game.
4. Update `docs/GAME_BACKLOG.md` to mark the game as implemented if applicable.

Because each game lives in its own file and no central registry needs updating, multiple contributors can work in parallel with minimal merge conflicts.
