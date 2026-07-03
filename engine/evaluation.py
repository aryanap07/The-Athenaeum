from .board import Board
from .constants import BOARD_SIZE, WHITE
from .game import Game

MAN_VALUE = 100
KING_VALUE = 175
ADVANCEMENT_BONUS = 3
CENTER_BONUS = 4
BACK_ROW_BONUS = 8
WIN_SCORE = 1_000_000

CENTER_COLUMNS = frozenset((2, 3, 4, 5))


def _center(row: int, col: int) -> int:
    return CENTER_BONUS if 2 <= row <= 5 and col in CENTER_COLUMNS else 0


WHITE_MAN_TABLE = [
    [
        MAN_VALUE
        + _center(row, col)
        + (BOARD_SIZE - 1 - row) * ADVANCEMENT_BONUS
        + (BACK_ROW_BONUS if row == BOARD_SIZE - 1 else 0)
        for col in range(BOARD_SIZE)
    ]
    for row in range(BOARD_SIZE)
]

BLACK_MAN_TABLE = [
    [
        MAN_VALUE
        + _center(row, col)
        + row * ADVANCEMENT_BONUS
        + (BACK_ROW_BONUS if row == 0 else 0)
        for col in range(BOARD_SIZE)
    ]
    for row in range(BOARD_SIZE)
]

KING_TABLE = [
    [KING_VALUE + _center(row, col) for col in range(BOARD_SIZE)]
    for row in range(BOARD_SIZE)
]


def evaluate(board: Board) -> int:
    score = 0
    grid = board.grid

    for row in range(BOARD_SIZE):
        grid_row = grid[row]
        white_man_row = WHITE_MAN_TABLE[row]
        black_man_row = BLACK_MAN_TABLE[row]
        king_row = KING_TABLE[row]

        for col in range(BOARD_SIZE):
            piece = grid_row[col]
            if piece is None:
                continue

            white = piece.is_white

            if piece.is_king:
                value = king_row[col]
            elif white:
                value = white_man_row[col]
            else:
                value = black_man_row[col]

            score += value if white else -value

    return score


def evaluate_for(board: Board, color: int) -> int:
    score = evaluate(board)
    return score if color == WHITE else -score


def evaluate_game(game: Game) -> int:
    winner = game.winner
    if winner is not None:
        return WIN_SCORE if winner == WHITE else -WIN_SCORE
    return evaluate(game.board)
