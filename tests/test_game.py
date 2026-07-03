import pytest
from helpers import make_board

from engine.board import Board
from engine.constants import BLACK, WHITE
from engine.game import Game
from engine.move import Move


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


def test_make_illegal_move_raises(game):
    fake_move = Move((3, 3), (2, 2))

    with pytest.raises(ValueError):
        game.make_move(fake_move)


def test_make_move_no_piece_raises(game):
    move = game.legal_moves[0]
    # Remove the piece directly, bypassing the move-cache invalidation, so
    # the (stale) cached move is still considered "legal" but the piece is
    # actually gone from the board.
    game.board.set_piece(*move.start, None)

    with pytest.raises(ValueError, match="no piece to move"):
        game.make_move(move)


def test_make_move_no_piece_to_capture_raises():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
        }
    )
    game = Game(board, turn=WHITE)
    move = game.legal_moves[0]
    assert move.is_capture

    # Remove the captured piece without invalidating the move cache.
    game.board.set_piece(*move.captures[0], None)

    with pytest.raises(ValueError, match="no piece to capture"):
        game.make_move(move)


def test_make_move_executes_capture():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
        }
    )
    game = Game(board, turn=WHITE)
    move = game.legal_moves[0]

    game.make_move(move)

    assert game.board.get_piece(3, 3) is None
    assert game.board.get_piece(4, 4) is None
    assert game.board.get_piece(2, 2) is not None


def test_make_move_promotes_piece():
    board = make_board(
        {
            (2, 2): (WHITE, 0),
            (1, 1): (BLACK, 0),
        }
    )
    game = Game(board, turn=WHITE)
    move = game.legal_moves[0]
    assert move.is_promotion

    piece = game.make_move(move)

    assert piece.is_king


def test_undo_move_with_no_history_raises(game):
    with pytest.raises(IndexError):
        game.undo_move()


def test_undo_move_restores_captured_piece():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
        }
    )
    game = Game(board, turn=WHITE)
    move = game.legal_moves[0]

    game.make_move(move)
    game.undo_move()

    assert game.board.get_piece(3, 3) is not None
    assert game.board.get_piece(4, 4) is not None
    assert game.board.get_piece(2, 2) is None
    assert game.turn == WHITE


def test_winner_is_none_when_moves_available(game):
    assert game.winner is None
    assert not game.is_over


def test_winner_set_when_no_moves():
    board = make_board({(0, 0): (WHITE, 0)})
    game = Game(board, turn=WHITE)

    assert game.is_over
    assert game.winner == BLACK


def test_move_count(game):
    assert game.move_count == 0

    game.make_move(game.legal_moves[0])

    assert game.move_count == 1


def test_copy_is_independent(game):
    clone = game.copy()
    clone.make_move(clone.legal_moves[0])

    assert clone.move_count == 1
    assert game.move_count == 0
    assert clone.board is not game.board


def test_reset_restores_default_board(game):
    game.make_move(game.legal_moves[0])

    game.reset()

    assert game.turn == WHITE
    assert game.move_count == 0
    assert len(game.legal_moves) > 0


def test_reset_with_custom_board():
    game = Game()
    custom_board = make_board({(0, 0): (WHITE, 0)})

    game.reset(custom_board, turn=BLACK)

    assert game.board is custom_board
    assert game.turn == BLACK
    assert game.history == []


def test_str_matches_board_str(game):
    assert str(game) == str(game.board)


def test_moves_from_unknown_square(game):
    assert game.moves_from(3, 3) == ()


def test_default_board_created_when_none_given():
    game = Game()

    assert isinstance(game.board, Board)
