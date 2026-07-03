from dataclasses import dataclass

from .board import Board
from .constants import WHITE
from .generator import generate_moves
from .move import Move
from .piece import Piece


@dataclass(slots=True)
class Undo:
    move: Move
    piece: Piece
    captured: tuple[Piece, ...]
    was_king: bool
    turn: int


class Game:
    __slots__ = (
        "board",
        "turn",
        "history",
        "_moves",
        "_moves_by_start",
        "_moves_dirty",
    )

    def __init__(self, board: Board | None = None, turn: int = WHITE) -> None:
        self.board = board if board is not None else Board()
        self.turn = turn
        self.history: list[Undo] = []
        self._moves: tuple[Move, ...] = ()
        self._moves_by_start: dict[tuple[int, int], tuple[Move, ...]] = {}
        self._moves_dirty = True

    def _refresh_moves(self) -> None:
        moves = generate_moves(self.board, self.turn)
        by_start: dict[tuple[int, int], list[Move]] = {}

        for move in moves:
            by_start.setdefault(move.start, []).append(move)

        self._moves = tuple(moves)
        self._moves_by_start = {
            start: tuple(group) for start, group in by_start.items()
        }
        self._moves_dirty = False

    @property
    def legal_moves(self) -> tuple[Move, ...]:
        if self._moves_dirty:
            self._refresh_moves()
        return self._moves

    def moves_from(self, row: int, col: int) -> tuple[Move, ...]:
        if self._moves_dirty:
            self._refresh_moves()
        return self._moves_by_start.get((row, col), ())

    def is_legal(self, move: Move) -> bool:
        return move in self.moves_from(*move.start)

    def make_move(self, move: Move) -> Piece:
        if not self.is_legal(move):
            raise ValueError(f"illegal move: {move}")

        board = self.board
        get_piece = board.get_piece
        set_piece = board.set_piece

        start_row, start_col = move.start
        end_row, end_col = move.end

        original_piece = get_piece(start_row, start_col)
        captured_pieces = tuple(get_piece(row, col) for row, col in move.captures)

        set_piece(start_row, start_col, None)
        for row, col in move.captures:
            set_piece(row, col, None)

        piece = original_piece.copy()
        if move.promoted:
            piece.promote()
        set_piece(end_row, end_col, piece)

        self.history.append(
            Undo(
                move, original_piece, captured_pieces, original_piece.is_king, self.turn
            )
        )

        self.turn ^= 1
        self._moves_dirty = True

        return piece

    def undo_move(self) -> Move:
        if not self.history:
            raise IndexError("no moves to undo")

        undo = self.history.pop()
        set_piece = self.board.set_piece

        start_row, start_col = undo.move.start
        end_row, end_col = undo.move.end

        set_piece(end_row, end_col, None)
        set_piece(start_row, start_col, undo.piece)

        for (row, col), captured_piece in zip(
            undo.move.captures, undo.captured, strict=False
        ):
            set_piece(row, col, captured_piece)

        self.turn = undo.turn
        self._moves_dirty = True

        return undo.move

    @property
    def winner(self) -> int | None:
        if self.legal_moves:
            return None
        return self.turn ^ 1

    @property
    def is_over(self) -> bool:
        return not self.legal_moves

    @property
    def move_count(self) -> int:
        return len(self.history)

    def copy(self) -> "Game":
        game = Game.__new__(Game)
        game.board = self.board.copy()
        game.turn = self.turn
        game.history = list(self.history)
        game._moves = self._moves
        game._moves_by_start = dict(self._moves_by_start)
        game._moves_dirty = self._moves_dirty
        return game

    def reset(self, board: Board | None = None, turn: int = WHITE) -> None:
        self.board = board if board is not None else Board()
        self.turn = turn
        self.history.clear()
        self._moves_dirty = True

    def __str__(self) -> str:
        return str(self.board)
