from engine.perft import divide, perft


def test_perft_depth_zero(game):
    assert perft(game, 0) == 1


def test_perft_depth_one(game):
    assert perft(game, 1) == len(game.legal_moves)


def test_divide(game):
    result = divide(game, 1)

    assert sum(result.values()) == len(game.legal_moves)