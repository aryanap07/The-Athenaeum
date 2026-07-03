from engine.move import Move


def test_simple_move():
    move = Move((5, 0), (4, 1))

    assert not move.is_capture
    assert move.jump_count == 0


def test_capture():
    move = Move(
        (5, 0),
        (1, 4),
        captures=((4, 1), (2, 3)),
    )

    assert move.is_capture
    assert move.jump_count == 2


def test_promotion():
    move = Move(
        (1, 2),
        (0, 3),
        promoted=True,
    )

    assert move.is_promotion