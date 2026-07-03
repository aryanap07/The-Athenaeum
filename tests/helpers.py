from engine.board import Board
from engine.piece import Piece


def make_board(pieces: dict[tuple[int, int], tuple[int, int]]) -> Board:
    """Build an empty board with pieces placed at explicit positions.

    ``pieces`` maps ``(row, col)`` -> ``(color, kind)``.
    """
    board = Board.__new__(Board)
    board.grid = [[None] * 8 for _ in range(8)]
    for (row, col), (color, kind) in pieces.items():
        board.grid[row][col] = Piece(color, kind)
    return board
