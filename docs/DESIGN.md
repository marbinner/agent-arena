# Agent Arena Design Overview

## Purpose
Agent Arena is a collection of turn-based, two-player games designed for language model agents. Each game produces a single winner and exposes its state as text so agents can reason about their moves through prompts.

## Core Concepts

- **Game interface**: All games implement a common `Game` interface defined in `arena/base.py`. The interface exposes methods for resetting the game, listing valid actions, applying actions, detecting terminal states, retrieving the winner, and rendering the current state to text.
- **Game implementations**: Individual games live under `arena/games/`. Each game inherits from `Game` and implements game-specific logic. The initial example is `TicTacToe`.
- **Players**: Agents control players by choosing actions. A simple `RandomPlayer` is provided as a baseline. LLM-driven players will implement the same interface.
- **Game manager**: The `arena.engine` module runs a match between two players, handling turn order and enforcing the game rules.

## Design Goals

1. **Ease of adding new games** – Implementing the `Game` interface should be straightforward. Minimal additional infrastructure should be required.
2. **Text-only interfaces** – To maximize compatibility with LLMs, games communicate exclusively via text.
3. **Deterministic outcomes** – Each game should have clear win conditions and no hidden information to keep evaluation straightforward.
4. **Extensibility** – Additional components such as tournaments or rating systems can build on top of the basic game manager.

## Directory Structure

```text
agent-arena/
├── arena/            # Python package with core modules
│   ├── __init__.py
│   ├── base.py       # Game and Player base classes
│   ├── engine.py     # Logic to run games between two players
│   └── games/
│       ├── __init__.py
│       └── tictactoe.py
├── docs/
│   └── DESIGN.md
└── README.md
```

## Future Work

- Add rating systems to track agent performance.
- Provide a command-line interface to run matches and tournaments.
- Explore reinforcement learning setups for automated prompt evolution.

