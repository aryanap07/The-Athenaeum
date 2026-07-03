from .constants import BLACK, BOARD_SIZE, EMPTY, WHITE
from .piece import Piece


class Board:
    __slots__ = ("grid",)

    def __init__(self) -> None:
        self.grid: list[list[Piece | None]] = [
            [EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)
        ]
        self._setup()

    def _setup(self) -> None:

        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece(BLACK)

        for row in range(5, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece(WHITE)

    def get_piece(self, row: int, col: int) -> Piece | None:
        return self.grid[row][col]

    def set_piece(self, row: int, col: int, piece: Piece | None) -> None:
        self.grid[row][col] = piece

    def remove_piece(self, row: int, col: int) -> None:
        self.grid[row][col] = EMPTY

    def move_piece(
        self,
        start_row: int,
        start_col: int,
        end_row: int,
        end_col: int,
    ) -> None:
        piece = self.grid[start_row][start_col]
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = EMPTY

    @staticmethod
    def in_bounds(row: int, col: int) -> bool:
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def pieces(self, color: int):
        grid = self.grid

        for row in range(BOARD_SIZE):
            grid_row = grid[row]
            for col in range(BOARD_SIZE):
                piece = grid_row[col]
                if piece is not None and piece.color == color:
                    yield row, col, piece

    def copy(self) -> "Board":
        board = Board.__new__(Board)
        board.grid = [
            [piece.copy() if piece else EMPTY for piece in row] for row in self.grid
        ]
        return board

    def __getitem__(self, position: tuple[int, int]) -> Piece | None:
        row, col = position
        return self.grid[row][col]

    def __setitem__(
        self,
        position: tuple[int, int],
        piece: Piece | None,
    ) -> None:
        row, col = position
        self.grid[row][col] = piece

    def __str__(self) -> str:
        rows = []

        for row in self.grid:
            rows.append(
                " ".join("." if piece is None else repr(piece) for piece in row)
            )

        return "\n".join(rows)
