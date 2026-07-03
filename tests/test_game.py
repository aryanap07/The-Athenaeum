def test_make_and_undo(game):
    before = str(game.board)

    move = game.legal_moves[0]

    game.make_move(move)
    game.undo_move()

    assert str(game.board) == before

def test_turn_changes(game):
    turn = game.turn

    game.make_move(game.legal_moves[0])

    assert game.turn != turn