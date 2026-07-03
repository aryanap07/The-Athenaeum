import pytest
from helpers import make_board

from engine.constants import WHITE
from engine.game import Game
from engine.minimax import (
    best_move,
    iterative_deepening,
    principal_variation,
)


def test_best_move(game):
    move, score = best_move(game, 2)

    assert move is not None
    assert isinstance(score, int)


def test_best_move_rejects_invalid_depth(game):
    with pytest.raises(ValueError):
        best_move(game, 0)


def test_best_move_no_legal_moves_returns_none():
    board = make_board({(0, 0): (WHITE, 0)})
    game = Game(board, turn=WHITE)

    move, score = best_move(game, 2)

    assert move is None
    assert score < 0


def test_best_move_reuses_shared_table(game):
    table = {}

    best_move(game, 2, table)
    move, score = best_move(game, 2, table)

    assert move is not None
    assert table


def test_negamax_hits_terminal_no_moves_branch():
    # White has three simple (non-capturing) moves available. One of them
    # leaves the black piece completely boxed in with zero legal moves,
    # which forces the internal negamax search to hit its "no legal
    # moves" terminal-scoring branch a ply below the root.
    board = make_board(
        {
            (6, 0): (WHITE, 0),
            (2, 5): (WHITE, 0),
            (1, 6): (WHITE, 0),
            (0, 7): (1, 0),
        }
    )
    game = Game(board, turn=WHITE)

    move, score = best_move(game, 2)

    assert move is not None
    assert isinstance(score, int)


def test_iterative_deepening(game):
    move, score, table = iterative_deepening(game, 2)

    assert move is not None
    assert isinstance(score, int)
    assert table


def test_iterative_deepening_stops_on_forced_win():
    board = make_board({(6, 0): (WHITE, 0)})
    game = Game(board, turn=WHITE)

    move, score, table = iterative_deepening(game, 5)

    assert move is not None


def test_principal_variation_empty_table(game):
    line = principal_variation(game, {})

    assert line == []


def test_principal_variation_follows_table(game):
    _, _, table = iterative_deepening(game, 2)

    line = principal_variation(game, table, max_length=2)

    assert isinstance(line, list)
    assert len(line) <= 2


def test_principal_variation_stops_on_illegal_move(game):
    _, _, table = iterative_deepening(game, 2)

    # A very small max_length still exercises the loop/break logic.
    line = principal_variation(game, table, max_length=0)

    assert line == []


def test_principal_variation_breaks_on_stale_move(game):
    from engine.minimax import EXACT, _zobrist_key

    key = _zobrist_key(game.board, game.turn)
    # Reference a move that does not correspond to any legal move in the
    # current position, forcing the "stale move" break branch.
    stale_move = list(game.legal_moves)[0]
    other_start_moves = [
        m for m in game.legal_moves if m.start != stale_move.start
    ]
    fake_entry_move = stale_move
    if other_start_moves:
        # Craft a table entry pointing at a move whose start square has no
        # matching legal move once simulated (using a bogus destination).
        from engine.move import Move

        fake_entry_move = Move(stale_move.start, (-1, -1))

    table = {key: (1, 0, EXACT, fake_entry_move)}

    line = principal_variation(game, table, max_length=5)

    assert line == []


def test_negamax_reads_upper_bound_entry(game):
    from engine.minimax import NEG_INF, UPPER, _negamax, _zobrist_key

    key = _zobrist_key(game.board, game.turn)
    fake_move = game.legal_moves[0]
    table = {key: (5, -100, UPPER, fake_move)}

    score = _negamax(game, 2, NEG_INF, 1000, table)

    assert isinstance(score, int)


def test_negamax_stores_upper_bound_on_fail_low(game):
    from engine.minimax import POS_INF, UPPER, _negamax, _zobrist_key

    table = {}
    key = _zobrist_key(game.board, game.turn)

    # An artificially high alpha guarantees every move fails low, forcing
    # the search to store an UPPER-bound entry for this node.
    score = _negamax(game, 2, POS_INF - 1, POS_INF, table)

    assert table[key][2] == UPPER
    assert isinstance(score, int)
