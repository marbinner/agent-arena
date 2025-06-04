from arena.games.word_ladder_duel import WordLadderDuel


def test_word_ladder_duel_path():
    dictionary = ["cold", "cord", "card", "ward", "warm"]
    game = WordLadderDuel("cold", "warm", dictionary)
    state = game.reset()
    moves = ["cord", "card", "ward", "warm"]
    for move in moves:
        state = game.apply_action(state, move)
    assert game.is_terminal(state)
    assert game.get_winner(state) == 1
