from engine.board import Board


def test_initial_piece_count():
    board = Board()

    pieces = sum(
        piece is not None
        for row in board.grid
        for piece in row
    )

    assert pieces == 24


def test_move_piece():
    board = Board()

    board.move_piece(5, 0, 4, 1)

    assert board.get_piece(5, 0) is None
    assert board.get_piece(4, 1) is not None


def test_copy():
    board = Board()

    clone = board.copy()

    assert clone is not board
    assert clone.grid != []