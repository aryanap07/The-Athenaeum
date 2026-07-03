from dataclasses import dataclass

from .constants import BLACK, KING, MAN, WHITE


@dataclass(slots=True)
class Piece:
    color: int
    kind: int = MAN

    @property
    def is_white(self) -> bool:
        return self.color == WHITE

    @property
    def is_black(self) -> bool:
        return self.color == BLACK

    @property
    def is_man(self) -> bool:
        return self.kind == MAN

    @property
    def is_king(self) -> bool:
        return self.kind == KING

    def promote(self) -> None:
        self.kind = KING

    def copy(self) -> "Piece":
        return Piece(self.color, self.kind)

    def __repr__(self) -> str:
        color = "W" if self.is_white else "B"
        piece = "K" if self.is_king else "M"
        return f"{color}{piece}"
