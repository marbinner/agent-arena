from arena.games.connect_four import ConnectFour
from arena.games.nim import Nim
from arena.games.othello import Othello


def test_connect_four_vertical_win():
    game = ConnectFour()
    state = game.reset()
    moves = ["0", "1", "0", "1", "0", "1", "0"]
    for m in moves:
        state = game.apply_action(state, m)
    assert game.get_winner(state) == 0


def test_nim_simple_win():
    game = Nim(total=3, max_take=3)
    state = game.reset()
    state = game.apply_action(state, "3")
    assert game.is_terminal(state)
    assert game.get_winner(state) == 0


def test_othello_simple_win():
    game = Othello(size=4)
    state = game.reset()
    moves = [
        "0,1",
        "0,0",
        "1,0",
        "0,2",
        "0,3",
        "2,0",
        "3,0",
        "1,3",
        "2,3",
        "3,1",
        "3,2",
        "3,3",
    ]
    for m in moves:
        state = game.apply_action(state, m)
    assert game.is_terminal(state)
    assert game.get_winner(state) == 1
