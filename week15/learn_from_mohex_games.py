#!/usr/bin/env python3
"""Add stronger MoHex recommendations for positions where our bot moved."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark_vs_mohex import DEFAULT_MOHEX, MoHex
from hex_ai import BLUE, EMPTY, RED, notation_to_move


ROOT = Path(__file__).resolve().parent


def board_key(board: list[list[int]], player: int) -> str:
    return f"{player}:" + "".join(str(cell) for row in board for cell in row)


def parse_tag(tag: str) -> tuple[int, tuple[int, int]]:
    color, notation = tag.split(":", 1)
    return (RED if color == "R" else BLUE), notation_to_move(notation)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("games", nargs="+", type=Path)
    parser.add_argument("--mohex", type=Path, default=DEFAULT_MOHEX)
    parser.add_argument("--playouts", type=int, default=600)
    parser.add_argument("--seed", type=int, default=20260622)
    parser.add_argument(
        "--overwrite", action="store_true",
        help="replace existing recommendations for positions in these games",
    )
    parser.add_argument("--book", type=Path, default=ROOT / "mohex_book.json")
    args = parser.parse_args()
    book = json.loads(args.book.read_text(encoding="utf-8")) if args.book.exists() else {}
    engine = MoHex(args.mohex.resolve(), args.playouts, seed=args.seed)
    added = 0
    try:
        for path in args.games:
            for line in path.read_text(encoding="utf-8").splitlines():
                game = json.loads(line)
                our_color = int(game["our_color"])
                history: list[tuple[int, tuple[int, int]]] = []
                board = [[EMPTY] * 11 for _ in range(11)]
                for ply, tag in enumerate(game["moves"]):
                    color, actual = parse_tag(tag)
                    position = board_key(board, color)
                    # The first RED stone is fixed randomly by the assignment,
                    # not selected by either player.
                    if color == our_color and ply > 0 and (args.overwrite or position not in book):
                        engine.reset()
                        for past_color, past_move in history:
                            engine.play(past_color, past_move)
                        recommendation = engine.genmove(color)
                        book[position] = [recommendation[0], recommendation[1]]
                        added += 1
                    board[actual[0]][actual[1]] = color
                    history.append((color, actual))
    finally:
        engine.close()
    args.book.write_text(json.dumps(book, separators=(",", ":")), encoding="utf-8")
    print(f"added {added} corrections; book now has {len(book)} positions")


if __name__ == "__main__":
    main()
