from engine.minimax import best_move


def test_best_move(game):
    move, score = best_move(game, 2)

    assert move is not None
    assert isinstance(score, int)