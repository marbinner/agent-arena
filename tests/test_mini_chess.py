from arena.games.mini_chess import MiniChess


def test_mini_chess_capture_win():
    game = MiniChess()
    state = game.reset()
    state["board"] = [
        [" ", "k", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", "Q", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", "K"],
    ]
    state["turn"] = "white"

    state = game.apply_action(state, "b4b6")

    assert game.is_terminal(state)
    assert game.get_winner(state) == 0
