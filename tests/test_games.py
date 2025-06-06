from arena.games.connect_four import ConnectFour
from arena.games.nim import Nim
from arena.games.othello import Othello
from arena.games.mancala import Mancala
from arena.games.dots_and_boxes import DotsAndBoxes
from arena.games.quoridor import Quoridor


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
    
def test_mancala_simple_win():
    game = Mancala()
    # board with a single stone for player 0 to move leading to victory
    state = ([0, 0, 0, 0, 0, 1, 10, 0, 0, 0, 0, 0, 0, 7], 0)
    state = game.apply_action(state, "5")
    assert game.is_terminal(state)
    assert game.get_winner(state) == 0

def test_dots_and_boxes_single_box():
    game = DotsAndBoxes(size=1)
    state = game.reset()
    moves = ["0", "2", "1", "3"]
    for m in moves:
        state = game.apply_action(state, m)
    assert game.is_terminal(state)
    assert game.get_winner(state) == 1


def test_quoridor_simple_race():
    game = Quoridor(size=5, walls_per_player=0)
    state = game.reset()
    moves = ["D", "L", "D", "L", "D", "U", "D"]
    for m in moves:
        state = game.apply_action(state, m)
    assert game.is_terminal(state)
    assert game.get_winner(state) == 0

