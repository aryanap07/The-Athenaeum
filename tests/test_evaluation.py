from helpers import make_board

from engine.constants import BLACK, KING, WHITE
from engine.evaluation import WIN_SCORE, evaluate, evaluate_for, evaluate_game
from engine.game import Game


def test_start_position_is_equal(game):
    assert evaluate(game.board) == 0


def test_king_worth_more_than_man():
    man_board = make_board({(4, 4): (WHITE, 0)})
    king_board = make_board({(4, 4): (WHITE, KING)})

    assert evaluate(king_board) > evaluate(man_board)


def test_evaluate_black_king():
    board = make_board({(4, 4): (BLACK, KING)})

    assert evaluate(board) < 0


def test_evaluate_for_white_and_black():
    board = make_board({(4, 4): (WHITE, 0)})

    white_score = evaluate_for(board, WHITE)
    black_score = evaluate_for(board, BLACK)

    assert white_score > 0
    assert black_score == -white_score


def test_evaluate_game_no_winner(game):
    assert evaluate_game(game) == evaluate(game.board)


def test_evaluate_game_white_wins():
    board = make_board({(7, 7): (BLACK, 0)})
    game = Game(board, turn=BLACK)

    assert game.winner == WHITE
    assert evaluate_game(game) == WIN_SCORE


def test_evaluate_game_black_wins():
    board = make_board({(0, 0): (WHITE, 0)})
    game = Game(board, turn=WHITE)

    assert game.winner == BLACK
    assert evaluate_game(game) == -WIN_SCORE