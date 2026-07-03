import runpy
import sys

import pytest
from helpers import make_board

from engine.constants import BLACK, WHITE
from engine.game import Game
from engine.perft import (
    _format_move,
    _print_bench,
    _print_divide,
    bench,
    divide,
    perft,
)


def test_perft_depth_zero(game):
    assert perft(game, 0) == 1


def test_perft_depth_one(game):
    assert perft(game, 1) == len(game.legal_moves)


def test_perft_depth_two(game):
    assert perft(game, 2) > 0


def test_divide(game):
    result = divide(game, 1)

    assert sum(result.values()) == len(game.legal_moves)


def test_divide_rejects_invalid_depth(game):
    with pytest.raises(ValueError):
        divide(game, 0)


def test_bench(game):
    results = bench(game, 2)

    assert len(results) == 2
    for depth, nodes, elapsed in results:
        assert isinstance(depth, int)
        assert isinstance(nodes, int)
        assert elapsed >= 0


def test_perft_matches_known_position():
    board = make_board(
        {
            (4, 4): (WHITE, 0),
            (3, 3): (BLACK, 0),
        }
    )
    game = Game(board, turn=WHITE)

    assert perft(game, 1) == 1


def test_format_move_simple():
    from engine.move import Move

    simple = Move((5, 0), (4, 1))
    capture = Move((5, 0), (3, 2), captures=((4, 1),))

    assert _format_move(simple) == "(5, 0)-(4, 1)"
    assert _format_move(capture) == "(5, 0)x(3, 2)"


def test_print_divide(game, capsys):
    _print_divide(game, 1)

    captured = capsys.readouterr()
    assert "total:" in captured.out


def test_print_bench(game, capsys):
    _print_bench(game, 2)

    captured = capsys.readouterr()
    assert "depth" in captured.out
    assert "nodes/s" in captured.out


def test_main_block_bench(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["perft.py", "2"])
    sys.modules.pop("engine.perft", None)

    runpy.run_module("engine.perft", run_name="__main__")

    captured = capsys.readouterr()
    assert "depth" in captured.out


def test_main_block_divide(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["perft.py", "2", "divide"])
    sys.modules.pop("engine.perft", None)

    runpy.run_module("engine.perft", run_name="__main__")

    captured = capsys.readouterr()
    assert "total:" in captured.out

