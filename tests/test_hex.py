from arena.games.hex import Hex


def test_hex_left_right_win():
    game = Hex(size=3)
    state = game.reset()
    moves = ["0,0", "1,0", "0,1", "1,1", "0,2"]
    for m in moves:
        state = game.apply_action(state, m)
    assert game.get_winner(state) == 0
