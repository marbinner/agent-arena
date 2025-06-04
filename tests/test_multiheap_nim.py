from arena.games.multiheap_nim import MultiHeapNim


def test_multiheap_nim_basic_win():
    game = MultiHeapNim(heaps=[1, 2], max_take=2)
    state = game.reset()
    state = game.apply_action(state, "0,1")
    state = game.apply_action(state, "1,1")
    state = game.apply_action(state, "1,1")
    assert game.is_terminal(state)
    assert game.get_winner(state) == 0
