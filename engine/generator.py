from .board import Board
from .constants import BOARD_SIZE, DIRECTIONS, KING_DIRECTIONS, WHITE
from .move import Move
from .piece import Piece

in_bounds = Board.in_bounds


def generate_moves(board: Board, color: int) -> list[Move]:
    captures = list(_iter_all_captures(board, color))
    if captures:
        return captures
    return list(_iter_all_simple_moves(board, color))


def generate_piece_moves(board: Board, row: int, col: int) -> list[Move]:
    piece = board.get_piece(row, col)
    if piece is None:
        return []

    captures = list(_walk_captures(board, row, col, piece))
    if captures:
        return captures

    return list(_simple_moves(board.grid, row, col, piece))


def has_legal_moves(board: Board, color: int) -> bool:
    for row, col, piece in board.pieces(color):
        if next(_walk_captures(board, row, col, piece), None) is not None:
            return True
        if next(_simple_moves(board.grid, row, col, piece), None) is not None:
            return True
    return False


def _iter_all_simple_moves(board: Board, color: int):
    grid = board.grid
    for row, col, piece in board.pieces(color):
        yield from _simple_moves(grid, row, col, piece)


def _iter_all_captures(board: Board, color: int):
    for row, col, piece in board.pieces(color):
        yield from _walk_captures(board, row, col, piece)


def _will_promote(piece: Piece, end_row: int) -> bool:
    if piece.is_king:
        return False
    if piece.color == WHITE:
        return end_row == 0
    return end_row == BOARD_SIZE - 1


def _simple_moves(grid: list[list[Piece | None]], row: int, col: int, piece: Piece):
    directions = KING_DIRECTIONS if piece.is_king else DIRECTIONS[piece.color]

    for dr, dc in directions:
        end_row, end_col = row + dr, col + dc
        if in_bounds(end_row, end_col) and grid[end_row][end_col] is None:
            yield Move(
                (row, col),
                (end_row, end_col),
                promoted=_will_promote(piece, end_row),
            )


def _walk_captures(board: Board, start_row: int, start_col: int, piece: Piece):
    yield from _walk(
        board.grid,
        start_row,
        start_col,
        start_row,
        start_col,
        piece,
        piece.is_man,
        [],
    )


def _walk(
    grid: list[list[Piece | None]],
    start_row: int,
    start_col: int,
    row: int,
    col: int,
    piece: Piece,
    was_man: bool,
    captured: list[tuple[int, int]],
):
    extended = False
    directions = KING_DIRECTIONS if piece.is_king else DIRECTIONS[piece.color]

    for dr, dc in directions:
        mid_row, mid_col = row + dr, col + dc
        end_row, end_col = row + 2 * dr, col + 2 * dc

        if not in_bounds(end_row, end_col):
            continue

        mid_piece = grid[mid_row][mid_col]
        if mid_piece is None or mid_piece.color == piece.color:
            continue
        if grid[end_row][end_col] is not None:
            continue

        extended = True
        captured.append((mid_row, mid_col))

        grid[row][col] = None
        grid[mid_row][mid_col] = None

        original_kind = piece.kind
        if _will_promote(piece, end_row):
            piece.promote()

        grid[end_row][end_col] = piece

        yield from _walk(
            grid,
            start_row,
            start_col,
            end_row,
            end_col,
            piece,
            was_man,
            captured,
        )

        grid[end_row][end_col] = None
        piece.kind = original_kind
        grid[row][col] = piece
        grid[mid_row][mid_col] = mid_piece

        captured.pop()

    if not extended and captured:
        yield Move(
            (start_row, start_col),
            (row, col),
            tuple(captured),
            promoted=was_man and piece.is_king,
        )
