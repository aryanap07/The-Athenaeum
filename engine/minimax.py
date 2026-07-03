import random

from .board import Board
from .constants import BOARD_SIZE, WHITE
from .evaluator import WIN_SCORE, evaluate
from .game import Game
from .move import Move

NEG_INF = -10_000_000
POS_INF = 10_000_000

EXACT = 0
LOWER = 1
UPPER = 2

_rng = random.Random(2024)

_ZOBRIST_PIECE = [
    [
        [[_rng.getrandbits(64) for _ in range(2)] for _ in range(2)]
        for _ in range(BOARD_SIZE)
    ]
    for _ in range(BOARD_SIZE)
]

_ZOBRIST_TURN = [_rng.getrandbits(64) for _ in range(2)]


def _zobrist_key(board: Board, turn: int) -> int:
    key = _ZOBRIST_TURN[turn]
    grid = board.grid

    for row in range(BOARD_SIZE):
        grid_row = grid[row]
        table_row = _ZOBRIST_PIECE[row]

        for col in range(BOARD_SIZE):
            piece = grid_row[col]
            if piece is not None:
                key ^= table_row[col][piece.color][piece.kind]

    return key


def _ordered(moves: tuple[Move, ...]) -> list[Move] | tuple[Move, ...]:
    if len(moves) < 2:
        return moves
    return sorted(
        moves, key=lambda move: (move.promoted, move.jump_count), reverse=True
    )


def _perspective_score(game: Game) -> int:
    score = evaluate(game.board)
    return score if game.turn == WHITE else -score


def best_move(
    game: Game,
    depth: int,
    table: dict | None = None,
) -> tuple[Move | None, int]:
    if depth < 1:
        raise ValueError("depth must be at least 1")

    if table is None:
        table = {}

    moves = game.legal_moves
    if not moves:
        return None, -WIN_SCORE

    alpha = NEG_INF
    beta = POS_INF
    chosen = moves[0]
    best_score = NEG_INF

    for move in _ordered(moves):
        game.make_move(move)
        score = -_negamax(game, depth - 1, -beta, -alpha, table)
        game.undo_move()

        if score > best_score:
            best_score = score
            chosen = move

        if score > alpha:
            alpha = score

    key = _zobrist_key(game.board, game.turn)
    table[key] = (depth, best_score, EXACT, chosen)

    return chosen, best_score


def _negamax(game: Game, depth: int, alpha: int, beta: int, table: dict) -> int:
    if depth == 0:
        return _perspective_score(game)

    key = _zobrist_key(game.board, game.turn)
    entry = table.get(key)
    alpha_orig = alpha

    if entry is not None and entry[0] >= depth:
        entry_depth, entry_score, entry_flag, _ = entry

        if entry_flag == EXACT:
            return entry_score
        if entry_flag == LOWER and entry_score > alpha:
            alpha = entry_score
        elif entry_flag == UPPER and entry_score < beta:
            beta = entry_score

        if alpha >= beta:
            return entry_score

    moves = game.legal_moves
    if not moves:
        return -(WIN_SCORE - depth)

    best = NEG_INF
    best_move_here = moves[0]

    for move in _ordered(moves):
        game.make_move(move)
        score = -_negamax(game, depth - 1, -beta, -alpha, table)
        game.undo_move()

        if score > best:
            best = score
            best_move_here = move

        if best > alpha:
            alpha = best

        if alpha >= beta:
            break

    if best <= alpha_orig:
        flag = UPPER
    elif best >= beta:
        flag = LOWER
    else:
        flag = EXACT

    table[key] = (depth, best, flag, best_move_here)

    return best


def iterative_deepening(
    game: Game,
    max_depth: int,
    table: dict | None = None,
) -> tuple[Move | None, int, dict]:
    if table is None:
        table = {}

    chosen: Move | None = None
    score = -WIN_SCORE

    for depth in range(1, max_depth + 1):
        chosen, score = best_move(game, depth, table)
        if abs(score) >= WIN_SCORE - max_depth:
            break

    return chosen, score, table


def principal_variation(
    game: Game,
    table: dict,
    max_length: int = 20,
) -> list[Move]:
    line: list[Move] = []
    sim = game.copy()

    for _ in range(max_length):
        key = _zobrist_key(sim.board, sim.turn)
        entry = table.get(key)
        if entry is None:
            break

        move = entry[3]
        if move not in sim.moves_from(*move.start):
            break

        sim.make_move(move)
        line.append(move)

    return line
