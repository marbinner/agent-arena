from arena.games.checkers import Checkers, CheckersState


def test_checkers_simple_capture_win():
    game = Checkers()
    # custom state with one piece each
    board = [[" "] * 8 for _ in range(8)]
    board[2][1] = "b"
    board[3][2] = "r"
    state = CheckersState(board, 0)
    # black jumps and captures red
    state = game.apply_action(state, "2,1->4,3")
    assert game.is_terminal(state)
    assert game.get_winner(state) == 0
