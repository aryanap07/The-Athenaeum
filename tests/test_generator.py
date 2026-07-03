from helpers import make_board

from engine.constants import BLACK, KING, WHITE
from engine.generator import generate_moves, generate_piece_moves, has_legal_moves


def test_initial_moves(game):
    moves = generate_moves(game.board, WHITE)

    assert len(moves) > 0


def test_all_moves_are_unique(game):
    moves = generate_moves(game.board, WHITE)

    assert len(moves) == len(set(moves))


def test_generate_piece_moves_empty_square():
    board = make_board({})

    assert generate_piece_moves(board, 4, 4) == []


def test_generate_piece_moves_simple():
    board = make_board({(4, 4): (WHITE, 0)})

    moves = generate_piece_moves(board, 4, 4)

    assert len(moves) == 2
    assert all(not move.is_capture for move in moves)


def test_generate_piece_moves_prefers_capture():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
        }
    )

    moves = generate_piece_moves(board, 4, 4)

    assert len(moves) == 1
    assert moves[0].is_capture
    assert moves[0].captures == ((3, 3),)
    assert moves[0].end == (2, 2)


def test_has_legal_moves_true():
    board = make_board({(4, 4): (WHITE, 0)})

    assert has_legal_moves(board, WHITE)


def test_has_legal_moves_false():
    board = make_board({(0, 0): (WHITE, 0)})

    assert not has_legal_moves(board, WHITE)


def test_has_legal_moves_true_via_capture():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
        }
    )

    assert has_legal_moves(board, WHITE)


def test_generate_moves_forces_capture():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
            (5, 1): (WHITE, 0),
        }
    )

    moves = generate_moves(board, WHITE)

    assert all(move.is_capture for move in moves)


def test_king_simple_move_not_promoted():
    board = make_board({(4, 4): (WHITE, KING)})

    moves = generate_piece_moves(board, 4, 4)

    assert len(moves) == 4
    assert all(not move.is_promotion for move in moves)


def test_multi_jump_capture_chain():
    board = make_board(
        {
            (6, 6): (WHITE, 0),
            (5, 5): (BLACK, 0),
            (3, 3): (BLACK, 0),
        }
    )

    moves = generate_piece_moves(board, 6, 6)

    double_jumps = [move for move in moves if move.jump_count == 2]
    assert len(double_jumps) == 1
    move = double_jumps[0]
    assert move.end == (2, 2)
    assert move.captures == ((5, 5), (3, 3))


def test_capture_promotes_man_to_king():
    board = make_board(
        {
            (2, 2): (WHITE, 0),
            (1, 1): (BLACK, 0),
        }
    )

    moves = generate_piece_moves(board, 2, 2)

    assert len(moves) == 1
    assert moves[0].is_promotion
    assert moves[0].end == (0, 0)