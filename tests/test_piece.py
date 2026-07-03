from engine.constants import BLACK, KING, MAN, WHITE
from engine.piece import Piece


def test_piece_defaults():
    piece = Piece(WHITE)

    assert piece.color == WHITE
    assert piece.kind == MAN
    assert piece.is_white
    assert piece.is_man


def test_piece_promote():
    piece = Piece(BLACK)

    piece.promote()

    assert piece.kind == KING
    assert piece.is_king


def test_piece_copy():
    piece = Piece(WHITE)

    copy = piece.copy()

    assert copy is not piece
    assert copy == piece


def test_repr():
    assert repr(Piece(WHITE)) == "WM"


def test_is_black():
    piece = Piece(BLACK)

    assert piece.is_black
    assert not piece.is_white


def test_is_king_repr():
    piece = Piece(BLACK, KING)

    assert piece.is_king
    assert not piece.is_man
    assert repr(piece) == "BK"