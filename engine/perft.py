import time

from .game import Game
from .move import Move


def perft(game: Game, depth: int) -> int:
    if depth == 0:
        return 1

    moves = game.legal_moves

    if depth == 1:
        return len(moves)

    nodes = 0

    for move in moves:
        game.make_move(move)
        nodes += perft(game, depth - 1)
        game.undo_move()

    return nodes


def divide(game: Game, depth: int) -> dict[Move, int]:
    if depth < 1:
        raise ValueError("depth must be at least 1")

    counts: dict[Move, int] = {}

    for move in game.legal_moves:
        game.make_move(move)
        counts[move] = perft(game, depth - 1)
        game.undo_move()

    return counts


def bench(game: Game, max_depth: int) -> list[tuple[int, int, float]]:
    results = []

    for depth in range(1, max_depth + 1):
        start = time.perf_counter()
        nodes = perft(game, depth)
        elapsed = time.perf_counter() - start
        results.append((depth, nodes, elapsed))

    return results


def _format_move(move: Move) -> str:
    marker = "x" if move.is_capture else "-"
    return f"{move.start}{marker}{move.end}"


def _print_divide(game: Game, depth: int) -> None:
    counts = divide(game, depth)
    total = 0

    for move, nodes in sorted(counts.items(), key=lambda item: _format_move(item[0])):
        print(f"{_format_move(move):16} {nodes}")
        total += nodes

    print(f"total: {total}")


def _print_bench(game: Game, max_depth: int) -> None:
    print(f"{'depth':>5} {'nodes':>12} {'time (s)':>10} {'nodes/s':>14}")

    for depth, nodes, elapsed in bench(game, max_depth):
        nps = nodes / elapsed if elapsed > 0 else float("inf")
        print(f"{depth:>5} {nodes:>12} {elapsed:>10.4f} {nps:>14,.0f}")


if __name__ == "__main__":
    import sys

    max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    game = Game()

    if len(sys.argv) > 2 and sys.argv[2] == "divide":
        _print_divide(game, max_depth)
    else:
        _print_bench(game, max_depth)
