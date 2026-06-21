#!/usr/bin/env python3
"""Distill winning lines from a strong MoHex teacher against a weak MoHex."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from benchmark_vs_mohex import DEFAULT_MOHEX, MoHex
from hex_ai import BLUE, EMPTY, RED, has_won, move_to_notation, opponent


ROOT = Path(__file__).resolve().parent


def key(board: list[list[int]], player: int) -> str:
    return f"{player}:" + "".join(str(cell) for row in board for cell in row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mohex", type=Path, default=DEFAULT_MOHEX)
    parser.add_argument("--games", type=int, default=20)
    parser.add_argument("--opponent-playouts", type=int, default=100)
    parser.add_argument("--teacher-playouts", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260621, help="opening and opponent seed")
    parser.add_argument(
        "--opponent-seed", type=int, default=None,
        help="override opponent seed while keeping the opening sample fixed",
    )
    parser.add_argument("--teacher-seed", type=int, default=424242)
    parser.add_argument(
        "--fresh-engine", action="store_true",
        help="start both players with independent derived seeds for every game",
    )
    parser.add_argument("--book", type=Path, default=ROOT / "mohex_book.json")
    args = parser.parse_args()
    opponent_seed = args.seed if args.opponent_seed is None else args.opponent_seed
    if args.games < 2 or args.games % 2:
        parser.error("--games must be a positive even number")

    book = json.loads(args.book.read_text(encoding="utf-8")) if args.book.exists() else {}
    openings = random.Random(args.seed).sample(
        [(row, col) for row in range(11) for col in range(11)], args.games // 2
    )
    weak = None if args.fresh_engine else MoHex(
        args.mohex.resolve(), args.opponent_playouts, seed=opponent_seed
    )
    teacher = None if args.fresh_engine else MoHex(
        args.mohex.resolve(), args.teacher_playouts, seed=args.teacher_seed
    )
    won_lines: list[dict[str, list[int]]] = []
    wins = 0
    try:
        game_number = 0
        for opening in openings:
            for teacher_color in (RED, BLUE):
                game_number += 1
                game_weak = weak or MoHex(
                    args.mohex.resolve(), args.opponent_playouts,
                    seed=opponent_seed + game_number,
                )
                game_teacher = teacher or MoHex(
                    args.mohex.resolve(), args.teacher_playouts,
                    seed=args.teacher_seed + game_number,
                )
                board = [[EMPTY] * 11 for _ in range(11)]
                board[opening[0]][opening[1]] = RED
                game_weak.reset()
                game_teacher.reset()
                game_weak.play(RED, opening)
                game_teacher.play(RED, opening)
                turn = BLUE
                line: dict[str, list[int]] = {}
                plies = 1
                while True:
                    if turn == teacher_color:
                        position = key(board, turn)
                        move = game_teacher.genmove(turn)
                        game_weak.play(turn, move)
                        line[position] = [move[0], move[1]]
                    else:
                        move = game_weak.genmove(turn)
                        game_teacher.play(turn, move)
                    board[move[0]][move[1]] = turn
                    plies += 1
                    flat = [cell for row in board for cell in row]
                    if has_won(flat, 11, turn):
                        won = turn == teacher_color
                        if won:
                            wins += 1
                            won_lines.append(line)
                        print(
                            f"game {game_number:02d}/{args.games}: teacher="
                            f"{'RED' if teacher_color == RED else 'BLUE':4s} "
                            f"opening={move_to_notation(opening):>3s} winner="
                            f"{'TEACHER' if won else 'OPPONENT'} plies={plies}",
                            flush=True,
                        )
                        if weak is None:
                            game_weak.close()
                            game_teacher.close()
                        break
                    turn = opponent(turn)
    finally:
        if weak is not None:
            weak.close()
        if teacher is not None:
            teacher.close()

    added = 0
    for line in won_lines:
        book.update(line)
        added += len(line)
    args.book.write_text(json.dumps(book, separators=(",", ":")), encoding="utf-8")
    print(f"teacher result: {wins}/{args.games} ({wins / args.games:.1%})")
    print(f"merged {added} winning-line positions; book has {len(book)} positions")


if __name__ == "__main__":
    main()
