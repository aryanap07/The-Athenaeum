from engine.constants import WHITE
from engine.generator import generate_moves


def test_initial_moves(game):
    moves = generate_moves(game.board, WHITE)

    assert len(moves) > 0


def test_all_moves_are_unique(game):
    moves = generate_moves(game.board, WHITE)

    assert len(moves) == len(set(moves))