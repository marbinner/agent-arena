from arena.games.sudoku_race import SudokuRace


def test_sudoku_race_solution():
    game = SudokuRace()
    state = game.reset()
    moves = [
        "0,1,2",
        "0,2,3",
        "1,0,4",
        "1,1,3",
        "1,2,2",
        "1,3,1",
        "2,0,2",
        "2,1,1",
        "2,2,4",
        "2,3,3",
        "3,1,4",
        "3,2,1",
    ]
    current = 0
    for m in moves:
        state = game.apply_action(state, m)
        current = 1 - current
    assert game.is_terminal(state)
    assert game.get_winner(state) == 1
