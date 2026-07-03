from engine.evaluation import evaluate


def test_start_position_is_equal(game):
    assert evaluate(game.board) == 0