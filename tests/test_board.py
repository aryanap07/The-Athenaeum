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


def test_copy_is_independent():
    board = Board()

    clone = board.copy()
    clone.remove_piece(0, 1)

    assert board.get_piece(0, 1) is not None
    assert clone.get_piece(0, 1) is None


def test_remove_piece():
    board = Board()

    board.remove_piece(0, 1)

    assert board.get_piece(0, 1) is None


def test_set_piece():
    board = Board()

    board.set_piece(3, 3, None)

    assert board.get_piece(3, 3) is None


def test_getitem():
    board = Board()

    assert board[0, 1] is board.grid[0][1]
    assert board[3, 3] is None


def test_setitem():
    board = Board()
    piece = board.get_piece(0, 1)

    board[3, 3] = piece

    assert board.grid[3][3] is piece


def test_in_bounds():
    assert Board.in_bounds(0, 0)
    assert Board.in_bounds(7, 7)
    assert not Board.in_bounds(-1, 0)
    assert not Board.in_bounds(0, 8)


def test_pieces_iterator():
    board = Board()

    white_pieces = list(board.pieces(0))
    black_pieces = list(board.pieces(1))

    assert len(white_pieces) == 12
    assert len(black_pieces) == 12
    for row, col, piece in white_pieces:
        assert board.get_piece(row, col) is piece


def test_str_representation():
    board = Board()

    text = str(board)

    assert isinstance(text, str)
    assert "\n" in text
    assert "." in text