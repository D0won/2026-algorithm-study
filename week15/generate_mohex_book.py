#!/usr/bin/env python3
"""Generate a shallow, reusable opening book from MoHex analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark_vs_mohex import DEFAULT_MOHEX, MoHex
from hex_ai import BLUE, EMPTY, RED


ROOT = Path(__file__).resolve().parent


def key(board: list[list[int]], player: int) -> str:
    return f"{player}:" + "".join(str(cell) for row in board for cell in row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mohex", type=Path, default=DEFAULT_MOHEX)
    parser.add_argument("--playouts", type=int, default=500)
    parser.add_argument("--depth", type=int, default=4, help="analyzed plies after forced RED opening")
    parser.add_argument("--seed", type=int, default=20260622)
    parser.add_argument("--output", type=Path, default=ROOT / "mohex_book.json")
    args = parser.parse_args()
    engine = MoHex(args.mohex.resolve(), args.playouts, seed=args.seed)
    book: dict[str, list[int]] = {}
    try:
        for opening_index in range(121):
            board = [[EMPTY] * 11 for _ in range(11)]
            opening = divmod(opening_index, 11)
            board[opening[0]][opening[1]] = RED
            engine.reset()
            engine.play(RED, opening)
            player = BLUE
            for _ in range(args.depth):
                position = key(board, player)
                move = engine.genmove(player)
                book[position] = [move[0], move[1]]
                board[move[0]][move[1]] = player
                player = 3 - player
            if (opening_index + 1) % 11 == 0:
                print(f"analyzed {opening_index + 1}/121 openings", flush=True)
    finally:
        engine.close()
    args.output.write_text(json.dumps(book, separators=(",", ":")), encoding="utf-8")
    print(f"wrote {len(book)} positions to {args.output}")


if __name__ == "__main__":
    main()
