BOARD_SIZE = 8

WHITE = 0
BLACK = 1

MAN = 0
KING = 1

EMPTY = None

DIRECTIONS = {
    WHITE: (
        (-1, -1),
        (-1, 1),
    ),
    BLACK: (
        (1, -1),
        (1, 1),
    ),
}

KING_DIRECTIONS = (
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
)
